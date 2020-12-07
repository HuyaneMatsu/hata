# -*- coding: utf-8 -*-
import ssl, selectors
from collections import deque
import socket as module_socket

from .futures import Future

def _create_transport_context(server_side, server_hostname):
    if server_side:
        raise ValueError('Server side SSL needs a valid SSLContext')
    
    # Client side may pass ssl=True to use a default
    # context; in that case the ssl_context passed is None.
    # The default is secure for client connections.
    ssl_context = ssl.create_default_context()
    if (server_hostname is None) or (not server_hostname):
        ssl_context.check_hostname = False
    
    return ssl_context

if hasattr(module_socket, 'TCP_NODELAY'):
    def _set_nodelay(sock):
        if (sock.family in (module_socket.AF_INET, module_socket.AF_INET6) and
            sock.type == module_socket.SOCK_STREAM and sock.proto == module_socket.IPPROTO_TCP):
            sock.setsockopt(module_socket.IPPROTO_TCP, module_socket.TCP_NODELAY, 1)
else:
    def _set_nodelay(sock):
        pass

MAX_SIZE = 262144

UNWRAPPED = 'UNWRAPPED'
DO_HANDSHAKE = 'DO_HANDSHAKE'
WRAPPED = 'WRAPPED'
SHUTDOWN = 'SHUTDOWN'

class _SSLPipe(object):
    __slots__=('_handshake_cb', '_incoming', '_outgoing', '_shutdown_cb', 'context', 'need_ssldata', 'server_hostname',
        'server_side', 'ssl_object', 'state',)
    
    def __init__(self, context, server_side, server_hostname=None):
        self.context = context
        self.server_side = server_side
        self.server_hostname = server_hostname
        self.state = UNWRAPPED
        self._incoming = ssl.MemoryBIO()
        self._outgoing = ssl.MemoryBIO()
        self.ssl_object = None
        self.need_ssldata = False
        self._handshake_cb = None
        self._shutdown_cb = None
    
    
    @property
    def wrapped(self):
        return self.state is WRAPPED
    
    def do_handshake(self, callback=None):
        if self.state is not UNWRAPPED:
            raise RuntimeError('handshake in progress or completed')
        self.ssl_object = self.context.wrap_bio(self._incoming, self._outgoing, server_side=self.server_side,
            server_hostname=self.server_hostname)
        
        self.state = DO_HANDSHAKE
        self._handshake_cb=callback
        ssldata, _ = self.feed_ssldata(b'', only_handshake=True)
        
        return ssldata
    
    def shutdown(self, callback=None):
        state = self.state
        if state is UNWRAPPED:
            raise RuntimeError('no security layer present')
        if state is SHUTDOWN:
            raise RuntimeError('shutdown in progress')
        
        self.state = SHUTDOWN
        self._shutdown_cb = callback
        ssldata, offset = self.feed_ssldata(b'')
        return ssldata
    
    def feed_eof(self):
        self._incoming.write_eof()
        self.feed_ssldata(b'') #return is ignored
    
    def feed_ssldata(self, data, only_handshake=False):
        if self.state is UNWRAPPED:
            # If unwrapped, pass plaintext data straight through.
            if data:
                appdata = [data]
            else:
                appdata = []
            return [], appdata
    
        self.need_ssldata = False
        if data:
            self._incoming.write(data)
        
        ssldata = []
        appdata = []
        try:
            state = self.state
            if state is DO_HANDSHAKE:
                # Call do_handshake() until it doesn't raise anymore.
                self.ssl_object.do_handshake()
                self.state = state = WRAPPED
                
                handshake_cb = self._handshake_cb
                if (handshake_cb is not None):
                    handshake_cb(None)
                
                if only_handshake:
                    return ssldata, appdata
                # Handshake done: execute the wrapped block
            
            if state is WRAPPED:
                # Main state: read data from SSL until close_notify
                while True:
                    chunk = self.ssl_object.read(MAX_SIZE)
                    appdata.append(chunk)
                    if not chunk:  # close_notify
                        break
            
            elif state is SHUTDOWN:
                # Call shutdown() until it doesn't raise anymore.
                self.ssl_object.unwrap()
                self.ssl_object = None
                self.state = UNWRAPPED
                
                shutdown_cb = self._shutdown_cb
                if (shutdown_cb is not None):
                    shutdown_cb()
            
            elif state is UNWRAPPED:
                # Drain possible plaintext data after close_notify.
                appdata.append(self._incoming.read())
        
        except (ssl.SSLError, ssl.CertificateError) as err:
            err_number = getattr(err, 'errno', None)
            if err_number not in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE, ssl.SSL_ERROR_SYSCALL):
                if self.state is DO_HANDSHAKE:
                    handshake_cb = self._handshake_cb
                    if (handshake_cb is not None):
                        handshake_cb(err)
                raise
            
            self.need_ssldata = (err_number == ssl.SSL_ERROR_WANT_READ)

        # Check for record level data that needs to be sent back.
        # Happens for the initial handshake and renegotiations.
        if self._outgoing.pending:
            ssldata.append(self._outgoing.read())
        return ssldata, appdata

    def feed_appdata(self, data, offset):
        ssldata = []
        if self.state is UNWRAPPED:
            # pass through data in unwrapped mode
            if offset < len(data):
                ssldata.append(memoryview(data)[offset:])
            oofset = len(data)
        else:
            view = memoryview(data)
            while True:
                self.need_ssldata = False
                try:
                    if offset < len(view):
                        offset += self.ssl_object.write(view[offset:])
                except ssl.SSLError as err:
                    # It is not allowed to call write() after unwrap() until the close_notify is acknowledged. We return
                    # the condition to the caller as a short write.
                    if err.reason == 'PROTOCOL_IS_SHUTDOWN':
                        err.errno = ssl.SSL_ERROR_WANT_READ
                        need_ssldata = True
                    else:
                        errno = err.errno
                        if errno == ssl.SSL_ERROR_WANT_READ:
                            need_ssldata = True
                        elif errno == ssl.SSL_ERROR_WANT_WRITE or errno == ssl.SSL_ERROR_SYSCALL:
                            need_ssldata = False
                        else:
                            raise
                    
                    self.need_ssldata = need_ssldata
    
                # See if there's any record level data back for us.
                if self._outgoing.pending:
                    ssldata.append(self._outgoing.read())
                
                if offset == len(view) or self.need_ssldata:
                    break
        
        return ssldata, offset

class _SSLProtocolTransport(object):
    """
    Asynchronous ssl protocol's read-write  transport implementation.
    
    Attributes
    ----------
    app_protocol : `Any`
        Asynchronous protocol implementation.
    closed : `bool`
        Whether the ssl protocol transport is closed.
    ssl_protocol : ``SSLProtocol``
        The respective ssl protocol, what's `.app_protocol` is the ``_SSLProtocolTransport`` instance.
    """
    __slots__ = ('app_protocol', 'closed', 'ssl_protocol',)
    def __init__(self, ssl_protocol, app_protocol):
        """
        Creates a  new ``_SSLProtocolTransport`` instance.
        
        Parameters
        ----------
        ssl_protocol : ``SSLProtocol``
            The respective ssl protocol, what's `.app_protocol` is the ``_SSLProtocolTransport`` instance.
        app_protocol : `Any`
            Asynchronous protocol implementation.
        """
        self.ssl_protocol = ssl_protocol
        self.app_protocol = app_protocol
        self.closed = False
    
    def __repr__(self):
        """Returns the ssl protocol transport's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' ',
                ]
        
        if self.closed:
            result.append('closed')
            add_comma = True
        else:
            add_comma = False
        
        ssl_protocol = self.ssl_protocol
        if (ssl_protocol is not None):
            if add_comma:
                result.append(', ')
            else:
                add_comma = True
            
            result.append('ssl_protocol=')
            result.append(ssl_protocol.__class__.__name__)
        
        app_protocol = self.ssl_protocol
        if (app_protocol is not None):
            if add_comma:
                result.append(', ')
            
            result.append('app_protocol=')
            result.append(app_protocol.__class__.__name__)
        
        result.append('>')
        
        return ''.join(result)
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be macthed. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
        return self.ssl_protocol.get_extra_info(name, default)
    
    def set_protocol(self, protocol):
        """
        Sets a new protocol to the transport.
        
        Parameters
        ----------
        protocol : `Any`
            Asynchronous protocol implementation.
        """
        self.app_protocol = protocol
        self.ssl_protocol.app_protocol = protocol
     
    def get_protocol(self):
        """
        Gets the ssl protocol transport actual protocol.
        
        Returns
        -------
        protocol : `Any`
            Asynchronous protocol implementation.
        """
        return self.app_protocol
    
    def is_closing(self):
        """
        Returns whether the ssl protoco ltransport is closing.
        
        Returns
        -------
        is_closing : `bool`
        """
        return self.closed
    
    def close(self):
        """
        Starts the shutdown process of the ssl protocol transport.
        """
        self.closed = True
        self.ssl_protocol._start_shutdown()

    def __del__(self):
        """
        Closes the ssl protocol transport ifn ot yet clsoed.
        """
        if not self.closed:
            self.close()

    def pause_reading(self):
        """
        Pause the receiving end.
        
        No data will be passed to the respective protocol's ``.data_received`` method until ``.resume_reading`` is
        called.
        """
        transport = self.ssl_protocol.transport
        if (transport is not None):
            transport.pause_reading()

    def resume_reading(self):
        """
        Resume the receiving end.
        
        Data received will once again be passed to the respective protocol's ``.data_received`` method.
        """
        transport = self.ssl_protocol.transport
        if (transport is not None):
            transport.resume_reading()
    
    def set_write_buffer_limits(self, low=None, high=None):
        """
        Set the high- and low-water limits for write flow control.
        
        These two values control when to call the protocol's ``.pause_writing`` and ``.resume_writing`` methods. If
        specified, the low-water limit must be less than or equal to the high-water limit. Neither value can be
        negative. The defaults are implementation-specific. If only the high-water limit is given, the low-water limit
        defaults to an implementation-specific value less than or equal to the high-water limit. Setting high to zero
        forces low to zero as well, and causes ``.pause_writing`` to be called whenever the buffer becomes non-empty.
        Setting low to zero causes ``.resume_writing`` to be called only once the buffer is empty. Use of zero for
        either limit is generally sub-optimal as it reduces opportunities for doing I/O and computation concurrently.
        
        Parameters
        ----------
        high : `None` or `int`, Optional
            High limit to stop reading if reached.
        low : `None` or `int`, Optional
            Low limit to start reading if reached.
        
        Raises
        ------
        ValueError
            If `low` is lower than `0` or if `low` is higher than `high`.
        """
        transport = self.ssl_protocol.transport
        if (transport is not None):
            transport.set_write_buffer_limits(high, low)
        
    def get_write_buffer_size(self):
        """
        Return the current size of the write buffer.
        
        Returns
        -------
        get_write_buffer_size : `int`
        """
        transport = self.ssl_protocol.transport
        if transport is None:
            write_buffer_size = 0
        else:
            write_buffer_size = transport.get_write_buffer_size()
        
        return write_buffer_size
    
    def write(self, data):
        """
        Write the given `data` to the transport.
        
        Do not blocks, but queues up the data instead to be sent as can.
        
        Parameters
        ----------
        data : `bytes-like`
            The data to send.
        
        Raises
        ------
        TypeError
            If `data` was not given as `bytes-like`.
        """
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f'`data` expecting a `bytes-like`, got {data.__class__.__name__}.')
        
        if data:
            self.ssl_protocol._write_appdata(data)
    
    def writelines(self, list_of_data):
        """
        Writes an `iterable` of `bytes-like` to the transport.
        
        Parameters
        ----------
        list_of_data : `iterable` of `bytes-like`
            An iterable of data to send.
        
        Raises
        ------
        TypeError
            If `list_of_data` was not given as `iterable` of `bytes-like`.
        """
        self.write(b''.join(list_of_data))
    
    def can_write_eof(self):
        """
        Return whether the transport supports ``.write_eof``.
        
        Returns
        -------
        can_write_eof : `bool`
            ``_SSLProtocolTransport`` instances always return `False`.
        """
        return False
    
    def abort(self):
        """
        Close the transport immediately.
        
        Buffered data will be lost and no more data will be received.
        
        The respective protocol's `.connection_lost` will be eventually called with `None`.
        """
        self.ssl_protocol._abort()


class SSLProtocol(object):
    """
    Asynchornous SSL protocol implementation on top of a `socket`. Uses `ssl.MemoryBIO` instances for incoming and
    outgoing data.
    
    Attributes
    ----------
    _call_connection_made : `bool`
        Whether the the ``.app_protocol``'s `.connection_made` should be called when handshake is completed.
    _connection_made_waiter : `None` or ``Future``
        A waiter future, what's result is set when connection is made, aka handshae is completed, or if when the
        connection is lost, depending which happens first.
        
        After the future's result or exception is set, the attribute is set as `None`.
    _extra : `dict` of (`str`, `Any`) items, Optional
        Optional transport informations.
    _in_handshake : `bool`
        Whether the ssl transport is in handshaking.
    _in_shutdown : `bool`
        Whether the ssl protocol is shut or shutting shutting down.
    _session_established : `bool`
        Whether the session is established. Is set after handshake and is set back to `False` when the connection is
        lost.
    _ssl_context : `ssl.SSLContext`
        The connection's ssl type.
    _write_backlog : `deque` of `tuple` (`bytes-like`, `int`)
        Ensured data queued up to be written. Each element contains a the data to write and an offset till write from.
    app_protocol : `Any`
        Asynchronous protcol implemnetation.
    app_transport : ``_SSLProtocolTransport``
        Asynchronous ssl protocol's read-write  transport implementation.
    loop : ``eventThread``
        The respective eventloop of the ssl protocol.
    server_hostname : `None` or `str`
        The ssl protocol's server hostname if applicable.
    server_side : `bool`
        Whether the ssl protocol is server side.
    sslpipe : `None` or ``_SSLPipe``
        Ssl pipe set meanwhile the protocol is connected to feed the ssl data to.
    transport : `None` or `Any`
        Asynchronous transport implementation.
    """
    __slots__ = ('_call_connection_made', '_connection_made_waiter', '_extra', '_handshake_start_time', '_in_handshake',
        '_in_shutdown', '_session_established', '_ssl_context', '_write_backlog', 'app_protocol', 'app_transport',
        'loop', 'server_hostname', 'server_side', 'sslpipe', 'transport',)
    
    def __new__(cls, loop, app_protocol, ssl_context, connection_made_waiter, server_side=False, server_hostname=None,
            call_connection_made=True):
        
        if ssl_context is None:
            ssl_context = _create_transport_context(server_side, server_hostname)
        
        self = object.__new__(cls)
        
        self.server_side = server_side
        if (server_hostname is not None) and server_side:
            server_hostname = None
        
        self.server_hostname = server_hostname
        
        self._ssl_context = ssl_context
        # SSL-specific extra info. More info are set when the handshake
        # completes.
        self._extra = {'sslcontext': ssl_context}

        # App data write buffering
        self._write_backlog = deque()
        
        self._connection_made_waiter = connection_made_waiter
        self.loop = loop
        self.app_protocol = app_protocol
        self.app_transport = _SSLProtocolTransport(self, app_protocol)
        # _SSLPipe instance (None until the connection is made)
        self.sslpipe = None
        self._session_established = False
        self._in_handshake = False
        self._in_shutdown = False
        # transport, ex: SelectorSocketTransport
        self.transport = None
        self._call_connection_made = call_connection_made
        
        return self
    
    def _wakeup_connection_made_waiter(self, exception=None):
        connection_made_waiter = self._connection_made_waiter
        if (connection_made_waiter is not None):
            self._connection_made_waiter = None
            if connection_made_waiter.pending():
                if exception is None:
                    connection_made_waiter.set_result(None)
                else:
                    connection_made_waiter.set_exception(exception)
    
    def connection_made(self, transport):
        self.transport = transport
        self.sslpipe = _SSLPipe(self._ssl_context, self.server_side, self.server_hostname)
        self._start_handshake()
    
    def connection_lost(self, exception):
        if self._session_established:
            self._session_established = False
            app_protocol = self.app_protocol
            self.loop.call_soon(app_protocol.__class__.connection_lost, app_protocol, exception)
        self.transport = None
        self.app_transport = None
        self._wakeup_connection_made_waiter(exception)
    
    def pause_writing(self):
        self.app_protocol.pause_writing()
    
    def resume_writing(self):
        self.app_protocol.resume_writing()
    
    def data_received(self, data):
        try:
            ssldata, appdata = self.sslpipe.feed_ssldata(data)
        except ssl.SSLError:
            self._abort()
            return
        
        for chunk in ssldata:
            self.transport.write(chunk)
        
        for chunk in appdata:
            if chunk:
                self.app_protocol.data_received(chunk)
                continue
            self._start_shutdown()
            break
    
    def eof_received(self):
        try:
            self._wakeup_connection_made_waiter(ConnectionResetError)
            if not self._in_handshake:
                #has no effect whatever it returns when we use ssl
                self.app_protocol.eof_received()
        finally:
            self.transport.close()

    def get_extra_info(self, name, default=None):
        try:
            extra_info = self._extra[name]
        except KeyError:
            transport = self.transport
            if transport is not None:
                extra_info = transport.get_extra_info(name, default)
            else:
                extra_info = default
        
        return extra_info
    
    def _start_shutdown(self):
        if self._in_shutdown:
            return
        self._in_shutdown = True
        self._write_appdata(b'')
    
    def _write_appdata(self, data):
        self._write_backlog.append((data, 0))
        self._process_write_backlog()
    
    def _start_handshake(self):
        self._handshake_start_time = None
        self._in_handshake = True
        #(b'',1) is a special value in _process_write_backlog() to do the SSL handshake
        self._write_backlog.append((b'', 1))
        self.loop.call_soon(self._process_write_backlog)
    
    def _on_handshake_complete(self, handshake_exc):
        self._in_handshake = False
        sslobj = self.sslpipe.ssl_object
        
        try:
            if (handshake_exc is not None):
                raise handshake_exc
            
            peercert = sslobj.getpeercert()
        except BaseException as err:
            self.transport.close()
            if isinstance(err, Exception):
                self._wakeup_connection_made_waiter(err)
                return
            raise
        
        
        # Add extra info that becomes available after handshake.
        extra = self._extra
        extra['peercert'] = peercert
        extra['cipher'] = sslobj.cipher()
        extra['compression']= sslobj.compression()
        extra['ssl_object'] = sslobj

        if self._call_connection_made:
            self.app_protocol.connection_made(self.app_transport)
            
        self._wakeup_connection_made_waiter()
        self._session_established = True
        # In case transport.write() was already called. Don't call
        # immediately _process_write_backlog(), but schedule it:
        # _on_handshake_complete() can be called indirectly from
        # _process_write_backlog(), and _process_write_backlog() is not
        # reentrant.
        self.loop.call_soon(self._process_write_backlog)

    def _process_write_backlog(self):
        # Try to make progress on the write backlog.
        transport = self.transport
        if transport is None:
            return
        
        try:
            for i in range(len(self._write_backlog)):
                data, offset = self._write_backlog[0]
                if data:
                    ssldata, offset = self.sslpipe.feed_appdata(data, offset)
                elif offset:
                    ssldata=self.sslpipe.do_handshake(self._on_handshake_complete)
                    offset = 1
                else:
                    ssldata = self.sslpipe.shutdown(self._finalize)
                    offset = 1

                for chunk in ssldata:
                    transport.write(chunk)

                if offset < len(data):
                    self._write_backlog[0] = (data, offset)
                    # A short write means that a write is blocked on a read
                    # We need to enable reading if it is paused!
                    assert self.sslpipe.need_ssldata
                    if transport._paused:
                        transport.resume_reading()
                    break
                
                # An entire chunk from the backlog was processed. We can
                # delete it and reduce the outstanding buffer size.
                del self._write_backlog[0]
        except BaseException as err:
            if self._in_handshake:
                self._on_handshake_complete(err)
            else:
                self._fatal_error(err, 'Fatal error on SSL transport')
            if not isinstance(err, Exception):
                # BaseException
                raise
    
    def _fatal_error(self, exception,message='Fatal error on transport'):
        # Should be called from exception handler only.
        if not isinstance(exception, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occured\n',
                repr(self),
                '\n',
                    ])
        
        transport = self.transport
        if (transport is not None):
            transport._force_close(exception)

    def _finalize(self):
        transport = self.transport
        if (transport is not None):
            transport.close()

    def _abort(self):
        transport = self.transport
        if (transport is not None):
            try:
                transport.abort()
            finally:
                self._finalize()


class _SelectorSocketTransport(object):
    __slots__ = ('_extra', 'loop', 'protocol', '_low_water', '_high_water', '_protocol_paused', 'socket', '_sock_fd',
        '_protocol_connected', 'server', 'buffer', '_conn_lost', 'closing', 'eof', 'paused',)
    
    def __init__(self, loop, sock, protocol, waiter=None, extra=None, server=None):
        
        if extra is None:
            extra = {}
        
        self._extra = extra
        self.loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()
        
        extra['socket'] = sock
        
        try:
            sockname = sock.getsockname()
        except OSError:
            sockname = None
        extra['sockname'] = sockname
        
        if 'peername' not in extra:
            try:
                peername = sock.getpeername()
            except module_socket.error:
                peername = None
            extra['peername'] = peername
        
        self.socket = sock
        self._sock_fd = sock.fileno()
        
        self.protocol = protocol
        self._protocol_connected = True
        
        self.server = server
        self.buffer = bytearray()
        self._conn_lost = 0  # Set when call to connection_lost scheduled.
        self.closing = False  # Set when close() called.
        if server is not None:
            server._attach()
        
        self.eof = False
        self.paused = False
        
        # Disable the Nagle algorithm -- small writes will be sent without waiting for the TCP ACK.  This generally
        # decreases the latency (in some cases significantly.)
        _set_nodelay(sock)
        
        loop.call_soon(protocol.connection_made, self)
        
        #only start reading when connection_made() has been called
        loop.call_soon(loop.add_reader, self._sock_fd, self._read_ready)
        if (waiter is not None):
            # only wake up the waiter when connection_made() has been called
            loop.call_soon(Future.set_result_if_pending, waiter, None)
    
    def __del__(self):
        socket = self.socket
        if socket is not None:
            socket.close()
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.socket is None:
            result.append(' closed')
        elif self.closing:
            result.append(' closing')
        
        result.append(' fd=')
        result.append(repr(self._sock_fd))
        
        loop = self.loop
        #is the transport open?
        if (loop is not None) and loop.running:
        
            try:
                key = loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling = 0
            else:
                polling = key.events&selectors.EVENT_READ
            
            result.append(' read=')
            if polling:
                state = 'polling'
            else:
                state = 'idle'
            result.append(state)

            try:
                key = loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling = 0
            else:
                polling = key.events&selectors.EVENT_WRITE

            result.append(' write=<')
            if polling:
                state = 'polling'
            else:
                state = 'idle'
            result.append(state)

            result.append(', bufsize=')
            
            bufsize = self.get_write_buffer_size()
            result.append(str(bufsize))
            result.append('>')
        
        result.append('>')
        
        return ''.join(result)
    
    def writelines(self, list_of_data):
        self.write(b''.join(list_of_data))
    
    def get_extra_info(self, name, default=None):
        return self._extra.get(name, default)
    
    def _maybe_pause_protocol(self):
        size = self.get_write_buffer_size()
        if size <= self._high_water:
            return
        
        if self._protocol_paused:
            return
        
        self._protocol_paused = True
        try:
            self.protocol.pause_writing()
        except Exception as err:
            self.loop.render_exc_async(err, [
                'Exception occured at:\n',
                repr(self),
                '._maybe_pause_protocol\n',
                    ])
    
    def _maybe_resume_protocol(self):
        if (not self._protocol_paused) or (self.get_write_buffer_size() > self._low_water):
            return
        self._protocol_paused = False
        try:
            self.protocol.resume_writing()
        except Exception as err:
            self.loop.render_exc_async(err, [
                'Exception occured at:\n',
                repr(self),
                '._maybe_resume_protocol\n',
                    ])
    
    def get_write_buffer_limits(self):
        return self._low_water, self._high_water
    
    def _set_write_buffer_limits(self, high=None, low=None):
        if high is None:
            if low is None:
                high = 65536
            else:
                high = low<<2
        
        if low is None:
            low = high>>2
        
        if not high >= low >= 0:
            raise ValueError(f'`high` ({high}) must be `>= low` ({low}) must be `>= 0`.')
        
        self._high_water = high
        self._low_water = low

    def set_write_buffer_limits(self, high=None, low=None):
        self._set_write_buffer_limits(high=high, low=low)
        self._maybe_pause_protocol()
    
    def abort(self):
        self._force_close(None)
    
    def set_protocol(self, protocol):
        self.protocol = protocol
    
    def get_protocol(self):
        return self.protocol
    
    def is_closing(self):
        return self.closing
    
    def close(self):
        if self.closing:
            return
        
        self.closing = True
        self.loop.remove_reader(self._sock_fd)
        if not self.buffer:
            self._conn_lost += 1
            self.loop.remove_writer(self._sock_fd)
            self.loop.call_soon(self._call_connection_lost, None)
    
    def _fatal_error(self, exception, message='Fatal error on transport'):
        if not isinstance(exception, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occured\n',
                repr(self),
                '\n',
                    ])
        
        self._force_close(exception)
    
    def _force_close(self, exception):
        if self._conn_lost:
            return
        
        if self.buffer:
            self.buffer.clear()
            self.loop.remove_writer(self._sock_fd)
        
        if not self.closing:
            self.closing = True
            self.loop.remove_reader(self._sock_fd)
        
        self._conn_lost += 1
        self.loop.call_soon(self._call_connection_lost, exception)
    
    def _call_connection_lost(self, exception):
        try:
            if self._protocol_connected:
                self.protocol.connection_lost(exception)
        finally:
            self.socket.close()
            self.socket = None
            self.protocol = None
            self.loop = None
            server = self.server
            if (server is not None):
                server._detach()
                self.server = None
    
    def get_write_buffer_size(self):
        return len(self.buffer)
    
    def pause_reading(self):
        if self.closing:
            raise RuntimeError('Cannot pause_reading() when closing')
        if self.paused:
            raise RuntimeError('Already paused')
        self.paused = True
        self.loop.remove_reader(self._sock_fd)
    
    def resume_reading(self):
        if not self.paused:
            raise RuntimeError('Not paused')
        
        self.paused = False
        if self.closing:
            return
        
        self.loop.add_reader(self._sock_fd, self._read_ready)
    
    def _read_ready(self):
        if self._conn_lost:
            return
        try:
            data = self.socket.recv(MAX_SIZE)
        except (BlockingIOError, InterruptedError):
            pass
        except Exception as err:
            self._fatal_error(err, 'Fatal read error on socket transport')
        else:
            if data:
                self.protocol.data_received(data)
            elif self.protocol.eof_received():
                # We're keeping the connection open so the
                # protocol can write more, but we still can't
                # receive more, so remove the reader callback.
                self.loop.remove_reader(self._sock_fd)
            else:
                self.close()
    
    def write(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f'data argument must be a bytes-like object, got {data.__class__.__name__}')
        if self.eof:
            raise RuntimeError('Cannot call write() after write_eof()')
        if not data:
            return
        
        if self._conn_lost:
            self._conn_lost += 1
            return
        
        if not self.buffer:
            # Optimization: try to send now.
            try:
                n = self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                pass
            except Exception as err:
                self._fatal_error(err, 'Fatal write error on socket transport')
                return
            else:
                data = data[n:]
                if not data:
                    return
            # Not all was written; register write handler.
            self.loop.add_writer(self._sock_fd, self._write_ready)
        
        # Add it to the buffer.
        self.buffer.extend(data)
        self._maybe_pause_protocol()

    def _write_ready(self):
        if self._conn_lost:
            return
        
        try:
            n = self.socket.send(self.buffer)
        except (BlockingIOError, InterruptedError):
            pass
        except Exception as err:
            self.loop.remove_writer(self._sock_fd)
            self.buffer.clear()
            self._fatal_error(err, 'Fatal write error on socket transport')
        else:
            if n:
                del self.buffer[:n]
            
            self._maybe_resume_protocol()  # May append to buffer.
            if not self.buffer:
                self.loop.remove_writer(self._sock_fd)
                
                if self.closing:
                    self._call_connection_lost(None)
                
                elif self.eof:
                    self.socket.shutdown(module_socket.SHUT_WR)
    
    def write_eof(self):
        if self.eof:
            return
        
        self.eof = True
        
        if not self.buffer:
            self.socket.shutdown(module_socket.SHUT_WR)
    
    def can_write_eof(self):
        return True


class _SelectorDatagramTransport(object):
    __slots__ = ('_extra', 'loop', '_protocol_paused', '_high_water', '_low_water', 'protocol', '_sock_fd',
        'buffer', '_conn_lost', 'socket', '_protocol_connected', 'closing', 'address')
    
    def __init__(self, loop, sock, protocol, address=None, waiter=None, extra=None):
        if extra is None:
            extra = {}
        
        self._extra = extra
        
        self.loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()
        
        extra['socket'] = sock
        
        try:
            sockname = sock.getsockname()
        except OSError:
            sockname = None
        extra['sockname'] = sockname
        
        if 'peername' not in extra:
            try:
                peername = sock.getpeername()
            except module_socket.error:
                peername = None
            
            extra['peername'] = peername
        
        self.socket = sock
        self._sock_fd = sock.fileno()
        
        self._protocol_connected = False
        self.protocol = protocol
        
        self.buffer = deque()
        self._conn_lost = 0 # Set when call to connection_lost scheduled.
        self.closing = False # Set when close() called.
        
        self.address = address
        self.loop.call_soon(self.protocol.connection_made, self)
        # only start reading when connection_made() has been called
        self.loop.call_soon(self._add_reader, self._sock_fd, self._read_ready)
        
        if waiter is not None:
            # only wake up the waiter when connection_made() has been called
            self.loop.call_soon(Future.set_result_if_pending, waiter, None)
    
    def get_extra_info(self, name, default=None):
        return self._extra.get(name, default)
    
    def is_reading(self):
        raise NotImplementedError
    
    def pause_reading(self):
        raise NotImplementedError
    
    def resume_reading(self):
        raise NotImplementedError
    
    def write(self, data):
        raise NotImplementedError
    
    def writelines(self, list_of_data):
        data = b''.join(list_of_data)
        self.write(data)
    
    def write_eof(self):
        raise NotImplementedError
    
    def can_write_eof(self):
        raise NotImplementedError
    
    def _maybe_pause_protocol(self):
        size = self.get_write_buffer_size()
        if size <= self._high_water:
            return
        
        if self._protocol_paused:
            return
            
        self._protocol_paused = True
        try:
            self.protocol.pause_writing()
        except Exception as err:
            self.loop.render_exc_async(err, [
                'Exception occured at:\n',
                repr(self),
                '._maybe_pause_protocol\n',
                    ])
    
    def _maybe_resume_protocol(self):
        if (not self._protocol_paused) or (self.get_write_buffer_size() > self._low_water):
            return
        
        self._protocol_paused = False
        try:
            self.protocol.resume_writing()
        except Exception as err:
            self.loop.render_exc_async(err, [
                'Exception occured at:\n',
                repr(self),
                '._maybe_resume_protocol\n',
                    ])
    
    def get_write_buffer_limits(self):
        return (self._low_water, self._high_water)
    
    def _set_write_buffer_limits(self, high=None, low=None):
        if high is None:
            if low is None:
                high = 65536
            else:
                high = low<<2
        
        if low is None:
            low = high>>2
        
        if not high >= low >= 0:
            raise ValueError(f'`high` ({high}) must be `>= low` ({low}) must be `>= 0`.')
        
        self._high_water = high
        self._low_water = low
    
    def set_write_buffer_limits(self, high=None, low=None):
        self._set_write_buffer_limits(high=high, low=low)
        self._maybe_pause_protocol()
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.socket is None:
            result.append(' closed')
        elif self.closing:
            result.append(' closing')
        
        result.append(' fd=')
        result.append(repr(self._sock_fd))
        
        loop = self.loop
        #is the transport open?
        if (loop is not None) and loop.running:
            try:
                key = loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling = 0
            else:
                polling = key.events&selectors.EVENT_READ
            
            result.append(' read=')
            if polling:
                state = 'polling'
            else:
                state = 'idle'
            result.append(state)
            
            try:
                key = loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling = 0
            else:
                polling = key.events&selectors.EVENT_WRITE
            
            result.append(' write=<')
            if polling:
                state = 'polling'
            else:
                state = 'idle'
            result.append(state)
            
            result.append(', bufsize=')
            
            bufsize = self.get_write_buffer_size()
            result.append(str(bufsize))
            result.append('>')
        
        result.append('>')
        
        return ''.join(result)
    
    def abort(self):
        self._force_close(None)
    
    def set_protocol(self, protocol):
        self.protocol = protocol
        self._protocol_connected = True
    
    def get_protocol(self):
        return self.protocol
    
    def is_closing(self):
        return self.closing
    
    def close(self):
        if self.closing:
            return
        
        self.closing = True
        self.loop.remove_reader(self._sock_fd)
        if not self.buffer:
            self._conn_lost += 1
            self.loop.remove_writer(self._sock_fd)
            self.loop.call_soon(self._call_connection_lost, None)
    
    def __del__(self):
        socket = self.socket
        if socket is not None:
            socket.close()
    
    def _fatal_error(self, exception, message='Fatal error on transport'):
        if not isinstance(exception, OSError):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occured\n',
                repr(self),
                '\n',
                    ])
        
        self._force_close(exception)
    
    def _force_close(self, exception):
        if self._conn_lost:
            return
        
        if self.buffer:
            self.buffer.clear()
            self.loop.remove_writer(self._sock_fd)
        
        if not self.closing:
            self.closing = True
            self.loop.remove_reader(self._sock_fd)
        
        self._conn_lost += 1
        self.loop.call_soon(self._call_connection_lost, exception)
    
    def _call_connection_lost(self, exception):
        try:
            if self._protocol_connected:
                self.protocol.connection_lost(exception)
        finally:
            self.socket.close()
            self.socket = None
            self.protocol = None
            self.loop = None
    
    def _add_reader(self, fd, callback, *args):
        if self.closing:
            return
        
        self.loop.add_reader(fd, callback, *args)
    
    def get_write_buffer_size(self):
        size = 0
        for data, address in self.buffer:
            size += len(data)
        
        return size
    
    def _read_ready(self):
        if self._conn_lost:
            return
        try:
            data, addr = self.socket.recvfrom(MAX_SIZE)
        except (BlockingIOError, InterruptedError):
            pass
        except OSError as err:
            self.protocol.error_received(err)
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as err:
            self._fatal_error(err, 'Fatal read error on datagram transport')
        else:
            self.protocol.datagram_received(data, addr)
    
    def sendto(self, data, addr=None):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f'data argument must be a bytes-like object, not {type(data).__name__!r}')
        
        if not data:
            return
        
        address = self.address
        if (address is not None):
            if (addr is not None) or (addr != address):
                raise ValueError(f'Invalid address: must be `None` or `{address!r}`, got {addr!r}.')
            addr = address
        
        if self._conn_lost and (address is not None):
            self._conn_lost += 1
            return
        
        buffer = self.buffer
        if not buffer:
            # Attempt to send it right away first.
            try:
                if self._extra['peername'] is None:
                    self.socket.sendto(data, addr)
                else:
                    self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                self.loop.add_writer(self._sock_fd, self._sendto_ready)
            except OSError as err:
                self.protocol.error_received(err)
                return
            except BaseException as err:
                self._fatal_error(err, 'Fatal write error on datagram transport')
                return
            else:
                return
        
        # Ensure that what we buffer is immutable.
        buffer.append((bytes(data), addr))
        self._maybe_pause_protocol()
    
    def _sendto_ready(self):
        buffer = self.buffer
        while buffer:
            data, addr = buffer.popleft()
            try:
                if self._extra['peername'] is None:
                    self.socket.sendto(data, addr)
                else:
                    self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                buffer.appendleft((data, addr))  # Try again later.
                break
            except OSError as err:
                self.protocol.error_received(err)
                return
            except BaseException as err:
                self._fatal_error(err, 'Fatal write error on datagram transport')
                return
        
        self._maybe_resume_protocol() # May append to buffer.
        if not buffer:
            self.loop.remove_writer(self._sock_fd)
            if self.closing:
                self._call_connection_lost(None)
