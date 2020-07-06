# -*- coding: utf-8 -*-
__all__ = ('VoiceClient', )

import socket as module_socket
from threading import Event

from ..backend.futures import Future, Task, sleep, future_or_timeout, Lock
from ..backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake

from .client_core import KOKORO
from .opus import OpusEncoder
from .player import AudioPlayer, AudioSource, PLAYER_DELAY
from .reader import AudioReader
from .gateway import DiscordGatewayVoice, SecretBox
from .channel import ChannelVoice

class VoiceClient(object):
    """
    Represents a client what is joined to a voice channel.
    
    Attributes
    ----------
    _encoder : ``OpusEncoder``
        Encode not opus encoded audio data.
    _endpoint : `None` or `str`
        The endpoint, where the voice client sends the audio data.
    _endpoint_ip : `None` or `tuple` of `int`
        The ip version of the `._endpoint` attribute.
    _freezed : `bool`
        Whether the ``VoiceClient`` is freezed and should be unfreezed when it's respective client gateway reconnects.
    _freezed_resume : `bool`
        Whether the VoiceClient was playin when it was freezed.
    _handshake_complete : `Future`
        Used for awaiting the connecting handshake with Discord.
    _ip : `None` or `tuple` of `int`
        The ip to what the voice client's gateway connects.
    _port : `None` or `int`
        The port to what the voice client's gateway connects.
    _pref_volume : `float`
        The preferred volume of the voice client. can be between `0.0` and `2.0`.
    _secret_box : `None` or `nacl.secret.SecretBox`
        Data encoder of teh voice client.
    _sequence : `int`
        Counter to define the sent data's sequence for Discord.
    _session_id : `None` or `str`
        The session id of the voice client's owner client's shard.
    _set_speaking_task : `None` or `Task`
        Synchronization task for the `.set_speaking` coroutine.
    _source : `int`
        An identificator sent by Discord what should be sent back with every voice packet.
    _timestamp : `int`
        A timestamp identificaotr to tell Discord how much frames we sent to it.
    _token : `str`
        Token received by the voice client's owner client's gateway. Used to authorize the voice client.
    _voice_port : `int`
        The port, where the voice client should send the audio data.
    call_after : `callable` (`awaitable`)
        A coroutine function what is awaited, when the voice clients's current audio finishes playing. By default
        this attribute is set to the ``._play_next`` function of the voice client (plays the next audio at the voice
        clients's ``.queue`` as expected.

        This attribute of the client can be modified freely. To it `1` argument is passed, the respective
        ``VoiceClient`` itself.
    
    channel : ``ChannelVoice``
        The channel where the voice client currently is.
    client : ``Client``
        The voice client's owner client.
    connected : `threading.Event`
        Used to communicate with the ``AudioPlayer`` thread.
    gateway : ``DiscordGatewayVoice``
        The gateway through what the voice client communicates with Discord.
    guild : ``Guild``
        The guild where the voice client is.
    lock : `Lock`
        A lock used meanwile changing the currently playing audio to modifying it pararelly.
    player : ``AudioPlayer``
        The actual player of the ``VoiceClient.md``. If the voice client is not playing nor paused, then set as `None`.
    queue : `list` of ``AudioSource`` instances
        A list of the scheduled audios.
    reader : `None` or ``AudioReader``
        Meanwhile the received audio is collected, this attribute is set to a running ``AudioReader`` instance.
    socket : `None` or `socket.socket`
        The socket through what the ``VoiceClient`` sends the voice data to Discord. Created by the ``._create_socket``
        method, when the client's gateway receives response after connecting. If the client leaves the voice channel,
        then the socket is closed and set back to `None`.
    sources : `dict` of (`int`, `int`) items
        `user_id`, `ssrc` mapping used by `.reader`.
    speaking : `int`
        Whether the client is showed by Discord as `speaking`, then this attribute should is set as `1`. Can be modified, with the
        ``.set_speaking``, however it is always adjusted to the voice client's current playing state.
    """
    __slots__ = ('_encoder', '_endpoint', '_endpoint_ip', '_freezed', '_freezed_resume', '_handshake_complete', '_ip',
        '_port', '_pref_volume', '_secret_box', '_sequence', '_session_id', '_set_speaking_task', '_source',
        '_timestamp', '_token', '_voice_port', 'call_after', 'channel', 'client', 'connected', 'gateway', 'guild',
        'lock', 'player', 'queue', 'reader', 'socket', 'sources', 'speaking', )
    
    def __new__(cls, client, channel):
        """
        Creates a ``VoiceClient`` instance. If any of the required libraries are not present, raises `RuntimeError`.
        
        If the voice client was succesfully created, returns a `Future`, what is a waiter for it's ``._connect``
        method. If connecting failed, then the future will raise `TimeoutError`.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        channel : ``ChannelVoice``
            The channel where the client will connect to.
        
        Returns
        -------
        waiter : `Future`
        
        Raises
        ------
        RuntimeError
            If `PyNaCl` is not loaded.
            If `Opus` is not loaded.
            If `channel` was given as a partial guild channel.
        TypeError
            When channel was not given as ``ChannelVoice`` instance.
        """
        #raise error at __new__
        if SecretBox is None:
            raise RuntimeError('PyNaCl is not loaded.')
        
        if OpusEncoder is None:
            raise RuntimeError('Opus is not loaded.')
        
        channel_type = channel.__class__
        if channel_type is ChannelVoice:
            guild = channel.guild
            if guild is None:
                raise RuntimeError('Cannot connect to partial channel.')
            
        else:
            raise TypeError(f'Can join only to {ChannelVoice.__name__}, got {channel_type.__name__}.')
        
        self = object.__new__(cls)
        
        self.guild          = guild
        self.channel        = channel
        self.gateway        = DiscordGatewayVoice(self)
        self.socket         = None
        self.client         = client
        self.connected      = Event() #this will be used at the AudioPlayer thread
        self.queue          = []
        self.player         = None
        self.call_after     = type(self)._play_next
        self.speaking       = 0
        self.lock           = Lock(KOKORO)
        self.sources        = {}
        self.reader         = None
        
        self._handshake_complete = Future(KOKORO)
        self._encoder       = OpusEncoder()
        self._sequence      = 0
        self._timestamp     = 0
        self._source        = 0
        self._pref_volume   = 1.0
        self._set_speaking_task = None
        self._endpoint      = None
        self._port          = None
        self._endpoint_ip   = None
        self._secret_box    = None
        self._voice_port    = None
        self._ip            = None
        self._freezed       = False
        self._freezed_resume= False
        
        client.voice_clients[guild.id] = self
        waiter = Future(KOKORO)
        Task(self._connect(waiter=waiter), KOKORO)
        return waiter
    
    #properties
    def _get_volume(self):
        return self._pref_volume
    
    def _set_volume(self,value):
        if value<0.:
            value=0.
        elif value>2.:
            value=2.
        
        self._pref_volume=value
    
    volume = property(_get_volume,_set_volume)
    del _get_volume,_set_volume
    if (__new__.__doc__ is not None):
        volume.__doc__ = (
        """
        Get-set proparty for accessing the voice client's volume.
        
        Can be between `0.0` and `2.0`.
        """)
    
    @property
    def source(self):
        """
        Returns the voice client's palyer's source if applicable.
        
        Returns
        -------
        source : `None` or ``AudioSource`` instance
        """
        player = self.player
        if player is None:
            return
        
        return player.source
    
    #methods
    async def set_speaking(self, value):
        """
        A coroutine, what is used when changing the ``.speaking`` state of the voice client. By default when audio is played,
        the speaking state is changed to `True` and meanwhile not, then to `False`.
        
        Parameters
        ----------
        value : `int` (`0`, `1`)
        
        Notes
        -----
        Tinkering with this method is not recommended.
        """
        task = self._set_speaking_task
        if (task is not None):
            await task
            
        if self.speaking==value:
            return

        self.speaking=value
        
        task = Task(self.gateway._set_speaking(value),KOKORO)
        self._set_speaking_task = task
        
        try:
            await task
        finally:
            self._set_speaking_task=None
    
    def listen(self):
        """
        If the client has a ``.reader`` returns that, else created a new one.
        
        Returns
        -------
        reader : ``AudioReader``
        """
        reader = self.reader
        if reader is None:
            self.reader = reader = AudioReader(self)
        
        return reader
    
    async def move_to(self, channel):
        """
        Move the voice client to an another ``ChannelVoice``.
        
        Arguments
        ---------
        channel : ``ChannelVoice``
            The channel where the voice client will move to.
        
        Raises
        ------
        TypeError
            If  `channel` was not given as ``ChannelVoice`` instance.
        RuntimeError
            If the ``VoiceClient`` would be moved between guilds.
        """
        channel_type = channel.__class__
        if (channel_type is not ChannelVoice):
            raise TypeError(f'Can join only to {ChannelVoice.__name__}, got {channel_type.__name__}.')
        
        if self.channel is channel:
            return
        
        own_guild = self.guild
        if (own_guild is not channel.guild):
            raise RuntimeError('Cannot move to an another guild.')
        
        gateway = self.client._gateway_for(own_guild)
        await gateway._change_voice_state(own_guild.id, channel.id)
    
    def append(self, source):
        """
        Starts playing the given audio source. If the voice client is already playing, puts it on it's queue instead.
        
        Arguments
        ---------
        source : ``AudioSource`` instance
            The audio source to put on the queue.
        """
        source_type = source.__class__
        if not issubclass(source_type, AudioSource):
            raise TypeError(f'Expected {AudioSource.__name__} instance, received {source_type.__name__}.')
        
        player = self.player
        if player is None:
            self.player = AudioPlayer(self, source,)
            Task(self.set_speaking(1), KOKORO)
            return True
        
        self.queue.append(source)
        
        return False
    
    def skip(self):
        """
        Skips the currently played audio if applicable.
        """
        KOKORO.create_task(self.play_next())
    
    def pause(self):
        """
        Pauses the currently played audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.resumed.clear()
            Task(self.set_speaking(0), KOKORO)
    
    def resume(self):
        """
        Resumes the currently stopped audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.resumed.set()
            Task(self.set_speaking(1), KOKORO)
    
    def stop(self):
        """
        Stops the currently playing audio and clears the audio queue.
        """
        self.queue.clear()
        
        player = self.player
        if (player is not None):
            self.player=None
            player.done=True
            player.resumed.set()
        
        reader = self.reader
        if (reader is not None):
            reader.stop()
    
    def is_connected(self):
        """
        Returns whether the voice client is connected to a ``ChannelVoice``.
        
        Returns
        -------
        is_connected : `bool`
        """
        return self.connected.is_set()
    
    def is_playing(self):
        """
        Returns whether the voice client is currently playing audio.
        
        Returns
        -------
        is_playing : `bool`
        """
        player = self.player
        if player is None:
            return False
        return (player.resumed.is_set() and (not player.done))
    
    def is_paused(self):
        """
        Returns whether the voice client is currently paused (or not playing).
        
        Returns
        -------
        is_paused : `bool`
        """
        player = self.player
        if player is None:
            return True
        return not (player.done or player.resumed.is_set())
    
    #connection related
    
    async def _connect(self, waiter=None):
        """
        Connects the voice client to Discord and keeps receiveing the gateway events.
        
        Parameters
        ----------
        waiter : `None` or `Future`, Optional
            A Waiter what's result is set (or is raised to), when the voice client connects (or failed to connect).
        """
        await self.gateway.start()
        tries=0
        while True:
            if tries==5:
                try:
                    del self.client.voice_clients[self.guild.id]
                except KeyError:
                    pass
                if (waiter is not None):
                    waiter.set_exception(TimeoutError())
                return
            
            self._secret_box=None
            
            try:
                await self._start_handshake()
            except TimeoutError:
                tries+=1
                continue
            
            try:
                task=Task(self.gateway.connect(),KOKORO)
                future_or_timeout(task,30.,)
                await task
                self.connected.clear()
                while True:
                    await self.gateway._poll_event()
                    if self._secret_box is not None:
                        break
                self.connected.set()
            except (OSError,TimeoutError,ConnectionError, ConnectionClosed, WebSocketProtocolError, InvalidHandshake,
                    ValueError) as err:
                
                if isinstance(err, ConnectionClosed) and (err.code == 4014):
                    await self.disconnect(force=False)
                    return
                
                await sleep(1+(tries<<1),KOKORO)
                tries+=1
                await self._terminate_handshake()
                continue
            
            if (waiter is not None):
                waiter.set_result(self)
                waiter = None
            
            tries=0
            while True:
                try:
                    await self.gateway._poll_event()
                except (OSError, TimeoutError, ConnectionClosed, WebSocketProtocolError,) as err:
                    
                    if isinstance(err, ConnectionClosed) and (err.code in (1000, 1006, 4014)):
                        await self.disconnect(force=False)
                        return
                    
                    self.connected.clear()
                    await sleep(5.,KOKORO)
                    await self._terminate_handshake()
                    break
        
    async def disconnect(self, force=False, terminate=True):
        """
        Disconnects the voice client.
        
        Parameters
        ----------
        force : `bool`, Optional
            Whether the voice client should disconnect only if it is not connected (for example when it is connecting).
        terminate : `bool`, Optional
           Whether it is an internal disconnect. If the Disconnect comes from Discord's side, then `terminate` is
           `False`, what means, we do not need to terminate the gateway handshake.
       
        Notes
        -----
        If you want to disconnecta voice client, then you should let the method to use it's default arguments. Passing
        bad default arguments at cases can cause misbehaviour.
        """
        if not (force or self.connected.is_set()):
            return
        
        if self._freezed:
            self.connected.clear()
            await self.gateway.terminate()
            if terminate:
                await self._terminate_handshake()
    
            socket = self.socket
            if (socket is not None):
                self.socket = None
                socket.close()
                
            return
        
        self.queue.clear()
        player = self.player
        if (player is not None):
            self.player = None
            player.done = True
            player.resumed.set()
            await sleep(PLAYER_DELAY,KOKORO)
        
        reader = self.reader
        if (reader is not None):
            reader.stop()
        
        self.connected.clear()
        
        try:
            del self.client.voice_clients[self.guild.id]
        except KeyError:
            #already disconnected
            return
        
        try:
            await self.gateway.close()
            if terminate:
                await self._terminate_handshake()
        finally:
            socket = self.socket
            if (socket is not None):
                self.socket = None
                socket.close()
    
    def _freeze(self):
        """
        Freezes the voice client and pauses it's player.
        """
        if self._freezed:
            return
        
        self._freezed=True
        resume=self.is_playing()
        self._freezed_resume=resume
        if resume:
            self.pause()
    
    def _unfreeze(self):
        """
        Unfreezes the voice client if needed.
        """
        if not self._freezed:
            return
        Task(self._unfreeze_task(),KOKORO)
        
    async def _unfreeze_task(self):
        """
        This coroutine ensured, when the voice client needs unfreezing.
        """
        if self.connected.is_set():
            await self._kill_ghost(self.client, self.channel)
            await sleep(1.0,KOKORO)
            
            self.client.voice_clients[self.guild.id] = self
        
        self._freezed=False
        
        self._handshake_complete=Future(KOKORO)
        self._sequence      = 0
        self._timestamp     = 0
        self._source        = 0
        
        self._set_speaking_task=None
        self._endpoint      = None
        self._port          = None
        self._endpoint_ip   = None
        self._secret_box    = None
        self._voice_port    = None
        self._ip            = None
        
        future=Future(KOKORO)
        Task(self._connect(waiter=future),KOKORO)
        
        try:
            await future
        except TimeoutError:
            self.stop()
            
            try:
                del self.client.voice_clients[self.guild.id]
            except KeyError:
                pass
            return
        
        if self._freezed_resume:
            await sleep(.6,KOKORO)
            self.resume()
    
    @classmethod
    async def _kill_ghost(cls, client, channel):
        """
        When a client is restarted, it might happen that it will be in still in some voice channels. At this
        case this function is ensured to kill the ghost connection.

        Parameters
        ----------
        client : ``Client``
            The owner client of the ghost connection.
        channel : ``ChannelVoice``
            The channel where the ghost voice client is connected to.
        Returns
        -------

        """
        try:
            voice_client = await cls(client, channel)
        except (RuntimeError, TimeoutError):
            return
        
        await voice_client.disconnect(force=True)
    
    async def play_next(self):
        """
        Skips the currently playing audio.
        
        Familiar to `.skip`, but it return when the operation id done.
        """
        async with self.lock:
            await self._play_next()
    
    async def _play_next(self):
        """
        Starts to play the next audio object on ``.queue`` and cancels the actual one if applicable.

        Should be used inside of ``.lock``to ensure that the voice client is not modified pararelly.
        """
        player = self.player
        queue = self.queue
        if player is None:
            if not queue:
                return
            
            source = queue.pop(0)
            self.player = AudioPlayer(self, source)
            if self.connected.is_set():
                Task(self.set_speaking(1), KOKORO)
            
            return
        
        if not queue:
            player.done = True
            player.resumed.set()
            if self.connected.is_set():
                Task(self.set_speaking(0), KOKORO)
            return
        
        player.resumed.clear()
        source = player.source
        if (source is not None):
            await sleep(PLAYER_DELAY, KOKORO)
            source.cleanup()
        
        source = queue.pop(0)
        player.source = source
        player.resumed.set()
        if self.connected.is_set():
            Task(self.set_speaking(1), KOKORO)
        return
    
    async def _start_handshake(self):
        """
        Requests a gateway handshake from Discord. If we get answer on it, means, we can open the socket to send audio
        data.
        
        Raises
        ------
        TimeoutError
            We did not receive answer in time.
        """
        client = self.client
        guild = self.guild
        gateway=client._gateway_for(guild)

        # request joining
        await gateway._change_voice_state(guild.id, self.channel.id)
        future_or_timeout(self._handshake_complete,60.0)
        
        try:
            await self._handshake_complete
        except TimeoutError as err:
            try:
                del self.client.voice_clients[guild.id]
            except KeyError:
                pass
            await self._terminate_handshake()
            raise err
    
    async def _terminate_handshake(self):
        """
        Called when connecting to Discord fails. Ensures, that everything is aborted correctly.
        """
        self._handshake_complete.clear()
        guild = self.guild
        gateway = self.client._gateway_for(guild)
        
        try:
            await gateway._change_voice_state(guild.id, None, self_mute=True)
        except ConnectionClosed:
            pass
        
        kokoro = self.gateway.kokoro
        if (kokoro is not None):
            kokoro.terminate()
    
    async def _create_socket(self, data):
        """
        Called when voice server update data is received from Discord.
        
        If full data was received, closes the actual socket if exists and creates a new one connected to the received
        adress.
        
        If the voice client is already connected reconnects it, if not then marks it as connected.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice server update data.
        """
        self.connected.clear()
        gateway = self.client._gateway_for(self.guild)
        self._session_id = gateway.session_id
        token = data.get('token',None)
        self._token=token
        endpoint = data.get('endpoint',None)
        
        if (endpoint is None) or (token is None):
            return
        
        self._endpoint = endpoint.replace(':80','')
        
        socket = self.socket
        if socket is not None:
            socket.close()
        
        socket = module_socket.socket(module_socket.AF_INET,module_socket.SOCK_DGRAM)
        socket.setblocking(False)
        self.socket = socket
        
        handshake_complete = self._handshake_complete
        if handshake_complete.done():
            #terminate the websocket and handle the reconnect loop if necessary.
            handshake_complete.clear()
            await self.gateway.terminate()
        else:
            handshake_complete.set_result(None)
    
    def __del__(self):
        """Stops and unallocates the resources by the voice client, if was not done already."""
        self.stop()
        self.connected.set()
        
        socket = self.socket
        if (socket is not None):
            self.socket = None
            socket.close()
    
    def __repr__(self):
        """Returns the voice client's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' client=',
            repr(self.client.full_name),
            ', channel='
                ]
        
        channel = self.channel
        result.append(repr(channel.name))
        result.append(' (')
        result.append(str(channel.id))
        result.append(')')
        
        guild = self.guild
        result.append(', guild=')
        result.append(repr(guild.name))
        result.append(' (')
        result.append(repr(guild.id))
        result.append(')')
        
        result.append('>')
        
        return ''.join(result)

from . import guild
guild.VoiceClient=VoiceClient
del guild
