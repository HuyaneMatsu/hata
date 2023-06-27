__all__ = ()

import sys, zlib

from scarletio import Future, Task, TaskGroup, from_json, repeat_timeout, sleep, to_json
from scarletio.web_common import ConnectionClosed, InvalidHandshake, WebSocketProtocolError

from ...env import API_VERSION, CACHE_PRESENCE, LIBRARY_NAME

from ..activity import ACTIVITY_UNKNOWN
from ..core import KOKORO
from ..events.core import PARSERS
from ..events.handling_helpers import call_unknown_dispatch_event_event_handler
from ..exceptions import DiscordGatewayException, GATEWAY_EXCEPTION_CODE_TABLE
from ..guild.guild.constants import LARGE_GUILD_LIMIT

from .heartbeat import Kokoro
from .rate_limit import GatewayRateLimiter


TIMEOUT_GATEWAY_CONNECT = 30.0
TIMEOUT_POLL = 60.0

DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
PRESENCE = 3
VOICE_STATE = 4
VOICE_PING = 5
RESUME = 6
RECONNECT = 7
REQUEST_GUILD_USERS = 8
INVALIDATE_SESSION = 9
HELLO = 10
HEARTBEAT_ACK = 11
GUILD_SYNC = 12
REQUEST_SOUNDBOARD_SOUNDS = 31

"""
DISPATCH : `int` = `0`
    Receive only, used at ``DiscordGateway._received_message``.
HEARTBEAT : `int` = `1`
    Send and receive, used at ``._beat`` and at ``._special_operation``.
IDENTIFY : `int` = `2`
    Send only, used ``DiscordGateway._identify``.
PRESENCE : `int` = `3`
    Send only, used at ``Client.edit_presence``.
VOICE_STATE : `int` = `4`
    Send only, used at ``DiscordGateway.change_voice_state``
VOICE_PING : `int` = `5`
    Removed.
RESUME : `int` = `6`
    Send only, used at ``DiscordGateway._resume``.
RECONNECT : `int` = `7`
    Receive only, used at ``._special_operation``.
REQUEST_GUILD_USERS : `int` = `8`
    Send only, used at ``Client._request_users_loop``, ``Client._request_users`` and at
    ``Client.request_member``.
INVALIDATE_SESSION : `int` = `9`
    Receive only, used at ``DiscordGateway._special_operation``.
HELLO : `int` = `10`
    Receive only, used at ``DiscordGateway._special_operation``.
HEARTBEAT_ACK : `int` = `11`
    Receive only, used at ``DiscordGateway._special_operation``.
GUILD_SYNC : `int` = `12`
    Send only, not used.
REQUEST_SOUNDBOARD_SOUNDS : `int` = `13`
    Send only, used to request the guilds' soundboard sounds.
"""

class DiscordGateway:
    """
    The gateway used by ``Client``-s to communicate with Discord with secure websocket.
    
    Attributes
    ----------
    _buffer : `bytearray`
        A buffer used to store not finished received payloads.
    _decompressor : `zlib.Decompress`
        Zlib decompressor used to decompress the received data.
    client : ``Client``
        The owner client of the gateway.
    kokoro : `None`, `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    resume_gateway_url : `None`, `str`
        The new gateway url to which we should connect on resuming.
    sequence : `None`, `int`
        Last sequence number received.
    session_id : `None`, `str`
        Last session id received at `READY`.
    shard_id : `int`
        The shard id of the gateway. If the respective client is not using sharding, it is set to `0` every time.
    websocket : `None`, `WebSocketClient`
        The websocket client of the gateway.
    """
    __slots__ = (
        '_buffer', '_decompressor', 'client', 'kokoro', 'rate_limit_handler', 'resume_gateway_url', 'sequence',
        'session_id', 'shard_id', 'websocket',
    )
    
    def __new__(cls, client, shard_id = 0):
        """
        Creates a gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        shard_id : `int` = `0`, Optional
            The shard id of the gateway. Defaults to `0`, if the owner client does not use sharding.
        """
        self = object.__new__(cls)
        
        self._buffer = bytearray()
        self._decompressor = None
        self.client = client
        self.kokoro = None
        self.rate_limit_handler = GatewayRateLimiter()
        self.resume_gateway_url = None
        self.sequence = None
        self.session_id = None
        self.shard_id = shard_id
        self.websocket = None
        
        return self
    
    
    async def start(self):
        """
        Starts the gateway's ``.kokoro``.
        
        This method is a coroutine.
        """
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self)
            return
        
        await kokoro.restart()
    
    
    async def run(self, waiter = None):
        """
        Keeps the gateway receiving message and processing it. If the gateway needs to be reconnected, reconnects
        itself. If connecting cannot succeed, because there is no internet returns `True`. If the `.client` is
        stopped, then returns `False`.
        
        If `True` is returned the respective client stops all other gateways as well and tries to reconnect. When
        the internet is back the client will launch back the gateway.
        
        This method is a coroutine.
        
        Parameters
        -----------
        waiter : `None`, ``Future`` = `None`, Optional
            A waiter future what is set, when the gateway finished connecting and started polling events.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        DiscordException
        """
        client = self.client
        while True:
            try:
                task = Task(KOKORO, self._connect())
                task.apply_timeout(TIMEOUT_GATEWAY_CONNECT)
                await task
                
                if (waiter is not None):
                    waiter.set_result(None)
                    waiter = None
                
                
                while True:
                    try:
                        with repeat_timeout(TIMEOUT_POLL) as loop:
                            for _ in loop:
                                should_reconnect = await self._poll_event()
                                if should_reconnect:
                                    if client.running:
                                        break
                                    
                                    return
                    
                    except TimeoutError:
                        # timeout, no internet probably
                        return
                    
                    task = Task(KOKORO, self._connect(resume = True))
                    task.apply_timeout(TIMEOUT_GATEWAY_CONNECT)
                    await task
            
            except (
                OSError, TimeoutError, ConnectionError, ConnectionClosed, WebSocketProtocolError, InvalidHandshake,
                ValueError
            ) as err:
                if not client.running:
                    return
                
                if isinstance(err, ConnectionClosed):
                    code = err.code
                    if code in (1000, 1006):
                        continue
                    
                    if code in GATEWAY_EXCEPTION_CODE_TABLE:
                        raise DiscordGatewayException(code) from err
                
                if isinstance(err, TimeoutError):
                    continue
                
                if isinstance(err, ConnectionError): # no internet
                    return
                
                await sleep(1.0, KOKORO)
    
    # connecting, message receive and processing
    
    async def _connect(self, resume = False):
        """
        Connects the gateway to Discord. If the connecting was successful will start it's `.kokoro` as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        resume : `bool` = `False`, Optional
            Whether the gateway should try to resume the existing connection.
        
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
        while True:
            self.kokoro.terminate()
            websocket = self.websocket
            if (websocket is not None) and (not websocket.closed):
                await websocket.close(4000)
                self.websocket = None
            
            self._decompressor = zlib.decompressobj()
            
            if resume:
                gateway_url = self.resume_gateway_url
            else:
                gateway_url = None
            
            if gateway_url is None:
                gateway_url = await self.client.client_gateway_url()
            
            gateway_url = f'{gateway_url}?encoding=json&v={API_VERSION}&compress=zlib-stream'
            
            self.websocket = await self.client.http.connect_websocket(gateway_url)
            self.kokoro.start_beating()
            
            if not resume:
                await self._identify()
                return
            
            await self._resume()
            
            try:
                await self.websocket.ensure_open()
            except ConnectionClosed:
                # websocket got closed so let's just do a regular IDENTIFY connect.
                self.clear_session()
                continue
            
            return
    
    
    async def _poll_event(self):
        """
        Waits for sockets from Discord till it collected a full one. If it did, decompresses and processes it.
        Returns `True`, if the gateway should reconnect.
        
        This method is a coroutine.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        ConnectionClosed
            If the websocket connection closed.
        TimeoutError
            If the gateways' `.kokoro` is not beating, meanwhile it should.
        """
        websocket = self.websocket
        if websocket is None:
            return True
        
        buffer = self._buffer
        try:
            while True:
                message = await websocket.receive()
                if len(message) >= 4 and message[-4:] == b'\x00\x00\xff\xff':
                    if buffer:
                        buffer.extend(message)
                        message = self._decompressor.decompress(buffer).decode('utf-8')
                        buffer.clear()
                    else:
                        message = self._decompressor.decompress(message).decode('utf-8')
                    return (await self._received_message(message))
                else:
                    buffer.extend(message)
        except ConnectionClosed as err:
            if err.code in (1000, 1006, 4004, 4010, 4011, 4013, 4014):
                raise err
            return True
        except zlib.error as err:
            # we need a full reset
            return True
    
    async def _received_message(self, message):
        """
        Processes the message sent by Discord. If the message is `DISPATCH`, ensures the specific parser for it and
        returns `False`. For every other operation code it calls ``._special_operation`` and returns that's return.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `bytes`
            The received message.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        TimeoutError
            If the gateway's `.kokoro` is not beating, meanwhile it should.
        """
        # return True if we should reconnect
        message = from_json(message)
        
        operation = message['op']
        data = message.get('d', None)
        sequence = message.get('s', None)
        
        if sequence is not None:
            self.sequence = sequence
        
        if operation:
            return await self._special_operation(operation, data)
        
        # self.DISPATCH
        event = message['t']
        client = self.client
        try:
            parser = PARSERS[event]
        except KeyError:
            call_unknown_dispatch_event_event_handler(client, event, data)
            return False
        
        if data is None:
            return
        
        try:
            if parser(client, data) is None:
                return False
        except BaseException as err:
            Task(KOKORO, client.events.error(client, event, err))
            return False
        
        if event == 'READY':
            self.session_id = data['session_id']
            self.resume_gateway_url = data.get('resume_gateway_url', None)
        
        # elif event == 'RESUMED':
            # pass
        
        return False
    
    
    async def _special_operation(self, operation, data):
        """
        Handles special operations (so everything except `DISPATCH`). Returns `True` if the gateway should reconnect.
        
        This method is a coroutine.
        
        Parameters
        ----------
        operation : `int`
            The gateway operation's code what the function will handle.
        data : `None`, `dict` of (`str`, `Any`) items
            Deserialized json data.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        TimeoutError
            If the gateways' `.kokoro` is not beating, meanwhile it should.
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = await Kokoro(self)
        
        if operation == HELLO:
            if (data is not None):
                interval = data['heartbeat_interval'] / 1000.0
                # send a heartbeat immediately
                kokoro.interval = interval
            
            await kokoro.beat_now()
            return False
        
        if operation == HEARTBEAT_ACK:
            kokoro.answered()
            return False
        
        if kokoro.beater is None:
            raise TimeoutError
            
        if operation == HEARTBEAT:
            await self._beat()
            return False
        
        if operation == RECONNECT:
            await self.terminate()
            return True
        
        if operation == INVALIDATE_SESSION:
            if (data is not None) and isinstance(data, bool) and data:
                await sleep(5.0, KOKORO)
                await self.close()
                return True
            
            self.clear_session()
            
            await self._identify()
            return False
        
        client = self.client
        Task(
            KOKORO,
            client.events.error(
                client,
                f'{self.__class__.__name__}._special_operation',
                f'Unknown operation {operation}\nData: {data!r}'
            ),
        )
        
        return False
        
    # general stuffs
    
    @property
    def latency(self):
        """
        The latency of the websocket in seconds. If no latency is recorded, will return `Kokoro.DEFAULT_LATENCY`.
        
        Returns
        -------
        latency : `float`
        """
        kokoro = self.kokoro
        if kokoro is None:
            latency = Kokoro.DEFAULT_LATENCY
        else:
            latency = kokoro.latency
        return latency
    
    
    async def terminate(self):
        """
        Terminates the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `4000`.
        
        This method is a coroutine.
        """
        self.kokoro.terminate()
        websocket = self.websocket
        if websocket is None:
            return
        self.websocket = None
        await websocket.close(4000)
    
    
    async def close(self):
        """
        Cancels the gateway's ``.kokoro`` and closes it's ``.websocket`` with close code of `1000`.
        
        This method is a coroutine.
        """
        self.kokoro.cancel()
        self.rate_limit_handler.cancel()
        
        websocket = self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(1000)
    
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``. If there is no websocket, or the websocket
        is closed will not raise.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        websocket = self.websocket
        if websocket is None:
            return
        
        if await self.rate_limit_handler:
            return
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed:
            pass
    
    
    def __repr__(self):
        """Returns the representation of the gateway."""
        return f'<{self.__class__.__name__} client = {self.client.full_name!r}, shard_id = {self.shard_id}>'
    
    # Special operations
    
    async def _identify(self):
        """
        Sends an `IDENTIFY` packet to Discord.
        
        This method is a coroutine.
        """
        client = self.client
        activity = client._activity
        if activity is ACTIVITY_UNKNOWN:
            activity = None
        else:
            activity = activity.to_data(user = not client.bot)
        
        status = client._status.value
        
        data = {
            'op': IDENTIFY,
            'd': {
                'token': client.token,
                'properties': {
                    'os': sys.platform,
                    'browser': LIBRARY_NAME,
                    'device': LIBRARY_NAME,
                },
                'compress': True,                       # Whether we support compression | Discord default: False
                'large_threshold': LARGE_GUILD_LIMIT,   # between 50 and 250             | Discord default: 50
                'guild_subscriptions': CACHE_PRESENCE,  # optional                       | Discord default: False
                'intents': client.intents,              # Grip & Break down              | Discord Default: all-p-gu
                'v': 3,
                'presence': {
                    'status': status,
                    'game': activity,
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
        Sends a `RESUME` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op': RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.client.token,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def change_voice_state(self, guild_id, channel_id, self_mute=False, self_deaf=False):
        """
        Sends a `VOICE_STATE` packet to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild_id : `int`
            The voice client's guild's id.
        channel_id : `int`
            The voice client's channel's id.
        self_mute : `bool` = `False`, Optional
            Whether the voice client is muted.
        self_deaf : `bool` = `False`, Optional
            Whether the voice client is deafen.
        """
        if (guild_id is not None) and (guild_id == 0):
            guild_id = None
        
        if (channel_id is not None) and (channel_id == 0):
            channel_id = None
        
        data = {
            'op': VOICE_STATE,
            'd': {
                'guild_id': guild_id,
                'channel_id': channel_id,
                'self_mute': self_mute,
                'self_deaf': self_deaf,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _beat(self):
        """
        Sends a `VOICE_STATE` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op': HEARTBEAT,
            'd': self.sequence,
        }
        
        await self.send_as_json(data)
    
    
    def clear_session(self):
        """
        Clears current session data, disabling the option of resuming the connection.
        """
        self.session_id = None
        self.sequence = None
        self.resume_gateway_url = None


class DiscordGatewaySharder:
    """
    Sharder gateway used to control more ``DiscordGateway``-s at the same time.
    
    Attributes
    ----------
    client : ``Client``
        The owner client of the gateway.
    gateways : `list` of ``DiscordGateway``
        The controlled gateways.
    """
    __slots__ = ('client', 'gateways',)
    
    def __new__(cls, client):
        """
        Creates a sharder gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        """
        gateways = [DiscordGateway(client, shard_id) for shard_id in range(client.shard_count)]
        
        self = object.__new__(cls)
        self.client = client
        self.gateways = gateways
        return self
    
    
    def reshard(self):
        """
        Modifies the shard amount of the gateway sharder.
        
        Should be called only if every shard is down.
        """
        gateways = self.gateways
        
        old_shard_count = len(gateways)
        new_shard_count = self.client.shard_count
        if new_shard_count > old_shard_count:
            for shard_id in range(old_shard_count, new_shard_count):
                gateway = DiscordGateway(self, shard_id)
                gateways.append(gateway)
        
        elif new_shard_count < old_shard_count:
            for _ in range(new_shard_count, old_shard_count):
                gateways.pop()
    
    
    async def start(self):
        """
        Starts the gateways of the sharder gateway.
        
        This method is a coroutine.
        """
        task_group = TaskGroup(KOKORO, (Task(KOKORO, gateway.start()) for gateway in self.gateways))
        failed_task = await task_group.wait_exception()
        if (failed_task is not None):
            task_group.cancel_all()
            failed_task.get_result()
    
    
    async def run(self):
        """
        Runs the gateway sharder's gateways. If any of them returns, stops the rest as well. And if any of them
        returned `True`, then returns `True`, else `False`.
        
        This method is a coroutine.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        DiscordException
            Any exception raised by the discord API when connecting.
        """
        max_concurrency = self.client._gateway_max_concurrency
        gateways = self.gateways
        
        index = 0
        limit = len(gateways)
        
        # At every step we add up to max_concurrency gateways to launch up. When a gateway is launched up, the waiter
        # yields a ``Future`` and if the same amount of ``Future`` is yielded as gateway started up, then we do the next
        # loop. An exception is, when the waiter yielded a ``Task``, because t–en 1 of our gateway stopped with no
        # internet stop, or it was stopped by the client, so we abort all the launching and return.
        task_group = TaskGroup(KOKORO)
        
        while True:
            left_from_batch = 0
            while True:
                future = task_group.create_future()
                task_group.create_task(gateways[index].run(future))
                
                index += 1
                left_from_batch += 1
                if index == limit:
                    break
                
                if left_from_batch == max_concurrency:
                    break
                
                continue
            
            while True:
                try:
                    done_future = await task_group.wait_first_and_pop()
                except:
                    task_group.cancel_all()
                    raise
                
                # We do not have any task?
                if done_future is None:
                    break
                
                if type(done_future) is Future:
                    left_from_batch -= 1
                    
                    if left_from_batch:
                        continue
                    
                    break
                
                # If we retrieved a task instead of a future, we cancel all and propagate the received exception if
                # there is any.
                task_group.cancel_all()
                done_future.get_result()
                return
            
            if index == limit:
                break
            
            # Each gateway does an `IDENTIFY` on connection. You can send `max_concurrency` amount of identifies every
            # second. That means here we sleep `5` seconds. We could rush this 5 seconds, but no need.
            await sleep(5.0, KOKORO)
            continue
        
        try:
            failed_task = await task_group.wait_exception()
        except:
            task_group.cancel_all()
            raise
        
        # If any tasks failed, cancel all other tasks and propagate the exception.
        if (failed_task is not None):
            task_group.cancel_all()
            failed_task.get_result()
    
    
    @property
    def latency(self):
        """
        The average latency of the gateways' websockets in seconds. If no latency was recorded, will return
        `Kokoro.DEFAULT_LATENCY`.
        
        Returns
        -------
        latency : `float`
        """
        total = 0.0
        count = 0
        for gateway in self.gateways:
            kokoro = gateway.kokoro
            if kokoro is None:
                continue
            total += kokoro.latency
            count += 1
        
        if count:
            return total / count
        
        return Kokoro.DEFAULT_LATENCY
    
    
    async def terminate(self):
        """
        Terminates the gateway sharder's gateways.
        
        This method is a coroutine.
        """
        await TaskGroup(KOKORO, (Task(KOKORO, gateway.terminate()) for gateway in self.gateways)).wait_all()
    
    
    async def close(self):
        """
        Cancels the gateway sharder's gateways.
        
        This method is a coroutine.
        """
        await TaskGroup(KOKORO, (Task(KOKORO, gateway.close()) for gateway in self.gateways)).wait_all()
    
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        data = to_json(data)
        
        task_group = TaskGroup(KOKORO, (Task(KOKORO, self._send_json(gateway, data)) for gateway in self.gateways))
        failed_task = await task_group.wait_exception()
        if (failed_task is not None):
            task_group.cancel_all()
            failed_task.get_result()
    
    
    @staticmethod
    async def _send_json(gateway, data):
        """
        Internal function of the gateways sharder to send already converted data with it's gateways.
        
        If the given gateway has no websocket, or if it is closed, will not raise.
        
        This method is a coroutine.
        """
        websocket = gateway.websocket
        if websocket is None:
            return
        
        if await gateway.rate_limit_handler:
            return
        
        try:
            await websocket.send(data)
        except ConnectionClosed:
            pass
    
    
    def __repr__(self):
        """Returns the representation of the gateway sharder."""
        return f'<{self.__class__.__name__} client={self.client.full_name}, shard_count={self.client.shard_count}>'
