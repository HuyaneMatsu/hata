__all__ = ('ComponentCommand', )

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern

from ...discord.interaction.components import COMPONENT_CUSTOM_ID_LENGTH_MAX
from ...discord.events.handling_helpers import route_value, Router, create_event_from_class
from .wrappers import SlasherCommandWrapper
from .utils import _check_maybe_route
from .converters import get_component_command_parameter_converters, RegexMatcher, \
    check_component_converters_satisfy_string, check_component_converters_satisfy_regex
from .responding import process_command_coroutine

SLASH_COMMAND_PARAMETER_NAMES = ('command', 'custom_id')

SLASH_COMMAND_NAME_NAME = None
SLASH_COMMAND_COMMAND_NAME = 'command'

def _validate_custom_id(custom_id):
    """
    Validates a `custom_id` value.
    
    Parameters
    ----------
    custom_id : `str` or `re.Pattern`
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `str`or `re.Pattern`
        The validated custom_id.
    
    Raises
    ------
    ValueError
        If `custom_id`'s length is out of the expected range.
    """
    if isinstance(custom_id, str):
        if type(custom_id) is not str:
            custom_id = str(custom_id)
        
        custom_id_length = len(custom_id)
        if (custom_id_length < 1) or (custom_id_length > COMPONENT_CUSTOM_ID_LENGTH_MAX):
            raise ValueError(f'`custom_id` length can be in range [1:{COMPONENT_CUSTOM_ID_LENGTH_MAX}], got '
                f'{custom_id_length}; {custom_id!r}.')
    
    return custom_id


def _validate_custom_ids(custom_id):
    """
    Validates one or more `custom_id` values.
    
    Parameters
    ----------
    custom_id : `str`, (`list` or `set`) of `str`.
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `set` of (`str` or `re.Pattern`)
        The non-duped custom-ids.
    
    Raises
    ------
    TypeError
        If `custom_id`'s type is incorrect.
    ValueError
        If a `custom_id`'s length is out of the expected range.
    """
    custom_ids = set()
    if isinstance(custom_id, (str, Pattern)):
        custom_id = _validate_custom_id(custom_id)
        custom_ids.add(custom_id)
    elif isinstance(custom_id, (list, set)):
        
        
        for sub_custom_id in custom_id:
            if isinstance(sub_custom_id, (str, Pattern)):
                sub_custom_id = _validate_custom_id(sub_custom_id)
                custom_ids.add(sub_custom_id)
                continue
            
            raise TypeError(f'`custom_id` contains a non `st` element, got: {custom_id.__class__.__name__}.')
        
        if not custom_id:
            raise ValueError(f'`custom_id` received as empty {custom_id.__class__.__name__}.')
    
    else:
        raise TypeError(f'`custom_id` can be given as `str`, (`list`, `set`) of `str`, got '
            f'{custom_id.__class__.__name__}.')
    
    return custom_ids


def split_and_check_satisfaction(custom_ids, parameter_converters):
    """
    Splits custom id-s to `str` and to `re.Pattern`-s and validates them.
    
    Parameters
    ----------
    custom_ids : `set` of (`str` or `re.Pattern`)
        The custom-ids to split and validate.
    parameter_converters : `tuple` of ``ParameterConverter``
        The parameter converters generated from a component command.
    
    Returns
    -------
    string_custom_ids : `None` or `tuple` of `str`
        String custom ids.
    regex_custom_ids : `None` or `tuple` of ``RegexMatcher``
        Regex custom ids.
    
    Raises
    ------
    ValueError
        A string or regex pattern is not satisfied.
    """
    # Build
    string_custom_ids = None
    regex_custom_ids = None
    for custom_id in custom_ids:
        if isinstance(custom_id, str):
            if string_custom_ids is None:
                string_custom_ids = []
            
            string_custom_ids.append(custom_id)
        else:
            if regex_custom_ids is None:
                regex_custom_ids = []
            
            regex_custom_ids.append(custom_id)
    
    # Convert
    if (string_custom_ids is not None):
        string_custom_ids = tuple(string_custom_ids)
    
    if (regex_custom_ids is not None):
        regex_custom_ids = tuple(RegexMatcher(regex_custom_id) for regex_custom_id in regex_custom_ids)
    
    # Check
    if (string_custom_ids is not None):
        check_component_converters_satisfy_string(parameter_converters)
    
    if (regex_custom_ids is not None):
        for regex_custom_id in regex_custom_ids:
            check_component_converters_satisfy_regex(parameter_converters, regex_custom_id)
    
    # Good
    return string_custom_ids, regex_custom_ids


class ComponentCommand:
    """
    A command, which is called if a command interaction is executed with a specific `custom_id`.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _string_custom_ids : `None` or `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None` or `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    """
    __slots__ = ('_command_function', '_parameter_converters', '_regex_custom_ids', '_string_custom_ids')
    
    
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
        return create_event_from_class(cls, klass, SLASH_COMMAND_PARAMETER_NAMES, SLASH_COMMAND_NAME_NAME,
            SLASH_COMMAND_COMMAND_NAME)
    
    
    def __new__(cls, func, custom_id):
        """
        Creates a new ``ComponentCommand`` instance with the given parameters
        
        Parameters
        ----------
        func : `None` or `async-callable`, Optional
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list` or `set`) of `str`, `tuple` of (`str`, (`list` or `set`) of `str`)
            Custom id to match by the component command.
        
        Returns
        -------
        self : ``ComponentCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only parameters.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`
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
        custom_id, route_to = _check_maybe_route('name', custom_id, route_to, _validate_custom_ids)
        
        command, parameter_converters = get_component_command_parameter_converters(command)
        
        if route_to:
            custom_id = route_value(custom_id, route_to)
            
            router = []
            
            for custom_id in custom_id:
                string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
                
                self = object.__new__(cls)
                self._command_function = command
                self._parameter_converters = parameter_converters
                self._string_custom_ids = string_custom_ids
                self._regex_custom_ids = regex_custom_ids
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            string_custom_ids, regex_custom_ids = split_and_check_satisfaction(custom_id, parameter_converters)
            
            self = object.__new__(cls)
            self._command_function = command
            self._parameter_converters = parameter_converters
            self._string_custom_ids = string_custom_ids
            self._regex_custom_ids = regex_custom_ids
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)

            return self
    
    
    def __repr__(self):
        """Returns the component command's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        string_custom_ids = self._string_custom_ids
        if (string_custom_ids is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' string_custom_ids=[')
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
            if field_added:
                repr_parts.append(', ')
            
            repr_parts.append(' regex_custom_ids=[')
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
            parameter = await parameter_converter(client, interaction_event, regex_match)
            parameters.append(parameter)
        
        command_coroutine = self._command_function(*parameters)
        
        await process_command_coroutine(client, interaction_event, False, command_coroutine)
    
    
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
        return new
