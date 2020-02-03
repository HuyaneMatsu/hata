# -*- coding: utf-8 -*-
import sys
import zlib
from time import time as time_now

try:
    import nacl.secret
except ImportError:
    SecretBox=None
else:
    SecretBox=nacl.secret.SecretBox
    del nacl
    
from .py_websocket import WSClient
from .futures import sleep, Task, future_or_timeout, WaitTillExc, WaitTillFirst, WaitTillAll
from .others import to_json,from_json
from .activity import ActivityUnknown
from .py_exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake
from .parsers import PARSERS
from .guild import LARGE_LIMIT
from .client_core import CACHE_PRESENCE, Kokoro
from .opus import SAMPLES_PER_FRAME


class DiscordGateway(object):
    __slots__=('_buffer', '_decompresser', 'client', 'kokoro', 'loop',
        'sequence', 'session_id', 'shard_id', 'websocket')
    
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

    def __init__(self,client,shard_id=0):
        self.client         = client
        self.shard_id       = shard_id
        self.websocket      = None
        self._buffer        = bytearray()
        self._decompresser  = None
        self.kokoro         = None
        self.loop           = None
        self.sequence       = None
        self.session_id     = None
    
    async def start(self,loop):
        self.loop=loop
        kokoro=self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self,loop)
            return

        await kokoro.restart()

    async def run(self):
        loop=self.loop
        client=self.client
        while True:
            try:
                task=Task(self._connect(),loop)
                future_or_timeout(task,30.,)
                await task
                while True:
                    if (await self._poll_event()):
                        task=Task(self._connect(resume=True,),loop)
                        future_or_timeout(task,30.)
                        await task

            except (OSError, TimeoutError, ConnectionError, ConnectionClosed,
                    WebSocketProtocolError, InvalidHandshake, ValueError) as err:
                
                if not client.running:
                    return False

                #u can extract and exception from here too:
                #if isinstance(err,exc.ConnectionClosed) and err.exception is not None:
                
                if isinstance(err,ConnectionClosed) and err.code in (1000,1006):
                    continue
                
                if isinstance(err,TimeoutError):
                    continue
                
                if isinstance(err,ConnectionError): #no internet
                    return True

                await sleep(1.,self.loop)
    
    #connecting, message receive and processing
    
    async def _connect(self,resume=False):
        while True:
            self.kokoro.terminate()
            websocket=self.websocket
            if websocket is not None and not websocket.closed:
                await websocket.close()
                self.websocket=None
            
            self._decompresser=zlib.decompressobj()
            gateway = await self.client.client_gateway()
            self.websocket = await WSClient(self.loop,gateway,)
            self.kokoro.start_beating()
        
            if not resume:
                await self._identify()
                self.loop.call_later(.2,self.client._unfreeze_voice_for,self,)
                return

            await self._resume()
            
            try:
                await self.websocket.ensure_open()
            except ConnectionClosed:
                #websocket got closed so let's just do a regular IDENTIFY connect.
                self.session_id=None
                self.sequence=None
                continue
            
            self.loop.call_later(.2,self.client._unfreeze_voice_for,self,)
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
            if err.code in (1000,1006,4004,4010,4011):
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
            Task(client.events.error(client,event,err),client.loop)
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
            for voice_client in self.client.voice_clients.values():
                voice_client._freeze()
            await self._terminate()
            return True

        if operation==self.INVALIDATE_SESSION:
            if data:
                await sleep(5.,self.client.loop)
                await self.close()
                return True
            
            self.session_id=None
            self.sequence=None
            
            await self._identify()
            return False
        
        client=self.client
        Task(client.events.error(client,'DiscordWebsocket._special_operation',f'Unknown operation {operation}\nData: {data!r}'),client.loop)
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
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed as err:
            pass
        
    async def close(self,*args,**kwargs):
        self.kokoro.cancel()
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(*args,**kwargs)
    
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
        
        status=client.settings.status.value
        
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
                'compress'              : True,             #if we support compression, default : True
                'large_threshold'       : LARGE_LIMIT,      #between 50 and 250, default is 50
                'guild_subscriptions'   : CACHE_PRESENCE,   #optional, default is `True`
                #'intents'               : client.intents,
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

    async def _terminate(self,*args,**kwargs):
        self.kokoro.terminate()
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(*args,**kwargs)
        
class DiscordGatewayVoice(object):
    __slots__ = ('client', 'kokoro', 'loop', 'websocket')
        
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

    def __init__(self,voice_client):
        self.websocket  = None
        self.client     = voice_client
        self.kokoro     = None
        self.loop       = None
    
    async def start(self,loop):
        self.loop=loop
        kokoro=self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self,loop)
            return

        await kokoro.restart()
    
    #connecting, message receive and processing
    
    async def connect(self,resume=False):
        self.kokoro.terminate()
        if self.websocket is not None and not self.websocket.closed:
            await self.websocket.close()
        gateway=f'wss://{self.client._endpoint}/?v=4'
        self.websocket = await WSClient(self.loop,gateway)
        self.kokoro.start_beating()
        
        if resume:
            await self._resume()
        else:
            await self._identify()

    async def send_as_json(self,data):
        websocket=self.websocket
        if websocket is None:
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
    
    async def close(self,*args,**kwargs):
        kokoro=self.kokoro
        if kokoro is not None:
            kokoro.cancel()
            self.kokoro=None
        
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(*args,**kwargs)

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
        received = await voice_client.loop.sock_recv(voice_client.socket,70)
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
                
                await sleep(0.02,voice_client.loop)
        
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
    
    async def _terminate(self,*args,**kwargs):
        kokoro=self.kokoro
        if kokoro is not None:
            kokoro.terminate()
            
        websocket=self.websocket
        if websocket is None:
            return
        self.websocket=None
        await websocket.close(*args,**kwargs)
    
class DiscordGatewaySharder(object):
    __slots__=('client', 'loop', 'gateways',)
    
    def __init__(self,client):
        self.client     = client
        self.loop       = None
        
        gateways        = []
        for shard_id in range(client.shard_count):
            gateway=DiscordGateway(client,shard_id)
            gateways.append(gateway)
        
        self.gateways   = gateways

    async def start(self,loop):
        self.loop=loop
        tasks=[]
        for gateway in self.gateways:
            task=Task(gateway.start(loop),loop)
            tasks.append(task)
        
        await WaitTillExc(tasks,loop)
        
        for task in tasks:
            task.cancel()
        
    async def run(self):
        tasks=[]
        loop=self.loop
        
        for gateway in self.gateways:
            task=Task(gateway.run(),loop)
            tasks.append(task)
        
        done, pending = await WaitTillFirst(tasks,loop)

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
                loop=self.loop
                Task(gateway.close(),loop)
        
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
        websockets=[]
        for gateway in self.gateways:
            websocket=gateway.websocket
            if websocket is None:
                continue
            websockets.append(websocket)
        
        if not websockets:
            return
        
        data=to_json(data)
        
        tasks=[]
        loop=self.loop
        for websocket in websockets:
            task=Task(websocket.send(data),loop)
            tasks.append(task)
        
        done, pending = await WaitTillExc(tasks,loop)
        
        for task in pending:
            task.cancel()
        
        for task in done:
            task.result()
        
    async def close(self,*args,**kwargs):
        tasks=[]
        loop=self.loop
        for gateway in self.gateways:
            task=Task(gateway.close(*args,**kwargs),loop)
            tasks.append(task)
            
        await WaitTillAll(tasks,loop)

    def __repr__(self):
        return f'<{self.__class__.__name__} client={self.client.full_name}, shard_count={self.client.shard_count}>'

