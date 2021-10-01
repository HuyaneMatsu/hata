__all__ = ('Role', )

from ...backend.export import export, include

from ..bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from ..core import ROLES, GUILDS
from ..utils import DATETIME_FORMAT_CODE
from ..color import Color
from ..user import create_partial_user_from_id
from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_color, preconvert_int, preconvert_bool, \
    preconvert_flag
from ..permission.utils import PERMISSION_KEY
from ..permission.permission import Permission, PERMISSION_NONE
from ..http import urls as module_urls

from .preinstanced import RoleManagerType

create_partial_integration_from_id = include('create_partial_integration_from_id')
create_unicode_emoji = include('create_unicode_emoji')
Emoji = include('Emoji')

ROLE_MANAGER_TYPE_NONE = RoleManagerType.none
ROLE_MANAGER_TYPE_UNSET = RoleManagerType.unset
ROLE_MANAGER_TYPE_UNKNOWN = RoleManagerType.unknown
ROLE_MANAGER_TYPE_BOT = RoleManagerType.bot
ROLE_MANAGER_TYPE_BOOSTER = RoleManagerType.booster
ROLE_MANAGER_TYPE_INTEGRATION = RoleManagerType.integration


@export
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
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
        
        Mutually exclusive with ``.unicode_emoji``
        
    icon_type : ``IconType``
        The guild's icon's type.
        
        Mutually exclusive with ``.unicode_emoji``
    
    guild_id : ``Guild`` or `None`
        The guild of the role. If the role is partial, including already deleted roles, then it's `.guild` is set to
        `None`.
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
    separated : `bool`
        Users show up in separated groups by their highest `separated` role.
    unicode_emoji : `None` or ``Emoji``
        Unicode emoji icon of the role.
        
        Mutually exclusive with ``.icon_hash`` and ``.icon_type``.
    """
    __slots__ = ('color', 'guild_id', 'manager_id', 'manager_type', 'mentionable', 'name', 'permissions', 'position',
        'separated', 'unicode_emoji')
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.role_icon_url,
        module_urls.role_icon_url_as,
    )
    
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
            self = ROLES[role_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = role_id
            update = True
            ROLES[role_id] = self
        else:
            update = self.partial
        
        if update:
            
            guild.roles[role_id] = self
            self.guild_id = guild.id
            
            self.name = data['name']
            
            self.position = data.get('position', 0)
            
            self.color = Color(data.get('color', 0))
            
            self.permissions = Permission(data[PERMISSION_KEY])
            
            self.separated = data.get('hoist', False)
            
            self._set_icon(data)
            
            if data.get('managed', False):
                self._set_managed(data)
            else:
                self.manager_id = 0
                self.manager_type = ROLE_MANAGER_TYPE_NONE
            
            self.mentionable = data.get('mentionable', False)
            
            unicode = data.get('unicode_emoji', None)
            if (unicode is None):
                unicode_emoji = None
            else:
                unicode_emoji = create_unicode_emoji(unicode)
            
            self.unicode_emoji = unicode_emoji
        
        return self
    
    
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
        **kwargs : keyword parameters
            Additional predefined attributes for the role.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The role's ``.name``.
        manager_id : `None`, `int` or `str`, Optional (Keyword only)
            The role's manager's id.
        manager_type : ``RoleManagerType``, Optional (Keyword only)
            The role's ``.manager_type``.
        mentionable : `bool`, Optional (Keyword only)
            The role's ``.mentionable``.
        separated : `bool`, Optional (Keyword only)
            The role's ``.separated``.
        position : `int`, Optional (Keyword only)
            The role's ``.position``.
        permissions : `int` or ``Permission``, Optional (Keyword only)
            The role's ``.permissions``.
        color : `int` or ``Color``, Optional (Keyword only)
            The role's ``.color``.
        icon : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The role's icon.
            
            > Mutually exclusive with `icon_type`, `icon_hash` and with `unicode_emoji`.
        
        icon_type : ``IconType``, Optional (Keyword only)
            The role's icon's type.
            
            > Mutually exclusive with `icon` and with `unicode_emoji`.
            
        icon_hash : `int`, Optional (Keyword only)
            The role's icon's hash.
            
            > Mutually exclusive with `icon`  and with `unicode_emoji`.
        
        unicode_emoji : `None` or ``Emoji``
            The role's icon as an unicode emoji.
            
            > Mutually exclusive with the `icon`, `icon_type` and `icon_hash` parameters.
        
        Returns
        -------
        role : ``Role``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
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
                color = preconvert_color(color, 'color', False)
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
            
            cls.icon.preconvert(kwargs, processable)
            
            try:
                unicode_emoji = kwargs.pop('unicode_emoji')
            except KeyError:
                pass
            else:
                if (unicode_emoji is not None):
                    if not isinstance(unicode_emoji, Emoji):
                        raise TypeError(f'`unicode_emoji` can be only `{Emoji.__name__}` instance, got '
                            f'{unicode_emoji.__class__.__name__}.')
                    
                    if not unicode_emoji.is_unicode_emoji():
                        raise ValueError(f'`unicode_emoji` can be only unicode emoji, got {unicode_emoji!r}.')
                    
                    processable.append(('unicode_emoji', unicode_emoji))
                    
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            self = ROLES[role_id]
        except KeyError:
            self = cls._create_empty(role_id)
            ROLES[role_id] = self
        else:
            if (not self.partial):
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
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
        
        
    def _update_attributes(self, data):
        """
        Updates the role with the given `data` with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        """
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
        
        self._set_icon(data)
        
        unicode = data.get('unicode_emoji', None)
        if (unicode is None):
            unicode_emoji = None
        else:
            unicode_emoji = create_unicode_emoji(unicode)
        
        self.unicode_emoji = unicode_emoji
        
        if clear_permission_cache:
            guild_id = self.guild_id
            if guild_id:
                try:
                    guild = GUILDS[self.guild_id]
                except KeyError:
                    pass
                else:
                    guild._invalidate_permission_cache()
        
    
    def __repr__(self):
        """Returns the role's representation."""
        repr_parts = ['<', self.__class__.__name__, ' id=', repr(self.id)]
        
        if self.partial:
            repr_parts.append(' (partial)')
        else:
            repr_parts.append(', name=')
            repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _difference_update_attributes(self, data):
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
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | color         | ``Color``             |
        +---------------+-----------------------+
        | icon          | ``Icon``              |
        +---------------+-----------------------+
        | managed       | `bool`                |
        +---------------+-----------------------+
        | mentionable   | `bool`                |
        +---------------+-----------------------+
        | name          | `str`                 |
        +---------------+-----------------------+
        | permissions   | ``Permission``        |
        +---------------+-----------------------+
        | position      | `int`                 |
        +---------------+-----------------------+
        | separated     | `bool`                |
        +---------------+-----------------------+
        | unicode_emoji | `None` or ``Emoji``   |
        +---------------+-----------------------+
        """
        old_attributes = {}
        
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
        
        self._update_icon(data, old_attributes)
        
        unicode = data.get('unicode_emoji', None)
        if (unicode is None):
            unicode_emoji = None
        else:
            unicode_emoji = create_unicode_emoji(unicode)
        
        if self.unicode_emoji is not unicode_emoji:
            old_attributes['unicode_emoji'] = self.unicode_emoji
            self.unicode_emoji = unicode_emoji
        
        if clear_permission_cache:
            guild_id = self.guild_id
            if guild_id:
                try:
                    guild = GUILDS[self.guild_id]
                except KeyError:
                    pass
                else:
                    guild._invalidate_permission_cache()
        
        return old_attributes
    
    
    def _delete(self):
        """
        Removes the role's references.
        
        Called when the role is deleted.
        """
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            guild._invalidate_permission_cache()
            
            role_id = self.id
            try:
                del guild.roles[role_id]
            except KeyError:
                pass
            else:
                for user in guild.users.values():
                    try:
                        guild_profile = user.guild_profiles[guild_id]
                    except KeyError:
                        pass
                    else:
                        role_ids = guild_profile.role_ids
                        if (role_ids is not None):
                            try:
                                index = role_ids.index(role_id)
                            except ValueError:
                                pass
                            else:
                                if len(role_ids) == 1:
                                    role_ids = None # It is so deep! (that's what she said)
                                else:
                                    role_ids = tuple(*role_ids[:index], *role_ids[index+1:])
                                guild_profile.role_ids = role_ids
    
    
    @property
    def is_default(self):
        """
        Returns whether the role is the default role at it's respective guild.
        
        Returns
        -------
        is_default : `bool`
        """
        return (self.id == self.guild_id)
    
    
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
        >>>> # no code stands for `role.name`.
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
            return self.name
        
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
        users : `list` of ``ClientUserBase`` instances
        """
        users = []
        guild_id = self.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            role_id = self.id
            if role_id == guild.id:
                users.extend(guild.users.values())
            else:
                for user in guild.users.values():
                    try:
                        guild_profile = user.guild_profiles[guild.id]
                    except KeyError:
                        # should not happen
                        pass
                    else:
                        role_ids = guild_profile
                        if (role_ids is not None):
                            if role_id in role_ids:
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
        manager : `None`, ``ClientUserBase`` or ``Integration``
        """
        manager_type = self.manager_type
        if manager_type is ROLE_MANAGER_TYPE_NONE:
            manager = None
        
        elif manager_type is ROLE_MANAGER_TYPE_BOT:
            manager = create_partial_user_from_id(self.manager_id)
            
            # `create_partial_user_from_id` sets newly created users' `.is_bot` attribute as `False`.
            if not manager.is_bot :
                manager.is_bot = True
        
        elif manager_type is ROLE_MANAGER_TYPE_INTEGRATION:
            manager = create_partial_integration_from_id(self.manager_id, role=self)
        
        else:
            manager = None
        
        return manager
    
    @property
    def guild(self):
        """
        Returns the role's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def partial(self):
        """
        Returns whether the role is partial.
        
        Partial roles have `.guild` set as ``None``.
        
        Returns
        -------
        partial : `bool`
        """
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                return guild.partial
        
        return True
    
    
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


    @classmethod
    def _create_empty(cls, role_id):
        """
        Creates an empty role with the given identifier.
        
        Parameters
        ----------
        role_id : `int`
            The role's identifier.
        
        Returns
        -------
        self : ``Role``
            The created role.
        """
        self = object.__new__(cls)
        self.id = role_id
        
        self.color = Color()
        self.guild_id = 0
        self.separated = False
        self.manager_type = ROLE_MANAGER_TYPE_NONE
        self.mentionable = False
        self.name = ''
        self.permissions = PERMISSION_NONE
        self.position = 1
        self.icon_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.unicode_emoji = None
        
        return self
