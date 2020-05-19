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

from ..backend.futures import sleep, Task, future_or_timeout, WaitTillExc, WaitTillFirst, WaitTillAll, Future
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
        kokoro=self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self)
            return

        await kokoro.restart()
    
    async def run(self):
        client=self.client
        while True:
            try:
                task=Task(self._connect(),KOKORO)
                future_or_timeout(task,30.,)
                await task
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
    
    async def _connect(self,resume=False):
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
        
    async def _received_message(self,message):
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

    async def _special_operation(self,operation,data):
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
            await self._terminate()
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
        kokoro=self.kokoro
        if kokoro is None:
            return Kokoro.DEFAULT_LATENCY
        return kokoro.latency
    
    async def send_as_json(self,data):
        websocket=self.websocket
        if websocket is None:
            return
        
        if await self.ratelimit_handler:
            return
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed:
            pass
    
    async def close(self, code=1000):
        self.kokoro.cancel()
        self.ratelimit_handler.cancel()
        
        websocket=self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(code)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} client={self.client.full_name}, shard_id={self.shard_id}>'
    
    #special operations
    
    async def _identify(self):
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
        data = {
            'op': self.RESUME,
            'd' : {
                'seq'       : self.sequence,
                'session_id': self.session_id,
                'token'     : self.client.token,
                    },
                }
        
        await self.send_as_json(data)

    async def _change_voice_state(self,guild_id,channel_id,self_mute=False,self_deaf=False):
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
        data = {
            'op': self.HEARTBEAT,
            'd' : self.sequence,
                }
        await self.send_as_json(data)

    async def _terminate(self):
        self.kokoro.terminate()
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(4000)
        
class DiscordGatewayVoice(object):
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
        self.websocket  = None
        self.client     = voice_client
        
        self.kokoro     = None
        self.ratelimit_handler = GatewayRateLimiter()
    
    async def start(self):
        kokoro=self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self)
            return
        
        await kokoro.restart()
    
    #connecting, message receive and processing
    
    async def connect(self,resume=False):
        self.kokoro.terminate()
        if self.websocket is not None and not self.websocket.closed:
            await self.websocket.close(4000)
        gateway=f'wss://{self.client._endpoint}/?v=4'
        self.websocket = await self.client.client.http.connect_ws(gateway)
        self.kokoro.start_beating()
        
        if resume:
            await self._resume()
        else:
            await self._identify()

    async def send_as_json(self,data):
        websocket=self.websocket
        if websocket is None:
            return
        
        if await self.ratelimit_handler:
            return
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed:
            pass

    async def _poll_event(self):
        message = await self.websocket.recv()
        await self._received_message(message)
    
    async def _received_message(self,message):
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
        kokoro=self.kokoro
        if kokoro is None:
            return Kokoro.DEFAULT_LATENCY
        return kokoro.latency
    
    async def close(self, code=1000):
        self.ratelimit_handler.cancel()
        
        kokoro = self.kokoro
        if (kokoro is not None):
            self.kokoro = None
            kokoro.cancel()
        
        websocket=self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(code)

    def __repr__(self):
        return f'<{self.__class__.__name__} of {self.client}>'
    
    #special operations

    async def _identify(self):
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
    
    async def _select_protocol(self,ip,port):
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
        data = {
            'op': self.HEARTBEAT,
            'd' : int(time_now()*1000),
                }
        
        await self.send_as_json(data)

    async def _initial_connection(self,data):
        voice_client=self.client
        voice_client._source=data['ssrc']
        voice_client._voice_port=data['port']
        voice_client._endpoint_ip=data['ip']
        
        packet=bytearray(70)
        packet[0:4]=voice_client._source.to_bytes(4,'big')
        voice_client.socket.sendto(packet,(voice_client._endpoint_ip,voice_client._voice_port))
        received = await KOKORO.sock_recv(voice_client.socket,70)
        # the ip is ascii starting at the 4th byte and ending at the first null
        voice_client._ip=received[4:received.index(0,4)].decode('ascii')
        voice_client._port=int.from_bytes(received[-2:],'big')
        
        await self._select_protocol(voice_client._ip,voice_client._port)
        
    async def _send_silente_packet(self):
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

    async def _set_speaking(self,is_speaking):
        data = {
            'op':self.SPEAKING,
            'd' : {
                'speaking'  : is_speaking,
                'delay'     : 0,
                    },
                }
        
        await self.send_as_json(data)
    
    async def _terminate(self,):
        kokoro=self.kokoro
        if kokoro is not None:
            kokoro.terminate()
            
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(4000)
    
class DiscordGatewaySharder(object):
    __slots__=('client', 'gateways',)
    
    def __init__(self,client):
        self.client     = client
        
        gateways        = []
        for shard_id in range(client.shard_count):
            gateway=DiscordGateway(client,shard_id)
            gateways.append(gateway)
        
        self.gateways   = gateways

    async def start(self):
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.start(), KOKORO)
            tasks.append(task)
        
        await WaitTillExc(tasks, KOKORO)
        
        for task in tasks:
            task.cancel()
        
    async def run(self):
        tasks=[]
        
        for gateway in self.gateways:
            task=Task(gateway.run(), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillFirst(tasks, KOKORO)
        
        for task in tasks:
            task.cancel()
        
        while done:
            if done.pop().result():
                no_internet_stop=True
                break
        else:
            no_internet_stop = False
        
        if no_internet_stop:
            for gateway in self.gateways:
                websocket=gateway.websocket
                if websocket is None:
                    continue
                Task(gateway.close(),KOKORO)
        
        return no_internet_stop
    
    @property
    def latency(self):
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
    
    async def send_as_json(self,data):
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
    
    async def _send_json(gateway, data):
        websocket = gateway.websocket
        if websocket is None:
            return
        
        if await gateway.ratelimit_handler:
            return
        
        try:
            await websocket.send(data)
        except ConnectionClosed:
            pass
    
    async def close(self, code=1000):
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.close(code), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} client={self.client.full_name}, shard_count={self.client.shard_count}>'

