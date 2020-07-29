﻿# -*- coding: utf-8 -*-
__all__ = ('PermOW', 'Role', 'RoleManagerType', 'cr_p_overwrite_object', 'cr_p_role_object', )

from .bases import DiscordEntity
from .client_core import ROLES
from .others import random_id
from .color import Color
from .permission import Permission
from .user import PartialUser
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_color, preconvert_int, preconvert_bool, \
    preconvert_flag

from . import ratelimit

PartialIntegration = NotImplemented

def PartialRole(role_id):
    """
    Creates a partial role from the given `role_id`. If the role already exists returns that instead.
    
    Parameters
    ----------
    role_id : `int`
        The unique identificator number of the role.
    
    Returns
    -------
    role : ``Role``
    """
    try:
        return ROLES[role_id]
    except KeyError:
        pass
    
    role=object.__new__(Role)
    role.id=role_id
    
    role.color=Color(0)
    role.guild=None
    role.separated=False
    # id is set up
    role.manager_type=ROLE_MANAGER_TYPE_NONE
    role.manager_id = 0
    role.mentionable=False
    role.name=''
    role.permissions=Permission.permission_none
    role.position=1 # 0 is default role, so we go for 1
    
    ROLES[role_id]=role
    
    return role

class RoleManagerType(object):
    """
    Represents a managed role's manager type.
    
    Attributes
    ----------
    name : `str`
        The name of the role manager type.
    value : `int`
        The identificator value the role manager type.
    
    Class Attributes
    ----------------
    Every predefind role manager type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | NONE                  | NONE          | 0     |
    +-----------------------+---------------+-------+
    | UNSET                 | UNSET         | 1     |
    +-----------------------+---------------+-------+
    | UNKNOWN               | UNKNOWN       | 2     |
    +-----------------------+---------------+-------+
    | BOT                   | BOT           | 3     |
    +-----------------------+---------------+-------+
    | BOOSTER               | BOOSTER       | 4     |
    +-----------------------+---------------+-------+
    | INTEGRATION           | INTEGRATION   | 5     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ('name', 'value', )
    
    def __init__(self, name, value):
        """
        Creates a new role manager type with the given name and value.
        
        Parameters
        ----------
        name : `str`
            The icon role manager's name.
        value : `int`
            The role manager type's identificator value.
        """
        self.name = name
        self.value = value
    
    def __str__(self):
        """Returns the name of the role manager type."""
        return self.name
    
    def __int__(self):
        """Returns the identificator value of the role manager type."""
        return self.value
    
    def __bool__(self):
        """Returns whether the role manager's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    def __repr__(self):
        """Returns the role manager type's representation."""
        return f'{self.__class__.__name__}(name={self.name!r}, value={self.value!r})'
    
    def __hash__(self):
        """Returns the role manager type's hash, what equals to it's value."""
        return self.value
    
    def __gt__(self, other):
        """Returns whether this role manager type's value is greater than the other's."""
        if type(self) is type(other):
            return self.value > other.value
        
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether this role manager type's value is greater or equal to the other's."""
        if type(self) is type(other):
            return self.value >= other.value
        
        return NotImplemented
    
    def __eq__(self, other):
        """Returns whether this role manager type's value is equal to the other's."""
        if type(self) is type(other):
            return self.value == other.value
        
        return NotImplemented
    
    def __ne__(self, other):
        """Returns whether this role manager type's value is not equal to the other's."""
        if type(self) is type(other):
            return self.value != other.value
        
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether this role manager type's value is less or equal to the other's."""
        if type(self) is type(other):
            return self.value <= other.value
        
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether this role manager type's value is less than the other's."""
        if type(self) is type(other):
            return self.value < other.value
        
        return NotImplemented
    
    NONE = NotImplemented
    UNSET = NotImplemented
    UNKNOWN = NotImplemented
    BOT = NotImplemented
    BOOSTER = NotImplemented
    INTEGRATION = NotImplemented

RoleManagerType.NONE        = ROLE_MANAGER_TYPE_NONE        = RoleManagerType('NONE'        , 0 ,)
RoleManagerType.UNSET       = ROLE_MANAGER_TYPE_UNSET       = RoleManagerType('UNSET'       , 1 ,)
RoleManagerType.UNKNOWN     = ROLE_MANAGER_TYPE_UNKNOWN     = RoleManagerType('UNKNOWN'     , 2 ,)
RoleManagerType.BOT         = ROLE_MANAGER_TYPE_BOT         = RoleManagerType('BOT'         , 3 ,)
RoleManagerType.BOOSTER     = ROLE_MANAGER_TYPE_BOOSTER     = RoleManagerType('BOOSTER'     , 4 ,)
RoleManagerType.INTEGRATION = ROLE_MANAGER_TYPE_INTEGRATION = RoleManagerType('INTEGRATION' , 5 ,)

class Role(DiscordEntity, immortal=True):
    """
    Represents a Discord guild's role.
    
    Attributes
    ----------
    id : `int`
        The unique identificator numebr of the role.
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
        But what type of entitiy is the role managed.
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
        role_id=int(data['id'])
        try:
            role=ROLES[role_id]
            update=(role.guild is None)
        except KeyError:
            role=object.__new__(cls)
            role.id=role_id
            update=True
            ROLES[role_id]=role
        
        if update:
            
            guild.all_role[role.id]=role
            role.guild=guild
            
            role.name=data['name']
            
            role.position=data.get('position',0)
            
            role.color=Color(data.get('color',0))
            
            role.permissions=Permission(data['permissions'])
            
            role.separated=data.get('hoist',False)
            
            if data.get('managed',False):
                role._set_managed(data)
            else:
                role.manager_id = 0
                role.manager_type = ROLE_MANAGER_TYPE_NONE
            
            role.mentionable=data.get('mentionable',False)
            
            guild.roles.append(role)
        
        return role
    
    @classmethod
    def precreate(cls, role_id, **kwargs):
        """
        Precreates a role by creating a partial one with the given paremeters. When the role is loaaded, then the
        precreated one will be picked up. However if the role is precreated when it already exists, then the existing
        one is picked up and is updated by the given paremeters only if it is partial.
        
        Parameters
        ----------
        role_id : `int` or `str`
            The role's id.
        **kwargs : keyword arguments
            Additonal predefined attributes for the role.
        
        Other parameters
        ----------------
        name : `str`
            The role's ``.name``.
        manager_id : `None`, `int` or `str`
            The role's manager's id.
        manager_type : `RoleManagerType`
            The role's ``.manager_type``.
        mentionable : `bool
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
                    processable.append((key,value))
            
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
                processable.append(('permissions',permissions))
            
            try:
                color = kwargs.pop('color')
            except KeyError:
                pass
            else:
                color = preconvert_color(color)
                processable.append(('color',color))
            
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
                    raise TypeError(f'`manager_type` can be given as `{RoleManagerType.__class__}` insatnce, got '
                        f'{manager_type_type.__name__}')
                
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            role=ROLES[role_id]
        except KeyError:
            role=object.__new__(cls)
            role.id=role_id
            
            role.color      = Color()
            role.guild      = None
            role.separated  = False
            role.manager_type = ROLE_MANAGER_TYPE_NONE
            role.mentionable= False
            role.name       = ''
            role.permissions= Permission.permission_none
            role.position   = 1
            ROLES[role_id]  = role
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
            guild.roles.sort()
            clear_permission_cache = True
        
        self.name=data['name']
        permissions = Permission(data['permissions'])
        if self.permissions != permissions:
            self.permissions = permissions
            clear_permission_cache = True
        
        self.color=Color(data['color'])
        self.separated=data['hoist']
        
        if self.manager_type is ROLE_MANAGER_TYPE_UNSET:
            self._set_managed(data)
        
        self.mentionable=data['mentionable']
        self.guild._cache_perm.clear()
        
        if clear_permission_cache:
            guild._cache_perm.clear()
            for channel in guild.all_channel.values():
                channel._cache_perm.clear()
        
    def __str__(self):
        """Returns teh role"s name or `'Partial'` if it has non."""
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
            guild.roles.sort()
            clear_permission_cache = True
        
        name=data['name']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
        
        permissions=Permission(data['permissions'])
        if self.permissions!=permissions:
            old_attributes['permissions']=self.permissions
            self.permissions=permissions
            clear_permission_cache = True
        
        color=data['color']
        if self.color!=color:
            old_attributes['color']=self.color
            self.color=Color(color)
        
        separated=data['hoist']
        if self.separated!=separated:
            old_attributes['separated']=self.separated
            self.separated=separated
        
        if self.manager_type is ROLE_MANAGER_TYPE_UNSET:
            self._set_managed(data)
        
        managed=data['managed']
        if self.managed!=managed:
            old_attributes['managed']=self.managed
            self.managed=managed
        
        mentionable=data['mentionable']
        if self.mentionable!=mentionable:
            old_attributes['mentionable']=self.mentionable
            self.mentionable=mentionable
        
        if clear_permission_cache:
            guild._cache_perm.clear()
            for channel in guild.all_channel.values():
                channel._cache_perm.clear()
        
        return old_attributes

    def _delete(self):
        """
        Removes the role's references.
        
        Used when the role is deleted.
        """
        guild=self.guild
        if guild is None:
            return #already deleted
        
        self.guild=None
        
        guild.roles.remove(self)
        del guild.all_role[self.id]
        
        guild._cache_perm.clear()
        for channel in guild.all_channel.values():
            channel._cache_perm.clear()
        
        for user in guild.users.values():
            try:
                profile=user.guild_profiles[guild]
            except KeyError:
                #the user has no GuildProfile, it supposed to be impossible
                continue
            try:
                profile.roles.remove(self)
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
        return self.position==0
    
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
        Formats the roel in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        role : `str`
        
        Examples
        --------
        >>>> from hata import Role, now_as_id
        >>>> role = Role.precreate(now_as_id(), name='admiralgeneral')
        >>>> role
        <Role name='admiralgeneral', id=725333995067277312>
        >>>> # no code stands for str(role).
        >>>> f'{role}'
        'admiralgeneral'
        >>>> # 'm' stands for mention.
        >>>> f'{role:m}'
        '<@&725333995067277312>'
        >>>> # 'c' stands for created at.
        >>>> f'{role:c}'
        '2020.06.24-12:58:20'
        """
        if not code:
            return self.__str__()
        if code=='m':
            return self.mention
        if code=='c':
            return self.created_at.__format__('%Y.%m.%d-%H:%M:%S')
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def users(self):
        """
        Returns the users who have the role.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) instances
        """
        guild=self.guild
        if guild is None:
            users = []
        elif self.position==0:
            users = list(guild.users.values())
        else:
            role_id=self.id
            users= [user for user in guild.users.values() if self in user.guild_profiles[guild].roles]
        
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
            manager = PartialUser(self.manager_id)
            
            # `Partialuser` sets newly created users' `.is_bot` attribute as `False`.
            if not manager.is_bot :
                manager.is_bot = True
        
        elif manager_type is ROLE_MANAGER_TYPE_INTEGRATION:
            manager = PartialIntegration(self.manager_id, role=self)
        
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
    
    def __gt__(self, other):
        """Returns whether this role's position is higher than the other's."""
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id>other.id:
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

#permission overwrite
class PermOW(object):
    """
    Represents a permission overwrite of a guild channel.
    
    Attributes
    ----------
    allow : `int`
        The allowed permissions by the overwrite.
    deny : `int`
        The denied permission by the overwrite.
    target : ``Client``, ``User`` or ``Role``
        The target entity of the overwrite.
    """
    __slots__ = ('allow', 'deny', 'target',)

    def __init__(self, data):
        """
        Creates a permission overwrite from the given data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        """
        id_=int(data['id'])
        if data['type']=='role':
            target=PartialRole(id_)
        else:
            target=PartialUser(id_)
        self.target = target
        self.allow=data['allow']
        self.deny=data['deny']
    
    @classmethod
    def custom(cls, target, allow, deny):
        """
        Creates an overwrite object with the given parameters.
        
        Parameters
        ----------
        target : ``Role`` or ``UserBase`` instance
            The target entity of the overwrite.
        allow : `int`
            The allowed permissions by the overtwrite.
        deny : `int`
            The denied permission by the overwrite.
        
        Returns
        -------
        self : ``PermOW``
        """
        self = object.__new__(cls)
        self.target = target
        self.allow = int(allow)
        self.deny = int(deny)
        return self
    
    def __hash__(self):
        """Returns teh permission overwrite's hash."""
        return self.target.id^self.allow^self.deny
    
    def __repr__(self):
        """Returns the permisison overwrite's represnetation."""
        return f'<{self.__class__.__name__} target={self.target!r}>'
    
    def keys(self):
        """
        Yields the permissions' names.
        
        Yields
        ------
        name : `str`
        """
        yield from Permission.__keys__.keys()
    
    __iter__=keys
    
    def values(self):
        """
        Yields position by position each permission's state. `+1` is yielded if the permission is enabled, `-1` if
        disabled and `0` if neither.
        
        Yields
        ------
        state : `int`
        """
        allow=self.allow
        deny=self.deny
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
        
        Yields
        -------
        name : str`
        state : `int`
        """
        allow=self.allow
        deny=self.deny
        for key,index in Permission.__keys__.items():
            if (allow>>index)&1:
                state = +1
            elif (deny>>index)&1:
                state = -1
            else:
                state = 0
            
            yield key, state
    
    def __getitem__(self, key):
        """Returns the permission's state for the given permission name."""
        index=Permission.__keys__[key]
        if (self.allow>>index)&1:
            state = +1
        elif (self.deny>>index)&1:
            state = -1
        else:
            state = 0
        
        return state
    
    @property
    def type(self):
        """
        Returns the Discord side identificator type permission overwrite.
        
        Returns
        -------
        type_ : `str`
            Can be either `'role'` or `'member'`
        """
        if type(self.target) is Role:
            type_ = 'role'
        else:
            type_ = 'member'
        return type_
    
    @property
    def id(self):
        """
        Returns the permission overwrite's target's id.
        
        Returns
        -------
        id : `int`
        """
        return self.target.id
    
    def __lt__(self, other):
        """Returns whether is this permission overwrite is at lower position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target = self.target
        other_target = other.target
        
        if type(self_target) is Role:
            if type(other_target) is Role:
                if self_target < other_target:
                    return True
                return False
            return True
        if type(other_target) is Role:
            return True
        if self_target < other.target:
            return True
        return False
        
    def __eq__(self,other):
        """Returns whether is this permission overwrite is same as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.target.id!=other.target.id:
            return False
        
        if self.allow!=other.allow:
            return False
        
        if self.deny!=other.deny:
            return False
        
        return True
    
    def __gt__(self,other):
        """Returns whether is this permission overwrite is at greater position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target = self.target
        other_target = other.target
        
        if type(self_target) is Role:
            if type(other_target) is Role:
                if self_target > other_target:
                    return True
                return False
            return False
        if type(other_target) is Role:
            return False
        if self_target > other_target:
            return True
        return True
    
def cr_p_role_object(name, id_=None, color=Color(0), separated=False, position=0, permissions=Permission(0),
        managed=False, mentionable=False):
    """
    Creates a json serializable object representing a ``Role``.
    
    Parameters
    ----------
    name : `str`
        The name of the role.
    id_ : `None` or `int`,`optional
        The role's unique identificator number. If given as `None`, then a random `id` will be generated.
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
        id_=random_id()
    
    return {
        'id'            : id_,
        'name'          : name,
        'color'         : color,
        'hoist'         : separated,
        'position'      : position,
        'permissions'   : permissions,
        'managed'       : managed,
        'mentionable'   : mentionable,
            }

def cr_p_overwrite_object(target, allow, deny):
    """
    Creates a json serializable object representing a ``PermOW``(permission overwrite).
    
    Parameters
    ----------
    target : ``Client``, ``User`` or ``Role``
        The target entity of the overwrite.
        The allowed permissions by the overwrite.
    deny : `int`
        The denied permission by the overwrite.
    
    Returns
    -------
    permission_overwrite_data : `dict` of (`str`, `Any) utems.
    """
    return {
        'allow' : allow,
        'deny'  : deny,
        'id'    : target.id,
        'type'  : 'role' if type(target) is Role else 'member',
            }

ratelimit.Role = Role

del ratelimit
del DiscordEntity
