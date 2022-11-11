__all__ = ('ChannelMetadataGuildStore', )

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_TEXT_AND_VOICE_DENY

from .fields import parse_nsfw, put_nsfw_into, validate_nsfw

from .guild_main_base import ChannelMetadataGuildMainBase


class ChannelMetadataGuildStore(ChannelMetadataGuildMainBase):
    """
    Guild store channel metadata.
    
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
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('nsfw',)
    
    @copy_docs(ChannelMetadataGuildMainBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildMainBase.__hash__(self)
        
        # nsfw
        hash_value ^= self.nsfw << 28
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildMainBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildMainBase._is_equal_same_type(self, other):
            return False
        
        # nsfw
        if self.nsfw != other.nsfw:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_display_name)
    def _get_display_name(self):
        return self.name.lower()
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildStore, cls)._create_empty()
        
        self.nsfw = False
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        # nsfw
        self.nsfw = parse_nsfw(data)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        # nsfw
        nsfw = parse_nsfw(data)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # store channels do not have text and voice related permissions
        result &= PERMISSION_TEXT_AND_VOICE_DENY
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # store channels do not have text and voice related permissions
        result &= PERMISSION_TEXT_AND_VOICE_DENY
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # nsfw
        try:
            nsfw = keyword_parameters.pop('nsfw')
        except KeyError:
            pass
        else:
            self.nsfw = validate_nsfw(nsfw)
    
    
    @copy_docs(ChannelMetadataGuildMainBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildMainBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        put_nsfw_into(self.nsfw, data, defaults)
        
        return data
