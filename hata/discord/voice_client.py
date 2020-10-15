# -*- coding: utf-8 -*-
__all__ = ('VoiceClient', )

import socket as module_socket
from threading import Event

from ..backend.dereaddons_local import DOCS_ENABLED
from ..backend.futures import Future, Task, sleep, future_or_timeout, Lock
from ..backend.exceptions import ConnectionClosed, WebSocketProtocolError, InvalidHandshake

from .client_core import KOKORO
from .opus import OpusEncoder
from .player import AudioPlayer, AudioSource, PLAYER_DELAY
from .reader import AudioReader, AudioStream
from .gateway import DiscordGatewayVoice, SecretBox
from .channel import ChannelVoice
from .exceptions import VOICE_CLIENT_DISCONNECTC_CLOSE_CODE

from . import guild

class VoiceClient(object):
    """
    Represents a client what is joined to a voice channel.
    
    Attributes
    ----------
    _audio_port : `int`
        The port, where the voice client should send the audio data.
    _audio_source : `int`
        An identificator sent by Discord what should be sent back with every voice packet.
    _audio_sources : `dict` of (`int`, `int`) items
        `user_id` - `audio_source` mapping used by ``AudioStream``-s.
    _audio_streams : `None` or `dict` of (`int`, (``AudioStream`` or (`list` of ``AudioStream``)) items
        `user_id` - ``AudioStream``(s) mapping for linking ``AudioStream`` to their respective user..
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
    _secret_box : `None` or `nacl.secret.SecretBox`
        Data encoder of the voice client.
    _sequence : `int`
        Counter to define the sent data's sequence for Discord.
    _session_id : `None` or `str`
        The session id of the voice client's owner client's shard.
    _set_speaking_task : `None` or ``Task``
        Synchronization task for the `.set_speaking` coroutine.
    _timestamp : `int`
        A timestamp identificaotr to tell Discord how much frames we sent to it.
    _token : `str`
        Token received by the voice client's owner client's gateway. Used to authorize the voice client.
    _video_source : `int`
        An identificator sent by Discord what should be sent back with every video packet.
    call_after : `callable` (`awaitable`)
        A coroutine function what is awaited, when the voice clients's current audio finishes playing. By default
        this attribute is set to the ``._play_next`` function of the voice client (plays the next audio at the voice
        clients's ``.queue`` as expected.
        
        This attribute of the client can be modified freely. To it `2` arguments are passed:
         +------------------+---------------------------+
         | Respective name  | Type                      |
         +==================+===========================+
         | client           | ``VoiceClient``           |
         +------------------+---------------------------+
         | last_source      | `None` or ``AudioSource`` |
         +------------------+---------------------------+
         
         The ``VoiceClient`` also includes some other predefined function for setting as `call_after`:
         - ``._loop_actual``
         - ``._loop_queue``
     
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
    speaking : `int`
        Whether the client is showed by Discord as `speaking`, then this attribute should is set as `1`. Can be
        modified, with the ``.set_speaking``, however it is always adjusted to the voice client's current playing state.
    """
    __slots__ = ('_audio_port', '_audio_source', '_audio_sources', '_audio_streams', '_encoder', '_endpoint',
        '_endpoint_ip', '_handshake_complete', '_ip', '_port', '_pref_volume', '_secret_box', '_sequence',
        '_session_id', '_set_speaking_task', '_timestamp', '_token', '_video_source', 'call_after', 'channel', 'client',
        'connected', 'gateway', 'guild', 'lock', 'player', 'queue', 'reader', 'socket', 'speaking', )
    
    def __new__(cls, client, channel):
        """
        Creates a ``VoiceClient`` instance. If any of the required libraries are not present, raises `RuntimeError`.
        
        If the voice client was succesfully created, returns a ``Future``, what is a waiter for it's ``._connect``
        method. If connecting failed, then the future will raise `TimeoutError`.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        channel : ``ChannelVoice``
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
        
        self.guild = guild
        self.channel = channel
        self.gateway = DiscordGatewayVoice(self)
        self.socket = None
        self.client = client
        self.connected = Event() #this will be used at the AudioPlayer thread
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
        self._audio_streams = None
        
        client.voice_clients[guild.id] = self
        waiter = Future(KOKORO)
        Task(self._connect(waiter=waiter), KOKORO)
        return waiter
    
    #properties
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
        A coroutine, what is used when changing the ``.speaking`` state of the voice client. By default when audio is
        played, the speaking state is changed to `True` and meanwhile not, then to `False`.
        
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
        **kwargs : Keyword arguments
            Additional keyword arguments.
        
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
        Unlinks the given audio stream from the voice client causing it to stop receiving audio.
        
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
                        
                        if (not reader_audio_streams):
                            self.reader = None
                            reader.stop()
    
    def _remove_audio_source(self, user_id):
        """
        Unlinks the audio streams's source listening to the given user (id), causing the affected audio stream(s)
        to stop receiving audio data at the meanwhile.
        
        Parameters
        ----------
        user_id : `int`
            The respective user's id.
        """
        voice_sources = self._audio_sources
        try:
            voice_source = voice_sources.pop(user_id)
        except KeyError:
            return
        
        audio_streams = self._audio_streams
        if (audio_streams is None):
            return
        
        try:
            audio_streams[user_id]
        except KeyError:
            return
        
        reader = self.reader
        if (reader is None):
            return
        
        try:
            del reader.audio_streams[voice_source]
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
            Audio source identitifcator of the user.
        """
        voice_sources = self._audio_sources
        try:
            old_audio_source = voice_sources.pop(user_id)
        except KeyError:
            # Should not happen if it is an update, onyl if it is an add
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
            KOKORO.create_task(self.play_next())
            player = self.player
            if player is None:
                source = None
            else:
                source = player.source
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
            self.player = None
            player.done = True
            player.source = None
            player.resumed.set()
    
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
                    tries+=1
                    continue
                except:
                    await self.disconnect(force=True)
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
                    if isinstance(err, ConnectionClosed) and (err.code == VOICE_CLIENT_DISCONNECTC_CLOSE_CODE):
                        await self.disconnect(force=False)
                        return
                    
                    await sleep(1+(tries<<1), KOKORO)
                    tries +=1
                    await self._terminate_handshake()
                    continue
                
                except:
                    await self.disconnect(force=True)
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
                        if isinstance(err, ConnectionClosed):
                            code = err.code
                            if code in (1000, 1006) or (code == VOICE_CLIENT_DISCONNECTC_CLOSE_CODE):
                                await self.disconnect(force=False)
                                return
                        
                        self.connected.clear()
                        await sleep(5., KOKORO)
                        await self._terminate_handshake()
                        break
                    
                    except:
                        await self.disconnect(force=True)
                        raise
        finally:
            try:
                del self.client.voice_clients[self.guild.id]
            except KeyError:
                pass
    
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
        
        self.queue.clear()
        player = self.player
        if (player is not None):
            self.player = None
            player.done = True
            player.source = None
            # Set connected so the player can do 1 full loop
            self.connected.set()
            player.resumed.set()
            await sleep(PLAYER_DELAY, KOKORO)
        
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
            socket = self.socket
            if (socket is not None):
                self.socket = None
                socket.close()
    
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
            await self._play_next(self, None)
    
    @staticmethod
    async def _play_next(self, last_source):
        """
        Starts to play the next audio object on ``.queue`` and cancels the actual one if applicable.

        Should be used inside of ``.lock``to ensure that the voice client is not modified pararelly.
        
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
    
    @staticmethod
    async def _loop_actual(self, last_source):
        """
        Repeats the last played audio if applicable.
        
        Should be used inside of ``.lock``to ensure that the voice client is not modified pararelly.
        
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
        elif player.done:
            # If we skipped the audio, `player.don`e is set as `True`, so we do not want to repeat.
            await self._play_next(self, None)
            return
        else:
            # The audio was over.
            player.source = last_source
            player.resumed.set()
        
        if self.connected.is_set():
            Task(self.set_speaking(1), KOKORO)
    
    @staticmethod
    async def _loop_queue(self, last_source):
        """
        Puts the last played audio back on the voice client's queue.
        
        Should be used inside of ``.lock``to ensure that the voice client is not modified pararelly.
        
        Parameters
        ----------
        self : ``VoiceClient``
            The respective voice client.
        last_source : `None` or ``AudioSource`` instance
            The audio what was played.
        """
        player = self.player
        if ((player is None) or (not player.done)) and ((last_source is not None) and last_source.REPEATABLE):
            # The last source was not skipped an we can repeat it.
            self.queue.append(last_source)
        
        await self._play_next(self, None)
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
        self._token = token
        endpoint = data.get('endpoint',None)
        
        if (endpoint is None) or (token is None):
            return
        
        self._endpoint = endpoint.replace(':80','').replace(':443','')
        
        socket = self.socket
        if socket is not None:
            socket.close()
        
        socket = module_socket.socket(module_socket.AF_INET, module_socket.SOCK_DGRAM)
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
        
        player = self.player
        if (player is not None):
            self.player = None
            player.done = True
            player.source = None
            player.resumed.set()
        
        reader = self.reader
        if (reader is not None):
            self.reader = None
            reader.stop()
        
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


guild.VoiceClient = VoiceClient

del guild
del DOCS_ENABLED
