__all__ = ('SlashCommandFunction',)

from functools import partial as partial_func

from scarletio import WeakReferer, RichAttributeErrorBaseType, copy_docs

from .....discord.application_command import ApplicationCommandOption, ApplicationCommandOptionType
from .....discord.client import Client
from .....discord.interaction import InteractionEvent

from ...converters import InternalParameterConverter, SlashCommandParameterConverter
from ...exceptions import _register_exception_handler, handle_command_exception, test_exception_handler
from ...responding import process_command_coroutine

from ..command_base import CommandBase
from ..command_base_application_command.constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS

from .helpers import _build_auto_complete_parameter_names, _register_auto_complete_function
from .slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


class SlashCommandFunction(RichAttributeErrorBaseType):
    """
    Represents a slash command's backend implementation.
    
    Attributes
    ----------
    _auto_completers : `None`, `list` of ``SlashCommandParameterAutoCompleter``
        Auto completer functions.
    
    _command_function : `async-callable˛
        The command's function to call.
    
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    
    _parent_reference : `None`, ``WeakReferer`` to (``SlashCommand``,``SlashCommandCategory``)
        Reference to the parent application command or category.
    
    _self_reference : `None`, ``WeakReferer`` to ``SlashCommandFunction``
        Back reference to the slasher application command function.
        
        Used by auto completers to access the parent entity.
    
    description : `str`
        The slash command's description.
    
    default : `bool`
        Whether the command is the default command in it's category.
    
    name : `str`
        The name of the slash command. It's length can be in range [1:32].
    
    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_command_function', '_exception_handlers', '_parameter_converters',
        '_parent_reference', '_self_reference', 'description', 'default', 'name', 'response_modifier'
    )
    
    def __new__(cls, command_function, parameter_converters, name, description, response_modifier, default):
        """
        Creates a new ``SlashCommandFunction`` with the given parameters.
        
        Parameters
        ----------
        command_function : `async-callable`
            The command's function to call.
        parameter_converters : `tuple` of ``ParameterConverter``
            Parsers to parse command parameters.
        name : `str`
            The name of the slash command.
        description : `str`
            The slash command's description.
        response_modifier : `None`, ``ResponseModifier``
            Modifies values returned and yielded to command coroutine processor.
        default : `bool`
            Whether the command is the default command in it's category.
        """
        self = object.__new__(cls)
        self._auto_completers = None
        self._command_function = command_function
        self._parameter_converters = parameter_converters
        self.response_modifier = response_modifier
        self.description = description
        self.name = name
        self.default = default
        self._exception_handlers = None
        self._parent_reference = None
        self._self_reference = None
        
        for parameter_converter in parameter_converters:
            parameter_converter.bind_parent(self)
        
        return self
    
    
    async def invoke(self, client, interaction_event, options):
        """
        Calls the slash command function.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None`, `list` of ``InteractionEventChoice``
            Options bound to the function.
        
        Raises
        ------
        SlashCommandParameterConversionError
            Exception occurred meanwhile parsing parameter.
        """
        parameters = []
        
        parameter_relation = {}
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for parameter_converter in self._parameter_converters:
            if isinstance(parameter_converter, InternalParameterConverter):
                value = None
            else:
                value = parameter_relation.get(parameter_converter.name, None)
            
            try:
                parameter = await parameter_converter(client, interaction_event, value)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                exception = err
            
            else:
                parameters.append(parameter)
                continue
                
            await handle_command_exception(
                self,
                client,
                interaction_event,
                exception,
            )
            return
            
        
        command_coroutine = self._command_function(*parameters)
        
        try:
            await process_command_coroutine(
                client,
                interaction_event,
                self.response_modifier,
                command_coroutine,
            )
        except GeneratorExit:
            raise
        
        except BaseException as err:
            exception = err
        
        else:
            return
        
        await handle_command_exception(
            self,
            client,
            interaction_event,
            exception,
        )
        return
    
    
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
        focused_option = auto_complete_option.focused_option
        if (focused_option is None):
            return
        
        parameter_name = focused_option.name
        
        for parameter_converter in self._parameter_converters:
            if isinstance(parameter_converter, SlashCommandParameterConverter):
                if parameter_converter.name == parameter_name:
                    break
        else:
            return
        
        auto_completer = parameter_converter.auto_completer
        if (auto_completer is not None):
            await auto_completer.invoke(client, interaction_event)
        
    
    def _get_auto_completable_parameters(self):
        """
        Gets the auto completable parameter converters of the application command function.
        
        Returns
        -------
        parameter_converters : `list` of ``SlashCommandParameterConverter``
        """
        auto_completable_parameters = set()
        
        for parameter_converter in self._parameter_converters:
            if (
                isinstance(parameter_converter, SlashCommandParameterConverter) and
                parameter_converter.can_auto_complete()
            ):
                auto_completable_parameters.add(parameter_converter)
        
        return auto_completable_parameters
    
    def __repr__(self):
        """Returns the application command option's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' name = ', repr(self.name),
            ', description = ', repr(self.description),
        ]
        
        if self.default:
            repr_parts.append(', default = True')
        
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            repr_parts.append(', response_modifier = ')
            repr_parts.append(repr(response_modifier))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __format__(self, code):
        """Formats the slash command function in a format string."""
        if not code:
            return str(self)
        
        if code == 'm':
            return self.mention
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"m"!r}.'
        )
    
    
    def as_option(self):
        """
        Returns the slash command function as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        parameter_converters = self._parameter_converters
        options = None
        for parameter_converter in parameter_converters:
            option = parameter_converter.as_option()
            if (option is not None):
                if options is None:
                    options = []
                
                options.append(option)
        
        return ApplicationCommandOption(
            self.name,
            self.description,
            ApplicationCommandOptionType.sub_command,
            options = options,
            default = self.default,
        )
    
    
    def copy(self):
        """
        Copies the slash command function.
        
        Returns
        -------
        self : ``SlashCommandFunction``
        """
        new = object.__new__(type(self))
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        # _command_function
        new._command_function = self._command_function
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        # _parameter_converters
        new._parameter_converters = self._parameter_converters
        
        # _parent_reference
        new._parent_reference = None
        
        # _self_reference
        new._self_reference = None
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # name
        new.name = self.name
        
        # response_modifier
        new.response_modifier = self.response_modifier
        
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two slash command functions are equal."""
        if type(self) is not type(other):
            return False
        
        # _auto_completers
        if self._auto_completers != other._auto_completers:
            return False
        
        # _command_function
        if self._command_function != other._command_function:
            return False
        
        # _exception_handlers
        if self._exception_handlers != other._exception_handlers:
            return False
        
        # _parameter_converters
        # Internal field
        
        # _parent_reference
        # Internal field
        
        # _self_reference
        # Internal field
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # response_modifier
        if self.response_modifier != other.response_modifier:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the slash command function's hash value."""
        hash_value = 0
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            hash_value ^= len(auto_completers)
            
            for auto_completer in auto_completers:
                hash_value ^= hash(auto_completer)
        
        # _command_function
        command_function = self._command_function
        try:
            command_function_hash_value = hash(command_function)
        except TypeError:
            command_function_hash_value = object.__hash__(command_function)
        hash_value ^= command_function_hash_value
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            hash_value ^= len(exception_handlers) << 4
            
            for exception_handler in exception_handlers:
                try:
                    exception_handler_hash_value = hash(exception_handler)
                except TypeError:
                    exception_handler_hash_value = object.__hash__(exception_handler)
                hash_value ^= exception_handler_hash_value
        
        # _parameter_converters
        # Internal field
        
        # _parent_reference
        # Internal field
        
        # _self_reference
        # Internal field
        
        # default
        hash_value ^= self.default << 8
        
        description = self.description
        hash_value ^= hash(description)
        
        # name
        name = self.name
        if name != description:
            hash_value ^= hash(name)
        
        # response_modifier
        hash_value ^= hash(self.response_modifier)
        
        return hash_value
        
    
    def autocomplete(self, parameter_name, *parameter_names, function = None):
        """
        Registers an auto completer function to the application command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `callable` = `None`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `callable`, `functools.partial`
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
        
        auto_completer = SlashCommandParameterAutoCompleter(
            function,
            parameter_names,
            APPLICATION_COMMAND_FUNCTION_DEEPNESS,
            self,
        )
        
        auto_completable_parameters = self._get_auto_completable_parameters()
        matched_auto_completable_parameters = auto_completer._difference_match_parameters(auto_completable_parameters)
        if not matched_auto_completable_parameters:
            raise RuntimeError(
                f'Application command function `{self.name}` has no parameter matching any '
                f'parameters of `{auto_completer!r}`.'
            )
        
        auto_completers = self._auto_completers
        if (auto_completers is None):
            auto_completers = []
            self._auto_completers = auto_completers
        
        auto_completers.append(auto_completer)
        
        for parameter_converter in matched_auto_completable_parameters:
            parameter_converter.register_auto_completer(auto_completer)
        
        return auto_completer
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command function.
        
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
        
        auto_completable_parameters = self._get_auto_completable_parameters()
        matched_auto_completable_parameters = auto_completer._difference_match_parameters(auto_completable_parameters)
        for parameter_converter in matched_auto_completable_parameters:
            resolved += parameter_converter.register_auto_completer(auto_completer)
        
        return resolved
    
    
    def error(self, exception_handler = None, *, first = False):
        """
        Registers an exception handler to the ``SlashCommandFunction``.
        
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
        Registers an exception handler to the ``SlashCommandFunction``.
        
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
    
    
    def _get_self_reference(self):
        """
        Gets a weak reference to the ``SlashCommandFunction``.
        
        Returns
        -------
        self_reference : ``WeakReferer`` to ``SlashCommandFunction``
        """
        self_reference = self._self_reference
        if self_reference is None:
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    # ---- Mention ----
    
    @property
    @copy_docs(CommandBase.mention)
    def mention(self):
        parent_reference = self._parent_reference
        if parent_reference is None:
            parent = None
        else:
            parent = parent_reference()
        
        if parent is None:
            return ''
        
        return parent._mention_recursive(self.name)
    
    
    @copy_docs(CommandBase.mention_at)
    def mention_at(self, guild):
        parent_reference = self._parent_reference
        if parent_reference is None:
            parent = None
        else:
            parent = parent_reference()
        
        if parent is None:
            return ''
        
        return parent._mention_at_recursive(guild, self.name)
