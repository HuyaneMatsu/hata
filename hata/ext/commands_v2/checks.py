"""
Checks can be added to commands or to categories to limit their usage to set users or places.


Checks can be either used as a decorator:

```py
from hata.ext.commands import checks

@Momiji.commands
@checks.owner_only()
async def knock_knock():
    return 'Awu!'
```

Or as a `.commands` parameter:

```py
from hata.ext.commands import checks

@Momiji.commands(checks=checks.owner_only())
async def knock_knock():
    return 'Awu!'
```

The implemented checks are the following:

+--------------------------------+-----------------+--------------------------------------------------------------+
| Name                           | Extra parameter | Description                                                  |
+================================+=================+==============================================================+
| announcement_channel_only      | N/A             | Whether the message's channel is an announcement channel.    |
+--------------------------------+-----------------+--------------------------------------------------------------+
| booster_only                   | N/A             | Whether the user boosts the respective guild.                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| bot_account_only               | N/A             | Whether the message's author is a bot account.               |
+--------------------------------+-----------------+--------------------------------------------------------------+
| client_only                    | N/A             | Whether the message was sent by a ``Client``.                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| custom                         | function        | Custom checks, to wrap a given `function`. (Can be async.)   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_only                     | N/A             | Whether the message was sent to a guild channel.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_owner_only               | N/A             | Whether the message's author is the guild's owner.           |
|                                |                 | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_any_role                   | *roles          | Whether the message's author has any of the given roles.     |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_client_guild_permissions   | permissions,    | Whether the client has the given permissions at the guild.   |
|                                | **kwargs        | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_client_permissions         | permissions,    | Whether the client has the given permissions at the channel. |
|                                | **kwargs        |                                                              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_guild_permissions          | permissions,    | Whether the message's author has the given permissions at    |
|                                | **kwargs        | the guild. (Fails in private channels.)                      |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_permissions                | permissions,    | Whether the message's author has the given permissions at    |
|                                | **kwargs        | the channel.                                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_role                       | role            | Whether the message's author has the given role.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_any_category                | *categories     | Whether the message was sent into a channel, what's category |
|                                |                 | is any of the specified ones.                                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_any_channel                 | *channels       | Whether the message was sent to any of the given channels.   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_any_guild                   | *guilds         | Whether the message was sent to any of the given guilds.     |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_category                    | category        | Whether the message was sent into a channel, what's category |
|                                |                 | is the specified one.                                        |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_channel                     | channel         | Whether the message's channel is the given one.              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_guild                       | guild           | Whether the message guild is the given one.                  |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_in_voice                    | N/A             | Whether the user is in a voice channel in the respective     |
|                                |                 | guild.                                                       |
+--------------------------------+-----------------+--------------------------------------------------------------+
| release_at                     | release_at,     | Whether the command is already released. Users with the      |
|                                | *roles          | given roles and the bot owners bypass the check.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| nsfw_channel_only              | N/A             | Whether the message's channel is nsfw.                       |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_only                     | N/A             | Whether the message's author is an owner of the client.      |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_guild_owner_only      | N/A             | `owner_only`, `guild_owner` (Fails in private channels.)   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_any_role          | *roles          | `owner_only`, `has_any_role`                               |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_guild_permissions | permissions,    | `owner_only`, `has_guild_permissions`                      |
|                                | **kwargs        | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_permissions       | permissions,    | `owner_only`, `has_permissions`                            |
|                                | **kwargs        |                                                              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_role              | role            | `owner_only`, `has_role`                                   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| private_only                   | N/A             | Whether the message's channel is a private channel.          |
+--------------------------------+-----------------+--------------------------------------------------------------+
| user_account_only              | N/A             | Whether the message's author is a user account.              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| user_account_or_client_only    | N/A             | Whether the message's author is a user account or a          |
|                                |                 | ``Client``.                                                  |
+--------------------------------+-----------------+--------------------------------------------------------------+

To handle a failed check, do:

```py
from hata.ext.commands import checks, CommandCheckError

@Momiji.commands
@checks.owner_only()
async def knock_knock():
    return 'Awu!'

@knock_knock.error
async def error_handler(ctx, exception):
    # `exception` is ``CommandCheckError`` if a check fails.
    if isinstance(err, CommandCheckError):
        await ctx.send('Owner only!')
        # Return `True` if we handled the exception and further error handles should not be called.
        return True
    
    return False
```
"""

__all__ = (
    'CheckBase',
    'announcement_channel_only',
    'booster_only',
    'bot_account_only',
    'client_only',
    'custom',
    'guild_only',
    'guild_owner_only',
    'has_any_role',
    'has_client_guild_permissions',
    'has_client_permissions',
    'has_guild_permissions',
    'has_permissions',
    'has_role',
    'is_any_category',
    'is_any_channel',
    'is_any_guild',
    'is_category',
    'is_channel',
    'is_guild',
    'is_in_voice',
    'release_at',
    'nsfw_channel_only',
    'owner_only',
    'owner_or_guild_owner_only',
    'owner_or_has_any_role',
    'owner_or_has_guild_permissions',
    'owner_or_has_permissions',
    'owner_or_has_role',
    'private_only',
    'user_account_only',
    'user_account_or_client_only',
)

from datetime import datetime
from functools import partial as partial_func

from scarletio import CallableAnalyzer, Task, copy_docs, export

from ...discord.bases import instance_or_id_to_instance, instance_or_id_to_snowflake
from ...discord.channel import Channel
from ...discord.client import Client
from ...discord.core import KOKORO
from ...discord.guild import Guild
from ...discord.permission import Permission
from ...discord.role import Role
from ...discord.user import ClientUserBase
from ...discord.utils import datetime_to_id

from .wrappers import CommandCheckWrapper


def _convert_permission(permission):
    """
    Validates the given `permission`.
    
    Parameters
    ----------
    permission : `None`, ``Permission``, `int`.
        Permission to validate.
    
    Returns
    -------
    permissions : ``Permission``
    
    Raises
    ------
    TypeError
        If `permissions` was not given as `None`, ``Permission`` nor as `int`.
    """
    if permission is None:
        permission = Permission()
    else:
        if type(permission) is Permission:
            pass
        elif isinstance(permission, int):
            permission = Permission(permission)
        else:
            raise TypeError(
                f'`permission` can be `None`, `{Permission.__name__}`, `int`, got '
                f'{permission.__class__.__name__}; {permission!r}.'
            )
    
    return permission


class CheckMeta(type):
    """
    Check metaclass for collecting their `__slots__` in a `__all_slot__` class attribute.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``CheckMeta``
        """
        if class_parents:
            parent = class_parents[0]
            inherited_slots = getattr(parent, '__all_slot__', None)
        else:
            inherited_slots = None
        
        new_slots = class_attributes.get('__slots__', None)
        
        final_slots = []
        if (inherited_slots is not None):
            final_slots.extend(inherited_slots)
        
        if (new_slots is not None):
            final_slots.extend(new_slots)
        
        class_attributes['__all_slot__'] = tuple(final_slots)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


@export
class CheckBase(metaclass=CheckMeta):
    """
    Base class for checks.
    """
    __slots__ = ()
    def __new__(cls):
        """
        Creates a new check instance.
        
        Subclasses should overwrite it.
        """
        return object.__new__(cls)
    
    async def __call__(client, context):
        """
        Returns whether the check's condition passes.
        
        Subclasses should overwrite it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        context : ``CommandContext``
            Processing context for the respective command.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
    
    def __repr__(self):
        """Returns the check's representation."""
        repr_parts = [
            self.__class__.__name__,
            '(',
        ]
        
        slots = self.__all_slot__
        limit = len(slots)
        if limit:
            index = 0
            while True:
                name = slots[index]
                index += 1
                if name.startswith('_'):
                    if index == limit:
                        break
                    else:
                        continue
                
                # case of `channel_id`, `guild_id`
                if name.endswith('id'):
                    display_name = name[:-3]
                # case of `channel_ids`, `guild_ids`
                elif name.endswith('ids'):
                    display_name = name[:-4]
                else:
                    display_name = name
                
                repr_parts.append(display_name)
                repr_parts.append('=')
                attr = getattr(self,name)
                repr_parts.append(repr(attr))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)
    
    def __invert__(self):
        """Inverts the check's condition returning a new check."""
        return CheckInvert(self)
    
    def __or__(self, other):
        """Connects the two check with `or` relation."""
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if type(self) is CheckBase:
            return other
        
        return CheckOrRelation(self, other)
    
    def __and__(self, other):
        """Connects the two checks which `and` relation."""
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if type(self) is CheckBase:
            return self
        
        return CheckAndRelation(self, other)


class CheckInvert(CheckBase):
    """
    Inverts the wrapped check's result.
    
    Attributes
    ----------
    check : ``CheckBase``
        The check to invert.
    """
    __slots__ = ('check', )
    
    def __new__(cls, check):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        check : ``CheckBase``
            The check to invert.

        Raises
        ------
        TypeError
            If `check` was not given as ``CheckBase``.
        """
        if not isinstance(check, CheckBase):
            raise TypeError(
                f'`check` can be `{CheckBase.__name__}`, got {check.__class__.__name__}; {check!r}.'
            )
        
        self = object.__new__(cls)
        self.check = check
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        return not await self.check(context)


class CheckRelationBase(CheckBase):
    """
    Base class for relation checks.
    
    Attributes
    ----------
    checks : `tuple` of ``CheckBase``
        The check to connect.
    """
    __slots__ = ('checks', )
    
    def __new__(cls, *checks):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *checks : ``CheckBase``
            The check to invert.

        Raises
        ------
        TypeError
            If a `check` was not given as ``CheckBase``.
        """
        for check in checks:
            if not isinstance(check, CheckBase):
                raise TypeError(
                    f'`check` can be `{CheckBase.__name__}`, got {check.__class__.__name__}; {check!r}.'
                )
        
        self = object.__new__(cls)
        self.checks = checks
        return self


class CheckOrRelation(CheckRelationBase):
    """
    Connects checks with `or` relation.
    
    Attributes
    ----------
    checks : `tuple` of ``CheckBase``
        The check to connect.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        for check in self.checks:
            if await check(context):
                return True
        
        return False


class CheckAndRelation(CheckRelationBase):
    """
    Connects checks with `and` relation.
    
    Attributes
    ----------
    checks : `tuple` of ``CheckBase``
        The check to connect.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        for check in self.checks:
            if not await check(context):
                return False
        
        return True



class CheckSingleBase(CheckBase):
    """
    Base class for single condition checks without attributes.
    """
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if other_type is type(self):
            return self
        
        return CheckOrRelation(self, other)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if other_type is type(self):
            return self
        
        return CheckAndRelation(self, other)


class CheckIsOwner(CheckSingleBase):
    """
    Checks whether the command was called by the client's owner.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if context.client.is_owner(context.message.author):
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if other_type is type(self):
            return self
        
        # Let the other check decide
        return other | self
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if type(self) is other_type:
            return self
        
        if issubclass(other, CheckIsOwner):
            if (type(self) is CheckIsOwner):
                return self
            
            if type(other) is CheckIsOwner:
                return other
        
        return CheckAndRelation(self, other)


class CheckHasRoleBase(CheckBase):
    """
    Base class for role checks.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckHasRoleBase):
            return CheckOrRelation(self, other)
        
        roles = {*self._iter_roles(), *other._iter_roles()}
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_allowed = True
        else:
            owner_allowed = False
        
        if owner_allowed:
            check_type = CheckHasRoleOrIsOwner
        else:
            check_type = HasAnyRoleCheckOrRelationIsOwner
        
        return check_type(*roles)
    
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if not issubclass(other_type, CheckHasRoleBase):
            return CheckAndRelation(self, other)
        
        roles = {*self._iter_roles()}&{*other._iter_roles()}
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_required = True
        else:
            owner_required = False
        
        if owner_required:
            check_type = CheckHasRoleOrIsOwner
        else:
            check_type = HasAnyRoleCheckOrRelationIsOwner
        
        return check_type(*roles)
    
    
    def _iter_roles(self):
        """
        Iterates the roles of the check.
        
        This method is a generator.
        
        Yields
        ------
        role : ``Role``
        """
        return
        yield


class CheckHasRole(CheckHasRoleBase):
    """
    Checks whether the message's author has the given role.
    
    Attributes
    ----------
    role : ``Role``
        The legend itself.
    """
    __slots__ = ('role', )
    
    def __new__(cls, role):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        role : `str`, `int`, ``Role``
            The role what the message's author should have.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role``, `str`, `int`.
        ValueError
            If `role` was given as `str`, `int`, but not as a valid snowflake, so ``Role``
            cannot be precreated with it.
        """
        role = instance_or_id_to_instance(role, Role, 'role')
        
        self = object.__new__(cls)
        self.role = role
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if context.message.author.has_role(self.role):
            return True
        
        return False
    
    @copy_docs(CheckHasRoleBase._iter_roles)
    def _iter_roles(self):
        yield self.role

class CheckHasRoleOrIsOwner(CheckHasRole, CheckIsOwner):
    """
    Checks whether the message's author has the given role, or if it the client's owner.
    
    Attributes
    ----------
    role : ``Role``
        The legend itself.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        user = context.message.author
        if user.has_role(self.role):
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckHasAnyRole(CheckHasRoleBase):
    """
    Checks whether the message's author has any of the given roles.
    
    Attributes
    ----------
    roles : `set` of ``Role``
        The legends themselves.
    """
    __slots__ = ('roles', )
    
    def __new__(cls, *roles):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *roles : `str`, `int`, ``Role``
            Role from which the message's author should have at least one.
        
        Raises
        ------
        TypeError
            If a role was not given neither as ``Role``, `str`, `int`.
        ValueError
            If a role was given as `str`, `int`, but not as a valid snowflake, so a ``Role``
            cannot be precreated with it.
        """
        roles_processed = set()
        for role in roles:
            role = instance_or_id_to_instance(role, Role, 'role')
            roles_processed.add(role)
        
        roles_processed_length = len(roles_processed)
        if roles_processed_length == 0:
            return CheckBase()
        
        if roles_processed_length == 1:
            return CheckHasRole(roles_processed.pop())
        
        self = object.__new__(cls)
        self.roles = roles_processed
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        user = context.message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        return False
    
    @copy_docs(CheckHasRoleBase._iter_roles)
    def _iter_roles(self):
        yield from self.roles


class HasAnyRoleCheckOrRelationIsOwner(CheckHasAnyRole, CheckIsOwner):
    """
    Checks whether the message's author has any of the given roles, or whether is it the client's owner.
    
    Attributes
    ----------
    roles : `set` of ``Role``
        The roles from what the user should have at least 1.
    """
    __slots__ = ()
    
    def __new__(cls, *roles):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *roles : `str`, `int`, ``Role``
            Role from which the message's author should have at least one.
        
        Raises
        ------
        TypeError
            If an element of role was not given neither as ``Role``, `str`, `int`.
        ValueError
            If a role was given as `str`, `int`, but not as a valid snowflake, so a ``Role``
            cannot be precreated with it.
        """
        roles_processed = set()
        for role in roles:
            role = instance_or_id_to_instance(role, Role, 'role')
            roles_processed.add(role)
        
        roles_processed_length = len(roles_processed)
        if roles_processed_length == 0:
            return CheckIsOwner()
        
        if roles_processed_length == 1:
            return CheckHasRoleOrIsOwner(roles_processed.pop())
        
        self = object.__new__(cls)
        self.roles = roles_processed
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        user = context.message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckIsInGuild(CheckSingleBase):
    """
    Checks whether the command was called from a guild.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        return context.message.channel.is_in_group_guild()
    
    @copy_docs(CheckBase.__invert__)
    def __invert__(self):
        return CheckIsInPrivate()


class CheckIsInPrivate(CheckSingleBase):
    """
    Checks whether the command was used inside of a private channel.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        return context.message.channel.is_in_group_private()
    
    @copy_docs(CheckBase.__invert__)
    def __invert__(self):
        return CheckIsInGuild()


class CheckIsGuildOwner(CheckBase):
    """
    Checks whether the command was called by the local guild's owner.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.context
        guild = message.guild
        if guild is None:
            return False
        
        if guild.owner_id == message.author.id:
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if other_type is type(self):
            return self
        
        if other_type is not CheckIsOwner:
            return CheckOrRelation(self, other)
        
        if isinstance(self, CheckIsOwner):
            return self
        
        return CheckIsGuildOwnerOrIsOwner()


class CheckIsGuildOwnerOrIsOwner(CheckIsGuildOwner, CheckIsOwner):
    """
    Checks whether a message was sent by the message's guild's owner or by the client's owner.
    
    > Guild check is always applied.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.context
        guild = message.guild
        if guild is None:
            return False
        
        user = message.author
        if guild.owner_id == user.id:
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckHasPermissionBase(CheckBase):
    """
    Base class for checking permissions.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    def __new__(cls, permission = None, **kwargs):
        """
        Creates a check, which will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        permissions : `None`, ``Permission``, `int` = `None`, Optional
            The permission, which the respective user should have. Defaults to `None`
        **kwargs : Keyword parameters
            `permission-name` - `bool` relations.
        
        Raises
        ------
        LookupError
            If a keyword is not a valid permission name.
        TypeError
            If `permission` was not given neither as `None`, ``Permission`` nor as `int`.
        """
        permission = _convert_permission(permission)
        permission = permission.update_by_keys(**kwargs)
        
        if not permission:
            if issubclass(cls, CheckIsOwner):
                permission_type = CheckIsOwner
            else:
                permission_type = CheckBase
            
            return permission_type()
        
        self = object.__new__(cls)
        self.permission = permission
        return self


class CheckHasPermission(CheckHasPermissionBase):
    """
    Checks whether the message's author has the given permissions in the message's channel.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        if message.channel.permissions_for(message.author) >= self.permission:
            return True
        
        return False

    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckHasPermission):
            return CheckAndRelation(self, other)
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_allowed = True
        else:
            owner_allowed = False
        
        permission = Permission(self.permission & other.permission)
        
        if owner_allowed:
            check_type = CheckHasPermissionOrIsOwner
        else:
            check_type = CheckHasPermission
        
        return check_type(permission)
    
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckHasPermission):
            return CheckOrRelation(self, other)
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_required = True
        else:
            owner_required = False
        
        permission = Permission(self.permission | other.permission)
        if permission:
            if owner_required:
                check_type = CheckHasPermissionOrIsOwner
            else:
                check_type = CheckHasPermission
            
            return check_type(permission)
        else:
            if owner_required:
                check_type = CheckIsOwner
            else:
                check_type = CheckBase
            
            return check_type()



class CheckHasPermissionOrIsOwner(CheckHasPermission, CheckIsOwner):
    """
    Checks whether the message's author is the client's owner or has the given permissions in the message's channel.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        user = message.author
        if message.channel.permissions_for(user) >= self.permission:
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckHasGuildPermission(CheckHasPermissionBase):
    """
    Checks whether the message's author has the given permissions in the message's guild.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        guild = message.guild
        if guild is None:
            return False
        
        if guild.permissions_for(message.author) >= self.permission:
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckHasGuildPermission):
            return CheckOrRelation(self, other)
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_allowed = True
        else:
            owner_allowed = False
        
        permission = Permission(self.permission & other.permission)
        
        if owner_allowed:
            check_type = CheckHasGuildPermissionOrIsOwner
        else:
            check_type = CheckHasGuildPermission
        
        return check_type(permission)
    
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckHasGuildPermission):
            return CheckAndRelation(self, other)
        
        if isinstance(self, CheckIsOwner) or issubclass(other_type, CheckIsOwner):
            owner_required = True
        else:
            owner_required = False
        
        permission = Permission(self.permission | other.permission)
        if permission:
            if owner_required:
                check_type = CheckHasGuildPermissionOrIsOwner
            else:
                check_type = CheckHasGuildPermission
            
            return check_type(permission)
        else:
            if owner_required:
                check_type = CheckIsOwner
            else:
                check_type = CheckBase
            
            return check_type()


class CheckHasGuildPermissionOrIsOwner(CheckHasGuildPermission, CheckIsOwner):
    """
    Checks whether the message's author has the given permissions in the message's guild.
    
    > Guild check is always applied.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        guild = message.guild
        if guild is None:
            return False
        
        user = message.author
        if guild.permissions_for(user) >= self.permission:
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckHasClientPermission(CheckHasPermissionBase):
    """
    Checks whether the client has the given permissions in the message's channel.
    
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if context.message.channel.cached_permissions_for(context.client) >= self.permission:
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if type(self) is not other_type:
            return CheckOrRelation(self, other)
        
        permission = Permission(self.permission & other.permission)
        
        return type(self)(permission)
    
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if type(self) is not other_type:
            return CheckOrRelation(self, other)
        
        permission = Permission(self.permission | other.permission)
        
        if not permission:
            return CheckBase()
        
        return type(self)(permission)


class CheckHasClientGuildPermission(CheckHasClientPermission):
    """
    Checks whether the client has the given permissions in the message's guild.
    
    Attributes
    ----------
    permission : ``Permission``
        The required permissions to pass the check.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        guild = context.message.guild
        if guild is None:
            return False
        
        if guild.cached_permissions_for(context.client) >= self.permission:
            return True
        
        return False


class CheckIsGuildBase(CheckBase):
    """
    Base class fro guild checks.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckIsGuildBase):
            return CheckOrRelation(self, other)
        
        guild_ids = {*self._iter_guild_ids(), *other._iter_guild_ids()}
        
        return CheckIsAnyGuild(*guild_ids)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if not issubclass(other_type, CheckIsGuildBase):
            return CheckAndRelation(self, other)
    
        guild_ids = {*self._iter_guild_ids()}&{*other._iter_guild_ids()}
        
        return CheckIsAnyGuild(*guild_ids)
    
    def _iter_guild_ids(self):
        """
        Iterates the guild ids of the check.
        
        This method is a generator.
        
        Yields
        ------
        guild_id : ``int``
        """
        return
        yield
    
    
class CheckIsGuild(CheckIsGuildBase):
    """
    Checks whether the message was sent to the given guild.
    
    Attributes
    ----------
    guild_id : `int`
        The respective guild's id.
    """
    __slots__ = ('guild_id', )
    
    def __new__(cls, guild):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        guild : `str`, `int`, ``Guild``
            The guild where the message should be sent.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, `str`, `int`.
        ValueError
            If `guild` was given as `str`, `int`, but not as a valid snowflake.
        """
        guild_id = instance_or_id_to_snowflake(guild, Guild, 'guild')
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        guild = context.message.guild
        if guild is None:
            return False
        
        if (guild.id == self.guild_id):
            return True
        
        return False
    
    @copy_docs(CheckIsGuildBase._iter_guild_ids)
    def _iter_guild_ids(self):
        yield self.guild_id


class CheckIsAnyGuild(CheckIsGuildBase):
    """
    Checks whether the message was sent into any of the given guilds.
    
    Attributes
    ----------
    guild_ids : `set` of `int`
        The respective guilds' identifiers.
    """
    __slots__ = ('guild_ids', )
    
    def __new__(cls, *guilds):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *guilds : `str`, `int`, ``Guild``
            The guilds where the message should be sent.
        
        Raises
        ------
        TypeError
            If a guild was not given neither as ``Guild``, `str`, `int`.
        ValueError
            If a guild was given as `str`, `int`, but not as a valid snowflake.
        """
        guild_ids_processed = set()
        
        for guild in guilds:
            guild_id = instance_or_id_to_snowflake(guild, Guild, 'guild')
            guild_ids_processed.add(guild_id)
        
        guild_ids_processed_length = len(guild_ids_processed)
        if guild_ids_processed_length == 0:
            return CheckBase()
        
        if guild_ids_processed_length == 1:
            return CheckIsGuild(guild_ids_processed.pop())
        
        self = object.__new__(cls)
        self.guild_ids = guild_ids_processed
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        guild = context.message.guild
        if guild is None:
            return False
        
        if (guild.id in self.guild_ids):
            return True
        
        return False
    
    @copy_docs(CheckIsGuildBase._iter_guild_ids)
    def _iter_guild_ids(self):
        yield from self.guild_ids


class CheckCustom(CheckBase):
    """
    Does a custom check.
    
    Attributes
    ----------
    _is_async : `bool`
        Whether ``.check`` is async.
    check : `callable`
        The custom check's function.
    """
    __slots__ = ('_is_async', 'check', )

    def __new__(cls, check):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        check : `callable`
            The custom check which should pass. Can be async.
        
        Raises
        ------
        TypeError
            - If `check` was not given as an `callable`.
            - If `check` accepts more or less non reserved positional non default parameters.
        
        Notes
        -----
        Only `int`-s are evaluated to boolean.
        """
        analyzer = CallableAnalyzer(check)
        non_reserved_positional_parameter_count = analyzer.get_non_reserved_positional_parameter_count()
        if  non_reserved_positional_parameter_count != 1:
            raise TypeError(
                f'`check` should accept `1` non reserved, positional, non default parameters, meanwhile it accepts '
                f'{non_reserved_positional_parameter_count}, got {check!r}.'
            )
        
        is_async = analyzer.is_async()
        
        self = object.__new__(cls)
        self.check = check
        self._is_async = is_async
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        try:
            result = self.check(context)
            if self._is_async:
                result = await result
        except GeneratorExit:
            raise
        
        except BaseException as err:
            client = context.client
            Task(KOKORO, client.events.error(client, repr(self), err))
            return False
        
        if result is None:
            return False
        
        if isinstance(result, int) and result:
            return True
        
        return False


class CheckIsChannelBase(CheckBase):
    """
    Base class for channel checks.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckIsChannelBase):
            return CheckOrRelation(self, other)
        
        channel_ids = {*self._iter_channel_ids(), *other._iter_channel_ids()}
        
        return CheckIsAnyChannel(*channel_ids)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if not issubclass(other_type, CheckIsChannelBase):
            return CheckAndRelation(self, other)
    
        channel_ids = {*self._iter_channel_ids()}&{*other._iter_channel_ids()}
        
        return CheckIsAnyChannel(*channel_ids)
    
    def _iter_channel_ids(self):
        """
        Iterates the channel id-s of the check.
        
        This method is a generator.
        
        Yields
        ------
        channel_id : ``int``
        """
        return
        yield


class CheckIsChannel(CheckIsChannelBase):
    """
    Checks whether the message was sent to the given channel.
    
    Attributes
    ----------
    channel_id : `int`
        The respective channel's id.
    """
    __slots__ = ('channel_id', )
    
    def __new__(cls, channel):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        channel : `str`, `int`, ``Guild``
            The guild where the message should be sent.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel``, `str`, `int`.
        ValueError
            If `channel` was given as `str`, `int`, but not as a valid snowflake.
        """
        channel_id = instance_or_id_to_snowflake(channel, Channel, 'channel')
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if (context.message.channel.id == self.channel_id):
            return True
        
        return False
    
    @copy_docs(CheckIsChannelBase._iter_channel_ids)
    def _iter_channel_ids(self):
        yield self.channel_id


class CheckIsAnyChannel(CheckIsChannelBase):
    """
    Checks whether the message was sent into any of the given channels.
    
    Attributes
    ----------
    channel_ids : `set` of `int`
        The respective channels' identifiers.
    """
    __slots__ = ('channel_ids', )
    
    def __new__(cls, *channels):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *channels : `str`, `int`, ``Channel``
            The channel where the message should be sent.
        
        Raises
        ------
        TypeError
            If a channel was not given neither as ``Channel``, `str`, `int`.
        ValueError
            If a channel was given as `str`, `int`, but not as a valid snowflake.
        """
        channel_ids_processed = set()
        
        for channel in channels:
            channel_id = instance_or_id_to_snowflake(channel, Channel, 'guild')
            channel_ids_processed.add(channel_id)
        
        channel_ids_processed_length = len(channel_ids_processed)
        if channel_ids_processed_length == 0:
            return CheckBase()
        
        if channel_ids_processed_length == 1:
            return CheckIsChannel(channel_ids_processed.pop())
        
        self = object.__new__(cls)
        self.channel_ids = channel_ids_processed
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if (context.message.channel.id in self.channel_ids):
            return True
        
        return False
    
    @copy_docs(CheckIsChannelBase._iter_channel_ids)
    def _iter_channel_ids(self):
        yield from self.channel_ids


class CheckIsNsfwChannel(CheckSingleBase):
    """
    Checks whether the message was sent to an nsfw channel.
    """
    __slots__ = ()

    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        return context.message.channel.nsfw


class CheckIsAnnouncementChannel(CheckSingleBase):
    """
    Checks whether the message was sent to an announcement channel.
    """
    __slots__ = ()

    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if context.message.channel.type == 5:
            return True
        
        return False


class CheckIsInVoice(CheckSingleBase):
    """
    Checks whether the message's author is in a voice channel in the respective guild.
    """
    __slots__ = ()

    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        guild = message.guild
        if guild is None:
            return False
        
        if message.author.id in guild.voice_states:
            return True
        
        return False


class CheckIsBooster(CheckSingleBase):
    """
    Checks whether the message's author boosts the respective guild.
    """
    __slots__ = ()

    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        guild = message.guild
        if guild is None:
            return
        
        try:
            profile = message.author.guild_profiles[guild.id]
        except KeyError:
            return False
        
        if profile.boosts_since is None:
            return False
        
        return True


class CheckIsClient(CheckSingleBase):
    """
    Check whether the message was sent by a client.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if isinstance(context.message.author, Client):
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if other_type is type(self):
            return self
        
        if other_type is CheckUserAccount:
            return CheckIsUserAccountOrIsClient()
        
        return CheckOrRelation(self, other)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if other_type is type(self):
            return self
        
        if (other_type is CheckIsUserAccountOrIsClient):
            return self
        
        return CheckAndRelation(self, other)


class CheckUserAccount(CheckSingleBase):
    """
    Checks whether the message was sent by an user account.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        if not context.message.author.bot:
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if other_type is type(self):
            return self
        
        if other_type is CheckIsClient:
            return CheckIsUserAccountOrIsClient()
        
        return CheckOrRelation(self, other)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if other_type is type(self):
            return self
        
        if (other_type is CheckIsUserAccountOrIsClient):
            return self
        
        return CheckAndRelation(self, other)


class CheckBotAccount(CheckSingleBase):
    """
    Checks whether the message was sent by a bot account.
    """
    __slots__ = ()

    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        user = context.message.author
        if user.bot and isinstance(user, ClientUserBase):
            return True
        
        return False


class CheckIsUserAccountOrIsClient(CheckIsClient, CheckUserAccount, CheckSingleBase):
    """
    Checks whether the message was sent by a user account or by a client.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        user = context.message.author
        if not user.bot:
            return True
        
        if isinstance(user, Client):
            return True
        
        return False
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if (other_type is type(self)) or (other_type is CheckIsClient) or (other_type is CheckUserAccount):
            return self
        
        return CheckOrRelation(self, other)

    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if other_type is type(self):
            return self
        
        if (other_type is CheckIsClient) or (other_type is CheckUserAccount):
            return other
        
        return CheckAndRelation(self, other)


class CheckIsCategoryBase(CheckBase):
    """
    Base class for category checks.
    """
    __slots__ = ()
    
    @copy_docs(CheckBase.__or__)
    def __or__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return self
        
        if not issubclass(other_type, CheckIsCategoryBase):
            return CheckOrRelation(self, other)
        
        category_ids = {*self._iter_category_ids(), *other._iter_category_ids()}
        
        return CheckIsAnyCategory(*category_ids)
    
    @copy_docs(CheckBase.__and__)
    def __and__(self, other):
        other_type = type(other)
        if not issubclass(other_type, CheckBase):
            return NotImplemented
        
        if other_type is CheckBase:
            return other
        
        if not issubclass(other_type, CheckIsCategoryBase):
            return CheckAndRelation(self, other)
        
        category_ids = {*self._iter_category_ids()}&{*other._iter_category_ids()}
        
        return CheckIsAnyCategory(*category_ids)
    
    def _iter_category_ids(self):
        """
        Iterates the category ids of the check.
        
        This method is a generator.
        
        Yields
        ------
        category_id : `int`
        """
        return
        yield


class CheckIsCategory(CheckIsCategoryBase):
    """
    Checks whether the message was sent into any channel of the given category.
    
    Attributes
    ----------
    category_id : `int`
        The respective category's id.
    """
    __slots__ = ('category_id', )
    
    def __new__(cls, category):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        category : `str`, `int`, ``Channel``, ``Guild``
            The category, within sent messages pass the check.
            
            If you want to check whether the channel is not in a category, pass the parameter as the respective guild
            instead.
        
        Raises
        ------
        TypeError
            If `category` was not given neither as ``Channel``, ``Guild``, `str`, `int`.
        ValueError
            If `category` was given as `str`, `int`, but not as a valid snowflake.
        """
        category_id = instance_or_id_to_snowflake(category, (Channel, Guild), 'category')
        
        self = object.__new__(cls)
        self.category_id = category_id
        return self
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        channel = context.message.channel
        
        parent = channel.parent
        if parent is None:
            guild = channel.guild
            if guild is None:
                return False
            
            parent_id = guild.id
        else:
            parent_id = parent.id
        
        if parent_id == self.category_id:
            return True
        
        return False
    
    @copy_docs(CheckIsCategoryBase._iter_category_ids)
    def _iter_category_ids(self):
        yield self.category_id


class CheckIsAnyCategory(CheckIsCategoryBase):
    """
    Checks whether the message was sent into any channel of the given categories.
    
    Attributes
    ----------
    category_ids : `set` of `int`
        The respective categories' id.
    """
    __slots__ = ('category_ids', )
    
    def __new__(cls, *categories):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        *categories : `str`, `int`, ``Channel``, ``Guild``
            The categories, within sent messages pass the check.
            
            If you want to check whether the channel is not in a category, pass the parameter as the respective guild
            instead.
        
        Raises
        ------
        TypeError
            If a category was not given neither as ``Channel``, ``Guild``, `str`, `int`.
        ValueError
            If a category was given as `str`, `int`, but not as a valid snowflake.
        """
        category_ids_processed = set()
        
        for category in categories:
            category_id = instance_or_id_to_snowflake(category, (Channel, Guild), 'category')
            category_ids_processed.add(category_id)
        
        category_ids_processed_length = len(category_ids_processed)
        if category_ids_processed_length == 0:
            return CheckBase()
        if category_ids_processed_length == 1:
            return CheckIsCategory(category_ids_processed.pop())
        
        self = object.__new__(cls)
        self.category_ids = category_ids_processed
        return self

    @copy_docs(CheckIsCategoryBase._iter_category_ids)
    def _iter_category_ids(self):
        yield from self.category_ids


class CheckReleaseAt(CheckBase):
    """
    Checks whether the command is already released.
    
    Attributes
    ----------
    release_at : `int`
        The time in snowflake, when the command will be released.
    pre_access_roles : `None`, `set` of ``Role``
        The roles, who are bypassed by the check.
    """
    def __new__(cls, release_at, *roles):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        release_at : `datetime`
            When the command is released.
        *roles : `str`, `int`, ``Role``
            Role from which the message's author should have at least one.
        
        Raises
        ------
        TypeError
            If an element of role was not given neither as ``Role``, `str`, `int`.
        ValueError
            If a role was given as `str`, `int`, but not as a valid snowflake, so a ``Role``
            cannot be precreated with it.
        """
        if not isinstance(release_at, datetime):
            raise TypeError(
                f'`release_at` can be `datetime`, got {release_at.__class__.__name__}; {release_at!r}.'
            )
        
        roles_processed = set()
        for role in roles:
            role = instance_or_id_to_instance(role, Role, 'role')
            roles_processed.add(role)
        
        release_at = datetime_to_id(release_at)
        
        self = object.__new__(cls)
        self.release_at = release_at
        self.pre_access_roles = roles_processed
        return self
    
    
    @copy_docs(CheckBase.__call__)
    async def __call__(self, context):
        message = context.message
        if message.id > self.release_at:
            return True
        
        user = message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        if context.client.is_owner(user):
            return True
        
        return False


has_role = partial_func(CommandCheckWrapper, CheckHasRole)
owner_or_has_role = partial_func(CommandCheckWrapper, CheckHasRoleOrIsOwner)
has_any_role = partial_func(CommandCheckWrapper, CheckHasAnyRole)
owner_or_has_any_role = partial_func(CommandCheckWrapper, HasAnyRoleCheckOrRelationIsOwner)
guild_only = partial_func(CommandCheckWrapper, CheckIsInGuild)
private_only = partial_func(CommandCheckWrapper, CheckIsInPrivate)
owner_only = partial_func(CommandCheckWrapper, CheckIsOwner)
guild_owner_only = partial_func(CommandCheckWrapper, CheckIsGuildOwner)
owner_or_guild_owner_only = partial_func(CommandCheckWrapper, CheckIsGuildOwnerOrIsOwner)
has_permissions = partial_func(CommandCheckWrapper, CheckHasPermission)
owner_or_has_permissions = partial_func(CommandCheckWrapper, CheckHasPermissionOrIsOwner)
has_guild_permissions = partial_func(CommandCheckWrapper, CheckHasGuildPermission)
owner_or_has_guild_permissions = partial_func(CommandCheckWrapper, CheckHasGuildPermissionOrIsOwner)
has_client_permissions = partial_func(CommandCheckWrapper, CheckHasClientPermission)
has_client_guild_permissions = partial_func(CommandCheckWrapper, CheckHasClientGuildPermission)
is_guild = partial_func(CommandCheckWrapper, CheckIsGuild)
is_any_guild = partial_func(CommandCheckWrapper, CheckIsAnyGuild)
custom = partial_func(CommandCheckWrapper, CheckCustom)
is_channel = partial_func(CommandCheckWrapper, CheckIsChannel)
is_any_channel = partial_func(CommandCheckWrapper, CheckIsAnyChannel)
nsfw_channel_only = partial_func(CommandCheckWrapper, CheckIsNsfwChannel)
announcement_channel_only = partial_func(CommandCheckWrapper, CheckIsAnnouncementChannel)
is_in_voice = partial_func(CommandCheckWrapper, CheckIsInVoice)
booster_only = partial_func(CommandCheckWrapper, CheckIsBooster)
client_only = partial_func(CommandCheckWrapper, CheckIsClient)
user_account_only = partial_func(CommandCheckWrapper, CheckUserAccount)
bot_account_only = partial_func(CommandCheckWrapper, CheckBotAccount)
user_account_or_client_only = partial_func(CommandCheckWrapper, CheckIsUserAccountOrIsClient)
is_category = partial_func(CommandCheckWrapper, CheckIsCategory)
is_any_category = partial_func(CommandCheckWrapper, CheckIsAnyCategory)
release_at = partial_func(CommandCheckWrapper, CheckReleaseAt)
