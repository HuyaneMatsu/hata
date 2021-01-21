# -*- coding: utf-8 -*-
import ssl, selectors
from collections import deque
import socket as module_socket

from .futures import Future

if hasattr(module_socket, 'TCP_NODELAY'):
    def _set_nodelay(socket):
        if (socket.family in (module_socket.AF_INET, module_socket.AF_INET6) and
            socket.type == module_socket.SOCK_STREAM and socket.proto == module_socket.IPPROTO_TCP):
            socket.setsockopt(module_socket.IPPROTO_TCP, module_socket.TCP_NODELAY, 1)
else:
    def _set_nodelay(socket):
        pass

MAX_SIZE = 262144

UNWRAPPED = 'UNWRAPPED'
DO_HANDSHAKE = 'DO_HANDSHAKE'
WRAPPED = 'WRAPPED'
SHUTDOWN = 'SHUTDOWN'

class _SSLPipe(object):
    """
    An SSL pipe.
    
    Allows you to communicate with an SSL/TLS protocol instance through memory buffers. It can be used to implement a
    security layer for an existing connection where you don't have access to the connection's file descriptor, or for
    some reason you don't want to use it.
    
    An ``_SSLPipe`` can be in `wrapped` and `unwrapped` mode. In unwrapped mode, data is passed through untransformed.
    In wrapped mode, application level data is encrypted to SSL record level data and vice versa. The SSL record level
    is the lowest level in the SSL protocol suite and is what travels as-is over the wire.
    
    An ``_SSLPipe`` initially is in `unwrapped` mode. To start SSL, call ``.do_handshake``, to shutdown SSL, call
    ``.unwrap``.
    
    Attributes
    ----------
    _handshake_cb : `None` or `callable`
        A Callback which will be called when handshake is completed. Set by ``.do_handshake``.
        
        Should accept the following parameters:
        +-------------------+---------------------------+
        | Respective name   | Value                     |
        +===================+===========================+
        | handshake_exception     | `None` or `BaseException` |
        +-------------------+---------------------------+
        
        If the handshake is successful, then the `handshake_exception` is given as `None`, else as an exception instance.
    _incoming : `ssl.MemoryBIO`
        Does the incoming data encryption/decryption.
    _outgoing : `ssl.MemoryBIO`
        Does the outgoing data encryption/decryption.
    _shutdown_cb : `None` or `callable`
        A callback which will be called when the shutdown is completed. Set by ``.shutdown``.
        
        Should accept no parameters.
    context : `ssl.SSLContext`
        The SSL pipe's SSL type.
    need_ssl_data : `bool`
        Whether more record level data is needed to complete a handshake that is currently in progress.
    server_hostname : `None` or `str`
        The ssl protocol's server hostname if applicable.
    server_side : `bool`
        Whether the ssl protocol is server side.
    ssl_object : `None` or `ssl.SSLObject`
        SSL object connecting ``._incoming`` and ``._outgoing`` memory bios set at ``.do_handshake``.
    state : `str`
        The state of the ``_SSLPipe``.
        
        Can be set as one of:
        
        +-------------------+-------------------+
        | Respective name   | Value             |
        +===================+===================+
        | UNWRAPPED         | `'UNWRAPPED'`     |
        +-------------------+-------------------+
        | DO_HANDSHAKE      | `'DO_HANDSHAKE'`  |
        +-------------------+-------------------+
        | WRAPPED           | `'WRAPPED'`       |
        +-------------------+-------------------+
        | SHUTDOWN          | `'SHUTDOWN'`      |
        +-------------------+-------------------+
        
        Note, that ``.state`` is checked by memory address and not by value.
    """
    __slots__ = ('_handshake_cb', '_incoming', '_outgoing', '_shutdown_cb', 'context', 'need_ssl_data',
        'server_hostname', 'server_side', 'ssl_object', 'state',)
    
    def __init__(self, context, server_side, server_hostname):
        """
        Creates a new ``_SSLPipe`` instance with the given parameters.
        
        Parameters
        ----------
        context : `ssl.SSLContext`
            The SSL pipe's SSL type.
        server_side : `bool`
            Whether the ssl protocol is server side.
        server_hostname : `None` or `str`
            The ssl protocol's server hostname if applicable.

        """
        self.context = context
        self.server_side = server_side
        self.server_hostname = server_hostname
        self.state = UNWRAPPED
        self._incoming = ssl.MemoryBIO()
        self._outgoing = ssl.MemoryBIO()
        self.ssl_object = None
        self.need_ssl_data = False
        self._handshake_cb = None
        self._shutdown_cb = None
    
    
    def is_wrapped(self):
        """
        Returns whether a security layer is currently is effect.
        
        In handshake or on in shutdown is always `False`.
        
        Returns
        -------
        is_wrapped : `bool`
        """
        return (self.state is WRAPPED)
    
    def do_handshake(self, callback=None):
        """
        Starts the SSL handshake.
        
        Parameters
        ----------
        callback : `None` or `callable`, Optional
            A Callback which will be called when handshake is completed.
            
            Should accept the following parameters:
            +-------------------+---------------------------+
            | Respective name   | Value                     |
            +===================+===========================+
            | handshake_exception     | `None` or `BaseException` |
            +-------------------+---------------------------+
            
            If the handshake is successful, then the `handshake_exception` is given as `None`, else as an exception
            instance.
            
        Returns
        -------
        ssl_data : `list` of `bytes`
            A list of SSL data. Always an empty list is returned.
        
        Raises
        ------
        RuntimeError
            If the handshake is in progress or is already completed.
        """
        if self.state is not UNWRAPPED:
            raise RuntimeError('Handshake in progress or completed.')
        
        self.ssl_object = self.context.wrap_bio(self._incoming, self._outgoing, server_side=self.server_side,
            server_hostname=self.server_hostname)
        
        self.state = DO_HANDSHAKE
        self._handshake_cb = callback
        ssl_data, application_data = self.feed_ssl_data(b'', only_handshake=True)
        
        return ssl_data
    
    def shutdown(self, callback=None):
        """
        Starts the SSL shutdown process.
        
        Parameters
        ----------
        callback : `None` or `callable`, Optional
            A callback which will be called when the shutdown is completed.
            
            Should accept no parameters.
        
        Returns
        -------
        ssl_data : `list` of `bytes`
            A list of SSL data.
        
        Raises
        ------
        RuntimeError
            - If the security layer is not yet present.
            - If shutdown is already in progress.
        """
        state = self.state
        if state is UNWRAPPED:
            raise RuntimeError('No security layer present.')
        if state is SHUTDOWN:
            raise RuntimeError('Shutdown in progress.')
        
        self.state = SHUTDOWN
        self._shutdown_cb = callback
        ssl_data, application_data = self.feed_ssl_data(b'')
        return ssl_data
    
    def feed_eof(self):
        """
        Sends an eof.
        
        Raises
        ------
        ssl.SSLError
            If the eof was unexpected. The raised ssl error has `errno` set as `ssl.SSL_ERROR_EOF`.
        """
        self._incoming.write_eof()
        # Ignore return.
        self.feed_ssl_data(b'')
    
    def feed_ssl_data(self, data, only_handshake=False):
        """
        Feed SSL record level data into the pipe.
        
        Parameters
        ----------
        data : `bytes`
            If empty `bytes` is given, then it will get ssl_data for the handshake initialization.
        
        Returns
        -------
        ssl_data : `list` of `bytes`
            Contains the SSL data that needs to be sent to the remote SSL.
        application_data : `list` of `bytes`
            Plaintext data that needs to be forwarded to the application.
            
            Might contain an empty `bytes`, what indicates that ``.shutdown`` should be called.
        """
        state = self.state
        ssl_data = []
        application_data = []
        
        if state is UNWRAPPED:
            # If unwrapped, pass plaintext data straight through.
            if data:
                application_data.append(data)
            
            return ssl_data, application_data
        
        self.need_ssl_data = False
        if data:
            self._incoming.write(data)
        
        try:
            if state is DO_HANDSHAKE:
                # Call do_handshake() until it doesn't raise anymore.
                self.ssl_object.do_handshake()
                self.state = state = WRAPPED
                
                handshake_cb = self._handshake_cb
                if (handshake_cb is not None):
                    handshake_cb(None)
                
                if only_handshake:
                    return ssl_data, application_data
                # Handshake done: execute the wrapped block
            
            if state is WRAPPED:
                # Main state: read data from SSL until close_notify.
                while True:
                    chunk = self.ssl_object.read(MAX_SIZE)
                    application_data.append(chunk)
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
                application_data.append(self._incoming.read())
        
        except (ssl.SSLError, ssl.CertificateError) as err:
            err_number = getattr(err, 'errno', None)
            if err_number not in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE, ssl.SSL_ERROR_SYSCALL):
                if self.state is DO_HANDSHAKE:
                    handshake_cb = self._handshake_cb
                    if (handshake_cb is not None):
                        handshake_cb(err)
                raise
            
            self.need_ssl_data = (err_number == ssl.SSL_ERROR_WANT_READ)

        # Check for record level data that needs to be sent back. Happens for the initial handshake and renegotiation.
        if self._outgoing.pending:
            ssl_data.append(self._outgoing.read())
        
        return ssl_data, application_data

    def feed_application_data(self, data, offset):
        """
        Feed plaintext data into the pipe.
        
        If the returned `offset` is less than the returned data's total length in bytes, that case is called
        `short write`. If `short-write` happens, than the same `data` should be passed to ``.feed_application_data``
        next time. (This is an OpenSSL requirement.) A further particularity is that a short write will always have
        `offset = 0`, because the `_ssl` module does not enable partial writes. And even though the offset is `0`,
        there will still be encrypted data in ssl_data.
        
        Returns
        -------
        ssl_data : `list` of `bytes-like`
            Containing record level data that needs to be sent to the remote SSL instance.
        offset : `int`
            The number of the processed plaintext data in bytes. Might be less than the total length of the returned
            data.
        
        Raises
        ------
        ssl.SSLError
            Any unexpected SSL error.
        """
        ssl_data = []
        if self.state is UNWRAPPED:
            # pass through data in unwrapped mode
            if offset < len(data):
                ssl_data.append(memoryview(data)[offset:])
            offset = len(data)
        else:
            view = memoryview(data)
            while True:
                self.need_ssl_data = False
                try:
                    if offset < len(view):
                        offset += self.ssl_object.write(view[offset:])
                except ssl.SSLError as err:
                    # It is not allowed to call `.write` after ``.unwrap`` until the close_notify is acknowledged. We
                    # return the condition to the caller as a short write.
                    if err.reason == 'PROTOCOL_IS_SHUTDOWN':
                        err.errno = ssl.SSL_ERROR_WANT_READ
                        need_ssl_data = True
                    else:
                        errno = getattr(err, 'errno', None)
                        if errno is None:
                            raise
                        
                        if errno == ssl.SSL_ERROR_WANT_READ:
                            need_ssl_data = True
                        elif errno == ssl.SSL_ERROR_WANT_WRITE or errno == ssl.SSL_ERROR_SYSCALL:
                            need_ssl_data = False
                        else:
                            raise
                    
                    self.need_ssl_data = need_ssl_data
    
                # See if there's any record level data back for us.
                if self._outgoing.pending:
                    ssl_data.append(self._outgoing.read())
                
                if offset == len(view) or self.need_ssl_data:
                    break
        
        return ssl_data, offset


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
            Default value to return if `name` could not be matched. Defaults to `None`.
        
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
        Gets the ssl protocol transport's actual protocol.
        
        Returns
        -------
        protocol : `Any`
            Asynchronous protocol implementation.
        """
        return self.app_protocol
    
    def is_closing(self):
        """
        Returns whether the ssl protocol transport is closing.
        
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
        Closes the ssl protocol transport if not yet closed.
        """
        if not self.closed:
            self.close()

    def pause_reading(self):
        """
        Pauses the receiving end.
        
        No data will be passed to the respective protocol's ``.data_received`` method until ``.resume_reading`` is
        called.
        """
        transport = self.ssl_protocol.transport
        if (transport is not None):
            transport.pause_reading()

    def resume_reading(self):
        """
        Resumes the receiving end.
        
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
            self.ssl_protocol._write_application_data(data)
    
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
    Asynchronous SSL protocol implementation on top of a `socket`. Uses `ssl.MemoryBIO` instances for incoming and
    outgoing data.
    
    Attributes
    ----------
    _call_connection_made : `bool`
        Whether the the ``.app_protocol``'s `.connection_made` should be called when handshake is completed.
    _connection_made_waiter : `None` or ``Future``
        A waiter future, what's result is set when connection is made, aka handshake is completed, or if when the
        connection is lost, depending which happens first.
        
        After the future's result or exception is set, the attribute is set as `None`.
    _extra : `dict` of (`str`, `Any`) items
        Optional transport information.
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
        Ensured data queued up to be written. Each element contains a tuple of the data to write and an offset till
        write from.
    app_protocol : `Any`
        Asynchronous protocol implementation.
    app_transport : ``_SSLProtocolTransport``
        Asynchronous ssl protocol's read-write  transport implementation.
    loop : ``EventThread``
        The respective event loop of the ssl protocol.
    server_hostname : `None` or `str`
        The ssl protocol's server hostname if applicable.
    server_side : `bool`
        Whether the ssl protocol is server side.
    ssl_pipe : `None` or ``_SSLPipe``
        Ssl pipe set meanwhile the protocol is connected to feed the ssl data to.
    transport : `None` or `Any`
        Asynchronous transport implementation.
    """
    __slots__ = ('_call_connection_made', '_connection_made_waiter', '_extra', '_handshake_start_time', '_in_handshake',
        '_in_shutdown', '_session_established', '_ssl_context', '_write_backlog', 'app_protocol', 'app_transport',
        'loop', 'server_hostname', 'server_side', 'ssl_pipe', 'transport',)
    
    def __new__(cls, loop, app_protocol, ssl_context, connection_made_waiter, server_side=False, server_hostname=None,
            call_connection_made=True):
        """
        Creates a new ``SSLProtocol`` instance.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop of the protocol.
        app_protocol : `Any`
            Asynchronous protocol implementation.
        ssl_context : `None` or `ssl.SSLContext`
            The connection ssl type. If SSl was given as `True` when creating a connection at this point we get it as
            `None`, so we create a default ssl context.
            
            Note, that if the connection is server side, a valid `ssl_context` should be given.
        connection_made_waiter : `None` or ``Future``
            A waiter future, what's result is set when connection is made, aka handshake is completed, or if when the
            connection is lost, depending which happens first.
            
            After the future's result or exception is set, the attribute is set as `None`.
        server_side
            Whether the ssl protocol is server side.
        server_hostname
            The ssl protocol's server hostname if applicable.
            
            If we are the `server_side`, then this parameter is forced to `None` (wont raise).
        call_connection_made
            Whether the the ``.app_protocol``'s `.connection_made` should be called when handshake is completed.
        
        Raises
        ------
        ValueError
            If the protocol is server side, but `ssl_context` is not given.
        """
        if ssl_context is None:
            if server_side:
                raise ValueError('Server side SSL needs a valid `ssl.SSLContext`.')
            
            ssl_context = ssl.create_default_context()
            if (server_hostname is None) or (not server_hostname):
                ssl_context.check_hostname = False
        
        if server_side:
            server_hostname = None
        
        self = object.__new__(cls)
        
        self.server_side = server_side
        self.server_hostname = server_hostname
        self._ssl_context = ssl_context
        self._extra = {'sslcontext': ssl_context}
        self._write_backlog = deque()
        self._connection_made_waiter = connection_made_waiter
        self.loop = loop
        self.app_protocol = app_protocol
        self.app_transport = _SSLProtocolTransport(self, app_protocol)
        self.ssl_pipe = None
        self._session_established = False
        self._in_handshake = False
        self._in_shutdown = False
        self.transport = None
        self._call_connection_made = call_connection_made
        
        return self
    
    def _wake_up_connection_made_waiter(self, exception=None):
        """
        Wakes up the ssl protocol's ``._connection_made_waiter`` if applicable.
        
        Called when connection is made closed or lost, depending, which happens first. If connection is made or closed,
        then the connection made waiter's result is set as `None`, if the connection is lost, then the respective
        exception is thrown into it if any.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``, Optional
            Exception to throw into ``._connection_made_waiter`` if any.
        """
        connection_made_waiter = self._connection_made_waiter
        if (connection_made_waiter is not None):
            self._connection_made_waiter = None
            if connection_made_waiter.pending():
                if exception is None:
                    connection_made_waiter.set_result(None)
                else:
                    connection_made_waiter.set_exception(exception)
    
    def connection_made(self, transport):
        """
        Called when the connection is made.
        
        Sets the ``SSLProtocol``'s ``.ssl_pipe`` and starts the ssl handshake.
        
        Parameters
        ----------
        transport : `Any`
            Asynchronous transport implementation, what calls the protocol's ``.data_received`` when data is
            received.
        """
        self.transport = transport
        self.ssl_pipe = _SSLPipe(self._ssl_context, self.server_side, self.server_hostname)
        
        self._handshake_start_time = None
        self._in_handshake = True
        # `(b'', 1)` is a special value in ``._process_write_backlog`` to do the SSL handshake
        self._write_backlog.append((b'', 1))
        self.loop.call_soon(self._process_write_backlog)
    
    def connection_lost(self, exception):
        """
        Called when the connection is lost or closed.
        
        Parameters
        ----------
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        if self._session_established:
            self._session_established = False
            app_protocol = self.app_protocol
            self.loop.call_soon(app_protocol.__class__.connection_lost, app_protocol, exception)
        
        self.transport = None
        self.app_transport = None
        self._wake_up_connection_made_waiter(exception)
    
    def pause_writing(self):
        """
        Called when the transport's buffer goes over the high-water mark.
        
        ``.pause_writing`` is called when the buffer goes over the high-water mark, and eventually
        ``.resume_writing`` is called when the buffer size reaches the low-water mark.
        """
        self.app_protocol.pause_writing()
    
    def resume_writing(self):
        """
        Called when the transport's buffer drains below the low-water mark.
        
        See ``.pause_writing`` for details.
        """
        self.app_protocol.resume_writing()
    
    def data_received(self, data):
        """
        Called when some data is received.
        
        Parameters
        ----------
        data : `bytes`
            The received data.
        """
        try:
            ssl_data, application_data = self.ssl_pipe.feed_ssl_data(data)
        except ssl.SSLError:
            self._abort()
            return
        
        for chunk in ssl_data:
            self.transport.write(chunk)
        
        for chunk in application_data:
            if chunk:
                self.app_protocol.data_received(chunk)
                continue
            
            self._start_shutdown()
            break
    
    def eof_received(self):
        """
        Calling ``.connection_lost`` without exception causes eof.
        
        Marks the protocol as it is at eof.
        
        If the protocol's ``._connection_made_waiter`` is not yet waken up, then raises `ConnectionResetError` into it.
        
        Returns
        -------
        transport_closes : `bool`
            Returns `False` if the transport will close itself. If it returns `True`, then closing the transport is up
            to the protocol.
            
            Always returns `False`.
        """
        try:
            self._wake_up_connection_made_waiter(ConnectionResetError)
            if not self._in_handshake:
                # has no effect whatever it returns when we use ssl
                self.app_protocol.eof_received()
        finally:
            self.transport.close()
        
        return False
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be matched. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
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
        """
        Starts the shutdown process of the ``SSLProtocol`` by writing empty bytes into itself.
        
        If the protocol is already in shutdown, does nothing.
        """
        if not self._in_shutdown:
            self._in_shutdown = True
            self._write_application_data(b'')
    
    def _write_application_data(self, data):
        """
        Writes data to the ``SSLProtocol`` to be sent.
        
        Parameters
        ----------
        data : `bytes-like`
            The data to write.
        """
        self._write_backlog.append((data, 0))
        self._process_write_backlog()
    
    def _on_handshake_complete(self, handshake_exception):
        """
        Called when ssl handshake is completed.
        
        Parameters
        ----------
        handshake_exception : `None` or `BaseException` instance
        
        """
        self._in_handshake = False
        ssl_object = self.ssl_pipe.ssl_object
        
        if (handshake_exception is None):
            try:
                peer_certification = ssl_object.getpeercert()
            except BaseException as err:
                handshake_exception = err
            else:
                handshake_exception = None
        
        if (handshake_exception is not None):
            self.transport.close()
            self._wake_up_connection_made_waiter(handshake_exception)
            raise
        
        # Add extra info that becomes available after handshake.
        extra = self._extra
        extra['peercert'] = peer_certification
        extra['cipher'] = ssl_object.cipher()
        extra['compression']= ssl_object.compression()
        extra['ssl_object'] = ssl_object
        
        if self._call_connection_made:
            self.app_protocol.connection_made(self.app_transport)
        
        self._wake_up_connection_made_waiter()
        self._session_established = True
        
        # Don's call it immediately, other tasks might be scheduled already.
        self.loop.call_soon(self._process_write_backlog)

    def _process_write_backlog(self):
        """
        Try to make progress on the write backlog.
        
        Feeds data to ``.ssl_pipe`` till it is full.
        """
        transport = self.transport
        if transport is None:
            return
        
        write_backlog = self._write_backlog
        try:
            for _ in range(len(write_backlog)):
                data, offset = write_backlog[0]
                if data:
                    ssl_data, offset = self.ssl_pipe.feed_application_data(data, offset)
                else:
                    # If data is given as empty bytes means we either have handshake complete or there is no more data
                    # to write
                    if offset:
                        ssl_data = self.ssl_pipe.do_handshake(self._on_handshake_complete)
                    else:
                        ssl_data = self.ssl_pipe.shutdown(self._finalize)
                    
                    offset = 1
                
                for chunk in ssl_data:
                    transport.write(chunk)
                
                if offset < len(data):
                    write_backlog[0] = (data, offset)
                    # A short write means that a write is blocked on a read, we need to enable reading if it is paused!
                    assert self.ssl_pipe.need_ssl_data
                    if transport._paused:
                        transport.resume_reading()
                    
                    break
                
                # An entire chunk from the backlog was processed. We can delete it and reduce the outstanding buffer
                # size.
                del self._write_backlog[0]
        except BaseException as err:
            if self._in_handshake:
                self._on_handshake_complete(err)
            else:
                self._fatal_error(err, 'Fatal error on SSL transport.')
            if not isinstance(err, Exception):
                # BaseException
                raise
    
    def _fatal_error(self, exception, message='Fatal error on transport.'):
        """
        If a fatal error occurs on the protocol renders it's traceback and closes it's transport.
        
        Parameters
        ----------
        exception : `BaseException`
            The occurred exception.
        message : `str`, Optional
            Additional error message to render.
        """
        if not isinstance(exception, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occurred\n',
                repr(self),
                '\n',
                    ])
        
        transport = self.transport
        if (transport is not None):
            transport._force_close(exception)

    def _finalize(self):
        """
        CLoses the ``SSLProtocol``'s transport.
        
        Called after shutdown or abortion.
        """
        transport = self.transport
        if (transport is not None):
            transport.close()

    def _abort(self):
        """
        Closes the protocol by trying to abort it's transport immediately.
        """
        transport = self.transport
        if (transport is not None):
            try:
                transport.abort()
            finally:
                self._finalize()


class _SelectorSocketTransport(object):
    __slots__ = ('_extra', 'loop', 'protocol', '_low_water', '_high_water', '_protocol_paused', 'socket', '_socket_fd',
        '_protocol_connected', 'server', 'buffer', '_conn_lost', 'closing', 'eof', 'paused',)
    
    def __init__(self, loop, socket, protocol, waiter=None, extra=None, server=None):
        
        if extra is None:
            extra = {}
        
        self._extra = extra
        self.loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()
        
        extra['socket'] = socket
        
        try:
            socket_name = socket.getsockname()
        except OSError:
            socket_name = None
        extra['sockname'] = socket_name
        
        if 'peername' not in extra:
            try:
                peer_name = socket.getpeername()
            except module_socket.error:
                peer_name = None
            extra['peername'] = peer_name
        
        self.socket = socket
        self._socket_fd = socket.fileno()
        
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
        _set_nodelay(socket)
        
        loop.call_soon(protocol.connection_made, self)
        
        #only start reading when connection_made() has been called
        loop.call_soon(loop.add_reader, self._socket_fd, self._read_ready)
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
        result.append(repr(self._socket_fd))
        
        loop = self.loop
        #is the transport open?
        if (loop is not None) and loop.running:
        
            try:
                key = loop.selector.get_key(self._socket_fd)
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
                key = loop.selector.get_key(self._socket_fd)
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

            result.append(', buffer_size=')
            
            buffer_size = self.get_write_buffer_size()
            result.append(str(buffer_size))
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
                'Exception occurred at:\n',
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
                'Exception occurred at:\n',
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
        self.loop.remove_reader(self._socket_fd)
        if not self.buffer:
            self._conn_lost += 1
            self.loop.remove_writer(self._socket_fd)
            self.loop.call_soon(self._call_connection_lost, None)
    
    def _fatal_error(self, exception, message='Fatal error on transport'):
        if not isinstance(exception, (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occurred\n',
                repr(self),
                '\n',
                    ])
        
        self._force_close(exception)
    
    def _force_close(self, exception):
        if self._conn_lost:
            return
        
        if self.buffer:
            self.buffer.clear()
            self.loop.remove_writer(self._socket_fd)
        
        if not self.closing:
            self.closing = True
            self.loop.remove_reader(self._socket_fd)
        
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
        self.loop.remove_reader(self._socket_fd)
    
    def resume_reading(self):
        if not self.paused:
            raise RuntimeError('Not paused')
        
        self.paused = False
        if self.closing:
            return
        
        self.loop.add_reader(self._socket_fd, self._read_ready)
    
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
                self.loop.remove_reader(self._socket_fd)
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
            self.loop.add_writer(self._socket_fd, self._write_ready)
        
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
            self.loop.remove_writer(self._socket_fd)
            self.buffer.clear()
            self._fatal_error(err, 'Fatal write error on socket transport')
        else:
            if n:
                del self.buffer[:n]
            
            self._maybe_resume_protocol()  # May append to buffer.
            if not self.buffer:
                self.loop.remove_writer(self._socket_fd)
                
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
    __slots__ = ('_extra', 'loop', '_protocol_paused', '_high_water', '_low_water', 'protocol', '_socket_fd',
        'buffer', '_conn_lost', 'socket', '_protocol_connected', 'closing', 'address')
    
    def __init__(self, loop, socket, protocol, address=None, waiter=None, extra=None):
        if extra is None:
            extra = {}
        
        self._extra = extra
        
        self.loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()
        
        extra['socket'] = socket
        
        try:
            socket_name = socket.getsockname()
        except OSError:
            socket_name = None
        extra['sockname'] = socket_name
        
        if 'peername' not in extra:
            try:
                peer_name = socket.getpeername()
            except module_socket.error:
                peer_name = None
            
            extra['peername'] = peer_name
        
        self.socket = socket
        self._socket_fd = socket.fileno()
        
        self._protocol_connected = False
        self.protocol = protocol
        
        self.buffer = deque()
        self._conn_lost = 0 # Set when call to connection_lost scheduled.
        self.closing = False # Set when close() called.
        
        self.address = address
        self.loop.call_soon(self.protocol.connection_made, self)
        # only start reading when connection_made() has been called
        self.loop.call_soon(self._add_reader, self._socket_fd, self._read_ready)
        
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
                'Exception occurred at:\n',
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
                'Exception occurred at:\n',
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
        result.append(repr(self._socket_fd))
        
        loop = self.loop
        #is the transport open?
        if (loop is not None) and loop.running:
            try:
                key = loop.selector.get_key(self._socket_fd)
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
                key = loop.selector.get_key(self._socket_fd)
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
            
            result.append(', buffer_size=')
            
            buffer_size = self.get_write_buffer_size()
            result.append(str(buffer_size))
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
        self.loop.remove_reader(self._socket_fd)
        if not self.buffer:
            self._conn_lost += 1
            self.loop.remove_writer(self._socket_fd)
            self.loop.call_soon(self._call_connection_lost, None)
    
    def __del__(self):
        socket = self.socket
        if socket is not None:
            socket.close()
    
    def _fatal_error(self, exception, message='Fatal error on transport'):
        if not isinstance(exception, OSError):
            self.loop.render_exc_async(exception, [
                message,
                ' exception occurred\n',
                repr(self),
                '\n',
                    ])
        
        self._force_close(exception)
    
    def _force_close(self, exception):
        if self._conn_lost:
            return
        
        if self.buffer:
            self.buffer.clear()
            self.loop.remove_writer(self._socket_fd)
        
        if not self.closing:
            self.closing = True
            self.loop.remove_reader(self._socket_fd)
        
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
            data, address = self.socket.recvfrom(MAX_SIZE)
        except (BlockingIOError, InterruptedError):
            pass
        except OSError as err:
            self.protocol.error_received(err)
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as err:
            self._fatal_error(err, 'Fatal read error on datagram transport')
        else:
            self.protocol.datagram_received(data, address)
    
    def sendto(self, data, maybe_address=None):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError(f'data argument must be a bytes-like object, not {type(data).__name__!r}')
        
        if not data:
            return
        
        address = self.address
        if (address is not None):
            if (maybe_address is not None) or (maybe_address != address):
                raise ValueError(f'Invalid address: must be `None` or `{address!r}`, got {maybe_address!r}.')
            maybe_address = address
        
        if self._conn_lost and (address is not None):
            self._conn_lost += 1
            return
        
        buffer = self.buffer
        if not buffer:
            # Attempt to send it right away first.
            try:
                if self._extra['peername'] is None:
                    self.socket.sendto(data, maybe_address)
                else:
                    self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                self.loop.add_writer(self._socket_fd, self._sendto_ready)
            except OSError as err:
                self.protocol.error_received(err)
                return
            except BaseException as err:
                self._fatal_error(err, 'Fatal write error on datagram transport')
                return
            else:
                return
        
        # Ensure that what we buffer is immutable.
        buffer.append((bytes(data), maybe_address))
        self._maybe_pause_protocol()
    
    def _sendto_ready(self):
        buffer = self.buffer
        while buffer:
            data, address = buffer.popleft()
            try:
                if self._extra['peername'] is None:
                    self.socket.sendto(data, address)
                else:
                    self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                buffer.appendleft((data, address))  # Try again later.
                break
            except OSError as err:
                self.protocol.error_received(err)
                return
            except BaseException as err:
                self._fatal_error(err, 'Fatal write error on datagram transport')
                return
        
        self._maybe_resume_protocol() # May append to buffer.
        if not buffer:
            self.loop.remove_writer(self._socket_fd)
            if self.closing:
                self._call_connection_lost(None)
