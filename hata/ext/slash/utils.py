# -*- coding: utf-8 -*-
__all__ = ('SlashCommandPermissionOverwriteWrapper', 'SlashCommandWrapper', )

from functools import partial as partial_func

from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake
from ...discord.interaction import ApplicationCommandPermissionOverwrite

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
        target : ``User``, ``Client`` or ``Role``, `tuple` ((``User``, ``UserBase``, ``Role`` type) or \
                `str` (`'Role'`, `'role'`, `'User'`, `'user'`), `int`)
            The target entity of the overwrite
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role`` instance
            - ``User`` instance
            - ``Client`` instance
            - `tuple` (``Role`` type, `int`)
            - `tuple` (``User`` type, `int`)
            - `tuple` (``UserBase`` type, `int`)
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
