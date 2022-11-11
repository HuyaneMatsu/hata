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
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
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
    __slots__ = ('_permission_cache', 'name', 'parent_id')
    
    
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
        
        self._permission_cache = None
        
        return self
    

    @copy_docs(ChannelMetadataBase._delete)
    def _delete(self, channel_entity, client):
        self.permission_overwrites.clear()
        self._permission_cache = None
    
    
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
        
        self._permission_cache = None
        
        # name
        self.name = parse_name(data)
        
        # parent_id
        self.parent_id = parse_parent_id(data)
        

    @copy_docs(ChannelMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataBase._difference_update_attributes(self, data)
        
        self._permission_cache = None
        
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
        
        self._permission_cache = None
        self.parent_id = 0
        self.name = ''
        
        return self
    
    
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
    
    
    @copy_docs(ChannelMetadataBase._get_user)
    def _get_user(self, channel_entity, name, default):
        name_length = len(name)
        if (name_length < 1) or (name_length > 32):
            return
        
        guild_id = channel_entity.guild_id
        if guild_id not in GUILDS:
            return
        
        users = self._get_users(channel_entity)
        
        if (name_length > 6) and (name[-5] == '#'):
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if (user.discriminator == discriminator) and (user.name == name_):
                        return user
        
        if name_length > 32:
            return default

        for user in users:
            if user.name == name:
                return user
        
        for user in users:
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            nick = guild_profile.nick
            if nick is None:
                continue
            
            if nick == name:
                return user
        
        return default
    
    
    @copy_docs(ChannelMetadataBase._get_user_like)
    def _get_user_like(self, channel_entity, name, default):
        name_length = len(name)
        if (name_length < 1) or (name_length > 37):
            return
        
        guild_id = channel_entity.guild_id
        if guild_id not in GUILDS:
            return
        
        users = self._get_users(channel_entity)
        
        if (name_length > 6) and (name[-5] == '#'):
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if (user.discriminator == discriminator) and (user.name == name_):
                        return user
        
        if (name_length > 32):
            return default
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        for user in users:
            if pattern.search(user.name) is not None:
                return user
            
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            nick = guild_profile.nick
            if nick is None:
                continue
            
            if pattern.search(nick) is None:
                continue
            
            return user
        
        return default


    @copy_docs(ChannelMetadataBase._get_users_like)
    def _get_users_like(self, channel_entity, name):
        result = []
        
        name_length = len(name)
        if (name_length < 1) or (name_length > 37):
            return result
        
        guild_id = channel_entity.guild_id
        if guild_id not in GUILDS:
            return
        
        users = self._get_users(channel_entity)
        
        if (name_length > 6) and (name[-5] == '#'):
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if (user.discriminator == discriminator) and (user.name == name_):
                        result.append(user)
                        break
        
        if name_length > 32:
            return result
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        for user in users:
            if pattern.search(user.name) is not None:
                result.append(user)
                continue
            
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            nick = guild_profile.nick
            if nick is None:
                continue
            
            if pattern.search(nick) is None:
                continue
            
            result.append(user)
        
        return result
    
    
    @copy_docs(ChannelMetadataBase._get_cached_permissions_for)
    def _get_cached_permissions_for(self, channel_entity, user):
        if not isinstance(user, Client):
            return self._get_permissions_for(channel_entity, user)
        
        permission_cache = self._permission_cache
        if permission_cache is None:
            self._permission_cache = permission_cache = {}
        else:
            try:
                return permission_cache[user.id]
            except KeyError:
                pass
        
        permissions = self._get_permissions_for(channel_entity, user)
        permission_cache[user.id] = permissions
        return permissions
    
    
    @copy_docs(ChannelMetadataBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            pass
        else:
            self.name = validate_name(name)
        
        # parent_id
        try:
            parent_id = keyword_parameters.pop('parent_id')
        except KeyError:
            pass
        else:
            self.parent_id = validate_parent_id(parent_id)
        
        return self
    
    
    @copy_docs(ChannelMetadataBase._invalidate_permission_cache)
    def _invalidate_permission_cache(self):
        self._permission_cache = None
