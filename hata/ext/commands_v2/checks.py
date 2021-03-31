# -*- coding: utf-8 -*-
__all__ = ()

from ...backend.futures import Task
from ...backend.analyzer import CallableAnalyzer

from ...discord.client_core import KOKORO
from ...discord.bases import instance_or_id_to_instance, instance_or_id_to_snowflake
from ...discord.guild import Guild
from ...discord.permission import Permission
from ...discord.role import Role
from ...discord.channel import ChannelBase, ChannelText, ChannelCategory, ChannelGuildBase, ChannelPrivate, \
    ChannelGroup
from ...discord.parsers import check_argcount_and_convert
from ...discord.client import Client

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
        class_parents : `tuple` of `type` instances
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``CheckMeta`` instance
        """
        if class_parents:
            parent = class_parents[0]
            inherited_slots = getattr(parent, '__all_slot__', None)
        else:
            inherited_slots = None
        
        new_slots = class_attributes.get('__slots__')
        
        final_slots = []
        if (inherited_slots is not None):
            final_slots.extend(inherited_slots)
        
        if (new_slots is not None):
            final_slots.extend(new_slots)
        
        class_attributes['__all_slot__'] = tuple(final_slots)
        
        return type.__new__(cls, class_name, class_parents, class_attributes)

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
        result = [
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
                
                result.append(display_name)
                result.append('=')
                attr = getattr(self,name)
                result.append(repr(attr))
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(')')
        
        return ''.join(result)


class CheckHasRole(CheckBase):
    """
    Checks whether a message's author has the given role.
    
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
        role : `str`, `int` or ``Role``
            The role what the message's author should have.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role``, `str` or `int` instance.
        ValueError
            If `role` was given as `str` or as `int` instance, but not as a valid snowflake, so ``Role``
                instance cannot be precreated with it.
        """
        role = instance_or_id_to_instance(role, Role, 'role')
        
        self = object.__new__(cls)
        self.role = role
        return self
    
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        if context.message.author.has_role(self.role):
            return True
        
        return False


class CheckIsOwnerOrHasRole(CheckHasRole):
    """
    Checks whether a message's author has the given role, or if it the client's owner.
    
    Attributes
    ----------
    role : ``Role``
        The legend itself.
    """
    __slots__ = ()
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        user = context.message.author
        if user.has_role(self.role):
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckHasAnyRole(CheckBase):
    """
    Checks whether a message's author has any of the given roles.
    
    Attributes
    ----------
    roles : `set` of ``Role``
        The legends themselves.
    """
    __slots__ = ('roles', )
    def __new__(cls, roles):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        roles : `iterable` of (`str`, `int` or ``Role``)
            Role from what the message's author should have at least 1.
        
        Raises
        ------
        TypeError
            - If `roles` was not given as an `iterable`.
            - If an element of `roles` was not given neither as ``Role``, `str` or `int` instance.
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
            return CheckBase()
        
        if roles_processed_length == 1:
            return CheckHasRole(roles_processed.pop())
        
        self = object.__new__(cls)
        self.roles = roles_processed
        return self
    
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        user = context.message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        return False
    

class CheckIsOwnerOrHasAnyRole(CheckHasAnyRole):
    """
    Checks whether a message's author has any of the given roles, or whether is it the client's owner.
    
    Attributes
    ----------
    roles : `set` of ``Role``
        The roles from what the user should have at least 1.
    """
    __slots__ = ()
    def __new__(cls, roles, handler=None):
        """
        Checks whether a respective condition passes.
        
        Parameters
        ----------
        roles : `iterable` of (`str`, `int` or ``Role``)
            Role from what the message's author should have at least 1.
        
        Raises
        ------
        TypeError
            - If `roles` was not given as an `iterable`.
            - If an element of `roles` was not given neither as ``Role``, `str` or `int` instance.
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
            return CheckIsOwner()
        
        if roles_processed_length == 1:
            return CheckIsOwnerOrHasRole(roles_processed.pop())
        
        self = object.__new__(cls)
        self.roles = roles_processed
        return self

    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        user = context.message.author
        for role in self.roles:
            if  user.has_role(role):
                return True
        
        if context.client.is_owner(user):
            return True
        
        return False


class CheckGuildOnly(CheckHasAnyRole):
    """
    Checks whether the command was called from a guild.
    """
    __slots__ = ()
    
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        if isinstance(context.message.channel, ChannelGuildBase):
            return True
        
        return False


class CheckPrivateOnly(CheckHasAnyRole):
    """
    Checks whether the command was used inside of a private channel.
    """
    __slots__ = ()
    
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        if isinstance(context.message.channel, (ChannelPrivate, ChannelGroup)):
            return True
        
        return False


class CheckIsOwner(CheckBase):
    """
    Checks whether the command was called by the client's owner.
    """
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        if context.client.is_owner(context.message.author):
            return True
        
        return False


class CheckIsGuildOwner(CheckBase):
    """
    Checks whether the command was called by the local guild's owner.
    """
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        message = context.context
        guild = message.channel.guild
        if guild is None:
            return False
        
        if guild.owner_id == message.author.id:
            return True
        
        return False


class CheckIsOwnerOrIsGuildOwner(CheckBase):
    """
    Checks whether a message was sent by the message's guild's owner or by the client's owner.
    
    Guild check is always applied.
    """
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        message = context.context
        guild = message.channel.guild
        if guild is None:
            return False
        
        user = message.author
        if guild.owner_id == user.id:
            return True
        
        if context.client.is_owner(user):
            return True
        
        return False

class CheckIsOwnerOrIsGuildOwner(CheckBase):
    """
    Checks whether a message was sent by the message's guild's owner or by the client's owner.
    
    Guild check is always applied.
    
    Attributes
    ----------
    permissions : ``Permission``
    """
    __slots__ = ('permissions', )
    async def __call__(self, context):
        """
        Returns whether the check's condition passes.
        
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
        message = context.message
        if message.channel.permissions_for(message.author) >= self.permissions:
            return True
        
        return False













