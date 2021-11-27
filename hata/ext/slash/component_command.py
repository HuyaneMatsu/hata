__all__ = ('ComponentCommand', )

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern

from functools import partial as partial_func

from ...discord.events.handling_helpers import route_value, Router, create_event_from_class, check_name, route_name

from .wrappers import SlasherCommandWrapper
from .utils import _check_maybe_route
from .converters import get_component_command_parameter_converters
from .responding import process_command_coroutine
from .exceptions import handle_command_exception, test_exception_handler, _register_exception_handler
from .custom_id_based_command import _validate_name, _validate_custom_ids, split_and_check_satisfaction, \
    CustomIdBasedCommand

COMPONENT_COMMAND_PARAMETER_NAMES = ('command', 'custom_id', 'name')

COMPONENT_COMMAND_NAME_NAME = 'name'
COMPONENT_COMMAND_COMMAND_NAME = 'command'


class ComponentCommand(CustomIdBasedCommand):
    """
    A command, which is called if a command interaction is executed with a specific `custom_id`.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _exception_handlers : `None` or `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None` or ``WeakReferer`` to ``SlasherApplicationCommand``
        The parent slasher of the component command.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _string_custom_ids : `None` or `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None` or `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    name : `str`
        The component commands name.
        
        Only used for debugging.
    """
    __slots__ = ()
    
    
    @classmethod
    def from_class(cls, klass):
        """
        Creates a new ``ComponentCommand`` instance from the given `klass`.
        
        Parameters
        ----------
        klass : `type`
            The class to create component command from.
        
        Returns
        -------
        self : ``ComponentCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's type is incorrect.
        ValueError
            If any attribute's value is incorrect.
        """
        return create_event_from_class(cls, klass, COMPONENT_COMMAND_PARAMETER_NAMES, COMPONENT_COMMAND_NAME_NAME,
            COMPONENT_COMMAND_COMMAND_NAME)
    
    
    def __new__(cls, func, custom_id, name=None):
        """
        Creates a new ``ComponentCommand`` instance with the given parameters
        
        Parameters
        ----------
        func : `None` or `async-callable`, Optional
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list` or `set`) of `str`, `tuple` of (`str`, (`list` or `set`) of `str`)
            Custom id to match by the component command.
        name : `str` or `None`, Optional
            The name of the component command.
        
        Returns
        -------
        self : ``ComponentCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only parameters.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `name` was not given neither as `None` or `str` instance.
            - If `custom_id`'s type is incorrect.
        ValueError:
            - If no `custom_id` was received.
            - If `custom_id` contains incorrect value.
        """
        if (func is not None) and isinstance(func, SlasherCommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing.
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        custom_id, route_to = _check_maybe_route('custom_id', custom_id, route_to, _validate_custom_ids)
        
        command, parameter_converters = get_component_command_parameter_converters(command)
        
        if route_to:
            custom_id = route_value(custom_id, route_to)
            name = route_name(name, route_to)
            name = [check_name(command, sub_name) for sub_name in name]
            
            router = []
            
            for custom_id, name in zip(custom_id, name):
                string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
                
                self = object.__new__(cls)
                self._command_function = command
                self._parameter_converters = parameter_converters
                self._string_custom_ids = string_custom_ids
                self._regex_custom_ids = regex_custom_ids
                self._parent_reference = None
                self._exception_handlers = None
                self.name = name
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        
        else:
            name = check_name(command, name)
            
            string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
            
            self = object.__new__(cls)
            self._command_function = command
            self._parameter_converters = parameter_converters
            self._string_custom_ids = string_custom_ids
            self._regex_custom_ids = regex_custom_ids
            self._parent_reference = None
            self._exception_handlers = None
            self.name = name
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    
    def __repr__(self):
        """Returns the component command's representation."""
        repr_parts = ['<', self.__class__.__name__, ' name=', repr(self.name)]
        
        string_custom_ids = self._string_custom_ids
        if (string_custom_ids is not None):
            
            repr_parts.append(', string_custom_ids=[')
            index = 0
            limit = len(string_custom_ids)
            
            while True:
                string_custom_id = string_custom_ids[index]
                repr_parts.append(repr(string_custom_id))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        regex_custom_ids = self._regex_custom_ids
        if (regex_custom_ids is not None):
            
            repr_parts.append(', regex_custom_ids=[')
            index = 0
            limit = len(regex_custom_ids)
            
            while True:
                regex_custom_id = regex_custom_ids[index]
                repr_parts.append(repr(regex_custom_id.pattern.pattern))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        return ''.join(repr_parts)
    
    
    async def __call__(self, client, interaction_event, regex_match):
        """
        Calls the component command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        regex_match : `None` or ``RegexMatch``
            The matched regex if applicable.
        """
        parameters = []
        
        for parameter_converter in self._parameter_converters:
            try:
                parameter = await parameter_converter(client, interaction_event, regex_match)
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
            await process_command_coroutine(client, interaction_event, False, command_coroutine)
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
    
    def __hash__(self):
        """Returns the component command's hash value."""
        hash_value = 0
        
        string_custom_ids = self._string_custom_ids
        if (string_custom_ids is not None):
            hash_value ^= hash(string_custom_ids)
        
        regex_custom_ids = self._regex_custom_ids
        if (regex_custom_ids is not None):
            hash_value ^= hash(regex_custom_ids)
        
        command_function = self._command_function
        try:
            command_hash_value = hash(command_function)
        except KeyError:
            command_hash_value = object.__hash__(command_function)
        
        hash_value ^= command_hash_value
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether self equals to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._command_function != other._command_function:
            return False
        
        if self._string_custom_ids != other._string_custom_ids:
            return False
        
        if self._regex_custom_ids != other._regex_custom_ids:
            return False
        
        if self._exception_handlers != other._exception_handlers:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the component command.
        
        Returns
        -------
        new : ``ComponentCommand``
        """
        new = object.__new__(type(self))
        new._command_function = self._command_function
        new._parameter_converters = self._parameter_converters
        new._string_custom_ids = self._string_custom_ids
        new._regex_custom_ids = self._regex_custom_ids
        new._parent_reference = None
        
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        return new


    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the ``SlasherApplicationCommandCategory``.
        
        Parameters
        ----------
        exception_handler : `None` or `CoroutineFunction`, Optional
            Exception handler to register.
        first : `bool`, Optional (Keyword Only)
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
        Registers an exception handler to the ``SlasherApplicationCommandCategory``.
        
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
