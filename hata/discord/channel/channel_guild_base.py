__all__ = ('ChannelGuildBase', 'ChannelGuildMainBase')

import re, warnings

from ...backend.utils import copy_docs
from ...backend.export import export, include

from ..permission import Permission, PermissionOverwrite
from ..permission.permission import PERMISSION_NONE, PERMISSION_ALL
from ..webhook import Webhook, WebhookRepr


from .channel_base import ChannelBase

Client = include('Client')

@export
class ChannelGuildBase(ChannelBase):
    """
    Base class for guild channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
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
    __slots__ = ('parent', 'guild', 'name', )
    
    ORDER_GROUP = 0
    
    @copy_docs(ChannelBase.__str__)
    def __str__(self):
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
                if self.permissions_for(user).can_view_channel:
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
        if self.guild is None:
            return default
        
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default

        for user in users:
            if user.name == name:
                return user
        
        guild = self.guild
        for user in users:
            nick = user.guild_profiles[guild]
            if nick is None:
                continue
            
            if nick == name:
                return user
        
        return default
    
    @copy_docs(ChannelBase.get_user_like)
    def get_user_like(self, name, default=None):
        guild = self.guild
        if guild is None:
            return default
        
        if not 1 < len(name) < 38:
            return default
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in guild.users.values():
                    if not self.permissions_for(user).can_view_channel:
                        continue
                    
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            
            if pattern.match(user.name) is not None:
                return user
            
            nick = user.guild_profiles[guild].nick
            if nick is None:
                continue
            
            if pattern.match(nick) is None:
                continue
            
            return user
        
        return default
    
    @copy_docs(ChannelBase.get_users_like)
    def get_users_like(self, name):
        result = []
        guild = self.guild
        if guild is None:
            return result
        
        if (not 1 < len(name) < 38):
            return result
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if not self.permissions_for(user).can_view_channel:
                        continue
                    
                    if user.discriminator == discriminator and user.name == name_:
                        result.append(user)
                        break
        
        if len(name) > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            
            nick = user.guild_profiles[guild].nick
            if nick is None:
                continue
            
            if pattern.match(nick) is None:
                continue
            
            result.append(user)
        
        return result
    
    @classmethod
    @copy_docs(ChannelBase._from_partial_data)
    def _from_partial_data(cls, data, channel_id, partial_guild):
        self = super(ChannelGuildBase, cls)._from_partial_data(data, channel_id, partial_guild)
        
        try:
            name = data['name']
        except KeyError:
            pass
        else:
            self.name = name
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        self.parent = None
        self.guild = partial_guild
        self.name = ''
        return self


@export
class ChannelGuildMainBase(ChannelGuildBase):
    """
    Base class for main guild channels not including thread channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    overwrites : `list` of ``PermissionOverwrite`` objects
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
    __slots__ = ('_cache_perm', 'overwrites', 'position', )
    
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
    
    def _init_parent_and_position(self, data, guild):
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
        self.guild = guild
        guild.channels[self.id] = self
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent = None
        else:
            parent = guild.channels[int(parent_id)]
        
        self.parent = parent
        
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
        guild = self.guild
        if guild is None:
            return
        
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent = None
        else:
            new_parent = guild.channels[int(new_parent_id)]
        
        position = data.get('position', 0)
        
        parent = self.parent
        if parent is new_parent:
            if self.position != position:
                self.position = position
        
        else:
            self.position = position
            self.parent = new_parent
    
    
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
        """
        guild = self.guild
        if guild is None:
            return
        
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent = None
        else:
            new_parent = guild.channels[int(new_parent_id)]
        
        position = data.get('position', 0)
        
        parent = self.parent
        if parent is new_parent:
            if self.position != position:
                old_attributes['position'] = self.position
                self.position = position
        else:
            old_attributes['parent'] = parent
            old_attributes['position'] = self.position
            
            self.position = position
            self.parent = parent
    
    
    def _permissions_for(self, user):
        """
        Base permission calculator method. Subclasses call this first, then apply their channel type related changes.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's permissions will be returned.
        
        Returns
        -------
        permission : ``Permission``
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        default_role = guild.roles.get(guild.id, None)
        if default_role is None:
            base = 0
        else:
            base = default_role.permissions
        
        try:
            guild_profile = user.guild_profiles[guild]
        except KeyError:
            if isinstance(user, (Webhook, WebhookRepr)) and user.channel is self:
                
                overwrites = self.overwrites
                if overwrites:
                    overwrite = overwrites[0]
                    
                    if overwrite.target_role is default_role:
                        base = (base&~overwrite.deny)|overwrite.allow
                
                return Permission(base)
            
            return PERMISSION_NONE
        
        roles = guild_profile.roles
        if (roles is not None):
            roles.sort()
            for role in roles:
                base |= role.permissions
        
        if Permission.can_administrator(base):
            return PERMISSION_ALL
        
        overwrites = self.overwrites
        if overwrites:
            overwrite = overwrites[0]
            
            if overwrite.target_role is default_role:
                base = (base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                overwrite_target_role = overwrite.target_role
                if (overwrite_target_role is not None):
                    if roles is None:
                        continue
                    
                    if overwrite_target_role not in roles:
                        continue
                
                else:
                    if overwrite.target_user_id != user.id:
                        continue
                
                base = (base&~overwrite.deny)|overwrite.allow
        
        return Permission(base)
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_ALL
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            result = PERMISSION_NONE
        
        return result
    
    @copy_docs(ChannelBase.cached_permissions_for)
    def cached_permissions_for(self, user):
        if not isinstance(user, Client):
            return self.permissions_for(user)
        
        cache_perm = self._cache_perm
        if cache_perm is None:
            self._cache_perm = cache_perm = {}
        else:
            try:
                return cache_perm[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        cache_perm[user.id] = permissions
        return permissions
    
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
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        default_role = guild.roles.get(guild.id, None)
        if default_role is None:
            base = 0
        else:
            base = default_role.permissions
        
        for role in sorted(roles):
            if role.guild is self:
                base |= role.permissions
        
        if Permission.can_administrator(base):
            return PERMISSION_ALL
        
        roles = set(roles)
        
        overwrites = self.overwrites
        if overwrites:
            overwrite = overwrites[0]
            
            if overwrite.target_role is default_role:
                base = (base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                overwrite_target_role = overwrite.target_role
                if (overwrite_target_role is None):
                    continue
                
                if overwrite_target_role not in roles:
                    continue
                
                base = (base&~overwrite.deny)|overwrite.allow
        
        return Permission(base)
    
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            result = PERMISSION_NONE
        
        return result
    
    
    def _parse_overwrites(self, data):
        """
        Parses the permission overwrites from the given data and returns them.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items) elements
            A list of permission overwrites' data.
        
        Returns
        -------
        overwrites : `list` of ``PermissionOverwrite``
        """
        overwrites = []
        try:
            overwrites_data = data['permission_overwrites']
        except KeyError:
            return overwrites
        
        if not overwrites_data:
            return overwrites
        
        default_role = self.guild.default_role
        
        for overwrite_data in overwrites_data:
            overwrite = PermissionOverwrite(overwrite_data)
            if overwrite.target_role is default_role:
                overwrites.insert(0, overwrite)
            else:
                overwrites.append(overwrite)
        
        return overwrites
    
    @property
    def category(self):
        """
        Deprecated, please use ``.parent`` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.category` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.parent` instead.',
            FutureWarning)
        
        return self.parent
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildMainBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._cache_perm = None
        self.overwrites = []
        self.position = 0
        return self
