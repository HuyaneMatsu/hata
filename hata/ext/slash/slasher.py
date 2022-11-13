__all__ = ('Slasher', )

import warnings
from datetime import datetime, timedelta
from functools import partial as partial_func

from scarletio import (
    RichAttributeErrorBaseType, Task, WaitTillAll, WeakKeyDictionary, WeakReferer, export, run_coroutine
)

from ...discord.application_command import (
    APPLICATION_COMMAND_CONTEXT_TARGET_TYPES, ApplicationCommand, ApplicationCommandTargetType
)
from ...discord.client import Client
from ...discord.client.request_helpers import get_guild_id
from ...discord.core import KOKORO
from ...discord.events.handling_helpers import EventHandlerBase, Router, asynclist
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.guild import Guild
from ...discord.interaction import InteractionEvent, InteractionType

from .command import (
    CommandBase, CommandBaseApplicationCommand, ComponentCommand, ContextCommand, FormSubmitCommand, SlashCommand,
    SlashCommandParameterAutoCompleter, validate_application_target_type
)
from .command.command_base_application_command.constants import APPLICATION_COMMAND_HANDLER_DEEPNESS
from .command.component_command.constants import COMMAND_TARGETS_COMPONENT_COMMAND
from .command.form_submit_command.constants import COMMAND_TARGETS_FORM_COMPONENT_COMMAND
from .command.slash_command.helpers import _build_auto_complete_parameter_names, _register_auto_complete_function
from .exceptions import (
    SlasherSyncError, _register_exception_handler, _validate_random_error_message_getter,
    default_slasher_exception_handler, default_slasher_random_error_message_getter, test_exception_handler
)
from .helpers import validate_translation_table
from .permission_mismatch import (
    PermissionMismatchWarning, are_application_command_permission_overwrites_equal,
    check_and_warn_can_request_owners_access_of, create_permission_mismatch_message
)
from .utils import (
    RUNTIME_SYNC_HOOKS, SYNC_ID_GLOBAL, SYNC_ID_MAIN, SYNC_ID_NON_GLOBAL, UNLOADING_BEHAVIOUR_DELETE,
    UNLOADING_BEHAVIOUR_KEEP
)


INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE = InteractionType.application_command_autocomplete
INTERACTION_TYPE_FORM_SUBMIT = InteractionType.form_submit

# It is 7 days, but lets re-request after 6
OWNERS_ACCESS_REQUEST_INTERVAL = timedelta(days=6)


def match_application_commands_to_commands(application_commands, commands, match_schema):
    """
    Matches the given application commands to application commands.
    
    Parameters
    ----------
    application_commands : `list` of ``ApplicationCommand``
        Received application commands.
    commands : `None`, `list` of ``CommandBaseApplicationCommand``
        A list of application commands if any.
    match_schema : `bool`
        Whether schema or just name should be matched.
    
    Returns
    -------
    commands : `None`, `list` of ``CommandBaseApplicationCommand``
        The remaining matched commands.
    matched : `None`, `list` of `tuple` (``ApplicationCommand``, ``CommandBaseApplicationCommand`)
        The matched commands in pairs.
    """
    matched = None
    
    if (commands is not None):
        for application_command_index in reversed(range(len(application_commands))):
            application_command = application_commands[application_command_index]
            application_command_name = application_command.name
            application_command_target_type = application_command.target_type
            
            for command_index in reversed(range(len(commands))):
                command = commands[command_index]
                
                if command.name != application_command_name:
                    continue
                
                if command.target is not application_command_target_type:
                    continue
                
                if match_schema:
                    if (command.get_schema() != application_command):
                        continue
                
                del application_commands[application_command_index]
                del commands[command_index]
                
                if matched is None:
                    matched = []
                
                matched.append((application_command, command))
                break
        
        if not commands:
            commands = None
    
    return commands, matched


COMMAND_STATE_IDENTIFIER_NONE = 0
COMMAND_STATE_IDENTIFIER_ADDED = 1
COMMAND_STATE_IDENTIFIER_REMOVED = 2
COMMAND_STATE_IDENTIFIER_ACTIVE = 3
COMMAND_STATE_IDENTIFIER_KEPT = 4
COMMAND_STATE_IDENTIFIER_NON_GLOBAL = 5


class CommandChange(RichAttributeErrorBaseType):
    """
    Represents an added or removed command inside of ``CommandState._changes``
    
    Attributes
    ----------
    added : `bool`
        Whether the command was added.
    command : ``CommandBaseApplicationCommand``
        The command itself.
    """
    __slots__ = ('added', 'command')
    
    def __init__(self, added, command):
        """
        Creates a new command change instance.
        
        Parameters
        ----------
        added : `bool`
            Whether the command was added.
        command : ``CommandBaseApplicationCommand``
            The command itself.
        """
        self.added = added
        self.command = command
    
    def __repr__(self):
        """returns the command change's representation."""
        return f'{self.__class__.__name__}(added={self.added!r}, command={self.command!r})'
    
    def __iter__(self):
        """Unpacks the command change."""
        yield self.added
        yield self.command
    
    def __len__(self):
        """Helper for unpacking."""
        return 2


class CommandState(RichAttributeErrorBaseType):
    """
    Represents command's state inside of a guild.
    
    Attributes
    ----------
    _active : `None`, `list` of ``CommandBaseApplicationCommand``
        Active application commands, which were added.
    _changes : `None`, `list` of ``CommandChange``
        Newly added or removed commands in order.
    _is_non_global : `bool`
        Whether the command state is a command state of non global commands.
    _kept : `None`, `list` of ``CommandBaseApplicationCommand``
        Slash commands, which are removed, but should not be deleted.
    """
    __slots__ = ('_active', '_changes', '_is_non_global', '_kept', )
    
    def __init__(self, is_non_global):
        """
        Creates a new ``CommandState``.
        
        Parameters
        ----------
        is_non_global : `bool`
            Whether the command state refers to non-local commands.
        """
        self._changes = None
        self._active = None
        self._kept = None
        self._is_non_global = is_non_global
    
    def __repr__(self):
        """Returns the command state's representation."""
        result = ['<', self.__class__.__name__]
        if self._is_non_global:
            result.append(' (non global)')
        
        active = self._active
        if (active is not None) and active:
            result.append(' active=[')
            
            for command in active:
                result.append(command.name)
                result.append(', ')
            
            result[-1] = ']'
            
            should_add_comma = True
        else:
            should_add_comma = False
            
        kept = self._kept
        if (kept is not None) and kept:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' kept=[')
            
            for command in kept:
                result.append(command.name)
                result.append(', ')
            
            result[-1] = ']'
        
        changes = self._changes
        if (changes is not None):
            if should_add_comma:
                result.append(',')
            
            result.append(' changes=')
            result.append(repr(changes))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_should_add_application_commands(self):
        """
        Returns the commands, which should be added.
        
        Returns
        -------
        commands : `list` of ``CommandBaseApplicationCommand``
        """
        commands = []
        active = self._active
        if (active is not None):
            commands.extend(active)
        
        changes = self._changes
        if (changes is not None):
            for added, command in changes:
                command_name = command.name
                command_target_type = command.target
                
                for index in range(len(commands)):
                    iter_command = commands[index]
                    if iter_command.name != command_name:
                        continue
                    
                    if iter_command.target is not command_target_type:
                        continue
                    
                    if added:
                        commands[index] = command
                    else:
                        del commands[index]
                    
                    break
                
                else:
                    if added:
                        commands.append(command)
        
        return commands
    
    def get_should_keep_commands(self):
        """
        Returns the commands, which should be kept.
        
        Returns
        -------
        commands : `list` of ``CommandBaseApplicationCommand``
        """
        commands = []
        kept = self._kept
        if (kept is not None):
            commands.extend(kept)
        
        changes = self._changes
        if (changes is not None):
            for command_change_state in changes:
                command_name = command_change_state.command.name
                command_target_type = command_change_state.command.target
                
                for index in range(len(commands)):
                    iter_command = commands[index]
                    if iter_command.name != command_name:
                        continue
                    
                    if iter_command.target is not command_target_type:
                        continue
                    
                    del commands[index]
                    break
        
        return commands
    
    def get_should_remove_application_commands(self):
        """
        Returns the commands, which should be removed.
        
        Returns
        -------
        commands : `list` of ``CommandBaseApplicationCommand``
        """
        commands = []
        
        changes = self._changes
        if (changes is not None):
            for added, command in changes:
                command_name = command.name
                command_target_type = command.target
                
                for index in range(len(commands)):
                    iter_command = commands[index]
                    if iter_command.name != command_name:
                        continue
                    
                    if iter_command.target is not command_target_type:
                        continue
                    
                    if added:
                        del commands[index]
                    else:
                        commands[index] = command
                    
                    break
                else:
                    if not added:
                        commands.append(command)
        
        return commands
    
    
    def exhaust_kept_commands(self):
        """
        Iterates over the kept commands of the command state. Each yielded command is popped out.
        
        This function is an iterable generator.
        
        Yields
        ------
        Yields
        """
        kept_commands = self._kept
        
        if (kept_commands is not None):
            while kept_commands:
                yield kept_commands.pop()
        
        self._kept = None
    
    
    def _try_purge_from_changes(self, name, target_type):
        """
        Purges the commands with the given names from the changed ones.
        
        Parameters
        ----------
        name : `str`
            The command's name.
        target_type : ``ApplicationCommandTargetType``
            The commands' target type.
        
        Returns
        -------
        command : `None`, ``CommandBaseApplicationCommand``
            The purged command if any.
        purged_from_identifier : `int`
            From which internal container was the command purged from.
            
            Can be any of the following values:
            
            +-----------------------------------+-------+
            | Respective name                   | Value |
            +===================================+=======+
            | COMMAND_STATE_IDENTIFIER_NONE     | 0     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ADDED    | 1     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_REMOVED  | 2     |
            +-----------------------------------+-------+
        """
        changes = self._changes
        if (changes is not None):
            for index in range(len(changes)):
                command_change_state = changes[index]
                command = command_change_state.command
                if command.name != name:
                    continue
                
                if command.target is not target_type:
                    continue
                
                del changes[index]
                if not changes:
                    self._changes = None
                
                if command_change_state.added:
                    purged_from_identifier = COMMAND_STATE_IDENTIFIER_ADDED
                else:
                    purged_from_identifier = COMMAND_STATE_IDENTIFIER_REMOVED
                
                return purged_from_identifier, command
        
        return None, COMMAND_STATE_IDENTIFIER_NONE
    
    
    def _try_purge(self, name, target_type):
        """
        Tries to purge the commands from the given name from the command state.
        
        Parameters
        ----------
        name : `str`
            The respective command's name.
        target_type : ``ApplicationCommandTargetType``
            The respective command's target type.
        
        Returns
        -------
        command : `None`, ``CommandBaseApplicationCommand``
            The purged command if any.
        purged_from_identifier : `int`
            From which internal container was the command purged from.
            
            Can be any of the following values:
            
            +-----------------------------------+-------+
            | Respective name                   | Value |
            +===================================+=======+
            | COMMAND_STATE_IDENTIFIER_NONE     | 0     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ADDED    | 1     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_REMOVED  | 2     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE   | 3     |
            +-----------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT     | 4     |
            +-----------------------------------+-------+
        """
        from_changes_result = self._try_purge_from_changes(name, target_type)
        
        active = self._active
        if (active is not None):
            for index in range(len(active)):
                command = active[index]
                if (command.name == name) and (command.target is target_type):
                    del active[index]
                    if not active:
                        self._active = None
                    
                    return command, COMMAND_STATE_IDENTIFIER_ACTIVE
        
        kept = self._kept
        if (kept is not None):
            for index in range(len(kept)):
                command = kept[index]
                if (command.name == name) and (command.target is target_type):
                    del kept[index]
                    if not kept:
                        self._kept = None
                    
                    return command, COMMAND_STATE_IDENTIFIER_KEPT
        
        return from_changes_result
    
    
    def activate(self, command):
        """
        Adds the command to the ``CommandState`` as active.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
            The application command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name, command.target)
        active = self._active
        if active is None:
            self._active = active = []
        
        active.append(command)
    
    
    def keep(self, command):
        """
        Marks the command, as it should be kept.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
            The application command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name, command.target)
        kept = self._kept
        if kept is None:
            self._kept = kept = []
        
        kept.append(command)
    
    
    def delete(self, command):
        """
        Deletes the command from the command state.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
            The application command.
        """
        if self._is_non_global:
            return
        
        self._try_purge(command.name, command.target)
    
    
    def add(self, command):
        """
        Adds a command to the ``CommandState``.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
            The command to add.
        
        Returns
        -------
        command : ``CommandBaseApplicationCommand``
            The existing command or the given one.
        
        action_identifier : `int`
            The action what took place.
            
            It's value can be any of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | COMMAND_STATE_IDENTIFIER_ADDED        | 1     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE       | 3     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT         | 4     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_NON_GLOBAL   | 5     |
            +---------------------------------------+-------+
        """
        if self._is_non_global:
            existing_command, purge_identifier = self._try_purge(command.name, command.target)
            active = self._active
            if active is None:
                self._active = active = []
            
            active.append(command)
            return existing_command, COMMAND_STATE_IDENTIFIER_NON_GLOBAL
        
        kept = self._kept
        if (kept is not None):
            command_name = command.name
            command_target_type = command.target
            
            for index in range(len(kept)):
                kept_command = kept[index]
                if kept_command.name != command_name:
                    continue
                
                if kept_command.target is not command_target_type:
                    continue
                
                if kept_command != command:
                    continue
                
                del kept[index]
                if not kept:
                    self._kept = None
                
                self._try_purge_from_changes(command_name, command_target_type)
                return kept_command, COMMAND_STATE_IDENTIFIER_KEPT
        
        
        active = self._active
        if (active is not None):
            command_name = command.name
            command_target_type = command.target
            
            for index in range(len(active)):
                active_command = active[index]
                if active_command.name != command_name:
                    continue
                
                if active_command.target is not command_target_type:
                    continue
                
                if active_command != command:
                    continue
                
                del active[index]
                if not active:
                    self._active = None
                
                self._try_purge_from_changes(command_name, command_target_type)
                return active_command, COMMAND_STATE_IDENTIFIER_ACTIVE
        
        changes = self._changes
        if changes is None:
            self._changes = changes = []
        
        change = CommandChange(True, command)
        changes.append(change)
        return command, COMMAND_STATE_IDENTIFIER_ADDED
    
    def remove(self, command, slasher_unloading_behaviour):
        """
        Removes the command from the ``CommandState``.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
            The command to add.
        slasher_unloading_behaviour : `int`
            The parent slasher's unload behaviour.
            
            Can be any of the following:
            
            +-------------------------------+-------+
            | Respective name               | Value |
            +-------------------------------+-------+
            | UNLOADING_BEHAVIOUR_DELETE    | 0     |
            +-------------------------------+-------+
            | UNLOADING_BEHAVIOUR_KEEP      | 1     |
            +-------------------------------+-------+
        
        Returns
        -------
        command : ``CommandBaseApplicationCommand``
            The existing command or the given one.
        action_identifier : `int`
            The action what took place.
            
            It's value can be any of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | COMMAND_STATE_IDENTIFIER_REMOVED      | 2     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_ACTIVE       | 3     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_KEPT         | 4     |
            +---------------------------------------+-------+
            | COMMAND_STATE_IDENTIFIER_NON_GLOBAL   | 5     |
            +---------------------------------------+-------+
        """
        unloading_behaviour = command._unloading_behaviour
        if unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
            should_keep = False
        elif unloading_behaviour == UNLOADING_BEHAVIOUR_KEEP:
            should_keep = True
        else: # if unloading_behaviour == UNLOADING_BEHAVIOUR_INHERIT:
            if slasher_unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
                should_keep = False
            else: # if slasher_unloading_behaviour == UNLOADING_BEHAVIOUR_KEEP:
                should_keep = True
        
        if self._is_non_global:
            existing_command, purge_identifier = self._try_purge(command.name, command.target)
            if should_keep:
                kept = self._kept
                if kept is None:
                    self._kept = kept = []
                
                kept.append(command)
            
            return existing_command, COMMAND_STATE_IDENTIFIER_NON_GLOBAL
        
        if should_keep:
            self._try_purge_from_changes(command.name, command.target)
            
            kept = self._kept
            if (kept is not None):
                command_name = command.name
                command_target_type = command.target
                
                for index in range(len(kept)):
                    kept_command = kept[index]
                    if kept_command.name != command_name:
                        continue
                    
                    if kept_command.target is not command_target_type:
                        continue
                    
                    if kept_command != command:
                        continue
                    
                    return kept_command, COMMAND_STATE_IDENTIFIER_KEPT
            
            active = self._active
            if (active is not None):
                command_name = command.name
                command_target_type = command.target
                
                for index in range(len(active)):
                    active_command = active[index]
                    if active_command.name != command_name:
                        continue
                    
                    if active_command.target is not command_target_type:
                        continue
                    
                    if active_command != command:
                        continue
                    
                    del active[index]
                    if not active:
                        self._active = None
                    
                    kept = self._kept
                    if kept is None:
                        self._kept = kept = []
                    
                    kept.append(active_command)
                    return active_command, COMMAND_STATE_IDENTIFIER_ACTIVE
            
            kept = self._kept
            if kept is None:
                self._kept = kept = []
            
            kept.append(command)
            return command, COMMAND_STATE_IDENTIFIER_KEPT
        
        # We do not purge active
        kept = self._kept
        if (kept is not None):
            command_name = command.name
            command_target_type = command.target
            
            for index in range(len(kept)):
                kept_command = kept[index]
                if kept_command.name != command_name:
                    continue
                
                if kept_command.target is not command_target_type:
                    continue
                
                if kept_command != command:
                    continue
                
                del kept[index]
                break
        
        changes = self._changes
        if changes is None:
            self._changes = changes = []
        
        change = CommandChange(False, command)
        changes.append(change)
        return command, COMMAND_STATE_IDENTIFIER_REMOVED
    
    
    def get_active_command_count(self):
        """
        Gets the active commands of the command state.
        
        Returns
        -------
        active_command_count : `int`
        """
        active = self._active
        if active is None:
            active_command_count = 0
        else:
            active_command_count = len(active)
        
        return active_command_count
    
    
    def get_active_command_count_with_sub_commands(self):
        """
        Gets the active commands of the command state including the sub command count as well.
        
        Returns
        -------
        active_command_count_with_sub_commands : `int`
        """
        active_command_count_with_sub_commands = 0
        
        active = self._active
        if (active is not None):
            for command in active:
                active_command_count_with_sub_commands += command.get_real_command_count()
        
        return active_command_count_with_sub_commands


@export
class Slasher(EventHandlerBase):
    """
    Slash command processor.
    
    Attributes
    ----------
    _assert_application_command_permission_missmatch_at : `None`, `set` of `int`
        The guilds' identifier, where permission overwrites missmatch should be asserted.
    
    _auto_completers : `None`, `list` of ``SlashCommandParameterAutoCompleter``
        Auto completer functions.
    
    _call_later : `None`, `list` of `tuple` (`bool`, `Any`)
        Slash command changes to apply later if syncing is in progress.
    
    _client_reference : ``WeakReferer`` to ``Client``
        Weak reference to the parent client.
    
    _command_states : `dict` of (`int`, ``CommandState``) items
        The slasher's commands' states.
    
    _command_unloading_behaviour : `int`
        Behaviour to describe what should happen when a command is unloaded.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
    
    _component_commands : `set` of ``ComponentCommand``
        The component commands added to the slasher.
    
    _component_interaction_waiters : ``WeakKeyDictionary`` of (``Message``, `async-callable`) items
        Whenever a component interaction is received on a message, it's respective waiters will be endured inside of
        a ``Task``.
    
    _enforce_application_command_permissions : `bool`
        Whether application command permissions should be enforced where they are asserted.
        
        > This only works if the application is NOT owned by a team.
    
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        The following parameters are passed to it:
        
        +-------------------+-------------------------------------------------------------------------------+
        | Name              | Type                                                                          |
        +===================+===============================================================================+
        | client            | ``Client``                                                                    |
        +-------------------+-------------------------------------------------------------------------------+
        | interaction_event | ``InteractionEvent``                                                          |
        +-------------------+-------------------------------------------------------------------------------+
        | command           | ``ComponentCommand``, ``ContextCommand``, ``SlashCommand``,                   |
        |                   | ``SlashCommandFunction``, ``SlashCommandCategory``                            |
        |                   | ``SlashCommandParameterAutoCompleter``, ``FormSubmitCommand``                 |
        +-------------------+-------------------------------------------------------------------------------+
        | exception         | `BaseException`                                                               |
        +-------------------+-------------------------------------------------------------------------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | handled           | `bool`    |
        +-------------------+-----------+
    
    _form_submit_commands : `set` of ``FormSubmitCommand``
        The form commands added to the slasher.
    
    _regex_custom_id_to_component_command : `dict` of (``RegexMatcher``, ``ComponentCommand``) items
        A dictionary which contains component commands based on regex patterns.
    
    _regex_custom_id_to_form_submit_command : `dict` of (``RegexMatcher``, ``FormSubmitCommand``) items
        A dictionary which contains form submit commands based on regex patterns.
    
    _self_reference : `None`, ``WeakReferer`` to ``Slasher``
        Reference back to the slasher. Used to reference back from commands.
    
    _string_custom_id_to_component_command : `dict` of (`str`, ``ComponentCommand``) items
        A dictionary which contains component commands by their `custom_id`.
    
    _string_custom_id_to_form_submit_command : `dict` of (`str`, ``FormSubmitCommand``) items
        A dictionary which contains form submit commands by their `custom_id`.
    
    _sync_done : `set` of `int`
        A set of guild id-s which are synced.
    
    _get_permission_tasks : `dict` of (`int`, ``Task``) items
        A dictionary of `guild-id` - `permission getter` tasks.
    
    _guild_level_permission_overwrites : `None`, `dict` of `set` of ``ApplicationCommandPermissionOverwrite``
        Guild level permission overwrites to apply.
    
    _owners_access : `None`, ``Oauth2Access`
        Oauth2 access of the client's owner.
    
    _owners_access_get_impossible : `bool`
        Whether the retrieving the owner's access is possible.
    
    _owners_access_get_task : `None`, ``Task``
        Synchronised task for requesting the owner's access.
    
    _sync_should : `set` of `int`
        A set of guild id-s which should be synced.
    
    _sync_tasks : `dict` of (`int, ``Task``) items
        A dictionary of guilds, which are in sync at the moment.
    
    _synced_permissions : `dict` of (`int`, `dict` of (`int`, ``ApplicationCommandPermission``) items) items
        A nested dictionary, which contains application command permission overwrites per guild_id and per
        `command_id`.
    
    _translation_table : `None`, `dict` of (``Locale`, `dict` of (`str`, `str`) items) items
        Translation table for the commands of the slasher.
    
    command_id_to_command : `dict` of (`int`, ``SlashCommand``) items
        A dictionary where the keys are application command id-s and the keys are their respective command.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = 'interaction_create'
        Tells for the ``EventHandlerManager`` that ``Slasher`` is a `interaction_create` event handler.
    
    SUPPORTED_TYPES : `tuple` (``SlashCommand``, ``ComponentCommand``, ``FormSubmitCommand``)
        Tells to ``eventlist`` what exact types the ``Slasher`` accepts.
    
    Notes
    -----
    ``Slasher``-s are weakreferable.
    """
    __slots__ = (
        '__weakref__', '_assert_application_command_permission_missmatch_at', '_auto_completers', '_call_later',
        '_client_reference', '_command_states', '_command_unloading_behaviour', '_component_commands',
        '_component_interaction_waiters', '_enforce_application_command_permissions', '_exception_handlers',
        '_form_submit_commands', '_get_permission_tasks', '_guild_level_permission_overwrites', '_owners_access',
        '_owners_access_get_impossible', '_owners_access_get_task', '_random_error_message_getter',
        '_regex_custom_id_to_component_command', '_regex_custom_id_to_form_submit_command', '_self_reference',
        '_string_custom_id_to_component_command', '_string_custom_id_to_form_submit_command', '_sync_done',
        '_sync_should', '_sync_tasks', '_synced_permissions', '_translation_table', 'command_id_to_command'
    )
    
    __event_name__ = 'interaction_create'
    
    SUPPORTED_TYPES = (SlashCommand, ContextCommand, ComponentCommand, FormSubmitCommand)
    
    def __new__(
        cls,
        client,
        assert_application_command_permission_missmatch_at = None,
        delete_commands_on_unload = False,
        enforce_application_command_permissions = False,
        use_default_exception_handler = True,
        random_error_message_getter = None,
        translation_table = None
    ):
        """
        Creates a new interaction event handler.
        
        Parameters
        ----------
        client : ``Client``
            The owner client instance.
            
        assert_application_command_permission_missmatch_at : `None`, `int`, ``Guild``, `iterable` of (`int`, ``Guild``)
                = `None`, Optional (Keyword only)
            Guilds, where permission overwrites missmatch should be asserted.
        
        delete_commands_on_unload: `bool`, Optional (Keyword only)
            Whether commands should be deleted when unloaded.
        
        enforce_application_command_permissions : `bool` = `False`, Optional (Keyword only)
            Whether application command permissions should be enforced where they are asserted.
            
            > This only works if the application is NOT owned by a team.
        
        random_error_message_getter : `None`, `FunctionType` = `None`, Optional (Keyword only)
            Random error message getter used by the default exception handler.
        
        translation_table : `None`, `str`, `dict` of ((``Locale``, `str`),
                (`None`, `dict` of (`str`, (`None`, `str`)) items)) items, Optional
            Translation table for the commands of the slasher.
        
        use_default_exception_handler : `bool`, Optional (Keyword only)
            Whether the default slash exception handler should be added as an exception handler.
        
        Raises
        ------
        FileNotFoundError
            - If `translation_table` is a string, but not a file.
        TypeError
            - If `delete_commands_on_unload` was not given as `bool`.
            - If `use_default_exception_handler` was not given as `bool`.
            - If `client` was not given as ``Client``.
            - If `translation_table`'s structure is incorrect.
        """
        # client
        if not isinstance(client, Client):
            raise TypeError(
                f'`client` can be `{Client.__name__}`, got {client.__class__.__name__}; {client!r}.'
            )
        
        client_reference = WeakReferer(client)
        
        # assert_application_command_permission_missmatch_at
        
        if assert_application_command_permission_missmatch_at is None:
            asserted_guild_ids = None
        else:
            asserted_guild_ids = set()
            
            if isinstance(assert_application_command_permission_missmatch_at, Guild):
                asserted_guild_ids.add(assert_application_command_permission_missmatch_at.id)
            
            elif type(assert_application_command_permission_missmatch_at) is int:
                asserted_guild_ids.add(assert_application_command_permission_missmatch_at)
            
            elif isinstance(assert_application_command_permission_missmatch_at, int):
                asserted_guild_ids.add(int(assert_application_command_permission_missmatch_at))
            
            else:
                iterator = getattr(type(assert_application_command_permission_missmatch_at), '__iter__', None)
                if iterator is None:
                    raise TypeError(
                        f'`assert_application_command_permission_missmatch_at` can be `iterable`, got {assert_application_command_permission_missmatch_at.__class__.__name__}; '
                        f'{assert_application_command_permission_missmatch_at!r}.'
                    )
                
                for additional_owner in iterator(assert_application_command_permission_missmatch_at):
                    if type(additional_owner) is int:
                        pass
                    elif isinstance(additional_owner, int):
                        additional_owner = int(additional_owner)
                    elif isinstance(additional_owner, Guild):
                        additional_owner = additional_owner.id
                    else:
                        raise TypeError(
                            f'`assert_application_command_permission_missmatch_at` contains a non `int`, `{Guild.__name__}` , got '
                            f'{additional_owner.__class__.__name__}; {additional_owner!r}.'
                        )
                    
                    asserted_guild_ids.add(additional_owner)
                
                if (not asserted_guild_ids):
                    asserted_guild_ids = None
        
        # delete_commands_on_unload
        if type(delete_commands_on_unload) is bool:
            pass
        elif isinstance(delete_commands_on_unload, bool):
            delete_commands_on_unload = bool(delete_commands_on_unload)
        else:
            raise TypeError(
                f'`delete_commands_on_unload` can be `bool`, got '
                f'{delete_commands_on_unload.__class__.__name__}; {delete_commands_on_unload!r}.'
            )
        
        if delete_commands_on_unload:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        # enforce_application_command_permissions
        if type(enforce_application_command_permissions) is bool:
            pass
        elif isinstance(enforce_application_command_permissions, bool):
            enforce_application_command_permissions = bool(enforce_application_command_permissions)
        else:
            raise TypeError(
                f'`enforce_application_command_permissions` can be `bool`, got '
                f'{enforce_application_command_permissions.__class__.__name__};'
                f'{enforce_application_command_permissions!r}.'
            )
        
        # random_error_message_getter
        if random_error_message_getter is None:
            random_error_message_getter = default_slasher_random_error_message_getter
        else:
            _validate_random_error_message_getter(random_error_message_getter)
        
        # translation_table
        translation_table = validate_translation_table(translation_table)
        
        # use_default_exception_handler
        if type(use_default_exception_handler) is bool:
            pass
        elif isinstance(use_default_exception_handler, bool):
            use_default_exception_handler = bool(use_default_exception_handler)
        else:
            raise TypeError(
                f'`use_default_exception_handler` can be `bool`, got '
                f'{use_default_exception_handler.__class__.__name__}; {use_default_exception_handler!r}.'
            )
        
        if use_default_exception_handler:
            exception_handlers = [default_slasher_exception_handler]
        else:
            exception_handlers = None
        
        
        self = object.__new__(cls)
        self._call_later = None
        self._client_reference = client_reference
        self._command_unloading_behaviour = command_unloading_behaviour
        self._command_states = {}
        self._sync_tasks = {}
        self._sync_should = set()
        self._sync_done = set()
        self._get_permission_tasks = {}
        self._synced_permissions = {}
        self._component_interaction_waiters = WeakKeyDictionary()
        self._random_error_message_getter = random_error_message_getter
        self._translation_table = translation_table
        
        self.command_id_to_command = {}
        
        self._component_commands = set()
        self._string_custom_id_to_component_command = {}
        self._regex_custom_id_to_component_command = {}
        
        self._form_submit_commands = set()
        self._string_custom_id_to_form_submit_command = {}
        self._regex_custom_id_to_form_submit_command = {}
        
        self._exception_handlers = exception_handlers
        self._self_reference = None
        self._auto_completers = None
        
        self._assert_application_command_permission_missmatch_at = asserted_guild_ids
        self._enforce_application_command_permissions = enforce_application_command_permissions
        
        self._owners_access = None
        self._owners_access_get_impossible = False
        self._owners_access_get_task = None
        self._guild_level_permission_overwrites = None
        
        return self
    
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slasher, processing a received interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        interaction_event_type = interaction_event.type
        if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
            await self._dispatch_application_command_event(client, interaction_event)
        
        elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
            await self._dispatch_component_event(client, interaction_event)
        
        elif interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE:
            await self._dispatch_application_command_autocomplete_event(client, interaction_event)
        
        elif interaction_event_type is INTERACTION_TYPE_FORM_SUBMIT:
            await self._dispatch_form_submit_event(client, interaction_event)
    
    
    async def _dispatch_application_command_event(self, client, interaction_event):
        """
        Dispatches an application command interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        try:
            command = await self._try_get_command_by_id(client, interaction_event)
        except GeneratorExit:
            raise
        
        except ConnectionError:
            return
        except BaseException as err:
            await client.events.error(client, f'{self!r}._dispatch_application_command_event', err)
        else:
            if (command is not None):
                await command.invoke(client, interaction_event)
    
    
    async def _dispatch_component_event(self, client, interaction_event):
        """
        Dispatches a component interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        try:
            waiter = self._component_interaction_waiters[interaction_event.message]
        except KeyError:
            pass
        else:
            if isinstance(waiter, asynclist):
                for waiter in waiter:
                    Task(waiter(interaction_event), KOKORO)
            else:
                Task(waiter(interaction_event), KOKORO)
            
            return
        
        custom_id = interaction_event.interaction.custom_id
        try:
            component_command = self._string_custom_id_to_component_command[custom_id]
        except KeyError:
            for regex_matcher in self._regex_custom_id_to_component_command:
                regex_match = regex_matcher(custom_id)
                if (regex_match is None):
                    continue
                
                component_command = self._regex_custom_id_to_component_command[regex_matcher]
                break
            else:
                return
        else:
            regex_match = None
        
        await component_command.invoke(client, interaction_event, regex_match)
    
    
    async def _dispatch_application_command_autocomplete_event(self, client, interaction_event):
        """
        Dispatches an application command interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        auto_complete_option = interaction_event.interaction
        if auto_complete_option.options is None:
            return
        
        try:
            command = await self._try_get_command_by_id(client, interaction_event)
        except GeneratorExit:
            raise
        
        except ConnectionError:
            return
        
        except BaseException as err:
            await client.events.error(client, f'{self!r}._dispatch_application_command_autocomplete_event', err)
        
        else:
            if (command is not None):
                await command.invoke_auto_completion(client, interaction_event, auto_complete_option)
    
    
    async def _dispatch_form_submit_event(self, client, interaction_event):
        """
        Dispatches a form submit interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the interaction.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        custom_id = interaction_event.interaction.custom_id
        try:
            form_submit_command = self._string_custom_id_to_form_submit_command[custom_id]
        except KeyError:
            for regex_matcher in self._regex_custom_id_to_form_submit_command:
                regex_match = regex_matcher(custom_id)
                if (regex_match is None):
                    continue
                
                form_submit_command = self._regex_custom_id_to_form_submit_command[regex_matcher]
                break
            else:
                return
        else:
            regex_match = None
        
        await form_submit_command.invoke(client, interaction_event, regex_match)
    
    
    def add_component_interaction_waiter(self, message, waiter):
        """
        Adds an component interaction waiter for the given message.
        
        Parameters
        ----------
        message : ``Message``
            The message to wait component interactions on.
        waiter : `async-callable`
            The waiter to call when the respective event occurs.
        """
        component_interaction_waiters = self._component_interaction_waiters
        try:
            actual_waiter = component_interaction_waiters[message]
        except KeyError:
            component_interaction_waiters[message] = waiter
        else:
            if type(actual_waiter) is asynclist:
                list.append(actual_waiter, waiter)
            else:
                new_waiter = asynclist()
                list.append(new_waiter, waiter)
                list.append(new_waiter, actual_waiter)
                component_interaction_waiters[message] = new_waiter
    
    
    def remove_component_interaction_waiter(self, message, waiter):
        """
        Removes a component interaction waiter for the given message.
        
        Parameters
        ----------
        message : ``Message``
            The message on which the waiter waits on.
        waiter : `async-callable`
            The waiter to remove.
        """
        component_interaction_waiters = self._component_interaction_waiters
        try:
            actual_waiter = component_interaction_waiters.pop(message)
        except KeyError:
            return
        
        if type(actual_waiter) is not asynclist:
            return
        
        try:
            list.remove(actual_waiter, waiter)
        except ValueError:
            pass
        else:
            if len(actual_waiter) == 1:
                self._component_interaction_waiters[message] = actual_waiter[0]
                return
        
        self._component_interaction_waiters[message] = actual_waiter
    
    
    def create_event(self, func, *args, target = None, **kwargs):
        """
        Adds a command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective command.
        
        name : `None`, `str`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any`, `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        is_global : `None`, `bool`, `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the application command command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        is_default : `None`, `bool`, `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the command is the default command in it's category.
        delete_on_unload : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command should be deleted from Discord when removed.
        allow_by_default : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command is enabled by default for everyone who has `use_application_commands` permission.
            
            > This field is deprecated.
        
        allow_in_dm : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`), Optional
            Whether the command can be used in private channels (dm).
        custom_id : `str`, (`list`, `set`) of `str`, `tuple` of (`str`, (`list`, `set`) of `str`)
            Custom id to match by the component command.
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, \
                `list` of (`str`, ``UserBase``, ``Role`` ), Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        target : `None`, `int`, `str`, ``ApplicationCommandTargetType`` = `None`, Optional
            The target type of the command.
        
        Returns
        -------
        func : ``CommandBase``
             The created or added command.
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, CommandBaseApplicationCommand):
            self._add_application_command(func)
            return func
        
        if isinstance(func, ComponentCommand):
            self._add_component_command(func)
            return func
        
        if isinstance(func, FormSubmitCommand):
            self._add_form_submit_command(func)
            return func
        
        
        if 'custom_id' in kwargs:
            if (target is None) or (target in COMMAND_TARGETS_COMPONENT_COMMAND):
                command = ComponentCommand(func, *args, **kwargs)
            
            elif (target in COMMAND_TARGETS_FORM_COMPONENT_COMMAND):
                command = FormSubmitCommand(func, *args, **kwargs)
            
            else:
                raise ValueError(
                    f'Unknown command target: {target!r}; If `custom_id` parameter is given, `target` '
                    f'can be any of: `{COMMAND_TARGETS_COMPONENT_COMMAND | COMMAND_TARGETS_FORM_COMPONENT_COMMAND}`.'
                )
        
        else:
            target = validate_application_target_type(target)
            if target in APPLICATION_COMMAND_CONTEXT_TARGET_TYPES:
                command = ContextCommand(func, *args, **kwargs, target = target)
            else:
                command = SlashCommand(func, *args, **kwargs)
        
        if isinstance(command, Router):
            command = command[0]
        
        # Register command
        
        if isinstance(command, CommandBaseApplicationCommand):
            self._add_application_command(command)
        
        elif isinstance(command, ComponentCommand):
            self._add_component_command(command)
        
        elif isinstance(command, FormSubmitCommand):
            self._add_form_submit_command(command)
        
        else:
            # No more cases
            pass
        
        return command
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        func : ``CommandBase``
             The created or added command.
        
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        """
        target = getattr(klass, 'target', None)
        
        if hasattr(klass, 'custom_id'):
            if (target is None) or (target in COMMAND_TARGETS_COMPONENT_COMMAND):
                command = ComponentCommand.from_class(klass)
            
            elif (target in COMMAND_TARGETS_FORM_COMPONENT_COMMAND):
                command = FormSubmitCommand.from_class(klass)
            
            else:
                raise ValueError(
                    f'Unknown command target: {target!r}; If `custom_id` parameter is given, `target` '
                    f'can be any of: `{COMMAND_TARGETS_COMPONENT_COMMAND | COMMAND_TARGETS_FORM_COMPONENT_COMMAND}`.'
                )
        
        else:
            target = validate_application_target_type(target)
            if target in APPLICATION_COMMAND_CONTEXT_TARGET_TYPES:
                command = ContextCommand.from_class(klass)
            
            else:
                command = SlashCommand.from_class(klass)
        
        
        if isinstance(command, Router):
            command = command[0]
        
        if isinstance(command, SlashCommand):
            self._add_application_command(command)
        else:
            self._add_component_command(command)
        
        return command
    
    
    def _add_application_command(self, command):
        """
        Adds a application command to the ``Slasher`` if applicable.
        
        Parameters
        ---------
        command : ``CommandBaseApplicationCommand``
            The command to add.
        """
        command._parent_reference = self._get_self_reference()
        
        if self._check_late_register(command, True):
            return
        
        self._register_application_command(command)
        
        self._maybe_sync()
    
    
    def _register_application_command(self, command):
        """
        Registers the given application command.
        
        Parameters
        ---------
        command : ``CommandBaseApplicationCommand``
            The command to add.
        """
        for sync_id in command._iter_sync_ids():
            if sync_id == SYNC_ID_NON_GLOBAL:
                is_non_global = True
            else:
                is_non_global = False
            
            try:
                command_state = self._command_states[sync_id]
            except KeyError:
                command_state = self._command_states[sync_id] = CommandState(is_non_global)
            
            command, change_identifier = command_state.add(command)
            if change_identifier == COMMAND_STATE_IDENTIFIER_ADDED:
                self._sync_done.discard(sync_id)
                self._sync_should.add(sync_id)
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_ACTIVE:
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_KEPT:
                for application_command_id in command._iter_application_command_ids():
                    self.command_id_to_command[application_command_id] = command
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_NON_GLOBAL:
                continue
    
    
    def _remove_application_command(self, command):
        """
        Tries to remove the given command from the ``Slasher``.
        
        Parameters
        ----------
        command : ``Command``
            The command to remove.
        """
        if self._check_late_register(command, False):
            return
        
        self._unregister_application_command(command)
        
        self._maybe_sync()
    
    
    def _unregister_application_command(self, command):
        """
        Unregisters the given application command.
        
        Parameters
        ----------
        command : ``Command``
            The command to remove.
        """
        for sync_id in command._iter_sync_ids():
            
            if sync_id == SYNC_ID_NON_GLOBAL:
                is_non_global = True
            else:
                is_non_global = False
            
            try:
                command_state = self._command_states[sync_id]
            except KeyError:
                command_state = self._command_states[sync_id] = CommandState(is_non_global)
            
            removed_command, change_identifier = command_state.remove(command, self._command_unloading_behaviour)
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_REMOVED:
                if sync_id == SYNC_ID_NON_GLOBAL:
                    for guild_id in removed_command._iter_guild_ids():
                        self._sync_should.add(guild_id)
                        self._sync_done.discard(guild_id)
                else:
                    self._sync_should.add(sync_id)
                    self._sync_done.discard(sync_id)
                
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_ACTIVE:
                for application_command_id in removed_command._iter_application_command_ids():
                    try:
                        del self.command_id_to_command[application_command_id]
                    except KeyError:
                        pass
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_KEPT:
                continue
            
            if change_identifier == COMMAND_STATE_IDENTIFIER_NON_GLOBAL:
                if (removed_command is not None):
                    for guild_id in removed_command._iter_guild_ids():
                        self._sync_done.discard(guild_id)
                        self._sync_should.add(guild_id)
                continue
    
    def _check_late_register(self, command, add):
        """
        Checks whether the given command should be registered only later.
        
        command : ``Command``
            The command to register or unregister later.
        add : `bool`
            Whether the command should be registered or unregistered.
        
        Returns
        -------
        later : `bool`
            Whether the command should be registered only later
        """
        if SYNC_ID_MAIN in self._sync_tasks:
            call_later = self._call_later
            if call_later is None:
                call_later = self._call_later = []
            
            call_later.append((add, command))
            
            later = True
        else:
            later = False
        
        return later
    
    def _late_register(self):
        """
        Register late-registered commands.
        
        Returns
        -------
        registered_any : `bool`
            Whether any command was registered or unregistered.
        """
        call_later = self._call_later
        if call_later is None:
            registered_any = False
        else:
            while call_later:
                add, command = call_later.pop()
                if add:
                    self._register_application_command(command)
                else:
                    self._unregister_application_command(command)
            
            self._call_later = None
            registered_any = True
        
        return registered_any
    
    
    def delete_event(self, func, name=None):
        """
        A method to remove a command by itself, or by it's function and name combination if defined.
        
        Parameters
        ----------
        func : ``CommandBase``, ``Router`` of ``CommandBase``
            The command to remove.
        name : `None`, `str` = `None`, Optional
            The command's name to remove.
        
        Raises
        ------
        TypeError
            If `func` was not given neither as ``CommandBase`` not as ``Router`` of ``CommandBase``.
        """
        if isinstance(func, Router):
            for sub_func in func:
                if not isinstance(sub_func, CommandBase):
                    raise TypeError(
                        f'`func` can be `{CommandBase.__name__}`, '
                        f'`{Router.__name__}` of `{CommandBase.__name__}`, got {func!r}.'
                    )
            
            commands = tuple(func)
        
        elif isinstance(func, CommandBase):
            commands = (func, )
        
        else:
            raise TypeError(
                f'`func` can be `{CommandBase.__name__}`, `{Router.__name__}` of '
                f'`{CommandBase.__name__}`, got {func!r}.'
            )
        
        for command in commands:
            if isinstance(command, CommandBaseApplicationCommand):
                self._remove_application_command(func)
            
            elif isinstance(command, ComponentCommand):
                self._remove_component_command(func)
            
            elif isinstance(command, FormSubmitCommand):
                self._remove_form_submit_command(func)
    
    
    async def _try_get_command_by_id(self, client, interaction_event):
        """
        Tries to get the command by id. If found it, returns it, if not, returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client instance, who received the interaction event.
        interaction_event : ``InteractionEvent``
            The invoked interaction.
        """
        interaction_id = interaction_event.interaction.id
        try:
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
        
        # First request guild commands
        guild = interaction_event.guild
        if (guild is not None):
            guild_id = guild.id
            if not await self._sync_guild(client, guild_id):
                return None
            
            try:
                command = self.command_id_to_command[interaction_id]
            except KeyError:
                pass
            else:
                return command
        
        if not await self._sync_global(client):
            return None
        
        try:
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
    
    
    async def _sync_guild(self, client, guild_id):
        """
        Syncs the respective guild's commands if not yet synced.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if guild_id in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[guild_id]
        except KeyError:
            task = self._sync_tasks[guild_id] = Task(self._sync_guild_task(client, guild_id), KOKORO)
        
        return await task
    
    async def _sync_global(self, client):
        """
        Syncs the not yet synced global commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if SYNC_ID_GLOBAL in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_GLOBAL]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_GLOBAL] = Task(self._sync_global_task(client), KOKORO)
        
        return await task
    
    
    def _unregister_helper(self, command, command_state, guild_id):
        """
        Unregisters all the call relations of the given command.
        
        Parameters
        ----------
        command : `None`, ``CommandBaseApplicationCommand``
            The application command to unregister.
        command_state : `None`, ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        """
        if (command is not None):
            command_id = command._pop_command_id_for(guild_id)
            if command_id:
                try:
                    del self.command_id_to_command[command_id]
                except KeyError:
                    pass
            
            if (command_state is not None):
                command_state.delete(command)
    
    
    def _register_helper(self, command, command_state, guild_id, application_command_id):
        """
        Registers the given command, guild id, application command relationship.
        
        Parameters
        ----------
        command : `None`, ``CommandBaseApplicationCommand``
            The application command to register.
        command_state : `None`, ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        application_command_id : `int`
            The respective command's identifier.
        """
        if (command is not None):
            self.command_id_to_command[application_command_id] = command
            command._register_guild_and_application_command_id(guild_id, application_command_id)
            if (command_state is not None):
                command_state.activate(command)
    
    
    def _keep_helper(self, command, command_state, guild_id):
        """
        Marks the given command to be kept at the given guild.
        
        Parameters
        ----------
        command : `None`, ``CommandBaseApplicationCommand``
            The application command to register.
        command_state : `None`, ``CommandState``
            The command's respective state instance.
        guild_id : `int`
            The respective guild's id.
        """
        if (command is not None):
            command_id = command._pop_command_id_for(guild_id)
            if command_id:
                try:
                    del self.command_id_to_command[command_id]
                except KeyError:
                    pass
            
            if (command_state is not None):
                command_state.keep(command)
    
    
    async def _sync_guild_task(self, client, guild_id):
        """
        Syncs the respective guild's commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        success = False
        
        try:
            application_commands = await client.application_command_guild_get_all(guild_id)
        except GeneratorExit:
            raise
        
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_guild_task', err)
        
        else:
            guild_command_state = self._command_states.get(guild_id, None)
            if guild_command_state is None:
                guild_added_commands = None
                guild_keep_commands = None
                guild_removed_commands = None
            
            else:
                guild_added_commands = guild_command_state.get_should_add_application_commands()
                if not guild_added_commands:
                    guild_added_commands = None
                
                guild_keep_commands = guild_command_state.get_should_keep_commands()
                if not guild_keep_commands:
                    guild_keep_commands = None
                
                guild_removed_commands = guild_command_state.get_should_remove_application_commands()
                if not guild_removed_commands:
                    guild_removed_commands = None
            
            non_global_command_state = self._command_states.get(SYNC_ID_NON_GLOBAL, None)
            if non_global_command_state is None:
                non_global_added_commands = None
                non_global_keep_commands = None
            else:
                non_global_added_commands = non_global_command_state.get_should_add_application_commands()
                if not non_global_added_commands:
                    non_global_added_commands = None
                
                non_global_keep_commands = non_global_command_state.get_should_keep_commands()
                if not non_global_keep_commands:
                    non_global_keep_commands = None
            
            command_create_callbacks = None
            command_edit_callbacks = None
            command_delete_callbacks = None
            command_register_callbacks = None
            guild_permission_sync_callbacks = None
            
            guild_added_commands, matched = match_application_commands_to_commands(
                application_commands, guild_added_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._sync_permissions_then_register, self, client, command, guild_command_state,
                        guild_id, application_command
                    )
                    
                    if command_register_callbacks is None:
                        command_register_callbacks = []
                    command_register_callbacks.append(callback)
            
            non_global_added_commands, matched = match_application_commands_to_commands(
                application_commands, non_global_added_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._sync_permissions_then_register, self, client, command, non_global_command_state,
                        guild_id, application_command
                    )
                    
                    if command_register_callbacks is None:
                        command_register_callbacks = []
                    command_register_callbacks.append(callback)
            
            guild_added_commands, matched = match_application_commands_to_commands(
                application_commands, guild_added_commands, False
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._edit_command, self, client, command, guild_command_state, guild_id,
                        application_command
                    )
                    
                    if command_edit_callbacks is None:
                        command_edit_callbacks = []
                    command_edit_callbacks.append(callback)
            
            non_global_added_commands, matched = match_application_commands_to_commands(
                application_commands, non_global_added_commands, False
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._edit_guild_command_to_non_global, self, client, command,
                        non_global_command_state, guild_id, application_command
                    )
                    if command_edit_callbacks is None:
                        command_edit_callbacks = []
                    command_edit_callbacks.append(callback)
            
            guild_keep_commands, matched = match_application_commands_to_commands(
                application_commands, guild_keep_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, guild_command_state, guild_id)
            
            non_global_keep_commands, matched = match_application_commands_to_commands(
                application_commands, non_global_keep_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, non_global_command_state, guild_id)
            
            guild_removed_commands, matched = match_application_commands_to_commands(
                application_commands, guild_removed_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._delete_command, self, client, command, guild_command_state, guild_id,
                        application_command
                    )
                    if command_delete_callbacks is None:
                        command_delete_callbacks = []
                    command_delete_callbacks.append(callback)
            
            if (guild_added_commands is not None):
                while guild_added_commands:
                    command = guild_added_commands.pop()
                    
                    callback = (type(self)._create_command, self, client, command, guild_command_state, guild_id)
                    if command_create_callbacks is None:
                        command_create_callbacks = []
                    command_create_callbacks.append(callback)
                    continue
            
            while application_commands:
                application_command = application_commands.pop()
                
                callback = (type(self)._delete_command, self, client, None, None, guild_id, application_command)
                if command_delete_callbacks is None:
                    command_delete_callbacks = []
                command_delete_callbacks.append(callback)
            
            assert_application_command_permission_missmatch_at = \
                self._assert_application_command_permission_missmatch_at
            
            if (
                (assert_application_command_permission_missmatch_at is not None) and
                (guild_id in assert_application_command_permission_missmatch_at)
            ):
                guild_permission_sync_callbacks = [
                    (type(self)._sync_permissions_task, self, client, guild_id, None, None),
                ]
            
            success = True
            for callbacks in (
                guild_permission_sync_callbacks, command_register_callbacks, command_delete_callbacks,
                command_edit_callbacks, command_create_callbacks,
            ):
                if (callbacks is not None):
                    done, pending = await WaitTillAll(
                        [Task(callback[0](*callback[1:]), KOKORO) for callback in callbacks],
                        KOKORO,
                    )
                    
                    for future in done:
                        if not future.result():
                            success = False
        
        finally:
            try:
                del self._sync_tasks[guild_id]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(guild_id)
            self._sync_done.add(guild_id)
        
        return success
    
    
    async def _sync_global_task(self, client):
        """
        Syncs the global commands off the ``Slasher``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the commands where synced with success.
        """
        success = False
        try:
            application_commands = await client.application_command_global_get_all()
        except GeneratorExit:
            raise
        
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_global_commands', err)
            
        else:
            global_command_state = self._command_states.get(SYNC_ID_GLOBAL, None)
            if global_command_state is None:
                global_added_commands = None
                global_keep_commands = None
                global_removed_commands = None
            
            else:
                global_added_commands = global_command_state.get_should_add_application_commands()
                if not global_added_commands:
                    global_added_commands = None
                
                global_keep_commands = global_command_state.get_should_keep_commands()
                if not global_keep_commands:
                    global_keep_commands = None
                
                global_removed_commands = global_command_state.get_should_remove_application_commands()
                if not global_removed_commands:
                    global_removed_commands = None
            
            command_create_callbacks = None
            command_edit_callbacks = None
            command_delete_callbacks = None
            command_register_callbacks = None
            
            global_added_commands, matched = match_application_commands_to_commands(
                application_commands, global_added_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._sync_permissions_then_register, self, client, command, global_command_state,
                        SYNC_ID_GLOBAL, application_command
                    )
                    
                    if command_register_callbacks is None:
                        command_register_callbacks = []
                    command_register_callbacks.append(callback)
            
            global_keep_commands, matched = match_application_commands_to_commands(
                application_commands, global_keep_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    self._keep_helper(command, global_command_state, SYNC_ID_GLOBAL)
            
            global_removed_commands, matched = match_application_commands_to_commands(
                application_commands, global_removed_commands, True
            )
            if (matched is not None):
                for application_command, command in matched:
                    callback = (
                        type(self)._delete_command, self, client, command, global_command_state, SYNC_ID_GLOBAL,
                        application_command
                    )
                    if command_delete_callbacks is None:
                        command_delete_callbacks = []
                    command_delete_callbacks.append(callback)
            
            if (global_added_commands is not None):
                while global_added_commands:
                    command = global_added_commands.pop()
                    
                    callback = (type(self)._create_command, self, client, command, global_command_state, SYNC_ID_GLOBAL)
                    if command_create_callbacks is None:
                        command_create_callbacks = []
                    command_create_callbacks.append(callback)
            
            while application_commands:
                application_command = application_commands.pop()
                
                callback = (type(self)._delete_command, self, client, None, None, SYNC_ID_GLOBAL, application_command)
                if command_delete_callbacks is None:
                    command_delete_callbacks = []
                command_delete_callbacks.append(callback)
            
            success = True
            for callbacks in (command_register_callbacks, command_delete_callbacks, command_edit_callbacks,
                    command_create_callbacks):
                if (callbacks is not None):
                    done, pending = await WaitTillAll(
                        [Task(callback[0](*callback[1:]), KOKORO) for callback in callbacks],
                        KOKORO,
                    )
                    
                    for future in done:
                        if not future.result():
                            success = False
        
        finally:
            try:
                del self._sync_tasks[SYNC_ID_GLOBAL]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(SYNC_ID_GLOBAL)
            self._sync_done.add(SYNC_ID_GLOBAL)
        
        return success
    
    
    async def _sync_permissions_then_register(self, client, command, command_state, guild_id, application_command):
        """
        Syncs the command's permissions, then registers it.
        
        This method is a coroutine.
        
        Attributes
        ----------
        client : ``Client``
            The respective client.
        command : ``CommandBaseApplicationCommand``
            The command to sync it's permissions of and register.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was registered successfully.
        """
        success = await self._sync_permissions(client, command, guild_id, application_command)
        if not success:
            return False
        
        self._register_helper(command, command_state, guild_id, application_command.id)
        return True
    
    
    async def _sync_permissions(self, client, command, guild_id, application_command):
        """
        Syncs the command's permissions.
        
        This method is a coroutine.
        
        Attributes
        ----------
        client : ``Client``
            The respective client.
        command : ``CommandBaseApplicationCommand``
            The command to sync it's permissions of.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command's permissions were synced successfully.
        """
        assert_application_command_permission_missmatch_at = self._assert_application_command_permission_missmatch_at
        if (assert_application_command_permission_missmatch_at is None):
            return True
        
        if guild_id == SYNC_ID_GLOBAL:
            tasks = []
            for permission_guild_id in command._get_permission_sync_ids():
                if permission_guild_id not in assert_application_command_permission_missmatch_at:
                    continue
                
                task = Task(
                    self._sync_permissions_task(client, permission_guild_id, command, application_command),
                    KOKORO,
                )
                tasks.append(task)
            
            if tasks:
                await WaitTillAll(tasks, KOKORO)
                
                success = True
                for future in tasks:
                    if not future.result():
                        success = False
                
                if not success:
                    return False
            
            return True
        
        if guild_id not in assert_application_command_permission_missmatch_at:
            return True
        
        return await self._sync_permissions_task(client, guild_id, command, application_command)
    
    
    async def _sync_permissions_task(self, client, guild_id, command, application_command):
        """
        Syncs a command's permissions inside of a guild.
        
        `command` and `application_command` parameters might be given as `None`. At that case guild level
        permission overwrite matching is performed.
        
        This method is a coroutine.
        
        Attributes
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        command : `None`, ``CommandBaseApplicationCommand``
            The command to sync it's permissions of.
        application_command : `None`, ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command's permissions were synced successfully.
        """
        if application_command is None:
            application_command_id = 0
        else:
            application_command_id = application_command.id
        
        
        success, permission = await self._get_permission_for(client, guild_id, application_command_id)
        if not success:
            return False
        
        if command is None:
            expected_permission_overwrites = self._get_permission_overwrites_for_guild(guild_id)
        else:
            expected_permission_overwrites = command.get_permission_overwrites_for(guild_id)
        
        if permission is None:
            current_permission_overwrites = None
        else:
            current_permission_overwrites = permission.permission_overwrites
        
        if are_application_command_permission_overwrites_equal(
            guild_id, expected_permission_overwrites, current_permission_overwrites
        ):
            return True
        
        if self._enforce_application_command_permissions:
            access = await self._get_owners_access(client)
            
            if (access is not None):
                try:
                    permission = await client.application_command_permission_edit(
                        access,
                        guild_id,
                        application_command,
                        expected_permission_overwrites,
                    )
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    if not isinstance(err, ConnectionError):
                        await client.events.error(
                            client,
                            f'{self!r}._sync_permissions_task',
                            SlasherSyncError(command, err),
                        )
                    return False
                
                try:
                    per_guild = self._synced_permissions[guild_id]
                except KeyError:
                    per_guild = self._synced_permissions[guild_id] = {}
                
                per_guild[permission.application_command_id] = permission
                
                warn = False
                success = True
            
            else:
                warn = True
                success = False
        else:
            warn = True
            success = True
        
        if warn:
            warnings.warn(
                create_permission_mismatch_message(
                    application_command,
                    guild_id,
                    current_permission_overwrites,
                    expected_permission_overwrites,
                ),
                PermissionMismatchWarning,
            )
        
        return success
    
    
    async def _edit_guild_command_to_non_global(self, client, command, command_state, guild_id, application_command):
        """
        Edits the given guild command to a non local one.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : ``CommandBaseApplicationCommand``
            The non_global command what replaced the application command.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            await client.application_command_guild_edit(
                guild_id,
                application_command,
                command.get_schema(),
            )
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return False
            
            if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_application_command):
                # no command, no problem, lol
                return True
            
            await client.events.error(
                client,
                f'{self!r}._edit_guild_command_to_non_global',
                SlasherSyncError(command, err),
            )
            return False
        
        success = await self._sync_permissions(client, command, guild_id, application_command)
        if not success:
            return False
        
        self._register_helper(command, command_state, guild_id, application_command.id)
        return True
    
    
    async def _edit_command(self, client, command, command_state, guild_id, application_command):
        """
        Updates the given guild bound application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : ``CommandBaseApplicationCommand``
            The application command to update the application command to.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            schema = command.get_schema()
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_edit(application_command, schema)
            else:
                coroutine = client.application_command_guild_edit(guild_id, application_command, schema)
            await coroutine
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                self._unregister_helper(command, command_state, guild_id)
                return await self._create_command(client, command, command_state, guild_id)
            
            await client.events.error(
                client,
                f'{self!r}._edit_command',
                SlasherSyncError(command, err),
            )
            return False
        
        success = await self._sync_permissions(client, command, guild_id, application_command)
        if not success:
            return False
        
        self._register_helper(command, command_state, guild_id, application_command.id)
        return True
    
    
    async def _delete_command(self, client, command, command_state, guild_id, application_command):
        """
        Deletes the given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : `None`, ``CommandBaseApplicationCommand``
            The application command to delete.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was deleted successfully.
        """
        try:
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_delete(application_command)
            else:
                coroutine = client.application_command_guild_delete(guild_id, application_command)
            await coroutine
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, ok, I guess.
                pass
            else:
                await client.events.error(
                    client,
                    f'{self!r}._delete_command',
                    SlasherSyncError(command, err),
                )
                return False
        
        self._unregister_helper(command, command_state, guild_id)
        return True
    
    
    async def _create_command(self, client, command, command_state, guild_id):
        """
        Creates a given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : `None`, ``CommandBaseApplicationCommand``
            The application command to create.
        command_state : ``CommandState``
            The command's command state.
        guild_id : `int`
            The respective guild's identifier where the command is.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            schema = command.get_schema()
            if guild_id == SYNC_ID_GLOBAL:
                coroutine = client.application_command_global_create(schema)
            else:
                coroutine = client.application_command_guild_create(guild_id, schema)
            application_command = await coroutine
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(
                client,
                f'{self!r}._create_command',
                SlasherSyncError(command, err),
            )
            return False
        
        
        success = await self._sync_permissions(client, command, guild_id, application_command)
        if not success:
            return False
        
        self._register_helper(command, command_state, guild_id, application_command.id)
        return True
    
    
    def sync(self):
        """
        Syncs the application commands with the client.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `bool`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if syncing was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                ``FutureAsyncWrapper``. The task will return `True`, if syncing was successful.
            - If the method was called from any other thread, then waits for the syncing task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            The slasher's client was already garbage collected.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError('The slasher\'s client was already garbage collected.')
        
        return run_coroutine(self._do_main_sync(client), KOKORO)
    
    
    async def _do_main_sync(self, client):
        """
        Syncs the application commands with the client. This method is the internal method of ``.sync``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the sync was successful.
        """
        if not self._sync_should:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_MAIN]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_MAIN] = Task(self._do_main_sync_task(client), KOKORO)
        
        return await task
    
    
    async def _do_main_sync_task(self, client):
        """
        Syncs the application commands with the client. This method is the internal coroutine of the ``._do_main_sync``
        method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the sync was successful.
        """
        try:
            while True:
                try:
                    tasks = []
                    for guild_id in self._sync_should:
                        if guild_id == SYNC_ID_GLOBAL:
                            coroutine = self._sync_global(client)
                        else:
                            coroutine = self._sync_guild(client, guild_id)
                        
                        task = Task(coroutine, KOKORO)
                        tasks.append(task)
                    
                    if tasks:
                        done, pending = await WaitTillAll(tasks, KOKORO)
                        
                        success = True
                        for future in done:
                            if not future.result():
                                success = False
                    else:
                        success = True
                except:
                    self._late_register()
                    raise
                
                else:
                    if self._late_register(): # Make sure this is called
                        if success:
                            continue
                    
                    return success
        
        finally:
            try:
                del self._sync_tasks[SYNC_ID_MAIN]
            except KeyError:
                pass
    
    
    def discard_kept_commands(self):
        """
        Discards the kept application commands out. If needed, triggers syncing.
        
        Returns
        -------
        task : `bool`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if syncing was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                ``FutureAsyncWrapper``. The task will return `True`, if syncing was successful.
            - If the method was called from any other thread, then waits for the syncing task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            The slasher's client was already garbage collected.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError('The slasher\'s client was already garbage collected.')
        
        return run_coroutine(self._do_discard_kept_commands(client), KOKORO)
    
    
    def _discard_kept_commands_and_update_sync_states(self):
        """
        Discards all kept commands and updates sync states.
        
        After calling this method syncing should be triggered. If any sync state was updated, it will trigger the sync
        task.
        """
        command_unloading_behaviour = self._command_unloading_behaviour
        if command_unloading_behaviour != UNLOADING_BEHAVIOUR_KEEP:
            return
        
        self._command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        
        for command_state in self._command_states.values():
            for command in command_state.exhaust_kept_commands():
                for sync_id in command._iter_sync_ids():
                    self._sync_should.add(sync_id)
                    self._sync_done.discard(sync_id)
        
        self._command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
    
    
    async def _do_discard_kept_commands(self, client):
        """
        Discards the kept application commands out. If needed, triggers syncing. This method is the internal method of
        ``.discard_kept_commands``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the sync was successful.
        """
        self._discard_kept_commands_and_update_sync_states()
        return await self._do_main_sync(client)
        
    
    def _maybe_register_guild_command(self, application_command, guild_id):
        """
        Tries to register the given non-global application command to the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just added application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        try:
            non_global_command_state = self._command_states[SYNC_ID_NON_GLOBAL]
        except KeyError:
            return
        
        for command in non_global_command_state.get_should_add_application_commands():
            if command.get_schema() == application_command:
                self._register_helper(command, non_global_command_state, guild_id, application_command.id)
                break
    
    def _maybe_unregister_guild_command(self, application_command, guild_id):
        """
        Tries to unregister the given non-global application command from the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just deleted application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        try:
            non_global_command_state = self._command_states[SYNC_ID_NON_GLOBAL]
        except KeyError:
            return
        
        for command in non_global_command_state.get_should_add_application_commands():
            if command.get_schema() == application_command:
                self._unregister_helper(command, non_global_command_state, guild_id)
                break
    
    def __repr__(self):
        """Returns the slasher's representation."""
        return f'<{self.__class__.__name__} sync_should={len(self._sync_should)}, sync_done={len(self._sync_done)}>'
    
    @property
    def delete_commands_on_unload(self):
        """
        A get-set property for changing the slasher's command unloading behaviour.
        
        Accepts and returns any `bool`.
        """
        command_unloading_behaviour = self._command_unloading_behaviour
        if command_unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
            delete_commands_on_unload = True
        else:
            delete_commands_on_unload = False
        
        return delete_commands_on_unload
    
    
    @delete_commands_on_unload.setter
    def delete_commands_on_unload(self, delete_commands_on_unload):
        if type(delete_commands_on_unload) is bool:
            pass
        elif isinstance(delete_commands_on_unload, bool):
            delete_commands_on_unload = bool(delete_commands_on_unload)
        else:
            raise TypeError(
                f'`delete_commands_on_unload` can be `bool`, got '
                f'{delete_commands_on_unload.__class__.__name__}; {delete_commands_on_unload!r}.'
            )
        
        if delete_commands_on_unload:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            command_unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        self._command_unloading_behaviour = command_unloading_behaviour
    
    
    def _maybe_store_application_command_permission(self, permission):
        """
        Stores an application command's new permissions if needed.
        
        Parameters
        ----------
        permission : ``ApplicationCommandPermission``
            The updated application command's permissions.
        """
        try:
            tracked_guild = self._synced_permissions[permission.guild_id]
        except KeyError:
            return
        
        tracked_guild[permission.application_command_id] = permission
    
    
    async def _get_permission_for(self, client, guild_id, application_command_id):
        """
        Gets the permissions for the given application command in the the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        guild_id : `int`
            The respective guild's identifier where the command is.
        
        application_command_id : `int`
            The respective application command's identifier.
            
            If passed as `None` will return the guild level permission overwrites instead.
        """
        try:
            per_guild = self._synced_permissions[guild_id]
        except KeyError:
            pass
        else:
            return True, per_guild.get(application_command_id, None)
        
        try:
            sync_permission_task = self._get_permission_tasks[guild_id]
        except KeyError:
            sync_permission_task = Task(self._get_permission_task(client, guild_id), KOKORO)
            self._get_permission_tasks[guild_id] = sync_permission_task
        
        success, per_guild = await sync_permission_task
        if success:
            permission = per_guild.get(application_command_id, None)
        else:
            permission = None
        
        return success, permission
    
    
    async def _get_permission_task(self, client, guild_id):
        """
        Syncs the respective guild's permissions.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        per_guild : `None`, `dict` of (`int`, ``ApplicationCommandPermission``) items
            The application command permission for the respective guild. If `success` is `False, this value is
            returned as `None`.
        """
        try:
            try:
                permissions = await client.application_command_permission_get_all_guild(guild_id)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                if not isinstance(err, ConnectionError):
                    await client.events.error(client, f'{self!r}._get_permission_task', err)
                
                return False, None
            else:
                try:
                    per_guild = self._synced_permissions[guild_id]
                except KeyError:
                    per_guild = self._synced_permissions[guild_id] = {}
                
                for permission in permissions:
                    application_command_id = permission.application_command_id
                    if application_command_id == client.application.id:
                        application_command_id = 0
                    
                    per_guild[application_command_id] = permission
                
                return True, per_guild
        
        finally:
            try:
                del self._get_permission_tasks[guild_id]
            except KeyError:
                pass
    
    
    def _maybe_sync(self):
        """
        Syncs the slasher runtime if required.
        """
        client = self._client_reference()
        if client is None:
            raise RuntimeError('The slasher\'s client was already garbage collected.')
        
        for sync_hook in RUNTIME_SYNC_HOOKS:
            if not sync_hook(client):
                return
        
        Task(self._do_main_sync(client), KOKORO)
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``Slasher``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `None`, Optional
            Exception handler to register.
        first : `bool` = `False`, Optional (Keyword Only)
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler / wrapper : `CoroutineFunction` / `functools.partial`
            If `exception_handler` is not given, returns a wrapper.
        """
        if exception_handler is None:
            return partial_func(_register_exception_handler, first)
        
        return self._register_exception_handler(exception_handler, first)
    
    
    def _register_exception_handler(self, exception_handler, first):
        """
        Registers an exception handler to the ``Slasher``.
        
        Parameters
        ----------
        exception_handler : `CoroutineFunction`
            Exception handler to register.
        first : `bool`
            Whether the exception handler should run first.
        
        Returns
        -------
        exception_handler : `CoroutineFunction`
        """
        test_exception_handler(exception_handler)
        
        exception_handlers = self._exception_handlers
        if exception_handlers is None:
            self._exception_handlers = exception_handlers = []
        
        if first:
            exception_handlers.insert(0, exception_handler)
        else:
            exception_handlers.append(exception_handler)
        
        return exception_handler
    
    
    def _add_component_command(self, component_command):
        """
        Adds a component command to the ``Slasher`` if applicable.
        
        Parameters
        ---------
        component_command : ``ComponentCommand``
            The command to add.
        
        Raises
        ------
        RuntimeError
            If the command would only partially overwrite an other commands.
        """
        self._add_custom_id_based_command(component_command, self._component_commands,
            self._string_custom_id_to_component_command, self._regex_custom_id_to_component_command)
    
    
    def _add_form_submit_command(self, form_submit_command):
        """
        Adds a form submit command to the ``Slasher`` if applicable.
        
        Parameters
        ---------
        form_submit_command : ``FormSubmitCommand``
            The command to add.
        
        Raises
        ------
        RuntimeError
            If the command would only partially overwrite an other commands.
        """
        self._add_custom_id_based_command(form_submit_command, self._form_submit_commands,
            self._string_custom_id_to_form_submit_command, self._regex_custom_id_to_form_submit_command)
    
    
    def _add_custom_id_based_command(self, custom_id_based_command, custom_id_based_commands,
            string_custom_id_to_custom_id_based_command, regex_custom_id_to_custom_id_based_command):
        """
        Adds a custom id based command to the ``Slasher`` if applicable.
        
        Parameters
        ---------
        custom_id_based_command : ``CommandBaseCustomId``
            The command to add.
        custom_id_based_commands : `set` of ``CommandBaseCustomId``
            A set of all the added commands.
        string_custom_id_to_custom_id_based_command : `dict` of (`str`, ``CommandBaseCustomId``) items
            A dictionary which contains commands by their `custom_id`.
        regex_custom_id_to_custom_id_based_command : ``dict` of (``RegexMatcher``, ``CommandBaseCustomId``) items
            A dictionary which contains commands based on regex patterns.
        
        Raises
        ------
        RuntimeError
            If the command would only partially overwrite an other commands.
        """
        custom_id_based_command._parent_reference = self._get_self_reference()
        
        overwrite_commands = None
        
        string_custom_ids = custom_id_based_command._string_custom_ids
        if (string_custom_ids is not None):
            for string_custom_id in string_custom_ids:
                try:
                    maybe_overwrite_command = string_custom_id_to_custom_id_based_command[string_custom_id]
                except KeyError:
                    continue
                
                if overwrite_commands is None:
                    overwrite_commands = set()
                
                overwrite_commands.add(maybe_overwrite_command)
                continue
        
        regex_custom_ids = custom_id_based_command._regex_custom_ids
        if (regex_custom_ids is not None):
            for regex_custom_id in regex_custom_ids:
                try:
                    maybe_overwrite_command = regex_custom_id_to_custom_id_based_command[regex_custom_id]
                except KeyError:
                    continue
                
                if overwrite_commands is None:
                    overwrite_commands = set()
                
                overwrite_commands.add(maybe_overwrite_command)
                continue
        
        if (overwrite_commands is not None):
            would_overwrite_custom_ids = set()
            for overwrite_command in overwrite_commands:
                overwrite_string_custom_ids = overwrite_command._string_custom_ids
                if (overwrite_string_custom_ids is not None):
                    would_overwrite_custom_ids.update(overwrite_string_custom_ids)
            
                overwrite_regex_custom_ids = overwrite_command._regex_custom_ids
                if (overwrite_regex_custom_ids is not None):
                    would_overwrite_custom_ids.update(overwrite_regex_custom_ids)
            
            custom_id_based_command_string_custom_ids = custom_id_based_command._string_custom_ids
            if (
                (custom_id_based_command_string_custom_ids is not None) and
                (not would_overwrite_custom_ids.issuperset(custom_id_based_command_string_custom_ids))
            ):
                raise RuntimeError(
                    f'Command: {custom_id_based_command!r} would only partially overwrite the following '
                    f'commands: {", ".join(repr(overwrite_command) for overwrite_command in overwrite_commands)}.'
                )
            
            for overwrite_command in overwrite_commands:
                custom_id_based_commands.discard(overwrite_command)
        
        string_custom_ids = custom_id_based_command._string_custom_ids
        if (string_custom_ids is not None):
            for string_custom_id in string_custom_ids:
                string_custom_id_to_custom_id_based_command[string_custom_id] = custom_id_based_command
        
        regex_custom_ids = custom_id_based_command._regex_custom_ids
        if (regex_custom_ids is not None):
            for regex_custom_id in regex_custom_ids:
                regex_custom_id_to_custom_id_based_command[regex_custom_id] = custom_id_based_command
        
        custom_id_based_commands.add(custom_id_based_command)
    
    
    def _remove_component_command(self, component_command):
        """
        Removes the given component command from the slasher.
        
        Parameters
        ----------
        component_command : ``ComponentCommand``
            The command to remove.
        """
        self._remove_custom_id_based_command(
            component_command, self._component_commands, self._string_custom_id_to_component_command,
            self._regex_custom_id_to_component_command
        )
    
    
    def _remove_form_submit_command(self, form_submit_command):
        """
        Removes the given form submit command from the ``Slasher`` if applicable.
        
        Parameters
        ---------
        form_submit_command : ``FormSubmitCommand``
            The command to remove.
        """
        self._add_custom_id_based_command(
            form_submit_command, self._form_submit_commands, self._string_custom_id_to_form_submit_command,
            self._regex_custom_id_to_form_submit_command
        )
    
    
    def _remove_custom_id_based_command(
        self, custom_id_based_command, custom_id_based_commands,
        string_custom_id_to_custom_id_based_command, regex_custom_id_to_custom_id_based_command
    ):
        """
        Removes a custom id based command from the ``Slasher`` if applicable.
        
        Parameters
        ---------
        custom_id_based_command : ``CommandBaseCustomId``
            The command to remove.
        custom_id_based_commands : `set` of ``CommandBaseCustomId``
            A set of all the added commands.
        string_custom_id_to_custom_id_based_command : `dict` of (`str`, ``CommandBaseCustomId``) items
            A dictionary which contains commands by their `custom_id`.
        regex_custom_id_to_custom_id_based_command : ``dict` of (``RegexMatcher``, ``CommandBaseCustomId``) items
            A dictionary which contains commands based on regex patterns.
        """
        try:
            custom_id_based_commands.remove(custom_id_based_command)
        except KeyError:
            pass
        else:
            string_custom_ids = custom_id_based_command._string_custom_ids
            if (string_custom_ids is not None):
                for string_custom_id in string_custom_ids:
                    if string_custom_id_to_custom_id_based_command[string_custom_id] is custom_id_based_command:
                        del string_custom_id_to_custom_id_based_command[string_custom_id]
            
            
            regex_custom_ids = custom_id_based_command._regex_custom_ids
            if (regex_custom_ids is not None):
                for regex_custom_id in regex_custom_ids:
                    if regex_custom_id_to_custom_id_based_command[regex_custom_id] is custom_id_based_command:
                        del regex_custom_id_to_custom_id_based_command[regex_custom_id]
    
    
    def get_global_command_count(self):
        """
        Gets the global command count of the slasher.
        
        Returns
        -------
        global_command_count : `int`
        """
        return self._get_command_count(SYNC_ID_GLOBAL)
    
    
    def get_global_command_count_with_sub_commands(self):
        """
        Returns the global command count including sub commands.
        
        Returns
        ------
        global_command_count_with_sub_commands : `int`
        """
        return self._get_command_count_with_sub_commands(SYNC_ID_GLOBAL)
    
    
    def get_guild_command_count(self, guild):
        """
        Gets the command count of the slasher for the specified guild.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to gets command count of.
        
        Returns
        -------
        guild_command_count : `int`
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild``, nor `int`.
        """
        guild_id = get_guild_id(guild)
        return self._get_command_count(guild_id)
    
    
    def get_guild_command_count_with_sub_commands(self, guild):
        """
        Returns the command count including sub commands for the specified guild.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to gets command count of.
        
        Returns
        ------
        guild_command_count_with_sub_commands : `int`
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild``, nor `int`.
        """
        guild_id = get_guild_id(guild)
        return self._get_command_count_with_sub_commands(guild_id)
    
    
    def _get_command_count(self, sync_id):
        """
        Gets command count for the specified sync-id.
        
        Parameters
        ----------
        sync_id : `int`
            Sync id to get commands of.
        
        Returns
        -------
        command_count : `int`
        """
        try:
            command_state = self._command_states[sync_id]
        except KeyError:
            command_count = 0
        else:
            command_count = command_state.get_active_command_count()
        
        return command_count
    
    
    def _get_command_count_with_sub_commands(self, sync_id):
        """
        Gets command count including sub commands for the specified sync-id.
        
        Parameters
        ----------
        sync_id : `int`
            Sync id to get commands of.
        
        Returns
        -------
        command_count_with_sub_commands : `int`
        """
        try:
            command_state = self._command_states[sync_id]
        except KeyError:
            command_count_with_sub_commands = 0
        else:
            command_count_with_sub_commands = command_state.get_active_command_count_with_sub_commands()
        
        return command_count_with_sub_commands
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``Slasher``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``Slasher``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference


    def autocomplete(self, parameter_name, *parameter_names, function=None):
        """
        Registers an auto completer function to the slasher.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `async-callable` = `None`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `async-callable`, `functools.partial`
            The registered function if given or a wrapper to register the function with.
        
        Raises
        ------
        RuntimeError
            - If the parameter already has a auto completer defined.
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            If `function` is not an asynchronous.
        """
        parameter_names = _build_auto_complete_parameter_names(parameter_name, parameter_names)
        
        if (function is None):
            return partial_func(_register_auto_complete_function, self, parameter_names)
            
        return self._add_autocomplete_function(parameter_names, function)
    
    
    def _add_autocomplete_function(self, parameter_names, function):
        """
        Registers an autocomplete function.
        
        Parameters
        ----------
        parameter_names : `list` of `str`
            The parameters' names.
        function : `async-callable`
            The function to register as auto completer.
        
        Returns
        -------
        function : `async-callable`
            The registered function.
        
        Raises
        ------
        RuntimeError
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            If `function` is not an asynchronous.
        """
        if isinstance(function, SlashCommandParameterAutoCompleter):
            function = function._command
        
        auto_completer = SlashCommandParameterAutoCompleter(
            function,
            parameter_names,
            APPLICATION_COMMAND_HANDLER_DEEPNESS,
            self,
        )
        
        auto_completers = self._auto_completers
        if (auto_completers is None):
            auto_completers = []
            self._auto_completers = auto_completers
        
        auto_completers.append(auto_completer)
        
        for command_state in self._command_states.values():
            active = command_state._active
            if (active is not None):
                for slasher_application_command in active:
                    slasher_application_command._try_resolve_auto_completer(auto_completer)
            
            
            changes = command_state._changes
            if (changes is not None):
                for command_change in changes:
                    if command_change.added:
                        command_change.command._try_resolve_auto_completer(auto_completer)
        
        return auto_completer
    
    
    def _schema_reset(self, command):
        """
        Called when an application command's schema is reset.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
        """
        for sync_id in command._iter_sync_ids():
            self._sync_done.discard(sync_id)
            self._sync_should.add(sync_id)
        
        self._maybe_sync()
    
    
    async def _get_owners_access(self, client):
        """
        Tries to request the client's oauth2 access.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        owners_access : `None`, ``Oauth2Access``
        """
        owners_access = self._owners_access
        if (owners_access is None):
            if self._owners_access_get_impossible:
                return None
            
            if not check_and_warn_can_request_owners_access_of(client):
                self._owners_access_get_impossible = True
                return None
            
        else:
            if (owners_access.created_at + OWNERS_ACCESS_REQUEST_INTERVAL) >= datetime.utcnow():
                return owners_access
        
        
        task = self._owners_access_get_task 
        if (task is None):
            task = self._get_owners_access_task(client)
            
            self._owners_access_get_task = task
            
            try:
                owners_access = await task 
            finally:
                self._owners_access_get_task = None
            
            self._owners_access = owners_access
        
        else:
            owners_access = await task
        
        return owners_access
    
    
    async def _get_owners_access_task(self, client):
        """
        Requests the client's owner's access. This method is synchronised by ``._get_owners_access``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        owners_access : `None`, ``Oauth2Access``
        """
        try:
           owners_access = await client.owners_access('applications.commands.permissions.update')
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return None
            
            await client.events.error(
                client,
                f'{self!r}._get_owners_access_task',
                SlasherSyncError(None, err),
            )
            return None
        
        return owners_access
    
    
    def _get_permission_overwrites_for_guild(self, guild_id):
        """
        Gets the permission overwrites for the given guild id.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier, what's permission overwrites we want to get.
        
        Returns
        -------
        permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        """
        guild_level_permission_overwrites = self._guild_level_permission_overwrites
        if guild_level_permission_overwrites is None:
            permission_overwrites = None
        
        else:
            try:
                permission_overwrites = guild_level_permission_overwrites[guild_id]
            except KeyError:
                permission_overwrites = None
            else:
                permission_overwrites = sorted(permission_overwrites)
        
        return permission_overwrites
    
    
    def _add_permission_overwrites_for_guild(self, guild_id, application_command_permission_overwrite):
        """
        Adds a permission overwrite for the given guild.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's identifier.
        application_command_permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The application command permission overwrite to add.
        """
        guild_level_permission_overwrites = self._guild_level_permission_overwrites
        if guild_level_permission_overwrites is None:
            guild_level_permission_overwrites = {}
            self._guild_level_permission_overwrites = guild_level_permission_overwrites
        
        try:
            permission_overwrites = guild_level_permission_overwrites[guild_id]
        except KeyError:
            permission_overwrites = set()
            guild_level_permission_overwrites[guild_id] = permission_overwrites
        
        permission_overwrites.add(application_command_permission_overwrite)
        
        self._sync_should.add(guild_id)
        self._sync_done.discard(guild_id)
    
    
    def _remove_permission_overwrite_for_guild(self, guild_id, application_command_permission_overwrite):
        """
        Removes a permission overwrite for the given guild.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's identifier.
        application_command_permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The application command permission overwrite to remove.
        """
        guild_level_permission_overwrites = self._guild_level_permission_overwrites
        if guild_level_permission_overwrites is not None:
            try:
                permission_overwrites = guild_level_permission_overwrites[guild_id]
            except KeyError:
                pass
            else:
                try:
                    permission_overwrites.remove(application_command_permission_overwrite)
                except ValueError:
                    pass
                else:
                    if not permission_overwrites:
                        del guild_level_permission_overwrites[guild_id]
        
        self._sync_should.add(guild_id)
        self._sync_done.discard(guild_id)
