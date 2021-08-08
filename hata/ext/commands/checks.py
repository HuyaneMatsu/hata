# -*- coding: utf-8 -*-
"""
Checks can be added to commands or to categories to limit their usage to set users or places.

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
| client_has_guild_permissions   | permissions     | Whether the client has the given permissions at the guild.   |
|                                |                 | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| client_has_permissions         | permissions     | Whether the client has the given permissions at the channel. |
+--------------------------------+-----------------+--------------------------------------------------------------+
| client_only                    | N/A             | Whether the message was sent by a ``Client``.                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| custom                         | function        | Custom checks, to wrap a given `function`. (Can be async.)   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_only                     | N/A             | Whether the message was sent to a guild channel.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_owner                    | N/A             | Whether the message's author is the guild's owner.           |
|                                |                 | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_any_role                   | roles           | Whether the message's author has any of the given roles.     |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_guild_permissions          | permissions     | Whether the message's author has the given permissions at    |
|                                |                 | the guild. (Fails in private channels.)                      |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_permissions                | permissions     | Whether the message's author has the given permissions at    |
|                                |                 | the channel.                                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| has_role                       | role            | Whether the message's author has the given role.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_any_channel                 | channels        | Whether the message was sent to any of the given channels.   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_any_guild                   | guilds          | Whether the message was sent to any of the given guilds.     |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_channel                     | channel         | Whether the message's channel is the given one.              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_guild                       | guild           | Whether the message guild is the given one.                  |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_in_any_category             | categories      | Whether the message was sent into a channel, what's category |
|                                |                 | is any of the specified ones.                                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_in_category                 | category        | Whether the message was sent into a channel, what's category |
|                                |                 | is the specified one.                                        |
+--------------------------------+-----------------+--------------------------------------------------------------+
| is_in_voice                    | N/A             | Whether the user is in a voice channel in the respective     |
|                                |                 | guild.                                                       |
+--------------------------------+-----------------+--------------------------------------------------------------+
| nsfw_channel_only              | N/A             | Whether the message's channel is nsfw.                       |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_only                     | N/A             | Whether the message's author is an owner of the client.      |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_guild_owner           | N/A             | `owner_only` or `guild_owner` (Fails in private channels.)   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_any_role          | roles           | `owner_only` or `has_any_role`                               |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_guild_permissions | permissions     | `owner_only` or `has_guild_permissions`                      |
|                                |                 | (Fails in private channels.)                                 |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_permissions       | permissions     | `owner_only` or `has_permissions`                            |
+--------------------------------+-----------------+--------------------------------------------------------------+
| owner_or_has_role              | role            | `owner_only` or `has_any_role`                               |
+--------------------------------+-----------------+--------------------------------------------------------------+
| private_only                   | N/A             | Whether the message's channel is a private channel.          |
+--------------------------------+-----------------+--------------------------------------------------------------+
| user_account_only              | N/A             | Whether the message's author is a user account.              |
+--------------------------------+-----------------+--------------------------------------------------------------+
| user_account_or_client         | N/A             | Whether the message's author is a user account or a          |
|                                |                 | ``Client`` instance.                                         |
+--------------------------------+-----------------+--------------------------------------------------------------+

Every check also accepts an additional keyword parameter, called `handler`, what is called, when the respective
check fails (returns `False`).

To a check's handler the following parameters are passed:

+-------------------+---------------------------+
| Respective name   | Type                      |
+===================+===========================+
| client            | ``Client``                |
+-------------------+---------------------------+
| message           | ``Message``               |
+-------------------+---------------------------+
| command           | ``Command`` or `str`      |
+-------------------+---------------------------+
| check             | ``_check_base`` instance  |
+-------------------+---------------------------+

If a command's check fails, then `command` is given as `Command` instance, tho checks can be added not only to
commands and at those cases, `command` is given as `str`.
"""

from ...backend.utils import NEEDS_DUMMY_INIT
from ...backend.futures import Task
from ...backend.analyzer import CallableAnalyzer

from ...discord.core import KOKORO
from ...discord.bases import instance_or_id_to_instance, instance_or_id_to_snowflake
from ...discord.guild import Guild
from ...discord.permission import Permission
from ...discord.role import Role
from ...discord.channel import ChannelBase, ChannelText, ChannelCategory, ChannelGuildBase
from ...discord.events.handling_helpers import check_parameter_count_and_convert
from ...discord.client import Client

def validate_checks(checks_):
    """
    Validates the given checks.
    
    Parameters
    ----------
    checks_ : `None`, ``_check_base`` instance or `list` of ``_check_base`` instances
        Checks to define in which circumstances a command should be called.
        
    Returns
    -------
    checks_processed : `None` or `list` of ``_check_base``
        Will never return an empty list.
    
    Raises
    ------
    TypeError
        If `checks_` was not given as `None` or as `list` of ``_check_base`` instances.
    """
    if checks_ is None:
        checks_processed = None
    elif isinstance(checks_, _check_base):
        checks_processed = [checks_]
    elif isinstance(checks_, list):
        checks_processed = []
        
        for index, check in enumerate(checks_):
            check_type = check.__class__
            if issubclass(check_type, _check_base):
                checks_processed.append(check)
                continue
            
            raise TypeError(f'`checks` element {index} was not given as `{_check_base.__name__}`, got '
                f'`{check_type.__name__}`.')
        
        if not checks_processed:
            checks_processed = None
    else:
        raise TypeError(f'`checks_` should have been given as `None`, `{_check_base.__name__}` instance or as '
            f'`list` of `{_check_base.__name__}` instances, got: {checks_.__class__.__name__}; {checks_!r}.')
    
    # Unwrap `and` checks
    if (checks_processed is not None):
        index = 0
        limit = len(checks_processed)
        while True:
            check = checks_processed[index]
            if isinstance(check, _and_op_check):
                del checks_processed[index]
                for check in check.checks:
                    checks_processed.append(check)
                
                limit = len(checks_processed)
            else:
                index += 1
            
            if index >= limit:
                break
    
    return checks_processed


def _convert_handler(handler):
    """
    Validates the given handler.
    
    Parameters
    ----------
    handler : `None` or `async-callable` or instantiable to `async-callable`
        The handler to convert.
        
        If the handler is `async-callable` or if it would be instanced to it, then it should accept the following
        parameters:
        +-------------------+---------------------------+
        | Respective name   | Type                      |
        +===================+===========================+
        | client            | ``Client``                |
        +-------------------+---------------------------+
        | message           | ``Message``               |
        +-------------------+---------------------------+
        | command           | ``Command`` or `str`      |
        +-------------------+---------------------------+
        | check             | ``_check_base`` instance  |
        +-------------------+---------------------------+
    
    Returns
    -------
    handler : `None` or `async-callable`
    
    Raises
    ------
    TypeError
        If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
    """
    if (handler is not None):
        handler = check_parameter_count_and_convert(handler, 4, name='handler', error_message= \
            '`handler` expects to pass 4 parameters (client, message, command, check).')
    return handler

def _convert_permissions(permissions):
    """
    Validates the given `permissions`.
    
    Parameters
    ----------
    permissions : ``Permission`` or `int` instance
        Permission to validate.
    
    Returns
    -------
    permissions : ``Permission``
    
    Raises
    ------
    TypeError
        `permissions` was not given as `int` instance.
    """
    permission_type = permissions.__class__
    if permission_type is Permission:
        pass
    elif issubclass(permission_type, int):
        permissions = Permission(permissions)
    else:
        raise TypeError(f'`permissions` should have been passed as a `{Permission.__name__}` object or as an '
            f'`int` instance, got {permission_type.__name__}.')
    
    return permissions

class _check_meta(type):
    """
    Check metaclass for collecting their slots in a `SLOTS` class attribute.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type` instances
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``_check_meta`` instance
        """
        if class_parents:
            parent = class_parents[0]
            inherited_slots = getattr(parent, 'SLOTS', None)
        else:
            inherited_slots = None
        
        new_slots = class_attributes.get('__slots__', None)
        
        final_slots = []
        if (inherited_slots is not None):
            final_slots.extend(inherited_slots)
        
        if (new_slots is not None):
            final_slots.extend(new_slots)
        
        class_attributes['SLOTS'] = tuple(final_slots)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

class _check_base(metaclass=_check_meta):
    """
    Base class for checks.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ('handler',)
    
    def __new__(cls, handler=None):
        """
        Creates a check with the given parameters.
        
        Parameters
        ----------
        handler : `None` or `async-callable` or instantiable to `async-callable`
            Will be called when the check fails.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        """
        handler = _convert_handler(handler)
        self = object.__new__(cls)
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        Subclasses should overwrite this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        return False
    
    def __repr__(self):
        """Returns the check's representation."""
        result = [
            self.__class__.__name__,
            '(',
                ]
        
        slots = self.SLOTS
        limit = len(slots)
        if limit:
            index = 0
            while True:
                name = slots[index]
                index += 1
                if (name == 'handler') or name.startswith('_'):
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
                
                result.append(display_name)
                result.append('=')
                attr = getattr(self,name)
                result.append(repr(attr))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        handler = self.handler
        if (handler is not None):
            if limit:
                result.append(', ')
            result.append('handler=')
            result.append(repr(handler))
        
        result.append(')')
        
        return ''.join(result)
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    
    def __invert__(self):
        """Inverts the check's condition returning a new check."""
        return _invert_op_check(self)
    
    def __or__(self, other):
        """Connects the two check with `or` relation."""
        if not isinstance(other, _check_base):
            return NotImplemented
        
        return _or_op_check(self, other)

    def __and__(self, other):
        """Connects the two check with `and` relation."""
        if not isinstance(other, _check_base):
            return NotImplemented
        
        return _and_op_check(self, other)

class _invert_op_check(_check_base):
    """
    Inverts an internal check.
    
    Attributes
    ----------
    check : ``_check_base`` instance
        The inverted check.
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ('check',)
    
    def __new__(cls, check):
        """
        Creates a new reverted check.
        
        Parameters
        ----------
        check : ``_check_base`` instance
            The check to invert.
        
        Returns
        -------
        self : ``_check_base`` instance
            The reverted check.
            
            If the check is already inverted, reverts it and returns the original one.
            
            If the check has an inverted check pair, returns an instead of that instead.
        """
        if isinstance(check, cls):
            self = check.check
        else:
            target_type = CHECK_INVERT_TABLE.get(check.__class__, None)
            if target_type is None:
                self = object.__new__(cls)
                self.check = check
                self.handler = check.handler
            else:
                # None of these classes have other attributes yet, so we need just to assign their `.handler`.
                self = object.__new__(target_type)
                self.handler = check.handler
        
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        return not await self.check(client, message)


class _or_op_check(_check_base):
    """
    Creates an `or` relations between 2 checks.
    
    Attributes
    ----------
    checks : `tuple` or ``_check_base`` instances
        The or-ed checks.
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ('checks', )
    def __new__(cls, check_1, check_2):
        """
        Creates a new or-ed check.
        
        Parameters
        ----------
        check_1 : ``_check_base`` instance
            The first check to connect.
        check_2 : ``_check_base`` instance
            The second check to connect.
        
        Returns
        -------
        self : ``_check_base`` instance
            The or-ed check.
            
            If the check has natural or relation with an other check, will return that one instead.
        """
        check_1_handler = check_1.handler
        check_2_handler = check_2.handler
        if check_2_handler is None:
            handler = check_1_handler
        else:
            handler = check_2_handler
        
        check_1_type = check_1.__class__
        check_2_type = check_2.__class__
        
        
        if (check_1_type is _check_base) or (check_2_type is _check_base):
            if check_1_type is _check_base:
                if check_2_type is _check_base:
                    return _check_base(handler=handler)
                
                other_check = check_2
            
            else:
                other_check = check_1
            
            self = object.__new__(other_check.__class__)
            self.handler = handler
            
            for slot_name in other_check.SLOTS:
                if slot_name == 'handler':
                    continue
                
                slot_value = getattr(other_check, slot_name)
                setattr(self, slot_name, slot_value)
            
            return self
        
        # Permission case?
        if (check_1_type is check_2_type) and (check_1_type in CHECK_PERMISSION_TABLE):
            self = object.__new__(check_1_type)
            self.handler = handler
            self.permissions = check_1.permissions | check_2.permissions
            return self
        
        check_type = CHECK_OR_TABLE.get(frozenset((check_1_type, check_2_type)))
        if (check_type is not None):
            # Guild only cases? -> facepalm?
            if issubclass(check_1_type, guild_only) or issubclass(check_2_type, guild_only):
                self = object.__new__(check_type)
                self.handler = handler
                return self
            
            # Connectible cases?
            if issubclass(check_1_type, CHECKS_OR_ONLY_TYPES) or issubclass(check_2_type, CHECKS_OR_ONLY_TYPES):
                if issubclass(check_1_type, CHECKS_OR_ONLY_TYPES):
                    other_check = check_2
                else:
                    other_check = check_1
                
                self = object.__new__(check_type)
                self.handler = handler
                for slot_name in other_check.SLOTS:
                    if slot_name == 'handler':
                        continue
                    
                    slot_value = getattr(other_check, slot_name)
                    setattr(self, slot_name, slot_value)
                
                return self
            
            # Entity or?
            if issubclass(check_1_type, CHECKS_ENTITY_TYPES) and issubclass(check_2_type, CHECKS_ENTITY_TYPES):
                entities = []
                
                for check in (check_1, check_2):
                    slot_name = CHECKS_ENTITY_SLOTS[check.__class__]
                    slot_value = getattr(check, slot_name)
                    if isinstance(slot_value, set):
                        entities.extend(slot_value)
                    else:
                        entities.append(slot_value)
                
                self = check_type(entities, handler=handler)
                return self
            
            # Other case Should not happen
        
        checks_unwrapped = []
        if issubclass(check_1_type, cls):
            checks_unwrapped.extend(check_1.checks)
        else:
            checks_unwrapped.append(check_1)
        
        if issubclass(check_2_type, cls):
            checks_unwrapped.extend(check_2.checks)
        else:
            checks_unwrapped.append(check_2)
        
        checks = tuple(checks_unwrapped)
        
        self = object.__new__(cls)
        self.checks = checks
        self.handler = handler
        
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        for check in self.checks:
            if await check(client, message):
                return True
        
        return False

class _and_op_check(_check_base):
    """
    Creates an `or` relations between 2 checks.
    
    Attributes
    ----------
    checks : `tuple` or ``_check_base`` instances
        The or-ed checks.
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ('checks', )
    def __new__(cls, check_1, check_2):
        """
        Creates a new and-ed check.
        
        Parameters
        ----------
        check_1 : ``_check_base`` instance
            The first check to connect.
        check_2 : ``_check_base`` instance
            The second check to connect.
        
        Returns
        -------
        self : ``_check_base`` instance
            The and-ed check.
            
            If the check has natural and relation with an other check, will return that one instead.
        
        Raises
        ------
        ValueError
            The two check's have different `handler`.
        """
        check_1_handler = check_1.handler
        check_2_handler = check_2.handler
        if check_1_handler != check_2_handler:
            raise ValueError(f'The two checks have different handlers: check_1={check_1!r}, check_2={check_2!r}. '
                'Please make sure they have the same when creating `and` connection between them.')
        
        handler = check_1_handler
        
        check_1_type = check_1.__class__
        check_2_type = check_2.__class__
        
        # Empty check?
        if (check_1_type is _check_base) or (check_2_type is _check_base):
            return _check_base(handler=handler)
        
        # Permission case?
        if (check_1_type is check_2_type) and (check_1_type in CHECK_PERMISSION_TABLE):
            self = object.__new__(check_1_type)
            self.handler = handler
            self.permissions = check_1.permissions & check_2.permissions
            return self
        
        check_type = CHECK_AND_TABLE.get(frozenset((check_1_type, check_2_type)))
        if (check_type is not None):
            # Connectible cases?
            if issubclass(check_1_type, CHECKS_AND_ONLY_TYPES) or issubclass(check_2_type, CHECKS_AND_ONLY_TYPES):
                if issubclass(check_1_type, CHECKS_AND_ONLY_TYPES):
                    other_check = check_2
                else:
                    other_check = check_1
                
                self = object.__new__(check_type)
                self.handler = handler
                for slot_name in other_check.SLOTS:
                    if slot_name == 'handler':
                        continue
                    
                    slot_value = getattr(other_check, slot_name)
                    setattr(self, slot_name, slot_value)
                
                return self
            
            # Entity or?
            if issubclass(check_1_type, CHECKS_ENTITY_TYPES) and issubclass(check_2_type, CHECKS_ENTITY_TYPES):
                entities = []
                
                slot_name = CHECKS_ENTITY_SLOTS[check_1_type]
                slot_value = getattr(check_1, slot_name)
                
                if isinstance(slot_value, set):
                    entities.extend(slot_value)
                else:
                    entities.append(slot_value)
                
                slot_name = CHECKS_ENTITY_SLOTS[check_2_type]
                slot_value = getattr(check_2, slot_name)
                
                if isinstance(slot_value, set):
                    for entity in slot_value:
                        try:
                            entities.remove(entity)
                        except ValueError:
                            pass
                else:
                    try:
                        entities.remove(slot_value)
                    except ValueError:
                        pass
                
                self = check_type(entities, handler=handler)
                return self
            
            # Other case Should not happen
        
        checks_unwrapped = []
        if isinstance(check_1, cls):
            checks_unwrapped.extend(check_1.checks)
        else:
            checks_unwrapped.append(check_1)
        
        if isinstance(check_2, cls):
            checks_unwrapped.extend(check_2.checks)
        else:
            checks_unwrapped.append(check_2)
        
        checks = tuple(checks_unwrapped)
        
        self = object.__new__(cls)
        self.checks = checks
        self.handler = handler
        
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        for check in self.checks:
            if not await check(client, message):
                return False
        
        return True


class has_role(_check_base):
    """
    Checks whether a message's author has the given role.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    role : ``Role``
        The role, what the user should have.
    """
    __slots__ = ('role', )
    def __new__(cls, role, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        role : `str`, `int` or ``Role``
            The role what the message's author should have.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            Will be called when the check fails.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `role` was not given neither as ``Role``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If `role` was given as `str` or as `int` instance, but not as a valid snowflake, so ``Role``
                instance cannot be precreated with it.
        """
        role = instance_or_id_to_instance(role, Role, 'role')
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.role = role
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if message.author.has_role(self.role):
            return True
        
        return False


class owner_or_has_role(has_role):
    """
    Checks whether a message's author has the given role, or if it the client's owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    role : ``Role``
        The role, what the user should have.
    """
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        user = message.author
        if user.has_role(self.role):
            return True
        
        if client.is_owner(user):
            return True
        
        return False


class has_any_role(_check_base):
    """
    Checks whether a message's author has any of the given roles.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    roles : `set` of ``Role``
        The roles from what the user should have at least 1.
    """
    __slots__ = ('roles', )
    def __new__(cls, roles, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        roles : `iterable` of (`str`, `int` or ``Role``)
            Role from what the message's author should have at least 1.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `roles` was not given as an `iterable`.
            - If an element of `roles` was not given neither as ``Role``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If an element of `roles` was given as `str` or as `int` instance, but not as a valid snowflake, so
                ``Role`` instance cannot be precreated with it.
        """
        roles_type = roles.__class__
        if not hasattr(roles_type,'__iter__'):
            raise TypeError(f'`roles` can be given as `iterable` of (`str`, `int` or `{Role.__name__}`), got '
                f'{roles_type.__name__}.')
        
        roles_processed = set()
        for role in roles:
            role = instance_or_id_to_instance(role, Role, 'role')
            roles_processed.add(role)
        
        roles_processed_length = len(roles_processed)
        if roles_processed_length == 0:
            return _check_base(handler)
        elif roles_processed_length == 1:
            return has_role(roles_processed.pop(), handler)
        
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.roles = roles_processed
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        user = message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        return False


class owner_or_has_any_role(has_any_role):
    """
    Checks whether a message's author has any of the given roles or if it is the client's owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    roles : `set` of ``Role``
        The roles from what the user should have at least 1.
    """
    def __new__(cls, roles, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        roles : `iterable` of (`str`, `int` or ``Role``)
            Role from what the message's author should have at least 1.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `roles` was not given as an `iterable`.
            - If an element of `roles` was not given neither as ``Role``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If an element of `roles` was given as `str` or as `int` instance, but not as a valid snowflake, so
                ``Role`` instance cannot be precreated with it.
        """
        roles_type = roles.__class__
        if not hasattr(roles_type,'__iter__'):
            raise TypeError(f'`roles` can be given as `iterable` of (`str`, `int` or `{Role.__name__}`), got '
                f'{roles_type.__name__}.')
        
        roles_processed = set()
        for role in roles:
            role = instance_or_id_to_instance(role, Role, 'role')
            roles_processed.add(role)
        
        if len(roles_processed) == 1:
            return owner_or_has_role(roles_processed.pop(), handler)
        
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.roles = roles_processed
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        user = message.author
        for role in self.roles:
            if user.has_role(role):
                return True
        
        if client.is_owner(user):
            return True
        
        return False


class guild_only(_check_base):
    """
    Checks whether a message was sent to a guild channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if (message.guild is not None):
            return True
        
        return False


class private_only(_check_base):
    """
    Checks whether a message was sent to a private channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if (message.guild is None):
            return True
        
        return False

class owner_only(_check_base):
    """
    Checks whether a message was sent by the client's owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if client.is_owner(message.author):
            return True
        
        return False


class guild_owner(_check_base):
    """
    Checks whether a message was sent by the message's guild's owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if guild.owner_id == message.author.id:
            return True
        
        return False


class owner_or_guild_owner(guild_owner):
    """
    Checks whether a message was sent by the message's guild's owner or by the client's owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        user = message.author
        if guild.owner_id == user.id:
            return True
        
        if client.is_owner(user):
            return True
        
        return False


class has_permissions(_check_base):
    """
    Checks whether a message's author has the given permissions at the message's channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the message's author should have at message's channel.
    """
    __slots__ = ('permissions', )
    def __new__(cls, permissions, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        permissions : ``Permission`` or `int` instance
            The permission, what the message's author should have at the message's channel.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - `permissions` was not given as `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        """
        permissions = _convert_permissions(permissions)
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if message.channel.permissions_for(message.author) >= self.permissions:
            return True
        
        return False


class owner_or_has_permissions(has_permissions):
    """
    Checks whether a message's author has the given permissions at the message's channel, or if it is the client's
    owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the message's author should have at message's channel.
    """
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        user = message.author
        if message.channel.permissions_for(user) >= self.permissions:
            return True
        
        if client.is_owner(user):
            return True
        
        return False


class has_guild_permissions(_check_base):
    """
    Checks whether a message's author has the given permissions at the message's guild.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the message's author should have at message's guild.
    """
    __slots__ = ('permissions', )
    def __new__(cls, permissions, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        permissions : ``Permission`` or `int` instance
            The permission, what the message's author should have at the message's guild.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - `permissions` was not given as `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        """
        permissions = _convert_permissions(permissions)
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if guild.permissions_for(message.author) >= self.permissions:
            return True
        
        return False


class owner_or_has_guild_permissions(has_permissions):
    """
    Checks whether a message's author has the given permissions at the message's guild, or if it is the client's
    owner.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the message's author should have at message's guild.
    """
    __slots__ = ('permissions', )
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        user = message.author
        
        if guild.permissions_for(user) >= self.permissions:
            return True
        
        if client.is_owner(user):
            return True
        
        return False


class client_has_permissions(_check_base):
    """
    Checks whether a client has the given permissions at the message's channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the client should have at message's channel.
    """
    __slots__ = ('permissions', )
    def __new__(cls, permissions, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        permissions : ``Permission`` or `int` instance
            The permission, what the client should have at the message's channel.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - `permissions` was not given as `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        """
        permissions = _convert_permissions(permissions)
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if message.channel.cached_permissions_for(client) >= self.permissions:
            return True
        
        return False


class client_has_guild_permissions(_check_base):
    """
    Checks whether a client has the given permissions at the message's guild.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    permissions : ``Permission``
        The permission what the client should have at message's guild.
    """
    __slots__ = ('permissions', )
    def __new__(cls, permissions, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        permissions : ``Permission`` or `int` instance
            The permission, what the client should have at the message's guild.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - `permissions` was not given as `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        """
        permissions = _convert_permissions(permissions)
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if guild.cached_permissions_for(client) >= self.permissions:
            return True
        
        return False


class is_guild(_check_base):
    """
    Checks whether the message was sent to the given guild.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    guild_id : `int`
        The respective guild's id.
    """
    __slots__ = ('guild_id', )
    def __new__(cls, guild, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        guild : `str`, `int` or ``Guild``
            The guild where the message should be sent.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If `guild` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        guild_id = instance_or_id_to_snowflake(guild, Guild, 'guild')
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if (guild.id == self.guild_id):
            return True
        
        return False


class is_any_guild(_check_base):
    """
    Checks whether the message was sent to any of the given guilds.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    guild_ids : `set of `int`
        The respective guilds' ids.
    """
    __slots__ = ('guild_ids', )
    def __new__(cls, guilds, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        guilds : `iterable` of (`str`, `int` or ``Guild``)
            Guilds to where the message should be sent.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `guilds` was not given as an `iterable`.
            - If an element of `guilds` was not given neither as ``Guild``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If an element of `guilds` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        guild_type = guilds.__class__
        if not hasattr(guild_type, '__iter__'):
            raise TypeError(f'`guilds` can be given as `iterable` of (`str`, `int` or `{Guild.__name__}`), got '
                f'{guild_type.__name__}.')
        
        guild_ids_processed = set()
        for guild in guilds:
            guild_id = instance_or_id_to_snowflake(guild, Guild, 'guild')
            guild_ids_processed.add(guild_id)
        
        guild_ids_processed_length = len(guild_ids_processed)
        if guild_ids_processed_length == 0:
            return _check_base(handler)
        elif guild_ids_processed_length == 1:
            return is_guild(guild_ids_processed.pop(), handler)
        
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.guild_ids = guild_ids_processed
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if (guild.id in self.guild_ids):
            return True
        
        return False


class custom(_check_base):
    """
    Checks whether the message and client passes the given custom condition.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    _is_async : `bool`
        Whether ``.function`` is async.
    function : `callable`
        The custom check's function.
    """
    __slots__ = ('_is_async', 'function')
    def __new__(cls, function, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        function : `callable`
            The custom check what should pass. Can be async.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `function` was not given as an `callable`.
            - `function` accepts more or less non reserved positional non default parameters.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        
        Notes
        -----
        Only `int` instances are evaluated to boolean.
        """
        analyzer = CallableAnalyzer(function)
        non_reserved_positional_parameter_count = analyzer.get_non_reserved_positional_parameter_count()
        if  non_reserved_positional_parameter_count != 2:
            raise TypeError(f'The passed function: {function!r} should have accept `2` non reserved, positional, '
                f'non default parameters, meanwhile it accepts `{non_reserved_positional_parameter_count}`.')
        
        is_async = analyzer.is_async()
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.function = function
        self._is_async = is_async
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        try:
            result = self.function(client, message)
            if self._is_async:
                result = await result
        except BaseException as err:
            Task(client.events.error(client, repr(self), err), KOKORO)
            return False
        
        if result is None:
            return False
        
        if isinstance(result, int) and result:
            return True
        
        return False


class is_channel(_check_base):
    """
    Checks whether the message was sent to the given channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    channel_id : `int`
        The respective channel's id.
    """
    __slots__ = ('channel_id', )
    def __new__(cls, channel, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        channel : `str`, `int` or ``ChannelBase``
            The channel where the message should be sent.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelBase``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If `channel` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        channel_id = instance_or_id_to_snowflake(channel, ChannelBase, 'channel')
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if (message.channel.id == self.channel_id):
            return True
        
        return False


class is_any_channel(_check_base):
    """
    Checks whether the message was sent to any of the given channels.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    channel_ids : `set` of `int`
        The respective channels' ids.
    """
    __slots__ = ('channel_ids', )
    def __new__(cls, channels, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        channels : `iterable` of (`str`, `int` or ``ChannelBase``)
            Channels to where the message should be sent.
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `channels` was not given as an `iterable`.
            - If an element of `channels` was not given neither as ``ChannelBase``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If an element of `channels` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        channels_type = channels.__class__
        if not hasattr(channels_type, '__iter__'):
            raise TypeError(f'`channels` can be given as `iterable` of (`str`, `int` or `{ChannelBase.__name__}`), '
                f'got {channels_type.__name__}.')
        
        channel_ids_processed = set()
        for channel in channels:
            channel_id = instance_or_id_to_snowflake(channel, ChannelBase, 'channel')
            channel_ids_processed.add(channel_id)
        
        channel_ids_processed_length = len(channel_ids_processed)
        if channel_ids_processed_length == 0:
            return _check_base(handler)
        elif channel_ids_processed_length == 1:
            return is_channel(channel_ids_processed.pop(), handler)
        
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.channel_ids = channel_ids_processed
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if (message.channel.id in self.channel_ids):
            return True
        
        return False


class nsfw_channel_only(_check_base):
    """
    Checks whether the message was sent to an nsfw channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        channel = message.channel
        if (isinstance(channel, ChannelText) and channel.nsfw):
            return True
        
        return False

class announcement_channel_only(_check_base):
    """
    Checks whether the message was sent to an announcement channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        channel = message.channel
        if channel.type == 5:
            return True
        
        return False


class is_in_voice(_check_base):
    """
    Checks whether the message was sent by a user who is in any of the respective guild's voice channel.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        guild = message.guild
        if guild is None:
            return False
        
        if message.author.id in guild.voice_states:
            return True
        
        return False


class booster_only(_check_base):
    """
    Checks whether the message was sent by a user who boosts the respective server.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
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


class client_only(_check_base):
    """
    Checks whether the message was sent by a client.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if isinstance(message.author, Client):
            return True
        
        return False


class user_account_only(_check_base):
    """
    Checks whether the message was sent by a user account.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if message.author.is_bot:
            return False
        
        return True


class bot_account_only(_check_base):
    """
    Checks whether the message was sent by a bot account.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        if message.author.is_bot:
            return True
        
        return False


class user_account_or_client(_check_base):
    """
    Checks whether the message was sent by a user account or by a ``Client`` instance.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    """
    __slots__ = ()
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        user = message.author
        if not user.is_bot:
            return True
        
        if isinstance(user, Client):
            return True
        
        return False


class is_in_category(_check_base):
    """
    Checks whether the message was sent to a channel within the given category.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    category_id : `int`
        The respective category's id.
    """
    __slots__ = ('category_id', )
    def __new__(cls, category, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        category : `str`, `int`, ``ChannelCategory`` or ``Guild``
            The category, within sent messages pass the check.
            
            If you want to check those channels, which are not in any category, pass the respective ``Guild`` instead.
        
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `category` was not given neither as ``ChannelCategory``, ``Guild``, `str` or `int` instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If `category` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        category_id = instance_or_id_to_snowflake(category, (ChannelCategory, Guild), 'category')
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.category_id = category_id
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        channel = message.channel
        if not isinstance(channel, ChannelGuildBase):
            return False
        
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


class is_in_any_category(_check_base):
    """
    Checks whether the message was sent to a channel within any of the given category.
    
    Attributes
    ----------
    handler : `None` or `async-callable`
        An async callable what will be called when the check fails.
    category_ids : `set` of `int`
        The respective category's id.
    """
    __slots__ = ('category_ids', )
    def __new__(cls, categories, handler=None):
        """
        Creates a check, what will validate whether the a received message of a client passes the given condition.
        
        Parameters
        ----------
        categories : `iterable` of (`str`, `int`, ``ChannelCategory`` or ``Guild``)
            The categories, within sent messages pass the check.
            
            If you want to check those channels, which are not in any category, pass the respective ``Guild`` instead.
        
        handler : `None` or `async-callable` or instantiable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following parameters:
            +-------------------+---------------------------+
            | Respective name   | Type                      |
            +===================+===========================+
            | client            | ``Client``                |
            +-------------------+---------------------------+
            | message           | ``Message``               |
            +-------------------+---------------------------+
            | command           | ``Command`` or `str`      |
            +-------------------+---------------------------+
            | check             | ``_check_base`` instance  |
            +-------------------+---------------------------+
        
        Raises
        ------
        TypeError
            - If `categories` was not given as an `iterable`.
            - If an element of `categories` was not given neither as ``ChannelCategory``, ``Guild``, `str` or `int`
                instance.
            - If `handler` was given as an invalid type, or it accepts a bad amount of parameters.
        ValueError
            If an element of `categories` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        categories_type = categories.__class__
        if not hasattr(categories_type, '__iter__'):
            raise TypeError(f'`categories` can be given as `iterable` of (`str`, `int`, `{ChannelCategory.__name__}`, '
                f'or `{Guild.__name__}`), got {categories_type.__name__}.')
        
        category_ids_processed = set()
        for category in categories:
            category_id = instance_or_id_to_snowflake(category, (ChannelCategory, Guild), 'category')
            category_ids_processed.add(category_id)
        
        category_ids_processed_length = len(category_ids_processed)
        if category_ids_processed_length == 0:
            return _check_base(handler)
        elif category_ids_processed_length == 1:
            return is_in_category(category_ids_processed.pop(), handler)
        
        handler = _convert_handler(handler)
        
        self = object.__new__(cls)
        self.category_ids = category_ids_processed
        self.handler = handler
        return self
    
    async def __call__(self, client, message):
        """
        Calls the check to validate whether it passes with the given conditions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who's received the message.
        message : ``Message``
            The received message.
        
        Returns
        -------
        passed : `bool`
            Whether the check passed.
        """
        channel = message.channel
        if not isinstance(channel, ChannelGuildBase):
            return False
        
        parent = channel.parent
        if parent is None:
            guild = channel.guild
            if guild is None:
                return False
            
            parent_id = guild.id
        else:
            parent_id = parent.id
        
        if parent_id in self.category_ids:
            return True
        
        return False


CHECK_INVERT_TABLE = {
    bot_account_only: user_account_only,
    guild_only: private_only,
    private_only: guild_only,
    user_account_only: bot_account_only,
}

CHECKS_ENTITY_SLOTS = {
    is_channel: 'channel_id',
    is_guild: 'guild_id',
    is_in_category: 'category_id',
    has_role: 'role',
    owner_or_has_role: 'role',
    is_any_channel: 'channel_ids',
    is_any_guild: 'guild_ids',
    is_in_any_category: 'category_ids',
    has_any_role: 'roles',
    owner_or_has_any_role: 'roles',
}

CHECKS_ENTITY_TYPES = (
    is_channel,
    is_guild,
    is_in_category,
    has_role,
    owner_or_has_role,
    is_any_channel,
    is_any_guild,
    is_in_any_category,
    has_any_role,
    owner_or_has_any_role,
)

CHECKS_OR_ONLY_TYPES = (
    owner_only,
    client_only,
)

CHECK_OR_TABLE = {
    frozenset((guild_only, client_has_guild_permissions)): guild_only,
    frozenset((guild_only, booster_only)): guild_only,
    frozenset((guild_only, has_guild_permissions)): guild_only,
    frozenset((guild_only, guild_only)): guild_only,
    frozenset((guild_only, guild_owner)): guild_only,
    frozenset((guild_only, has_guild_permissions)): guild_only,
    frozenset((guild_only, is_guild)): guild_only,
    frozenset((guild_only, is_any_guild)): guild_only,
    frozenset((guild_only, is_in_category)): guild_only,
    frozenset((guild_only, is_in_any_category)): guild_only,
    frozenset((guild_only, owner_or_guild_owner)): guild_only,
    frozenset((guild_only, owner_or_has_guild_permissions)): guild_only,
    
#   Note, that `guild_owner` and `has_guild_permissions` require to be inside of a `guild`, so we cannot take them.
#   frozenset((owner_only, guild_owner)): owner_or_guild_owner,
#   frozenset((owner_only, has_guild_permissions)): owner_or_has_guild_permissions,
    
    frozenset((owner_only, has_any_role)): owner_or_has_any_role,
    frozenset((owner_only, has_permissions)): owner_or_has_permissions,
    frozenset((owner_only, has_role)): owner_or_has_role,
    
    frozenset((client_only, user_account_only)): user_account_or_client,
    
    frozenset((is_channel, is_channel)): is_any_channel,
    frozenset((is_channel, is_any_channel)): is_any_channel,
    frozenset((is_any_channel, is_any_channel)): is_any_channel,
    frozenset((is_guild, is_guild)): is_any_guild,
    frozenset((is_guild, is_any_guild)): is_any_guild,
    frozenset((is_any_guild, is_any_guild)): is_any_guild,
    frozenset((is_in_category, is_in_any_category)): is_in_any_category,
    frozenset((is_in_category, is_in_any_category)): is_in_any_category,
    frozenset((is_in_any_category, is_in_any_category)): is_in_any_category,
    frozenset((has_role, has_role)): has_any_role,
    frozenset((has_role, has_any_role)): has_any_role,
    frozenset((has_any_role, has_any_role)): has_any_role,
    frozenset((owner_or_has_role, owner_or_has_role)): owner_or_has_any_role,
    frozenset((owner_or_has_role, owner_or_has_any_role)): owner_or_has_any_role,
    frozenset((owner_or_has_any_role, owner_or_has_any_role)): owner_or_has_any_role,
}


CHECK_PERMISSION_TABLE = {
    client_has_guild_permissions,
    client_has_permissions,
    has_guild_permissions,
    has_permissions,
    owner_or_has_guild_permissions,
    owner_or_has_permissions,
}

CHECKS_AND_ONLY_TYPES = (
    guild_only,
)

CHECK_AND_TABLE = {
    frozenset((guild_only, client_has_guild_permissions)): client_has_guild_permissions,
    frozenset((guild_only, booster_only)): booster_only,
    frozenset((guild_only, has_guild_permissions)): has_guild_permissions,
    frozenset((guild_only, guild_only)): guild_only,
    frozenset((guild_only, guild_owner)): guild_owner,
    frozenset((guild_only, has_guild_permissions)): has_guild_permissions,
    frozenset((guild_only, is_guild)): is_guild,
    frozenset((guild_only, is_any_guild)): is_any_guild,
    frozenset((guild_only, is_in_category)): is_in_category,
    frozenset((guild_only, is_in_any_category)): is_in_any_category,
    frozenset((guild_only, owner_or_guild_owner)): owner_or_guild_owner,
    frozenset((guild_only, owner_or_has_guild_permissions)): owner_or_has_guild_permissions,
    
    frozenset((is_channel, is_channel)): is_any_channel,
    frozenset((is_channel, is_any_channel)): is_any_channel,
    frozenset((is_any_channel, is_any_channel)): is_any_channel,
    frozenset((is_guild, is_guild)): is_any_guild,
    frozenset((is_guild, is_any_guild)): is_any_guild,
    frozenset((is_any_guild, is_any_guild)): is_any_guild,
    frozenset((is_in_category, is_in_any_category)): is_in_any_category,
    frozenset((is_in_category, is_in_any_category)): is_in_any_category,
    frozenset((is_in_any_category, is_in_any_category)): is_in_any_category,
    frozenset((has_role, has_role)): has_any_role,
    frozenset((has_role, has_any_role)): has_any_role,
    frozenset((has_any_role, has_any_role)): has_any_role,
    frozenset((owner_or_has_role, owner_or_has_role)): owner_or_has_any_role,
    frozenset((owner_or_has_role, owner_or_has_any_role)): owner_or_has_any_role,
    frozenset((owner_or_has_any_role, owner_or_has_any_role)): owner_or_has_any_role,
}
