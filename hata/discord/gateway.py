# -*- coding: utf-8 -*-
import sys, zlib
from time import time as time_now
from collections import deque

try:
    import nacl.secret
except ImportError:
    SecretBox = None
else:
    SecretBox = nacl.secret.SecretBox
    del nacl

from ..env import CACHE_PRESENCE
from ..backend.futures import sleep, Task, future_or_timeout, WaitTillExc, WaitTillAll, Future, WaitContinuously
from ..backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake
from ..backend.event_loop import LOOP_TIME

from .utils import to_json, from_json
from .activity import ActivityUnknown
from .parsers import PARSERS
from .guild import LARGE_LIMIT
from .client_core import Kokoro, KOKORO
from .exceptions import DiscordGatewayException, VOICE_CLIENT_DISCONNECT_CLOSE_CODE

GATEWAY_RATE_LIMIT_LIMIT = 120
GATEWAY_RATE_LIMIT_RESET = 60.0

class GatewayRateLimiter:
    """
    Burst rate limit handler for gateways, what operates on the clients' loop only.
    
    Attributes
    ----------
    queue : `deque` of ``Future``
        The queue of the rate limit handler. It is filled up with futures, if the handler's limit is exhausted.
        These futures are removed and their result is set, when the limit is reset.
    remaining : `int`
        The amount of requests which can be done, before the limit is exhausted.
    resets_at : `float`
        When the rate limit of the respective gateway will be reset.
    wake_upper : `None`  or `TimerHandle`
        A handler what will reset the limiter's limit and ensure it's queue if needed.
    """
    __slots__ = ('queue', 'remaining', 'resets_at', 'wake_upper', )
    
    def __init__(self):
        """
        Creates a gateway rate limiter.
        """
        self.remaining = GATEWAY_RATE_LIMIT_LIMIT
        self.queue = deque()
        self.wake_upper = None
        self.resets_at = 0.0
    
    def __iter__(self):
        """
        Awaits the rate limit handler.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        cancelled : `bool`
            Whether the respective gateway was closed.
        """
        now = LOOP_TIME()
        if now >= self.resets_at:
            self.resets_at = now+GATEWAY_RATE_LIMIT_RESET
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            remaining = self.remaining
        
        if remaining:
            self.remaining = remaining-1
            return False
        
        if self.wake_upper is None:
            self.wake_upper = KOKORO.call_at(self.resets_at, type(self).wake_up, self)
        
        future = Future(KOKORO)
        self.queue.append(future)
        return (yield from future)
    
    __await__ = __iter__
    
    def wake_up(self):
        """
        Wake ups the waiting futures of the ``GatewayRateLimiter``.
        """
        queue = self.queue
        remaining = GATEWAY_RATE_LIMIT_LIMIT
        if queue:
            while True:
                if not queue:
                    wake_upper = None
                    break
                
                if not remaining:
                    self.resets_at = resets_at = LOOP_TIME() + GATEWAY_RATE_LIMIT_RESET
                    wake_upper = KOKORO.call_at(resets_at + GATEWAY_RATE_LIMIT_RESET, type(self).wake_up, self)
                    break
                
                queue.popleft().set_result_if_pending(False)
                remaining -= 1
        
        else:
            wake_upper = None
        
        self.wake_upper = wake_upper
        self.remaining = remaining
    
    def cancel(self):
        """
        Cancels the ``GatewayRateLimiter``'s queue and it's `.wake_upper` if set.
        """
        queue = self.queue
        while queue:
            queue.popleft().set_result_if_pending(True)
        
        wake_upper = self.wake_upper
        if (wake_upper is not None):
            self.wake_upper = None
            wake_upper.cancel()
    
    def __repr__(self):
        """Returns the gateway rate limiter's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        resets_at = self.resets_at
        if resets_at <= LOOP_TIME():
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            result.append(' resets_at=')
            result.append(repr(LOOP_TIME()))
            result.append(' (monotonic),')
            
            remaining = self.remaining
        
        result.append(' remaining=')
        result.append(repr(remaining))
        result.append('>')
        
        return ''.join(result)

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
    
    Class Attributes
    ----------------
    DISPATCH : `int` = `0`
        Receive only, used at ``._received_message``.
    HEARTBEAT : `int` = `1`
        Send and receive, used at ``._beat`` and at ``._special_operation``.
    IDENTIFY : `int` = `2`
        Send only, used ``._identify``.
    PRESENCE : `int` = `3`
        Send only, used at ``Client.client_edit_presence``.
    VOICE_STATE : `int` = `4`
        Send only, used at ``._change_voice_state``
    VOICE_PING : `int` = `5`
        Removed.
    RESUME : `int` = `6`
        Send only, used at ``._resume``.
    RECONNECT : `int` = `7`
        Receive only, used at ``._special_operation``.
    REQUEST_MEMBERS : `int` = `8`
        Send only, used at ``Client._request_members_loop``, ``Client._request_members`` and at
        ``Client.request_member``.
    INVALIDATE_SESSION : `int` = `9`
        Receive only, used at ``._special_operation``.
    HELLO : `int` = `10`
        Receive only, used at ``._special_operation``.
    HEARTBEAT_ACK : `int` = `11`
        Receive only, used at ``._special_operation``.
    GUILD_SYNC : `int` = `12`
        Send only, not used.
    """
    __slots__ = ('_buffer', '_decompressor', 'client', 'kokoro', 'rate_limit_handler', 'sequence', 'session_id',
        'shard_id', 'websocket')
    
    DISPATCH           = 0
    HEARTBEAT          = 1
    IDENTIFY           = 2
    PRESENCE           = 3
    VOICE_STATE        = 4
    VOICE_PING         = 5
    RESUME             = 6
    RECONNECT          = 7
    REQUEST_MEMBERS    = 8
    INVALIDATE_SESSION = 9
    HELLO              = 10
    HEARTBEAT_ACK      = 11
    GUILD_SYNC         = 12
    
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
                    
                    if code in DiscordGatewayException.CODETABLE:
                        raise DiscordGatewayException(code) from err
                
                if isinstance(err, TimeoutError):
                    continue
                
                if isinstance(err, ConnectionError): #no internet
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
                #websocket got closed so let's just do a regular IDENTIFY connect.
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
            if err.code in (1000, 1006, 4004, 4010, 4011, 4013, 4014, ):
                raise err
            return True
        except zlib.error as err:
            #we need a full reset
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
                    KOKORO)
            
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
        
        if operation == self.HELLO:
            interval = data['heartbeat_interval']/1000.0
            #send a heartbeat immediately
            kokoro.interval = interval
            await kokoro.beat_now()
            return False
        
        if operation == self.HEARTBEAT_ACK:
            kokoro.answered()
            return False
        
        if kokoro.beater is None:
            raise TimeoutError
            
        if operation == self.HEARTBEAT:
            await self._beat()
            return False
        
        if operation == self.RECONNECT:
            await self.terminate()
            return True
        
        if operation == self.INVALIDATE_SESSION:
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
                KOKORO)
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
            latency =  Kokoro.DEFAULT_LATENCY
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
        if activity is ActivityUnknown:
            activity = None
        else:
            if client.is_bot:
                activity = activity.bot_dict()
            else:
                activity = activity.user_dict()
        
        status = client._status.value
        
        data = {
            'op' : self.IDENTIFY,
            'd'  : {
                'token'      : client.token,
                'properties' : {
                    '$os'               : sys.platform,
                    '$browser'          : 'hata',
                    '$device'           : 'hata',
                    '$referrer'         : '',
                    '$referring_domain' : '',
                        },
                'compress'            : True,             # if we support compression, default : False
                'large_threshold'     : LARGE_LIMIT,      # between 50 and 250, default is 50
                'guild_subscriptions' : CACHE_PRESENCE,   # optional, default is `False`
                'intents'             : client.intents,   # Grip & Break down
                'v'                   : 3,
                'presence' : {
                    'status' : status,
                    'game'   : activity,
                    'since'  : 0.0,
                    'afk'    : False,
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
            'op' : self.RESUME,
            'd'  : {
                'seq'        : self.sequence,
                'session_id' : self.session_id,
                'token'      : self.client.token,
                    },
                }
        
        await self.send_as_json(data)

    async def _change_voice_state(self, guild_id, channel_id, self_mute=False, self_deaf=False):
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
        if guild_id == 0:
            guild_id = None
        
        data = {
            'op' : self.VOICE_STATE,
            'd'  : {
                'guild_id'   : guild_id,
                'channel_id' : channel_id,
                'self_mute'  : self_mute,
                'self_deaf'  : self_deaf,
                    },
                }
        await self.send_as_json(data)
    
    async def _beat(self):
        """
        Sends a `VOICE_STATE` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op' : self.HEARTBEAT,
            'd'  : self.sequence,
                }
        await self.send_as_json(data)


class DiscordGatewayVoice:
    """
    The gateway used by ``VoiceClient``-s to communicate with Discord with secure websocket.
    
    Attributes
    ----------
    client : ``VoiceClient``
        The owner voice client of the gateway.
    kokoro : `None` or `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    websocket : `None` or `WSClient`
        The websocket client of the gateway.
    
    Class Attributes
    ----------------
    IDENTIFY : `int` = `0`
        Send only, used at ``._identify``.
    SELECT_PROTOCOL : `int` = `1`
        Send only, used at ``._select_protocol``.
    READY : `int` = `2`
        Receive only, used at ``._initial_connection``.
    HEARTBEAT : `int` = `3`
        Send only, used at ``._beat``.
    SESSION_DESCRIPTION : `int` = `4`
        Receive only, used at ``._received_message``.
    SPEAKING : `int` = `5`
        Send and receive, used at ``._set_speaking`` and at ``._received_message``.
    HEARTBEAT_ACK : `int` = `6`
        Receive only, used at ``._received_message``.
    RESUME : `int` = `7`
        Send only, used at ``._resume``.
    HELLO : `int` = `8`
        Receive only, used at ``._received_message``.
    INVALIDATE_SESSION : `int` = `9`
        Receive only, used at ``._received_message``.
    CLIENT_CONNECT : `int` = `12`
        Receive only, used at ``._received_message``.
    CLIENT_DISCONNECT : `int` = `13`
        Receive only, used at ``._received_message``.
    VIDEO_SESSION_DESCRIPTION : `int` = `14`
        Receive only. Not used.
    VIDEO_SINK : `int` = `15`
        Receive and send, not used.
    """
    __slots__ = ('client', 'kokoro', 'rate_limit_handler', 'websocket')
        
    IDENTIFY            = 0
    SELECT_PROTOCOL     = 1
    READY               = 2
    HEARTBEAT           = 3
    SESSION_DESCRIPTION = 4
    SPEAKING            = 5
    HEARTBEAT_ACK       = 6
    RESUME              = 7
    HELLO               = 8
    INVALIDATE_SESSION  = 9
    CLIENT_CONNECT      = 12
    CLIENT_DISCONNECT   = 13
    VIDEO_SESSION_DESCRIPTION = 14
    VIDEO_SINK          = 15
    
    def __init__(self, voice_client):
        """
        Creates a voice gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``VoiceClient``
            The owner client of the gateway.
        """
        self.websocket = None
        self.client = voice_client
        
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
        else:
            await kokoro.restart()
    
    # connecting, message receive and processing
    
    async def connect(self, resume=False):
        """
        Connects the gateway to Discord. If the connecting was successful, will start it's `.kokoro` as well.
        
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
        """
        kokoro = self.kokoro
        if (kokoro is not None):
            kokoro.terminate()
            del kokoro
        
        websocket = self.websocket
        if (websocket is not None) and (not websocket.closed):
            await websocket.close(4000)
            self.websocket = None
        
        gateway = f'wss://{self.client._endpoint}/?v=4'
        self.websocket = await self.client.client.http.connect_ws(gateway)
        
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = kokoro = await Kokoro(self)
        kokoro.start_beating()
        del kokoro
        
        if resume:
            await self._resume()
        else:
            await self._identify()
    
    async def _poll_event(self):
        """
        Waits to receive a message from Discord, then calls ``._received_message``.
        
        This method is a coroutine.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        ConnectionClosed
            If the websocket is already closed. Can happen when destroying ghost clients.
        """
        websocket = self.websocket
        if websocket is None:
            raise ConnectionClosed(VOICE_CLIENT_DISCONNECT_CLOSE_CODE, None)
        
        message = await websocket.receive()
        await self._received_message(message)
    
    async def _received_message(self, message):
        """
        Processes the message sent by Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `bytes`
            The received message.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        message = from_json(message)
        
        operation = message['op']
        try:
            data = message['d']
        except KeyError:
            data = None
        
        if operation == self.CLIENT_CONNECT:
            user_id = int(data['user_id'])
            try:
                audio_source = data['audio_ssrc']
            except KeyError:
                pass
            else:
                self.client._update_audio_source(user_id, audio_source)
            
            try:
                video_source = data['video_ssrc']
            except KeyError:
                pass
            else:
                self.client._update_video_source(user_id, video_source)
            
            return
        
        if operation == self.SPEAKING:
            user_id = int(data['user_id'])
            audio_source = data['ssrc']
            self.client._update_audio_source(user_id, audio_source)
            return
        
        if operation == self.CLIENT_DISCONNECT:
            user_id = int(data['user_id'])
            self.client._remove_source(user_id)
            return
        
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = await Kokoro(self)
        
        if operation == self.HELLO:
            # sowwy, but we need to ignore these or we will keep getting timeout
            # kokoro.interval=data['heartbeat_interval']/100.
            # send a heartbeat immediately
            await kokoro.beat_now()
            return
        
        if operation == self.HEARTBEAT_ACK:
            kokoro.answered()
            return
        
        if operation == self.SESSION_DESCRIPTION:
            # data['mode'] is same as our default every time?
            self.client._secret_box = SecretBox(bytes(data['secret_key']))
            if kokoro.beater is None: # Discord order bug ?
                kokoro.start_beating()
                await self._beat()
            
            await self._set_speaking(self.client.speaking)
            return
        
        if kokoro.beater is None:
            raise TimeoutError
        
        if operation == self.READY:
            # need to ignore interval
            # kokoro.interval = data['heartbeat_interval']/100.
            await self._initial_connection(data)
            return
        
        if operation == self.INVALIDATE_SESSION:
            await self._identify()
            return
        
        # Ignore VIDEO_SESSION_DESCRIPTION and VIDEO_SINK for now
    
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
            return Kokoro.DEFAULT_LATENCY
        return kokoro.latency
    
    async def terminate(self):
        """
        Terminates the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `4000`.
        
        This method is a coroutine.
        """
        kokoro = self.kokoro
        if kokoro is not None:
            kokoro.terminate()
            
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
        self.rate_limit_handler.cancel()
        
        kokoro = self.kokoro
        if (kokoro is not None):
            self.kokoro = None
            kokoro.cancel()
        
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
        return f'<{self.__class__.__name__} of {self.client}>'
    
    #special operations
    
    async def _identify(self):
        """
        Sends an `IDENTIFY` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        
        data = {
            'op' : self.IDENTIFY,
            'd'  : {
                'server_id'  : str(voice_client.channel.guild.id),
                'user_id'    : str(voice_client.client.id),
                'session_id' : voice_client._session_id,
                'token'      : voice_client._token,
                    },
                }
        await self.send_as_json(data)
    
    async def _resume(self):
        """
        Sends a `RESUME` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        
        data = {
            'op' : self.RESUME,
            'd'  : {
                'token'      : voice_client._token,
                'server_id'  : str(voice_client.channel.guild.id),
                'session_id' : voice_client._session_id,
                    },
                }
        await self.send_as_json(data)
    
    async def _select_protocol(self, ip, port):
        """
        Sends a `SELECT_PROTOCOL` packet to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        ip : `str`
            The received ip of the voice client to use.
        port : `int`
            The received port of the voice client to use.
        """
        data = {
            'op' : self.SELECT_PROTOCOL,
            'd'  : {
                'protocol' : 'udp',
                'data'     : {
                    'address' : ip,
                    'port'    : port,
                    'mode'    : 'xsalsa20_poly1305'
                        },
                    },
                }
        
        await self.send_as_json(data)
    
    async def _beat(self):
        """
        Sends a `HEARTBEAT` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op' : self.HEARTBEAT,
            'd'  : int(time_now()*1000),
                }
        
        await self.send_as_json(data)
    
    async def _initial_connection(self, data):
        """
        Processes the data from `READY` operation and selects protocol with ``._select_protocol``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data from Discord.
        """
        voice_client = self.client
        voice_client._audio_source = data['ssrc']
        voice_client._audio_port = data['port']
        voice_client._endpoint_ip = data['ip']
        packet = bytearray(70)
        packet[0:4] = voice_client._audio_source.to_bytes(4, 'big')
        
        voice_client.send_packet(packet)
        
        protocol = voice_client._protocol
        # Make sure, that the voice client's reader do not wanna read our data away from us.
        protocol.cancel_current_reader()
        received = await protocol.read(70)
        
        # the ip is ascii starting at the 4th byte and ending at the first null
        voice_client._ip = ip = received[4:received.index(0, 4)].decode('ascii')
        voice_client._port = port = int.from_bytes(received[-2:], 'big')
        
        await self._select_protocol(ip, port)
        await self._client_connect()
        
    async def _client_connect(self):
        """
        Sends a `CLIENT_CONNECT` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        data = {
            'op' : self.CLIENT_CONNECT,
            'd'  : {
                'audio_ssrc' : voice_client._audio_source,
                'video_ssrc' : voice_client._video_source,
                'rtx_ssrc'   : 0,
                    }
                }
        
        await self.send_as_json(data)
    
    async def _set_speaking(self, is_speaking):
        """
        Sends a `SPEAKING` packet with given `is_speaking` state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        is_speaking : `bool`
            Whether the voice client should show up as speaking and be able to send voice data or not.
        """
        data = {
            'op' :self.SPEAKING,
            'd'  : {
                'speaking' : is_speaking,
                'delay'    : 0,
                    },
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
        data=to_json(data)
        
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
