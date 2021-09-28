__all__ = ('VoiceClient', )

import socket as module_socket
from datetime import datetime

from ...backend.utils import DOCS_ENABLED
from ...backend.futures import Future, Task, sleep, future_or_timeout, Lock, Event
from ...backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake
from ...backend.protocol import DatagramMergerReadProtocol
from ...backend.export import export

from ..core import KOKORO, GUILDS
from ..gateway.voice_client_gateway import DiscordGatewayVoice, SecretBox
from ..channel import ChannelVoiceBase, ChannelStage
from ..exceptions import VOICE_CLIENT_DISCONNECT_CLOSE_CODE, VOICE_CLIENT_RECONNECT_CLOSE_CODE
from ..user import User
from ..utils import datetime_to_timestamp

from .audio_source import AudioSource
from .opus import OpusEncoder
from .player import AudioPlayer
from .reader import AudioReader, AudioStream

@export
class VoiceClient:
    """
    Represents a client what is joined to a voice channel.
    
    Attributes
    ----------
    _audio_port : `int`
        The port, where the voice client should send the audio data.
    _audio_source : `int`
        An identifier sent by Discord what should be sent back with every voice packet.
    _audio_sources : `dict` of (`int`, `int`) items
        `user_id` - `audio_source` mapping used by ``AudioStream``-s.
    _audio_streams : `None` or `dict` of (`int`, (``AudioStream`` or (`list` of ``AudioStream``)) items
        `user_id` - ``AudioStream``(s) mapping for linking ``AudioStream`` to their respective user.
    _encoder : ``OpusEncoder``
        Encode not opus encoded audio data.
    _endpoint : `None` or `str`
        The endpoint, where the voice client sends the audio data.
    _endpoint_ip : `None` or `tuple` of `int`
        The ip version of the `._endpoint` attribute.
    _handshake_complete : ``Future``
        Used for awaiting the connecting handshake with Discord.
    _ip : `None` or `tuple` of `int`
        The ip to what the voice client's gateway connects.
    _port : `None` or `int`
        The port to what the voice client's gateway connects.
    _pref_volume : `float`
        The preferred volume of the voice client. can be between `0.0` and `2.0`.
    _protocol : `None` or ``DatagramMergerReadProtocol``
        Asynchronous protocol of the voice client to communicate with it's socket.
    _reconnecting : `bool`
        Whether the voice client plans to reconnect and it's reader and player should not be stopped.
    _secret_box : `None` or `nacl.secret.SecretBox`
        Data encoder of the voice client.
    _sequence : `int`
        Counter to define the sent data's sequence for Discord.
    _session_id : `None` or `str`
        The session id of the voice client's owner client's shard.
    _set_speaking_task : `None` or ``Task``
        Synchronization task for the `.set_speaking` coroutine.
    _socket : `None` or `socket.socket`
        The socket through what the ``VoiceClient`` sends the voice data to Discord. Created by the ``._create_socket``
        method, when the client's gateway receives response after connecting. If the client leaves the voice channel,
        then the socket is closed and set back to `None`.
    _timestamp : `int`
        A timestamp identifier to tell Discord how much frames we sent to it.
    _token : `str`
        Token received by the voice client's owner client's gateway. Used to authorize the voice client.
    _transport : `None` or ``_SelectorDatagramTransport``
        Asynchronous transport of the voice client to communicate with it's socket.
    _video_source : `int`
        An identifier sent by Discord what should be sent back with every video packet.
    _video_sources : `dict` of (`int`, `int`) items
        `user_id` - `video_source` mapping. Not used for now.
    call_after : `callable` (`awaitable`)
        A coroutine function what is awaited, when the voice clients's current audio finishes playing. By default
        this attribute is set to the ``._play_next`` function of the voice client (plays the next audio at the voice
        clients's ``.queue`` as expected.
        
        This attribute of the client can be modified freely. To it `2` parameters are passed:
         +------------------+---------------------------+
         | Respective name  | Type                      |
         +==================+===========================+
         | client           | ``VoiceClient``           |
         +------------------+---------------------------+
         | last_source      | `None` or ``AudioSource`` |
         +------------------+---------------------------+
         
         The ``VoiceClient`` also includes some other predefined function for setting as `call_after`:
         - ``._play_next``
         - ``._loop_actual``
         - ``._loop_queue``
     
    channel : ``ChannelVoiceBase``
        The channel where the voice client currently is.
    client : ``Client``
        The voice client's owner client.
    connected : ``Event``
        Used to communicate with the ``AudioPlayer`` thread.
    gateway : ``DiscordGatewayVoice``
        The gateway through what the voice client communicates with Discord.
    guild : ``Guild```
        The guild where the voice client is.
    lock : `Lock`
        A lock used meanwhile changing the currently playing audio to not modifying it parallelly.
    player : ``AudioPlayer``
        The actual player of the ``VoiceClient``. If the voice client is not playing nor paused, then set as `None`.
    queue : `list` of ``AudioSource`` instances
        A list of the scheduled audios.
    reader : `None` or ``AudioReader``
        Meanwhile the received audio is collected, this attribute is set to a running ``AudioReader`` instance.
    region : ``VoiceRegion``
        The actual voice region of the voice client.
    speaking : `int`
        Whether the client is showed by Discord as `speaking`, then this attribute should is set as `1`. Can be
        modified, with the ``.set_speaking``, however it is always adjusted to the voice client's current playing state.
    """
    __slots__ = ('_audio_port', '_audio_source', '_audio_sources', '_audio_streams', '_encoder', '_endpoint',
        '_endpoint_ip', '_handshake_complete', '_ip', '_port', '_pref_volume', '_protocol', '_reconnecting',
        '_secret_box', '_sequence', '_session_id', '_set_speaking_task', '_socket', '_timestamp', '_token',
        '_transport', '_video_source', '_video_sources', 'call_after', 'channel', 'client', 'connected', 'gateway',
        'guild', 'lock', 'player', 'queue', 'reader', 'region', 'speaking',)
    
    def __new__(cls, client, channel):
        """
        Creates a ``VoiceClient`` instance. If any of the required libraries are not present, raises `RuntimeError`.
        
        If the voice client was successfully created, returns a ``Future``, what is a waiter for it's ``._connect``
        method. If connecting failed, then the future will raise `TimeoutError`.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        channel : ``ChannelVoiceBase``
            The channel where the client will connect to.
        
        Returns
        -------
        waiter : ``Future``
        
        Raises
        ------
        RuntimeError
            If `PyNaCl` is not loaded.
            If `Opus` is not loaded.
            If `channel` was given as a partial guild channel.
        TypeError
            When channel was not given as ``ChannelVoice`` instance.
        """
        # raise error at __new__
        if SecretBox is None:
            raise RuntimeError('PyNaCl is not loaded.')
        
        if OpusEncoder is None:
            raise RuntimeError('Opus is not loaded.')
        
        if isinstance(channel, ChannelVoiceBase):
            guild_id = channel.guild_id
            if guild_id == 0:
                guild = None
            else:
                guild = GUILDS.get(guild_id)
            
            if guild is None:
                raise RuntimeError(f'Cannot connect to partial channel: {channel!r}.')
        else:
            raise TypeError(f'`channel` can only be {ChannelVoiceBase.__name__}, got {channel.__class__.__name__}.')
        
        region = channel.region
        if region is None:
            region = guild.region
        
        self = object.__new__(cls)
        
        self.guild = guild
        self.channel = channel
        self.region = region
        self.gateway = DiscordGatewayVoice(self)
        self._socket = None
        self._protocol = None
        self._transport = None
        self.client = client
        self.connected = Event(KOKORO)
        self.queue = []
        self.player = None
        self.call_after = cls._play_next
        self.speaking = 0
        self.lock = Lock(KOKORO)
        self.reader = None
        
        self._handshake_complete = Future(KOKORO)
        self._encoder = OpusEncoder()
        self._sequence = 0
        self._timestamp = 0
        self._audio_source = 0
        self._video_source = 0
        self._pref_volume = 1.0
        self._set_speaking_task = None
        self._endpoint = None
        self._port = None
        self._endpoint_ip = None
        self._secret_box = None
        self._audio_port = None
        self._ip = None
        self._audio_sources = {}
        self._video_sources = {}
        self._audio_streams = None
        self._reconnecting = True
        
        client.voice_clients[guild.id] = self
        waiter = Future(KOKORO)
        Task(self._connect(waiter=waiter), KOKORO)
        return waiter
    
    # properties
    def _get_volume(self):
        return self._pref_volume
    
    def _set_volume(self, value):
        if value < 0.:
            value = 0.
        elif value > 2.:
            value = 2.
        
        self._pref_volume = value
    
    volume = property(_get_volume,_set_volume)
    del _get_volume,_set_volume
    if DOCS_ENABLED:
        volume.__doc__ = (
        """
        Get-set property for accessing the voice client's volume.
        
        Can be between `0.0` and `2.0`.
        """)
    
    @property
    def source(self):
        """
        Returns the voice client's player's source if applicable.
        
        Returns
        -------
        source : `None` or ``AudioSource`` instance
        """
        player = self.player
        if player is None:
            return
        
        return player.source
    
    # methods
    async def set_speaking(self, value):
        """
        A coroutine, what is used when changing the ``.speaking`` state of the voice client. By default when audio is
        played, the speaking state is changed to `True` and meanwhile not, then to `False`.
        
        This method is a coroutine.
        
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
            
        if self.speaking == value:
            return

        self.speaking = value
        
        task = Task(self.gateway._set_speaking(value), KOKORO)
        self._set_speaking_task = task
        
        try:
            await task
        finally:
            self._set_speaking_task = None
    
    def listen_to(self, user, **kwargs):
        """
        Creates an audio stream for the given user.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's voice will be captured.
        **kwargs : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        auto_decode : `bool`
            Whether the received packets should be auto decoded.
        yield_decoded : `bool`
            Whether the audio stream should yield encoded data.
        
        Returns
        -------
        audio_stream : ``AudioStream``
        """
        stream = AudioStream(self, user, **kwargs)
        self._link_audio_stream(stream)
        return stream
    
    def _link_audio_stream(self, stream):
        """
        Links the given ``AudioStream`` to self causing to start receiving audio.
        
        Parameters
        ----------
        stream : ``AudioStream``
        """
        voice_client_audio_streams = self._audio_streams
        if voice_client_audio_streams is None:
            voice_client_audio_streams = self._audio_streams = {}
        
        user_id = stream.user.id
        try:
            voice_client_actual_stream = voice_client_audio_streams[user_id]
        except KeyError:
            voice_client_audio_streams[user_id] = stream
        else:
            if type(voice_client_actual_stream) is list:
                voice_client_actual_stream.append(stream)
            else:
                voice_client_audio_streams[user_id] = [voice_client_actual_stream, stream]
        
        source = stream.source
        if (source is not None):
            reader = self.reader
            if reader is None:
                reader = self.reader = AudioReader(self)
            
            reader_audio_streams = reader.audio_streams
            try:
                reader_actual_stream = reader_audio_streams[source]
            except KeyError:
                reader_audio_streams[source] = stream
            else:
                if type(reader_actual_stream) is list:
                    reader_actual_stream.append(stream)
                else:
                    reader_audio_streams[source] = [reader_actual_stream, stream]
    
    def _unlink_audio_stream(self, audio_stream):
        """
        Un-links the given audio stream from the voice client causing it to stop receiving audio.
        
        Parameters
        ----------
        audio_stream : ``AudioStream``
        """
        voice_client_audio_streams = self._audio_streams
        if (voice_client_audio_streams is not None):
            user_id = audio_stream.user.id
            try:
                voice_client_actual_stream = voice_client_audio_streams[user_id]
            except KeyError:
                pass
            else:
                if type(voice_client_actual_stream) is list:
                    try:
                        voice_client_actual_stream.remove(audio_stream)
                    except ValueError:
                        pass
                    else:
                        if len(voice_client_actual_stream) == 1:
                            voice_client_audio_streams[user_id] = voice_client_actual_stream[0]
                else:
                    if voice_client_actual_stream is audio_stream:
                        del voice_client_audio_streams[user_id]
        
        reader = self.reader
        if (reader is not None):
            source = audio_stream.source
            if (source is not None):
                reader_audio_streams = reader.audio_streams
                try:
                    reader_actual_stream = reader_audio_streams[source]
                except KeyError:
                    pass
                else:
                    if type(reader_actual_stream) is list:
                        try:
                            reader_actual_stream.remove(audio_stream)
                        except ValueError:
                            pass
                        else:
                            if len(reader_actual_stream) == 1:
                                reader_audio_streams[source] = reader_actual_stream[0]
                    else:
                        if reader_actual_stream is audio_stream:
                            del reader_audio_streams[source]
    
    def _remove_source(self, user_id):
        """
        Un-links the audio and video streams's source listening to the given user (id), causing the affected audio
        str-eam(s) to stop receiving audio data at the meanwhile.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        """
        voice_sources = self._audio_sources
        try:
            voice_source = voice_sources.pop(user_id)
        except KeyError:
            pass
        else:
            audio_streams = self._audio_streams
            if (audio_streams is not None):
                try:
                    audio_streams[user_id]
                except KeyError:
                    pass
                else:
                    reader = self.reader
                    if (reader is not None):
                        try:
                            del reader.audio_streams[voice_source]
                        except KeyError:
                            pass
        
        try:
            del self._video_sources[user_id]
        except KeyError:
            pass
    
    def _update_audio_source(self, user_id, audio_source):
        """
        Updates (or adds) an `user-id` - `audio-source` relation to the voice client causing the affected audio
        streams to listen to their new source.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        audio_source : `int`
            Audio source identifier of the user.
        """
        voice_sources = self._audio_sources
        try:
            old_audio_source = voice_sources.pop(user_id)
        except KeyError:
            # Should not happen if it is an update, only if it is an add
            pass
        else:
            # Should happen if it is an update
            if audio_source == old_audio_source:
                # Should double happen if it is an update
                return
            
            reader = self.reader
            if (reader is not None):
                reader_audio_streams = reader.audio_streams
                try:
                    del reader_audio_streams[old_audio_source]
                except KeyError:
                    pass
        
        voice_sources[user_id] = audio_source
        
        streams = self._audio_streams
        if streams is None:
            return
        
        try:
            voice_client_actual_stream = streams[user_id]
        except KeyError:
            return
        
        # Link source
        if type(voice_client_actual_stream) is list:
            for stream in voice_client_actual_stream:
                stream.source = audio_source
        else:
            voice_client_actual_stream.source = audio_source
        
        # Add the sources to reader
        reader = self.reader
        if reader is None:
            reader = self.reader = AudioReader(self)
        
        reader_audio_streams = reader.audio_streams
        try:
            reader_actual_stream = reader_audio_streams[audio_source]
        except KeyError:
            # This should happen
            if type(voice_client_actual_stream) is list:
                reader_new_stream = voice_client_actual_stream.copy()
            else:
                reader_new_stream = voice_client_actual_stream
            reader_audio_streams[audio_source] = reader_new_stream
        else:
            # Should not happen
            if type(reader_actual_stream) is list:
                if type(voice_client_actual_stream) is list:
                    reader_actual_stream.extend(voice_client_actual_stream)
                else:
                    reader_actual_stream.append(voice_client_actual_stream)
            else:
                reader_new_stream = [reader_actual_stream]
                if type(voice_client_actual_stream) is list:
                    reader_new_stream.extend(voice_client_actual_stream)
                else:
                    reader_new_stream.append(voice_client_actual_stream)
                
                reader_audio_streams[audio_source] = reader_new_stream
    
    def _update_video_source(self, user_id, video_source):
        """
        Updates (or adds) an `user-id` - `video-source` relation to the voice client.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        video_source : `int`
            Video source identifier of the user.
        """
        self._video_sources[user_id] = video_source
    
    def get_audio_streams(self):
        """
        Returns the audio streams of the voice client within a `list`.
        
        Returns
        -------
        streams : `list` of `tuple` (``ClientUserBase``, ``AudioStream``)
            Audio streams as a `list` of `tuples` of their respective listened `user` and `stream`.
        """
        streams = []
        voice_client_audio_streams = self._audio_streams
        if (voice_client_audio_streams is not None):
            for user_id, stream in voice_client_audio_streams.items():
                user = User.precreate(user_id)
                if type(stream) is list:
                    for stream in stream:
                        streams.append((user, stream))
                else:
                    streams.append((user, stream))
        
        return streams
    
    @property
    def voice_state(self):
        """
        Returns the voice state of the client.
        
        Returns
        -------
        voice_state : `None` or ``VoiceState``
        """
        guild = self.guild
        if (guild is not None):
            return guild.voice_states.get(self.client.id, None)
    
    
    async def move_to(self, channel):
        """
        Move the voice client to an another ``ChannelVoiceBase``.
        
        This method is a coroutine.
        
        Parameters
        ---------
        channel : ``ChannelVoiceBase``
            The channel where the voice client will move to.
        
        Raises
        ------
        TypeError
            If  `channel` was not given as ``ChannelVoice`` instance.
        RuntimeError
            - If `channel` is partial.
            - If the ``VoiceClient`` would be moved between guilds.
        """
        if not isinstance(channel, ChannelVoiceBase):
            raise TypeError(f'Can join only to {ChannelVoiceBase.__name__}, got {channel.__class__.__name__}.')
        
        if self.channel is channel:
            return
        
        guild = channel.guild
        if guild is None:
            raise RuntimeError(f'Cannot connect to partial channel: {channel!r}.')
        
        own_guild = self.guild
        if (own_guild is not guild):
            raise RuntimeError('Cannot move to an another guild.')
        
        gateway = self.client.gateway_for(own_guild.id)
        await gateway.change_voice_state(own_guild.id, channel.id)
    
    
    async def join_speakers(self, *, request=False):
        """
        Requests to speak at the voice client's voice channel. Only applicable for stage channels.
        
        This method is a coroutine.
        
        Parameters
        ----------
        request : `bool`, Optional (Keyword only)
            Whether the client should only request to speak.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild = self.guild
        if guild is None:
            return
        
        channel = self.channel
        if not isinstance(channel, ChannelStage):
            return
        
        try:
            voice_state = guild.voice_states[self.client.id]
        except KeyError:
            return
        
        if voice_state.is_speaker:
            return
        
        if request:
            timestamp = datetime_to_timestamp(datetime.now())
        else:
            timestamp = None
        
        data = {
            'suppress': False,
            'request_to_speak_timestamp': timestamp,
            'channel_id': channel.id
        }
        
        await self.client.http.voice_state_client_edit(guild.id, data)
    
    
    async def join_audience(self):
        """
        Joins the audience in the voice client's voice chanel. Only applicable for stage channels.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild = self.guild
        if guild is None:
            return
        
        channel = self.channel
        if not isinstance(channel, ChannelStage):
            return
        
        try:
            voice_state = guild.voice_states[self.client.id]
        except KeyError:
            return
        
        if not voice_state.is_speaker:
            return
        
        data = {
            'suppress': True,
            'channel_id': channel.id
        }
        
        await self.client.http.voice_state_client_edit(guild.id, data)
        return
    
    def append(self, source):
        """
        Starts playing the given audio source. If the voice client is already playing, puts it on it's queue instead.
        
        Parameters
        ---------
        source : ``AudioSource`` instance
            The audio source to put on the queue.
        
        Returns
        -------
        on_queue : `bool`
            Whether the source was put on the voice client's queue or be used up as the player's source initially.
        """
        source_type = source.__class__
        if not issubclass(source_type, AudioSource):
            raise TypeError(f'Expected {AudioSource.__name__} instance, received {source_type.__name__}.')
        
        player = self.player
        if player is None:
            self.player = AudioPlayer(self, source,)
            Task(self.set_speaking(1), KOKORO)
            return True
        
        queue = self.queue
        if queue or (player.source is not None):
            queue.append(source)
            return False
        
        player.set_source(source)
        Task(self.set_speaking(1), KOKORO)
        return True
    
    
    def skip(self, index=0):
        """
        Skips the currently played audio at the given index and returns it.
        
        Skipping nothing yields to returning `None`.
        
        Parameters
        ----------
        index : `int`
            The index of the audio to skip. Defaults to `0`, what causes the currently playing source to skipped.
        
        Returns
        -------
        source : `None` or ``AudioSource`` instance
        """
        if index == 0:
            player = self.player
            if player is None:
                source = None
            else:
                source = player.source
            
            # Try playing next even if player is `None`.
            Task(self.play_next(), KOKORO)
        
        elif index < 0:
            source = None
        else:
            queue = self.queue
            if index > len(queue):
                source = None
            else:
                source = queue.pop(index-1)
        
        return source
    
    def pause(self):
        """
        Pauses the currently played audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.pause()
            Task(self.set_speaking(0), KOKORO)
    
    def resume(self):
        """
        Resumes the currently stopped audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.resume()
            Task(self.set_speaking(1), KOKORO)
    
    def stop(self):
        """
        Stops the currently playing audio and clears the audio queue.
        """
        self.queue.clear()
        
        player = self.player
        if (player is not None):
            self.player = None
            player.stop()
    
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
        
        if player.done:
            return False
        
        if not player.resumed_waiter.is_set():
            return False
        
        return True
    
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
        
        if player.done:
            return True
        
        if not player.resumed_waiter.is_set():
            return True
        
        return False
    
    # connection related
    
    async def _connect(self, waiter=None):
        """
        Connects the voice client to Discord and keeps receiving the gateway events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        waiter : `None` or ``Future``, Optional
            A Waiter what's result is set (or is raised to), when the voice client connects (or failed to connect).
        """
        try:
            await self.gateway.start()
            tries = 0
            while True:
                if tries == 5:
                    if (waiter is not None):
                        waiter.set_exception(TimeoutError())
                    return
                
                self._secret_box = None
                
                try:
                    await self._start_handshake()
                except TimeoutError:
                    tries += 1
                    continue
                except:
                    await self._disconnect(force=True)
                    raise
                
                try:
                    task = Task(self.gateway.connect(), KOKORO)
                    future_or_timeout(task, 30.,)
                    await task
                    
                    self.connected.clear()
                    while True:
                        task = Task(self.gateway._poll_event(), KOKORO)
                        future_or_timeout(task, 60.)
                        await task
                        
                        if self._secret_box is not None:
                            break
                        
                    self.connected.set()
                
                except (OSError, TimeoutError, ConnectionError, ConnectionClosed, WebSocketProtocolError,
                        InvalidHandshake, ValueError) as err:
                    self._maybe_close_socket()
                    
                    if isinstance(err, ConnectionClosed) and (err.code == VOICE_CLIENT_DISCONNECT_CLOSE_CODE):
                        # If we are getting disconnected and voice region changed, then Discord disconnects us, not
                        # user nor us, so reconnect.
                        if not self._maybe_change_voice_region():
                            self._reconnecting = False
                            await self._disconnect(force=False)
                            return
                    
                    if not (isinstance(err, ConnectionClosed) and (err.code == VOICE_CLIENT_RECONNECT_CLOSE_CODE)):
                        await sleep(1+(tries<<1), KOKORO)
                    
                    self._maybe_change_voice_region()
                    
                    tries += 1
                    await self._terminate_handshake()
                    continue
                
                except:
                    await self._disconnect(force=True)
                    raise
                
                if (waiter is not None):
                    waiter.set_result(self)
                    waiter = None
                
                tries = 0
                while True:
                    try:
                        task = Task(self.gateway._poll_event(), KOKORO)
                        future_or_timeout(task, 60.)
                        await task
                    except (OSError, TimeoutError, ConnectionClosed, WebSocketProtocolError,) as err:
                        self._maybe_close_socket()
                        
                        if isinstance(err, ConnectionClosed):
                            # If we are getting disconnected and voice region changed, then Discord disconnects us, not
                            # user nor us, so reconnect.
                            code = err.code
                            if code == 1000 or (
                                     (code == VOICE_CLIENT_DISCONNECT_CLOSE_CODE) and
                                     (not self._maybe_change_voice_region())
                                        ):
                                self._reconnecting = False
                                await self._disconnect(force=False)
                                return
                        
                        self.connected.clear()
                        
                        if not (isinstance(err, ConnectionClosed) and (err.code == VOICE_CLIENT_RECONNECT_CLOSE_CODE)):
                            await sleep(5., KOKORO)
                        
                        self._maybe_change_voice_region()
                        
                        await self._terminate_handshake()
                        break
                    
                    except:
                        self._reconnecting = False
                        await self._disconnect(force=True)
                        raise
        finally:
            self._reconnecting = False
            
            try:
                del self.client.voice_clients[self.guild.id]
            except KeyError:
                pass
    
    
    async def disconnect(self):
        """
        Disconnects the voice client.
        
        This method is a coroutine.
        """
        await self._disconnect()
    
    
    async def _disconnect(self, force=False, terminate=True):
        """
        Disconnects the voice client.
        
        If you want to disconnect a voice client, then you should use ``.disconnect``. Passing bad parameters to this
        method the can cause misbehaviour.
        
        This method is a coroutine.
        
        Parameters
        ----------
        force : `bool`, Optional
            Whether the voice client should disconnect only if it is not connected (for example when it is connecting).
        terminate : `bool`, Optional
           Whether it is an internal disconnect. If the Disconnect comes from Discord's side, then `terminate` is
           `False`, what means, we do not need to terminate the gateway handshake.
        """
        if not (force or self.connected.is_set()):
            return
        
        self.queue.clear()
        
        if not self._reconnecting:
            player = self.player
            if (player is not None):
                self.player = None
                player.stop()
                
                # skip 1 full loop
                waiter = Future(KOKORO)
                KOKORO.call_later(0.0, Future.set_result_if_pending, waiter, None)
                await waiter
            
            reader = self.reader
            if (reader is not None):
                self.reader = None
                reader.stop()
        
        self.connected.clear()
        
        try:
            await self.gateway.close()
            if terminate:
                await self._terminate_handshake()
        finally:
            self._maybe_close_socket()
    
    
    @classmethod
    async def _kill_ghost(cls, client, voice_state):
        """
        When a client is restarted, it might happen that it will be in still in some voice channels. At this
        case this function is ensured to kill the ghost connection.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the ghost connection.
        voice_state : ``VoiceState``
            The ghost voice client's voice state.
        """
        try:
            voice_client = await cls(client, voice_state.channel)
        except (RuntimeError, TimeoutError):
            return
        
        await voice_client._disconnect(force=True)
    
    
    async def play_next(self):
        """
        Skips the currently playing audio.
        
        Familiar to `.skip`, but it return when the operation id done.
        
        This method is a coroutine.
        """
        async with self.lock:
            await self._play_next(self, None)
    
    
    @staticmethod
    async def _play_next(self, last_source):
        """
        Starts to play the next audio object on ``.queue`` and cancels the actual one if applicable.

        Should be used inside of ``.lock`` to ensure that the voice client is not modified parallelly.
        
        This function is a coroutine.
        
        Parameters
        ----------
        self : ``VoiceClient``
            The respective voice client.
        last_source : `None` or ``AudioSource`` instance
            The audio what was played.
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
            player.set_source(None)
            if self.connected.is_set():
                Task(self.set_speaking(0), KOKORO)
            return
        
        source = queue.pop(0)
        player.set_source(source)
        if self.connected.is_set():
            Task(self.set_speaking(1), KOKORO)
    
    
    @staticmethod
    async def _loop_actual(self, last_source):
        """
        Repeats the last played audio if applicable.
        
        Should be used inside of ``.lock``to ensure that the voice client is not modified parallelly.
        
        This function is a coroutine.
        
        Parameters
        ----------
        self : ``VoiceClient``
            The respective voice client.
        last_source : `None` or ``AudioSource`` instance
            The audio what was played.
        """
        if (last_source is None) or (not last_source.REPEATABLE):
            await self._play_next(self, None)
            return
        
        player = self.player
        if player is None:
            # Should not happen, lol
            self.player = AudioPlayer(self, last_source)
        else:
            # The audio was over.
            player.set_source(last_source)
        
        if self.connected.is_set():
            Task(self.set_speaking(1), KOKORO)
    
    
    @staticmethod
    async def _loop_queue(self, last_source):
        """
        Puts the last played audio back on the voice client's queue.
        
        Should be used inside of ``.lock``to ensure that the voice client is not modified parallelly.
        
        This function is a coroutine.
        
        Parameters
        ----------
        self : ``VoiceClient``
            The respective voice client.
        last_source : `None` or ``AudioSource`` instance
            The audio what was played.
        """
        if (last_source is not None) and last_source.REPEATABLE:
            # The last source was not skipped an we can repeat it.
            self.queue.append(last_source)
        
        await self._play_next(self, None)
    
    
    async def _start_handshake(self):
        """
        Requests a gateway handshake from Discord. If we get answer on it, means, we can open the socket to send audio
        data.
        
        This method is a coroutine.
        
        Raises
        ------
        TimeoutError
            We did not receive answer in time.
        """
        client = self.client
        
        guild = self.guild
        if guild is None:
            guild_id = 0
        else:
            guild_id = guild.id
        gateway = client.gateway_for(guild_id)
        
        # request joining
        await gateway.change_voice_state(guild_id, self.channel.id)
        future_or_timeout(self._handshake_complete, 60.0)
        
        try:
            await self._handshake_complete
        except TimeoutError:
            await self._terminate_handshake()
            raise
    
    
    async def _terminate_handshake(self):
        """
        Called when connecting to Discord fails. Ensures, that everything is aborted correctly.
        
        This method is a coroutine.
        """
        self._handshake_complete.clear()
        
        guild = self.guild
        if guild is None:
            guild_id = 0
        else:
            guild_id = guild.id
        gateway = self.client.gateway_for(guild_id)
        
        try:
            await gateway.change_voice_state(guild_id, 0, self_mute=True)
        except ConnectionClosed:
            pass
        
        kokoro = self.gateway.kokoro
        if (kokoro is not None):
            kokoro.terminate()
    
    
    async def _create_socket(self, event):
        """
        Called when voice server update data is received from Discord.
        
        If full data was received, closes the actual socket if exists and creates a new one connected to the received
        address.
        
        If the voice client is already connected reconnects it, if not then marks it as connected.
        
        This method is a coroutine.
        
        Parameters
        ----------
        event : ``VoiceServerUpdateEvent``
            Voice server update event.
        """
        self.connected.clear()
        
        guild = self.guild
        if guild is None:
            guild_id = 0
        else:
            guild_id = guild.id
        gateway = self.client.gateway_for(guild_id)
        
        self._session_id = gateway.session_id
        token = event.token
        self._token = token
        endpoint = event.endpoint
        
        if (endpoint is None) or (token is None):
            return
        
        self._endpoint = endpoint.replace(':80', '').replace(':443', '')
        
        self._maybe_close_socket()
        
        socket = module_socket.socket(module_socket.AF_INET, module_socket.SOCK_DGRAM)
        
        transport, protocol = await KOKORO.create_datagram_endpoint(DatagramMergerReadProtocol(KOKORO), socket=socket)
        self._transport = transport
        self._protocol = protocol
        self._socket = socket
        
        if self.reader is None:
            self.reader = AudioReader(self)
        
        handshake_complete = self._handshake_complete
        if handshake_complete.done():
            # terminate the websocket and handle the reconnect loop if necessary.
            handshake_complete.clear()
            await self.gateway.terminate()
        else:
            handshake_complete.set_result(None)
    
    
    def send_packet(self, packet):
        """
        Sends the given packet to Discord with the voice client's socket.
        
        Parameters
        ----------
        packet : `bytes-like`
            The packet to send.
        """
        transport = self._transport
        if (transport is not None):
            transport.send_to(packet, (self._endpoint_ip, self._audio_port))
    
    def __del__(self):
        """Stops and unallocates the resources by the voice client, if was not done already."""
        self.stop()
        self.connected.set()
        
        player = self.player
        if (player is not None):
            self.player = None
            player.stop()
        
        reader = self.reader
        if (reader is not None):
            self.reader = None
            reader.stop()
        
        self._maybe_close_socket()
    
    
    def _maybe_close_socket(self):
        """
        Closes the voice client's socket and transport if they are set.
        """
        protocol = self._protocol
        if (protocol is not None):
            self._protocol = None
            self._transport = None
            protocol.close()
        
        socket = self._socket
        if socket is not None:
            self._socket = None
            socket.close()
    
    
    def _maybe_change_voice_region(self):
        """
        Resets the voice region of the voice client.
        
        Returns
        -------
        changed: `bool`
            Whether voice region changed.
        """
        region = self.channel.region
        if region is None:
            region = self.guild.region
        
        if region is self.region:
            return False
        
        self.region = region
        return True
    
    
    def __repr__(self):
        """Returns the voice client's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' client=',
            repr(self.client.full_name),
            ', channel='
        ]
        
        channel = self.channel
        repr_parts.append(repr(channel.name))
        repr_parts.append(' (')
        repr_parts.append(str(channel.id))
        repr_parts.append(')')
        
        guild = self.guild
        repr_parts.append(', guild=')
        repr_parts.append(repr(guild.name))
        repr_parts.append(' (')
        repr_parts.append(repr(guild.id))
        repr_parts.append(')')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
