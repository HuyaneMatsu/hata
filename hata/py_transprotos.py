# -*- coding: utf-8 -*-
import ssl, sys
from collections import deque
import socket as module_socket
import selectors

def _create_transport_context(server_side,server_hostname):
    if server_side:
        raise ValueError('Server side SSL needs a valid SSLContext')

    # Client side may pass ssl=True to use a default
    # context; in that case the sslcontext passed is None.
    # The default is secure for client connections.
    sslcontext=ssl.create_default_context()
    if not server_hostname:
        sslcontext.check_hostname=False
    return sslcontext

if hasattr(module_socket,'TCP_NODELAY'):
    def _set_nodelay(sock):
        if (sock.family in (module_socket.AF_INET,module_socket.AF_INET6) and
            sock.type==module_socket.SOCK_STREAM and sock.proto==module_socket.IPPROTO_TCP):
            sock.setsockopt(module_socket.IPPROTO_TCP,module_socket.TCP_NODELAY,1)
else:
    def _set_nodelay(sock):
        pass
    

def _set_result_if_can(future,result):
    if future.done():
        return
    future.set_result(result)
    
UNWRAPPED   = 'UNWRAPPED'
DO_HANDSHAKE= 'DO_HANDSHAKE'
WRAPPED     = 'WRAPPED'
SHUTDOWN    = 'SHUTDOWN'
MAX_SIZE    = 262144

class _SSLPipe(object):
    __slots__=('_handshake_cb', '_incoming', '_outgoing', '_shutdown_cb',
        'context', 'need_ssldata', 'server_hostname', 'server_side',
        'ssl_object', 'state',)
    
    def __init__(self,context,server_side,server_hostname=None):
        self.context        = context
        self.server_side    = server_side
        self.server_hostname= server_hostname
        self.state          = UNWRAPPED
        self._incoming      = ssl.MemoryBIO()
        self._outgoing      = ssl.MemoryBIO()
        self.ssl_object     = None
        self.need_ssldata   = False
        self._handshake_cb  = None
        self._shutdown_cb   = None


    @property
    def wrapped(self):
        return self.state is WRAPPED

    def do_handshake(self,callback=None):
        if self.state is not UNWRAPPED:
            raise RuntimeError('handshake in progress or completed')
        self.ssl_object=self.context.wrap_bio(self._incoming,self._outgoing,
            server_side=self.server_side,server_hostname=self.server_hostname)

        self.state=DO_HANDSHAKE
        self._handshake_cb=callback
        ssldata,_=self.feed_ssldata(b'',only_handshake=True)

        return ssldata

    def shutdown(self, callback=None):
        if self.state is UNWRAPPED:
            raise RuntimeError('no security layer present')
        if self.state is SHUTDOWN:
            raise RuntimeError('shutdown in progress')

        self.state=SHUTDOWN
        self._shutdown_cb=callback
        ssldata,_=self.feed_ssldata(b'')
        return ssldata

    def feed_eof(self):
        self._incoming.write_eof()
        self.feed_ssldata(b'') #return is ignored

    def feed_ssldata(self, data, only_handshake=False):
        if self.state is UNWRAPPED:
            # If unwrapped, pass plaintext data straight through.
            if data:
                appdata=[data]
            else:
                appdata=[]
            return [],appdata

        self.need_ssldata = False
        if data:
            self._incoming.write(data)

        ssldata = []
        appdata = []
        try:
            if self.state is DO_HANDSHAKE:
                # Call do_handshake() until it doesn't raise anymore.
                self.ssl_object.do_handshake()
                self.state = WRAPPED
                if self._handshake_cb:
                    self._handshake_cb(None)
                if only_handshake:
                    return ssldata,appdata
                # Handshake done: execute the wrapped block

            if self.state is WRAPPED:
                # Main state: read data from SSL until close_notify
                while True:
                    chunk = self.ssl_object.read(MAX_SIZE)
                    appdata.append(chunk)
                    if not chunk:  # close_notify
                        break

            elif self.state is SHUTDOWN:
                # Call shutdown() until it doesn't raise anymore.
                self.ssl_object.unwrap()
                self.ssl_object = None
                self.state = UNWRAPPED
                if self._shutdown_cb:
                    self._shutdown_cb()

            elif self.state is UNWRAPPED:
                # Drain possible plaintext data after close_notify.
                appdata.append(self._incoming.read())
        except (ssl.SSLError,ssl.CertificateError) as err:
            err_number=getattr(err,'errno',None)
            if err_number not in (ssl.SSL_ERROR_WANT_READ,ssl.SSL_ERROR_WANT_WRITE,ssl.SSL_ERROR_SYSCALL):
                if self.state is DO_HANDSHAKE and self._handshake_cb:
                    self._handshake_cb(err)
                raise
            self.need_ssldata=(err_number==ssl.SSL_ERROR_WANT_READ)

        # Check for record level data that needs to be sent back.
        # Happens for the initial handshake and renegotiations.
        if self._outgoing.pending:
            ssldata.append(self._outgoing.read())
        return ssldata,appdata

    def feed_appdata(self, data, offset=0):
        if self.state is UNWRAPPED:
            # pass through data in unwrapped mode
            if offset<len(data):
                ssldata=[data[offset:]]
            else:
                ssldata=[]
            return ssldata,len(data)

        ssldata=[]
        view=memoryview(data)
        while True:
            self.need_ssldata = False
            try:
                if offset<len(view):
                    offset =self.ssl_object.write(view[offset:])
            except ssl.SSLError as err:
                # It is not allowed to call write() after unwrap() until the
                # close_notify is acknowledged. We return the condition to the
                # caller as a short write.
                if err.reason == 'PROTOCOL_ISSHUTDOWN':
                    err.errno=ssl.SSL_ERROR_WANT_READ
                if err.errno not in (ssl.SSL_ERROR_WANT_READ,ssl.SSL_ERROR_WANT_WRITE,ssl.SSL_ERROR_SYSCALL):
                    raise
                self.need_ssldata = (err.errno==ssl.SSL_ERROR_WANT_READ)

            # See if there's any record level data back for us.
            if self._outgoing.pending:
                ssldata.append(self._outgoing.read())
            if offset==len(view) or self.need_ssldata:
                break
        return ssldata,offset

class _SSLProtocolTransport(object):
    __slots__=('app_protocol', 'closed', 'loop', 'ssl_protocol',)
    def __init__(self,loop,ssl_protocol,app_protocol):
        self.loop           = loop
        self.ssl_protocol   = ssl_protocol
        self.app_protocol   = app_protocol
        self.closed         = False

    def get_extra_info(self,name,default=None):
        return self.ssl_protocol._get_extra_info(name,default)

    def set_protocol(self, protocol):
        self.app_protocol=protocol

    def get_protocol(self):
        return self.app_protocol

    def is_closing(self):
        return self.closed

    def close(self):
        self.closed=True
        self.ssl_protocol._start_shutdown()

    def __del__(self):
        if not self.closed:
            self.close()

    def pause_reading(self):
        self.ssl_protocol.transport.pause_reading()

    def resume_reading(self):
        self.ssl_protocol.transport.resume_reading()

    def set_write_buffer_limits(self,high=None,low=None):
        self.ssl_protocol.transport.set_write_buffer_limits(high,low)
    
    def get_write_buffer_size(self):
        return self.ssl_protocol.transport.get_write_buffer_size()
            
    def write(self,data):
        if not isinstance(data,(bytes,bytearray,memoryview)):
            raise TypeError(f'data: expecting a bytes-like instance, got {data.__class__.__name__}')
        if data:
            self.ssl_protocol._write_appdata(data)

    def writelines(self,list_of_data):
        self.write(b''.join(list_of_data))
        
    def can_write_eof(self):
        return False

    def abort(self):
        self.ssl_protocol._abort()

        
class SSLProtocol(object):
    __slots__=('_call_connection_made', '_extra', '_handshake_start_time',
        '_in_handshake', '_in_shutdown', '_session_established', '_sslcontext',
        '_waiter', '_write_backlog', '_write_buffer_size', 'app_protocol',
        'app_transport', 'loop', 'server_hostname', 'server_side', 'sslpipe',
        'transport',)
    
    def __init__(self,loop,app_protocol,sslcontext,waiter,server_side=False,
                 server_hostname='',call_connection_made=True):

        if not sslcontext:
            sslcontext=_create_transport_context(server_side,server_hostname)

        self.server_side = server_side
        if server_hostname and not server_side:
            self.server_hostname = server_hostname
        else:
            self.server_hostname=None
        
        self._sslcontext=sslcontext
        # SSL-specific extra info. More info are set when the handshake
        # completes.
        self._extra={'sslcontext':sslcontext}

        # App data write buffering
        self._write_backlog=deque()
        self._write_buffer_size=0

        self._waiter=waiter
        self.loop=loop
        self.app_protocol=app_protocol
        self.app_transport=_SSLProtocolTransport(loop,self,app_protocol)
        # _SSLPipe instance (None until the connection is made)
        self.sslpipe=None
        self._session_established=False
        self._in_handshake=False
        self._in_shutdown=False
        # transport, ex: SelectorSocketTransport
        self.transport=None
        self._call_connection_made=call_connection_made

    def _wakeup_waiter(self,exception=None):
        waiter=self._waiter
        if waiter is None:
            return
        if waiter.pending():
            if exception is None:
                waiter.set_result(None)
            else:
                waiter.set_exception(exception)

        self._waiter=None

    def connection_made(self, transport):
        self.transport=transport
        self.sslpipe=_SSLPipe(self._sslcontext,self.server_side,self.server_hostname)
        self._start_handshake()

    def connection_lost(self,exception):
        if self._session_established:
            self._session_established = False
            self.loop.call_soon(self.app_protocol.connection_lost,exception)
        self.transport = None
        self.app_transport = None
        self._wakeup_waiter(exception)
    
    def pause_writing(self):
        self.app_protocol.pause_writing()

    def resume_writing(self):
        self.app_protocol.resume_writing()

    def data_received(self, data):
        try:
            ssldata,appdata = self.sslpipe.feed_ssldata(data)
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
            self._wakeup_waiter(ConnectionResetError)
            if not self._in_handshake:
                #has no effect whatever it returns when we use ssl
                self.app_protocol.eof_received()
        finally:
            self.transport.close()

    def _get_extra_info(self,name,default=None):
        try:
            return self._extra[name]
        except KeyError:
            pass
        return self.transport.get_extra_info(name,default)

    def _start_shutdown(self):
        if self._in_shutdown:
            return
        self._in_shutdown=True
        self._write_appdata(b'')

    def _write_appdata(self, data):
        self._write_backlog.append((data,0))
        self._write_buffer_size+=len(data)
        self._process_write_backlog()

    def _start_handshake(self):
        self._handshake_start_time = None
        self._in_handshake = True
        #(b'',1) is a special value in _process_write_backlog() to do the SSL handshake
        self._write_backlog.append((b'',1))
        self.loop.call_soon(self._process_write_backlog)

    def _on_handshake_complete(self,handshake_exc):
        self._in_handshake = False
        sslobj=self.sslpipe.ssl_object
        
        try:
            if handshake_exc is not None:
                raise handshake_exc

            peercert = sslobj.getpeercert()
        except BaseException as err:
            self.transport.close()
            if isinstance(err,Exception):
                self._wakeup_waiter(err)
                return
            raise


        # Add extra info that becomes available after handshake.
        extra=self._extra
        extra['peercert']   = peercert
        extra['cipher']     = sslobj.cipher()
        extra['compression']= sslobj.compression()
        extra['ssl_object'] = sslobj

        if self._call_connection_made:
            self.app_protocol.connection_made(self.app_transport)
            
        self._wakeup_waiter()
        self._session_established = True
        # In case transport.write() was already called. Don't call
        # immediately _process_write_backlog(), but schedule it:
        # _on_handshake_complete() can be called indirectly from
        # _process_write_backlog(), and _process_write_backlog() is not
        # reentrant.
        self.loop.call_soon(self._process_write_backlog)

    def _process_write_backlog(self):
        # Try to make progress on the write backlog.
        if self.transport is None:
            return

        try:
            for i in range(len(self._write_backlog)):
                data,offset=self._write_backlog[0]
                if data:
                    ssldata,offset=self.sslpipe.feed_appdata(data,offset)
                elif offset:
                    ssldata=self.sslpipe.do_handshake(self._on_handshake_complete)
                    offset=1
                else:
                    ssldata=self.sslpipe.shutdown(self._finalize)
                    offset=1

                for chunk in ssldata:
                    self.transport.write(chunk)

                if offset<len(data):
                    self._write_backlog[0]=(data,offset)
                    # A short write means that a write is blocked on a read
                    # We need to enable reading if it is paused!
                    assert self.sslpipe.need_ssldata
                    if self.transport._paused:
                        self.transport.resume_reading()
                    break

                # An entire chunk from the backlog was processed. We can
                # delete it and reduce the outstanding buffer size.
                del self._write_backlog[0]
                self._write_buffer_size-=len(data)
        except BaseException as err:
            if self._in_handshake:
                self._on_handshake_complete(err)
            else:
                self._fatal_error(err,'Fatal error on SSL transport')
            if not isinstance(err,Exception):
                # BaseException
                raise

    def _fatal_error(self,exception,message='Fatal error on transport'):
        # Should be called from exception handler only.
        if not isinstance(exception,(BrokenPipeError,ConnectionResetError,ConnectionAbortedError)):
            self.loop.render_exc_async(exception,[
                message,
                ' exception occured\n',
                self.__repr__(),
                '\n',
                    ])
            
        if self.transport is not None:
            self.transport._force_close(exception)

    def _finalize(self):
        if self.transport is not None:
            self.transport.close()

    def _abort(self):
        if self.transport is not None:
            try:
                self.transport.abort()
            finally:
                self._finalize()


class _SelectorSocketTransport(object):

    __slots__=('__weakref__','_extra','loop','protocol','_low_water',
        '_high_water','_protocol_paused', 'socket','_sock_fd',
        '_protocol_connected','server','buffer','_conn_lost',
        'closing','eof','paused',)
    
    def __init__(self,loop,sock,protocol,waiter=None,extra=None,server=None):

        if extra is None:
            extra={}
        self._extra=extra
        self.loop = loop
        self._protocol_paused = False
        self._set_write_buffer_limits()
        
        self._extra['socket'] = sock
        self._extra['sockname'] = sock.getsockname()
        if 'peername' not in extra:
            try:
                extra['peername'] = sock.getpeername()
            except module_socket.error:
                extra['peername'] = None
        
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
        loop.transports[self._sock_fd]=self
        
        self.eof = False
        self.paused = False

        # Disable the Nagle algorithm -- small writes will be
        # sent without waiting for the TCP ACK.  This generally
        # decreases the latency (in some cases significantly.)
        _set_nodelay(sock)

        self.loop.call_soon(self.protocol.connection_made,self)
        
        #only start reading when connection_made() has been called
        self.loop.call_soon(self.loop._add_reader,self._sock_fd,self._read_ready)
        if waiter is not None:
            # only wake up the waiter when connection_made() has been called
            self.loop.call_soon(_set_result_if_can,waiter,None)

    def __del__(self):
        socket=self.socket
        if socket is not None:
            socket.close()

    def __repr__(self):
        result=['<',self.__class__.__name__]
        if self.socket is None:
            result.append(' closed')
        elif self.closing:
            result.append(' closing')
        result.append(' fd=')
        result.append(self._sock_fd.__repr__())
        
        loop=self.loop
        #is the transport open?
        if (loop is not None) and loop.running:

            try:
                key=loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling=0
            else:
                polling=key.events&selectors.EVENT_READ

            if polling:
                result.append(' read=polling')
            else:
                result.append(' read=idle')

            try:
                key=loop.selector.get_key(self._sock_fd)
            except KeyError:
                polling=0
            else:
                polling=key.events&selectors.EVENT_WRITE

            result.append(' write=<')
            if polling:
                result.append('polling')
            else:
                result.append('idle')

            result.append(', bufsize=')
            
            bufsize=self.get_write_buffer_size()
            result.append(str(bufsize))
            result.append('>')
        result.append('>')
        
        return ''.join(result)

    def writelines(self,list_of_data):
        self.write(b''.join(list_of_data))


    def get_extra_info(self,name,default=None):
        return self._extra.get(name,default)

    def _maybe_pause_protocol(self):
        size=self.get_write_buffer_size()
        if size<=self._high_water:
            return
        
        if self._protocol_paused:
            return
        
        self._protocol_paused = True
        try:
            self.protocol.pause_writing()
        except Exception as err:
            self.loop.render_exc_async(err,[
                'Exception occured at:\n',
                self.__repr__(),
                '._maybe_pause_protocol\n',
                    ])
    def _maybe_resume_protocol(self):
        if (not self._protocol_paused) or (self.get_write_buffer_size()>self._low_water):
            return
        self._protocol_paused = False
        try:
            self.protocol.resume_writing()
        except Exception as err:
            self.loop.render_exc_async(err,[
                'Exception occured at:\n',
                self.__repr__(),
                '._maybe_resume_protocol\n',
                    ])

    def get_write_buffer_limits(self):
        return self._low_water,self._high_water

    def _set_write_buffer_limits(self, high=None, low=None):
        if high is None:
            if low is None:
                high=65536
            else:
                high=low<<2
        if low is None:
            low=high>>2
            
        if not high>=low>=0:
            raise ValueError(f'high ({high}) must be >= low ({low}) must be >= 0')
        self._high_water=high
        self._low_water=low

    def set_write_buffer_limits(self,high=None,low=None):
        self._set_write_buffer_limits(high=high,low=low)
        self._maybe_pause_protocol()

    def abort(self):
        self._force_close(None)

    def set_protocol(self, protocol):
        self.protocol=protocol

    def get_protocol(self):
        return self.protocol

    def is_closing(self):
        return self.closing

    def close(self):
        if self.closing:
            return
        self.closing=True
        self.loop.remove_reader(self._sock_fd)
        if not self.buffer:
            self._conn_lost+=1
            self.loop.remove_writer(self._sock_fd)
            self.loop.call_soon(self._call_connection_lost, None)

    def _fatal_error(self, exception, message='Fatal error on transport'):
        # Should be called from exception handler only.
        if not isinstance(exception,(BrokenPipeError,ConnectionResetError,ConnectionAbortedError)):
            self.loop.render_exc_async(exception,[
                message,
                ' exception occured\n',
                self.__repr__(),
                '\n',
                    ])
        
        self._force_close(exception)

    def _force_close(self,exception):
        if self._conn_lost:
            return
        
        if self.buffer:
            self.buffer.clear()
            self.loop.remove_writer(self._sock_fd)
            
        if not self.closing:
            self.closing = True
            self.loop.remove_reader(self._sock_fd)
        
        self._conn_lost+=1
        self.loop.call_soon(self._call_connection_lost,exception)

    def _call_connection_lost(self, exception):
        try:
            if self._protocol_connected:
                self.protocol.connection_lost(exception)
        finally:
            self.socket.close()
            self.socket=None
            self.protocol=None
            self.loop=None
            server=self.server
            if server is not None:
                server._detach()
                self.server=None

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
        self.loop._add_reader(self._sock_fd,self._read_ready)

    def _read_ready(self):
        if self._conn_lost:
            return
        try:
            data = self.socket.recv(MAX_SIZE)
        except (BlockingIOError, InterruptedError):
            pass
        except Exception as err:
            self._fatal_error(err,'Fatal read error on socket transport')
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

    def write(self,data):
        if not isinstance(data,(bytes,bytearray, memoryview)):
            raise TypeError(f'data argument must be a bytes-like object, got {data.__class__.__name__}')
        if self.eof:
            raise RuntimeError('Cannot call write() after write_eof()')
        if not data:
            return

        if self._conn_lost:
            self._conn_lost+=1
            return

        if not self.buffer:
            # Optimization: try to send now.
            try:
                n = self.socket.send(data)
            except (BlockingIOError, InterruptedError):
                pass
            except Exception as err:
                self._fatal_error(err,'Fatal write error on socket transport')
                return
            else:
                data=data[n:]
                if not data:
                    return
            # Not all was written; register write handler.
            self.loop._add_writer(self._sock_fd,self._write_ready)

        # Add it to the buffer.
        self.buffer.extend(data)
        self._maybe_pause_protocol()

    def _write_ready(self):
        if self._conn_lost:
            return
        try:
            n=self.socket.send(self.buffer)
        except (BlockingIOError,InterruptedError):
            pass
        except Exception as err:
            self.loop.remove_writer(self._sock_fd)
            self.buffer.clear()
            self._fatal_error(err,'Fatal write error on socket transport')
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

    
