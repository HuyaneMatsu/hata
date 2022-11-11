__all__ = ('ChannelMetadataGuildVoice',)

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import (
    PERMISSION_MASK_CONNECT, PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_STAGE_DENY,
    PERMISSION_VOICE_DENY_CONNECTION
)

from .fields import (
    parse_nsfw, parse_video_quality_mode, put_nsfw_into, put_video_quality_mode_into, validate_nsfw,
    validate_video_quality_mode
)
from .preinstanced import VideoQualityMode

from .guild_voice_base import ChannelMetadataGuildVoiceBase


class ChannelMetadataGuildVoice(ChannelMetadataGuildVoiceBase):
    """
    Guild voice channel metadata.
    
    Attributes
    ----------
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `int`
        The channel's parent's identifier.
    name : `str`
        The channel's name.
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : ``VoiceRegion``
        The voice region of the channel.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    
    Class Attributes
    ----------------
    order_group: `int` = `2`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('nsfw', 'video_quality_mode',)
    
    @copy_docs(ChannelMetadataGuildVoiceBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildVoiceBase.__hash__(self)
        
        # nsfw
        hash_value ^= self.nsfw << 28
        
        # video_quality_mode
        hash_value ^= self.video_quality_mode.value << 11
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildVoiceBase._is_equal_same_type(self, other):
            return False
        
        # nsfw
        if self.nsfw != other.nsfw:
            return False
        
        # video_quality_mode
        if self.video_quality_mode is not other.video_quality_mode:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildVoiceBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildVoice, cls)._create_empty()
        
        self.nsfw = False
        self.video_quality_mode = VideoQualityMode.none
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildVoiceBase._update_attributes(self, data)
        
        # nsfw
        self.nsfw = parse_nsfw(data)
        
        # video_quality_mode
        self.video_quality_mode = parse_video_quality_mode(data)
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildVoiceBase._difference_update_attributes(self, data)
        
        # nsfw
        nsfw = parse_nsfw(data)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        # video_quality_mode
        video_quality_mode = parse_video_quality_mode(data)
        if self.video_quality_mode is not video_quality_mode:
            old_attributes['video_quality_mode'] = self.video_quality_mode
            self.video_quality_mode = video_quality_mode
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildVoiceBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # nsfw
        try:
            nsfw = keyword_parameters.pop('nsfw')
        except KeyError:
            pass
        else:
            self.nsfw = validate_nsfw(nsfw)
        
        # video_quality_mode
        try:
            video_quality_mode = keyword_parameters.pop('video_quality_mode')
        except KeyError:
            pass
        else:
            self.video_quality_mode = validate_video_quality_mode(video_quality_mode)
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildVoiceBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # nsfw
        put_nsfw_into(self.nsfw, data, defaults)
        
        # video_quality_mode
        put_video_quality_mode_into(self.video_quality_mode, data, defaults)
        
        return data
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_STAGE_DENY
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_STAGE_DENY
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
