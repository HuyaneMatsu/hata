__all__ = ('SolarPlayer', )

from math import floor
from random import randrange
from time import monotonic
from datetime import datetime

from ...backend.futures import Future, Task

from ...discord.core import KOKORO, GUILDS
from ...discord.channel import ChannelVoiceBase
from ...discord.bases import maybe_snowflake
from ...discord.utils import datetime_to_timestamp

from .constants import LAVALINK_KEY_GUILD_ID, LAVALINK_KEY_NODE_OPERATION, LAVALINK_KEY_NODE_OPERATION_VOICE_UPDATE, \
    LAVALINK_KEY_NODE_OPERATION_PLAYER_STOP, LAVALINK_KEY_NODE_OPERATION_PLAYER_PAUSE, LAVALINK_KEY_PAUSE, \
    LAVALINK_KEY_NODE_OPERATION_PLAYER_VOLUME, LAVALINK_KEY_VOLUME, LAVALINK_KEY_NODE_OPERATION_PLAYER_SEEK, \
    LAVALINK_KEY_POSITION_MS, LAVALINK_KEY_BAND, LAVALINK_KEY_GAIN, LAVALINK_KEY_NODE_OPERATION_PLAYER_EDIT_BANDS, \
    LAVALINK_KEY_BANDS, LAVALINK_BAND_COUNT, LAVALINK_KEY_START_TIME, LAVALINK_KEY_END_TIME, LAVALINK_KEY_NO_REPLACE, \
    LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY, LAVALINK_KEY_TRACK, LAVALINK_KEY_NODE_OPERATION_PLAYER_DESTROY
from .track import Track, ConfiguredTrack


class SolarPlayer:
    """
    Player of solar link.
    
    Attributes
    ----------
    _bands : `list` of `float`
        The bands of the player.
    _current_track : `None` or ``ConfiguredTrack``
        The currently played track if any.
    _forward_data : `None` or `dict` of (`str`, `Any`) items
        Json to forward to the player's node as necessary.
    _paused_track : `None` or ``ConfiguredTrack``
        The paused track.
    _position : `float`
        The position of the current track.
    _position_update : `float`
        When ``._position`` was last updated in monotonic time.
    _repeat : `bool`
        Whether tracks should be repeated.
    _repeat_actual : `bool`
        Whether the current track should be repeated. Defaults to `False`.
    _shuffle : `bool`
        Whether tracks should be shuffled.
    _volume : `float`
        The player's volume.
    channel_id : `int`
        The channel's identifier, where the node is connected to.
    guild_id : `int`
        The guild's identifier, where the player is.
    node : ``SolarNode``
        The node that the player is connected to. Defaults to `0`.
    queue : `list` of ``ConfiguredTrack``
        The queue of the tracks to play.
    """
    __slots__ = ('_bands', '_current_track', '_forward_data', '_paused_track', '_position', '_position_update',
        '_repeat', '_repeat_actual', '_shuffle', '_volume', 'channel_id', 'guild_id', 'node', 'queue')
    
    def __new__(cls, node, guild_id, channel_id):
        """
        Creates a new solar player instance.
        
        Parameters
        ----------
        node : ``SolarNode``
            The node of the player.
        guild_id : `int`
            The guild's identifier, where the node will connect to.
        channel_id : `int`
            The channel's identifier, where the node will connect to.
        
        Returns
        -------
        waiter : ``Future`` to ``SolarPlayer``
            A future, which can be awaited to get the connected player.
        """
        self = object.__new__(cls)
        
        self._position = 0.0
        self._position_update = 0.0
        
        self._shuffle = False
        self._repeat = False
        self._repeat_actual = False
        
        self._current_track = None
        self._paused_track = None
        self._bands = [0.0 for band_index in range(LAVALINK_BAND_COUNT)]
        self._volume = 1.0
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.node = node
        self.queue = []
        self._forward_data = None
        
        waiter = Future(KOKORO)
        Task(self._connect(waiter=waiter), KOKORO)
        return waiter
    
    
    async def _connect(self, waiter=None):
        """
        Connecting task of the solar player.
        
        This method is a coroutine.
        
        Parameters
        ----------
        waiter : `None` or ``Future``
            Waiter to set it's result or exception, when connection is established.
        """
        try:
            client = self.node.client
            
            gateway = client.gateway_for(self.guild_id)
            await gateway.change_voice_state(self.guild_id, self.channel_id)
        
        except GeneratorExit as err:
            if (waiter is not None):
                waiter.set_exception_if_pending(err)
                waiter = None
            
            raise
        
        except BaseException as err:
            if (waiter is not None):
                waiter.set_exception_if_pending(err)
                waiter = None
        
        if (waiter is not None):
            waiter.set_result_if_pending(self)
            waiter = None
    
    @property
    def is_playing(self):
        """
        Returns whether the player is currently playing anything.
        
        Returns
        -------
        is_playing : `bool`
        """
        if not self.channel_id:
            is_playing = False
        elif self._paused_track:
            is_playing = False
        elif self._current_track is None:
            is_playing = False
        else:
            is_playing = True
        
        return is_playing
    
    
    @property
    def is_connected(self):
        """
        Returns whether the player is connected to a voice channel.
        
        Returns
        -------
        is_connected : `bool`
        """
        if self.channel_id:
            is_connected = True
        else:
            is_connected = False
        
        return is_connected
    
    
    @property
    def position(self):
        """
        Returns the position in the track.
        
        Returns
        -------
        position : `float`
        """
        if (not self.is_playing):
            position = 0.0
        else:
            position = self._position
            
            if (self._paused_track is None):
                position += monotonic() - self._position_update
            
            duration = self._current_track.track.duration
            if position > duration:
                position = duration
        
        return position
    
    
    async def append(self, track, start_time=0.0, end_time=0.0, **added_attributes):
        """
        Adds a new track to play.
        
        This method is a coroutine.
        
        Parameters
        ----------
        track : ``Track``
            The track to play.
        start_time : `float`, Optional
            Where the track will start in seconds.
        **end_time : `float`. Optional
            Where the track will start in seconds.
        added_attributes : `dict` of (`str`, `Any`)
            Additional user defined attributes.
        
        Returns
        -------
        started_playing : `bool`
            Whether the source is started playing and not put on queue.
        
        Raises
        ------
        ValueError
            - If `start_time` is out of the expected [0.0:duration] range.
            - If `end_time` is out of the expected [0.0:duration] range.
        """
        configured_track = ConfiguredTrack(track, start_time, end_time, added_attributes)
        
        if self._current_track is None:
            node = self.node
            if (node is not None):
                await node._send({
                    LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                    LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    LAVALINK_KEY_NO_REPLACE: False,
                    **configured_track.un_pack(),
                })
            
            self._current_track = configured_track
            self._paused_track = None
            started_playing = True
        else:
            self.queue.append(configured_track)
            started_playing = False
        
        return started_playing
    
    
    async def play_next(self):
        """
        Plays the next track of the player. Calls this method, when a track is over, and not skipped.
        
        This method is a coroutine.
        
        Returns
        -------
        old_track : `None` or ``ConfiguredTrack``
        new_track : `None` or ``ConfiguredTrack``
        """
        # Are we paused, derp
        if (self._paused_track is not None):
            return
        
        old_track = self._current_track
        queue = self.queue
        if old_track is None:
            if queue:
                if self._shuffle:
                    pop_after = randrange(randrange(len(queue)))
                    
                else:
                    pop_after = 0
                new_track = queue[pop_after]
            
            else:
                pop_after = -1
                new_track = None
        else:
            if queue:
                if self._repeat_actual:
                    new_track = old_track
                    pop_after =  -1
                else:
                    if self._shuffle:
                        pop_after = randrange(len(queue))
                    else:
                        pop_after = 0
                    new_track = queue[pop_after]
                    
                    if self._repeat:
                        queue.append(old_track)
            
            else:
                pop_after = -1
                if self._repeat:
                    new_track = old_track
                else:
                    new_track = None
        
        if (new_track is None):
            if (old_track is None):
                # We are stopped, do nothing
                pass
            else:
                # We stop
                node = self.node
                if (node is not None):
                    await node._send({
                        LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_STOP,
                        LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    })
        else:
            node = self.node
            if (node is not None):
                await node._send({
                    LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                    LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    LAVALINK_KEY_NO_REPLACE: False,
                    **new_track.un_pack(),
                })
        
        self._current_track = new_track
        
        if pop_after != -1:
            del queue[pop_after]
        
        return old_track, new_track
    
    
    def get_current(self):
        """
        Returns the currently playing or paused track of the player.
        
        Returns
        -------
        track : `None` or ``ConfiguredTrack``
        """
        return self._current_track
    
    
    def iter_all_track(self):
        """
        Iterates over all the tracks of the player.
        
        This method is an iterable generator.
        
        Yields
        ------
        track : ``ConfiguredTrack``
        """
        current_track = self._current_track
        if (current_track is not None):
            yield current_track
        
        yield from self.queue
    
    
    async def stop(self):
        """
        Stops the player's current track.
        
        This method is a coroutine.
        """
        # Are we already stopped?
        if self._current_track is None:
            return
        
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_STOP,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
            })
        
        self._paused_track = None
        self._current_track = None
    
    
    async def skip(self, index=0):
        """
        Skips the given track from the queue and returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        index : `int`, Optional
            The track's index to skip.
            
            When skipping the `0`-th track, so the current, it will start to play the next if not paused.
        
        Returns
        -------
        track : `None` or ``ConfiguredTrack``
        """
        queue = self.queue
        
        if index == 0:
            track = self._current_track
            self._current_track = None
            
            if queue:
                if self._shuffle:
                    track_index = randrange(len(queue))
                    new_track = queue[track_index]
                else:
                    track_index = 0
                    new_track = queue[0]
            else:
                new_track = None
                track_index = -1
            
            node = self.node
            if new_track is None:
                if (node is not None):
                    await node._send({
                        LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_STOP,
                        LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    })
            
            else:
                if (self._paused_track is not None):
                    if (node is not None):
                        await node._send({
                            LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                            LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                            LAVALINK_KEY_NO_REPLACE: False,
                            **new_track.un_pack(),
                        })
                
                self._current_track = new_track
            
            if track_index != -1:
                del queue[track_index]
        
        elif index < 0:
            track = None
        
        else:
            if index > len(queue):
                track = None
            else:
                track = queue.pop(index-1)
        
        return track
        
    
    def set_repeat(self, repeat, actual=None):
        """
        Sets the player to repeat the tracks.
        
        Parameters
        ----------
        repeat : `bool`
            Whether to repeat the player or not.
        actual : `bool`
            Whether the current track should be repeated.
        """
        self._repeat = repeat
        
        if repeat:
            if (actual is not None):
                self._repeat_actual = actual
        else:
            self._repeat_actual = False
    
    
    def is_repeating(self):
        """
        Returns whether the player is repeating the tracks.
        
        Returns
        -------
        repeat : `bool`
        """
        return self._repeat
    
    
    def is_repeating_actual(self):
        """
        Returns whether the player is repeating the actual track.
        
        Returns
        -------
        repeat_actual : `bool`
        """
        return self._repeat_actual
    
    
    def set_shuffle(self, shuffle):
        """
        Sets the player's shuffle the tracks.
        
        Note, that if the current actual track is repeated shuffling is ignored.
        
        Parameters
        ----------
        shuffle : `bool`
            Whether to shuffle the player or not.
        """
        self._shuffle = shuffle
    
    
    def is_shuffling(self):
        """
        Returns whether the player is shuffling the tracks.
        
        Returns
        -------
        shuffle : `bool`
        """
        return self._shuffle
    
    
    async def pause(self):
        """
        Pauses the player.
        
        This method is a coroutine.
        """
        if (self._paused_track is not None):
            return
        
        current_track = self._current_track
        if (current_track is None):
            return
        
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PAUSE,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_PAUSE: True,
            })
        
        self._paused_track = current_track
    
    
    async def resume(self):
        """
        Resumes the player.
        
        This method is a coroutine.
        """
        paused_track = self._paused_track
        if (paused_track is None):
            return
        
        current_track = self._current_track
        if (current_track is None):
            # Should not happen.
            return
        
        node = self.node
        if (node is not None):
            if (paused_track is current_track):
                await node._send({
                    LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PAUSE,
                    LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    LAVALINK_KEY_PAUSE: False,
                })
            else:
                await node._send({
                    LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                    LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    LAVALINK_KEY_NO_REPLACE: False,
                    **current_track.un_pack(),
                })
        
        self._paused_track = None
    
    
    def is_paused(self):
        """
        Returns whether the player is currently paused.
        
        Returns
        -------
        is_paused : `bool`
        """
        return (self._paused_track is not None)
    
    
    async def set_volume(self, volume):
        """
        Sets the player's volume.
        
        This method is a coroutine.
        
        Parameters
        ----------
        volume : `float`
            The new volume level. Can be in range [0.0:10.0].
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 10.0:
            volume = 10.0
        
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_VOLUME,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_VOLUME: floor(volume*100.0),
            })
        
        self._volume = volume
    
    
    def get_volume(self):
        """
        Returns the player's volume.
        
        Returns
        -------
        volume : `float`
        """
        return self._volume
    
    
    async def seek(self, position):
        """
        Seeks to a given position in the track.
        
        This method is a coroutine.
        
        Parameters
        ----------
        position : `float`
            The new position in seconds.
        """
        if (self._current_track is None):
            return
        
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_SEEK,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_POSITION_MS: floor(position*1000.0),
        })
    
    
    async def set_gain(self, band, gain):
        """
        Sets the band gain to the given amount.
        
        This method is a coroutine.
        
        Parameters
        ----------
        band : `int`
            Band number [0:14].
        gain : `float`
            A float representing gain of a band [-0.25:1.0]. Defaults to `0.0`.
        
        Raises
        ------
        ValueError
            If `band` is out of range [0:14].
        """
        await self.set_gains((band, gain))
    
    
    async def set_gains(self, *band_gain_pairs):
        """
        Modifies the player's band settings.
        
        This method is a coroutine
        
        Parameters
        ----------
        *band_gain_pairs : `list` of `tuple` of (`int`, `float`)
            `band` - `gain` tuples.
        
        Raises
        ------
        TypeError
            If `band_gain_pairs` contains a non-tuple element.
        ValueError
            If `band` is out of range [0:14].
        """
        to_update = []
        
        for band_gain_pair in band_gain_pairs:
            if not isinstance(band_gain_pair, tuple):
                raise TypeError(f'`band_gain_pairs` can contain only `tuple` elements, got '
                    f'{band_gain_pair.__class__.__name__}; {band_gain_pair!r}.')
            
            band, gain = band_gain_pair
            
            if (band < 0) or (band > 14):
                raise ValueError(f'`band`, can be in range [0:14], got {band}.')
            
            if gain > 1.0:
                gain = 1.0
            elif gain < -0.25:
                gain = -0.25
            
            to_update.append((band, gain))
        
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_EDIT_BANDS,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_BANDS: [
                    {
                        LAVALINK_KEY_BAND: band,
                        LAVALINK_KEY_GAIN: gain,
                    } for band, gain in to_update
                ],
            })
        
        for band, gain in to_update:
            self._bands[band] = gain
    
    
    async def reset_gains(self):
        """
        Resets all bands of the player to their default value.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_EDIT_BANDS,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_BANDS: [
                    {
                        LAVALINK_KEY_BAND: band,
                        LAVALINK_KEY_GAIN: 0.0,
                    } for band in range(LAVALINK_BAND_COUNT)
                ],
            })
        
        for band in LAVALINK_BAND_COUNT:
            self._bands[band] = 0.0


    async def _update_state(self, data):
        """
        Updates the position of the player.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            State data given.
        """
        try:
            position = data[LAVALINK_KEY_POSITION_MS]
        except KeyError:
            position = 0.0
        else:
            position = position*1000.0
        
        self._position = position
        self._position_update = monotonic()
        # There is also a time key, but dunno why i would use it.
    
    
    async def change_node(self, node):
        """
        Changes the player's node
        
        Parameters
        ----------
        node ``SolarNode``
            The node the player is changed to.
        """
        old_node = self.node
        if (old_node is not None) and old_node.available:
            await old_node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_DESTROY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
            })
        
        self.node = node
        
        forward_data = self._forward_data
        if (forward_data is not None) and (len(forward_data) == 2):
            await node._send(
                {
                    LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_VOICE_UPDATE,
                    LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                    **forward_data,
                }
            )
        
        current_track = self._current_track
        if (current_track is not None):
            node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                **current_track.un_pack(),
                LAVALINK_KEY_START_TIME: floor(self.position*1000.0),
                LAVALINK_KEY_PAUSE: (self._paused_track is current_track),
                LAVALINK_KEY_VOLUME: floor(self._volume*100.0),
            })
        
        modified_bands = None
        bands = self._bands
        for band in range(LAVALINK_BAND_COUNT):
            gain = bands[band]
            if gain:
                if modified_bands is None:
                    modified_bands = []
                
                modified_bands.append((band, gain))
        
        
        if (modified_bands is not None):
            node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_EDIT_BANDS,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_BANDS: [
                    {
                        LAVALINK_KEY_BAND: band,
                        LAVALINK_KEY_GAIN: gain,
                    } for band, gain in modified_bands
                ],
            })
    
    
    async def disconnect(self):
        """
        Disconnects the player from Discord.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is None):
            return
            
        client = node.client
        
        try:
            client.solarlink.players[self.guild_id]
        except KeyError:
            pass
        
        if (not node.available):
            await self.node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_DESTROY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
            })
        
        gateway = client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, 0)
        
        self.node = None
    
    
    async def move_to(self, channel):
        """
        Move the voice client to an another voice channel.
        
        This method is a coroutine.
        
        Parameters
        ---------
        channel : ``ChannelVoiceBase`` or `int` instance
            The channel where the voice client will move to.
        
        Raises
        ------
        TypeError
            If  `channel` was not given as ``ChannelVoiceBase`` not `int` instance.
        """
        node = self.node
        if node is None:
            # Already disconnected.
            return
        
        if isinstance(channel, ChannelVoiceBase):
            channel_id = channel.id
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(f'`channel` can be given as {ChannelVoiceBase.__name__}, or as `int` instance, got '
                    f'{channel.__class__.__name__}.')
        
        if self.channel_id == channel_id:
            return
        
        gateway = node.client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, channel_id)
    
    
    def __repr__(self):
        """Returns the representation of the player."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' guild_id=', repr(self.guild_id),
        ]
        
        channel_id = self.channel_id
        if channel_id:
            repr_parts.append(', channel_id=')
            repr_parts.append(repr(channel_id))
        
        repr_parts.append('>')
        
        repr_parts.append(''.join(repr_parts))


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
        RuntimeError
            Operation on disconnected player.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        node = self.node
        if node is None:
            # Already disconnected.
            return
        
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            try:
                voice_state = guild.voice_states[node.client.id]
            except KeyError:
                return
            
            if voice_state.is_speaker:
                return
        
        if request:
            timestamp = datetime_to_timestamp(datetime.utcnow())
        else:
            timestamp = None
        
        data = {
            'suppress': False,
            'request_to_speak_timestamp': timestamp,
            'channel_id': self.channel_id
        }
        
        await node.client.http.voice_state_client_edit(guild_id, data)
    
    
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
        node = self.node
        if node is None:
            # Already disconnected.
            return
        
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            try:
                voice_state = guild.voice_states[node.client.id]
            except KeyError:
                return
            
            if not voice_state.is_speaker:
                return
        
        data = {
            'suppress': True,
            'channel_id': self.channel_id
        }
        
        await node.client.http.voice_state_client_edit(guild_id, data)
