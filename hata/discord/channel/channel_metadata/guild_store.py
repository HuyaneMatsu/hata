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
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    name : `str`
        The channel's name.
    parent_id : `int`
        The channel's parent's identifier.
    permission_overwrites :`None`,  `dict` of (`int`, ``PermissionOverwrite``) items
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
    
    
    def __new__(
        cls,
        *,
        name = ...,
        nsfw = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
    ):
        """
        Creates a new guild store channel metadata from the given parameters.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The channel's name.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = validate_nsfw(nsfw)
        
        # Construct
        self = ChannelMetadataGuildMainBase.__new__(
            cls,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
        )
        self.nsfw = nsfw
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            name = keyword_parameters.pop('name', ...),
            nsfw = keyword_parameters.pop('nsfw', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
        )
    
    
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
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy)
    def copy(self):
        new = ChannelMetadataGuildMainBase.copy(self)
        new.nsfw = self.nsfw
        return new
    
    
    def copy_with(
        self,
        *,
        name = ...,
        nsfw = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
    ):
        """
        Copies the guild store channel metadata from the given fields.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The channel's name.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # nsfw
        if nsfw is ...:
            nsfw = self.nsfw
        else:
            nsfw = validate_nsfw(nsfw)
        
        # Construct
        new = ChannelMetadataGuildMainBase.copy_with(
            self,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
        )
        new.nsfw = nsfw
        return new
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            name = keyword_parameters.pop('name', ...),
            nsfw = keyword_parameters.pop('nsfw', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
        )
    
    
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
    
    
    @copy_docs(ChannelMetadataGuildMainBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildMainBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        put_nsfw_into(self.nsfw, data, defaults)
        
        return data
