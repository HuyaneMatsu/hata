# -*- coding: utf-8 -*-
__all__ = ('SlashCommandPermissionOverwriteWrapper', 'SlashCommandWrapper', 'wait_for_component_interaction')

from functools import partial as partial_func

from ...backend.futures import Future, future_or_timeout
from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake
from ...discord.interaction import ApplicationCommandPermissionOverwrite
from ...discord.client_core import APPLICATION_ID_TO_CLIENT, KOKORO
from ...discord.message import Message
from ...discord.parsers import InteractionEvent

UNLOADING_BEHAVIOUR_DELETE = 0
UNLOADING_BEHAVIOUR_KEEP = 1
UNLOADING_BEHAVIOUR_INHERIT = 2


SYNC_ID_GLOBAL = 0
SYNC_ID_MAIN = 1
SYNC_ID_NON_GLOBAL = 2


def raw_name_to_display(raw_name):
    """
    Converts the given raw application command name to it's display name.
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return '-'.join([w for w in raw_name.strip('_ ').lower().replace(' ', '-').replace('_', '-').split('-') if w])


class SlashCommandWrapper:
    """
    Wraps a slash command enabling the wrapper to postprocess the created slash command.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    """
    __slots__ = ('_wrapped',)
    def __new__(cls):
        """
        Creates a partial function to wrap a slash command.
        
        Subclasses should overwrite this method.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlashCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        return partial_func(cls._decorate, cls)
    
    def _decorate(cls, wrapped):
        """
        Wraps the given command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlashCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._wrapped = wrapped
        return self
    
    def apply(self, slash_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
        """
        pass
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}>'
    
    def fetch_function_and_wrappers_back(self):
        """
        Fetches back the source function and all the wrappers, the returns them.
        
        Returns
        -------
        function : `Any`
            The wrapped function.
        wrappers : `list` of ``SlashCommandWrapper`` instances
            The fetched back wrappers.
        """
        wrappers = [self]
        maybe_wrapper = self._wrapped
        while True:
            if isinstance(maybe_wrapper, SlashCommandWrapper):
                wrappers.append(maybe_wrapper)
                maybe_wrapper = maybe_wrapper._wrapped
            else:
                function = maybe_wrapper
                break
        
        wrappers.reverse()
        return function, wrappers


class SlashCommandPermissionOverwriteWrapper(SlashCommandWrapper):
    """
    Wraps a slash to command allowing / disallowing it only for the given user or role inside of a guild.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _guild_id : `int`
        The guild id where the overwrites should be applied to.
    _overwrite : ``ApplicationCommandPermissionOverwrite``
        The permission overwrite to apply.
    """
    __slots__ = ('_guild_id', '_overwrite')
    def __new__(cls, guild, target, allow):
        """
        Creates a partial function to wrap a slash command.
        
        Parameters
        ----------
        guild : ``Guild`` or `int`
            The guild's identifier where the overwrite is applied.
        target : ``ClientUserBase`` or ``Role``, `tuple` ((``ClientUserBase``, ``Role`` type) or \
                `str` (`'Role'`, `'role'`, `'User'`, `'user'`), `int`)
            The target entity of the overwrite
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role`` instance
            - ``ClientUserBase`` instance
            - `tuple` (``Role`` type, `int`)
            - `tuple` (``ClientUserBase``, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlashCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(f'`guild` can be given neither as `{Guild.__class__.__name__}`, and as `int` instance, '
                f'got {guild.__class__.__name__}.')
        
        overwrite = ApplicationCommandPermissionOverwrite(target, allow)
        
        return partial_func(cls._decorate, cls, guild_id, overwrite)
    
    def _decorate(cls, guild_id, overwrite, wrapped):
        """
        Wraps given command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild id where the overwrites should be applied to.
        overwrite : ``ApplicationCommandPermissionOverwrite``
            The permission overwrite to apply.
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlashCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._guild_id = guild_id
        self._overwrite = overwrite
        self._wrapped = wrapped
        return self

    def apply(self, slash_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
        """
        slash_command.add_overwrite(self._guild_id, self._overwrite)
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}, guild_id={self._guild_id!r}, ' \
            f'overwrite={self._overwrite!r}>'


RUNTIME_SYNC_HOOKS = []

def runtime_sync_hook_is_client_running(client):
    """
    Runtime sync hook to check whether a slash command should be registered and synced instantly when added or removed.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the ``Slasher``.
    """
    return client.running

RUNTIME_SYNC_HOOKS.append(runtime_sync_hook_is_client_running)


async def event_received_callback(waiter, client, event):
    """
    Callback added to ``Slasher`` by ``wait_for_component_interaction``.
    
    Parameters
    ----------
    waiter : ``Future``
        Interaction event waiter future.
    client : ``Client``
        The respective client instance.
    event : ``InteractionEvent``
        The received interaction event.
    """
    waiter.set_result_if_pending(event)


async def wait_for_component_interaction(event_or_message, *, timeout=None):
    """
    Waits for interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event_or_message : ``InteractionEvent``, ``Message``
        The interaction event or the sent message to wait component on.
    
    Returns
    ------
    interaction_event : ``InteractionEvent``
    
    Raises
    ------
    TimeoutError
        No component interaction was received in time
    TypeError
        `event_or_message` is neither ``Message`` nor ``InteractionEvent`` instance.
    ValueError
        The given message message has no bound interaction.
    RuntimeError
        The message or interaction is bound to a 3rd party application.
    """
    if isinstance(event_or_message, Message):
        message_interaction = event_or_message.interaction
        if message_interaction:
            raise ValueError(f'The given message has no bound interaction, got {event_or_message!r}.')
        
        message = event_or_message
        application_id = message_interaction.application_id
    
    elif isinstance(event_or_message, InteractionEvent):
        message = await event_or_message.wait_for_response_message(timeout=timeout)
        application_id = event_or_message.application_id
    
    else:
        raise TypeError(f'`event_or_message` can be either `{Message.__name__}` or `{InteractionEvent.__name__}` '
            f'instance, got {event_or_message.__class__.__name__}.')
    
    try:
        client = APPLICATION_ID_TO_CLIENT[application_id]
    except KeyError as err:
        raise RuntimeError(f'The message or interaction is bound to a 3rd party application, got: '
            f'{event_or_message!r}.') from err
    
    waiter = Future(KOKORO)
    if (timeout is not None):
        future_or_timeout(waiter, timeout)
    
    callback = partial_func(event_received_callback, waiter)
    client.slasher.append(message, callback)
    
    try:
        result = await waiter
    finally:
        client.slasher.remove(message, callback)
    
    return result
