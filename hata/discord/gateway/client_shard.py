__all__ = ()

from sys import platform as PLATFORM
from zlib import decompressobj as create_zlib_decompressor, error as ZlibError

from scarletio import Task, copy_docs, from_json, repeat_timeout, skip_ready_cycle, sleep, to_json
from scarletio.web_common import ConnectionClosed, InvalidHandshake, WebSocketProtocolError

from ...env import API_VERSION, CACHE_PRESENCE, LIBRARY_NAME

from ..activity import ACTIVITY_UNKNOWN
from ..core import KOKORO
from ..events.core import PARSERS
from ..events.handling_helpers import call_unknown_dispatch_event_event_handler
from ..exceptions import DiscordGatewayException, GATEWAY_EXCEPTION_CODE_TABLE
from ..guild.guild.constants import LARGE_GUILD_LIMIT

from .client_base import DiscordGatewayClientBase
from .constants import (
    GATEWAY_ACTION_CONNECT, GATEWAY_ACTION_KEEP_GOING, GATEWAY_ACTION_RESUME, GATEWAY_CONNECT_TIMEOUT,
    GATEWAY_OPERATION_CLIENT_DISPATCH, GATEWAY_OPERATION_CLIENT_HEARTBEAT,
    GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE, GATEWAY_OPERATION_CLIENT_HELLO, GATEWAY_OPERATION_CLIENT_IDENTIFY,
    GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION, GATEWAY_OPERATION_CLIENT_RECONNECT, GATEWAY_OPERATION_CLIENT_RESUME,
    GATEWAY_OPERATION_CLIENT_VOICE_STATE, LATENCY_DEFAULT, POLL_TIMEOUT
)
from .heartbeat import Kokoro
from .rate_limit import GatewayRateLimiter


async def _poll_compressed_message(websocket):
    """
    Polls a compressed message from the given web socket.
    
    This function is a coroutine.
    
    Parameters
    ----------
    websocket : ``WebSocketClient``
        The web socket to poll with.
    
    Returns
    -------
    raw_message : `bytes`
    
    Raises
    ------
    ConnectionClosed
        If the web socket connection closed.
    """
    buffer = None
    
    while True:
        data = await websocket.receive()
        if data.endswith(b'\x00\x00\xff\xff'):
            if buffer is None:
                compressed_message = data
            else:
                buffer.append(data)
                compressed_message = b''.join(buffer)
            return compressed_message
        
        if buffer is None:
            buffer = []
        
        buffer.append(data)
        continue


class DiscordGatewayClientShard(DiscordGatewayClientBase):
    """
    Gateway of a client representing a shard.
    
    Attributes
    ----------
    _buffer : `list<bytes>`
        A buffer used to store not finished received payloads.
    _decompressor : `ZlibDecompressorType`
        Zlib decompressor used to decompress the received data.
    _operation_handlers : `dict<int, (instance, dict<str, object>) -> int>`
        Handler for each expected operation.
    _should_run : `bool`
        Whether the gateway should be running.
    client : ``Client``
        The owner client of the gateway.
    kokoro : `None | Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    resume_gateway_url : `None | str`
        The new gateway url to which we should connect on resuming.
    sequence : `None`, `int`
        Last sequence number received.
    session_id : `None | str`
        Last session id received at `READY` event.
    shard_id : `int`
        The shard id of the gateway. If the respective client is not using sharding, it is set to `0` every time.
    websocket : `None | WebSocketClient`
        The web socket client of the gateway.
    """
    __slots__ = (
        '_buffer', '_decompressor', '_operation_handlers', '_should_run', 'client', 'kokoro', 'rate_limit_handler',
        'resume_gateway_url', 'sequence', 'session_id', 'shard_id', 'websocket',
    )
    
    def __new__(cls, client, shard_id):
        """
        Creates a client shard gateway.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        shard_id : `int`
            The shard id of the gateway.
        """
        operation_handlers = {
            GATEWAY_OPERATION_CLIENT_DISPATCH: cls._handle_operation_dispatch,
            GATEWAY_OPERATION_CLIENT_HELLO: cls._handle_operation_hello,
            GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE: cls._handle_operation_heartbeat_acknowledge,
            GATEWAY_OPERATION_CLIENT_HEARTBEAT: cls._handle_operation_heartbeat,
            GATEWAY_OPERATION_CLIENT_RECONNECT: cls._handle_operation_reconnect,
            GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION: cls._handle_operation_invalidate_session,
        }
        
        self = object.__new__(cls)
        self._buffer = []
        self._decompressor = None
        self._operation_handlers = operation_handlers
        self._should_run = False
        self.client = client
        self.kokoro = None
        self.rate_limit_handler = GatewayRateLimiter()
        self.resume_gateway_url = None
        self.sequence = -1
        self.session_id = None
        self.shard_id = shard_id
        self.websocket = None
        return self
    
    
    @copy_docs(DiscordGatewayClientBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(' client = ')
        repr_parts.append(repr(self.client.full_name))
        
        repr_parts.append(', shard_id = ')
        repr_parts.append(repr(self.shard_id))
    
    
    async def run(self, waiter = None):
        """
        Keeps the gateway receiving message and processing it. If the gateway needs to be reconnected, reconnects
        itself. If connecting cannot succeed, because there is no internet returns `False`. If the `.client` is
        stopped, then returns `False`.
        
        This method is a coroutine.
        
        Parameters
        -----------
        waiter : `None | Future<bool>` = `None`, Optional
            A waiter future what is set, when the gateway finished connecting and started polling events.
            Its result is also set in case the task is finished before connection.
        
        Returns
        -------
        outcome : `bool<False>`
            Always `False`.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        DiscordException
        """
        self._should_run = True
        client = self.client
        action = GATEWAY_ACTION_CONNECT
        
        try:
            while True:
                if (not self._should_run) or (not client.running):
                    return False
                
                try:
                    task = Task(KOKORO, self._connect(action == GATEWAY_ACTION_RESUME))
                    task.apply_timeout(GATEWAY_CONNECT_TIMEOUT)
                    action = await task
                    
                    if action != GATEWAY_ACTION_KEEP_GOING:
                        continue
                    
                    if (waiter is not None):
                        waiter.set_result_if_pending(True)
                        waiter = None
                    
                    action = await self._keep_polling_and_handling()
                
                except GeneratorExit:
                    self.abort()
                    raise
                
                except ConnectionClosed as exception:
                    code = exception.code
                    if code in GATEWAY_EXCEPTION_CODE_TABLE:
                        raise DiscordGatewayException(code) from exception
                    
                    if code not in (1000, 1006):
                        await sleep(1.0, KOKORO)
                
                except TimeoutError:
                    pass
                
                except (ConnectionError, InvalidHandshake, OSError, ValueError, WebSocketProtocolError):
                    await sleep(1.0, KOKORO)
                
                else:
                    continue
                
                action = GATEWAY_ACTION_CONNECT
                continue    
                
        finally:
            # set waiter if not set
            if (waiter is not None):
                waiter.set_result_if_pending(False)
                waiter = None
            
            # we are not running anymore.
            self._should_run = False
            
        return False
    
    
    @property
    @copy_docs(DiscordGatewayClientBase.latency)
    def latency(self):
        kokoro = self.kokoro
        if kokoro is None:
            latency = LATENCY_DEFAULT
        else:
            latency = kokoro.latency
        return latency
    
    
    def _cancel_self_and_get_websocket(self):
        """
        Cancels the gateway except its websocket. Returns the websocket if still running instead.
        
        Returns
        -------
        websocket : `None | WebSocketClient`
        """
        kokoro = self.kokoro
        if (kokoro is not None):
            kokoro.stop()
        
        websocket = self.websocket
        if websocket is None:
            return None
        
        self.websocket = None
        
        if websocket.closed:
            return None
        
        return websocket
    
    
    @copy_docs(DiscordGatewayClientBase.terminate)
    async def terminate(self):
        websocket = self._cancel_self_and_get_websocket()
        if (websocket is not None):
            await websocket.close(4000)
    
    
    @copy_docs(DiscordGatewayClientBase.close)
    async def close(self):
        websocket = self._cancel_self_and_get_websocket()
        if (websocket is not None):
            await websocket.close(1000)
    
    
    @copy_docs(DiscordGatewayClientBase.abort)
    def abort(self):
        websocket = self._cancel_self_and_get_websocket()
        if (websocket is not None):
            websocket.close_transport(True)
        
        self._should_run = False
    
    
    @copy_docs(DiscordGatewayClientBase.send_as_json)
    async def send_as_json(self, data):
        websocket = self.websocket
        if websocket is None:
            return
        
        if not (await self.rate_limit_handler):
            return
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed:
            pass
    
    
    @copy_docs(DiscordGatewayClientBase.beat)
    async def beat(self):
        data = {
            'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
            'd': self.sequence,
        }
        
        await self.send_as_json(data)
    
    
    # client base

    
    @copy_docs(DiscordGatewayClientBase.change_voice_state)
    async def change_voice_state(self, guild_id, channel_id, *, self_deaf = False, self_mute = False):
        if guild_id:
            guild_id = str(guild_id)
        else:
            guild_id = None
        
        if channel_id:
            channel_id = str(channel_id)
        else:
            channel_id = None
        
        data = {
            'op': GATEWAY_OPERATION_CLIENT_VOICE_STATE,
            'd': {
                'guild_id': guild_id,
                'channel_id': channel_id,
                'self_deaf': self_deaf,
                'self_mute': self_mute,
            },
        }
        
        await self.send_as_json(data)
    
    
    # connecting, message receive and processing
    
    async def _connect(self, resume):
        """
        Connects the gateway to Discord. If the connecting was successful will start it's `.kokoro` as well.
        
        Parameters
        ----------
        resume : `bool`
            Whether the gateway should try to resume the existing connection.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionError
        OSError
        ValueError
        ConnectionClosed
        InvalidHandshake
        WebSocketProtocolError
        DiscordException
        """
        self._create_kokoro()
        
        websocket = self.websocket
        if (websocket is not None) and (not websocket.closed):
            self.websocket = None
            await websocket.close(4000)
        
        if resume:
            gateway_url = self.resume_gateway_url
        else:
            gateway_url = None
        
        if gateway_url is None:
            gateway_url = await self.client.client_gateway_url()
        
        gateway_url = f'{gateway_url}?encoding=json&v={API_VERSION}&compress=zlib-stream'
        
        self._decompressor = create_zlib_decompressor()
        
        self.websocket = await self.client.http.connect_web_socket(gateway_url)
        self.kokoro.start()
        # skip one loop to wait for kokoro to start up.
        await skip_ready_cycle()
        
        # poll hello
        gateway_action = await self._poll_and_handle_received_operation()
        if gateway_action != GATEWAY_ACTION_KEEP_GOING:
            return gateway_action
        
        if not resume:
            await self._identify()
            return GATEWAY_ACTION_KEEP_GOING
        
        await self._resume()
        
        try:
            await self.websocket.ensure_open()
        except ConnectionClosed:
            # websocket got closed so let's just do a regular connect.
            self._clear_session()
            self.kokoro.stop()
            self.websocket = None
            return GATEWAY_ACTION_CONNECT
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _keep_polling_and_handling(self):
        """
        Keeps polling and handling till decided otherwise.
        
        This function is a coroutine.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionClosed
            If the websocket connection closed.
        """
        try:
            with repeat_timeout(POLL_TIMEOUT) as loop:
                for _ in loop:
                    action = await self._poll_and_handle_received_operation()
                    if action != GATEWAY_ACTION_KEEP_GOING:
                        return action
        
        except TimeoutError:
            # timeout, no internet probably.
            pass
        
        return GATEWAY_ACTION_CONNECT
    
    
    async def _poll_and_handle_received_operation(self):
        """
        Waits for sockets from Discord till it collected a full one. If it did, decompresses and processes it.
        Returns `True`, if the gateway should reconnect.
        
        This method is a coroutine.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionClosed
            If the websocket connection closed.
        TimeoutError
            If the gateways' `.kokoro` is not beating, meanwhile it should.
        """
        websocket = self.websocket
        if websocket is None:
            # No websocket? Were the connection closed?
            return GATEWAY_ACTION_CONNECT
        
        try:
            raw_message = await _poll_compressed_message(websocket)
        except ConnectionClosed as exception:
            # propagate a few kind of `ConnectionClosed` exceptions while swallow the rest for reconnection.
            if exception.code in (1000, 1006, 4004, 4010, 4011, 4013, 4014):
                raise
            
            return GATEWAY_ACTION_CONNECT
        
        try:
            decompressed_message = self._decompressor.decompress(raw_message)
        except ZlibError:
            # we need a full reset
            return GATEWAY_ACTION_CONNECT
        
        # This may raise `TimeoutError`
        return (await self._handle_received_operation(decompressed_message.decode('utf-8')))
    
    
    async def _handle_received_operation(self, message):
        """
        Processes the message sent by Discord. If the message is `DISPATCH`, ensures the specific parser for it and
        returns `False`. For every other operation code it calls ``._handle_special_operation`` and returns that's return.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `bytes`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        # return True if we should reconnect
        message = from_json(message)
        
        sequence = message.get('s', None)
        if (sequence is not None):
            self.sequence = sequence
        
        operation = message['op']
        
        try:
            operation_handler = self._operation_handlers[operation]
        except KeyError:
            client = self.client
            Task(
                KOKORO,
                client.events.error(
                    client,
                    f'{type(self).__name__}._handle_received_operation',
                    f'Unknown operation: {operation!r}\nMessage: {message!r}'
                ),
            )
            return GATEWAY_ACTION_KEEP_GOING
        
        return (await operation_handler(self, message))
    
    
    async def _handle_operation_hello(self, message):
        """
        Handles a hello operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = Kokoro(self)
            self.kokoro = kokoro
        
        data = message.get('d', None)
        if (data is not None):
            interval = data['heartbeat_interval'] / 1000.0
            # send a heartbeat immediately
            kokoro.interval = interval
        
        await kokoro.beat_now()
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_heartbeat_acknowledge(self, message):
        """
        Handles a heartbeat acknowledge operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = Kokoro(self)
            self.kokoro = kokoro
        
        kokoro.answered()
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_heartbeat(self, message):
        """
        Handles a heartbeat operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        kokoro = self.kokoro
        if (kokoro is None) or (kokoro.runner is None):
            return GATEWAY_ACTION_CONNECT
        
        await self.beat()
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_reconnect(self, message):
        """
        Handles a reconnect operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        await self.terminate()
        return GATEWAY_ACTION_RESUME
    
    
    async def _handle_operation_invalidate_session(self, message):
        """
        Handles an invalidate session operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if (data is not None) and isinstance(data, bool) and data:
            # Should sleep between 0 - 5 seconds, but actually dont need to sleep any, derp.
            # await sleep(5.0, KOKORO)
            await self.close()
            return GATEWAY_ACTION_RESUME
        
        self._clear_session()
        return GATEWAY_ACTION_CONNECT
    
    
    async def _handle_operation_dispatch(self, message):
        """
        Handles a dispatch operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        event = message['t']
        
        client = self.client
        try:
            parser = PARSERS[event]
        except KeyError:
            call_unknown_dispatch_event_event_handler(client, event, data)
            return GATEWAY_ACTION_KEEP_GOING
        
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        try:
            if parser(client, data) is None:
                return GATEWAY_ACTION_KEEP_GOING
        except BaseException as err:
            Task(KOKORO, client.events.error(client, event, err))
            return GATEWAY_ACTION_KEEP_GOING
        
        if event == 'READY':
            self.session_id = data.get('session_id', None)
            self.resume_gateway_url = data.get('resume_gateway_url', None)
        
        # elif event == 'RESUMED':
            # pass
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    def _clear_session(self):
        """
        Clears current session data, disabling the option of resuming the connection.
        """
        self.session_id = None
        self.sequence = -1
        self.resume_gateway_url = None
    
    
    async def _identify(self):
        """
        Sends an `GATEWAY_OPERATION_CLIENT_IDENTIFY` packet to Discord.
        
        This method is a coroutine.
        """
        client = self.client
        activity = client._activity
        if activity is ACTIVITY_UNKNOWN:
            activity_data = None
        else:
            activity_data = activity.to_data(user = not client.bot)
        
        status_value = client._status.value
        
        data = {
            'op': GATEWAY_OPERATION_CLIENT_IDENTIFY,
            'd': {
                'token': client.token,
                'properties': {
                    'os': PLATFORM,
                    'browser': LIBRARY_NAME,
                    'device': LIBRARY_NAME,
                },
                'compress': True,                       # Whether we support compression | Discord default: False
                'large_threshold': LARGE_GUILD_LIMIT,   # between 50 and 250             | Discord default: 50
                'guild_subscriptions': CACHE_PRESENCE,  # optional                       | Discord default: False
                'intents': client.intents,              # Grip & Break down              | Discord Default: all-p-gu
                'v': 3,
                'presence': {
                    'status': status_value,
                    'game': activity_data,
                    'since': 0.0,
                    'afk': False,
                },
            },
        }
        
        shard_count = client.shard_count
        if shard_count:
            data['d']['shard'] = [self.shard_id, shard_count]
        
        await self.send_as_json(data)
    
    
    async def _resume(self):
        """
        Sends a `GATEWAY_OPERATION_CLIENT_RESUME` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op': GATEWAY_OPERATION_CLIENT_RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.client.token,
            },
        }
        
        await self.send_as_json(data)

    
    async def _send_json(self, data):
        """
        Internal function to send already converted json data.
        
        If the given gateway has no websocket, or if it is closed, will not raise.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `str`
            The data to send.
        """
        websocket = self.websocket
        if websocket is None:
            return
        
        if not (await self.rate_limit_handler):
            return
        
        try:
            await websocket.send(data)
        except ConnectionClosed:
            pass
    
    
    def _create_kokoro(self):
        """
        Creates the gateway's kokoro.
        """
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = Kokoro(self)
        else:
            kokoro.stop()
