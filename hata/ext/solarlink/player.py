__all__ = ('SolarPlayer', )

from datetime import datetime
from random import randrange

from scarletio import copy_docs

from ...discord.core import GUILDS
from ...discord.utils import datetime_to_timestamp

from .filters import Volume
from .player_base import SolarPlayerBase
from .track import ConfiguredTrack, Track


class SolarPlayer(SolarPlayerBase):
    """
    Player of solar link.
    
    Attributes
    ----------
    _forward_data : `None`, `dict` of (`str`, `object`) items
        Json to forward to the player's node as necessary.
    _position : `float`
        The position of the current track.
    _position_update : `float`
        When ``._position`` was last updated in monotonic time.
    channel_id : `int`
        The channel's identifier, where the node is connected to.
    guild_id : `int`
        The guild's identifier, where the player is.
    node : ``SolarNode``
        The node that the player is connected to. Defaults to `None`.
    _current_track : `None`, ``ConfiguredTrack``
        The currently played track if any.
    _paused : `bool`
        Whether the player is paused.
    _paused_track : `None`, ``ConfiguredTrack``
        The paused track.
    _repeat_current : `bool`
        Whether the current track should be repeated. Defaults to `False`.
    _repeat_queue : `bool`
        Whether tracks should be repeated.
    _shuffle : `bool`
        Whether tracks should be shuffled.
    queue : `list` of ``ConfiguredTrack``
        The queue of the tracks to play.
    """
    __slots__ = (
        '_current_track', '_paused', '_paused_track', '_repeat_current', '_repeat_queue', '_shuffle', 'queue'
    )
    
    @copy_docs(SolarPlayerBase.__new__)
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
        waiter : ``Future`` to ``SolarPlayerBase``
            A future, which can be awaited to get the connected player.
        """
        self, waiter = SolarPlayerBase.__new__(cls, node, guild_id, channel_id)
        
        self._shuffle = False
        self._repeat_queue = False
        self._repeat_current = False
        self._current_track = None
        self._paused = None
        self._paused_track = None
        self.queue = []
        
        return self, waiter
    
    
    @copy_docs(SolarPlayerBase.is_paused)
    def is_paused(self):
        return self._paused
    
    
    @copy_docs(SolarPlayerBase.get_current)
    def get_current(self):
        return self._current_track
    
    
    def get_volume(self):
        """
        Returns the player's volume.
        
        Returns
        -------
        volume : `float`
        """
        filter = self.get_filter(Volume)
        if filter is None:
            volume = 1.0
        else:
            volume = filter._volume
        
        return volume
    
    
    async def append(self, track, start_time = 0.0, end_time = 0.0, **added_attributes):
        """
        Adds a new track to play.
        
        This method is a coroutine.
        
        Parameters
        ----------
        track : ``Track``
            The track to play.
        start_time : `float` = `0.0`, Optional
            Where the track will start in seconds.
        end_time : `float` = `0.0`, Optional
            Where the track will start in seconds.
        **added_attributes : `dict` of (`str`, `object`)
            Additional user defined attributes.
        
        Returns
        -------
        started_playing : `bool`
            Whether the source is started playing and not put on queue.
        
        Raises
        ------
        TypeError
            If `track` is neither ``Track``, nor ``ConfiguredTrack``.
        ValueError
            - If `start_time` is out of the expected [0.0:duration] range.
            - If `end_time` is out of the expected [0.0:duration] range.
        """
        configured_track = ConfiguredTrack(track, start_time, end_time, added_attributes)
        
        if self._current_track is None:
            paused = self._paused
            if (not paused):
                await self._play(configured_track)
            
            self._current_track = configured_track
            
            if paused:
                started_playing = False
            else:
                started_playing = True
        else:
            self.queue.append(configured_track)
            started_playing = False
        
        return started_playing
    
    
    def move_track(self, source_index, target_index):
        """
        Moves the track to the target index.
        
        Parameters
        ----------
        source_index : `int`
            The track's current index.
        target_index : `int`
            the track's new index.
        
        Returns
        -------
        track : `None`, ``ConfiguredTrack``
            The moved track if any.
        
        Raises
        ------
        AssertionError
            - If `source_index` is not `int`.
            - If `target_index` is not `int`.
        """
        if __debug__:
            if not isinstance(source_index, int):
                raise AssertionError(
                    f'`source_index` can be `int`, got {source_index.__class__.__name__}; {source_index!r}.'
                )
            
            if not isinstance(target_index, int):
                raise AssertionError(
                    f'`target_index` can be `int`, got {target_index.__class__.__name__}; {target_index!r}.'
                )
        
        queue = self.queue
        if queue:
            queue_length = len(queue)
            
            if source_index < 0:
                source_index = 0
            elif source_index >= queue_length:
                source_index = queue_length-1
            
            if target_index < 0:
                target_index = 0
            
            
            if target_index == source_index:
                track = None
            
            else:
                track = queue.pop(source_index)
                queue.insert(target_index, track)
        
        else:
            track = None
        
        return track
    
    
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
        
        await self._stop()
        
        # do not change `self._paused`
        self._paused_track = None
        self._current_track = None
    
    
    async def skip(self, index=0):
        """
        Skips the given track by it's index and returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        index : `int` = `0.0`, Optional
            The track's index to skip.
            
            When skipping the `0`-th track, so the current, it will start to play the next if not paused.
        
        Returns
        -------
        track : `None`, ``ConfiguredTrack``
        """
        queue = self.queue
        
        if index == 0:
            track = self._current_track
            self._current_track = None
            
            if self._repeat_current:
                if not self._paused:
                    await self._play(track)
                
                self._current_track = track
            
            elif self._repeat_queue:
                # Only repeat the actual, if there is no other.
                if queue:
                    if self._shuffle:
                        track_index = randrange(len(queue))
                    else:
                        track_index = 0
                    
                    new_track = queue[track_index]
                else:
                    new_track = track
                    track_index = -1
                
                if not self._paused:
                    await self._play(new_track)
                
                self._current_track = new_track
                
                if track_index != -1:
                    del queue[track_index]
                    queue.append(track)
            
            else:
                if queue:
                    if self._shuffle:
                        track_index = randrange(len(queue))
                    else:
                        track_index = 0
                    new_track = queue[track_index]
                else:
                    new_track = None
                    track_index = -1
                
                if new_track is None:
                    await self._stop()
                
                else:
                    if not self._paused:
                        await self._play(new_track)
                    
                    self._current_track = new_track
                
                if track_index != -1:
                    del queue[track_index]
        
        elif index < 0:
            track = None
        
        else:
            if index > len(queue):
                track = None
            else:
                track = queue.pop(index - 1)
                
                if self._repeat_queue and (not self._repeat_current):
                    queue.append(track)
        
        return track
    
    
    async def remove(self, index=0):
        """
        Removes the track with the given index from the queue and returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        index : `int` = `0.0`, Optional
            The track's index to skip.
            
            When skipping the `0`-th track, so the current, it will start to play the next if not paused.
        
        Returns
        -------
        track : `None`, ``ConfiguredTrack``
        """
        queue = self.queue
        
        if index == 0:
            track = self._current_track
            self._current_track = None
            
            if queue:
                if self._shuffle:
                    track_index = randrange(len(queue))
                else:
                    track_index = 0
                new_track = queue[track_index]
                
                if not self._paused:
                    await self._play(new_track)
                
                self._current_track = new_track
                del queue[index]
            
            else:
                if (track is not None):
                    await self._stop()
        
        elif index > len(queue):
            track = None
        else:
            track = queue.pop(index - 1)
        
        return track
    
    
    async def pause(self):
        """
        Pauses the player.
        
        This method is a coroutine.
        """
        if self._paused:
            return
        
        current_track = self._current_track
        if (current_track is not None):
            await self._pause()
        
        self._paused = True
        self._paused_track = current_track
    
    
    async def resume(self):
        """
        Resumes the player.
        
        This method is a coroutine.
        """
        if not self._paused:
            return
        
        paused_track = self._paused_track
        if (paused_track is not None):
            current_track = self._current_track
            if (current_track is not None):
                node = self.node
                if (node is not None):
                    if (paused_track is current_track):
                        await self._resume()
                    else:
                        await self._play(current_track)
        
        self._paused_track = None
        self._paused = False
    
    
    def set_repeat_queue(self, repeat):
        """
        Sets the player to repeat the whole queue.
        
        Parameters
        ----------
        repeat : `bool`
            Whether to repeat queue.
        """
        self._repeat_queue = repeat
        
        if repeat:
            self._repeat_current = False
    
    
    def set_repeat_current(self, repeat):
        """
        Sets the player to repeat the actual track.
        
        Parameters
        ----------
        repeat : `bool`
            Whether to repeat the player or not.
        actual : `bool`
            Whether the repeat the current track.
        """
        self._repeat_current = repeat
        
        if repeat:
            self._repeat_queue = False
    
    
    def is_repeating_queue(self):
        """
        Returns whether the player is repeating the queue.
        
        Returns
        -------
        repeat : `bool`
        """
        return self._repeat_queue
    
    
    def is_repeating_current(self):
        """
        Returns whether the player is repeating the current track.
        
        Returns
        -------
        repeat_current : `bool`
        """
        return self._repeat_current
    
    
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
    
    
    async def set_volume(self, volume):
        """
        Sets the player's volume.
        
        This method is a coroutine.
        
        Parameters
        ----------
        volume : `float`
            The new volume level. Can be in range [0.0:10.0].
        """
        self.add_filter(Volume(volume))
        await self.apply_filters()
    
    
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
        
        await self._seek(position)
    
    
    async def join_speakers(self, *, request=False):
        """
        Requests to speak at the voice client's voice channel. Only applicable for stage channels.
        
        This method is a coroutine.
        
        Parameters
        ----------
        request : `bool` = `False`, Optional (Keyword only)
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
            
            if voice_state.speaker:
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
        Joins the audience in the voice client's voice channel. Only applicable for stage channels.
        
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
            
            if not voice_state.speaker:
                return
        
        data = {
            'suppress': True,
            'channel_id': self.channel_id
        }
        
        await node.client.http.voice_state_client_edit(guild_id, data)
