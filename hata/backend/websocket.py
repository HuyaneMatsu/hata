__all__ = ('WSClient', 'WSServer', )

import hashlib, codecs
import http as module_http
from base64 import b64encode, b64decode
from collections import OrderedDict
from binascii import Error as BinasciiError
from email.utils import formatdate
from os import urandom
from functools import partial as partial_func

from .utils import imultidict
from .futures import Future, Task, AsyncQueue, future_or_timeout, shield, CancelledError, WaitTillAll, is_coroutine, Lock
from .export import include

from .url import URL
from .headers import CONNECTION, SEC_WEBSOCKET_KEY, AUTHORIZATION, SEC_WEBSOCKET_VERSION, build_subprotocols, \
    SEC_WEBSOCKET_EXTENSIONS, SEC_WEBSOCKET_PROTOCOL, HOST, ORIGIN, SEC_WEBSOCKET_ACCEPT, UPGRADE, DATE, METHOD_GET, \
    CONTENT_TYPE, SERVER, CONTENT_LENGTH, build_extensions, parse_subprotocols, parse_upgrades, \
    parse_connections, parse_extensions
from .exceptions import PayloadError, InvalidUpgrade, AbortHandshake, ConnectionClosed, InvalidHandshake, \
    InvalidOrigin, WebSocketProtocolError
from .helpers import HttpVersion11, BasicAuth
from .protocol import ProtocolBase, WS_OP_CONT, WS_OP_TEXT, WS_OP_BINARY , WS_OP_CLOSE, WS_OP_PING, WS_OP_PONG, \
    WS_DATA_OPCODES, WS_CTRL_OPCODES, Frame

FORBIDDEN = module_http.HTTPStatus.FORBIDDEN
UPGRADE_REQUIRED = module_http.HTTPStatus.UPGRADE_REQUIRED
BAD_REQUEST = module_http.HTTPStatus.BAD_REQUEST
INTERNAL_SERVER_ERROR = module_http.HTTPStatus.INTERNAL_SERVER_ERROR
SERVICE_UNAVAILABLE = module_http.HTTPStatus.SERVICE_UNAVAILABLE
SWITCHING_PROTOCOLS = module_http.HTTPStatus.SWITCHING_PROTOCOLS

CONNECTING = 'CONNECTING'
OPEN = 'OPEN'
CLOSING = 'CLOSING'
CLOSED = 'CLOSED'

WS_KEY = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

EXTERNAL_CLOSE_CODES = (1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011,)

HTTPClient = include('HTTPClient')

DECODER = codecs.getincrementaldecoder('utf-8')(errors='strict')


class WebSocketCommonProtocol(ProtocolBase):
    """
    Websocket protocol base which implements common functions between the client and the server side.
    
    Attributes
    ----------
    _chunks : `deque` of `bytes`
        Right feed, left pop queue, used to store the received data chunks.
    _eof : `bool`
        Whether the protocol received end of file.
    _offset : `int`
        Byte offset, of the used up data of the most-left chunk.
    _paused : `bool`
        Whether the protocol's respective transport's reading is paused. Defaults to `False`.
        
        Also note, that not every transport supports pausing.
    exception : `None` or `BaseException`
        Exception set by ``.set_exception``, when an unexpected exception occurs meanwhile reading from socket.
    loop : ``EventThread``
        The event loop to what the protocol is bound to.
    payload_reader : `None` or `generator`
        Payload reader generator, what gets the control back, when data, eof or any exception is received.
    payload_waiter : `None` of ``Future``
        Payload waiter of the protocol, what's result is set, when the ``.payload_reader`` generator returns.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    transport : `None` or `Any`
        Asynchronous transport implementation. Is set meanwhile the protocol is alive.
    _drain_waiter : `None` or ``Future``
        A future, what is used to block the writing task, till it's writen data is drained.
    _drain_lock : ``Lock``
        Asynchronous lock to ensure, that only `1` frame is written in `1` time.
    close_code : `int`
        The websocket's close code if applicable. Defaults to `0`.
    close_connection_task : `None` or ``Task`` of ``.close_connection``
        A task, what is present meanwhile the websocket is closing to avoid race condition.
    close_timeout : `float`
        The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
    close_reason : `None` or `str`
        The reason, why the websocket was closed. Set only after the websocket is closed. Close reason might not be
        received tho.
    connection_lost_waiter : ``Future``
        A future, what's result is set as `None`, when the connection is closed. Used to wait for close frames.
        
        ``shield`` it if using from outside.
    extensions : `None` or (`list` of `Any`)
        Websocket extensions. Defaults to `None`, if there is not any.
    host : `str`
        The respective server's address to connect to.
    max_queue : `None` or `int`
        Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is removed.
         Defaults to `None`.
    max_size : `int`
        Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864` bytes.
    messages : ``AsyncQueue``
        An asynchronous queue of the received messages.
    is_ssl : `bool`
        Whether the connection is secure. Defaults to `False`.
    pings : `OrderedDict` of (`bytes`, ``Future``) items
        An ordered dictionary of ping payloads and of their waiter futures.
    port : `int`
        The respective server's port to connect to.
    state : `str`
        The websocket's state.
        
        Can be set as one of the following values:
        
        +-------------------+-------------------+
        | Respective name   | Value             |
        +===================+===================+
        | CONNECTING        | `'CONNECTING'`    |
        +-------------------+-------------------+
        | OPEN              | `'OPEN'`          |
        +-------------------+-------------------+
        | CLOSING           | `'CLOSING'`       |
        +-------------------+-------------------+
        | CLOSED            | `'CLOSED'`        |
        +-------------------+-------------------+
        
        Note, that state is compared by memory address and not by value.
    subprotocol : `None`, `str`
        Chosen subprotocol at handshake. Defaults to `None` and might be set as `str`. Chosen from the available
        subprotocols by their priority order.
    transfer_data_exc : `None` or `BaseException``
        Exception catched meanwhile processing received data.
    transfer_data_task : `None` or ``Task`` of ``.transfer_data``
        Data receiving task.
    
    Class Attributes
    ----------------
    is_client : `bool` = `True`
        Whether the websocket protocol is client or server side.
    """
    __slots__ = ('_drain_lock', 'close_code', 'close_connection_task', 'close_timeout', 'close_reason',
        'connection_lost_waiter', 'extensions', 'host', 'is_ssl', 'max_queue', 'max_size', 'messages', 'pings', 'port',
        'state', 'subprotocol', 'transfer_data_exc', 'transfer_data_task', )
    
    is_client = True # placeholder for subclasses
    
    def __init__(self, loop, host, port, *, is_ssl=False, close_timeout=10., max_size=1<<26, max_queue=None):
        """
        Initializes the ``WebSocketCommonProtocol`` with setting it's common attributes.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop, what the protocol uses for it's asynchronous tasks.
        host : `str`
            The respective server's address to connect to.
        port : `int`
            The respective server's port to connect to.
        is_ssl : `bool`, Optional (Keyword only)
            Whether the connection is secure. Defaults to `False`.
        close_timeout : `float`, Optional (Keyword only)
            The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
        max_size : `int`, Optional (Keyword only)
            Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864`
            bytes.
        max_queue : `None` or `int`, Optional (Keyword only)
            Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is
            removed. Defaults to `None`.
        """
        ProtocolBase.__init__(self, loop)
        
        self.host = host
        self.port = port
        self.is_ssl = is_ssl
        self.close_timeout = close_timeout
        self.max_size = max_size # set it to a BIG number if u wanna ignore max size
        self.max_queue = max_queue
        
        self._drain_lock = Lock(loop)
        
        self.state = CONNECTING
        
        self.extensions = None # set from outside
        self.subprotocol = None # set from outside
        
        self.close_code = 0
        self.close_reason = None
        
        self.connection_lost_waiter = Future(loop)
        self.messages = AsyncQueue(loop=loop, max_length=max_queue)
        
        self.pings = OrderedDict()
        
        self.transfer_data_task = None
        self.transfer_data_exc = None
        self.close_connection_task = None
    
    def connection_open(self):
        """
        Method called when the connection is established at the end of the handshake.
        
        Marks the websocket as open and start it's ``.transfer_data_task`` and ``.close_connection_task``.
        """
        self.state = OPEN
        loop = self.loop
        self.transfer_data_task = Task(self.transfer_data(), loop)
        self.close_connection_task = Task(self.close_connection(), loop)
    
    @property
    def local_address(self):
        """
        Local address of the connection as a `tuple` of host and port. If the connection is not open yet, returns
        `None`.
        
        Returns
        -------
        local_address : `None` or `tuple` of (`str`, `int`)
        """
        return self.get_extra_info('sockname')
    
    @property
    def remote_address(self):
        """
        Remote address of the connection as a `tuple` of host and port. If the connection is not open yet, returns
        `None`.
        
        Returns
        -------
        remote_address : `None` or `tuple` of (`str`, `int`)
        """
        return self.get_extra_info('peername')
    
    @property
    def open(self):
        """
        Returns whether the websocket is open.
        
        If the websocket is closed, ``ConnectionClosed`` is raised when using it.
        
        Returns
        -------
        open : `bool`
        """
        if self.state is not OPEN:
            return False
        
        transfer_data_task = self.transfer_data_task
        if transfer_data_task is None:
            return False
        
        if self.transfer_data_task.done():
            return False
        
        return True
    
    @property
    def closed(self):
        """
        Returns whether the websocket is closed.
        
        Note, meanwhile connection is establishing, ``.open`` and ``.close`` will return `False`.
        
        Returns
        -------
        closed : `bool`
        """
        return self.state is CLOSED
    
    def receive(self):
        """
        Returns a future, what can be awaited to receive the next message of the websocket.
        
        Returns
        -------
        future : ``Future``
            The future returns `bytes` or `str` instance respective to the received payload's type. If the websocket
            is closed, ``ConnectionClosed`` is raised.
        """
        return self.messages.result()
    
    def receive_no_wait(self):
        """
        Returns a future, what can be awaited to receive the next message of the websocket.
        
        Returns
        -------
        message : `bytes` or `str`
            The received payload.
        
        Raises
        ------
        IndexError
            There are no messages to retrieve right now.
        ConnectionClosed
            Websocket closed.
        """
        return self.messages.result_no_wait()
    
    async def send(self, data):
        """
        Sends the given data with the websocket.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `bytes-like` or `str`
            The data to send
        
        Raises
        ------
        TypeError
            `data` was not given as `bytes-like`, neither as `str`.
        ConnectionClosed
            Websocket connection closed.
        Exception
            Websocket connection not yet established.
        """
        await self.ensure_open()
        
        if isinstance(data, (bytes, bytearray, memoryview)):
            op_code = WS_OP_BINARY
        elif isinstance(data, str):
            op_code = WS_OP_TEXT
            data = data.encode('utf-8')
        else:
            raise TypeError(f'Data must be `bytes-like` or `str`, got: {data.__class__.__name__}.')

        await self.write_frame(op_code, data)

    async def close(self, code=1000, reason=''):
        """
        Closes the websocket.
        
        Writes close frame first and then if we don't receive close frame response in ``.close_timeout``, then we
        cancel the connection.
        
        This method is a coroutine.
        
        Parameters
        ----------
        code : `int`, Optional.
            Websocket close code. Defaults to `1000`. Can be one of:
            `(1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011) | [3000:5000)`.
        reason : `str`, Optional
            Websocket close reason. Can be given as empty string. Defaults to empty string as well.
        
        Raises
        ------
        WebSocketProtocolError
            Close code is not given as one of `(1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011) | [3000:5000)`.
        """
        # if no close frame is received within the close_timeout we cancel the connection
        close_message = self._serialize_close(code, reason)
        try:
            task = Task(self.write_close_frame(close_message), self.loop)
            future_or_timeout(task, self.close_timeout)
            await task
        except TimeoutError:
            self.fail_connection()
        
        try:
            # if close() is cancelled during the wait, self.transfer_data_task is cancelled before the close_timeout
            # elapses
            task = self.transfer_data_task
            future_or_timeout(task, self.close_timeout)
            await task
        except (TimeoutError, CancelledError):
            pass
        
        # quit for the close connection task to close the TCP connection.
        await shield(self.close_connection_task, self.loop)
    
    @staticmethod
    def _serialize_close(code, reason):
        """
        Packs the given `code` and `reason` together into a close message.
        
        Parameters
        ----------
        code : `int`
            Websocket close code. Can be one of:
            `(1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011) | [3000:5000)`.
        reason : `str`
            Websocket close reason. Can be given as empty string.
        
        Returns
        -------
        close_message : `bytes`
        
        Raises
        ------
        WebSocketProtocolError
            Close code is not given as one of `(1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011) | [3000:5000)`.
        """
        if not (code in EXTERNAL_CLOSE_CODES or 2999<code<5000):
            raise WebSocketProtocolError(f'Status can be in range [3000:5000), got {code!r}.')
        return code.to_bytes(2, 'big')+reason.encode('utf-8')
    
    async def ping(self, data=None):
        """
        Sends a ping to the other side and waits till answer is received.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `None`, `bytes-like`, `str`
            Ping payload to send. Defaults to `None`.
            
            If the given or generated payload is already waiting for response, then will regenerate it, till a free
            one is hit.
        
        Raises
        ------
        TypeError
            `data` is not given neither as `None`, `bytes-like`, or `str` instance.
        ConnectionClosed
            Websocket connection closed.
        Exception
            Websocket connection not yet established.
        """
        await self.ensure_open()
        
        if data is None:
            data = urandom(4)
        elif isinstance(data, (bytes, bytearray, memoryview)):
            pass
        elif isinstance(data, str):
            data = data.encode('utf-8')
        else:
            raise TypeError(f'Data must be `bytes-like` or `str`, got: {data.__class__.__name__}.')
        
        pings = self.pings
        while data in pings:
            data = urandom(4)
        
        waiter = Future(self.loop)
        pings[data] = waiter
        
        await self.write_frame(WS_OP_PING, data)
        
        await waiter
    
    async def pong(self, data=None):
        """
        Sends a pong payload to the other side.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `None`, `bytes-like`, `str`
            Ping payload to send. Defaults to `None`.
        
        Raises
        ------
        TypeError
            `data` is not given neither as `None`, `bytes-like`, or `str` instance.
        ConnectionClosed
            Websocket connection closed.
        Exception
            Websocket connection not yet established.
        """
        await self.ensure_open()
        
        if data is None:
            data = urandom(4)
        elif isinstance(data, (bytes, bytearray, memoryview)):
            pass
        elif isinstance(data, str):
            data = data.encode('utf-8')
        else:
            raise TypeError(f'Data must be `bytes-like` or `str`, got: {data.__class__.__name__}.')
        
        await self.write_frame(WS_OP_PONG, data)
    
    # Private methods - no guarantees.
    
    async def ensure_open(self):
        """
        Checks whether the websocket is still open.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionClosed
            Websocket connection closed.
        Exception
            Websocket connection not yet established.
        """
        state = self.state
        if state is OPEN:
            # if self.transfer_data_task exited without a closing handshake.
            if self.transfer_data_task.done():
                await shield(self.close_connection_task, self.loop)
                raise ConnectionClosed(self.close_code, None, self.close_reason)
            return
        
        if state is CLOSED:
            raise ConnectionClosed(self.close_code, None, self.close_reason) from self.transfer_data_exc
        
        if state is CLOSING:
            if not self.close_code:
                #if we started the closing handshake, wait for its completion
                await shield(self.close_connection_task, self.loop)
            raise ConnectionClosed(self.close_code, None, self.close_reason) from self.transfer_data_exc
        
        raise Exception('WebSocket connection isn\'t established yet.')
    
    async def transfer_data(self):
        """
        The transfer data task of a websocket keeps reading it's messages and putting it into it's ``.messages``
        ``AsyncQueue``.
        
        Meanwhile runs, it wrapped inside of a ``Task`` and can be accessed as ``.transfer_data_task``.
        
        This method is a coroutine.
        """
        try:
            while True:
                message = await self.read_message()
                # exit the loop when receiving a close frame.
                if message is None:
                    break
                
                self.messages.set_result(message)
        except CancelledError as err:
            # we already failed connection
            exception = ConnectionClosed(self.close_code or 1000, err, self.close_reason)
        
        except WebSocketProtocolError as err:
            exception = ConnectionClosed(1002, err)
            self.fail_connection(1002)
        
        except (ConnectionError, EOFError, TimeoutError) as err:
            exception = ConnectionClosed(1006, err)
            self.fail_connection(1006)
        
        except UnicodeDecodeError as err:
            exception = ConnectionClosed(1007, err)
            self.fail_connection(1007)
        
        except PayloadError as err:
            exception = ConnectionClosed(1009, err)
            self.fail_connection(1009)
        
        except BaseException as err:
            await self.loop.render_exc_async(err, [
                'Unexpected exception occurred at ',
                repr(self),
                '.transfer_data\n',
                    ])
            # should not happen
            exception = ConnectionClosed(1011, err)
            self.fail_connection(1011)
        
        else:
            # connection was closed
            exception = ConnectionClosed(self.close_code or 1000, None, self.close_reason)
            
            # If we are a client and we receive this, we closed our own
            # connection, there is no reason to wait for TCP abort
            if self.is_client:
                self.connection_lost_waiter.set_result_if_pending(None)
        
        if self.transfer_data_exc is None:
            self.transfer_data_exc = exception
            self.messages.set_exception(exception)
    
    async def read_message(self):
        """
        Reads a message from the websocket.
        
        This method is a coroutine.
        
        Returns
        -------
        message : `None`, `bytes` or `str`
            A received message. It's type depend on the frame's type. returns `None` if close frame was received.
        
        Raises
        ------
        WebSocketProtocolError
            - Unexpected op code.
            - Incomplete fragmented message.
            - If the reserved bits are not `0`.
            - If the frame is a control frame, but is too long for one.
            - If the websocket frame is fragmented frame. (Might be supported if people request is.)
            - If the frame op_code is not any of the expected ones.
            - Close frame received with invalid status code.
            - Close frame too short.
        CancelledError
            ``.transfer_data_task`` cancelled.
        """
        frame = await self.read_data_frame(max_size=self.max_size)
        if frame is None: # close frame
            return
        
        if frame.op_code == WS_OP_TEXT:
            text = True
        elif frame.op_code == WS_OP_BINARY:
            text = False
        else: # frame.op_code == OP_CONT:
            raise WebSocketProtocolError(f'Unexpected op_code, got {frame.op_code!r}, expected {WS_OP_TEXT!r} or '
                f'{WS_OP_BINARY!r}.')
        
        # we got a whole frame, nice
        if frame.fin:
            message = frame.data
            
            if text:
                message = message.decode('utf-8')
            
            return message
        
        max_size = self.max_size # set max size to BIG number to ignore it
        
        frames = []
        while True:
            max_size -= len(frame.data)
            
            frames.append(frame)
            if frame.fin:
                break
            
            frame = await self.read_data_frame(max_size=max_size)
            if frame is None:
                raise WebSocketProtocolError('Incomplete fragmented message.')
            
            if frame.op_code != WS_OP_CONT:
                raise WebSocketProtocolError(f'Unexpected op_code, got {frame.op_code!r}, expected {WS_OP_CONT!r}.')
        
        if text:
            try:
                message = ''.join(DECODER.decode(frame.data, frame.fin) for frame in frames)
            except:
                DECODER.reset()
                raise
        else:
            message = b''.join(frame.data for frame in frames)
        
        return message
    
    
    async def read_data_frame(self, max_size):
        """
        Reads a websocket frame from the websocket. If the frame is a control frame processes and loops for reading an
        another one.
        
        This method is a coroutine.
        
        Parameters
        ----------
        
        Returns
        -------
        frame : ``Frame`` or `None`
            The read websocket frame. Returns `None` if close frame was received.
        
        Raises
        ------
        WebSocketProtocolError
            - If the reserved bits are not `0`.
            - If the frame is a control frame, but is too long for one.
            - If the websocket frame is fragmented frame. (Might be supported if people request is.)
            - If the frame op_code is not any of the expected ones.
            - Close frame received with invalid status code.
            - Close frame too short.
        CancelledError
            ``.transfer_data_task`` cancelled.
        """
        while True:
            
            frame = await self.set_payload_reader(self._read_websocket_frame(self.is_client, max_size))
            
            extensions = self.extensions
            if (extensions is not None):
                for extension in reversed(extensions):
                    frame = extension.decode(frame, max_size=max_size)
            
            frame.check()
            
            # most likely
            if frame.op_code in WS_DATA_OPCODES:
                return frame

            if (await self._process_CTRL_frame(frame)):
                continue
            
            return
    
    async def _process_CTRL_frame(self, frame):
        """
        Processes a control websocket frame.
        
        This method is a coroutine.
        
        Parameters
        ----------
        frame : ``Frame``
            A received control websocket frame.
        
        Returns
        -------
        can_continue : `bool`
            Returns `False` if the processed `frame` was a close frame.
        
        Raises
        ------
        WebSocketProtocolError
            - Close frame received with invalid status code.
            - Close frame too short.
        """
        op_code = frame.op_code
        if op_code == WS_OP_CLOSE:
            data = frame.data
            length = len(data)
            if length >= 2:
                code = int.from_bytes(data[:2], 'big')
                if not (code in EXTERNAL_CLOSE_CODES or 2999 < code < 5000):
                    raise WebSocketProtocolError(f'Invalid status code {code}.')
                reason = data[2:].decode('utf-8')
                self.close_code = code
                self.close_reason = reason
            elif length == 0:
                self.close_code = 1005
            else:
                raise WebSocketProtocolError(f'Close frame too short: {length}.')
            
            await self.write_close_frame(frame.data)
            return False
        
        if op_code == WS_OP_PING:
            await self.pong(frame.data)
            return True
        
        # op_code == OP_PONG:
        if frame.data in self.pings:
            #checking all pings up to the one matching this pong.
            ping_id = b''
            while ping_id != frame.data:
                ping_id, pong_waiter = self.pings.popitem(0)
                pong_waiter.set_result_if_pending(None)
        
        return True
    
    async def write_frame(self, op_code, data, _expected_state=OPEN):
        """
        Writes the data as websocket.
        
        This method is a coroutine.
        
        Parameters
        ----------
        op_code : `int`
            The operation code of the websocket frame.
            
            Can be 1 of the following:
            
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | WS_OP_CONT        | 0     |
            +-------------------+-------+
            | WS_OP_TEXT        | 1     |
            +-------------------+-------+
            | WS_OP_BINARY      | 2     |
            +-------------------+-------+
            | WS_OP_CLOSE       | 8     |
            +-------------------+-------+
            | WS_OP_PING        | 9     |
            +-------------------+-------+
            | WS_OP_PONG        | 10    |
            +-------------------+-------+
        
        data : `bytes-like`
            The data to send.
        
        _expected_state : `str`
            Expected state of the websocket. If the websocket is in other state, an `Exception` instance it raised.
            Defaults to `'OPEN'`.
            
            Can be set as one of the following values:
            
            +-------------------+-------------------+
            | Respective name   | Value             |
            +===================+===================+
            | CONNECTING        | `'CONNECTING'`    |
            +-------------------+-------------------+
            | OPEN              | `'OPEN'`          |
            +-------------------+-------------------+
            | CLOSING           | `'CLOSING'`       |
            +-------------------+-------------------+
            | CLOSED            | `'CLOSED'`        |
            +-------------------+-------------------+
            
            Note, that state is compared by memory address and not by value.
        
        Raises
        ------
        WebSocketProtocolError
            - If an extension set a reserved bit not to `0`.
            - If an extension modified the frame to a control frame, what is too long one.
            - If an extension modified the frame to be a fragmented one. (Might be supported if people request is.)
            - If an extension modified the frame's op code to not any of the expected ones.
        ConnectionClosed
            Websocket connection closed.
        Exception
            - Websocket connection not yet established.
            - Cannot write to websocket with it's current state.
        RuntimeError
            Protocol has no attached transport.
        """
        # Defensive assertion for protocol compliance.
        if self.state is not _expected_state:
            raise Exception(f'Cannot write to a WebSocket in the {self.state} state.')

        # we write only 1 frame at a time, so we 'queue' it
        async with self._drain_lock:
            try:
                frame = Frame(True, op_code, data)
                
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
        """
        Writes close frame to the websocket if the websocket is not yet closed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `bytes-like`, Optional
            The data to send. Defaults to empty `bytes`.
        
        Raises
        ------
        WebSocketProtocolError
            - If an extension set a reserved bit not to `0`.
            - If an extension modified the frame to a control frame, what is too long one.
            - If an extension modified the frame to be a fragmented one. (Might be supported if people request is.)
            - If an extension modified the frame's op code to not any of the expected ones.
        ConnectionClosed
            Websocket connection closed.
        Exception
            - Websocket connection not yet established.
            - Cannot write to websocket with it's current state.
        RuntimeError
            Protocol has no attached transport.
        """
        # check connection before we write
        if self.state is OPEN:
            self.state = CLOSING
            await self.write_frame(WS_OP_CLOSE, data, CLOSING)
    
    async def close_connection(self):
        """
        Makes sure that the websocket is closed correctly.
        
        Meanwhile the websocket is closing, it's ``.close_connection_task`` is set as a ``Task`` object wrapping the
        ``.close_connection`` coroutine to avoid race condition.
        
        This method is a coroutine.
        """
        try:
            # Wait for the data transfer phase to complete.
            transfer_data_task = self.transfer_data_task
            if (transfer_data_task is not None):
                try:
                    await transfer_data_task
                except (CancelledError, TimeoutError):
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
            if self.connection_lost_waiter.done() and not self.is_ssl:
                return
            
            #Close the TCP connection
            transport = self.transport
            if (transport is not None):
                transport.close()
                if (await self.wait_for_connection_lost()):
                    return
                # Abort the TCP connection
                transport.abort()
            # connection_lost() is called quickly after aborting.
            await self.wait_for_connection_lost()
            
    async def wait_for_connection_lost(self):
        """
        Waits until ``.connection_lost_waiter`` is set. If ``.close_timeout`` is over before it happens, returns.
        
        This method is a coroutine.
        
        Returns
        -------
        is_connection_lost : `bool`
            Returns `True` if the connection is lost.
        """
        if self.connection_lost_waiter.pending():
            try:
                task = shield(self.connection_lost_waiter, self.loop)
                future_or_timeout(task, self.close_timeout)
                await task
            except TimeoutError:
                pass
        
        # re-check self.connection_lost_waiter.done() synchronously because connection_lost() could run between the
        # moment the timeout occurs and the moment this coroutine resumes running.
        return self.connection_lost_waiter.done()
    
    def fail_connection(self, code=1006, reason=''):
        """
        Closes the websocket if any unexpected exception occurred.
        
        Parameters
        ----------
        code : `int`, Optional
            Websocket close code. Defaults to `1006`.
        reason : `str`, Optional
            Websocket close reason. Defaults to empty string.
        
        Returns
        -------
        close_connection_task : ``Task`` of ``.close_connection``
            Close connection task, what can be awaited to wait till the connection is closed.
        
        Raises
        ------
        WebSocketProtocolError
            - If an extension set a reserved bit not to `0`.
            - If an extension modified the frame to a control frame, what is too long one.
            - If an extension modified the frame to be a fragmented one. (Might be supported if people request is.)
            - If an extension modified the frame's op code to not any of the expected ones.
        RuntimeError
            Protocol has no attached transport.
        """
        # cancel transfer_data_task if the opening handshake succeeded
        transfer_data_task = self.transfer_data_task
        if transfer_data_task is not None:
            transfer_data_task.cancel()
        
        # send a close frame when the state is OPEN and the connection is not broken
        if code != 1006 and self.state is OPEN:
            
            frame_data = self._serialize_close(code, reason)
            # Write the close frame without draining the write buffer.
            self.state = CLOSING
            
            frame = Frame(True, WS_OP_CLOSE, frame_data)
            
            extensions = self.extensions
            if (extensions is not None):
                for extension in extensions:
                    frame = extension.encode(frame)
                
                frame.check()
            
            self.write_websocket_frame(frame, self.is_client)
        
        # start close_connection_task if the opening handshake didn't succeed.
        close_connection_task = self.close_connection_task
        if close_connection_task is None:
            close_connection_task = Task(self.close_connection(), self.loop)
            self.close_connection_task = close_connection_task
        
        return close_connection_task
    
    # compatibility method (overwrite)
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
        self.state = CLOSED
        if not self.close_code:
            self.close_code = 1006
        
        # `self.connection_lost_waiter` should be pending
        self.connection_lost_waiter.set_result_if_pending(None)
        
        ProtocolBase.connection_lost(self, exception)
    
    # compatibility method (overwrite)
    def eof_received(self):
        """
        Calling ``.connection_lost`` without exception causes eof.
        
        Marks the protocols as it is at eof and stops payload processing if applicable.
        
        Returns
        -------
        transport_closes : `bool`
            Returns `False` if the transport will close itself. If it returns `True`, then closing the transport is up
            to the protocol.
            
            Returns `True` if the websocket is not secure.
        """
        ProtocolBase.eof_received(self)
        return (not self.is_ssl)

class WSClient(WebSocketCommonProtocol):
    """
    Asynchronous websocket client implementation.
    
    Inherits common websocket features from the ``WebSocketCommonProtocol`` class.
    
    Attributes
    ----------
    _chunks : `deque` of `bytes`
        Right feed, left pop queue, used to store the received data chunks.
    _eof : `bool`
        Whether the protocol received end of file.
    _offset : `int`
        Byte offset, of the used up data of the most-left chunk.
    _paused : `bool`
        Whether the protocol's respective transport's reading is paused. Defaults to `False`.
        
        Also note, that not every transport supports pausing.
    exception : `None` or `BaseException`
        Exception set by ``.set_exception``, when an unexpected exception occurs meanwhile reading from socket.
    loop : ``EventThread``
        The event loop to what the protocol is bound to.
    payload_reader : `None` or `generator`
        Payload reader generator, what gets the control back, when data, eof or any exception is received.
    payload_waiter : `None` of ``Future``
        Payload waiter of the protocol, what's result is set, when the ``.payload_reader`` generator returns.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    transport : `None` or `Any`
        Asynchronous transport implementation. Is set meanwhile the protocol is alive.
    _drain_waiter : `None` or ``Future``
        A future, what is used to block the writing task, till it's writen data is drained.
    _drain_lock : ``Lock``
        Asynchronous lock to ensure, that only `1` frame is written in `1` time.
    close_code : `int`
        The websocket's close code if applicable. Defaults to `0`.
    close_connection_task : `None` or ``Task`` of ``.close_connection``
        A task, what is present meanwhile the websocket is closing to avoid race condition.
    close_timeout : `float`
        The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
    close_reason : `None` or `str`
        The reason, why the websocket was closed. Set only after the websocket is closed. Close reason might not be
        received tho.
    connection_lost_waiter : ``Future``
        A future, what's result is set as `None`, when the connection is closed. Used to wait for close frames.
        
        ``shield`` it if using from outside.
    extensions : `None` or (`list` of `Any`)
        Websocket extensions. Defaults to `None`, if there is not any.
    host : `str`
        The respective server's address to connect to.
    max_queue : `None` or `int`
        Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is removed.
         Defaults to `None`.
    max_size : `int`
        Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864` bytes.
    messages : ``AsyncQueue``
        An asynchronous queue of the received messages.
    is_ssl : `bool`
        Whether the connection is secure. Defaults to `False`.
    pings : `OrderedDict` of (`bytes`, ``Future``) items
        An ordered dictionary of ping payloads and of their waiter futures.
    port : `int`
        The respective server's port to connect to.
    state : `str`
        The websocket's state.
        
        Can be set as one of the following values:
        
        +-------------------+-------------------+
        | Respective name   | Value             |
        +===================+===================+
        | CONNECTING        | `'CONNECTING'`    |
        +-------------------+-------------------+
        | OPEN              | `'OPEN'`          |
        +-------------------+-------------------+
        | CLOSING           | `'CLOSING'`       |
        +-------------------+-------------------+
        | CLOSED            | `'CLOSED'`        |
        +-------------------+-------------------+
        
        Note, that state is compared by memory address and not by value.
    subprotocol : `None`, `str`
        Chosen subprotocol at handshake. Defaults to `None` and might be set as `str`. Chosen from the available
        subprotocols by their priority order.
    transfer_data_exc : `None` or `BaseException``
        Exception catched meanwhile processing received data.
    transfer_data_task : `None` or ``Task`` of ``.transfer_data``
        Data receiving task.
    
    Class Attributes
    ----------------
    is_client : `bool` = `True`
        Whether the websocket protocol is client or server side.
    """
    is_client = True
    
    __slots__ = ()
    async def __new__(cls, loop, url, *, origin=None, available_extensions=None, available_subprotocols=None,
            extra_request_headers=None, http_client=None, **websocket_kwargs):
        """
        Connects the websocket client to the given `url`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop, what the protocol uses for it's asynchronous tasks.
        url : `str` or ``URL``
            The url to connect to.
        origin : `None` or `str`, Optional (Keyword only)
            Value of the Origin header.
        available_extensions : `None` or (`list` of `Any`), Optional (Keyword only)
            Available websocket extensions. Defaults to `None`.
            
            Each websocket extension should have the following `4` attributes / methods:
            - `name`, type `str`. The extension's name.
            - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
            - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
                parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what describes the
                maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
            - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
                parameter, the respective websocket ``Frame``.
        available_subprotocols : `None` or (`list` of `str`), Optional (Keyword only)
            A list of supported subprotocols in order of decreasing preference.
        extra_request_headers : ``imultidict`` or `dict-like` with (`str`, `str`) items, Optional (Keyword only)
            Extra request headers.
        http_client : `None` or ``HTTPClient`` instance, Optional (Keyword only)
            Http client to use to connect the websocket.
        **websocket_kwargs : Keyword parameters
            Additional keyword parameters to create the websocket with.
        
        Other Parameters
        ----------------
        close_timeout : `float`, Optional (Keyword only)
            The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
        max_size : `int`, Optional (Keyword only)
            Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864`
            bytes.
        max_queue : `None` or `int`, Optional (Keyword only)
            Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is
            removed. Defaults to `None`.
        
        Returns
        -------
        self : ``WSClient``
        
        Raises
        ------
        ConnectionError
            - Too many redirects.
            - Would be redirected to not `http` or `https`.
            - Connector closed.
        TypeError
            `extra_response_headers` is not given as `None`, neither as `dict-like`.
        ValueError
            - Host could not be detected from `url`.
            - The response's http version is unsupported (not `HTTP1.1`).
            - Received extension header is incorrect.
            - Received connection header is incorrect.
        TimeoutError
            - Did not receive answer in time.
        InvalidHandshake
            - The response's status code is invalid (not `101`).
            - The response's connection headers do not contain `'upgrade'`.
            - The response's headers contains 0 or more than 1 upgrade headers.
            - The response's upgrade header is not `'WebSocket'`.
            - The response's headers contain sec websocket accept 0 or more than 1 times.
            - The response's secret key not matches the send one.
            - No extensions are supported, but still received.
            - Unsupported extension received.
            - No subprotocols are supported, but still received.
            - Multiple subprotocols received.
            - Unsupported subprotocol received.
        """
        if http_client is None:
            http_client = HTTPClient(loop)
        
        url = URL(url)
        is_ssl = (url.scheme == 'wss')
        
        # building headers
        sec_key = b64encode(urandom(16)).decode()
        request_headers = imultidict()
        
        request_headers[UPGRADE] = 'websocket'
        request_headers[CONNECTION] = 'Upgrade'
        request_headers[SEC_WEBSOCKET_KEY] = sec_key
        request_headers[SEC_WEBSOCKET_VERSION] = '13'
        
        if url.port == (443 if is_ssl else 80):
            request_host = url.host
        else:
            request_host = f'{url.host}:{url.port}'
        
        request_headers[HOST] = request_host
        
        user = url.user
        password = url.password
        if (user is not None) or (password is not None):
            request_headers[AUTHORIZATION] = BasicAuth(user, password).encode()
        
        if origin is not None:
            request_headers[ORIGIN] = origin
        
        if available_extensions is not None:
            request_headers[SEC_WEBSOCKET_EXTENSIONS] = build_extensions(available_extensions)
        
        if available_subprotocols is not None:
            request_headers[SEC_WEBSOCKET_PROTOCOL] = build_subprotocols(available_subprotocols)
        
        if extra_request_headers is not None:
            # we use especially items, so we check that
            if isinstance(extra_request_headers, imultidict) or hasattr(type(extra_request_headers), 'items'):
                for name, value in extra_request_headers.items():
                    request_headers[name] = value
            else:
                raise TypeError('`extra_response_headers` should be `dict-like` with `.items` method, got '
                    f'{extra_request_headers.__class__.__name__} instance.')
        
        async with http_client.request(METHOD_GET, url, request_headers) as response:
           
            if response.raw_message.version != HttpVersion11:
                raise ValueError(f'Unsupported HTTP version: {response.raw_message.version}.')
            
            if response.status != 101:
                raise InvalidHandshake(f'Invalid status code: {response.status!r}.')
            
            response_headers = response.headers
            connections = []
            received_connections = response_headers.get_all(CONNECTION,)
            if (received_connections is not None):
                for received_connection in received_connections:
                    connections.extend(parse_connections(received_connection))
            
            if not any(value.lower() == 'upgrade' for value in connections):
                raise InvalidHandshake(f'Invalid connection, no upgrade found, got {connections!r}.')
            
            upgrade = []
            received_upgrades = response_headers.get_all(UPGRADE)
            if (received_upgrades is not None):
                for received_upgrade in received_upgrades:
                    upgrade.extend(parse_upgrades(received_upgrade))
            
            if len(upgrade) != 1 and upgrade[0].lower() != 'websocket': # ignore case
                raise InvalidHandshake(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}.')
            
            expected_key = b64encode(hashlib.sha1((sec_key+WS_KEY).encode()).digest()).decode()
            received_keys = response_headers.get_all(SEC_WEBSOCKET_ACCEPT)
            if received_keys is None:
                raise InvalidHandshake(f'Expected 1 secret key {expected_key!r}, but received 0.')
            if len(received_keys) > 1:
                raise InvalidHandshake(f'Expected 1 secret key {expected_key!r}, but received more: {received_keys!r}.')
            
            received_key = received_keys[0]
            if received_key != expected_key:
                raise InvalidHandshake(f'Expected secret key {expected_key}, but got {received_key!r}.')
            
            #extensions
            accepted_extensions = []
            received_extensions = response_headers.get_all(SEC_WEBSOCKET_EXTENSIONS)
            if (received_extensions is not None):
                if available_extensions is None:
                    raise InvalidHandshake(f'No extensions supported, but received {received_extensions!r}.')
                
                parsed_extension_values = []
                for value in received_extensions:
                    parsed_extension_values.extend(parse_extensions(value))
                
                for name, params in parsed_extension_values:
                    for extension in available_extensions:
                        # do names and params match?
                        if extension.name == name and extension.are_valid_params(params, accepted_extensions):
                            accepted_extensions.append(extension)
                            break
                    else:
                        # no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name={name!r}, params={params!r}.')
            
            subprotocol = None
            received_subprotocols = response_headers.get_all(SEC_WEBSOCKET_PROTOCOL)
            if (received_subprotocols is not None):
                if available_subprotocols is None:
                    raise InvalidHandshake(f'No subprotocols supported, but received {received_subprotocols!r}.')
                
                parsed_subprotocol_values = []
                for received_subprotocol in received_subprotocols:
                    parsed_subprotocol_values.extend(parse_subprotocols(received_subprotocol))
                
                if len(parsed_subprotocol_values) > 1:
                    raise InvalidHandshake(f'Multiple subprotocols: {parsed_subprotocol_values!r}.')
                
                subprotocol = parsed_subprotocol_values[0]
                
                if subprotocol not in available_subprotocols:
                    raise InvalidHandshake(f'Unsupported subprotocol: {subprotocol}.')
            
            connection = response.connection
            protocol = connection.protocol
            connection.detach()
            
            self = object.__new__(cls)
            WebSocketCommonProtocol.__init__(self, loop, url.host, url.port, is_ssl=is_ssl, **websocket_kwargs)
            protocol._copy_attrs_to(self)
            self.extensions = accepted_extensions
            self.subprotocol = subprotocol
            self.transport.set_protocol(self)
        
        self.connection_open()
        return self

class WSServerProtocol(WebSocketCommonProtocol):
    """
    Asynchronous server side websocket protocol implementation.
    
    Attributes
    ----------
    _chunks : `deque` of `bytes`
        Right feed, left pop queue, used to store the received data chunks.
    _eof : `bool`
        Whether the protocol received end of file.
    _offset : `int`
        Byte offset, of the used up data of the most-left chunk.
    _paused : `bool`
        Whether the protocol's respective transport's reading is paused. Defaults to `False`.
        
        Also note, that not every transport supports pausing.
    exception : `None` or `BaseException`
        Exception set by ``.set_exception``, when an unexpected exception occurs meanwhile reading from socket.
    loop : ``EventThread``
        The event loop to what the protocol is bound to.
    payload_reader : `None` or `generator`
        Payload reader generator, what gets the control back, when data, eof or any exception is received.
    payload_waiter : `None` of ``Future``
        Payload waiter of the protocol, what's result is set, when the ``.payload_reader`` generator returns.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    transport : `None` or `Any`
        Asynchronous transport implementation. Is set meanwhile the protocol is alive.
    _drain_waiter : `None` or ``Future``
        A future, what is used to block the writing task, till it's writen data is drained.
    _drain_lock : ``Lock``
        Asynchronous lock to ensure, that only `1` frame is written in `1` time.
    close_code : `int`
        The websocket's close code if applicable. Defaults to `0`.
    close_connection_task : `None` or ``Task`` of ``.close_connection``
        A task, what is present meanwhile the websocket is closing to avoid race condition.
    close_timeout : `float`
        The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
    close_reason : `None` or `str`
        The reason, why the websocket was closed. Set only after the websocket is closed. Close reason might not be
        received tho.
    connection_lost_waiter : ``Future``
        A future, what's result is set as `None`, when the connection is closed. Used to wait for close frames.
        
        ``shield`` it if using from outside.
    extensions : `None` or (`list` of `Any`)
        Websocket extensions. Defaults to `None`, if there is not any.
    host : `str`
        The respective server's address to connect to.
    max_queue : `None` or `int`
        Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is removed.
         Defaults to `None`.
    max_size : `int`
        Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864` bytes.
    messages : ``AsyncQueue``
        An asynchronous queue of the received messages.
    is_ssl : `bool`
        Whether the connection is secure. Defaults to `False`.
    pings : `OrderedDict` of (`bytes`, ``Future``) items
        An ordered dictionary of ping payloads and of their waiter futures.
    port : `int`
        The respective server's port to connect to.
    state : `str`
        The websocket's state.
        
        Can be set as one of the following values:
        
        +-------------------+-------------------+
        | Respective name   | Value             |
        +===================+===================+
        | CONNECTING        | `'CONNECTING'`    |
        +-------------------+-------------------+
        | OPEN              | `'OPEN'`          |
        +-------------------+-------------------+
        | CLOSING           | `'CLOSING'`       |
        +-------------------+-------------------+
        | CLOSED            | `'CLOSED'`        |
        +-------------------+-------------------+
        
        Note, that state is compared by memory address and not by value.
    subprotocol : `None`, `str`
        Chosen subprotocol at handshake. Defaults to `None` and might be set as `str`. Chosen from the available
        subprotocols by their priority order.
    transfer_data_exc : `None` or `BaseException``
        Exception catched meanwhile processing received data.
    transfer_data_task : `None` or ``Task`` of ``.transfer_data``
        Data receiving task.
    available_extensions : `None` or (`list` of `Any`)
        Available websocket extensions. Defaults to `None`.
        
        Each websocket extension should have the following `4` attributes / methods:
        - `name`, type `str`. The extension's name.
        - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
        - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
            parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what describes the
            maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
        - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
            parameter, the respective websocket ``Frame``.
    available_subprotocols : `None` or (`list` of `str`)
        A list of supported subprotocols in order of decreasing preference.
    extra_response_headers : ``imultidict`` or `dict-like` with (`str`, `str`) items
        Extra response headers.
    handler : `async-callable`
        An asynchronous callable, what will handle a websocket connection.
        
        Should be given as an `async-callable` accepting `1` parameter the respective asynchronous server side
        websocket protocol implementations.
    handler_task : `None` or ``Task`` of ``.lifetime_handler``
        Handles the connected websocket meanwhile it is alive.
    origin : `None` or `str`
        Value of the Origin header.
    request_processor : `None` or `callable`
        An optionally asynchronous callable, what processes the initial requests from the potential clients.
        
        Should accept the following parameters:
        - `path` : `str`. The requested path.
        - `request_headers` : ``imultidict`` of (`str`, `str`). The request's headers.
        
        The `request_processor` on accepted request should return `None`, otherwise a `tuple` of
        ``AbortHandshake`` parameters.
    server : ``WSServer``
        The owner websocket server instance.
    subprotocol_selector `None` or `callable`
        User hook to select subprotocols. Should accept the following parameters:
        - `parsed_header_subprotocols` : `list` of `str`. The subprotocols supported by the client.
        - `available_subprotocols` : `list` of `str`. The subprotocols supported by the server.
    request : `None` or ``RawRequestMessage``
        The received http request if applicable.
    response_headers : `None` or `imultidict` of (`str`, `str`) items
        The server websocket's response's headers if applicable.
    """
    is_client = False
    
    __slots__ = ('available_extensions', 'available_subprotocols', 'extra_response_headers', 'handler', 'handler_task',
        'origin', 'origin', 'request_processor', 'server', 'subprotocol_selector', 'request', 'response_headers')
    
    def __init__(self, server):
        """
        Creates a new ``WSServerProtocol`` with the given parameters.
        
        This method is usually wrapped into a partial function.
        
        Parameters
        ----------
        server : ``WSServer``
            The parent websocket server.
        """
        handler, host, port, is_ssl, origin, available_extensions, available_subprotocols , extra_response_headers, \
        request_processor, subprotocol_selector, websocket_kwargs = server.protocol_parameters
        
        self.handler = handler
        self.server = server
        self.origin = origin
        self.available_extensions = available_extensions
        self.available_subprotocols = available_subprotocols
        self.extra_response_headers = extra_response_headers
        self.request_processor = request_processor
        self.subprotocol_selector = subprotocol_selector
        self.handler_task = None
        
        WebSocketCommonProtocol.__init__(self, server.loop, host, port, is_ssl=is_ssl, **websocket_kwargs)
        
        self.request = None
        self.response_headers = None
        self.origin = None
        
    def connection_made(self, transport):
        """
        Called when a connection is made.
        
        Parameters
        ----------
        transport : `Any`
            Asynchronous transport implementation, what calls the protocol's ``.data_received`` when data is
            received.
        """
        WebSocketCommonProtocol.connection_made(self, transport)
        self.server.register(self)
        self.handler_task = Task(self.lifetime_handler(), self.loop)
        
    async def lifetime_handler(self):
        """
        The asynchronous websocket protocol's main "lifetime" task.
        
        This method is a coroutine.
        """
        try:
            # handshake returns True if it succeeded
            if not (await self.handshake()):
                return
            
            try:
                await self.handler(self)
            except BaseException as err:
                await self.loop.render_exc_async(err, before = [
                    'Unhandled exception occurred at',
                    self.__class__.__name__,
                    '.lifetime_handler meanwhile running: ',
                    repr(self.handler),
                    '\n',
                        ])
                return
            
            await self.close()
        except:
            # We will let Task.__del__ to render the exception...
            
            transport = self.transport
            if transport is None:
                raise
                
            transport.close()
            transport.abort()
            raise
        
        finally:
            self.handler_task = None
            self.server.unregister(self)
    
    async def handshake(self):
        """
        Handles a received websocket connect request.
        
        This method is a coroutine.
        
        Returns
        -------
        handshake_succeeded : `bool`
            If the websocket handshake succeeded and starting's it's handler can begin, returns `True`.
        """
        try:
            self.request = request = await self.set_payload_reader(self._read_http_request())
            
            request_headers = request.headers
            if self.server.is_serving():
                path = request.path
                
                request_processor = self.request_processor
                if request_processor is None:
                    early_response = None
                else:
                    early_response = request_processor(path, request_headers)
                    if is_coroutine(early_response):
                        early_response = await early_response
                
                if (early_response is not None):
                    raise AbortHandshake(*early_response)
                
            else:
                raise AbortHandshake(SERVICE_UNAVAILABLE, 'Server is shutting down.')
            
            connections = []
            connection_headers = request_headers.get_all(CONNECTION)
            if (connection_headers is not None):
                for connection_header in connection_headers:
                    connections.extend(parse_connections(connection_header))
        
            if not any(value.lower() == 'upgrade' for value in connections):
                raise InvalidUpgrade(f'Invalid connection, no upgrade found, got {connections!r}.')
            
            upgrade = []
            upgrade_headers = request_headers.get_all(UPGRADE)
            if (upgrade_headers is not None):
                for upgrade_header in upgrade_headers:
                    upgrade.extend(parse_upgrades(upgrade_header))
            
            if len(upgrade) != 1 and upgrade[0].lower() != 'websocket': # ignore case
                raise InvalidUpgrade(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}.')
            
            received_keys = request_headers.get_all(SEC_WEBSOCKET_KEY)
            if received_keys is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_KEY!r} from headers')
            
            if len(received_keys) > 1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_KEY!r} values at headers')
            
            key = received_keys[0]
        
            try:
                raw_key = b64decode(key.encode(), validate=True)
            except BinasciiError:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}: {key!r}.')
            
            if len(raw_key) != 16:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}, should be length 16; {key!r}.')
            
            sw_version = request_headers.get_all(SEC_WEBSOCKET_VERSION)
            if sw_version is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_VERSION!r} values at headers.')
            
            if len(sw_version) > 1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_VERSION!r} values at headers.')
            
            sw_version = sw_version[0]
            if sw_version != '13':
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_VERSION!r}: {sw_version!r}.')
            
            while True:
                origin = self.origin
                if (origin is None):
                    origin = None
                    break
                
                origin_headers = request_headers.get_all(ORIGIN)
                
                if (origin_headers is None):
                    raise InvalidOrigin('No origin at header.')
                
                if len(origin_headers) > 1:
                    raise InvalidOrigin('More than 1 origin at header.')
                
                origin = origin_headers[0]
                
                if origin in origin:
                    break
                    
                raise InvalidOrigin(origin)
            
            self.origin = origin
            
            while True:
                accepted_extensions = []
                
                available_extensions = self.available_extensions
                if (available_extensions is None):
                    extension_header = None
                    break
                
                extension_headers_ = request_headers.get_all(SEC_WEBSOCKET_EXTENSIONS)
                if (extension_headers_ is None):
                    extension_header = None
                    break
                
                extension_headers = []
                parsed_extension_values = []
                for extension_header_ in extension_headers_:
                    parsed_extension_values.extend(parse_extensions(extension_header_))
                
                for name, params in parsed_extension_values:
                    for extension in available_extensions:
                        # do names and params match?
                        if extension.name == name and extension.are_valid_params(params, accepted_extensions):
                            accepted_extensions.append(extension)
                            extension_headers.append((name, params))
                            break
                    else:
                        # no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name={name!r}, params={params!r}.')
                    
                    # If we didn't break from the loop, no extension in our list matched what the client sent. The
                    # extension is declined.
                
                # Serialize extension header.
                if extension_headers:
                    extension_header = build_extensions(extension_headers)
                    break
                
                extension_header = None
                break
            
            self.extensions = accepted_extensions
            
            
            while True:
                available_subprotocols = self.available_subprotocols
                if (available_subprotocols is None):
                    selected_subprotocol = None
                    break
                    
                protocol_headers = request_headers.get_all(SEC_WEBSOCKET_PROTOCOL)
                if (protocol_headers is None):
                    selected_subprotocol = None
                    break
                
                parsed_header_subprotocols = []
                for protocol_header in protocol_headers:
                    parsed_header_subprotocols.extend(parse_subprotocols(protocol_header))
                
                subprotocol_selector = self.subprotocol_selector
                if (subprotocol_selector is not None):
                    selected_subprotocol = subprotocol_selector(parsed_header_subprotocols, available_subprotocols)
                    break
                    
                subprotocols = set(parsed_header_subprotocols)
                subprotocols.intersection_update(available_subprotocols)
                
                if not subprotocols:
                    selected_subprotocol = None
                    break
                
                lowest_priority = len(parsed_header_subprotocols) + len(available_subprotocols)
                selected_subprotocol = None
                
                for subprotocol in subprotocols:
                    priority = parsed_header_subprotocols.index(subprotocol)+available_subprotocols.index(subprotocol)
                    if priority < lowest_priority:
                        lowest_priority = priority
                        selected_subprotocol = subprotocol
                
                break
            
            self.subprotocol = selected_subprotocol
            
            response_headers = imultidict()
    
            response_headers[UPGRADE] = 'websocket'
            response_headers[CONNECTION] = 'Upgrade'
            response_headers[SEC_WEBSOCKET_ACCEPT] = b64encode(hashlib.sha1((key+WS_KEY).encode()).digest()).decode()
            
            if (extension_header is not None):
                response_headers[SEC_WEBSOCKET_EXTENSIONS] = extension_header
    
            if (selected_subprotocol is not None):
                response_headers[SEC_WEBSOCKET_PROTOCOL] = selected_subprotocol
            
            extra_response_headers = self.extra_response_headers
            if (extra_response_headers is not None):
                for key, value in extra_response_headers.items():
                    response_headers[key] = value
            
            response_headers.setdefault(DATE, formatdate(usegmt=True))
            response_headers.setdefault(SERVER, '')
            
            self.response_headers = response_headers
            self.write_http_response(SWITCHING_PROTOCOLS, response_headers)
            
            self.connection_open()
        except (CancelledError, ConnectionError) as err:
            await self.loop.render_exc_async(err, before = [
                'Unhandled exception occurred at ',
                self.__class__.__name__,
                '.handshake, when handshaking:\n'])
            return False
        except BaseException as err:
            if isinstance(err, AbortHandshake):
                status = err.code
                headers = err.headers
                if headers is None:
                    headers = imultidict()
                body = err.message
                if not body.endswith('\n'):
                    body = body+b'\n'
            elif isinstance(err, InvalidOrigin):
                status = FORBIDDEN
                headers = imultidict()
                body = f'Failed to open a WebSocket connection: {err}.\n'.encode()
            elif isinstance(err, InvalidUpgrade):
                status = UPGRADE_REQUIRED
                headers = imultidict()
                headers[UPGRADE] = 'websocket'
                body = (
                    f'Failed to open a WebSocket connection: {err}.\n\n'
                    f'You cannot access a WebSocket server directly with a browser. You need a WebSocket client.\n'
                        ).encode()
            elif isinstance(err, InvalidHandshake):
                status = BAD_REQUEST
                headers = imultidict()
                body = f'Failed to open a WebSocket connection: {err}.\n'.encode()
            elif isinstance(err, PayloadError):
                status = BAD_REQUEST
                headers = imultidict()
                body = f'Invalid request body: {err}.\n'.encode()
            else:
                status = INTERNAL_SERVER_ERROR
                headers = imultidict()
                body = b'Failed to open a WebSocket connection.\n'
            
            headers.setdefault(DATE, formatdate(usegmt=True))
            headers.setdefault(SERVER, '')
            headers.setdefault(CONTENT_LENGTH, repr(len(body)))
            headers.setdefault(CONTENT_TYPE, 'text/plain')
            headers.setdefault(CONNECTION, 'close')
            
            try:
                self.write_http_response(status, headers, body=body)
                self.fail_connection()
                await self.wait_for_connection_lost()
            except BaseException as err2:
                await self.loop.render_exc_async(err2, before=[
                    'Unhandled exception occurred at ',
                    self.__class__.__name__,
                    '.handshake, when handling an other exception;',
                    repr(err), ':'])
            return False
        
        return True


class WSServer:
    """
    Asynchronous websocket server implementation.
    
    Attributes
    ----------
    loop : ``EventThread``
        The event loop to what the websocket server is bound to.
    websockets : `set` of (``WSServerProtocol`` or `Any`)
        Active server side asynchronous websocket protocol implementations.
    close_connection_task : `None` or ``Task`` of ``_close``
        Close connection task, what's result is set, when closing of the websocket is done.
        
        Should not be cancelled.
        
        Set, when ``.close`` is called.
    handler : `async-callable`
        An asynchronous callable, what will handle a websocket connection.
        
        Should be given as an `async-callable` accepting `1` parameter the respective asynchronous server side websocket
        protocol implementations.
    server : `None` or ``Server``
        Asynchronous server instance. Set meanwhile the websocket server is running.
    protocol_parameters : `tuple` of `Any`
        Websocket protocol parameters.
        
        Contains the following elements:
            - `handler` : `async-callable` Same as ``.handler``.
            - `host` : `None` or `str`, `iterable` of (`None` or `str`). To what network interfaces the server be bound.
            - `port` :  `None` or `int`. The port used by the `host`(s).
            - `is_ssl` : `bool`
                Whether the server is secure.
            - `origin` : `None` or `str`. Value of the Origin header.
            - `available_extensions` : `None` or (`list` of `Any`).Available websocket extensions.
                Each websocket extension should have the following `4` attributes / methods:
                - `name`, type `str`. The extension's name.
                - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
                - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
                    parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what describes the
                    maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
                - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
                    parameter, the respective websocket ``Frame``.
            - `available_subprotocols` : `None` or (`list` of `str`). A list of supported subprotocols in order of
                decreasing preference.
            - `extra_response_headers` : `None` or (``imultidict``, `dict-like`) of (`str`, `str`) items. Extra
                headers to send with the http response.
            - `request_processor` : `None` or `callable`. An optionally asynchronous callable, what processes the
                initial requests from the potential clients. Should accept the following parameters:
                - `path` : `str`. The requested path.
                - `request_headers` : ``imultidict`` of (`str`, `str`). The request's headers.
                
                The `request_processor` on accepted request should return `None`, otherwise a `tuple` of
                ``AbortHandshake`` parameters.
            - `subprotocol_selector` : `None` or `callable`. User hook to select subprotocols. Should accept the
                following parameters:
                - `parsed_header_subprotocols` : `list` of `str`. The subprotocols supported by the client.
                - `available_subprotocols` : `list` of `str`. The subprotocols supported by the server.
            - `websocket_kwargs` : `dict` of (`str`, `Any`). Extra parameters for creating the websocket protocol.
                
                Can have any of the following items:
                - `close_timeout` : `float`. The maximal duration in seconds what is waited for response after close
                    frame is sent. Defaults to `10.0`.
                - `max_size` : `int`.Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised.
                    Defaults to `67108864` bytes.
                - `max_queue` : `None` or `int`.
                    Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of
                    it is removed. Defaults to `None`.
    """
    __slots__ = ('loop', 'websockets', 'close_connection_task', 'handler', 'server', 'protocol_parameters')
    async def __new__(cls, loop, host, port, handler, *, protocol=WSServerProtocol, available_extensions=None,
            extra_response_headers=None, origin=None, available_subprotocols=None, request_processor=None,
            subprotocol_selector=None, websocket_kwargs=None, ssl=None, **server_kwargs):
        """
        Creates a new ``WSServer`` instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the websocket server is bound to.
        host : `None` or `str`, `iterable` of (`None` or `str`)
            To what network interfaces should the server be bound.
        port : `None` or `int`
            The port to use by the `host`(s).
        handler : `async-callable`
            An asynchronous callable, what will handle a websocket connection.
            
            Should be given as an `async-callable` accepting `1` parameter the respective asynchronous server side
            websocket protocol implementations.
        protocol : `Any`, Optional (Keyword only)
            Asynchronous server side websocket protocol implementation. Defaults to ``WSServerProtocol``.
        available_extensions : `None` or (`list` of `Any`), Optional (Keyword only)
            Available websocket extensions.
            
            Each websocket extension should have the following `4` attributes / methods:
            - `name`, type `str`. The extension's name.
            - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
            - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
                parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what decides the
                maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
            - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
                parameter, the respective websocket ``Frame``.
        extra_response_headers : `None` or (``imultidict``, `dict-like`) of (`str`, `str`) items, Optional (Keyword only)
            Extra headers to send with the http response.
        origin : `None` or `str`, Optional (Keyword only)
            Value of the Origin header.
        available_subprotocols : `None` or (`list` of `str`), Optional (Keyword only)
            A list of supported subprotocols in order of decreasing preference.
        request_processor : `None` or `callable`, Optional (Keyword only)
            An optionally asynchronous callable, what processes the initial requests from the potential clients.
            
            Should accept the following parameters:
            - `path` : `str`. The requested path.
            - `request_headers` : ``imultidict`` of (`str`, `str`). The request's headers.
            
            The `request_processor` on accepted request should return `None`, otherwise a `tuple` of
            ``AbortHandshake`` parameters.
        subprotocol_selector `None` or `callable`, Optional (Keyword only)
            User hook to select subprotocols. Should accept the following parameters:
            - `parsed_header_subprotocols` : `list` of `str`. The subprotocols supported by the client.
            - `available_subprotocols` : `list` of `str`. The subprotocols supported by the server.
        websocket_kwargs : `dict` of (`str`, `Any`), Optional (Keyword only)
            Extra parameters for creating the websocket protocol.
            
            Can have any of the following items:
            - `close_timeout` : `float`. The maximal duration in seconds what is waited for response after close
                frame is sent. Defaults to `10.0`.
            - `max_size` : `int`.Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised.
                Defaults to `67108864` bytes.
            - `max_queue` : `None` or `int`.
                Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of
                it is removed. Defaults to `None`.
        ssl : `None` or ``SSLContext``, Optional (Keyword only)
            Whether and what ssl is enabled for the connections.
        **server_kwargs : Keyword parameters
            Additional keyword parameters to create the websocket server with.
        
        Other Parameters
        ----------------
        family : `AddressFamily` or `int`, Optional (Keyword only)
            Can be given either as `socket.AF_INET` or `socket.AF_INET6` to force the socket to use `IPv4` or `IPv6`.
            If not given, then  will be determined from host name.
        backlog : `int`, Optional (Keyword only)
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        reuse_address : `bool`, Optional (Keyword only)
            Tells the kernel to reuse a local socket in `TIME_WAIT` state, without waiting for its natural timeout to
            expire. If not specified will automatically be set to True on Unix.
        reuse_port : `bool`, Optional (Keyword only)
            Tells to the kernel to allow this endpoint to be bound to the same port as an other existing endpoint
            already might be bound to.
            
            Not supported on Windows.
        
        Returns
        -------
        self : ``WSServer``
        
        Raises
        ------
        TypeError
            - `extra_response_headers` is not given as `None`, neither as `dict-like`.
            - If `ssl` is not given either as `None` or as `ssl.SSLContext` instance.
            - If `reuse_port` is given as non `bool`.
            - If `reuse_address` is given as non `bool`.
            - If `reuse_port` is given as non `bool`.
            - If `host` is not given as `None`, `str` and neither as `iterable` of `None` or `str`.
        ValueError
            - If `host` or `port` parameter is given, when `socket` is defined as well.
            - If `reuse_port` is given as `True`, but not supported.
            - If neither `host`, `port nor `socket` were given.
            - If `socket` is given, but it's type is not `module_socket.SOCK_STREAM`.
        OsError
            Error while attempting to binding to address.
        """
        if websocket_kwargs is None:
            websocket_kwargs = {}
        
        is_ssl = (ssl is not None)
        
        if available_extensions is None:
            available_extensions = []
        
        if (extra_response_headers is None):
            pass
        elif type(extra_response_headers) is imultidict:
            pass
        elif hasattr(type(extra_response_headers), 'items'):
            extra_response_headers_local = imultidict()
            
            for name, value in extra_response_headers.items():
                extra_response_headers_local[name] = value
            
            extra_response_headers = extra_response_headers_local
        else:
            raise TypeError(f'`extra_response_headers` should be `None` or a dict-like with \'.items\' method, got '
                f'{extra_response_headers.__class__.__name__} instance.')
        
        if (extra_response_headers is not None) and (not extra_response_headers):
            extra_response_headers = None
        
        self = object.__new__(cls)
        self.loop = loop
        self.handler = handler
        self.websockets = set()
        self.close_connection_task = None
        self.server = None
        self.protocol_parameters = (handler, host, port, is_ssl, origin, available_extensions, available_subprotocols,
            extra_response_headers, request_processor, subprotocol_selector, websocket_kwargs)
        
        factory = partial_func(protocol, self,)
        server = await loop.create_server(factory, host, port, ssl=ssl, **server_kwargs)
        
        self.server = server
        await server.start()
        
        return self
    
    def register(self, protocol):
        """
        Registers a newly created server side websocket to the websocket server itself.
        
        Parameters
        ----------
        protocol : ``WSServerProtocol`` or `Any`
            The connected server side websocket.
        """
        self.websockets.add(protocol)
    
    def unregister(self, protocol):
        """
        Unregisters a newly created server side websocket from the websocket server itself.
        
        Parameters
        ----------
        protocol : ``WSServerProtocol`` or `Any`
            The disconnected server side websocket.
        """
        self.websockets.discard(protocol)
    
    def is_serving(self):
        """
        Returns whether the websocket server is serving.
        
        Returns
        -------
        is_serving : `bool`
        """
        server = self.server
        if server is None:
            return False
        
        if server.sockets is None:
            return False
        
        return True
    
    def close(self):
        """
        Closes the websocket server. Returns a closing task, what can be awaited.
        
        Returns
        -------
        close_connection_task : ``Task`` of ``_close``
            Close connection task, what's result is set, when closing of the websocket is done.
            
            Should not be cancelled.
        """
        close_connection_task = self.close_connection_task
        if close_connection_task is None:
            close_connection_task = Task(self._close(), self.loop)
            self.close_connection_task = close_connection_task
        
        return close_connection_task
    
    async def _close(self):
        """
        Closes the websocket server. If the websocket task is already closed does nothing.
        
        This method is a coroutine.
        """
        server = self.server
        if server is None:
            return
        
        server.close()
        await server.wait_closed()
        
        loop = self.loop
        
        # Skip 1 full loop
        future = Future(loop)
        loop.call_at(0.0, Future.set_result_if_pending, future, None)
        await future
        
        websockets = self.websockets
        if websockets:
            tasks = []
            for websocket in websockets:
                tasks.append(websocket.close(1001))
            
            future = WaitTillAll(tasks, loop)
            tasks = None
            await future
            
        if websockets:
            tasks = []
            for websocket in websockets:
                task = websocket.handler_task
                if task is None:
                    continue
                
                tasks.append(task)
            
            task = None
            if tasks:
                future = WaitTillAll(tasks, loop)
                tasks = None
                await future

del module_http
