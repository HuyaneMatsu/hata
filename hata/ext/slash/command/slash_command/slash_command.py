__all__ = ('SlashCommand',)

from warnings import warn

from scarletio import copy_docs, export

from .....discord.application import ApplicationIntegrationType
from .....discord.application_command import ApplicationCommandTargetType, INTEGRATION_CONTEXT_TYPES_ALL
from .....discord.application_command.application_command.constants import (
    OPTIONS_MAX as APPLICATION_COMMAND_OPTIONS_MAX
)
from .....discord.events.handling_helpers import check_name
from .....discord.permission import Permission

from ...constants import (
    APPLICATION_COMMAND_CATEGORY_DEEPNESS_START, APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND,
    APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY
)
from ...converters import get_slash_command_parameter_converters
from ...exceptions import SlashCommandParameterConversionError, handle_command_exception
from ...interfaces.autocomplete import AutocompleteInterface
from ...interfaces.command import CommandInterface
from ...interfaces.nestable import NestableInterface
from ...interfaces.self_reference import SelfReferenceInterface
from ...response_modifier import ResponseModifier
from ...utils import (
    UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT, UNLOADING_BEHAVIOUR_KEEP, raw_name_to_display
)
from ...wrappers import CommandWrapper, get_parameter_configurers

from ..command_base_application_command import CommandBaseApplicationCommand
from ..command_base_application_command.helpers import (
    _maybe_exclude_dm_from_integration_context_types, _reset_application_command_schema, _validate_allow_in_dm,
    _validate_delete_on_unload, _validate_guild, _validate_integration_context_types, _validate_integration_types,
    _validate_is_global, _validate_name, _validate_nsfw, _validate_required_permissions
)

from .helpers import _generate_description_from, _validate_is_default
from .slash_command_category import SlashCommandCategory
from .slash_command_function import SlashCommandFunction
from .slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


@export
class SlashCommand(
    AutocompleteInterface, CommandInterface, NestableInterface, SelfReferenceInterface, CommandBaseApplicationCommand
):
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _auto_completers : `None | list<SlashCommandParameterAutoCompleter>`
        Auto completer functions.
    
    _command : `None | SlashCommandFunction`
        The command of the slash command.
    
    _exception_handlers : `None | list<CoroutineFunction>`
        Exception handlers added with ``.error`` to the interaction handler.
    
    _parent_reference : `None | WeakReferer<SelfReferenceInterface>`
        Reference to the slasher application command's parent.
    
    _permission_overwrites : `None | dict<int, list<ApplicationCommandPermissionOverwrite>>
        Permission overwrites applied to the slash command.
    
    _registered_application_command_ids : `None | dict<int, int>`
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    
    _schema : `None | ApplicationCommand`
        Internal slot used by the ``.get_schema`` method.
    
    _self_reference : `None | WeakReferer<instance>`
        Back reference to the slasher application command.
        
        Used by sub commands to access the parent entity.
    
    _sub_commands : `None | dict<str, SlashCommandFunction | SlashCommandCategory>`
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    
    _unloading_behaviour : `int`
        Behaviour what describes what should happen when the command is removed from the slasher.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_INHERIT   | 2     |
        +-------------------------------+-------+
    
    default : `bool`
        Whether the command is the default command in it's category.
    
    description : `str`
        Application command description. It's length can be in range [2:100].
    
    global_ : `bool`
        Whether the command is a global command.
        
        Global commands have their ``.guild_ids`` set as `None`.
    
    guild_ids : `None | set<int>`
        The ``Guild``'s id to which the command is bound to.
    
    integration_context_types : `None | tuple<ApplicationCommandIntegrationContextType>`
        The places where the application command shows up.
    
    integration_types : `None | tuple<ApplicationIntegrationType>`
        The options where the application command can be integrated to.
    
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    nsfw : `None | bool`
        Whether the application command is only allowed in nsfw channels.
    
    required_permissions : ``Permission``
        The required permissions to use the application command inside of a guild.
    
    Notes
    -----
    Slash commands are weakreferable.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_command', '_self_reference', '_sub_commands', 'default', 'description'
    )
    
    
    def __new__(
        cls,
        function,
        name = None,
        *,
        allow_in_dm = ...,
        delete_on_unload = ...,
        description = ...,
        guild = ...,
        integration_context_types = ...,
        integration_types = ...,
        is_default = ...,
        is_global = ...,
        nsfw = ...,
        required_permissions = ...,
        **keyword_parameters,
    ):
        """
        Creates a new ``SlashCommand`` with the given parameters.
        
        Parameters
        ----------
        function : `None | async-callable`
            The function used as the command when using the respective slash command.
        
        name : `None | str` = `None`, Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        
        delete_on_unload : `bool`, Optional (Keyword only)
            Whether the command should be deleted from Discord when removed.
        
        description : `str | object`, Optional (Keyword only)
            Description to use instead of the function's docstring.
        
        guild : `int | Guild | (list | set)<int | Guild>`, Optional (Keyword only)
            To which guild(s) the command is bound to.
        
        integration_context_types : `None | ApplicationCommandIntegrationContextType | int | str | \
                iterable<ApplicationCommandIntegrationContextType | int | str>`, Optional (Keyword only)
            The places where the application command shows up.
        
        integration_types : `None | ApplicationIntegrationType | int | str | \
                iterable<ApplicationIntegrationType | int | str>`, Optional
            The options where the application command can be integrated to.
        
        is_default : `bool`, Optional (Keyword only)
            Whether the context command is the default command in it's category.
        
        is_global : `None | bool` = `None`, Optional
            Whether the slash command is the default command in it's category.
        
        nsfw : `None`, Optional (Keyword only)
            Whether the application command is only allowed in nsfw channels.
        
        required_permissions : `int | Permission`, Optional (Keyword only)
            The required permissions to use the application command inside of a guild.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        allowed_mentions : `None | str, UserBase | Role | AllowedMentionProxy | list<str | UserBase | Role> \
                , Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        
        wait_for_acknowledgement : `bool`, Optional (Keyword only)
            Whether acknowledge tasks should be ensure asynchronously.
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if (function is not None) and isinstance(function, CommandWrapper):
            command_function, wrappers = function.fetch_function_and_wrappers_back()
        else:
            command_function = function
            wrappers = None
        
        # Pre validate
        name = _validate_name(name)
        
        # allow_in_dm
        if (allow_in_dm is not ...):
            warn(
                (
                    '`allow_in_dm` parameter is deprecated and will be removed in 2024 November. '
                    'Please use `integration_context_types` instead.'
                ),
                FutureWarning,
                stacklevel = 5,
            )
            
            allow_in_dm = _validate_allow_in_dm(allow_in_dm)
        
        # delete_on_unload
        if delete_on_unload is ...:
            unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
        elif _validate_delete_on_unload(delete_on_unload):
            unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        # description (no pre-validation)
        if description is ...:
            description = None
        
        # guild
        if guild is ...:
            guild_ids = None
        else:
            guild_ids = _validate_guild(guild)
        
        # integration_context_types
        if integration_context_types is ...:
            integration_context_types = INTEGRATION_CONTEXT_TYPES_ALL
        else:
            integration_context_types = _validate_integration_context_types(integration_context_types)
        
        # integration_types
        if integration_types is ...:
            integration_types = (ApplicationIntegrationType.guild_install,)
        else:
            integration_types = _validate_integration_types(integration_types)
        
        # is_default
        if is_default is ...:
            is_default = False
        else:
            is_default = _validate_is_default(is_default)
        
        # is_global
        if is_global is ...:
            is_global = False
        else:
            is_global = _validate_is_global(is_global)
        
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = _validate_nsfw(nsfw)
        
        # required_permissions
        if required_permissions is ...:
            required_permissions = Permission()
        else:
            required_permissions = _validate_required_permissions(required_permissions)
        
        # Check extra parameters
        response_modifier = ResponseModifier(keyword_parameters)
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        # Post validate
        name = check_name(command_function, name)
        name = raw_name_to_display(name)
        
        description = _generate_description_from(command_function, name, description)
        
        if command_function is None:
            parameter_converters = None
        else:
            parameter_configurers = get_parameter_configurers(wrappers)
            command_function, parameter_converters = get_slash_command_parameter_converters(command_function, parameter_configurers)
        
        if is_global and (guild_ids is not None):
            raise TypeError(
                f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                f'guild = {guild!r}.'
            )
        
        if (allow_in_dm is not ...):
            integration_context_types = _maybe_exclude_dm_from_integration_context_types(
                allow_in_dm, integration_context_types
            )
        
        if not is_global:
            integration_types = None
            integration_context_types = None
        
        if (command_function is None):
            slash_command_function = None
        else:
            slash_command_function = SlashCommandFunction(
                command_function, parameter_converters, name, description, response_modifier, is_default
            )
        
        # Construct
        self = object.__new__(cls)
        self._command = slash_command_function
        self._sub_commands = None
        self.description = description
        self.guild_ids = guild_ids
        self.global_ = is_global
        self.name = name
        self._schema = None
        self._registered_application_command_ids = None
        self.default = is_default
        self._unloading_behaviour = unloading_behaviour
        self.nsfw = nsfw
        self.required_permissions = required_permissions
        self._permission_overwrites = None
        self._auto_completers = None
        self._exception_handlers = None
        self._parent_reference = None
        self._self_reference = None
        self.integration_context_types = integration_context_types
        self.integration_types = integration_types
        
        if (slash_command_function is not None):
            slash_command_function._parent_reference = self.get_self_reference()
        
        if (wrappers is not None):
            for wrapper in wrappers:
                wrapper.apply(self)
        
        return self
    
    
    @copy_docs(CommandBaseApplicationCommand._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts = CommandBaseApplicationCommand._put_repr_parts_into(self, repr_parts)
        
        # default
        default = self.default
        if default:
            repr_parts.append(', default = ')
            repr_parts.append(repr(default))
        
        # description
        description = self.description
        if self.name != description:
             repr_parts.append(', description = ')
             repr_parts.append(repr(description))
        
        return repr_parts
    
    
    @copy_docs(CommandBaseApplicationCommand.__hash__)
    def __hash__(self):
        hash_value = CommandBaseApplicationCommand.__hash__(self)
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            hash_value ^= len(auto_completers) << 22
            
            for auto_completer in auto_completers:
                hash_value ^= hash(auto_completer)
        
        # _command
        command = self._command
        if (command is not None):
            hash_value ^= hash(command)
        
        # _sub_commands
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            hash_value ^= len(sub_commands) << 26
            
            for sub_command in sub_commands:
                hash_value ^= hash(sub_command)
        
        # default
        hash_value ^= self.default << 30
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        
        return hash_value
    
    
    @copy_docs(CommandBaseApplicationCommand._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not CommandBaseApplicationCommand._is_equal_same_type(self, other):
            return False
        
        # _auto_completers
        if self._auto_completers != other._auto_completers:
            return False
        
        # _command
        if self._command != other._command:
            return False
        
        # _self_reference
        # Internal field
        
        # _sub_commands
        if self._sub_commands != other._sub_commands:
            return False
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        return True
    
    
    @copy_docs(CommandBaseApplicationCommand.invoke)
    async def invoke(self, client, interaction_event):
        options = interaction_event.interaction.options
        
        command = self._command
        if (command is not None):
            await command.invoke(client, interaction_event, options)
            return
        
        sub_commands = self._sub_commands
        if (sub_commands is None):
            return
        
        if (options is None) or (len(options) != 1):
            return
        
        option = options[0]
        
        try:
            sub_command = sub_commands[option.name]
        except KeyError:
            pass
        else:
            await sub_command.invoke(client, interaction_event, option.options)
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            SlashCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                [*sub_commands.keys()],
            )
        )
        return
    
    
    @copy_docs(CommandBaseApplicationCommand.copy)
    def copy(self):
        new = CommandBaseApplicationCommand.copy(self)
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        # _command
        command = self._command
        if (command is not None):
            command = command.copy()
        new._command = command
        
        # _self_reference
        new._self_reference = None
        
        # _sub_commands
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            sub_commands = {name: category.copy() for name, category in sub_commands.items()}
        new._sub_commands = sub_commands
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # ---- POST LINKING ----
        
        if (sub_commands is not None):
            for sub_command in sub_commands.values():
                sub_command._parent_reference = new.get_self_reference()
        
        return new
    
    
    @CommandBaseApplicationCommand.target.getter
    def target(self):
        return ApplicationCommandTargetType.chat

    
    @copy_docs(CommandInterface.get_command_function)
    def get_command_function(self):
        slash_command_function = self._command
        if (slash_command_function is not None):
            return slash_command_function.get_command_function()
    
    
    async def invoke_auto_completion(self, client, interaction_event, auto_complete_option):
        """
        Calls the respective auto completion function of the command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        
        interaction_event : ``InteractionEvent``
            The received interaction event.
        
        auto_complete_option : `InteractionMetadataApplicationCommandAutocomplete | InteractionOption`
            The option to autocomplete.
        """
        command_function = self._command
        if (command_function is not None):
            await command_function.invoke_auto_completion(client, interaction_event, auto_complete_option)
            return
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            auto_complete_option = auto_complete_option.options[0]
            
            auto_complete_option_type = auto_complete_option.type
            if (
                (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND) or
                (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY)
            ):
                options = auto_complete_option.options
                if (options is not None):
                    try:
                        sub_command = sub_commands[auto_complete_option.name]
                    except KeyError:
                        pass
                    else:
                        await sub_command.invoke_auto_completion(client, interaction_event, auto_complete_option)
            
            return
        
        # no more cases
    
    @copy_docs(CommandBaseApplicationCommand._get_schema_options)
    def _get_schema_options(self):
        while True:
            command = self._command
            if (command is not None):
                parameter_converters = command._parameter_converters
                
                options = None
                for parameter_converter in parameter_converters:
                    option = parameter_converter.as_option()
                    if (option is not None):
                        if (options is None):
                            options = []
                        
                        options.append(option)
                break
            
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                options = [sub_command.as_option() for name, sub_command in sorted(sub_commands.items())]
                break
            
            options = None
            break
        
        return options
    
    
    def as_sub_command(self, deepness):
        """
        Returns the slash command as a sub-command or sub-category.
        
        Parameters
        ----------
        deepness : `int`
            How nested the category or function will be.
        
        Returns
        -------
        new : `SlashCommandFunction | SlashCommandCategory`
        """
        command = self._command
        if (command is not None):
            return command
        
        return SlashCommandCategory(self.name, self.description, self.default, deepness)
    
    
    @copy_docs(NestableInterface._is_nestable)
    def _is_nestable(self):
        return True if self.get_command_function() is None else False
    
    
    @copy_docs(NestableInterface._make_command_instance_from_parameters)
    def _make_command_instance_from_parameters(self, function, positional_parameters, keyword_parameters):
        return type(self)(function, *positional_parameters, **keyword_parameters)
    
    
    @copy_docs(NestableInterface._store_command_instance)
    def _store_command_instance(self, command):
        if isinstance(command, type(self)):
            instance = self._add_application_command(command)
            return True, instance
        
        return False, None
        
    
    def _add_application_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if (
            (sub_commands is not None) and
            (len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX) and
            (command.name not in sub_commands)
        ):
            raise RuntimeError(
                f'The {self!r} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).'
            )
        
        if (sub_commands is not None) and command.default:
            for sub_command in sub_commands.values():
                if sub_command.default and (sub_command.name != command.name):
                    raise RuntimeError(
                        f'{self!r} already has a default command.'
                    )
        
        as_sub_command = command.as_sub_command(APPLICATION_COMMAND_CATEGORY_DEEPNESS_START)
        as_sub_command._parent_reference = self.get_self_reference()
        
        if sub_commands is None:
            sub_commands = {}
            self._sub_commands = sub_commands
        
        sub_commands[as_sub_command.name] = as_sub_command
        _reset_application_command_schema(self)
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            for auto_completer in auto_completers:
                as_sub_command._try_resolve_auto_completer(auto_completer)
        
        return as_sub_command
    
    
    @copy_docs(CommandBaseApplicationCommand.get_real_command_count)
    def get_real_command_count(self):
        while True:
            if (self._command is not None):
                real_command_count = 1
                break
            
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                real_command_count = 0
                
                for sub_command_or_category in sub_commands.values():
                    if isinstance(sub_command_or_category, SlashCommandFunction):
                        real_command_count += 1
                        continue
                    
                    # Nesting more is not allowed by Discord.
                    sub_commands = sub_command_or_category._sub_commands
                    if (sub_commands is not None):
                        real_command_count += len(sub_commands)
                break
            
            real_command_count = 0
            break
        
        return real_command_count
    
    
    @copy_docs(AutocompleteInterface._register_auto_completer)
    def _register_auto_completer(self, function, parameter_names):
        while True:
            slash_command_function = self._command
            if (slash_command_function is not None):
                auto_completer = slash_command_function._register_auto_completer(function, parameter_names)
                break
                
            auto_completer = self._make_auto_completer(function, parameter_names)
            self._store_auto_completer(auto_completer)
            
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                for sub_command in sub_commands.values():
                    sub_command._try_resolve_auto_completer(auto_completer)
                break
            
            break
        
        _reset_application_command_schema(self)
        return auto_completer
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command.
        
        Parameters
        ----------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The auto completer.
        
        Returns
        -------
        resolved : `int`
            The amount of parameters resolved.
        """
        resolved = 0
        
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                for sub_command in sub_commands.values():
                    resolved += sub_command._try_resolve_auto_completer(auto_completer)
        else:
            resolved += command._try_resolve_auto_completer(auto_completer)
        
        if resolved:
            _reset_application_command_schema(self)
        
        return resolved
