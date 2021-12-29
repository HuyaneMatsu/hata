__all__ = ('SolarPlayerBase', )

from math import floor
from random import randrange
from time import monotonic
from datetime import datetime

from scarletio import Future, Task

from ...discord.core import KOKORO, GUILDS, CHANNELS
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


class SolarPlayerBase:
    """
    Base player of solar link.
    
    Attributes
    ----------
    _forward_data : `None`, `dict` of (`str`, `Any`) items
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
    
    
    When subclassing please overwrite the following methods:
    
    - ``.is_paused``
    - ``.get_current``
    - ``.get_volume``
    - ``.get_bands``.
    
    """
    __slots__ = ('_forward_data', '_position', '_position_update', 'channel_id', 'guild_id',
        'node',)
    
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
        self : ``SolarPlayerBase``
            The player.
        waiter : ``Future``
            A future, which can be awaited to wait till the player is connected.
        """
        self = object.__new__(cls)
        
        self._position = 0.0
        self._position_update = 0.0
        self._forward_data = None
        
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.node = node
        
        waiter = Future(KOKORO)
        Task(self._connect(waiter=waiter), KOKORO)
        
        return self, waiter
    
    
    async def _connect(self, waiter=None):
        """
        Connecting task of the solar player.
        
        This method is a coroutine.
        
        Parameters
        ----------
        waiter : `None`, ``Future``
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
    
    
    def is_playing(self):
        """
        Returns whether the player is currently playing anything.
        
        Returns
        -------
        is_playing : `bool`
        """
        if not self.channel_id:
            is_playing = False
        elif self.is_paused():
            is_playing = False
        elif (self.get_current() is not None):
            is_playing = True
        else:
            is_playing = True
        
        return is_playing
    
    
    def is_paused(self):
        """
        Returns whether the player is currently paused.
        
        Returns
        -------
        is_paused : `bool`
        """
        raise NotImplementedError
    
    
    def is_connected(self):
        """
        Returns whether the player is connected to a voice channel.
        
        Returns
        -------
        is_connected : `bool`
        """
        if self.node is None:
            is_connected = False
        elif self.channel_id:
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
        current_track = self.get_current()
        if (current_track is None):
            position = 0.0
        else:
            position = self._position
            
            if not self.is_paused():
                position += monotonic() - self._position_update
            
            duration = current_track.track.duration
            if position > duration:
                position = duration
        
        return position
    
    
    def get_current(self):
        """
        Returns the currently playing or paused track of the player.
        
        Returns
        -------
        track : `None`, ``ConfiguredTrack``
        """
        raise NotImplementedError
    
    
    def get_volume(self):
        """
        Returns the player's volume.
        
        Returns
        -------
        volume : `float`
        """
        raise NotImplementedError
    
    
    def get_bands(self):
        """
        Returns the bands of the player.
        
        Returns
        -------
        bands : `list` of `float`
        """
        raise NotImplementedError
    
    
    async def _play(self, configured_track, replace=True):
        """
        Sends a play payload to the player's node.
        
        This method is a coroutine.
        
        Parameters
        ----------
        configured_track : ``ConfiguredTrack``
            The track to play.
        replace : `bool`, Optional
            Whether the current operation, like playing and pausing should be overwritten.
            
            Defaults to `True`.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_NO_REPLACE: (not replace),
                **configured_track.un_pack(),
            })
    
    
    async def _stop(self):
        """
        Sends a stop payload to the player's node.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_STOP,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
            })
    
    
    async def _pause(self):
        """
        Sends a pause payload to the player's node.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PAUSE,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_PAUSE: True,
            })
    
    
    async def _resume(self):
        """
        Sends a resume payload to the player's node.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PAUSE,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_PAUSE: False,
            })
    
    
    async def _set_volume(self, volume):
        """
        Sends a a set volume payload to the player's node.
        
        This method is a coroutine.
        
        Parameters
        ----------
        volume : `float`
            The new volume level. Can be in range [0.0:10.0].
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_VOLUME,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_VOLUME: floor(volume*100.0),
            })
    
    
    async def _set_gains(self, band_gain_pairs):
        """
        Sends a band edit update to the player's node.
        
        This method is a coroutine
        
        Parameters
        ----------
        band_gain_pairs : `list` (`int`, `float`)
            `band` - `gain` tuples.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_EDIT_BANDS,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_BANDS: [
                    {
                        LAVALINK_KEY_BAND: band,
                        LAVALINK_KEY_GAIN: gain,
                    } for band, gain in band_gain_pairs
                ],
            })
    
    async def _seek(self, position):
        """
        Sends a seek payload to the player's node.
        
        This method is a coroutine.
        
        Parameters
        ----------
        position : `float`
            The new position in seconds.
        """
        node = self.node
        if (node is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_SEEK,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                LAVALINK_KEY_POSITION_MS: floor(position*1000.0),
        })
    
    
    async def _destroy(self):
        """
        Sends a destroy payload to the player's node.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None) and node.available:
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_DESTROY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
            })
    
    
    async def _voice_update(self):
        """
        Sends voice update payload to the player's node.
        
        This method is a coroutine.
        """
        node = self.node
        if (node is not None):
            forward_data = self._forward_data
            if (forward_data is not None) and (len(forward_data) == 2):
                await node._send(
                    {
                        LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                        LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_VOICE_UPDATE,
                        **self._forward_data,
                    }
                )
    
    
    def _update_state(self, data):
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
            del client.solarlink.players[self.guild_id]
        except KeyError:
            pass
        
        await self._destroy()
        
        gateway = client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, 0)
        
        self.node = None
    
    
    async def move_to(self, channel):
        """
        Move the voice client to an another voice channel.
        
        This method is a coroutine.
        
        Parameters
        ---------
        channel : ``ChannelVoiceBase``, `int`
            The channel where the voice client will move to.
        
        Raises
        ------
        TypeError
            If  `channel` was not given as ``ChannelVoiceBase`` not `int`.
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
                raise TypeError(
                    f'`channel` can be `{ChannelVoiceBase.__name__}`, `int`, got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
        
        if self.channel_id == channel_id:
            return
        
        gateway = node.client.gateway_for(self.guild_id)
        await gateway.change_voice_state(self.guild_id, channel_id)
    
    
    async def change_node(self, node):
        """
        Changes the player's node
        
        Parameters
        ----------
        node ``SolarNode``
            The node the player is changed to.
        """
        await self._destroy()
        
        self.node = node
        
        await self._voice_update()
        
        current_track = self.get_current()
        if (current_track is not None):
            await node._send({
                LAVALINK_KEY_NODE_OPERATION: LAVALINK_KEY_NODE_OPERATION_PLAYER_PLAY,
                LAVALINK_KEY_GUILD_ID: str(self.guild_id),
                **current_track.un_pack(),
                LAVALINK_KEY_START_TIME: floor(self.position*1000.0),
                LAVALINK_KEY_PAUSE: (self._paused_track is current_track),
                LAVALINK_KEY_VOLUME: floor(self._volume*100.0),
            })
        
        
        modified_bands = None
        bands = self.get_bands()
        for band in range(LAVALINK_BAND_COUNT):
            gain = bands[band]
            if gain:
                if modified_bands is None:
                    modified_bands = []
                
                modified_bands.append((band, gain))
        
        
        if (modified_bands is not None):
            await self._set_gains(modified_bands)
    
    
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
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two players are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self is not other:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the player's hash value."""
        return self.guild_id
    
    
    @property
    def channel(self):
        """
        Returns the player's channel.
        
        Returns
        -------
        channel : `None`, ``ChannelVoiceBase``
        """
        channel_id = self.channel_id
        if channel_id:
            return CHANNELS.get(channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the player's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
