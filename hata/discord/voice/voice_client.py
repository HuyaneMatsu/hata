__all__ = ('VoiceClient', )

import socket as module_socket
from datetime import datetime as DateTime, timezone as TimeZone
from functools import partial as partial_func

from scarletio import (
    DOCS_ENABLED, DatagramMergerReadProtocol, Future, Lock, Task, export, RichAttributeErrorBaseType, skip_poll_cycle
)
from scarletio.web_common import ConnectionClosed

from ..bases import maybe_snowflake
from ..channel import Channel, ChannelType, create_partial_channel_from_id
from ..core import GUILDS, KOKORO
from ..exceptions import VOICE_CLIENT_DISCONNECT_CLOSE_CODE
from ..gateway.voice import DiscordGatewayVoice
from ..gateway.voice_base import DiscordGatewayVoiceBase
from ..user import User
from ..utils import datetime_to_timestamp

from .audio_source import AudioSource
from .encryption_adapters import AVAILABLE_ENCRYPTION_ADAPTERS, EncryptionAdapterBase
from .opus import OpusEncoder
from .player import AudioPlayer
from .reader import AudioReader, AudioStream
from .utils import try_get_voice_region


ENCRYPTION_ADAPTER_DEFAULT = EncryptionAdapterBase(b'\x00' * EncryptionAdapterBase.key_length)



@export
class VoiceClient(RichAttributeErrorBaseType):
    """
    Represents a client what is joined to a voice channel.
    
    Attributes
    ----------
    _audio_source : `int`
        An identifier sent by Discord what should be sent back with every voice packet.
    _audio_sources : `dict` of (`int`, `int`) items
        `user_id` - `audio_source` mapping used by ``AudioStream``-s.
    _audio_streams : `None`, `dict` of (`int`, (``AudioStream`` or (`list` of ``AudioStream``)) items
        `user_id` - ``AudioStream``(s) mapping for linking ``AudioStream`` to their respective user.
    _connected : `bool`
        Whether the voice client is connected.
    _connected_waiters : `None | set<Future>`
        Waiter futures waiting for the voice client to be connected again.
    _encoder : ``OpusEncoder``
        Encode not opus encoded audio data.
    _encryption_adapter : ``EncryptionAdapterBase``
        Data encoder & decoder of the voice client.
    _encryption_adapter_type : `type<EncryptionAdapterBase>`
        Data encoder & decoder type. Set before ``._encryption_adapter`` is actually instantiated.
    _endpoint : `None`, `str`
        The endpoint, where the voice client sends the audio data.
    _endpoint_ip : `None`, `tuple` of `int`
        The ip version of the `._endpoint` attribute.
    _endpoint_port : `int`
        The port, where the voice client should send the audio data.
    _handshake_complete : ``Future``
        Used for awaiting the connecting handshake with Discord.
    _ip : `None | str`
        The ip to what the voice client's gateway connects.
    _port : `None`, `int`
        The port to what the voice client's gateway connects.
    _preferred_volume : `float`
        The preferred volume of the voice client. can be between `0.0` and `2.0`.
    _protocol : `None`, ``DatagramMergerReadProtocol``
        Asynchronous protocol of the voice client to communicate with it's socket.
    _sequence : `int`
        Counter to define the sent data's sequence for Discord.
    _set_speaking_task : `None`, ``Task``
        Synchronization task for the `.set_speaking` coroutine.
    _socket : `None`, `socket.socket`
        The socket through what the ``VoiceClient`` sends the voice data to Discord. Created by the ``._create_socket``
        method, when the client's gateway receives response after connecting. If the client leaves the voice channel,
        then the socket is closed and set back to `None`.
    _timestamp : `int`
        A timestamp identifier to tell Discord how much frames we sent to it.
    _token : `str`
        Token received by the voice client's owner client's gateway. Used to authorize the voice client.
    _transport : `None`, ``_SelectorDatagramTransport``
        Asynchronous transport of the voice client to communicate with it's socket.
    _video_source : `int`
        An identifier sent by Discord what should be sent back with every video packet.
    _video_sources : `dict` of (`int`, `int`) items
        `user_id` - `video_source` mapping. Not used for now.
    call_after : `callable` (`awaitable`)
        A coroutine function what is awaited, when the voice clients' current audio finishes playing. By default
        this attribute is set to the ``._play_next`` function of the voice client (plays the next audio at the voice
        clients' ``.queue`` as expected.
        
        This attribute of the client can be modified freely. To it `2` parameters are passed:
        
        +------------------+---------------------------+
        | Respective name  | Type                      |
        +==================+===========================+
        | client           | ``VoiceClient``           |
        +------------------+---------------------------+
        | last_source      | `None`, ``AudioSource``   |
        +------------------+---------------------------+
        
        The ``VoiceClient`` also includes some other predefined function for setting as `call_after`:
        - ``._play_next``
        - ``._loop_actual``
        - ``._loop_queue``
    
    channel_id : `int`
        The channel's identifier where the voice client currently is.
    client : ``Client``
        The voice client's owner client.
    gateway : ``DiscordGatewayVoice``
        The gateway through what the voice client communicates with Discord.
    guild_id : `int``
        The guild's identifier where the voice client is.
    lock : `Lock`
        A lock used meanwhile changing the currently playing audio to not modifying it parallelly.
    player : ``AudioPlayer``
        The actual player of the ``VoiceClient``. If the voice client is not playing nor paused, then set as `None`.
    running : `bool`
        Whether the voice client plans to reconnect and it's reader and player should not be stopped.
    queue : `list` of ``AudioSource``
        A list of the scheduled audios.
    reader : `None`, ``AudioReader``
        Meanwhile the received audio is collected, this attribute is set to a running ``AudioReader``.
    region : ``VoiceRegion``
        The actual voice region of the voice client.
    speaking : `int`
        Whether the client is showed by Discord as `speaking`, then this attribute should is set as `1`. Can be
        modified, with the ``.set_speaking``, however it is always adjusted to the voice client's current playing state.
    """
    __slots__ = (
        '_audio_source', '_audio_sources', '_audio_streams', '_connected', '_connected_waiters', '_encoder',
        '_encryption_adapter', '_encryption_adapter_type', '_endpoint', '_endpoint_ip', '_endpoint_port',
        '_handshake_complete', '_ip', '_port', '_preferred_volume', '_protocol', '_sequence', '_set_speaking_task',
        '_socket', '_timestamp', '_token', '_transport', '_video_source', '_video_sources', 'call_after', 'channel_id',
        'client', 'gateway', 'guild_id', 'lock', 'player', 'running', 'queue', 'reader', 'region', 'speaking'
    )
    
    def __new__(cls, client, guild_id, channel_id):
        """
        Creates a voice client. If any of the required dependencies are not present, raises `RuntimeError`.
        
        If the voice client was successfully created, returns a ``Future``, what is a waiter for it's ``._connect``
        method. If connecting failed, then the future will raise `TimeoutError`.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        guild_id : `int`
            the guild's identifier, where the the client will connect to.
        channel_id : `int`
            The channel's identifier where the client will connect to.
        
        Raises
        ------
        RuntimeError
            If `PyNaCl` is not loaded.
            If `Opus` is not loaded.
        """
        # raise error at __new__
        if not AVAILABLE_ENCRYPTION_ADAPTERS :
            raise RuntimeError(
                '`libnacl` either not installed or not available. '
                'It is a package required for encrypting & decrypting voice packets.'
            )
        
        if OpusEncoder is None:
            raise RuntimeError('Opus is not loaded.')
        
        region = try_get_voice_region(guild_id, channel_id)
        
        self = object.__new__(cls)
        
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.region = region
        self.gateway = DiscordGatewayVoiceBase()
        self._socket = None
        self._protocol = None
        self._transport = None
        self.client = client
        self._connected = False
        self._connected_waiters = None
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
        self._preferred_volume = 1.0
        self._set_speaking_task = None
        self._endpoint = None
        self._port = None
        self._endpoint_ip = None
        self._encryption_adapter = ENCRYPTION_ADAPTER_DEFAULT
        self._encryption_adapter_type = EncryptionAdapterBase
        self._endpoint_port = None
        self._ip = None
        self._audio_sources = {}
        self._video_sources = {}
        self._audio_streams = None
        self.running = False
        self._token = ''
        
        self.gateway = DiscordGatewayVoice(self)
        
        client.voice_clients[guild_id] = self
        
        return self
    
    
    def start(self):
        """
        Starts the voice client and returns a waiter than can be awaited to wait for connection.
        
        Returns
        -------
        waiter : `Future<bool>`
        """
        waiter = Future(KOKORO)
        Task(KOKORO, self._run(waiter = waiter))
        return waiter
    
    
    # properties
    def _get_volume(self):
        return self._preferred_volume
    
    
    def _set_volume(self, value):
        if value < 0.:
            value = 0.
        elif value > 2.:
            value = 2.
        
        self._preferred_volume = value
    
    
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
        source : `None`, ``AudioSource``
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
        
        task = Task(KOKORO, self.gateway.set_speaking(value))
        self._set_speaking_task = task
        
        try:
            await task
        finally:
            self._set_speaking_task = None
    
    
    def listen_to(self, user, **keyword_parameters):
        """
        Creates an audio stream for the given user.
        
        Parameters
        ----------
        user : ``UserBase``
            The user, who's voice will be captured.
        **keyword_parameters : Keyword parameters
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
        stream = AudioStream(self, user, **keyword_parameters)
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
    
    
    def _remove_audio_source(self, user_id):
        """
        Un-links the audio streams' source listening to the given user (id), causing the affected audio
        stream(s) to stop receiving audio data at the meanwhile.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        """
        audio_sources = self._audio_sources
        try:
            audio_source = audio_sources.pop(user_id)
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
                            del reader.audio_streams[audio_source]
                        except KeyError:
                            pass
        
        
    def _remove_video_source(self, user_id):
        """
        Un-links a video stream's source.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        """
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
        audio_sources = self._audio_sources
        try:
            old_audio_source = audio_sources.pop(user_id)
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
        
        audio_sources[user_id] = audio_source
        
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
        voice_state : `None`, ``VoiceState``
        """
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            return guild.get_voice_state(self.client.id)
    
    
    async def move_to(self, channel):
        """
        Move the voice client to an another voice channel.
        
        This method is a coroutine.
        
        Parameters
        ---------
        channel : ``Channel``, `int`
            The channel where the voice client will move to.
        
        Returns
        -------
        moved : `bool`
            Returns `False` if the voice client is already in the channel.
        
        Raises
        ------
        TypeError
            If  `channel` was not given as ``Channel`` not `int`.
        """
        while True:
            if isinstance(channel, Channel):
                if channel.is_in_group_guild_connectable() or channel.partial:
                    channel_id = channel.id
                    break
                
            else:
                channel_id = maybe_snowflake(channel)
                if channel_id is not None:
                    break
            
            raise TypeError(
                f'`channel` can be guild connectable channel, `int`, got '
                f'{channel.__class__.__name__}; {channel!r}.'
            )
        
        if self.channel_id == channel_id:
            return False
        
        gateway = self.client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, channel_id)
        return True
    
    
    async def join_speakers(self, *, request = False):
        """
        Requests to speak at the voice client's voice channel. Only applicable for stage channels.
        
        This method is a coroutine.
        
        Parameters
        ----------
        request : `bool` = `False`, Optional (Keyword only)
            Whether the client should only request to speak.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            voice_state = guild.get_voice_state(self.client.id)
            if (voice_state is None) or voice_state.speaker:
                return
        
        if request:
            timestamp = datetime_to_timestamp(DateTime.now(TimeZone.utc))
        else:
            timestamp = None
        
        data = {
            'suppress': False,
            'request_to_speak_timestamp': timestamp,
            'channel_id': self.channel_id
        }
        
        await self.client.api.voice_state_edit_own(guild_id, data)
    
    
    async def join_audience(self):
        """
        Joins the audience in the voice client's voice channel. Only applicable for stage channels.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            voice_state = guild.get_voice_state(self.client.id)
            if (voice_state is None) or not voice_state.speaker:
                return
        
        data = {
            'suppress': True,
            'channel_id': self.channel_id
        }
        
        await self.client.api.voice_state_edit_own(guild_id, data)
   
    
    def append(self, source):
        """
        Starts playing the given audio source. If the voice client is already playing, puts it on it's queue instead.
        
        Parameters
        ---------
        source : ``AudioSource``
            The audio source to put on the queue.
        
        Returns
        -------
        started_playing : `bool`
            Whether the source is started playing and not put on queue.
        """
        if not isinstance(source, AudioSource):
            raise TypeError(
                f'Expected `{AudioSource.__name__}`, got {source.__class__.__name__}; {source!r}.'
            )
        
        player = self.player
        if player is None:
            self.player = AudioPlayer(self, source,)
            Task(KOKORO, self.set_speaking(1))
            return True
        
        queue = self.queue
        if queue or (player.source is not None):
            queue.append(source)
            return False
        
        player.set_source(source)
        Task(KOKORO, self.set_speaking(1))
        return True
    
    
    def skip(self, index = 0):
        """
        Skips the currently played audio at the given index and returns it.
        
        Skipping nothing yields to returning `None`.
        
        Parameters
        ----------
        index : `int` = `0`, Optional
            The index of the audio to skip. Defaults to `0`, what causes the currently playing source to skipped.
        
        Returns
        -------
        source : `None`, ``AudioSource``
        """
        if index == 0:
            player = self.player
            if player is None:
                source = None
            else:
                source = player.source
            
            # Try playing next even if player is not `None`.
            Task(KOKORO, self.play_next())
        
        elif index < 0:
            source = None
        else:
            queue = self.queue
            if index > len(queue):
                source = None
            else:
                source = queue.pop(index - 1)
        
        return source
    
    
    def pause(self):
        """
        Pauses the currently played audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.pause()
            Task(KOKORO, self.set_speaking(0))
    
    
    def resume(self):
        """
        Resumes the currently stopped audio if applicable.
        """
        player = self.player
        if (player is not None):
            player.resume()
            Task(KOKORO, self.set_speaking(1))
    
    
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
        Returns whether the voice client is connected to a ``Channel``.
        
        Returns
        -------
        is_connected : `bool`
        """
        return self._connected
    
    
    def clear_connected(self):
        """
        Sets the voice client's state to be not connected.
        """
        self._connected = False
    
    
    def set_connected(self):
        """
        Sets the voice client's state to be connected.
        """
        self._connected = True
        self._set_connected_waiters(True)
    
    
    def _create_connected_waiter(self):
        """
        Creates a connected state waiter.
        
        Returns
        -------
        connected_waiter : ``Future``
        """
        connected_waiter = Future(KOKORO)
        
        connected_waiters = self._connected_waiters
        if (connected_waiters is None):
            connected_waiters = set()
            self._connected_waiters = connected_waiters
        
        connected_waiters.add(connected_waiter)
        
        return connected_waiter
    
    
    def _remove_connected_waiter(self, connected_waiter):
        """
        Removes the given connected state waiter.
        
        Parameters
        ----------
        connected_waiter : ``Future``
            The connection waiter to remove.
        """
        connected_waiters = self._connected_waiters
        if (connected_waiters is not None):
            try:
                connected_waiters.remove(connected_waiter)
            except ValueError:
                pass
            else:
                if not connected_waiters:
                    self._connected_waiters = None
    
    
    async def wait_connected(self, timeout = None):
        """
        Waits until the voice client is connected.
        
        Parameters
        ----------
        timeout : `None | float`
            Timeout to apply while waiting for connection.
        
        Returns
        -------
        connected : `bool`
            Whether the voice client connected or disconnected before `timeout`.
        
        Raises
        ------
        TimeoutError
            - 
        """
        if self._connected:
            return True
        
        if not self.running:
            return False
        
        connected_waiter = self._create_connected_waiter()
        
        if (timeout is not None):
            connected_waiter.apply_timeout(timeout)
        
        try:
            return (await connected_waiter)
        finally:
            self._remove_connected_waiter(connected_waiter)

    
    def _set_connected_waiters(self, result):
        """
        Sets the connection waiter's result.
        
        Parameters
        ----------
        result : `bool`
            The value to set the waiter's result to.
        """
        connected_waiters = self._connected_waiters
        if (connected_waiters is not None):
            self._connected_waiters = None
            
            while connected_waiters:
                connected_waiters.pop().set_result_if_pending(result)
    
    
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
    
    async def _run(self, waiter = None):
        """
        Connects the voice client to Discord and keeps receiving the gateway events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        waiter : `None`, ``Future`` = `None`, Optional
            A Waiter what's result is set (or is raised to), when the voice client connects (or failed to connect).
        """
        # Are we double started?
        if self.running:
            if (waiter is not None):
                waiter.set_result_if_pending(True)
                waiter = None
            return False
        
        self.running = True
        try:
            while True:
                if not self.running:
                    return False
                
                try:
                    await self._start_handshake()
                except TimeoutError:
                    continue
                
                except GeneratorExit:
                    raise
                
                try:
                    await self.gateway.run(waiter)
                except ConnectionClosed as exception:
                    self._close_socket()
                    
                    if exception.code == VOICE_CLIENT_DISCONNECT_CLOSE_CODE:
                        # If we are getting disconnected and voice region changed, then Discord disconnects us, not
                        # user nor us, so reconnect.
                        if not self._maybe_change_voice_region():
                            self.running = False
                            await self._disconnect(force = False)
                            return False
                    
                    self._maybe_change_voice_region()
                    await self._terminate_handshake()
                    continue
                
                else:
                    break
                
                finally:
                    if (waiter is not None) and waiter.is_done():
                        waiter = None
        
        except GeneratorExit:
            self.running = False
            self._stop_player_and_reader()
            self.gateway.abort()
            raise
        
        except:
            self.running = False
            await self._disconnect(force = True)
            raise
        
        finally:
            if (waiter is not None):
                waiter.set_result_if_pending(False)
                waiter = None
            
            self.running = False
            
            try:
                del self.client.voice_clients[self.guild_id]
            except KeyError:
                pass
            
            self._set_connected_waiters(False)
        
        return False
        
        
    async def disconnect(self):
        """
        Disconnects the voice client.
        
        This method is a coroutine.
        """
        await self._disconnect()
    
    
    async def _disconnect(self, force = False, terminate = True):
        """
        Disconnects the voice client.
        
        If you want to disconnect a voice client, then you should use ``.disconnect``. Passing bad parameters to this
        method the can cause misbehaviour.
        
        This method is a coroutine.
        
        Parameters
        ----------
        force : `bool` = `False`, Optional
            Whether the voice client should disconnect only if it is not connected (for example when it is connecting).
        terminate : `bool` = `True`, Optional
            Whether it is an internal disconnect. If the Disconnect comes from Discord's side, then `terminate` is
            `False`, what means, we do not need to terminate the gateway handshake.
        """
        if not (force or self._connected):
            return
        
        try:
            self.queue.clear()
            
            self._stop_player_and_reader()
                    
            # skip 1 full loop
            await skip_poll_cycle(KOKORO)
            
            self.clear_connected()
            
            await self.gateway.close()
            if terminate:
                await self._terminate_handshake()
        finally:
            self.running = False
            self._close_socket()
            self.gateway.abort()
    
    
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
            voice_client = await cls(client, voice_state.guild_id, voice_state.channel_id)
        except (RuntimeError, TimeoutError):
            return
        
        await voice_client._disconnect(force = True)
    
    
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
        last_source : `None`, ``AudioSource``
            The audio what was played.
        """
        player = self.player
        queue = self.queue
        if player is None:
            if not queue:
                return
            
            source = queue.pop(0)
            self.player = AudioPlayer(self, source)
            if self._connected:
                Task(KOKORO, self.set_speaking(1))
            
            return
        
        if not queue:
            player.set_source(None)
            if self._connected:
                Task(KOKORO, self.set_speaking(0))
            return
        
        source = queue.pop(0)
        player.set_source(source)
        if self._connected:
            Task(KOKORO, self.set_speaking(1))
    
    
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
        last_source : `None`, ``AudioSource``
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
        
        if self._connected:
            Task(KOKORO, self.set_speaking(1))
    
    
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
        last_source : `None`, ``AudioSource``
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
        
        gateway = client.gateway_for(self.guild_id)
        
        # request joining
        await gateway.change_voice_state(self.guild_id, self.channel_id)
        self._handshake_complete.apply_timeout(60.0)
        
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
        self._handshake_complete = Future(KOKORO)
        gateway = self.client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, 0, self_mute = True)
    
    
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
        self.clear_connected()
        
        token = event.token
        self._token = token
        endpoint = event.endpoint
        
        if (endpoint is None) or (token is None):
            return
        
        self._endpoint = endpoint.replace(':80', '').replace(':443', '')
        
        self._close_socket()
        
        socket = module_socket.socket(module_socket.AF_INET, module_socket.SOCK_DGRAM)
        
        protocol = await KOKORO.create_datagram_connection_with(
            partial_func(DatagramMergerReadProtocol, KOKORO), socket = socket
        )
        self._transport = protocol.get_transport()
        self._protocol = protocol
        self._socket = socket
        
        if self.reader is None:
            self.reader = AudioReader(self)
        
        handshake_complete = self._handshake_complete
        if handshake_complete.is_done():
            # terminate the web socket and handle the reconnect loop if necessary.
            self._handshake_complete = Future(KOKORO)
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
            transport.send_to(packet, (self._endpoint_ip, self._endpoint_port))
    
    
    def __del__(self):
        """Stops and unallocates the resources by the voice client, if was not done already."""
        self.stop()
        self._set_connected_waiters(False)
        self._stop_player_and_reader()
        self._close_socket()
        self.gateway.abort()
    
    
    def _stop_player_and_reader(self):
        """
        Stops the voice client's player and reader.
        """
        player = self.player
        if (player is not None):
            self.player = None
            player.stop()
        
        reader = self.reader
        if (reader is not None):
            self.reader = None
            reader.stop()
    
    
    def _close_socket(self):
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
        region = try_get_voice_region(self.guild_id, self.channel_id)
        
        if region is self.region:
            changed = False
        else:
            self.region = region
            changed = True
        
        return changed
    
    
    def __repr__(self):
        """Returns the voice client's representation."""
        repr_parts = [
            '<',
            type(self).__name__,
            ' client = ',
            repr(self.client.full_name),
            ', channel_id = ',
            repr(self.channel_id),
            ', guild_id = ',
            repr(self.guild_id),
        ]
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @property
    def channel(self):
        """
        Returns the voice client's channel.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the voice client's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    def get_encryption_mode(self):
        """
        Returns the encryption mode the voice client is currently using. Returns empty string if nothing yet.
        
        Returns
        -------
        encryption_mode : `str`
        """
        return self._encryption_adapter_type.name
    
    
    def set_encryption_mode(self, mode, key):
        """
        Sets encryption mode.
        
        Parameters
        ----------
        mode : `str`
            Encryption mode to set.
        
        key : `bytes`
            Secret key to initialize the adapter with.
        
        Raises
        ------
        RuntimeError
            - Not supported encryption mode given.
        """
        for encryption_adapter_type in AVAILABLE_ENCRYPTION_ADAPTERS:
            if encryption_adapter_type.name == mode:
                break
        
        else:
            available_nodes = ", ".join(
                repr(mode) for mode in
                sorted(encryption_adapter_type.name for encryption_adapter_type in AVAILABLE_ENCRYPTION_ADAPTERS)
            )
            
            raise RuntimeError(
                f'Failed to set encryption mode.'
                f'Received: {mode!r}.\n'
                f'Available: {available_nodes!s}.\n'
                f'The receive encryption mode is not available.'
            )
        
        self._encryption_adapter_type = encryption_adapter_type
        self._encryption_adapter = encryption_adapter_type(key)
    
    
    def prefer_encryption_mode_from_options(self, modes):
        """
        Prefers an encryption mode out of the given ones.
        
        Parameters
        ----------
        modes : `str`
            Encryption modes to prefer from.
        
        Raises
        ------
        RuntimeError
            - Not intersection between received and available encryption modes.
        """
        for encryption_adapter_type in AVAILABLE_ENCRYPTION_ADAPTERS:
            if encryption_adapter_type.name in modes:
                break
        
        else:
            received_nodes = ", ".join(repr(mode) for mode in sorted(modes))
            available_nodes = ", ".join(
                repr(mode) for mode in
                sorted(encryption_adapter_type.name for encryption_adapter_type in AVAILABLE_ENCRYPTION_ADAPTERS)
            )
            raise RuntimeError(
                f'Encryption mode mismatch.\n'
                f'Received: {received_nodes!s}.\n'
                f'Available: {available_nodes!s}.\n'
                f'No intersection.'
            )
        
        self._encryption_adapter_type = encryption_adapter_type
