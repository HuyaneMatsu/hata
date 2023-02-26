__all__ = ('SlashCommand',)

from functools import partial as partial_func

from scarletio import WeakReferer, copy_docs, export

from .....discord.application_command import ApplicationCommandTargetType
from .....discord.application_command.application_command.constants import APPLICATION_COMMAND_OPTIONS_MAX
from .....discord.events.handling_helpers import Router, _EventHandlerManager, check_name, route_name, route_value

from ...converters import get_slash_command_parameter_converters
from ...exceptions import SlashCommandParameterConversionError, handle_command_exception
from ...response_modifier import ResponseModifier
from ...utils import _check_maybe_route, raw_name_to_display
from ...wrappers import CommandWrapper, get_parameter_configurers

from ..command_base_application_command import CommandBaseApplicationCommand
from ..command_base_application_command.constants import (
    APPLICATION_COMMAND_CATEGORY_DEEPNESS_START, APPLICATION_COMMAND_DEEPNESS,
    APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND, APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY
)
from ..command_base_application_command.helpers import (
    _reset_application_command_schema, _validate_allow_in_dm, _validate_delete_on_unload,
    _validate_guild, _validate_is_global, _validate_name, _validate_nsfw, _validate_required_permissions
)


from .helpers import (
    _build_auto_complete_parameter_names, _generate_description_from, _register_auto_complete_function,
    _validate_is_default
)
from .slash_command_category import SlashCommandCategory
from .slash_command_function import SlashCommandFunction
from .slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


@export
class SlashCommand(CommandBaseApplicationCommand):
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``Slasher``
        Reference to the slasher application command's parent.
    
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    _permission_overwrites : `None`, `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the slash command.
    
    _registered_application_command_ids : `None`, `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    
    _schema : `None`, ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    
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
    
    allow_in_dm : `None`, `bool`
        Whether the command can be used in private channels (dm).
    
    global_ : `bool`
        Whether the command is a global command.
        
        Global commands have their ``.guild_ids`` set as `None`.
    
    guild_ids : `None`, `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    
    nsfw : `None,` bool`
        Whether the application command is only allowed in nsfw channels.
    
    required_permissions : `None`, ``Permission``
        The required permissions to use the application command inside of a guild.
    
    _auto_completers : `None`, `list` of ``SlashCommandParameterAutoCompleter``
        Auto completer functions.
    
    _command : `None`, ``SlashCommandFunction``
        The command of the slash command.
    
    _self_reference : `None`, ``WeakReferer`` to ``SlashCommand``
        Back reference to the slasher application command.
        
        Used by sub commands to access the parent entity.
    
    _sub_commands : `None`, `dict` of (`str`, (``SlashCommandFunction`` or ``SlashCommandCategory``)) items
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    
    default : `bool`
        Whether the command is the default command in it's category.
    
    description : `str`
        Application command description. It's length can be in range [2:100].
    
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : `tuple` of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's "command" defining parameter's name.
    
    Notes
    -----
    ``SlashCommand``-s are weakreferable.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_command', '_self_reference', '_sub_commands', 'description'
    )
    
    SLASH_COMMAND_PARAMETER_NAMES = (
        *CommandBaseApplicationCommand.COMMAND_PARAMETER_NAMES,
        'description',
        'is_default',
    )
    
    @CommandBaseApplicationCommand.target.getter
    def target(self):
        return ApplicationCommandTargetType.chat
    
    
    def __new__(
        cls,
        func,
        name = None,
        description = None,
        is_global = None,
        guild = None,
        is_default = None,
        delete_on_unload = None,
        allow_in_dm = None,
        required_permissions = None,
        nsfw = None,
        **keyword_parameters,
    ):
        """
        Creates a new ``SlashCommand`` with the given parameters.
        
        Parameters
        ----------
        func : `None`, `async-callable` = `None`, Optional
            The function used as the command when using the respective slash command.
        
        name : `None`, `str`, `tuple` of (`str`, `Ellipsis`, `None`) = `None`, Optional
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        
        description : `None`, `Any`, `tuple` of (`None`, `Ellipsis`, `Any`) = `None`, Optional
            Description to use instead of the function's docstring.
        
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the slash command is global. Defaults to `False`.
        
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)) = `None`
                , Optional
            To which guild(s) the command is bound to.
        
        is_global : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the slash command is the default command in it's category.
        
        delete_on_unload : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command should be deleted from Discord when removed.
        
        allow_in_dm : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the command can be used in private channels (dm).
        
        required_permissions : `None`, `int`, ``Permission``, `tuple` of (`None`, `int`, ``Permission``,
                `Ellipsis`) = `None`, Optional
            The required permissions to use the application command inside of a guild.
        
        nsfw : `None`, `bool`, `tuple` of (`None`, `bool`, `Ellipsis`) = `None`, Optional
            Whether the application command is only allowed in nsfw channels.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other parameters
        ----------------
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, \
                `list` of (`str`, ``UserBase``, ``Role`` ), Optional (Keyword only)
            Which user or role can the response message ping (or everyone).
        show_for_invoking_user_only : `bool`, Optional (Keyword only)
            Whether the response message should only be shown for the invoking user.
        wait_for_acknowledgement : `bool`, Optional (Keyword only)
            Whether acknowledge tasks should be ensure asynchronously.
        
        Returns
        -------
        self : ``SlashCommand``, ``Router``
        
        Raises
        ------
        TypeError
            If a parameter's type is incorrect.
        ValueError
            If a parameter's value is incorrect.
        """
        if (func is not None) and isinstance(func, CommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing
        
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        description, route_to = _check_maybe_route('description', description, route_to, None)
        is_global, route_to = _check_maybe_route('is_global', is_global, route_to, _validate_is_global)
        guild_ids, route_to = _check_maybe_route('guild', guild, route_to, _validate_guild)
        is_default, route_to = _check_maybe_route('is_default', is_default, route_to, _validate_is_default)
        unloading_behaviour, route_to = _check_maybe_route(
            'delete_on_unload', delete_on_unload, route_to, _validate_delete_on_unload
        )
        allow_in_dm, route_to = _check_maybe_route('allow_in_dm', allow_in_dm, route_to, _validate_allow_in_dm)
        nsfw, route_to = _check_maybe_route('nsfw', nsfw, route_to, _validate_nsfw)
        required_permissions, route_to = _check_maybe_route(
            'required_permissions', required_permissions, route_to, _validate_required_permissions
        )
        
        if route_to:
            name = route_name(name, route_to)
            name = [raw_name_to_display(check_name(command, sub_name)) for sub_name in name]
            
            default_description = _generate_description_from(command, None, None)
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            is_default = route_value(is_default, route_to)
            unloading_behaviour = route_value(unloading_behaviour, route_to)
            allow_in_dm = route_value(allow_in_dm, route_to)
            nsfw = route_value(nsfw, route_to)
            required_permissions = route_value(required_permissions, route_to)
            
            description = [
                (
                    _generate_description_from(command, sub_name, description)
                    if ((description is None) or (description is not default_description)) else
                    default_description
                )
                for sub_name, description in zip(name, description)
            ]
        
        else:
            name = check_name(command, name)
            name = raw_name_to_display(name)
            
            description = _generate_description_from(command, name, description)
        
        
        # Check extra parameters
        response_modifier = ResponseModifier(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        
        if command is None:
            parameter_converters = None
        else:
            parameter_configurers = get_parameter_configurers(wrappers)
            command, parameter_converters = get_slash_command_parameter_converters(command, parameter_configurers)
    
        
        if route_to:
            router = []
            
            for (
                name, description, is_global, guild_ids, is_default, unloading_behaviour,
                nsfw, required_permissions, allow_in_dm
            ) in zip(
                name, description, is_global, guild_ids, is_default, unloading_behaviour,
                nsfw, required_permissions, allow_in_dm
            ):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(
                        f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                        f'guild={guild!r}.'
                    )
                
                if (command is None):
                    command_function = None
                    sub_commands = {}
                else:
                    command_function = SlashCommandFunction(
                        command, parameter_converters, name, description, response_modifier, is_default
                    )
                    sub_commands = None
                
                self = object.__new__(cls)
                self._command = command_function
                self._sub_commands = sub_commands
                self.description = description
                self.guild_ids = guild_ids
                self.global_ = is_global
                self.name = name
                self._schema = None
                self._registered_application_command_ids = None
                self.default = is_default
                self._unloading_behaviour = unloading_behaviour
                self.allow_in_dm = allow_in_dm
                self.nsfw = nsfw
                self.required_permissions = required_permissions
                self._permission_overwrites = None
                self._auto_completers = None
                self._exception_handlers = None
                self._parent_reference = None
                self._self_reference = None
                
                if (command_function is not None):
                    command_function._parent_reference = self._get_self_reference()
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(
                    f'`is_global` and `guild` contradict each other, got is_global = {is_global!r}, '
                    f'guild={guild!r}.'
                )
            
            if (command is None):
                sub_commands = {}
                command_function = None
            else:
                command_function = SlashCommandFunction(
                    command, parameter_converters, name, description, response_modifier, is_default
                )
                sub_commands = None
            
            self = object.__new__(cls)
            self._command = command_function
            self._sub_commands = sub_commands
            self.description = description
            self.guild_ids = guild_ids
            self.global_ = is_global
            self.name = name
            self._schema = None
            self._registered_application_command_ids = None
            self.default = is_default
            self._unloading_behaviour = unloading_behaviour
            self.allow_in_dm = allow_in_dm
            self.nsfw = nsfw
            self.required_permissions = required_permissions
            self._permission_overwrites = None
            self._auto_completers = None
            self._exception_handlers = None
            self._parent_reference = None
            self._self_reference = None
            
            if (command_function is not None):
                command_function._parent_reference = self._get_self_reference()
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    @copy_docs(CommandBaseApplicationCommand._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in CommandBaseApplicationCommand._cursed_repr_builder(self):
            
            yield repr_parts
            
            description = self.description
            if self.name != description:
                 repr_parts.append(', description = ')
                 repr_parts.append(repr(description))
    
    
    @copy_docs(CommandBaseApplicationCommand.invoke)
    async def invoke(self, client, interaction_event):
        options = interaction_event.interaction.options
        
        command = self._command
        if (command is not None):
            await command.invoke(client, interaction_event, options)
            return
        
        if (options is None) or (len(options) != 1):
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
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
                list(self._sub_commands.keys()),
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
            sub_commands = {category_name: category.copy() for category_name, category in sub_commands.items()}
        new._sub_commands = sub_commands
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # ---- POST LINKING ----
        
        if (sub_commands is not None):
            for sub_command in sub_commands.values():
                sub_command._parent_reference = new._get_self_reference()
        
        return new
    
    
    
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
        auto_complete_option : ``ApplicationCommandAutocompleteInteraction``, \
                ``ApplicationCommandAutocompleteInteractionOption``
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
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            options = [sub_command.as_option() for sub_command in sub_commands.values()]
        
        else:
            parameter_converters = command._parameter_converters
            
            options = None
            for parameter_converter in parameter_converters:
                option = parameter_converter.as_option()
                if (option is not None):
                    if (options is None):
                        options = []
                    
                    options.append(option)
    
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
        new : ``SlashCommandFunction``, ``SlashCommandCategory``
        """
        command = self._command
        if (command is not None):
            return command
        
        return SlashCommandCategory(self, deepness)
    
    
    @property
    @copy_docs(CommandBaseApplicationCommand.interactions)
    def interactions(self):
        if self._command is not None:
            raise RuntimeError(
                f'The {self.__class__.__name__} is not a category.'
            )
        
        return _EventHandlerManager(self)
    
    
    def create_event(self, func, *args, **keyword_parameters):
        """
        Adds a sub-command under the slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        *args : Positional Parameters
            Positional parameters to pass to ``SlashCommand``'s constructor.
        **keyword_parameters : Keyword parameters
            Keyword parameters to pass to the ``SlashCommand``'s constructor.
        
        Returns
        -------
        self : ``SlashCommandFunction``, ``SlashCommandCategory``
        
        Raises
        ------
        TypeError
            If Any parameter's type is incorrect.
        ValueError
            If Any parameter's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self!r} is not a category.')
        
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, type(self)):
            self._add_application_command(func)
            return self
        
        command = type(self)(func, *args, **keyword_parameters)
        
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command or sub-category.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``SlashCommandFunction``, ``SlashCommandCategory``
         
        Raises
        ------
        TypeError
            If Any attribute's type is incorrect.
        ValueError
            If Any attribute's value is incorrect.
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        command = type(self).from_class(klass)
        
        if isinstance(command, Router):
            command = command[0]
        
        return self._add_application_command(command)
    
    
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
        if len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX and (command.name not in sub_commands):
            raise RuntimeError(
                f'The {self!r} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).'
            )
        
        if command.default:
            for sub_command in sub_commands.values():
                if sub_command.default:
                    raise RuntimeError(
                        f'{self!r} already has a default command.'
                    )
        
        as_sub_command = command.as_sub_command(APPLICATION_COMMAND_CATEGORY_DEEPNESS_START)
        as_sub_command._parent_reference = self._get_self_reference()
        
        sub_commands[as_sub_command.name] = as_sub_command
        _reset_application_command_schema(self)
        
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            for auto_completer in auto_completers:
                as_sub_command._try_resolve_auto_completer(auto_completer)
        
        return as_sub_command
    
    
    @copy_docs(CommandBaseApplicationCommand.get_real_command_count)
    def get_real_command_count(self):
        if (self._command is None):
            sub_commands = self._sub_commands
            real_command_count = 0
            
            if (sub_commands is not None):
                for sub_command_or_category in sub_commands.values():
                    if isinstance(sub_command_or_category, SlashCommandFunction):
                        real_command_count += 1
                    else:
                        # Nesting more is not allowed by Discord.
                        real_command_count += len(sub_command_or_category._sub_commands)
        
        else:
            real_command_count = 1
        
        return real_command_count
    
    
    @copy_docs(CommandBaseApplicationCommand.autocomplete)
    def autocomplete(self, parameter_name, *parameter_names, function = None):
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
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The registered auto completer
        
        Raises
        ------
        RuntimeError
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            - If `function` is not an asynchronous.
        """
        if isinstance(function, SlashCommandParameterAutoCompleter):
            function = function._command_function
        
        command_function = self._command
        if command_function is None:
            
            auto_completer = SlashCommandParameterAutoCompleter(
                function,
                parameter_names,
                APPLICATION_COMMAND_DEEPNESS,
                self,
            )
            
            # If it is none, try to resolve the parameters in sub commands.
            auto_completers = self._auto_completers
            if (auto_completers is None):
                auto_completers = []
                self._auto_completers = auto_completers
            
            auto_completers.append(auto_completer)
            
            sub_commands = self._sub_commands
            if (sub_commands is not None):
                for sub_command in sub_commands.values():
                    sub_command._try_resolve_auto_completer(auto_completer)
        
        else:
            auto_completer = command_function._add_autocomplete_function(parameter_names, function)
        
        _reset_application_command_schema(self)
        
        return auto_completer
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``SlashCommand``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``SlashCommand``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    
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
