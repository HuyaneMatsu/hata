# -*- coding: utf-8 -*-
__all__ = ('WSClient', 'WSServer', )

import hashlib, codecs, functools, http
from random import getrandbits
from base64 import b64encode, b64decode
from collections import OrderedDict
from binascii import Error as BinasciiError
from email.utils import formatdate

from .dereaddons_local import multidict_titled
from .futures import Future, Task, AsyncQue, future_or_timeout, shield, CancelledError, WaitTillAll, iscoroutine, Lock

from .url import URL
from .hdrs import CONNECTION, SEC_WEBSOCKET_KEY, AUTHORIZATION, SEC_WEBSOCKET_VERSION, build_subprotocols, \
    SEC_WEBSOCKET_EXTENSIONS, SEC_WEBSOCKET_PROTOCOL, HOST, ORIGIN, SEC_WEBSOCKET_ACCEPT, UPGRADE, DATE, METH_GET, \
    CONTENT_TYPE, SERVER, CONTENT_LENGTH, build_extensions, build_basic_auth, parse_subprotocols, parse_upgrades, \
    parse_connections, parse_extensions
from .exceptions import PayloadError, InvalidUpgrade, AbortHandshake, ConnectionClosed, InvalidHandshake, \
    InvalidOrigin, WebSocketProtocolError
from .helpers import HttpVersion11
from .protocol import ProtocolBase, WS_OP_CONT, WS_OP_TEXT, WS_OP_BINARY , WS_OP_CLOSE, WS_OP_PING, WS_OP_PONG, \
    WS_DATA_OPCODES, WS_CTRL_OPCODES, Frame

FORBIDDEN             = http.HTTPStatus.FORBIDDEN
UPGRADE_REQUIRED      = http.HTTPStatus.UPGRADE_REQUIRED
BAD_REQUEST           = http.HTTPStatus.BAD_REQUEST
INTERNAL_SERVER_ERROR = http.HTTPStatus.INTERNAL_SERVER_ERROR
SERVICE_UNAVAILABLE   = http.HTTPStatus.SERVICE_UNAVAILABLE
SWITCHING_PROTOCOLS   = http.HTTPStatus.SWITCHING_PROTOCOLS

CONNECTING  = 'CONNECTING'
OPEN        = 'OPEN'
CLOSING     = 'CLOSING'
CLOSED      = 'CLOSED'

WS_KEY = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

EXTERNAL_CLOSE_CODES=(1000,1001,1002,1003,1007,1008,1009,1010,1011,)

HTTPClient = NotImplemented

class WebSocketCommonProtocol(ProtocolBase):
    __slots__ = ('_drain_lock', 'close_code', 'close_connection_task', 'close_reason', 'connection_lost_waiter',
        'extensions', 'host', 'max_queue', 'max_size', 'messages', 'over_ssl', 'pings', 'port', 'read_limit', 'secure',
        'source', 'state', 'subprotocol', 'timeout', 'transfer_data_exc', 'transfer_data_task', 'write_limit', )
    
    is_client = True #placeholder for subclasses
    
    def __init__(self, loop, host, port, *, secure=None, timeout=10.,
            max_size=1<<26, max_queue=None, read_limit=1<<16, write_limit=1<<16,
                ):
        
        ProtocolBase.__init__(self, loop)
        
        self.host = host
        self.port = port
        self.secure = secure
        self.timeout = timeout
        self.max_size = max_size #set it to a BIG number if u wanna ignore max size
        self.max_queue = max_queue
        self.read_limit = read_limit
        self.write_limit = write_limit
        
        self.over_ssl = False #we will set it later
        
        self._drain_lock = Lock(loop)
        
        self.state = CONNECTING
        
        self.extensions  = None #set from outside
        self.subprotocol = None #set from outside
        
        self.close_code = 0
        self.close_reason = None
        
        self.connection_lost_waiter=Future(loop)
        self.messages = AsyncQue(loop=loop,maxlen=max_queue)
        
        self.pings = OrderedDict()
        
        self.transfer_data_task = None
        self.transfer_data_exc = None
        self.close_connection_task = None
    
    def connection_open(self):
        self.state = OPEN
        self.transfer_data_task     = Task(self.transfer_data(),self.loop)
        self.close_connection_task  = Task(self.close_connection(),self.loop)
    
    @property
    def local_address(self):
        return self.get_extra_info('sockname')
    
    @property
    def remote_address(self):
        return self.get_extra_info('peername')
    
    @property
    def open(self):
        return self.state is OPEN and not self.transfer_data_task.done()
    
    @property
    def closed(self):
        return self.state is CLOSED
    
    #await it
    def recv(self):
        return self.messages.result()
    
    def recv_no_wait(self):
        return self.messages.result_no_wait()
    
    async def send(self,data):
        await self.ensure_open()
        
        if isinstance(data,(bytes,bytearray,memoryview)):
            opcode=WS_OP_BINARY
        elif type(data) is str:
            opcode=WS_OP_TEXT
            data=data.encode('utf-8')
        else:
            raise TypeError(f'data must be bytes or str, got: {data.__class__.__name__}')

        await self.write_frame(opcode,data)

    async def close(self, code=1000, reason=''):
        #if no close frame is received within the timeout
        #we cancel the connection
        try:
            task=Task(self.write_close_frame(self._serialize_close(code,reason)),self.loop)
            future_or_timeout(task,self.timeout)
            await task
        except TimeoutError:
            self.fail_connection()

        try:
            #if close() is cancelled durlng the wait, self.transfer_data_task
            #is cancelled before the timeout elapses
            task=self.transfer_data_task
            future_or_timeout(task,self.timeout)
            await task
        except (TimeoutError,CancelledError):
            pass
        
        #quit for the close connection task to close the TCP connection.
        await shield(self.close_connection_task,self.loop)

    @staticmethod
    def _serialize_close(code,reason):
        if not (code in EXTERNAL_CLOSE_CODES or 2999<code<5000):
            raise WebSocketProtocolError(f'Invalid status code {code}')
        return code.to_bytes(2,'big')+reason.encode('utf-8')
    
    async def ping(self,data=b''):
        await self.ensure_open()
        
        if type(data) is str:
            data.encode('utf-8')
        
        # Protect against duplicates if a payload is explicitly set.
        if data in self.pings:
            raise ValueError('Already waiting for a pong with the same data')
        
        # Generate a unique random payload otherwise.
        while data in self.pings:
            data=getrandbits(32).to_bytes(4,'big')
        
        self.pings[data]=Future(self.loop)
        
        await self.write_frame(WS_OP_PING,data)
        
        return shield(self.pings[data],self.loop)
    
    async def pong(self,data=b''):
        await self.ensure_open()
        if type(data) is str:
            data.encode('utf-8')
        await self.write_frame(WS_OP_PONG,data)
    
    # Private methods - no guarantees.
    
    async def ensure_open(self):
        if self.state is OPEN:
            #if self.transfer_data_task exited without a closing handshake.
            if self.transfer_data_task.done():
                await shield(self.close_connection_task,self.loop)
                raise ConnectionClosed(self.close_code,None,self.close_reason)
            return
        
        if self.state is CLOSED:
            raise ConnectionClosed(self.close_code,None,self.close_reason) from self.transfer_data_exc
        
        if self.state is CLOSING:
            if not self.close_code:
                #if we started the closing handshake, wait for its completion
                await shield(self.close_connection_task,self.loop)
            raise ConnectionClosed(self.close_code,None,self.close_reason) from self.transfer_data_exc

        raise Exception('WebSocket connection isn\'t established yet')
    
    async def transfer_data(self):
        try:
            while True:
                message = await self.read_message()
                #exit the loop when receiving a close frame.
                if message is None:
                    break
                
                self.messages.set_result(message)
        except CancelledError as err:
            #we alrady failed connection
            exception=ConnectionClosed(self.close_code or 1000, err, self.close_reason)
        
        except WebSocketProtocolError as err:
            exception=ConnectionClosed(1002,err)
            self.fail_connection(1002)
        
        except (ConnectionError, EOFError, TimeoutError) as err:
            exception=ConnectionClosed(1006,err)
            self.fail_connection(1006)
        
        except UnicodeDecodeError as err:
            exception=ConnectionClosed(1007,err)
            self.fail_connection(1007)
        
        except PayloadError as err:
            exception=ConnectionClosed(1009,err)
            self.fail_connection(1009)
        
        except BaseException as err:
            await self.loop.render_exc_async(err, [
                'Unexpected exception occured at ',
                repr(self),
                '.transfer_data\n',
                    ])
            #should not happen
            exception=ConnectionClosed(1011,err)
            self.fail_connection(1011)
        
        else:
            # connection wa closed
            exception = ConnectionClosed(self.close_code or 1000, None, self.close_reason)
            
            # If we are a client and we receive this, we closed our own
            # connection, there is no reason to wait for TCP abort
            if self.is_client:
                self.connection_lost_waiter.set_result_if_pending(None)
        
        if self.transfer_data_exc is None:
            self.transfer_data_exc=exception
            self.messages.set_exception(exception)
    
    async def read_message(self):
        frame = await self.read_data_frame(max_size=self.max_size)
        if frame is None: #close frame
            return
        
        if frame.opcode == WS_OP_TEXT:
            text = True
        elif frame.opcode == WS_OP_BINARY:
            text = False
        else: #frame.opcode == OP_CONT:
            raise WebSocketProtocolError('Unexpected opcode')
        
        #we got a whole frame, nice
        if frame.fin:
            return frame.data.decode('utf-8') if text else frame.data
        
        max_size=self.max_size #set max size to BIG number to ignore it
        chunks=[]
        
        if text:
            decoder = codecs.getincrementaldecoder('utf-8')(errors='strict')
            append=lambda frame : chunks.append(decoder.decode(frame.data,frame.fin))
        else:
            append=lambda frame : chunks.append(frame.data)
        
        while True:
            append(frame)
            max_size-=len(frame.data)

            if frame.fin:
                break
            
            frame = await self.read_data_frame(max_size=max_size)
            if frame is None:
                raise WebSocketProtocolError('Incomplete fragmented message')
            if frame.opcode!=WS_OP_CONT:
                raise WebSocketProtocolError('Unexpected opcode')
        
        return ('' if text else b'').join(chunks)
    
    async def read_data_frame(self,max_size):
        while True:
            
            frame = await self.set_payload_reader(self.read_websocket_frame(self.is_client, max_size))
            
            extensions = self.extensions
            if (extensions is not None):
                for extension in reversed(extensions):
                    frame = extension.decode(frame,max_size=max_size)
            
            frame.check()
            
            #most likely
            if frame.opcode in WS_DATA_OPCODES:
                return frame

            if (await self._process_CTRL_frame(frame)):
                continue
            
            return
    
    async def _process_CTRL_frame(self,frame):
        opcode=frame.opcode
        if opcode==WS_OP_CLOSE:
            data=frame.data
            length=len(data)
            if length>=2:
                code=int.from_bytes(data[:2],'big')
                if not (code in EXTERNAL_CLOSE_CODES or 2999<code<5000):
                    raise WebSocketProtocolError(f'Invalid status code {code}')
                reason=data[2:].decode('utf-8')
                self.close_code=code
                self.close_reason=reason
            elif length==0:
                self.close_code=1005
            else:
                raise WebSocketProtocolError(f'Close frame too short: {length}')

            await self.write_close_frame(frame.data)
            return False
        
        if opcode==WS_OP_PING:
            await self.pong(frame.data)
            return True
        
        #opcode==OP_PONG:
        if frame.data in self.pings:
            #checking all pings up to the one matching this pong.
            ping_id=b''
            while ping_id!=frame.data:
                ping_id,pong_waiter=self.pings.popitem(0)
                pong_waiter.set_result(None)
        return True
    
    async def write_frame(self,opcode,data,_expected_state=OPEN):
        # Defensive assertion for protocol compliance.
        if self.state is not _expected_state:
            raise Exception(f'Cannot write to a WebSocket in the {self.state} state')

        #we write only 1 frame at a time, so we 'queue' it
        async with self._drain_lock:
            try:
                frame=Frame(True,opcode,data)
                
                extensions = self.extensions
                if (extensions is not None):
                    for extension in extensions:
                        frame = extension.encode(frame)
                    
                    frame.check()
                
                self.write_websocket_frame(frame, self.is_client)
                await self.drain()
            except ConnectionError:
                self.fail_connection()
                #raise ConnectionClosed with the correct code and reason.
                await self.ensure_open()

    async def write_close_frame(self, data=b''):
        #check connection before we write
        if self.state is OPEN:
            self.state = CLOSING
            await self.write_frame(WS_OP_CLOSE, data, CLOSING)

    async def close_connection(self):
        try:
            # Wait for the data transfer phase to complete.
            transfer_data_task = self.transfer_data_task
            if (transfer_data_task is not None):
                try:
                    await transfer_data_task
                except (CancelledError,TimeoutError):
                    pass
            
            # Cancel all pending pings because they'll never receive a pong.
            for ping in self.pings.values():
                ping.cancel()
            
            # A client should wait for a TCP close from the server.
            if self.is_client and (self.transfer_data_task is not None):
                if (await self.wait_for_connection_lost()):
                    return
            
            if self.can_write_eof():
                self.write_eof()
                if (await self.wait_for_connection_lost()):
                    return
        finally:
            #finally ensures that the transport never remains open
            if self.connection_lost_waiter.done() and not self.secure:
                return
            
            #Close the TCP connection
            transport = self.transport
            if (transport is not None):
                transport.close()
                if (await self.wait_for_connection_lost()):
                    return
                #Abort the TCP connection
                transport.abort()
            #connection_lost() is called quickly after aborting.
            await self.wait_for_connection_lost()
            
    async def wait_for_connection_lost(self):
        if self.connection_lost_waiter.pending():
            try:
                task=shield(self.connection_lost_waiter,self.loop)
                future_or_timeout(task,self.timeout)
                await task
            except TimeoutError:
                pass
        
        #re-check self.connection_lost_waiter.done() synchronously because
        #connection_lost() could run between the moment the timeout occurs
        #and the moment this coroutine resumes running.
        return self.connection_lost_waiter.done()

    def fail_connection(self, code=1006, reason=''):
        #cancel transfer_data_task if the opening handshake succeeded
        transfer_data_task = self.transfer_data_task
        if transfer_data_task is not None:
            transfer_data_task.cancel()
        
        #send a close frame when the state is OPEN and the connection is not
        #broken
        if code!=1006 and self.state is OPEN:

            frame_data = self._serialize_close(code,reason)
            #Write the close frame without draining the write buffer.
            self.state = CLOSING
            
            frame = Frame(True,WS_OP_CLOSE,frame_data)
            
            extensions = self.extensions
            if (extensions is not None):
                for extension in extensions:
                    frame = extension.encode(frame)
                
                frame.check()
            
            self.write_websocket_frame(frame, self.is_client)
        
        #start close_connection_task if the opening handshake didn't succeed.
        close_task=self.close_connection_task
        if close_task is None:
            close_task=Task(self.close_connection(),self.loop)
            self.close_connection_task=close_task
            
        return close_task
    
    #compability method (overwrite)
    def connection_made(self, transport):
        transport.set_write_buffer_limits(self.write_limit)
        self.over_ssl = (transport.get_extra_info('sslcontext') is not None)
        self.transport = transport
    
    #compability method (overwrite)
    def connection_lost(self, exception):
        self.state = CLOSED
        if not self.close_code:
            self.close_code = 1006
        
        # `self.connection_lost_waiter` should be pending
        self.connection_lost_waiter.set_result_if_pending(None)
        
        ProtocolBase.connection_lost(self, exception)
    
    #compability method (overwrite)
    def eof_received(self):
        ProtocolBase.eof_received(self)
        return (not self.over_ssl)

class WSClient(WebSocketCommonProtocol):
    is_client = True
    
    async def __new__(cls, loop, url, *, origin=None, available_extensions=None, available_subprotocols=None,
            extra_headers=None, compression=None, connection_kwargs=None, websocket_kwargs=None, http_client=None, ):
        
        if http_client is None:
            http_client = HTTPClient(loop)
        
        if connection_kwargs is None:
            connection_kwargs={}
        if websocket_kwargs is None:
            websocket_kwargs={}
        
        url = URL(url)
        secure = (url.scheme == 'wss')
        if secure:
            connection_kwargs.setdefault('ssl',True)
        elif connection_kwargs.get('ssl',None) is not None:
            raise ValueError(f'{cls.__name__} received a SSL context for a ws:// URI, use a wss:// URI to enable TLS')
        
        if compression is not None and compression!='deflate':
            raise ValueError(f'Unsupported compression: {compression}')
        
        if connection_kwargs.get('sock') is None:
            host=url.host
            port=url.port
        else:
            #if sock is given, host and port must be None
            host=None
            port=None
        
        #building headers
        sec_key=b64encode(int.to_bytes(getrandbits(128),length=16,byteorder='big')).decode()
        request_headers = multidict_titled()
        
        request_headers[UPGRADE]='websocket'
        request_headers[CONNECTION]='Upgrade'
        request_headers[SEC_WEBSOCKET_KEY]=sec_key
        request_headers[SEC_WEBSOCKET_VERSION]='13'
        
        if url.port == (443 if secure else 80):
            request_headers[HOST] = url.host
        else:
            request_headers[HOST] = f'{url.host}:{url.port}'
        
        user = url.user
        password = url.password
        if (user is not None) or (password is not None):
            request_headers[AUTHORIZATION]=build_basic_auth(user, password)
        
        if origin is not None:
            request_headers[ORIGIN]=origin

        if available_extensions is not None:
            request_headers[SEC_WEBSOCKET_EXTENSIONS]=build_extensions(available_extensions)
            
        if available_subprotocols is not None:
            request_headers[SEC_WEBSOCKET_PROTOCOL]=build_subprotocols(available_subprotocols)

        if extra_headers is not None:
            if isinstance(extra_headers,multidict_titled) or hasattr(extra_headers,'items'): #we use expecially items, so we check that
                for name,value in extra_headers.items():
                    request_headers[name]=value
            else:
                raise TypeError(f'extra_headers should be dictlike with \'.items\' method, got {extra_headers.__class__.__name__} instance.')
        
        async with http_client.request(METH_GET, url, request_headers) as response:
           
            if response.raw_message.version != HttpVersion11:
                raise ValueError(f'Unsupported HTTP version: {response.raw_message.version}')
            
            if response.status!=101:
                raise InvalidHandshake(f'Invalid status code: {response.status}')
            
            response_headers = response.headers
            connections=[]
            received_connections=response_headers.getall(CONNECTION,)
            if (received_connections is not None):
                for received_connection in received_connections:
                    connections.extend(parse_connections(received_connection))
            
            if not any(value.lower()=='upgrade' for value in connections):
                raise InvalidHandshake(f'Invalid connection, no upgrade found, got {connections!r}')
            
            upgrade=[]
            received_upgrades=response_headers.getall(UPGRADE)
            if (received_upgrades is not None):
                for received_upgrade in received_upgrades:
                    upgrade.extend(parse_upgrades(received_upgrade))
            
            if len(upgrade)!=1 and upgrade[0].lower()!='websocket': #ignore upper/lover case
                raise InvalidHandshake(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}')
            
            expected_key=b64encode(hashlib.sha1((sec_key+WS_KEY).encode()).digest()).decode()
            received_keys=response_headers.getall(SEC_WEBSOCKET_ACCEPT)
            if received_keys is None:
                raise InvalidHandshake(f'Expected 1 secret key \'{expected_key}\', but received 0')
            if len(received_keys)>1:
                raise InvalidHandshake(f'Expected 1 secret key \'{expected_key}\', but received more : {received_keys}')
            
            received_key=received_keys[0]
            if received_key!=expected_key:
                raise InvalidHandshake(f'Expected secret key \'{expected_key}\', but got \'{received_key}\'')

            #extensions
            accepted_extensions=[]
            received_extensions=response_headers.getall(SEC_WEBSOCKET_EXTENSIONS)
            if (received_extensions is not None):
                if available_extensions is None:
                    raise InvalidHandshake(f'No extensions supported, but received {received_extensions!r}')
                
                parsed_extension_values=[]
                for value in received_extensions:
                    parsed_extension_values.extend(parse_extensions(value))
                
                for name,params in parsed_extension_values:
                    for extension in available_extensions:
                        #do names and params match?
                        if extension.name==name and extension.are_valid_params(params,accepted_extensions):
                            accepted_extensions.append(extension)
                            break
                    else:
                        #no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name = {name}, params = {params}')
            
            subprotocol = None
            received_subprotocols=response_headers.getall(SEC_WEBSOCKET_PROTOCOL)
            if (received_subprotocols is not None):
                if available_subprotocols is None:
                    raise InvalidHandshake('No subprotocols supported, btu received {received_subprotocol!r}')
                
                parsed_subprotocol_values=[]
                for received_subprotocol in received_subprotocols:
                    parsed_subprotocol_values.extend(parse_subprotocols(received_subprotocol))
                
                if len(parsed_subprotocol_values)>1:
                    raise InvalidHandshake(f'Multiple subprotocols: {parsed_subprotocol_values!r}')
                
                subprotocol=parsed_subprotocol_values[0]
                
                if subprotocol not in available_subprotocols:
                    raise InvalidHandshake(f'Unsupported subprotocol: {subprotocol}')
            
            connection = response.connection
            protocol = connection.protocol
            connection.detach()
            
            self = object.__new__(cls)
            WebSocketCommonProtocol.__init__(self, loop, host, port, **websocket_kwargs)
            protocol._copy_attrs_to(self)
            self.extensions = accepted_extensions
            self.subprotocol = subprotocol
            self.transport.set_protocol(self)
        
        self.connection_open()
        return self

class WSServerProtocol(WebSocketCommonProtocol):
    is_client = False
    
    __slots__ = ('available_extensions', 'available_subprotocols',
        'extra_headers', 'handler', 'handler_task', 'origin', 'origins',
        'request_processer', 'server', 'subprotocol_selector',
        'request', 'response_headers')
    
    def __init__(self,server):
        handler, host, port, secure, origins, available_extensions, \
        available_subprotocols , extra_headers, request_processer, \
        subprotocol_selector, websocket_kwargs = server.proto_args
        
        self.handler=handler
        self.server=server
        self.origins=origins
        self.available_extensions=available_extensions
        self.available_subprotocols=available_subprotocols
        self.extra_headers=extra_headers
        self.request_processer=request_processer
        self.subprotocol_selector=subprotocol_selector
        self.handler_task=None
        
        WebSocketCommonProtocol.__init__(self, server.loop, host, port,
            secure=secure, **websocket_kwargs)
        
        self.request=None
        self.response_headers=None
        self.origin=None
        
    def connection_made(self, transpot):
        WebSocketCommonProtocol.connection_made(self,transpot)
        self.server.register(self)
        self.handler_task=Task(self.lifetime_handler(),self.loop)
        
    async def lifetime_handler(self):
        try:
            # handshake returns True if it succeeded
            if not (await self.handshake()):
                return
            
            try:
                await self.handler(self)
            except BaseException as err:
                await self.loop.render_exc_async(err,before = [
                    'Unhandled exception occured at',
                    self.__class__.__name__,
                    '.lifetime_handler meanhile running: ',
                    repr(self.handler),
                    '\n',
                        ])
                return
            
            await self.close()
        except:
            # We will let Task.__del__ to render the exception...
            
            transport=self.transport
            if transport is None:
                raise
                
            transport.close()
            transport.abort()
            raise
        
        finally:
            self.server.unregister(self)
    
    async def handshake(self):
        try:
            self.request = request =await self.set_payload_reader(self.read_http_request())
            
            request_headers=request.headers
            if self.server.is_serving():
                path=request.path
                
                request_processer=self.request_processer
                if request_processer is None:
                    early_response=None
                else:
                    early_response=request_processer(path, request_headers)
                    if iscoroutine(early_response):
                        early_response=await early_response
                
                if (early_response is not None):
                    raise AbortHandshake(*early_response)
                
            else:
                raise AbortHandshake(SERVICE_UNAVAILABLE,multidict_titled(),b'Server is shutting down.\n',)
            
            connections=[]
            connection_headers=request_headers.getall(CONNECTION)
            if (connection_headers is not None):
                for connection_header in connection_headers:
                    connections.extend(parse_connections(connection_header))
        
            if not any(value.lower()=='upgrade' for value in connections):
                raise InvalidUpgrade(f'Invalid connection, no upgrade found, got {connections!r}')
            
            upgrade=[]
            upgrade_headers=request_headers.getall(UPGRADE)
            if (upgrade_headers is not None):
                for upgrade_header in upgrade_headers:
                    upgrade.extend(parse_upgrades(upgrade_header))
            
            if len(upgrade)!=1 and upgrade[0].lower()!='websocket': #ignore upper/lover case
                raise InvalidUpgrade(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}')
            
            received_keys=request_headers.getall(SEC_WEBSOCKET_KEY)
            if received_keys is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_KEY!r} from headers')
            
            if len(received_keys)>1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_KEY!r} values at headers')
            
            key=received_keys[0]
        
            try:
                raw_key = b64decode(key.encode(),validate=True)
            except BinasciiError:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}: {key!r}')
            
            if len(raw_key)!=16:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}, should be length 16; {key!r}')
        
            sw_version=request_headers.getall(SEC_WEBSOCKET_VERSION)
            if sw_version is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_VERSION!r} values at headers')
            
            if len(sw_version)>1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_VERSION!r} values at headers')
            
            sw_version=sw_version[0]
            if sw_version != "13":
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_VERSION!r}: {sw_version!r}')
            
            while True:
                origins=self.origins
                if (origins is None):
                    origin=None
                    break
                
                origin_headers=request_headers.getall(ORIGIN)
                
                if (origin_headers is None):
                    raise InvalidOrigin('No origin at header.')
                
                if len(origin_headers)>1:
                    raise InvalidOrigin('More than 1 origin at header.')
                
                origin=origin_headers[0]
                
                if origin in origins:
                    break
                    
                raise InvalidOrigin(origin)
            
            self.origin=origin
            
            while True:
                accepted_extensions=[]
                
                available_extensions=self.available_extensions
                if (available_extensions is None):
                    extension_header=None
                    break
                
                extension_headers_=request_headers.getall(SEC_WEBSOCKET_EXTENSIONS)
                if (extension_headers_ is None):
                    extension_header=None
                    break
                
                extension_headers=[]
                parsed_extension_values=[]
                for extension_header_ in extension_headers_:
                    parsed_extension_values.extend(parse_extensions(extension_header_))
                
                for name,params in parsed_extension_values:
                    for extension in available_extensions:
                        #do names and params match?
                        if extension.name==name and extension.are_valid_params(params,accepted_extensions):
                            accepted_extensions.append(extension)
                            extension_headers.append((name,params))
                            break
                    else:
                        #no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name = {name}, params = {params}')
                    
                    # If we didn't break from the loop, no extension in our list
                    # matched what the client sent. The extension is declined.
        
                # Serialize extension header.
                if extension_headers:
                    extension_header=build_extensions(extension_headers)
                    break
                
                extension_header=None
                break
            
            self.extensions=accepted_extensions
            
            
            while True:
                available_subprotocols=self.available_subprotocols
                if (available_subprotocols is None):
                    subprotocol_header=None
                    break
                    
                protocol_headers=request_headers.getall(SEC_WEBSOCKET_PROTOCOL)
                if (protocol_headers is None):
                    subprotocol_header=None
                    break
                
                parsed_header_subprotocols=[]
                for protocol_header in protocol_headers:
                    parsed_header_subprotocols.extend(parse_subprotocols(protocol_header))
                
                subprotocol_selector=self.subprotocol_selector
                if (subprotocol_selector is not None):
                    subprotocol_header=subprotocol_selector(parsed_header_subprotocols,available_subprotocols)
                    break
                    
                subprotocols=set(parsed_header_subprotocols)
                subprotocols.intersection_update(available_subprotocols)
                
                if not subprotocols:
                    subprotocol_header=None
                    break
                    
                subprotocol_header=sorted(subprotocols, key = lambda priority: (parsed_header_subprotocols.index(priority)+available_subprotocols.index(priority)))[0]
                break
            
            self.subprotocol=subprotocol_header
            
            response_headers = multidict_titled()
    
            response_headers[UPGRADE] = 'websocket'
            response_headers[CONNECTION] = 'Upgrade'
            response_headers[SEC_WEBSOCKET_ACCEPT] = b64encode(hashlib.sha1((key+WS_KEY).encode()).digest()).decode()
            
            if (extension_header is not None):
                response_headers[SEC_WEBSOCKET_EXTENSIONS] = extension_header
    
            if (subprotocol_header is not None):
                response_headers[SEC_WEBSOCKET_PROTOCOL] = subprotocol_header
            
            extra_headers=self.extra_headers
            if (extra_headers is not None):
                for key, value in extra_headers.items():
                    response_headers[key] = value
    
            response_headers.setdefault(DATE, formatdate(usegmt=True))
            response_headers.setdefault(SERVER, '')
            
            self.response_headers = response_headers
            self.write_http_response(SWITCHING_PROTOCOLS, response_headers)
            
            self.connection_open()
        except (CancelledError, ConnectionError) as err:
            await self.loop.render_exc_async(err,before = [
                'Unhandled exception occured at ',
                self.__class__.__name__,
                '.handshake, when handshaking:\n'])
            return False
        except BaseException as err:
            if isinstance(err,AbortHandshake):
                status=err.status
                headers=err.headers
                body=err.body
            elif isinstance(err,InvalidOrigin):
                status=FORBIDDEN
                headers=multidict_titled()
                body=f'Failed to open a WebSocket connection: {err}.\n'.encode()
            elif isinstance(err,InvalidUpgrade):
                status=UPGRADE_REQUIRED
                headers=multidict_titled()
                headers[UPGRADE]='websocket'
                body = (
                    f'Failed to open a WebSocket connection: {err}.\n\n'
                    f'You cannot access a WebSocket server directly with a '
                    f'browser. You need a WebSocket client.\n'
                        ).encode()
            elif isinstance(err,InvalidHandshake):
                status=BAD_REQUEST
                headers=multidict_titled()
                body=f'Failed to open a WebSocket connection: {err}.\n'.encode()
            else:
                status=INTERNAL_SERVER_ERROR
                headers=multidict_titled()
                body=b'Failed to open a WebSocket connection.\n'
                
            headers.setdefault(DATE             , formatdate(usegmt=True))
            headers.setdefault(SERVER           , '')
            headers.setdefault(CONTENT_LENGTH   , repr(len(body)))
            headers.setdefault(CONTENT_TYPE     , 'text/plain')
            headers.setdefault(CONNECTION       , 'close')
            
            try:
                self.write_http_response(status, headers, body=body)
                self.fail_connection()
                await self.wait_for_connection_lost()
            except BaseException as err2:
                await self.loop.render_exc_async(err2,before = [
                    'Unhandled exception occured at ',
                    self.__class__.__name__,
                    '.handshake, when handling an other exception;',
                    repr(err),':'])
            return False
        
        return True

    def __setattr__(self, name, value):
        counter = getattr(type(self),'counter',0)
        if name =='payload_reader' and value is None and counter==0:
            raise RuntimeError
        
        type(self).counter = counter+1
        object.__setattr__(self, name, value)

class WSServer(object):
    __slots__ = ('loop', 'websockets', 'close_connection_task','handler', 'server', 'proto_args')
    async def __new__(cls, loop, host, port, handler, *, protocol=None,
            compression=None, available_extensions=None, extra_headers=None,
            origins=None, available_subprotocols=None, request_processer=None,
            subprotocol_selector=None, websocket_kwargs=None, **kwargs):
        
        if protocol is None:
            protocol=WSServerProtocol
        
        if websocket_kwargs is None:
            websocket_kwargs={}
        
        secure = (kwargs.get("ssl") is not None)
        
        if (compression is not None):
            if compression!='deflate':
                raise ValueError(f'Unsupported compression: {compression}')
        
            if available_extensions is None:
                available_extensions=[]
        
        if (extra_headers is None):
            pass
        elif type(extra_headers) is multidict_titled:
            pass
        elif hasattr(type(extra_headers),'items'):
            extra_headers_local=multidict_titled()
            
            for name,value in extra_headers.items():
                extra_headers_local[name]=value
            
            extra_headers=extra_headers_local
        else:
            raise TypeError(f'extra_headers should be `None` or a dictlike with \'.items\' method, got {extra_headers.__class__.__name__} instance.')
        
        if (extra_headers is not None) and (not extra_headers):
            extra_headers=None
        
        self=object.__new__(cls)
        self.loop=loop
        self.handler=handler
        self.websockets=set()
        self.close_connection_task=None
        self.server = None
        self.proto_args = (handler, host, port, secure, origins,
            available_extensions, available_subprotocols , extra_headers,
            request_processer, subprotocol_selector, websocket_kwargs)
        
        factory = functools.partial(protocol, self,)
        server = await loop.create_server(factory, host, port, **kwargs)
        
        self.server = server
        await server.start()
        
        return self
    
    def register(self,protocol):
        self.websockets.add(protocol)
    
    def unregister(self, protocol):
        try:
            self.websockets.remove(protocol)
        except KeyError:
            pass
    
    def is_serving(self):
        server=self.server
        if server is None:
            return False
        
        if server.sockets is None:
            return False
        
        return True
    
    def close(self):
        close_connection_task = self.close_connection_task
        if close_connection_task is None:
            close_connection_task=Task(self._close(),self.loop)
            self.close_connection_task=close_connection_task
        
        return close_connection_task
    
    async def _close(self):
        server=self.server
        if server is None:
            return
        
        server.close()
        await server.wait_closed()
        
        loop=self.loop
        
        # Skip 1 full loop
        future=Future(loop)
        loop.call_at(0.0,Future.set_result_if_pending,future,None)
        await future
        
        websockets=self.websockets
        if websockets:
            await WaitTillAll([websocket.close(1001) for websocket in websockets],loop)
            
        if websockets:
            await WaitTillAll([websocket.handler_task for websocket in websockets],loop)

del http
