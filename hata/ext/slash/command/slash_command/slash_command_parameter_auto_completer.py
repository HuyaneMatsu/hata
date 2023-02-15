__all__ = ('SlashCommandParameterAutoCompleter', )


from functools import partial as partial_func

from scarletio import RichAttributeErrorBaseType, export

from .....discord.client import Client
from .....discord.interaction import InteractionEvent

from ...converters import SlashCommandParameterConverter, get_application_command_parameter_auto_completer_converters

from ...exceptions import _register_exception_handler, handle_command_exception, test_exception_handler
from ...responding import process_command_coroutine
from ...utils import raw_name_to_display

from ..command_base_application_command.constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS


@export
class SlashCommandParameterAutoCompleter(RichAttributeErrorBaseType):
    """
    Represents an application command parameter's auto completer.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _parent_reference : `None`, ``WeakReferer`` to (``SlashCommand``,
            ``SlashCommandFunction``, ``SlashCommandCategory``)
        The parent slash command of the auto completer, where it was registered to.
    name_pairs : `frozenset` of `tuple` (`str`, `str`)
        Raw - display parameter names, to which the converter should autocomplete.
    deepness : `int`
        How deep the auto completer was created. Deeper auto completers always overwrite higher ones.
    """
    __slots__ = (
        '_command_function', '_exception_handlers', '_parameter_converters', '_parent_reference', 'deepness',
        'name_pairs'
    )
    
    def __new__(cls, function, parameter_names, deepness, parent):
        """
        Creates a new ``SlashCommandParameterAutoCompleter`` with the given parameters.
        
        Parameters
        ----------
        function : `async-callable`
            The function to create auto completer from.
        parameter_names : `list` of `str`
            The names, which should be auto completed.
        deepness : `int`
            How deep the auto completer was created.
        parent : `None`, ``Slasher``, ``SlashCommand``, ``SlashCommandCategory``,
            ``SlashCommandFunction``
        """
        command, parameter_converters = get_application_command_parameter_auto_completer_converters(function)
        
        name_pairs = frozenset((name, raw_name_to_display(name)) for name in set(parameter_names))
        
        if parent is None:
            parent_reference = None
        else:
            parent_reference = parent._get_self_reference()
        
        self = object.__new__(cls)
        
        self._command_function = command
        self._parameter_converters = parameter_converters
        self.name_pairs = name_pairs
        self.deepness = deepness
        self._parent_reference = parent_reference
        self._exception_handlers = None
        
        return self
    
    
    def _bind_parent(self, new_parent):
        """
        Binds the parent application command function to self.
        
        If the auto completer is already bound to an other object, will return a new one.
        
        Parameter
        ---------
        new_parent : `None`, ``SlashCommandFunction``
            The parent to bind to self.
        
        Returns
        -------
        new : ``SlashCommandParameterAutoCompleter``
            The new auto completer function bound to the new parent.
        """
        parent_reference = self._parent_reference
        if (parent_reference is None):
            self_parent = None
        else:
            self_parent = parent_reference()
        
        if (new_parent is None):
            if (self_parent is None):
                new = self
                new._parent_reference = None
            
            else:
                new = self.copy()
                new._parent_reference = None
        
        else:
            if (self_parent is None):
                new = self
                new._parent_reference = new_parent._get_self_reference()
            
            else:
                if (new_parent is self_parent):
                    new = self
                
                else:
                    new = self.copy()
                    new._parent_reference = new_parent._get_self_reference()
        
        return new
    
    
    def copy(self):
        """
        Copies the parameter auto completer.
        
        Returns
        -------
        new : ``SlashCommandFunction``
        """
        new = object.__new__(type(self))
        
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
        
        # deepness
        new.deepness = self.deepness
        
        # name_pairs
        new.name_pairs = self.name_pairs
        
        return new
    

    def __repr__(self):
        """Returns the parameter auto completer's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name_pairs=')
        repr_parts.append(repr(self.name_pairs))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the parameter auto completer's hash value."""
        hash_value = 0
        
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
        
        # _parent_reference
        # Internal field
        
        # deepness
        hash_value ^= self.deepness
        
        # name_pairs
        hash_value ^= hash(self.name_pairs)
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return
        
        # _command_function
        if self._command_function != other._command_function:
            return False
        
        # _exception_handlers
        if self._exception_handlers != other._exception_handlers:
            return False
        
        # _parent_reference
        # Internal field
        
        # deepness
        if self.deepness != other.deepness:
            return False
        
        # name_pairs
        if self.name_pairs != other.name_pairs:
            return False
        
        return True
    
    
    async def invoke(self, client, interaction_event):
        """
        Calls the parameter auto completer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        parameters = []
        
        for parameter_converter in self._parameter_converters:
            parameter = await parameter_converter(client, interaction_event, None)
            parameters.append(parameter)
        
        auto_completer_coroutine = self._command_function(*parameters)
        
        try:
            await process_command_coroutine(
                client,
                interaction_event,
                None,
                auto_completer_coroutine,
            )
        except GeneratorExit:
            raise
        
        except BaseException as err:
            exception = err
        
        else:
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            exception,
        )
        return
    
    
    def _is_deeper_than(self, other):
        """
        Returns whether self is deeper than other.
        
        Parameters
        ----------
        other : ``SlashCommandParameterAutoCompleter``
        """
        self_deepness = self.deepness
        if self_deepness == APPLICATION_COMMAND_FUNCTION_DEEPNESS:
            return True
        
        other_deepness = other.deepness
        if other_deepness == APPLICATION_COMMAND_FUNCTION_DEEPNESS:
            return False
        
        if self_deepness > other_deepness:
            return True
        
        return False
    
    
    def _difference_match_parameters(self, auto_completable_parameters):
        """
        Matches auto completable parameters returning a list of the matched ones.
        
        Parameters
        ----------
        auto_completable_parameters : `set` of ``SlashCommandParameterConverter``
            Auto completable parameters.
        
        Returns
        -------
        matched : `list` of ``SlashCommandParameterConverter``
            The matched parameters.
        """
        matched = []
        
        name_pairs = set(self.name_pairs)
        
        for name_pair in list(name_pairs):
            name = name_pair[1]
            
            for parameter in auto_completable_parameters:
                if parameter.name == name:
                    name_pairs.discard(name_pair)
                    matched.append(parameter)
                    auto_completable_parameters.discard(parameter)
                    break
        
        for name_pair in list(name_pairs):
            name = name_pair[0]
            
            for parameter in auto_completable_parameters:
                if parameter.parameter_name == name:
                    name_pairs.discard(name_pair)
                    matched.append(parameter)
                    auto_completable_parameters.discard(parameter)
                    break
        
        return matched
    
    
    def error(self, exception_handler = None, *, first = False):
        """
        Registers an exception handler to the ``SlashCommandParameterAutoCompleter``.
        
        Parameters
        ----------
        exception_handler : `None`, `CoroutineFunction` = `True`, Optional
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
        Registers an exception handler to the ``SlashCommandParameterAutoCompleter``.
        
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
