__all__ = ('ChannelMetadataGuildBase',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import copy_docs, export, include

from ...core import GUILDS
from ...permission.permission import PERMISSION_MASK_VIEW_CHANNEL

from .fields import parse_name, parse_parent_id, put_name_into, put_parent_id_into, validate_name, validate_parent_id

from .base import ChannelMetadataBase


Client = include('Client')


@export
class ChannelMetadataGuildBase(ChannelMetadataBase):
    """
    Base guild channel metadata type.
    
    Attributes
    ----------
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    name : `str`
        The channel's name.
    parent_id : `int`
        The channel's parent's identifier.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('_cache_permission', 'name', 'parent_id')
    
    
    def __new__(
        cls,
        *,
        name = ...,
        parent_id = ...,
    ):
        """
        Creates a new guild base channel metadata from the given parameters.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # parent_id
        if parent_id is ...:
            parent_id = 0
        else:
            parent_id = validate_parent_id(parent_id)
        
        # Construct
        self = object.__new__(cls)
        self._cache_permission = None
        self.name = name
        self.parent_id = parent_id
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
        )
    
    
    @copy_docs(ChannelMetadataBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataBase.__hash__(self)
        
        # name
        name = self.name
        if name:
            hash_value ^= hash(name)
        
        # parent_id
        hash_value ^= self.parent_id
        
        return hash_value
    
    
    @classmethod
    @copy_docs(ChannelMetadataBase.from_data)
    def from_data(cls, data):
        self = super(ChannelMetadataGuildBase, cls).from_data(data)
        
        self._cache_permission = None
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        
        # name
        if self.name != other.name:
            return False
        
        # parent_id
        if self.parent_id != other.parent_id:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # name
        put_name_into(self.name, data, defaults)
        
        # parent_id
        put_parent_id_into(self.parent_id, data, defaults)
        
        return data
    
    
    @classmethod
    @copy_docs(ChannelMetadataBase._from_partial_data)
    def _from_partial_data(cls, data):
        self = super(ChannelMetadataGuildBase, cls)._from_partial_data(data)
        
        if (data is not None):
            name = data.get('name', None)
            if (name is not None):
                self.name = name
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataBase._update_attributes(self, data)
        
        self._cache_permission = None
        
        # name
        self.name = parse_name(data)
        
        # parent_id
        self.parent_id = parse_parent_id(data)
        

    @copy_docs(ChannelMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataBase._difference_update_attributes(self, data)
        
        self._cache_permission = None
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # parent_id
        parent_id = parse_parent_id(data)
        if self.parent_id != parent_id:
            old_attributes['parent_id'] = self.parent_id
            self.parent_id = parent_id
        
        return old_attributes
    
    
    @classmethod
    @copy_docs(ChannelMetadataBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildBase, cls)._create_empty()
        
        self._cache_permission = None
        self.parent_id = 0
        self.name = ''
        
        return self
    
    
    @copy_docs(ChannelMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new._cache_permission = None
        new.parent_id = self.parent_id
        new.name = self.name
        return new
    
    
    def copy_with(
        self,
        *,
        name = ...,
        parent_id = ...,
    ):
        """
        Copies the guild base channel metadata with the given fields.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
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
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # parent_id
        if parent_id is ...:
            parent_id = self.parent_id
        else:
            parent_id = validate_parent_id(parent_id)
        
        # Construct
        self = object.__new__(type(self))
        self._cache_permission = None
        self.name = name
        self.parent_id = parent_id
        return self
    
    
    @copy_docs(ChannelMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
        )
    
    
    @copy_docs(ChannelMetadataBase._get_users)
    def _get_users(self, channel_entity):
        return [*self._iter_users(channel_entity)]
    
    
    @copy_docs(ChannelMetadataBase._iter_users)
    def _iter_users(self, channel_entity):
        guild = channel_entity.guild
        if (guild is not None):
            for user in guild.users.values():
                if self._get_permissions_for(channel_entity, user) & PERMISSION_MASK_VIEW_CHANNEL:
                    yield user
    
    
    @copy_docs(ChannelMetadataBase._get_clients)
    def _get_clients(self, channel_entity):
        guild = channel_entity.guild
        if guild is None:
            return []
        
        return guild.clients
    
    
    @copy_docs(ChannelMetadataBase._get_cached_permissions_for)
    def _get_cached_permissions_for(self, channel_entity, user):
        if not isinstance(user, Client):
            return self._get_permissions_for(channel_entity, user)
        
        permission_cache = self._cache_permission
        if permission_cache is None:
            self._cache_permission = permission_cache = {}
        else:
            try:
                return permission_cache[user.id]
            except KeyError:
                pass
        
        permissions = self._get_permissions_for(channel_entity, user)
        permission_cache[user.id] = permissions
        return permissions
    
    
    @copy_docs(ChannelMetadataBase._invalidate_cache_permission)
    def _invalidate_cache_permission(self):
        self._cache_permission = None
