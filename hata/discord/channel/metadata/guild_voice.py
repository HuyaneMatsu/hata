__all__ = ('ChannelMetadataGuildVoice',)

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import (
    PERMISSION_MASK_CONNECT, PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_TEXT_AND_STAGE_DENY,
    PERMISSION_VOICE_DENY_CONNECTION
)
from ...preconverters import preconvert_preinstanced_type

from .. import channel_types as CHANNEL_TYPES
from ..preinstanced import VideoQualityMode

from .guild_main_base import ChannelMetadataGuildMainBase
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
    region : `None`, ``VoiceRegion``
        The voice region of the channel.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    
    Class Attributes
    ----------------
    type : `int` = `CHANNEL_TYPES.guild_voice`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('video_quality_mode',)
    
    type = CHANNEL_TYPES.guild_voice
    
    @copy_docs(ChannelMetadataGuildVoiceBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataGuildVoiceBase._compare_attributes_to(self, other):
            return False
        
        if self.video_quality_mode is not other.video_quality_mode:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildVoiceBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildVoice, cls)._create_empty()
        
        self.video_quality_mode = VideoQualityMode.none
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildVoiceBase._update_attributes(self, data)
        
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildVoiceBase._difference_update_attributes(self, data)
        
        video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        if self.video_quality_mode is not video_quality_mode:
            old_attributes['video_quality_mode'] = self.video_quality_mode
            self.video_quality_mode = video_quality_mode
        
        return old_attributes
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildVoiceBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildVoice, cls)._precreate(keyword_parameters)
        
        try:
            video_quality_mode = keyword_parameters.pop('video_quality_mode')
        except KeyError:
            pass
        else:
            video_quality_mode = preconvert_preinstanced_type(
                video_quality_mode,
                'video_quality_mode',
                VideoQualityMode,
            )
            
            self.video_quality_mode = video_quality_mode
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildVoiceBase._to_data(self)
        
        video_quality_mode = self.video_quality_mode
        if (video_quality_mode is not VideoQualityMode.nonde):
            data['video_quality_mode'] = video_quality_mode.value
        
        return data


    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
