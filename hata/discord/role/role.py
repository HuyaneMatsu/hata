__all__ = ('Role', )

from scarletio import export, include

from ..bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ..color import Color
from ..core import GUILDS, ROLES
from ..http import urls as module_urls
from ..permission.permission import PERMISSION_NONE, Permission
from ..permission.utils import PERMISSION_KEY
from ..preconverters import preconvert_snowflake
from ..user import User
from ..utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_color, parse_manager, parse_mentionable, parse_name, parse_permissions, parse_position, parse_separated,
    parse_unicode_emoji, put_color_into, put_manager_into, put_mentionable_into, put_name_into, put_permissions_into,
    put_position_into, put_separated_into, put_unicode_emoji_into, validate_color, validate_manager,
    validate_manager_id, validate_manager_type, validate_mentionable, validate_name, validate_permissions,
    validate_position, validate_separated, validate_unicode_emoji
)
from .preinstanced import RoleManagerType


create_partial_integration_from_id = include('create_partial_integration_from_id')


PRECREATE_FIELDS = {
    'color': ('color', validate_color),
    'manager_id': ('manager_id', validate_manager_id),
    'manager_type': ('manager_type', validate_manager_type),
    'mentionable': ('mentionable', validate_mentionable),
    'name': ('name', validate_name),
    'permissions': ('permissions', validate_permissions),
    'position': ('position', validate_position),
    'separated': ('separated', validate_separated),
}


@export
class Role(DiscordEntity, immortal = True):
    """
    Represents a Discord guild's role.
    
    Attributes
    ----------
    color : ``Color``
        The role's color. If the color equals to `Color(0)`, then it is ignored meanwhile calculating towards a
        user's display color.
    
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
        
        Mutually exclusive with ``.unicode_emoji``
        
    icon_type : ``IconType``
        The guild's icon's type.
        
        Mutually exclusive with ``.unicode_emoji``
    
    guild_id : `int`
        The role's guild's identifier.
    
    id : `int`
        The unique identifier number of the role.
    
    manager_id : `int`
        If the role is managed, then it's manager's id if applicable. Defaults to `0`.
    
    manager_type : ``RoleManagerType``
        If the role is managed, defines by what it is.
    
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
    
    unicode_emoji : `None`, ``Emoji``
        Unicode emoji icon of the role.
        
        Mutually exclusive with ``.icon_hash`` and ``.icon_type``.
    """
    __slots__ = (
        'color', 'guild_id', 'manager_id', 'manager_type', 'mentionable', 'name', 'permissions', 'position',
        'separated', 'unicode_emoji'
    )
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.role_icon_url,
        module_urls.role_icon_url_as,
    )
    
    
    def __new__(
        cls,
        *,
        color = ...,
        icon = ...,
        manager = ...,
        mentionable = ...,
        name = ...,
        permissions = ...,
        position = ...,
        separated = ...,
        unicode_emoji = ...,
    ):
        """
        Creates a new partial role from the given fields.
        
        Parameters
        ----------
        color : `int`, ``Color``, Optional (Keyword only)
            The role's color.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The role's icon.
            
            > Mutually exclusive with the `unicode_emoji` parameter.
        
        manager : `None`, `tuple` (``RoleManagerType``, `int`), Optional (Keyword only)
            The role's manager.
        
        mentionable : `bool`, Optional (Keyword only)
            Whether the role can be mentioned.
        
        name : `str`, Optional (Keyword only)
            The role's name.
        
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions of the users having the role.
        
        position : `int`, Optional (Keyword only)
            The role's position.
        
        separated : `bool`, Optional (Keyword only)
            Users show up in separated groups by their highest `separated` role.
        
        unicode_emoji : `None`, ``Emoji``, Optional (Keyword only)
            The role's icon as an unicode emoji.
            
            > Mutually exclusive with the `icon` parameter.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - Value of invalid type given.
        ValueError
            - Value of invalid value given.
            - `icon` and `unicode_emoji` are mutually exclusive.
        """
        # color
        if color is ...:
            color = Color()
        else:
            color = validate_color(color)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
        
        # manager
        if manager is ...:
            manager_id = 0
            manager_type = RoleManagerType.none
        else:
            manager_type, manager_id = validate_manager(manager)
        
        # mentionable
        if mentionable is ...:
            mentionable = False
        else:
            mentionable = validate_mentionable(mentionable)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # permissions
        if permissions is ...:
            permissions = Permission()
        else:
            permissions = validate_permissions(permissions)
        
        # position
        if position is ...:
            position = 0
        else:
            position = validate_position(position)
        
        # separated
        if separated is ...:
            separated = False
        else:
            separated = validate_separated(separated)
        
        # unicode_emoji
        if unicode_emoji is ...:
            unicode_emoji = None
        else:
            unicode_emoji = validate_unicode_emoji(unicode_emoji)
        
        if (icon is not None) and (unicode_emoji is not None):
            raise ValueError(
                f'`icon` and `unicode_emoji` parameters are mutually exclusive, got '
                f'icon={icon!r}; unicode_emoji={unicode_emoji!r}.'
            )
        
        
        self = object.__new__(cls)
        self.color = color
        self.guild_id = 0
        self.icon = icon
        self.id = 0
        self.manager_id = manager_id
        self.manager_type = manager_type
        self.mentionable = mentionable
        self.name = name
        self.permissions = permissions
        self.position = position
        self.separated = separated
        self.unicode_emoji = unicode_emoji
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id):
        """
        Creates a role from the given `data` at the given `guild`. If the role already exists and is not partial, then
        returns it. However it is partial, then updates it as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        guild_id : `int`
            The owner guild's identifier.
        
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
            ROLES[role_id] = self
        
        else:
            if not self.partial:
                return self
        
        self.guild_id = guild_id
        self._set_attributes(data)
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            guild.roles[role_id] = self
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the role into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # color
        put_color_into(self.color, data, defaults)
        
        # icon
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        
        # id
        if include_internals:
            data['id'] = str(self.id)
        
        # manager
        if include_internals:
            put_manager_into((self.manager_type, self.manager_id), data, defaults)
        
        # mentionable
        put_mentionable_into(self.mentionable, data, defaults)
        
        # name
        put_name_into(self.name, data, defaults)
        
        # permissions
        put_permissions_into(self.permissions, data, defaults)
        
        # position
        put_position_into(self.position, data, defaults)
        
        # separated
        put_separated_into(self.separated, data, defaults)
        
        # unicode_emoji
        put_unicode_emoji_into(self.unicode_emoji, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the role's attributes from the given data.
        
        `.id` and `.guild_id` fields should be already set,
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received role data.
        """
        self.color = parse_color(data)
        self._set_icon(data)
        self.manager_type, self.manager_id = parse_manager(data)
        self.mentionable = parse_mentionable(data)
        self.name = parse_name(data)
        self.permissions = parse_permissions(data)
        self.position = parse_position(data)
        self.separated = parse_separated(data)
        self.unicode_emoji = parse_unicode_emoji(data)

    
    @classmethod
    def precreate(cls, role_id, guild_id = 0, **keyword_parameters):
        """
        Precreates a role by creating a partial one with the given parameters. When the role is loaded, then the
        precreated one will be picked up. However if the role is precreated when it already exists, then the existing
        one is picked up and is updated by the given parameters only if it is partial.
        
        Parameters
        ----------
        role_id : `int`, `str`
            The role's id.
        
        guild_id : `int` = `0`, Optional
            The role's guild's identifier.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the role.
        
        Other Parameters
        ----------------
        color : `int`, ``Color``, Optional (Keyword only)
            The role's color.

        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The role's icon.
            
            > Mutually exclusive with `icon_type`, `icon_hash` and with `unicode_emoji`.
        
        icon_type : ``IconType``, Optional (Keyword only)
            The role's icon's type.
            
            > Mutually exclusive with `icon` and with `unicode_emoji`.
            
        icon_hash : `int`, Optional (Keyword only)
            The role's icon's hash.
            
            > Mutually exclusive with `icon`  and with `unicode_emoji`.
        
        manager : `None`, `tuple` (``RoleManagerType``, `int`), Optional (Keyword only)
            The role's manager.
        
        manager_id : `None`, `int`, `str`, Optional (Keyword only)
            The role's manager's id.
        
        manager_type : ``RoleManagerType``, Optional (Keyword only)
            TIf the role is managed, defines by what it is.
        
        mentionable : `bool`, Optional (Keyword only)
            Whether the role can be mentioned.
        
        name : `str`, Optional (Keyword only)
            The name of the role.
        
        separated : `bool`, Optional (Keyword only)
            Users show up in separated groups by their highest `separated` role.
        
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions of the users having the role.
        
        position : `int`, Optional (Keyword only)
            The permissions of the users having the role.
        
        unicode_emoji : `None`, ``Emoji``
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
        guild_id = preconvert_snowflake(guild_id, 'guild_id')
        
        if keyword_parameters:
            processable = []
            
            # icon
            icon = cls.icon.parse_from_keyword_parameters(keyword_parameters)
            if (icon is not None):
                processable.append(('icon', icon))
            
            # unicode_emoji
            try:
                unicode_emoji = keyword_parameters.pop('unicode_emoji')
            except KeyError:
                unicode_emoji = None
            else:
                unicode_emoji = validate_unicode_emoji(unicode_emoji)
                if (unicode_emoji is not None):
                    processable.append(('unicode_emoji', unicode_emoji))
            
            # Mutually exclusive check
            if (icon is not None) and (unicode_emoji is not None):
                raise ValueError(
                    f'`icon` and `unicode_emoji` parameters are mutually exclusive, got '
                    f'icon={icon!r}; unicode_emoji={unicode_emoji!r}.'
                )
            
            # manager
            try:
                manager = keyword_parameters.pop('manager')
            except KeyError:
                pass
            else:
                manager_type, manager_id = validate_manager(manager)
                processable.append(('manager_type', manager_type))
                processable.append(('manager_id', manager_id))
            
            extra = None
            
            while keyword_parameters:
                field_name, field_value = keyword_parameters.popitem() 
                try:
                    attribute_name, validator = PRECREATE_FIELDS[field_name]
                except KeyError:
                    if extra is None:
                        extra = {}
                    extra[field_name] = field_value
                    continue
                
                attribute_value = validator(field_value)
                processable.append((attribute_name, attribute_value))
                continue
                
            if (extra is not None):
                raise TypeError(
                    f'Unused or unsettable keyword parameters: {extra!r}.'
                )
        
        else:
            processable = None
        
        try:
            self = ROLES[role_id]
        except KeyError:
            self = cls._create_empty(role_id, guild_id)
            ROLES[role_id] = self
        else:
            if (not self.partial):
                return self
            
            if guild_id and (not self.guild_id):
                self.guild_id = guild_id
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    def _update_attributes(self, data):
        """
        Updates the role with the given `data` with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Role data received from Discord.
        """
        clear_permission_cache = False
        
        # color
        self.color = parse_color(data)
        
        # icon
        self._set_icon(data)
        
        # manager
        if self.manager_type is RoleManagerType.unset:
            self.manager_type, self.manager_id = parse_manager(data)
        
        # mentionable
        self.mentionable = parse_mentionable(data)
        
        # name
        self.name = parse_name(data)
        
        # permissions
        permissions = Permission(data[PERMISSION_KEY])
        if self.permissions != permissions:
            self.permissions = permissions
            clear_permission_cache = True
        
        # position
        position = parse_position(data)
        if self.position != position:
            self.position = position
            clear_permission_cache = True
        
        # separated
        self.separated = parse_separated(data)
        
        # unicode_emoji
        self.unicode_emoji = parse_unicode_emoji(data)
        
        if clear_permission_cache:
            self._clear_permission_cache()
    
    
    def _clear_permission_cache(self):
        """
        Clears the role's guild's permission cache.
        """
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
        repr_parts = ['<', self.__class__.__name__]
        
        role_id = self.id
        if role_id:
            repr_parts.append(' role_id=')
            repr_parts.append(repr(role_id))
        
        if self.partial:
            repr_parts.append(' (partial)')
    
        else:
            if role_id:
                repr_parts.append(',')
            
            repr_parts.append(' name=')
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
        | unicode_emoji | `None`, ``Emoji``     |
        +---------------+-----------------------+
        """
        old_attributes = {}
        
        clear_permission_cache = False
        
        # color
        color = parse_color(data)
        if self.color != color:
            old_attributes['color'] = self.color
            self.color = color
        
        # icon
        self._update_icon(data, old_attributes)
        
        # managed
        if self.manager_type is RoleManagerType.unset:
            self.manager_type, self.manager_id = parse_manager(data)
        
        # mentionable
        mentionable = parse_mentionable(data)
        if self.mentionable != mentionable:
            old_attributes['mentionable'] = self.mentionable
            self.mentionable = mentionable
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # permissions
        permissions = parse_permissions(data)
        if self.permissions != permissions:
            old_attributes['permissions'] = self.permissions
            self.permissions = permissions
            clear_permission_cache = True
        
        # position
        position = parse_position(data)
        if self.position != position:
            old_attributes['position'] = self.position
            self.position = position
            clear_permission_cache = True
        
        # separated
        separated = parse_separated(data)
        if self.separated != separated:
            old_attributes['separated'] = self.separated
            self.separated = separated
        
        # unicode_emoji
        unicode_emoji = parse_unicode_emoji(data)
        if self.unicode_emoji is not unicode_emoji:
            old_attributes['unicode_emoji'] = self.unicode_emoji
            self.unicode_emoji = unicode_emoji
        
        if clear_permission_cache:
            self._clear_permission_cache()
        
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
                                    role_ids = (*role_ids[:index], *role_ids[index + 1:])
                                guild_profile.role_ids = role_ids
    
    
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
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"m"!r}.'
        )
    
    
    @property
    def users(self):
        """
        Returns the users who have the role.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
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
                        role_ids = guild_profile.role_ids
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
        return (self.manager_type is not RoleManagerType.none)
    
    
    @property
    def manager(self):
        """
        Returns the manager entity of the role if applicable.
        
        Returns
        -------
        manager : `None`, ``ClientUserBase``, ``Integration``
        """
        manager_type = self.manager_type
        if manager_type is RoleManagerType.none:
            manager = None
        
        elif manager_type is RoleManagerType.bot:
            manager = User.precreate(self.manager_id, bot = True)
        
        elif manager_type is RoleManagerType.integration:
            manager = create_partial_integration_from_id(self.manager_id, self.id)
        
        else:
            manager = None
        
        return manager
    
    
    @property
    def guild(self):
        """
        Returns the role's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
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
                if (not guild.partial) and (self.id in guild.roles):
                    return False
        
        return True
    
    
    def __eq__(self, other):
        """Returns whether the two roles are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id == other_id
        
        return self._is_equal_partial(other)
    
    
    def __ne__(self, other):
        """Returns whether the two roles are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id != other_id
        
        return not self._is_equal_partial(other)
    
    
    def __gt__(self, other):
        """Returns whether this role's position is higher than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.position > other.position:
            return True
        
        if self.position == other.position:
            if self.id > other.id:
                return True
    
        return False
    
    
    def __ge__(self, other):
        """Returns whether this role's position is higher or equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
            
        if self.position > other.position:
            return True
        
        if self.position == other.position:
            if self.id >= other.id:
                return True
        
        return False
    
        
    def __le__(self, other):
        """Returns whether this role's position is less or equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.position < other.position:
            return True
        
        if self.position == other.position:
            if self.id <= other.id:
                return True
        
        return False
        
    
    
    def __lt__(self, other):
        """Returns whether this role's position is less than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.position < other.position:
            return True
        
        if self.position == other.position:
            if self.id < other.id:
                return True
        
        return False
    
    
    def __hash__(self):
        """Returns the role's hash value."""
        role_id = self.id
        if role_id:
            return role_id
        
        return self._get_hash_partial()
    
    
    @classmethod
    def _create_empty(cls, role_id, guild_id):
        """
        Creates an empty role with the given identifier.
        
        Parameters
        ----------
        role_id : `int`
            The role's identifier.
        guild_id : `int`
            The role's guild's identifier.
        
        Returns
        -------
        self : ``Role``
            The created role.
        """
        self = object.__new__(cls)
        self.id = role_id
        
        self.color = Color()
        self.guild_id = guild_id
        self.separated = False
        self.manager_id = 0
        self.manager_type = RoleManagerType.none
        self.mentionable = False
        self.name = ''
        self.permissions = PERMISSION_NONE
        self.position = 1
        self.icon_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.unicode_emoji = None
        
        return self
    
    
    def _is_equal_partial(self, other):
        """
        Returns whether the role is equal to the given one.
        This function is called when one or both the roles are partial.
        
        Parameters
        ----------
        other : ``instance<type<self>>``
            The other role to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # color
        if self.color != other.color:
            return False
        
        # icon
        if self.icon != other.icon:
            return False
        
        # guild_id
        # SKip it, non partial field
        
        # id
        # Skip it, non partial field
        
        # manager_id
        if self.manager_id != other.manager_id:
            return False
        
        # manager_type
        if self.manager_type != other.manager_type:
            return False
        
        # mentionable
        if self.mentionable != other.mentionable:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # permissions
        if self.permissions != other.permissions:
            return False
        
        # position
        if self.position != other.position:
            return False
        
        # separated
        if self.separated != other.separated:
            return False
        
        # unicode_emoji
        if self.unicode_emoji is not other.unicode_emoji:
            return False
        
        return True
    
    
    def _get_hash_partial(self):
        """
        Returns the role's hash value.
        This function is called when the role is partial.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # color
        hash_value ^= self.color
        
        # icon
        hash_value ^= hash(self.icon)
        
        # guild_id
        # SKip it, non partial field
        
        # id
        # Skip it, non partial field
        
        # manager_id
        hash_value ^= self.manager_id
        
        # manager_type
        hash_value ^= hash(self.manager_type) << 24
        
        # mentionable
        hash_value ^= self.mentionable << 28
        
        # name
        hash_value ^= hash(self.name)
        
        # permissions
        hash_value ^= self.permissions
        
        # position
        hash_value ^= self.position << 29
        
        # separated
        hash_value ^= self.separated << 37
        
        # unicode_emoji
        unicode_emoji = self.unicode_emoji
        if (unicode_emoji is not None):
            hash_value ^= self.unicode_emoji.id << 38
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the role returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        new.color = self.color
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.guild_id = 0
        new.id = 0
        new.manager_id = self.manager_id
        new.manager_type = self.manager_type
        new.mentionable = self.mentionable
        new.name = self.name
        new.permissions = self.permissions
        new.position = self.position
        new.separated = self.separated
        new.unicode_emoji = self.unicode_emoji
        return new
    
    
    def copy_with(
        self,
        *,
        color = ...,
        icon = ...,
        manager = ...,
        mentionable = ...,
        name = ...,
        permissions = ...,
        position = ...,
        separated = ...,
        unicode_emoji = ...,
    ):
        """
        Copies the role with modifying its defined fields, returning a new partial one.
        
        Parameters
        ----------
        color : `int`, ``Color``, Optional (Keyword only)
            The role's color.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The role's icon.
            
            > Mutually exclusive with the `unicode_emoji` parameter.
        
        manager : `None`, `tuple` (``RoleManagerType``, `int`), Optional (Keyword only)
            The role's manager.
        
        mentionable : `bool`, Optional (Keyword only)
            Whether the role can be mentioned.
        
        name : `str`, Optional (Keyword only)
            The role's name.
        
        permissions : `int`, ``Permission``, Optional (Keyword only)
            The permissions of the users having the role.
        
        position : `int`, Optional (Keyword only)
            The role's position.
        
        separated : `bool`, Optional (Keyword only)
            Users show up in separated groups by their highest `separated` role.
        
        unicode_emoji : `None`, ``Emoji``, Optional (Keyword only)
            The role's icon as an unicode emoji.
            
            > Mutually exclusive with the `icon` parameter.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Value of invalid type given.
        ValueError
            - Value of invalid value given.
            - `icon` and `unicode_emoji` are mutually exclusive.
        """
        # Make sure by passing only either `icon` / `unicode_emoji` we wont raise error by nulling out the existing.
        if (icon is ...):
            self_unicode_emoji = self.unicode_emoji
        else:
            self_unicode_emoji = None
        
        if (unicode_emoji is ...):
            self_icon = self.icon
        else:
            self_icon = None
        
        # color
        if color is ...:
            color = self.color
        else:
            color = validate_color(color)
        
        # icon
        if icon is ...:
            icon = self_icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
        
        # manager
        if manager is ...:
            manager_id = self.manager_id
            manager_type = self.manager_type
        else:
            manager_type, manager_id = validate_manager(manager)
        
        # mentionable
        if mentionable is ...:
            mentionable = self.mentionable
        else:
            mentionable = validate_mentionable(mentionable)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # permissions
        if permissions is ...:
            permissions = self.permissions
        else:
            permissions = validate_permissions(permissions)
        
        # position
        if position is ...:
            position = self.position
        else:
            position = validate_position(position)
        
        # separated
        if separated is ...:
            separated = self.separated
        else:
            separated = validate_separated(separated)
        
        # unicode_emoji
        if unicode_emoji is ...:
            unicode_emoji = self_unicode_emoji
        else:
            unicode_emoji = validate_unicode_emoji(unicode_emoji)
        
        if (icon is not None) and (unicode_emoji is not None):
            raise ValueError(
                f'`icon` and `unicode_emoji` parameters are mutually exclusive, got '
                f'icon={icon!r}; unicode_emoji={unicode_emoji!r}.'
            )
        
        
        new = object.__new__(type(self))
        new.color = color
        new.guild_id = 0
        new.icon = icon
        new.id = 0
        new.manager_id = manager_id
        new.manager_type = manager_type
        new.mentionable = mentionable
        new.name = name
        new.permissions = permissions
        new.position = position
        new.separated = separated
        new.unicode_emoji = unicode_emoji
        return new
