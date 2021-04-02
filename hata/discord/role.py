# -*- coding: utf-8 -*-
__all__ = ('PermissionOverwrite', 'Role', 'cr_p_overwrite_object', 'cr_p_role_object', )

from ..backend.utils import DOCS_ENABLED

from ..env import API_VERSION

from .bases import DiscordEntity
from .client_core import ROLES
from .utils import random_id, DATETIME_FORMAT_CODE
from .color import Color
from .permission import Permission, PERMISSION_NONE
from .user import create_partial_user
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_color, preconvert_int, preconvert_bool, \
    preconvert_flag
from .preinstanced import RoleManagerType

from . import rate_limit as module_rate_limit, user as module_user

create_partial_integration = NotImplemented

ROLE_MANAGER_TYPE_NONE        = RoleManagerType.none
ROLE_MANAGER_TYPE_UNSET       = RoleManagerType.unset
ROLE_MANAGER_TYPE_UNKNOWN     = RoleManagerType.unknown
ROLE_MANAGER_TYPE_BOT         = RoleManagerType.bot
ROLE_MANAGER_TYPE_BOOSTER     = RoleManagerType.booster
ROLE_MANAGER_TYPE_INTEGRATION = RoleManagerType.integration

if API_VERSION in (6, 7):
    PERMISSION_KEY = 'permissions_new'
    PERMISSION_ALLOW_KEY = 'allow_new'
    PERMISSION_DENY_KEY = 'deny_new'
    
    PERM_OW_TYPE_ROLE = 'role'
    PERM_OW_TYPE_USER = 'member'
    
    def get_perm_ow_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `str`
        """
        return data['type']
else:
    PERMISSION_KEY = 'permissions'
    PERMISSION_ALLOW_KEY = 'allow'
    PERMISSION_DENY_KEY = 'deny'
    
    PERM_OW_TYPE_ROLE = 0
    PERM_OW_TYPE_USER = 1
    
    def get_perm_ow_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `int`
        """
        return int(data['type'])


def create_partial_role(role_id):
    """
    Creates a partial role from the given `role_id`. If the role already exists returns that instead.
    
    Parameters
    ----------
    role_id : `int`
        The unique identifier number of the role.
    
    Returns
    -------
    role : ``Role``
    """
    try:
        return ROLES[role_id]
    except KeyError:
        pass
    
    role = object.__new__(Role)
    role.id = role_id
    
    role.color = Color()
    role.guild = None
    role.separated = False
    # id is set up
    role.manager_type = ROLE_MANAGER_TYPE_NONE
    role.manager_id = 0
    role.mentionable = False
    role.name = ''
    role.permissions = PERMISSION_NONE
    role.position = 1 # 0 is default role, so we go for 1
    
    ROLES[role_id] = role
    
    return role


class Role(DiscordEntity, immortal=True):
    """
    Represents a Discord guild's role.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the role.
    color : ``Color``
        The role's color. If the color equals to ``Color(0)``, then it is ignored meanwhile calculating towards a
        user's display color.
    guild : ``Guild`` or `None`
        The guild of the role. If the role is partial, including already deleted roles, then it's `.guild` is set to
        `None`.
    separated : `bool`
        Users show up in separated groups by their highest `separated` role.
    manager_id : `int`
        If the role is managed, then it's manager's id if applicable. Defaults to `0`.
    manager_type : `RoleManagerType`
        But what type of entity is the role managed.
    mentionable : `bool`
        Whether the role can be mentioned.
    name : `str`
        The name of the role. Can be empty string, if the role has no known name.
    permissions : ``Permission``
        The permissions of the users having the role.
    position : `int`
        The role's position.
    """
    __slots__ = ('color', 'guild', 'separated', 'manager_id', 'manager_type', 'mentionable', 'name', 'permissions',
        'position',)
    
    def __new__(cls, data, guild):
        """
        Creates a role from the given `data` at the given `guild`. If the role already exists and is not partial, then
        returns it. However it is partial, then updates it as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        guild : ``Guild``
            The owner guild of the role.
        
        Returns
        -------
        role : ``Role``
        """
        role_id = int(data['id'])
        try:
            role = ROLES[role_id]
            update = (role.guild is None)
        except KeyError:
            role = object.__new__(cls)
            role.id = role_id
            update = True
            ROLES[role_id] = role
        
        if update:
            
            guild.roles[role.id] = role
            role.guild = guild
            
            role.name = data['name']
            
            role.position = data.get('position', 0)
            
            role.color = Color(data.get('color', 0))
            
            role.permissions = Permission(data[PERMISSION_KEY])
            
            role.separated = data.get('hoist', False)
            
            if data.get('managed', False):
                role._set_managed(data)
            else:
                role.manager_id = 0
                role.manager_type = ROLE_MANAGER_TYPE_NONE
            
            role.mentionable = data.get('mentionable', False)
        
        return role
    
    @classmethod
    def precreate(cls, role_id, **kwargs):
        """
        Precreates a role by creating a partial one with the given parameters. When the role is loaded, then the
        precreated one will be picked up. However if the role is precreated when it already exists, then the existing
        one is picked up and is updated by the given parameters only if it is partial.
        
        Parameters
        ----------
        role_id : `int` or `str`
            The role's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the role.
        
        Other parameters
        ----------------
        name : `str`
            The role's ``.name``.
        manager_id : `None`, `int` or `str`
            The role's manager's id.
        manager_type : `RoleManagerType`
            The role's ``.manager_type``.
        mentionable : `bool`
            The role's ``.mentionable``.
        separated : `bool`
            The role's ``.separated``.
        position : `int`
            The role's ``.position``.
        permissions : `int` or ``Permission``
            The role's ``.permissions``.
        color : `int` or ``Color``
            The role's ``.color``.
        
        Returns
        -------
        role : ``Role``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        role_id = preconvert_snowflake(role_id, 'role_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 32)
                processable.append(('name',name))
            
            for key in ('mentionable', 'separated',):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_bool(value, key)
                    processable.append((key, value))
            
            try:
                position = kwargs.pop('position')
            except KeyError:
                pass
            else:
                position = preconvert_int(position, 'position', 0, 250)
                processable.append(('position', position))
            
            try:
                permissions = kwargs.pop('permissions')
            except KeyError:
                pass
            else:
                permissions = preconvert_flag(permissions, 'permissions', Permission)
                processable.append(('permissions', permissions))
            
            try:
                color = kwargs.pop('color')
            except KeyError:
                pass
            else:
                color = preconvert_color(color)
                processable.append(('color', color))
            
            try:
                manager_type = kwargs.pop('manager_type')
            except KeyError:
                try:
                    manager_id = kwargs.pop('manager_id')
                except KeyError:
                    pass
                else:
                    raise ValueError(f'`manager_type` was not given, meanwhile `manager_id` was. Received values: '
                        f'manager_id: {manager_id!r}')
            else:
                manager_type_type = manager_type.__class__
                if manager_type_type is not RoleManagerType:
                    raise TypeError(f'`manager_type` can be given as `{RoleManagerType.__class__}` instance, got '
                        f'{manager_type_type.__name__}')
                
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            role = ROLES[role_id]
        except KeyError:
            role = object.__new__(cls)
            role.id = role_id
            
            role.color = Color()
            role.guild = None
            role.separated = False
            role.manager_type = ROLE_MANAGER_TYPE_NONE
            role.mentionable = False
            role.name = ''
            role.permissions = PERMISSION_NONE
            role.position = 1
            ROLES[role_id] = role
        else:
            if (role.guild is not None):
                return role
        
        if (processable is not None):
            for item in processable:
                setattr(role, *item)
        
        return role
    
    def _set_managed(self, data):
        """
        Called when the role's manager_type is `ROLE_MANAGER_TYPE_UNSET` for trying to set the role's ``.manager_type``
        and ``.manager_id``.
        
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        """
        while True:
            try:
                tags = data['tags']
            except KeyError:
                manager_id = 0
                manager_type = ROLE_MANAGER_TYPE_UNSET
                break
            
            try:
                manager_id = tags['bot']
            except KeyError:
                pass
            else:
                manager_id = int(manager_id)
                manager_type = ROLE_MANAGER_TYPE_BOT
                break
            
            if 'premium_subscriber' in tags:
                manager_id = 0
                manager_type = ROLE_MANAGER_TYPE_BOOSTER
                break
            
            try:
                manager_id = data['integration']
            except KeyError:
                pass
            else:
                manager_id = int(manager_id)
                manager_type = ROLE_MANAGER_TYPE_INTEGRATION
                break
            
            manager_id = 0
            manager_type = ROLE_MANAGER_TYPE_UNKNOWN
            break
        
        self.manager_id = manager_id
        self.manager_type = manager_type
        
    def _update_no_return(self, data):
        """
        Updates the role with the given `data` with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        """
        guild = self.guild
        if guild is None:
            return
        
        clear_permission_cache = False
        
        position = data['position']
        if self.position != position:
            self.position = position
            clear_permission_cache = True
        
        self.name = data['name']
        
        permissions = Permission(data[PERMISSION_KEY])
        if self.permissions != permissions:
            self.permissions = permissions
            clear_permission_cache = True
        
        self.color = Color(data['color'])
        self.separated = data['hoist']
        
        if self.manager_type is ROLE_MANAGER_TYPE_UNSET:
            self._set_managed(data)
        
        self.mentionable = data['mentionable']
        
        if clear_permission_cache:
            guild._invalidate_perm_cache()
        
    def __str__(self):
        """Returns the role"s name or `'Partial'` if it has non."""
        name = self.name
        if not name:
            name = 'Partial'
        return name
    
    def __repr__(self):
        """Returns the role's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    def _update(self, data):
        """
        Updates the role with the given `data` and returns it's overwritten attributes as a `dict` with a
        `attribute-name` - `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-------------------+
        | Keys          | Values            |
        +===============+===================+
        | color         | ``Color``         |
        +---------------+-------------------+
        | managed       | `bool`            |
        +---------------+-------------------+
        | mentionable   | `bool`            |
        +---------------+-------------------+
        | name          | `str`             |
        +---------------+-------------------+
        | permissions   | ``Permission``    |
        +---------------+-------------------+
        | position      | `int`             |
        +---------------+-------------------+
        | separated     | `bool`            |
        +---------------+-------------------+
        """
        old_attributes = {}
        guild = self.guild
        if guild is None:
            return old_attributes
        
        clear_permission_cache = False
        
        position = data['position']
        if self.position != position:
            old_attributes['position'] = self.position
            self.position = position
            clear_permission_cache = True
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        permissions = Permission(data[PERMISSION_KEY])
        if self.permissions != permissions:
            old_attributes['permissions'] = self.permissions
            self.permissions = permissions
            clear_permission_cache = True
        
        color = data['color']
        if self.color != color:
            old_attributes['color'] = self.color
            self.color = Color(color)
        
        separated = data['hoist']
        if self.separated != separated:
            old_attributes['separated'] = self.separated
            self.separated = separated
        
        if self.manager_type is ROLE_MANAGER_TYPE_UNSET:
            self._set_managed(data)
        
        managed = data['managed']
        if self.managed != managed:
            old_attributes['managed'] = self.managed
            self.managed = managed
        
        mentionable = data['mentionable']
        if self.mentionable != mentionable:
            old_attributes['mentionable'] = self.mentionable
            self.mentionable = mentionable
        
        if clear_permission_cache:
            guild._invalidate_perm_cache()
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the role's references.
        
        Used when the role is deleted.
        """
        guild = self.guild
        if guild is None:
            return # already deleted
        
        self.guild = None
        
        try:
            del guild.roles[self.id]
        except KeyError:
            pass
        
        guild._cache_perm = None
        for channel in guild.channels.values():
            channel._cache_perm = None
        
        for user in guild.users.values():
            try:
                profile = user.guild_profiles[guild]
            except KeyError:
                # the user has no ``GuildProfile``, it supposed to be impossible
                continue
            
            roles = profile.roles
            if roles is None:
                continue
            
            try:
                roles.remove(self)
            except ValueError:
                pass
    
    @property
    def is_default(self):
        """
        Returns whether the role is the default role at it's respective guild.
        
        Returns
        -------
        is_default : `bool`
        """
        return (self.position == 0)
    
    @property
    def mention(self):
        """
        The role's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<@&{self.id}>'
    
    def __format__(self, code):
        """
        Formats the role in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        role : `str`
        
        Examples
        --------
        ```py
        >>>> from hata import Role, now_as_id
        >>>> role = Role.precreate(now_as_id(), name='admiral-general')
        >>>> role
        <Role name='admiral-general', id=725333995067277312>
        >>>> # no code stands for str(role).
        >>>> f'{role}'
        'admiral-general'
        >>>> # 'm' stands for mention.
        >>>> f'{role:m}'
        '<@&725333995067277312>'
        >>>> # 'c' stands for created at.
        >>>> f'{role:c}'
        '2020.06.24-12:58:20'
        ```
        """
        if not code:
            return str(self)
        
        if code == 'm':
            return self.mention
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def users(self):
        """
        Returns the users who have the role.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) instances
        """
        guild = self.guild
        if guild is None:
            users = []
        elif self.position == 0:
            users = list(guild.users.values())
        else:
            users = []
            for user in guild.users.values():
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    # should not happen
                    continue
                
                roles = profile.roles
                if roles is None:
                    continue
                
                if self not in user.roles:
                    continue
                
                users.append(user)
        
        return users
    
    @property
    def managed(self):
        """
        Returns whether the role is managed.
        
        Returns
        -------
        managed: `bool`
        """
        return (self.manager_type is not ROLE_MANAGER_TYPE_NONE)
    
    @property
    def manager(self):
        """
        Returns the manager entity of the role if applicable.
        
        Returns
        -------
        manager : `None`, ``User``, ``Client`` or ``Integration``
        """
        manager_type = self.manager_type
        if manager_type is ROLE_MANAGER_TYPE_NONE:
            manager = None
        
        elif manager_type is ROLE_MANAGER_TYPE_BOT:
            manager = create_partial_user(self.manager_id)
            
            # `create_partial_user` sets newly created users' `.is_bot` attribute as `False`.
            if not manager.is_bot :
                manager.is_bot = True
        
        elif manager_type is ROLE_MANAGER_TYPE_INTEGRATION:
            manager = create_partial_integration(self.manager_id, role=self)
        
        else:
            manager = None
        
        return manager
    
    @property
    def partial(self):
        """
        Returns whether the role is partial.
        
        Partial roles have `.guild` set as ``None``.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.guild is None)
    
    def _get_colour(self):
        return self.color
    
    def _set_colour(self, color):
        self.color = color
    
    colour = property(_get_colour, _set_colour)
    if DOCS_ENABLED:
        colour.__doc__ = """Alias of ``.color``."""
    
    def __gt__(self, other):
        """Returns whether this role's position is higher than the other's."""
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id > other.id:
                    return True
        
            return False
        
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether this role's position is higher or equal to the other's."""
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id >= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether this role's position is less or equal to the other's."""
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id <= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether this role's position is less than the other's."""
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id < other.id:
                    return True
            
            return False
        
        return NotImplemented


class PermissionOverwrite:
    """
    Represents a permission overwrite of a guild channel.
    
    Attributes
    ----------
    allow : ``Permission``
        The allowed permissions by the overwrite.
    deny : ``Permission``
        The denied permission by the overwrite.
    target_role : `None`, ``Role`` or ``Unknown``
        The target role entity of the overwrite if applicable. Defaults to `None`.
    target_user_id : `int`
        The target user id of the overwrite if applicable. Defaults to `0`.
    """
    __slots__ = ('allow', 'deny', 'target_role', 'target_user_id')
    
    def __init__(self, data):
        """
        Creates a permission overwrite from the given data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        """
        id_ = int(data['id'])
        if get_perm_ow_key_value(data) == PERM_OW_TYPE_ROLE:
            target_role = create_partial_role(id_)
            target_user_id = 0
        else:
            target_role = None
            target_user_id = id_
        
        self.target_role = target_role
        self.target_user_id = target_user_id
        self.allow = Permission(data[PERMISSION_ALLOW_KEY])
        self.deny = Permission(data[PERMISSION_DENY_KEY])
    
    @property
    def target(self):
        """
        Returns the target entity of the overwrite.
        
        Returns
        -------
        target : ``Client``, ``User`` or ``Role``
        """
        target = self.target_role
        if target is None:
            target = create_partial_user(self.target_user_id)
        
        return target
    
    @classmethod
    def custom(cls, target, allow, deny):
        """
        Creates an overwrite object with the given parameters.
        
        Parameters
        ----------
        target : ``Role`` or ``UserBase`` instance
            The target entity of the overwrite.
        allow : `int`
            The allowed permissions by the overwrite.
        deny : `int`
            The denied permission by the overwrite.
        
        Returns
        -------
        self : ``PermissionOverwrite``
        """
        if type(target) is Role:
            target_role = target
            target_user_id = 0
        else:
            target_role = None
            target_user_id = target.id
        
        self = object.__new__(cls)
        self.target_role = target_role
        self.target_user_id = target_user_id
        self.allow = Permission(allow)
        self.deny = Permission(deny)
        return self
    
    def __hash__(self):
        """Returns the permission overwrite's hash."""
        return self.target.id^self.allow^self.deny
    
    def __repr__(self):
        """Returns the permission overwrite's representation."""
        return f'<{self.__class__.__name__} target={self.target!r}>'
    
    def keys(self):
        """
        Yields the permissions' names.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
            Permissions' respective name.
        """
        yield from Permission.__keys__.keys()
    
    __iter__ = keys
    
    def values(self):
        """
        Yields position by position each permission's state. `+1` is yielded if the permission is enabled, `-1` if
        disabled and `0` if neither.
        
        This method is a generator.
        
        Yields
        ------
        state : `int`
            The permission's state.
            
            Can be one of the following:
            
            +-----------+-------+
            | Name      | Value |
            +===========+=======+
            | Enabled   | +1    |
            +-----------+-------+
            | None      | 0     |
            +-----------+-------+
            | Disabled  | -1    |
            +-----------+-------+
        """
        allow = self.allow
        deny = self.deny
        for index in Permission.__keys__.values():
            if (allow>>index)&1:
                state = +1
            elif (deny>>index)&1:
                state = -1
            else:
                state = 0
            
            yield state
    
    def items(self):
        """
        Yields the permission overwrite's items. What includes their name and their state. As state `+1` is yielded
        if the permission is enabled, `-1` if disabled and `0` if neither.
        
        This method is a generator.
        
        Yields
        -------
        name : str`
            Permissions' respective name.
        state : `int`
            The permission's state.
            
            Can be one of the following:
            
            +-----------+-------+
            | Name      | Value |
            +===========+=======+
            | Enabled   | +1    |
            +-----------+-------+
            | None      | 0     |
            +-----------+-------+
            | Disabled  | -1    |
            +-----------+-------+
        """
        allow = self.allow
        deny = self.deny
        for key, index in Permission.__keys__.items():
            if (allow>>index)&1:
                state = +1
            elif (deny>>index)&1:
                state = -1
            else:
                state = 0
            
            yield key, state
    
    def __getitem__(self, key):
        """Returns the permission's state for the given permission name."""
        index = Permission.__keys__[key]
        if (self.allow>>index)&1:
            state = +1
        elif (self.deny>>index)&1:
            state = -1
        else:
            state = 0
        
        return state
    
    @property
    def type(self):
        if type(self.target) is Role:
            type_ = PERM_OW_TYPE_ROLE
        else:
            type_ = PERM_OW_TYPE_USER
        return type_
    
    if DOCS_ENABLED:
        if API_VERSION in (6, 7):
            type.__doc__ = (
        """
        Returns the Discord side identifier value permission overwrite.
        
        Returns
        -------
        type_ : `str`
            Can be either `'role'` or `'member'`
        """)
        else:
            type.__doc__ = (
        """
        Returns the Discord side identifier value permission overwrite.
        
        Returns
        -------
        type_ : `int`
            Can be either 0` or `1`
        """)
    
    @property
    def id(self):
        """
        Returns the permission overwrite's target's id.
        
        Returns
        -------
        id_ : `int`
        """
        target_role = self.target_role
        if target_role is None:
            id_ = self.target_user_id
        else:
            id_ = target_role.id
        
        return id_
    
    def __lt__(self, other):
        """Returns whether is this permission overwrite is at lower position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_type = 0
            self_target_id = self.target_user_id
        else:
            self_target_type = 1
            self_target_id = self_target_role.id
        
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_type = 0
            other_target_id = other.target_user_id
        else:
            other_target_type = 1
            other_target_id = other_target_role.id
        
        if self_target_type < other_target_type:
            return True
        
        if self_target_type == other_target_type:
            if self_target_id < other_target_id:
                return True
            
            return False
        
        return False
    
    def __eq__(self, other):
        """Returns whether is this permission overwrite is same as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.allow != other.allow:
            return False
        
        if self.deny != other.deny:
            return False
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_id = self.target_user_id
        else:
            self_target_id = self_target_role.id
        
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_id = other.target_user_id
        else:
            other_target_id = other_target_role.id
        
        if self_target_id != other_target_id:
            return False
        
        return True
    
    def __gt__(self, other):
        """Returns whether is this permission overwrite is at greater position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_type = 0
            self_target_id = self.target_user_id
        else:
            self_target_type = 1
            self_target_id = self_target_role.id
            
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_type = 0
            other_target_id = other.target_user_id
        else:
            other_target_type = 1
            other_target_id = other_target_role.id
        
        if self_target_type > other_target_type:
            return True
        
        if self_target_type == other_target_type:
            if self_target_id > other_target_id:
                return True
            
            return False
        
        return False

def cr_p_role_object(name, id_=None, color=Color(), separated=False, position=0, permissions=Permission(),
        managed=False, mentionable=False):
    """
    Creates a json serializable object representing a ``Role``.
    
    Parameters
    ----------
    name : `str`
        The name of the role.
    id_ : `None` or `int`,`optional
        The role's unique identifier number. If given as `None`, then a random `id` will be generated.
    color : ``Color``, Optional
        The role's color. Defaults to `Color(0)`
    separated : `bool`
        Users show up in separated groups by their highest `separated` role. Defaults to `False`.
    position : `int`
        The role's position at the guild. Defaults to `0`.
    permissions : ``Permission``
        The permissions of the users having the role.
    managed : `bool`
        Whether the role is managed by an integration.
    mentionable : `bool`
        Whether the role can be mentioned.
    
    Returns
    -------
    role_data : `dict` of (`str`, `Any`) items
    """
    if id_ is None:
        id_ = random_id()
    
    return {
        'id'          : id_,
        'name'        : name,
        'color'       : color,
        'hoist'       : separated,
        'position'    : position,
        'permissions' : permissions,
        'managed'     : managed,
        'mentionable' : mentionable,
            }

def cr_p_overwrite_object(target, allow, deny):
    """
    Creates a json serializable object representing a ``PermissionOverwrite``(permission overwrite).
    
    Parameters
    ----------
    target : ``Client``, ``User`` or ``Role``
        The target entity of the overwrite.
        The allowed permissions by the overwrite.
    deny : `int`
        The denied permission by the overwrite.
    
    Returns
    -------
    permission_overwrite_data : `dict` of (`str`, `Any) items
    """
    return {
        'allow' : allow,
        'deny'  : deny,
        'id'    : target.id,
        'type'  : PERM_OW_TYPE_ROLE if type(target) is Role else PERM_OW_TYPE_USER,
            }

module_rate_limit.Role = Role
module_user.create_partial_role = create_partial_role

del module_rate_limit
del module_user
