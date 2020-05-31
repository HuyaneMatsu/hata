# -*- coding: utf-8 -*-
import sys, zlib
from time import time as time_now, monotonic
from collections import deque

try:
    import nacl.secret
except ImportError:
    SecretBox=None
else:
    SecretBox=nacl.secret.SecretBox
    del nacl

from ..backend.futures import sleep, Task, future_or_timeout, WaitTillExc, WaitTillFirst, WaitTillAll, Future, WaitContinously
from ..backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake

from .others import to_json, from_json
from .activity import ActivityUnknown
from .parsers import PARSERS
from .guild import LARGE_LIMIT
from .client_core import CACHE_PRESENCE, Kokoro, KOKORO
from .opus import SAMPLES_PER_FRAME
from .exceptions import IntentError

GATEWAY_RATELIMIT_LIMIT = 120
GATEWAY_RATELIMIT_RESET = 60.0

class GatewayRateLimiter(object):
    """
    Burst ratelimit handler for gateways, what operates on the clients' loop only.
    
    Attributes
    ----------
    queue : `deque` of `Future`
        The queue of the ratelimit handler. It is filled up with futures, if the handler's limit is exhausted.
        These futures are removed and their result is set, when the limit is reset.
    remaining : `int`
        The amount of requests which can be done, before the limit is exhausted.
    resets_at : `float`
        When the ratelimit of the respective gateway will be reset.
    wakeupper : `None`  or `TimerHandle`
        A handler what will reset the limiter's limit and ensure it's queue if nedded.
    """
    __slots__ = ('queue', 'remaining', 'resets_at', 'wakeupper', )
    
    def __init__(self):
        """
        Creates a gateway rate limiter.
        """
        self.remaining = GATEWAY_RATELIMIT_LIMIT
        self.queue = deque()
        self.wakeupper = None
        self.resets_at = 0.0
    
    def __await__(self):
        """
        Awaits the ratelimit handler.
        
        Returns
        -------
        cancelled : `bool`
            Whether the respective gateway was closed.
        """
        now = monotonic()
        if now>=self.resets_at:
            self.resets_at = now+GATEWAY_RATELIMIT_RESET
            remaining = GATEWAY_RATELIMIT_LIMIT
        else:
            remaining = self.remaining
        
        if remaining:
            self.remaining= remaining-1
            return False
        
        if self.wakeupper is None:
            self.wakeupper = KOKORO.call_at(self.resets_at, type(self).wakeup, self)
        
        future = Future(KOKORO)
        self.queue.append(future)
        return (yield from future)
    
    def wakeup(self):
        """
        Wakeups the waiting futures of the ``GatewayRateLimiter``.
        """
        queue = self.queue
        remaining = GATEWAY_RATELIMIT_LIMIT
        if queue:
            while True:
                if not queue:
                    wakeupper = None
                    break
                
                if not remaining:
                    self.resets_at = resets_at = monotonic() + GATEWAY_RATELIMIT_RESET
                    wakeupper = KOKORO.call_at(resets_at + GATEWAY_RATELIMIT_RESET, type(self).wakeup, self)
                    break
                
                queue.popleft().set_result_if_pending(False)
                remaining -=1
        
        else:
            wakeupper = None
        
        self.wakeupper = wakeupper
        self.remaining = remaining
    
    def cancel(self):
        """
        Cancels the ``GatewayRateLimiter``'s queue and it's `.wakeupper` if set.
        """
        queue = self.queue
        while queue:
            queue.popleft().set_result_if_pending(True)
        
        wakeupper = self.wakeupper
        if (wakeupper is not None):
            self.wakeupper = None
            wakeupper.cancel()
    
    def __repr__(self):
        """Returns the gateway ratelimiter's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        resets_at = self.resets_at
        if resets_at <= monotonic():
            remaining = GATEWAY_RATELIMIT_LIMIT
        else:
            result.append(' resets_at=')
            result.append(repr(monotonic()))
            result.append(' (monotnonic),')
            
            remaining = self.remaining
        
        result.append(' remaining=')
        result.append(repr(remaining))
        result.append('>')
        
        return ''.join(result)

class DiscordGateway(object):
    """
    The gateway used by ``Client``-s to communicate with Discord with secure websocket.
    
    Attributes
    ----------
    _buffer : `bytearray`
        A buffer used to store not finished received payloads.
    _decompresser : `zlib.Decompress`
        Zlib decompressor used to decompress the received data.
    client : ``Client``
        The owner client of the gateway.
    kokoro : `None` or `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    ratelimit_handler : ``GatewayRateLimiter``
        The ratelimit handler of the gateway.
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
    __slots__ = ('_buffer', '_decompresser', 'client', 'kokoro', 'ratelimit_handler', 'sequence', 'session_id',
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
        self.client         = client
        self.shard_id       = shard_id
        self.websocket      = None
        self._buffer        = bytearray()
        self._decompresser  = None
        self.sequence       = None
        self.session_id     = None
        
        self.kokoro = None
        self.ratelimit_handler = GatewayRateLimiter()
    
    async def start(self):
        """
        Starts the gateway's `.kokoro`.
        """
        kokoro=self.kokoro
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
        
        Parameters
        -----------
        waiter : `Future`, Optional
            A waiter future what is set, when the gateway finished connecting and started polling events.
        
        Returns
        -------
        no_internet_stop : `bool`
        
        Raises
        ------
        IntentError
            The client tries to connect with bad or not acceptable intent values.
        """
        client=self.client
        while True:
            try:
                task=Task(self._connect(),KOKORO)
                future_or_timeout(task,30.,)
                await task
                
                if (waiter is not None):
                    waiter.set_result(None)
                    waiter = None
                
                while True:
                    if (await self._poll_event()):
                        task=Task(self._connect(resume=True,),KOKORO)
                        future_or_timeout(task,30.)
                        await task
            
            except (OSError, TimeoutError, ConnectionError, ConnectionClosed,
                    WebSocketProtocolError, InvalidHandshake, ValueError) as err:
                if not client.running:
                    return False
                
                if isinstance(err,ConnectionClosed):
                    code = err.code
                    if code in (1000,1006):
                        continue
                    
                    if code in (4013, 4014):
                        raise IntentError(code) from err
                
                if isinstance(err,TimeoutError):
                    continue
                
                if isinstance(err,ConnectionError): #no internet
                    return True
                
                await sleep(1.,KOKORO)
    
    #connecting, message receive and processing
    
    async def _connect(self, resume=False):
        """
        Connects the gateway to Discord. If the connecting was successfull will start it's `.kokoro` as well.
        
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
        while True:
            self.kokoro.terminate()
            websocket=self.websocket
            if (websocket is not None) and (not websocket.closed):
                await websocket.close(4000)
                self.websocket=None
            
            self._decompresser=zlib.decompressobj()
            gateway = await self.client.client_gateway()
            self.websocket = await self.client.http.connect_ws(gateway)
            self.kokoro.start_beating()
            
            if not resume:
                await self._identify()
                KOKORO.call_later(.2,self.client._unfreeze_voice_for,self,)
                return
            
            await self._resume()
            
            try:
                await self.websocket.ensure_open()
            except ConnectionClosed:
                #websocket got closed so let's just do a regular IDENTIFY connect.
                self.session_id=None
                self.sequence=None
                continue
            
            KOKORO.call_later(.2,self.client._unfreeze_voice_for,self,)
            return

    #w8s for the next event
    async def _poll_event(self):
        """
        Waits for sockets from Discord till it collected a full one. If it did, decompresses and processes it.
        Returns `True`, if the gateway should reconnect.
        
        Returns
        -------
        should_reconnect : `bool`
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        websocket=self.websocket
        if websocket is None:
            return True
        
        buffer=self._buffer
        try:
            while True:
                message=await websocket.recv()
                if len(message)>=4 and message[-4:]==b'\x00\x00\xff\xff':
                    if buffer:
                        buffer.extend(message)
                        message=self._decompresser.decompress(buffer).decode('utf-8')
                        buffer.clear()
                    else:
                        message=self._decompresser.decompress(message).decode('utf-8')
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
        message     = from_json(message)

        operation   = message['op']
        data        = message['d']
        sequence    = message['s']

        if sequence is not None:
            self.sequence=sequence
            
        if operation:
            return await self._special_operation(operation,data)
        
        # self.DISPATCH
        event=message['t']
        client=self.client
        try:
            if PARSERS[event](client,data) is None:
                return False
        except BaseException as err:
            Task(client.events.error(client,event,err),KOKORO)
            return False
        
        if event=='READY':
            self.session_id=data['session_id']
        #elif event=='RESUMED':
            #pass

        return False

    async def _special_operation(self, operation, data):
        """
        Handles special operations (so everything except `DISPATCH`). Returns `True` if the gateway should reconnect.
        
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
        kokoro=self.kokoro

        if operation==self.HELLO:
            interval=data['heartbeat_interval']/1000.0
            #send a heartbeat immediately
            kokoro.interval=interval
            await kokoro.beat_now()
            return False

        if operation==self.HEARTBEAT_ACK:
            kokoro.answered()
            return False
        
        if kokoro.beater is None:
            raise TimeoutError
            
        if operation==self.HEARTBEAT:
            await self._beat()
            return False
        
        if operation==self.RECONNECT:
            self.client._freeze_voice_for(self)
            await self.terminate()
            return True
        
        if operation==self.INVALIDATE_SESSION:
            if data:
                await sleep(5.,KOKORO)
                await self.close()
                return True
            
            self.session_id=None
            self.sequence=None
            
            await self._identify()
            return False
        
        client=self.client
        Task(client.events.error(client,f'{self.__clas__.__name__}._special_operation',f'Unknown operation {operation}\nData: {data!r}'),KOKORO)
        return False
        
    #general stuffs
    
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
        """
        self.kokoro.terminate()
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(4000)
    
    async def close(self):
        """
        Cancels the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `1000`.
        """
        self.kokoro.cancel()
        self.ratelimit_handler.cancel()
        
        websocket=self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(1000)
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``. If there is no websocket, or the websocket
        is closed will not raise.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        websocket=self.websocket
        if websocket is None:
            return
        
        if await self.ratelimit_handler:
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
        """
        client=self.client
        activity=client._activity
        if activity is ActivityUnknown:
            activity=None
        else:
            if client.is_bot:
                activity=activity.botdict()
            else:
                activity=activity.hoomandict()
        
        status=client._status.value
        
        data = {
            'op': self.IDENTIFY,
            'd' : {
                'token'     : client.token,
                'properties': {
                    '$os'               : sys.platform,
                    '$browser'          : 'hata',
                    '$device'           : 'hata',
                    '$referrer'         : '',
                    '$referring_domain' : '',
                        },
                'compress'              : True,             # if we support compression, default : False
                'large_threshold'       : LARGE_LIMIT,      # between 50 and 250, default is 50
                'guild_subscriptions'   : CACHE_PRESENCE,   # optional, default is `False`
                'intents'               : client.intents,   # Grip & Break down
                'v'                     : 3,
                'presence' : {
                    'status': status,
                    'game'  : activity,
                    'since' : 0.0,
                    'afk'   : False,
                        },
                    },
                }

        if not client.is_bot:
            data['d']['synced_guilds']=[]
        
        shard_count=client.shard_count
        if shard_count:
            data['d']['shard']=[self.shard_id,shard_count]
        
        await self.send_as_json(data)
        
    async def _resume(self):
        """
        Sends a `RESUME` packet to Discord.
        """
        data = {
            'op': self.RESUME,
            'd' : {
                'seq'       : self.sequence,
                'session_id': self.session_id,
                'token'     : self.client.token,
                    },
                }
        
        await self.send_as_json(data)

    async def _change_voice_state(self, guild_id, channel_id, self_mute=False, self_deaf=False):
        """
        Sends a `VOICE_STATE` packet to Discord.
        
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
        data = {
            'op': self.VOICE_STATE,
            'd' : {
                'guild_id'  : guild_id,
                'channel_id': channel_id,
                'self_mute' : self_mute,
                'self_deaf' : self_deaf,
                    },
                }
        await self.send_as_json(data)
    
    async def _beat(self):
        """
        Sends a `VOICE_STATE` packet to Discord.
        """
        data = {
            'op': self.HEARTBEAT,
            'd' : self.sequence,
                }
        await self.send_as_json(data)


class DiscordGatewayVoice(object):
    """
    The gateway used by ``VoiceClient``-s to communicate with Discord with secure websocket.
    
    Attributes
    ----------
    client : ``VoiceClient``
        The owner voice client of the gateway.
    kokoro : `None` or `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    ratelimit_handler : ``GatewayRateLimiter``
        The ratelimit handler of the gateway.
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
    """
    __slots__ = ('client', 'kokoro', 'ratelimit_handler', 'websocket')
        
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
    
    def __init__(self, voice_client):
        """
        Creates a voice gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``VoiceClient``
            The owner client of the gateway.
        """
        self.websocket  = None
        self.client     = voice_client
        
        self.kokoro     = None
        self.ratelimit_handler = GatewayRateLimiter()
    
    async def start(self):
        """
        Starts the gateway's `.kokoro`.
        """
        kokoro=self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self)
            return
        
        await kokoro.restart()
    
    #connecting, message receive and processing
    
    async def connect(self, resume=False):
        """
        Connects the gateway to Discord. If the connecting was successfull, will start it's `.kokoro` as well.
        
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
        self.kokoro.terminate()
        websocket=self.websocket
        if (websocket is not None) and (not websocket.closed):
            await websocket.close(4000)
            self.websocket=None
        
        gateway=f'wss://{self.client._endpoint}/?v=4'
        self.websocket = await self.client.client.http.connect_ws(gateway)
        self.kokoro.start_beating()
        
        if resume:
            await self._resume()
        else:
            await self._identify()
    
    async def _poll_event(self):
        """
        Waits to receive a message from Discord, then calls ``._received_message``.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        message = await self.websocket.recv()
        await self._received_message(message)
    
    async def _received_message(self, message):
        """
        Processes the message sent by Discord.
        
        Parameters
        ----------
        message : `bytes`
            The received message.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        message=from_json(message)
        
        operation=message['op']
        try:
            data=message['d']
        except KeyError:
            data=None
        
        kokoro=self.kokoro
        
        if operation==self.HELLO:
            #sowwy, but we need to ignore these or we will keep getting timeout
            #kokoro.interval=data['heartbeat_interval']/100.
            #send a heartbeat immediately
            await kokoro.beat_now()
            return
        
        if operation==self.HEARTBEAT_ACK:
            kokoro.answered()
            return
        
        if operation==self.SESSION_DESCRIPTION:
            #data['mode'] is same as our default every time?
            self.client._secret_box=SecretBox(bytes(data['secret_key']))
            if kokoro.beater is None: # Discord order bug ?
                kokoro.start_beating()
                await self._beat()
            
            await self._send_silente_packet()
            return
        
        if kokoro.beater is None:
            raise TimeoutError
        
        if operation==self.READY:
            #need to ignore interval
            #kokoro.interval=data['heartbeat_interval']/100.
            await self._initial_connection(data)
            return
        
        if operation==self.INVALIDATE_SESSION:
            await self._identify()
            return
        
        if operation==self.SPEAKING:
            user_id=int(data['user_id'])
            source=data['ssrc']
            self.client.sources[user_id]=source
            return
        
        if operation==self.CLIENT_CONNECT:
            user_id=int(data['user_id'])
            source=data['audio_ssrc']
            self.client.sources[user_id]=source
            return
        
        if operation==self.CLIENT_DISCONNECT:
            user_id=int(data['user_id'])
            try:
                del self.client.sources[user_id]
            except KeyError:
                pass
            return
    
    # general stuffs
    
    @property
    def latency(self):
        """
        The latency of the websocket in seconds. If no latency is recorded, will return `Kokoro.DEFAULT_LATENCY`.
        
        Returns
        -------
        latency : `float`
        """
        kokoro=self.kokoro
        if kokoro is None:
            return Kokoro.DEFAULT_LATENCY
        return kokoro.latency
    
    async def terminate(self):
        """
        Terminates the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `4000`.
        """
        kokoro=self.kokoro
        if kokoro is not None:
            kokoro.terminate()
            
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(4000)
    
    async def close(self):
        """
        Cancels the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `1000`.
        """
        self.ratelimit_handler.cancel()
        
        kokoro = self.kokoro
        if (kokoro is not None):
            self.kokoro = None
            kokoro.cancel()
        
        websocket=self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(1000)
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``. If there is no websocket, or the websocket
        is closed will not raise.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        websocket=self.websocket
        if websocket is None:
            return
        
        if await self.ratelimit_handler:
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
        """
        voice_client=self.client

        data = {
            'op': self.IDENTIFY,
            'd' : {
                'server_id' : str(voice_client.channel.guild.id),
                'user_id'   : str(voice_client.client.id),
                'session_id': voice_client._session_id,
                'token'     : voice_client._token,
                    },
                }
        await self.send_as_json(data)
    
    async def _resume(self):
        """
        Sends a `RESUME` packet to Discord.
        """
        voice_client=self.client

        data = {
            'op': self.RESUME,
            'd' : {
                'token'     : voice_client._token,
                'server_id' : str(voice_client.channel.guild.id),
                'session_id': voice_client._session_id,
                    },
                }
        await self.send_as_json(data)
    
    async def _select_protocol(self, ip, port):
        """
        Sends a `SELECT_PROTOCOL` packet to Discord.
        
        Parameters
        ----------
        ip : `str`
            The received ip of the voice client to use.
        port : `int`
            The received port of the voice client to use.
        """
        data = {
            'op': self.SELECT_PROTOCOL,
            'd' : {
                'protocol'  : 'udp',
                'data'      : {
                    'address'   : ip,
                    'port'      : port,
                    'mode'      : 'xsalsa20_poly1305'
                        },
                    },
                }
        
        await self.send_as_json(data)
    
    async def _beat(self):
        """
        Sends a `HEARTBEAT` packet to Discord.
        """
        data = {
            'op': self.HEARTBEAT,
            'd' : int(time_now()*1000),
                }
        
        await self.send_as_json(data)
    
    async def _initial_connection(self, data):
        """
        Processes the data from `READY` operation and selects protocol with ``._select_protocol``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data from Discord.
        """
        voice_client=self.client
        voice_client._source=data['ssrc']
        voice_client._voice_port=data['port']
        voice_client._endpoint_ip=data['ip']
        
        packet=bytearray(70)
        packet[0:4]=voice_client._source.to_bytes(4,'big')
        voice_client.socket.sendto(packet,(voice_client._endpoint_ip,voice_client._voice_port))
        received = await KOKORO.sock_recv(voice_client.socket,70)
        # the ip is ascii starting at the 4th byte and ending at the first null
        voice_client._ip = ip = received[4:received.index(0,4)].decode('ascii')
        voice_client._port = port =int.from_bytes(received[-2:],'big')
        
        await self._select_protocol(ip, port)
        
    async def _send_silente_packet(self):
        """
        Sends silence packets to Discord on the gateway's voice client's socket.
        
        Used after connecting.
        """
        await self._set_speaking(1)
        voice_client=self.client
        socket=voice_client.socket
        if socket is not None:
            for x in range(5):
                sequence=voice_client._sequence
                if sequence==65535:
                    sequence=0
                else:
                    sequence=sequence+1
                voice_client._sequence=sequence

                header=b''.join([
                    b'\x80x',
                    voice_client._sequence.to_bytes(2,'big'),
                    voice_client._timestamp.to_bytes(4,'big'),
                    voice_client._source.to_bytes(4,'big'),
                        ])

                nonce=header+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                packet=bytearray(header)+voice_client._secret_box.encrypt(b'\xf8\xff\xfe',nonce).ciphertext

                try:
                    voice_client.socket.sendto(packet,(voice_client._endpoint_ip,voice_client._voice_port))
                except BlockingIOError:
                    pass

                timestamp=voice_client._timestamp+SAMPLES_PER_FRAME
                if timestamp>4294967295:
                    timestamp=0
                voice_client._timestamp=timestamp
                
                await sleep(0.02, KOKORO)
        
        await self._set_speaking(voice_client.speaking)

    async def _set_speaking(self, is_speaking):
        """
        Sends a `SPEAKING` packet with given `is_speaking` state.
        
        Parameters
        ----------
        is_speaking : `bool`
            Whether the voice client should show up as speaking and be able to send voice data or not.
        """
        data = {
            'op':self.SPEAKING,
            'd' : {
                'speaking'  : is_speaking,
                'delay'     : 0,
                    },
                }
        
        await self.send_as_json(data)

class DiscordGatewaySharder(object):
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
            gateway=DiscordGateway(client,shard_id)
            gateways.append(gateway)
        
        self.gateways = gateways
    
    async def start(self):
        """
        Starts the gateways of the sharder gateway.
        """
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.start(), KOKORO)
            tasks.append(task)
        
        await WaitTillExc(tasks, KOKORO)
        
        for task in tasks:
            task.cancel()
    
    async def run(self):
        """
        Runs the gateway sharder's gateways. If any of them returns, stops the rest as well. And if any of them
        returned `True`, then returns `True`, else `False`.
        
        Returns
        -------
        no_internet_stop : `bool`
        """
        max_concurrency = self.client._gateway_max_concurrency
        gateways = self.gateways
        
        index = 0
        limit = len(gateways)
        
        # At every step we add up to max_concurrency gateways to launch up. When a gateway is launched up, the waiter
        # yields a `Future` and if the same amount of `Future` is yielded as gateway started up, then we do the next
        # loop. An exception is, when the waiter yielded a `Task`, because t–en 1 of our gateway stopped with no
        # internet stop, or it was stopped by the client, so we abort all the launching and return.
        waiter = WaitContinously(None, KOKORO)
        while True:
            if index == limit:
                break
            
            left_from_bacth = 0
            while True:
                future = Future(KOKORO)
                waiter.add(future)
                
                task = Task(gateways[index].run(future), KOKORO)
                waiter.add(task)
                
                index +=1
                left_from_bacth +=1
                if index == limit:
                    break
                
                if left_from_bacth == max_concurrency:
                    break
                
                continue
            
            while True:
                result = await waiter
                waiter.reset()
                
                if type(result) is Future:
                    left_from_bacth -=1
                    
                    if left_from_bacth:
                        continue
                    
                    break
                
                no_internet_stop = result.result()
                waiter.cancel()
                return no_internet_stop
            
            continue
        
        result = await waiter
        
        no_internet_stop = result.result()
        waiter.cancel()
        return no_internet_stop
    
    @property
    def latency(self):
        """
        The average latency of the gateways' websockets in seconds. If no latency was recorded, will return
        `Kokoro.DEFAULT_LATENCY`.
        
        Returns
        -------
        latency : `float`
        """
        total=0
        count=0
        for gateway in self.gateways:
            kokoro=gateway.kokoro
            if kokoro is None:
                continue
            total=total+kokoro.latency
            count=count+1
        
        if count:
            return total/count
        
        return Kokoro.DEFAULT_LATENCY
    
    async def terminate(self):
        """
        Terminates the gateway sharder's gateways.
        """
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.terminate(), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    
    async def close(self):
        """
        Cancels the gateway sharder's gateways.
        """
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.close(), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        data=to_json(data)
        
        tasks=[]
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
        """
        websocket = gateway.websocket
        if websocket is None:
            return
        
        if await gateway.ratelimit_handler:
            return
        
        try:
            await websocket.send(data)
        except ConnectionClosed:
            pass
    
    def __repr__(self):
        """Returns the representation of the gateway sharder."""
        return f'<{self.__class__.__name__} client={self.client.full_name}, shard_count={self.client.shard_count}>'
