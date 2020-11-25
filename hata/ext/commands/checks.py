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
| client_has_permissions         | permissions     | Wehther the client has the given permissions at the channel. |
+--------------------------------+-----------------+--------------------------------------------------------------+
| client_only                    | N/A             | Whether the message was sent by a ``Client``.                |
+--------------------------------+-----------------+--------------------------------------------------------------+
| custom                         | function        | Custom checks, to wrap a given `function`. (Can be async.)   |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_only                     | N/A             | Whether the message was sent to a guild channel.             |
+--------------------------------+-----------------+--------------------------------------------------------------+
| guild_owner                    | N/A             | Wehther the message's author is the guild's owner.           |
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
| is_any_guild                   | guils           | Whether the message was sent to any of the given guilds.     |
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

from ...discord.client_core import KOKORO
from ...discord.bases import instance_or_id_to_instance, instance_or_id_to_snowflake
from ...discord.guild import Guild
from ...discord.permission import Permission
from ...discord.role import Role
from ...discord.channel import ChannelBase, ChannelText, ChannelCategory, ChannelGuildBase
from ...discord.parsers import check_argcount_and_convert
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
    
    return checks_processed

def _convert_handler(handler):
    """
    Validates the given handler.
    
    Parameters
    ----------
    handler : `None` or `async-callable` or instanceable to `async-callable`
        The handler to convert.
        
        If the handler is `async-callable` or if it would be instanced to it, then it should accept the following
        arguments:
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
        If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
    """
    if (handler is not None):
        handler = check_argcount_and_convert(handler, 4, name='handler', error_message= \
            '`handler` expects to pass 4 arguments (client, message, command, check).')
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


class _check_base(object):
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
        
        Paramaters
        ----------
        handler : `None` or `async-callable` or instanceable to `async-callable`
            Will be called when the check fails.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        return True
    
    def __repr__(self):
        """Returns the check's representation."""
        result = [
            self.__class__.__name__,
            '(',
                ]
        
        slots = self.__slots__
        limit = len(slots)
        if limit:
            index = 0
            while True:
                name = slots[index]
                index +=1
                # case of `_is_async`
                if name.startswith('_'):
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            Will be called when the check fails.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        
        self = object.__new__(cls)
        self.roles = roles_processed
        self.handler = _convert_handler(handler)
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
        guild = message.channel.guild
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
        guild = message.channel.guild
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
        permissions : ``Permission`` or `in` instance
            The permisison, what the message's author should have at the message's channel.
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        permissions : ``Permission`` or `in` instance
            The permisison, what the message's author should have at the message's guild.
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        guild = message.channel.guild
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
        guild = message.channel.guild
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
        permissions : ``Permission`` or `in` instance
            The permisison, what the client should have at the message's channel.
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        permissions : ``Permission`` or `in` instance
            The permisison, what the client should have at the message's guild.
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        guild = message.channel.guild
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        guild = message.channel.guild
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
        ValueError
            If an element of `guilds` was given as `str` or as `int` instance, but not as a valid snowflake.
        """
        guild_type = guilds.__class__
        if not hasattr(guild_type,'__iter__'):
            raise TypeError(f'`guilds` can be given as `iterable` of (`str`, `int` or `{Guild.__name__}`), got '
                f'{guild_type.__name__}.')
        
        guild_ids_processed = set()
        for guild in guilds:
            guild_id = instance_or_id_to_snowflake(guild, Guild, 'guild')
            guild_ids_processed.add(guild_id)
        
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
        guild = message.channel.guild
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - `function` accepts more or less non reserved positional non default arguments.
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
        
        Notes
        -----
        Only `int` instances are evaluated to boolean.
        """
        analyzer = CallableAnalyzer(function)
        non_reserved_positional_argument_count = analyzer.get_non_reserved_positional_argument_count()
        if  non_reserved_positional_argument_count != 2:
            raise TypeError(f'The passed function: {function!r} should have accept `2` non reserved, positional, '
                f'non default arguments, meanwhile it accepts `{non_reserved_positional_argument_count}`.')
        
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        guild = message.channel.guild
        if guild is None:
            return
        
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
        guild = message.channel.guild
        if guild is None:
            return
        
        try:
            profile = message.author.guild_profiles[guild]
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
            The category, whitin sent messages pass the check.
            
            If you want to check those channels, which are not in any category, pass the respective ``Guild`` instead.
        
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        
        category = channel.category
        if category is None:
            return False
        
        if category.id == self.category_id:
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
            The categories, whitin sent messages pass the check.
            
            If you want to check those channels, which are not in any category, pass the respective ``Guild`` instead.
        
        handler : `None` or `async-callable` or instanceable to `async-callable`
            The handler to convert.
            
            If the handler is `async-callable` or if it would be instanced to it, then it should accept the
            following arguments:
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
            - If `handler` was given as an invalid type, or it accepts a bad amount of arguments.
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
        
        category = channel.category
        if category is None:
            return False
        
        if category.id in self.category_ids:
            return True
        
        return False


del NEEDS_DUMMY_INIT
