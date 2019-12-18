# -*- coding: utf-8 -*-
__all__ = ('VoiceClient', )

import socket as module_socket
from threading import Event, Lock

from .futures import Future, Task, sleep, future_or_timeout
from .py_exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake

from .opus import OpusEncoder
from .player import AudioPlayer, AudioSource, PCM_volume_transformer, PLAYER_DELAY
from .reader import AudioReader
from .gateway import DiscordGatewayVoice, SecretBox

class VoiceClient(object):
    __slots__ = ('_encoder', '_endpoint', '_endpoint_ip', '_freezed',
        '_freezed_resume', '_handshake_complete', '_ip', '_port',
        '_pref_volume', '_secret_box', '_sequence', '_session_id',
        '_set_speaking_task', '_source', '_timestamp', '_token', '_voice_port',
        'call_after', 'channel', 'client', 'connected', 'gateway', 'lock',
        'loop', 'player', 'queue', 'reader', 'socket', 'sources', 'speaking')

    def __new__(cls,client,channel):
        #raise error at __new__
        if SecretBox is None:
            raise RuntimeError('PyNaCl is not loaded')

        if OpusEncoder is None:
            raise RuntimeError('Opus is not loaded')

        self=object.__new__(cls)
        
        self.channel        = channel
        self.gateway        = DiscordGatewayVoice(self)
        self.socket         = None
        self.loop           = client.loop
        self.client         = client
        self.connected      = Event() #this will be used at the AudioPlayer thread
        self.queue          = []
        self.player         = None
        self.call_after     = type(self)._play_next
        self.speaking       = 0
        self.lock           = Lock()
        self.sources        = {}
        self.reader         = None

        self._handshake_complete=Future(client.loop)
        self._encoder       = OpusEncoder()
        self._sequence      = 0
        self._timestamp     = 0
        self._source        = 0
        self._pref_volume   = 1.0
        self._set_speaking_task=None
        self._endpoint      = None
        self._port          = NotImplemented
        self._endpoint_ip   = NotImplemented
        self._secret_box    = None
        self._voice_port    = NotImplemented
        self._ip            = NotImplemented
        self._freezed       = False
        self._freezed_resume= False
        
        client.voice_clients[channel.guild.id]=self
        future=Future(self.loop)
        Task(self._connect(waiter=future),self.loop)
        return future
    
    #properties
    def _get_volume(self):
        return self._pref_volume

    def _set_volume(self,value):
        if value<0.:
            value=0.
        elif value>2.:
            value=2.
        self._pref_volume=value

        player=self.player
        if player is None:
            return

        source=player.source
        if isinstance(source,PCM_volume_transformer):
            source.volume=self._pref_volume

    volume=property(_get_volume,_set_volume)
    del _get_volume,_set_volume

    @property
    def guild(self):
        return self.channel.guild

    @property
    def source(self):
        player=self.player
        if player is None:
            return
        return player.source

    #methods
    async def set_speaking(self,value):
        task=self._set_speaking_task
        if task is not None:
            await task
            
        if self.speaking==value:
            return

        self.speaking=value
        
        task=Task(self.gateway._set_speaking(value),self.loop)
        self._set_speaking_task=task
        try:
            await task
        except ConnectionClosed:
            pass
        self._set_speaking_task=None
    
    def listen(self):
        reader=self.reader
        if reader is None:
            reader=AudioReader(self)
            self.reader=reader
        
        return reader

    async def move_to(self,channel):
        gateway=self.client._gateway_for(self.channel.guild)
        await gateway._change_voice_state(channel.guild.id,channel.id)

    def append(self,source):
        if not isinstance(source,AudioSource):
            raise TypeError(f'Expected {AudioSource.__name__} instance, received {source}')

        if isinstance(source,PCM_volume_transformer):
            source.volume=self._pref_volume

        player=self.player
        if player is None:
            self.player=AudioPlayer(self,source,)
            Task(self.set_speaking(1),self.loop)
            return True

        self.queue.append(source)
        if source.downloaded:
            if player.source.downloaded and player.source.title==source.title:
                player.source.delete=None
            for index in range(len(self.queue)-2,-1,-1):
                element=self.queue[index]
                if element.downloaded and element.title==source.title:
                    element.delete=None

        return False

    def skip(self):
        self.loop.create_task(self._play_next(True))

    def pause(self):
        player=self.player
        if player is None:
            return
        player.resumed.clear()
        Task(self.set_speaking(0),self.loop)

    def resume(self):
        player=self.player
        if player is None:
            return
        player.resumed.set()
        Task(self.set_speaking(1),self.loop)

    def stop(self):
        self.queue.clear()
        
        player=self.player
        if player is not None:
            self.player=None
            player.done=True
            player.resumed.set()
        
        reader=self.reader
        if reader is not None:
            reader.stop()

    def is_connected(self):
        return self.connected.is_set()

    def is_playing(self):
        player=self.player
        if self.player is None:
            return False
        return (player.resumed.is_set() and (not player.done))

    def is_paused(self):
        player=self.player
        if player is None:
            return True
        return not (player.done or player.resumed.is_set())

    #connection related
    
    async def _connect(self,waiter=None):
        await self.gateway.start(self.loop)
        tries=0
        while True:
            if tries==5:
                try:
                    del self.client.voice_clients[self.channel.guild.id]
                except KeyError:
                    pass
                if waiter is not None:
                    waiter.set_exception(TimeoutError())
                return
            
            self._secret_box=None
            
            try:
                await self._start_handshake()
            except TimeoutError:
                tries+=1
                continue

            try:
                task=Task(self.gateway.connect(),self.loop)
                future_or_timeout(task,30.,)
                await task
                self.connected.clear()
                while True:
                    await self.gateway._poll_event()
                    if self._secret_box is not None:
                        break
                self.connected.set()
            except (OSError,TimeoutError,ConnectionError, ConnectionClosed,
                    WebSocketProtocolError, InvalidHandshake,ValueError):
                await sleep(1+(tries<<1),self.loop)
                tries+=1
                await self._terminate_handshake()
                continue

            if waiter is not None:
                waiter.set_result(self)
                waiter=None
            
            tries=0
            while True:
                try:
                    await self.gateway._poll_event()
                except (OSError,TimeoutError,ConnectionClosed,WebSocketProtocolError,) as err:
                    if isinstance(err,ConnectionClosed):
                        if err.code in (1000,1006):
                            await self.disconnect(force=False)
                            return

                    self.connected.clear()
                    await sleep(5.,self.loop)
                    await self._terminate_handshake()
                    break
        
    async def disconnect(self,force=False,terminate=True):
        if not (force or self.connected.is_set()):
            return
        
        if self._freezed:
            self.connected.clear()
            await self.gateway._terminate()
            if terminate:
                await self._terminate_handshake()
    
            socket=self.socket
            if socket is not None:
                socket.close()
                self.socket=None
        
            return
        
        self.queue.clear()
        player=self.player
        if player is not None:
            self.player=None
            player.done=True
            player.resumed.set()
            await sleep(PLAYER_DELAY,self.loop)

        reader=self.reader
        if reader is not None:
            reader.stop()
        
        self.connected.clear()
        
        try:
            del self.client.voice_clients[self.channel.guild.id]
        except KeyError:
            #already disconnected
            return
        
        try:
            await self.gateway.close()
            if terminate:
                await self._terminate_handshake()
        finally:
            socket=self.socket
            if socket is not None:
                socket.close()
                self.socket=None
    
    def _freeze(self):
        if self._freezed:
            return
        
        self._freezed=True
        resume=self.is_playing()
        self._freezed_resume=resume
        if resume:
            self.pause()
    
    def _unfreeze(self):
        if not self._freezed:
            return
        Task(self._unfreeze_task(),self.loop)
        
    async def _unfreeze_task(self):
        if self.connected.is_set():
            await self._kill_ghost(self.client,self.channel)
            await sleep(1.0,self.loop)
            self.client.voice_clients[self.channel.guild.id]=self
        
        self._freezed=False

        self._handshake_complete=Future(self.loop)
        self._sequence      = 0
        self._timestamp     = 0
        self._source        = 0
        
        self._set_speaking_task=None
        self._endpoint      = None
        self._port          = NotImplemented
        self._endpoint_ip   = NotImplemented
        self._secret_box    = None
        self._voice_port    = NotImplemented
        self._ip            = NotImplemented
        
        future=Future(self.loop)
        Task(self._connect(waiter=future),self.loop)
        
        try:
            await future
        except TimeoutError:
            self.stop()
            try:
                del self.client.voice_clients[self.channel.guild.id]
            except KeyError:
                pass
            return
        
        if self._freezed_resume:
            await sleep(.6,self.loop)
            self.resume()

    @classmethod
    async def _kill_ghost(cls,client,channel):
        try:
            voice_client = await cls(client,channel)
        except RuntimeError:
            return
        except TimeoutError:
            return
        
        await voice_client.disconnect(force=True)
        
    async def _play_next(self,lock):
        player=self.player
        if lock:
            if self.lock.locked():
                return (player is not None)
            
            with self.lock:
                if player is None:
                    if self.queue:
                        source=self.queue.pop(0)
                        self.player=AudioPlayer(self,source)
                        if self.connected.is_set():
                            Task(self.set_speaking(1),self.loop)
                    
                    return False

                if self.queue:
                    player.resumed.clear()
                    source=player.source
                    if source is not None:
                        await sleep(PLAYER_DELAY,self.loop)
                        source.cleanup()
                    source=self.queue.pop(0)
                    player.source=source
                    player.resumed.set()
                    if self.connected.is_set():
                        Task(self.set_speaking(1),self.loop)
                    return False
                
                player.done=True
                player.resumed.set()
                if self.connected.is_set():
                    Task(self.set_speaking(0),self.loop)
                return True

        if self.queue:
            source=self.queue.pop(0)
            player.source=source
            player.resumed.set()
            if self.connected.is_set():
                Task(self.set_speaking(1),self.loop)
            return False
        
        self.player=None
        if self.connected.is_set():
            Task(self.set_speaking(0),self.loop)
        return True

    async def _start_handshake(self):
        client=self.client
        gateway=client._gateway_for(self.channel.guild)

        # request joining
        channel=self.channel
        await gateway._change_voice_state(channel.guild.id,channel.id)
        future_or_timeout(self._handshake_complete,60.0)
        
        try:
            await self._handshake_complete
        except TimeoutError as err:
            try:
                del self.client.voice_clients[channel.guild.id]
            except KeyError:
                pass
            await self._terminate_handshake()
            raise err

    async def _terminate_handshake(self):
        self._handshake_complete.clear()
        gateway=self.client._gateway_for(self.channel.guild)
        try:
            await gateway._change_voice_state(self.channel.guild.id,None,self_mute=True)
        except ConnectionClosed:
            pass
        
        kokoro=self.gateway.kokoro
        if kokoro is None:
            return
        kokoro.terminate()

    async def _create_socket(self,data):
        self.connected.clear()
        gateway=self.client._gateway_for(self.channel.guild)
        self._session_id=gateway.session_id
        token=data.get('token',None)
        self._token=token
        endpoint=data.get('endpoint',None)

        if (endpoint is None) or (token is None):
            return

        self._endpoint=endpoint.replace(':80','')

        socket=self.socket
        if socket is not None:
            socket.close()

        socket=module_socket.socket(module_socket.AF_INET,module_socket.SOCK_DGRAM)
        socket.setblocking(False)
        self.socket=socket

        handshake_complete=self._handshake_complete
        if handshake_complete.done():
            #terminate the websocket and handle the reconnect loop if necessary.
            handshake_complete.clear()
            await self.gateway.close(4000)
        else:
            handshake_complete.set_result(None)

    def __del__(self):
        self.stop()
        self.connected.set()
        
        socket=self.socket
        if socket is None:
            return
        socket.close()
        self.socket=None
        
    def __repr__(self):
        channel=self.channel
        guild=channel.guild
        if guild is None:
            guild_name='Unknown'
            guild_id=0
        else:
            guild_name=guild.name
            guild_id=guild.id
            
        return f'<{self.__class__.__name__} client={self.client.full_name}, channel=\'{channel.name}\', guild=\'{guild_name}\' ({guild_id})>'

from . import guild
guild.VoiceClient=VoiceClient
del guild
