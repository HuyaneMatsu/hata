__all__ = ('VoiceState', )

from datetime import datetime

from ...backend.export import include

from ..utils import timestamp_to_datetime

from .utils import create_partial_user_from_id

create_partial_role_from_id = include('create_partial_role_from_id')

class VoiceState:
    """
    Represents a user at a ``ChannelVoice``.
    
    Attributes
    ----------
    channel : ``ChannelVoice``
        The channel to where the user is connected to.
    deaf : `bool`
        Whether the user is deafen.
    is_speaker : `bool`
        Whether the user is suppressed inside of the voice channel.
        
        If the channel is a ``ChannelVoice``, it is always `False`, meanwhile it ``ChannelStage`` it can vary.
    mute : `bool`
        Whether the user is muted.
    requested_to_speak_at : `None` or `datetime`
        When the user requested to speak.
        
        Only applicable for ``ChannelStage``-s.
    self_deaf : `bool`
        Whether the user muted everyone else.
    self_mute : `bool`
        Whether the user muted itself.
    self_stream : `bool`
        Whether the user screen shares with the go live option.
    self_video : `bool`
        Whether the user sends video from a camera source.
    session_id : `str`
        The user's voice session id.
    user : ``User`` or ``Client``
        The voice state's respective user. If user caching is disabled it will be set as a partial user.
    """
    __slots__ = ('channel', 'deaf', 'is_speaker', 'mute', 'requested_to_speak_at', 'self_deaf', 'self_mute', 'self_stream',
        'self_video', 'session_id', 'user', )
    
    def __init__(self, data, channel):
        """
        Creates a ``VoiceState`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoiceBase``
            The channel of the voice state.
        """
        self.channel = channel
        self.user = create_partial_user_from_id(int(data['user_id']))
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
    
    @property
    def guild(self):
        """
        Returns the voice state's respective guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return self.channel.guild
    
    def _difference_update_attributes(self, data, channel):
        """
        Updates the voice state and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoice``
            The channel of the voice state.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | channel               | ``ChannelVoice``      |
        +-----------------------+-----------------------+
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
        
        if (self.channel is not channel):
            old_attributes['channel'] = self.channel
            self.channel = channel
        
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
    
    def _update_attributes(self, data, channel):
        """
        Updates the voice state with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoice``
            The channel of the voice state.
        """
        self.channel = channel
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
        return f'<{self.__class__.__name__} user={self.user.full_name!r}, channel={self.channel!r}>'
