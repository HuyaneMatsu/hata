__all__ = ('ChannelGuildBase', 'ChannelGuildMainBase')

import re, warnings

from ...backend.utils import copy_docs
from ...backend.export import export, include

from ..permission import Permission, PermissionOverwriteTargetType
from ..permission.permission import PERMISSION_NONE, PERMISSION_ALL, PERMISSION_MASK_ADMINISTRATOR, \
    PERMISSION_MASK_VIEW_CHANNEL
from ..core import GUILDS, CHANNELS
from ..user import ClientUserBase

PERMISSION_OVERWRITE_TYPE_ROLE = PermissionOverwriteTargetType.role
PERMISSION_OVERWRITE_TYPE_USER = PermissionOverwriteTargetType.user

from .channel_base import ChannelBase

Client = include('Client')
create_partial_guild_from_id = include('create_partial_guild_from_id')

@export
class ChannelGuildBase(ChannelBase):
    """
    Base class for guild channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _permission_cache : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `int`
        The channel's parent's identifier.
    guild_id : `int`
        The channel's guild's identifier.
    name : `str`
        The channel's name.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('_permission_cache', 'parent_id', 'guild_id', 'name', )
    
    ORDER_GROUP = 0
    
    @copy_docs(ChannelBase._get_processed_name)
    def _get_processed_name(self):
        return self.name
    
    
    @property
    @copy_docs(ChannelBase.users)
    def users(self):
        return list(self.iter_users())
    
    
    @copy_docs(ChannelBase.iter_users)
    def iter_users(self):
        guild = self.guild
        if (guild is not None):
            for user in guild.users.values():
                if self.permissions_for(user)&PERMISSION_MASK_VIEW_CHANNEL:
                    yield user
    
    
    @property
    @copy_docs(ChannelBase.clients)
    def clients(self):
        guild = self.guild
        if guild is None:
            return []
        
        return guild.clients
    
    
    @copy_docs(ChannelBase.get_user)
    def get_user(self, name, default=None):
        name_length = len(name)
        if (name_length < 1) or (name_length > 32):
            return
        
        if self.guild is None:
            return default
        
        users = self.users
        
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
        
        guild_id = self.guild_id
        
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
    
    
    @copy_docs(ChannelBase.get_user_like)
    def get_user_like(self, name, default=None):
        name_length = len(name)
        if (name_length < 1) or (name_length > 37):
            return
        
        guild = self.guild
        if guild is None:
            return default
        
        if (name_length > 6) and (name[-5] == '#'):
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in guild.users.values():
                    if not self.permissions_for(user)&PERMISSION_MASK_VIEW_CHANNEL:
                        continue
                    
                    if (user.discriminator == discriminator) and (user.name == name_):
                        return user
        
        if (name_length > 32):
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        guild_id = guild.id
        
        for user in guild.users.values():
            if not self.permissions_for(user)&PERMISSION_MASK_VIEW_CHANNEL:
                continue
            
            if pattern.match(user.name) is not None:
                return user
            
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            nick = guild_profile.nick
            if nick is None:
                continue
            
            if pattern.match(nick) is None:
                continue
            
            return user
        
        return default
    
    
    @copy_docs(ChannelBase.get_users_like)
    def get_users_like(self, name):
        result = []
        
        name_length = len(name)
        if (name_length < 1) or (name_length > 37):
            return result
        
        guild = self.guild
        if guild is None:
            return result
        
        users = self.users
        
        if (name_length > 6) and (name[-5] == '#'):
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if not self.permissions_for(user)&PERMISSION_MASK_VIEW_CHANNEL:
                        continue
                    
                    if (user.discriminator == discriminator) and (user.name == name_):
                        result.append(user)
                        break
        
        if name_length > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        
        guild_id = guild.id
        for user in guild.users.values():
            if not self.permissions_for(user)&PERMISSION_MASK_VIEW_CHANNEL:
                continue
            
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            nick = guild_profile.nick
            if nick is None:
                continue
            
            if pattern.match(nick) is None:
                continue
            
            result.append(user)
        
        return result
    
    
    @classmethod
    @copy_docs(ChannelBase._from_partial_data)
    def _from_partial_data(cls, data, channel_id, guild_id):
        self = super(ChannelGuildBase, cls)._from_partial_data(data, channel_id, guild_id)
        
        try:
            name = data['name']
        except KeyError:
            pass
        else:
            self.name = name
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, guild_id):
        self = super(ChannelGuildBase, cls)._create_empty(channel_id, channel_type, guild_id)
        self._permission_cache = None
        self.parent_id = 0
        self.guild_id = guild_id
        self.name = ''
        return self
    
    
    @property
    def guild(self):
        """
        Returns the channel's guild.
        
        Returns
        -------
        guild : ``Guild`` or `None`
        """
        guild_id = self.guild_id
        if guild_id:
            return create_partial_guild_from_id(guild_id)
    
    
    @property
    def parent(self):
        """
        Returns the channel's parent channel.
        
        Returns
        -------
        parent : `None` or ``ChannelGuildBase``
        """
        parent_id = self.parent_id
        if parent_id:
            return CHANNELS.get(parent_id, None)
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        self.permission_overwrites.clear()
        self._permission_cache = None


    @copy_docs(ChannelBase.cached_permissions_for)
    def cached_permissions_for(self, user):
        if not isinstance(user, Client):
            return self.permissions_for(user)
        
        permission_cache = self._permission_cache
        if permission_cache is None:
            self._permission_cache = permission_cache = {}
        else:
            try:
                return permission_cache[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        permission_cache[user.id] = permissions
        return permissions


@export
class ChannelGuildMainBase(ChannelGuildBase):
    """
    Base class for main guild channels not including thread channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    parent_id : `int`
        The channel's parent's identifier.
    guild_id : `int`
        The channel's guild's identifier.
    name : `str`
        The channel's name.
    _permission_cache : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('permission_overwrites', 'position', )
    
    def __gt__(self, other):
        """
        Whether this channel has higher (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP > other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position > other.position:
                    return True
                
                if self.position == other.position:
                    if self.id > other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id > other.id
        
        return NotImplemented
    
    def __ge__(self, other):
        """
        Whether this channel is same as the other one, or has higher (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP > other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position > other.position:
                    return True
                
                if self.position == other.position:
                    if self.id >= other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id > other.id
        
        return NotImplemented
    
    def __le__(self, other):
        """
        Whether this channel is same as the other one, or has lower (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP < other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position < other.position:
                    return True
                
                if self.position == other.position:
                    if self.id <= other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id < other.id
        
        return NotImplemented
    
    def __lt__(self, other):
        """
        Whether this channel has lower (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP < other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position < other.position:
                    return True
                
                if self.position == other.position:
                    if self.id < other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id < other.id
        
        return NotImplemented
    
    
    def _init_parent_and_position(self, data, guild_id):
        """
        Initializes the `.parent` and the `.position` of the channel. If a channel is under the ``Guild``,
        and not in a parent (parent channels are all like these), then their `.parent` is the ``Guild`` itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild_id = guild_id
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            guild.channels[self.id] = self
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent_id = 0
        else:
            parent_id = int(parent_id)
        
        self.parent_id = parent_id
        
        self.position = data.get('position', 0)
    
    
    def _set_parent_and_position(self, data):
        """
        Similar to the ``._init_parent_and_position`` method, but this method applies the changes too, so moves the channel
        between categories and moves the channel inside of the parent too, to keep the order.
        
        Called from `._update_no_return` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        """
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent_id = 0
        else:
            new_parent_id = int(new_parent_id)
        
        position = data.get('position', 0)
        
        parent_id = self.parent_id
        if parent_id is new_parent_id:
            if self.position != position:
                self.position = position
        
        else:
            self.position = position
            self.parent_id = new_parent_id
    
    
    def _update_parent_and_position(self, data, old_attributes):
        """
        Acts same as ``._set_parent_and_position``, but it sets the modified attributes' previous value to
        `old_attributes`.
        
        Called from `._update` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        old_attributes : `dict` of (`str`, `Any`) items
            `attribute-name` - `old-value` relations containing the changes of caused by the update.
        
            The method may add the following items to the dictionary:
            +---------------+-----------------------------------+
            | Keys          | Values                            |
            +===============+===================================+
            | parent_id     | `int`                             |
            +---------------+-----------------------------------+
            | position      | `int`                             |
            +---------------+-----------------------------------+
        """
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent_id = 0
        else:
            new_parent_id = int(new_parent_id)
        
        position = data.get('position', 0)
        
        parent_id = self.parent_id
        if parent_id is new_parent_id:
            if self.position != position:
                old_attributes['position'] = self.position
                self.position = position
        else:
            old_attributes['parent_id'] = parent_id
            old_attributes['position'] = self.position
            
            self.position = position
            self.parent_id = parent_id
    
    
    def _permissions_for(self, user):
        """
        Base permission calculator method. Subclasses call this first, then apply their channel type related changes.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        """
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_ALL
        
        if not isinstance(user, ClientUserBase):
            if  user.guild_id in guild.channels:
                role_everyone = guild.roles.get(guild_id, None)
                if role_everyone is None:
                    permissions = PERMISSION_NONE
                else:
                    permissions = role_everyone.permissions
                
                # Apply everyone's if applicable
                permission_overwrites = self.permission_overwrites
                try:
                    permission_overwrite_everyone = permission_overwrites[guild_id]
                except KeyError:
                    pass
                else:
                    permissions &= ~permission_overwrite_everyone.deny
                    permissions |= permission_overwrite_everyone.allow
            
                return permissions
            else:
                return PERMISSION_NONE
        
        # Are we in the guild?
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            return PERMISSION_NONE
        
        # Apply everyone's
        role_everyone = guild.roles.get(guild_id, None)
        if role_everyone is None:
            permissions = 0
        else:
            permissions = role_everyone.permissions
        
        roles = guild_profile.roles
        
        # Apply permissions of each role of the user.
        if (roles is not None):
            for role in roles:
                permissions |= role.permissions
        
        # Apply everyone's if applicable
        permission_overwrites = self.permission_overwrites
        try:
            permission_overwrite_everyone = permission_overwrites[guild_id]
        except KeyError:
            pass
        else:
            permissions &= ~permission_overwrite_everyone.deny
            permissions |= permission_overwrite_everyone.allow
        
        # Apply role overwrite
        allow = 0
        deny = 0
        
        if (roles is not None):
            for role in roles:
                try:
                    permission_overwrite_role = permission_overwrites[role.id]
                except KeyError:
                    pass
                else:
                    allow |= permission_overwrite_role.allow
                    deny |= permission_overwrite_role.deny
        
        permissions &= ~deny
        permissions |= allow
        
        # Apply user specific
        try:
            permission_overwrite_user = permission_overwrites[user.id]
        except KeyError:
            pass
        else:
            permissions &= ~permission_overwrite_user.deny
            permissions |= permission_overwrite_user.allow
        
        # Are we admin?
        if permissions&PERMISSION_MASK_ADMINISTRATOR:
            return PERMISSION_ALL
        
        return Permission(permissions)
    
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        result = self._permissions_for(user)
        if not result&PERMISSION_MASK_VIEW_CHANNEL:
            result = PERMISSION_NONE
        
        return result
    
    
    def _permissions_for_roles(self, roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles. This method is called
        first by subclasses to apply their own related permissions on it.
        
        Parameters
        ----------
        roles : `tuple` of ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        guild_id = guild.id
        role_everyone = guild.roles.get(guild_id, None)
        if role_everyone is None:
            permissions = 0
        else:
            permissions = role_everyone.permissions
        
        roles = sorted(roles)
        for role in roles:
            if role.guild_id == guild_id:
                permissions |= role.permissions
        
        if permissions&PERMISSION_MASK_ADMINISTRATOR:
            return PERMISSION_ALL
        
        permission_overwrites = self.permission_overwrites
        try:
            permission_overwrite_everyone = permission_overwrites[guild_id]
        except KeyError:
            pass
        else:
            permissions &= ~permission_overwrite_everyone.deny
            permissions |= permission_overwrite_everyone.allow
        
        allow = 0
        deny = 0
        
        for role in roles:
            try:
                permission_overwrite_role = permission_overwrites[role.id]
            except KeyError:
                pass
            else:
                allow |= permission_overwrite_role.allow
                deny |= permission_overwrite_role.deny
        
        permissions &= ~deny
        permissions |= allow
        
        return Permission(permissions)
    
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        permissions = self._permissions_for_roles(roles)
        if not permissions&PERMISSION_MASK_VIEW_CHANNEL:
            permissions = PERMISSION_NONE
        
        return permissions
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, guild_id):
        self = super(ChannelGuildMainBase, cls)._create_empty(channel_id, channel_type, guild_id)
        self.permission_overwrites = {}
        self.position = 0
        return self
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        self.permission_overwrites.clear()
        self._permission_cache = None
        
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            try:
                del guild.channels[self.id]
            except KeyError:
                pass
