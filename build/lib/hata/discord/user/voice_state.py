__all__ = ('VoiceState', )

from datetime import datetime

from ...backend.export import include

from ..utils import timestamp_to_datetime
from ..core import CHANNELS, GUILDS

from .utils import create_partial_user_from_id

create_partial_role_from_id = include('create_partial_role_from_id')

class VoiceState:
    """
    Represents a user at a ``ChannelVoice``.
    
    Attributes
    ----------
    _cache_user : ``ClientUserBase``
        The voice state's respective user.
    channel_id : `int`
        The channel's identifier to where the user is connected to.
    deaf : `bool`
        Whether the user is deafen.
    guild_id : `int`
        The guild's identifier where the user is connected to.
    is_speaker : `bool`
        Whether the user is suppressed inside of the voice channel.
        
        If the channel is a ``ChannelVoice``, it is always `False`, meanwhile it ``ChannelStage`` it can vary.
    
    mute : `bool`
        Whether the user is muted.
    requested_to_speak_at : `None` or `datetime`
        When the user requested to speak.
        
        Only applicable if the user is connected to a ``ChannelStage`` instance.
    
    self_deaf : `bool`
        Whether the user muted everyone else.
    self_mute : `bool`
        Whether the user muted itself.
    self_stream : `bool`
        Whether the user screen shares with the go live option.
    self_video : `bool`
        Whether the user sends video from a camera source.
    session_id : `str``
        The user's voice session id.
    user_id : `int`
        The voice state's respective user's identifier.
    """
    __slots__ = ('_cache_user', 'channel_id', 'deaf', 'guild_id', 'is_speaker', 'mute', 'requested_to_speak_at',
        'self_deaf', 'self_mute', 'self_stream', 'self_video', 'session_id', 'user_id')
    
    def __new__(cls, data, guild_id):
        """
        Creates a ``VoiceState`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        guild_id : `int`
            The voice state's guild's identifier.
        """
        channel_id = data.get('channel_id', None)
        if channel_id is None:
            return
        
        channel_id = int(channel_id)
        
        user_id = int(data['user_id'])
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            guild = None
        else:
            try:
                return guild.voice_states[user_id]
            except KeyError:
                pass
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.user_id = user_id
        self.session_id = data['session_id']
        self.mute = data['mute']
        self.deaf = data['deaf']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.self_stream = data.get('self_stream', False)
        self.self_video = data['self_video']
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = timestamp_to_datetime(requested_to_speak_at)
        
        self.is_speaker = not data.get('suppress', False)
        
        self.requested_to_speak_at = requested_to_speak_at
        
        if (guild is not None):
            guild.voice_states[user_id] = self
        
        return self
    
    
    @property
    def user(self):
        """
        Returns the voice state's user.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        user = self._cache_user
        if (user is None):
            user = create_partial_user_from_id(self.user_id)
            self._cache_user = user
        
        return user
    
    def _set_cache_user(self, user):
        """
        Sets the cached user of the voice state.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The respective user of the voice state.
        """
        self._cache_user = user
    
    @property
    def channel(self):
        """
        Returns the voice state's channel, where the user is connected to.
        
        Returns
        -------
        channel : `None` or ``ChannelVoiceBase``
        """
        channel_id = self.channel_id
        if channel_id:
            return CHANNELS[channel_id]
    
    
    @property
    def guild(self):
        """
        Returns the voice state's respective guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        channel = self.channel
        if (channel is not None):
            return channel.guild
    
    
    def _update_channel(self, data):
        """
        Updates the voice state's channel.
        
        Returns
        -------
        old_channel_id : `int`
            The voice state's old channel's identifier.
        new_channel_id : `int`
            The voice state's new channel's identifier.
        """
        channel_id = data.get('channel_id', None)
        if channel_id is None:
            channel_id = 0
            
            try:
                guild = GUILDS[self.guild_id]
            except KeyError:
                pass
            else:
                try:
                    del guild.voice_states[self.user_id]
                except KeyError:
                    pass
        else:
            channel_id = int(channel_id)
        
        old_channel_id = self.channel_id
        self.channel_id = channel_id
        
        return old_channel_id, channel_id
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the voice state and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | is_speaker            | `bool`                |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None` or `datetime`  |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        """
        old_attributes = {}
        
        deaf = data['deaf']
        if self.deaf != deaf:
            old_attributes['deaf'] = self.deaf
            self.deaf = deaf
        
        mute = data['mute']
        if self.mute != mute:
            old_attributes['mute'] = self.mute
            self.mute = mute
        
        self_deaf = data['self_deaf']
        if self.self_deaf != self_deaf:
            old_attributes['self_deaf'] = self.self_deaf
            self.self_deaf = self_deaf
        
        self_video = data['self_video']
        if self.self_video != self_video:
            old_attributes['self_video'] = self.self_video
            self.self_video = self_video
        
        self_stream = data.get('self_stream', False)
        if self.self_stream != self_stream:
            old_attributes['self_stream'] = self.self_stream
            self.self_stream = self_stream
        
        self_mute = data['self_mute']
        if self.self_mute != self_mute:
            old_attributes['self_mute'] = self.self_mute
            self.self_mute = self_mute
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = timestamp_to_datetime(requested_to_speak_at)
        
        if self.requested_to_speak_at != requested_to_speak_at:
            old_attributes['requested_to_speak_at'] = self.requested_to_speak_at
            self.requested_to_speak_at = requested_to_speak_at
        
        is_speaker = not data.get('suppress', False)
        if self.is_speaker != is_speaker:
            old_attributes['is_speaker'] = self.is_speaker
            self.is_speaker = is_speaker
        
        return old_attributes
    
    
    def _update_attributes(self, data):
        """
        Updates the voice state with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        """
        self.deaf = data['deaf']
        self.mute = data['mute']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.self_stream = data.get('self_stream', False)
        self.self_video = data['self_video']
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = timestamp_to_datetime(requested_to_speak_at)
        
        self.requested_to_speak_at = requested_to_speak_at
        
        self.is_speaker = not data.get('suppress', False)
    
    def __repr__(self):
        """Returns the voice state's representation."""
        return (
            f'<{self.__class__.__name__} user_id={self.user_id}, guild_id={self.guild_id}, '
            f'channel_id={self.channel_id}>'
        )
