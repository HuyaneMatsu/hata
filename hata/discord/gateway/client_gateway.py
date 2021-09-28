__all__ = ()

import sys, zlib

from ...env import CACHE_PRESENCE
from ...backend.futures import sleep, Task, future_or_timeout, WaitTillExc, WaitTillAll, Future, WaitContinuously
from ...backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake
from ...backend.utils import to_json, from_json

from ..activity import ACTIVITY_UNKNOWN
from ..events.core import PARSERS
from ..guild import LARGE_GUILD_LIMIT
from ..core import KOKORO
from ..exceptions import DiscordGatewayException, GATEWAY_EXCEPTION_CODE_TABLE

from .heartbeat import Kokoro
from .rate_limit import GatewayRateLimiter

DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
PRESENCE = 3
VOICE_STATE = 4
VOICE_PING = 5
RESUME = 6
RECONNECT = 7
REQUEST_MEMBERS = 8
INVALIDATE_SESSION = 9
HELLO = 10
HEARTBEAT_ACK = 11
GUILD_SYNC = 12


"""
DISPATCH : `int` = `0`
    Receive only, used at ``DiscordGateway._received_message``.
HEARTBEAT : `int` = `1`
    Send and receive, used at ``._beat`` and at ``._special_operation``.
IDENTIFY : `int` = `2`
    Send only, used ``DiscordGateway._identify``.
PRESENCE : `int` = `3`
    Send only, used at ``Client.client_edit_presence``.
VOICE_STATE : `int` = `4`
    Send only, used at ``DiscordGateway.change_voice_state``
VOICE_PING : `int` = `5`
    Removed.
RESUME : `int` = `6`
    Send only, used at ``DiscordGateway._resume``.
RECONNECT : `int` = `7`
    Receive only, used at ``._special_operation``.
REQUEST_MEMBERS : `int` = `8`
    Send only, used at ``Client._request_members_loop``, ``Client._request_members`` and at
    ``Client.request_member``.
INVALIDATE_SESSION : `int` = `9`
    Receive only, used at ``DiscordGateway._special_operation``.
HELLO : `int` = `10`
    Receive only, used at ``DiscordGateway._special_operation``.
HEARTBEAT_ACK : `int` = `11`
    Receive only, used at ``DiscordGateway._special_operation``.
GUILD_SYNC : `int` = `12`
    Send only, not used.
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
    kokoro : `None` or `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    sequence : `None` or `int`
        Last sequence number received.
    session_id : `None` or `str`
        Last session id received at `READY`.
    shard_id : `int`
        The shard id of the gateway. If the respective client is not using sharding, it is set to `0` every time.
    websocket : `None` or `WSClient`
        The websocket client of the gateway.
    """
    __slots__ = ('_buffer', '_decompressor', 'client', 'kokoro', 'rate_limit_handler', 'sequence', 'session_id',
        'shard_id', 'websocket')

    
    def __init__(self, client, shard_id=0):
        """
        Creates a gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        shard_id : `int`, Optional
            The shard id of the gateway. Defaults to `0`, if the owner client does not use sharding.
        """
        self.client = client
        self.shard_id = shard_id
        self.websocket = None
        self._buffer = bytearray()
        self._decompressor = None
        self.sequence = None
        self.session_id = None
        
        self.kokoro = None
        self.rate_limit_handler = GatewayRateLimiter()
    
    
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
    
    
    async def run(self, waiter=None):
        """
        Keeps the gateway receiving message and processing it. If the gateway needs to be reconnected, reconnects
        itself. If connecting cannot succeed, because there is no internet returns `True`. If the `.client` is
        stopped, then returns `False`.
        
        If `True` is returned the respective client stops all other gateways as well and tries to reconnect. When
        the internet is back the client will launch back the gateway.
        
        This method is a coroutine.
        
        Parameters
        -----------
        waiter : ``Future``, Optional
            A waiter future what is set, when the gateway finished connecting and started polling events.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        InvalidToken
            When the client's token is invalid.
        DiscordException
        """
        client = self.client
        while True:
            try:
                task = Task(self._connect(), KOKORO)
                future_or_timeout(task, 30.0)
                await task
                
                if (waiter is not None):
                    waiter.set_result(None)
                    waiter = None
                
                while True:
                    task = Task(self._poll_event(), KOKORO)
                    future_or_timeout(task, 60.0)
                    try:
                        should_reconnect = await task
                    except TimeoutError:
                        # timeout, no internet probably
                        return
                    
                    if should_reconnect:
                        if not client.running:
                            return
                        
                        task = Task(self._connect(resume=True,), KOKORO)
                        future_or_timeout(task, 30.0)
                        await task
            
            except (OSError, TimeoutError, ConnectionError, ConnectionClosed, WebSocketProtocolError, InvalidHandshake,
                    ValueError) as err:
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
    
    async def _connect(self, resume=False):
        """
        Connects the gateway to Discord. If the connecting was successful will start it's `.kokoro` as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        resume : `bool`
            Whether the gateway should try to resume the existing connection.
        
        Raises
        ------
        ConnectionError
        OSError
        ValueError
        ConnectionClosed
        InvalidHandshake
        WebSocketProtocolError
        InvalidToken
            When the client's token is invalid
        DiscordException
        """
        while True:
            self.kokoro.terminate()
            websocket = self.websocket
            if (websocket is not None) and (not websocket.closed):
                await websocket.close(4000)
                self.websocket = None
            
            self._decompressor = zlib.decompressobj()
            gateway_url = await self.client.client_gateway_url()
            self.websocket = await self.client.http.connect_ws(gateway_url)
            self.kokoro.start_beating()
            
            if not resume:
                await self._identify()
                return
            
            await self._resume()
            
            try:
                await self.websocket.ensure_open()
            except ConnectionClosed:
                # websocket got closed so let's just do a regular IDENTIFY connect.
                self.session_id = None
                self.sequence = None
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
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
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
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        # return True if we should reconnect
        message = from_json(message)
        
        operation = message['op']
        data = message['d']
        sequence = message['s']
        
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
            Task(client.events.error(client,
                f'{self.__class__.__name__}._received_message',
                f'Unknown dispatch event {event}\nData: {data!r}'),
                KOKORO,
            )
            
            return False
        
        try:
            if parser(client, data) is None:
                return False
        except BaseException as err:
            Task(client.events.error(client, event, err), KOKORO)
            return False
        
        if event == 'READY':
            self.session_id = data['session_id']
        #elif event=='RESUMED':
            #pass
        
        return False

    async def _special_operation(self, operation, data):
        """
        Handles special operations (so everything except `DISPATCH`). Returns `True` if the gateway should reconnect.
        
        This method is a coroutine.
        
        Parameters
        ----------
        operation : `int`
            The gateway operation's code what the function will handle.
        data : `dict` of (`str`, `Any`) items
            Deserialized json data.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = await Kokoro(self)
        
        if operation == HELLO:
            interval = data['heartbeat_interval']/1000.0
            #send a heartbeat immediately
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
            if data:
                await sleep(5.0, KOKORO)
                await self.close()
                return True
            
            self.session_id = None
            self.sequence = None
            
            await self._identify()
            return False
        
        client = self.client
        Task(client.events.error(client,
            f'{self.__class__.__name__}._special_operation',
            f'Unknown operation {operation}\nData: {data!r}'),
                KOKORO,
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
        return f'<{self.__class__.__name__} client={self.client.full_name!r}, shard_id={self.shard_id}>'
    
    #special operations
    
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
            if client.is_bot:
                activity = activity.bot_dict()
            else:
                activity = activity.user_dict()
        
        status = client._status.value
        
        data = {
            'op': IDENTIFY,
            'd': {
                'token': client.token,
                'properties': {
                    '$os': sys.platform,
                    '$browser': 'hata',
                    '$device': 'hata',
                    '$referrer': '',
                    '$referring_domain': '',
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
        self_mute : `bool`
            Whether the voice client is muted.
        self_deaf : `bool`
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
    
    def __init__(self, client):
        """
        Creates a sharder gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        """
        self.client = client
        
        gateways = []
        for shard_id in range(client.shard_count):
            gateway = DiscordGateway(client,shard_id)
            gateways.append(gateway)
        
        self.gateways = gateways
    
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
        tasks = []
        for gateway in self.gateways:
            task = Task(gateway.start(), KOKORO)
            tasks.append(task)
        
        await WaitTillExc(tasks, KOKORO)
        
        for task in tasks:
            task.cancel()
    
    async def run(self):
        """
        Runs the gateway sharder's gateways. If any of them returns, stops the rest as well. And if any of them
        returned `True`, then returns `True`, else `False`.
        
        This method is a coroutine.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        InvalidToken
            When the client's token is invalid.
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
        waiter = WaitContinuously(None, KOKORO)
        while True:
            if index == limit:
                break
            
            left_from_batch = 0
            while True:
                future = Future(KOKORO)
                waiter.add(future)
                
                task = Task(gateways[index].run(future), KOKORO)
                waiter.add(task)
                
                index += 1
                left_from_batch += 1
                if index == limit:
                    break
                
                if left_from_batch == max_concurrency:
                    break
                
                continue
            
            while True:
                try:
                    result = await waiter
                except:
                    waiter.cancel()
                    raise
                
                waiter.reset()
                
                if type(result) is Future:
                    left_from_batch -= 1
                    
                    if left_from_batch:
                        continue
                    
                    break
                
                waiter.cancel()
                result.result()
            
            # We could time gateway connect rate limit more precisely, but this is already fine. We don't need to rush
            # it, there is many gateway to connect and sync with.
            await sleep(5.0, KOKORO)
            
            continue
        
        try:
            result = await waiter
        finally:
            waiter.cancel()
        
        result.result()
    
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
            return total/count
        
        return Kokoro.DEFAULT_LATENCY
    
    async def terminate(self):
        """
        Terminates the gateway sharder's gateways.
        
        This method is a coroutine.
        """
        tasks = []
        for gateway in self.gateways:
            task = Task(gateway.terminate(), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    
    async def close(self):
        """
        Cancels the gateway sharder's gateways.
        
        This method is a coroutine.
        """
        tasks = []
        for gateway in self.gateways:
            task = Task(gateway.close(), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        data = to_json(data)
        
        tasks = []
        for gateway in self.gateways:
            task = Task(self._send_json(gateway, data), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillExc(tasks, KOKORO)
        
        for task in pending:
            task.cancel()
        
        for task in done:
            task.result()
    
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
