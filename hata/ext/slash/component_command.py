__all__ = ('ComponentCommand', )

from ...discord.limits import COMPONENT_CUSTOM_ID_LENGTH_MAX
from ...discord.events.handling_helpers import route_value, Router, create_event_from_class
from .wrappers import SlashCommandWrapper
from .utils import _check_maybe_route
from .converters import generate_parameter_parsers
from .responding import process_command_coroutine

SLASH_COMMAND_PARAMETER_NAMES = ('command', 'custom_id')

SLASH_COMMAND_NAME_NAME = None
SLASH_COMMAND_COMMAND_NAME = 'command'

def _validate_custom_id(custom_id):
    """
    Validates a `custom_id` value.
    
    Parameters
    ----------
    custom_id : `str`
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `str`
        The validated custom_id.
    
    Raises
    ------
    ValueError
        If `custom_id`'s length is out of the expected range.
    """
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
    custom_id : `tuple` of `set`
        The non-duped custom-ids.
    
    Raises
    ------
    TypeError
        If `custom_id`'s type is incorrect.
    ValueError
        If a `custom_id`'s length is out of the expected range.
    """
    if isinstance(custom_id, str):
        custom_id = _validate_custom_id(custom_id)
        custom_ids = (custom_id,)
    elif isinstance(custom_id, (list, set)):
        custom_ids = set()
        
        for sub_custom_id in custom_id:
            if isinstance(sub_custom_id, str):
                sub_custom_id = _validate_custom_id(sub_custom_id)
                custom_ids.add(sub_custom_id)
                continue
            
            raise TypeError(f'`custom_id` contains a non `st` element, got: {custom_id.__class__.__name__}.')
        
        if not custom_id:
            raise ValueError(f'`custom_id` received as empty {custom_id.__class__.__name__}.')
        
        custom_ids = tuple(sorted(custom_ids))
    
    else:
        raise TypeError(f'`custom_id` can be given as `str`, (`list`, `set`) of `str`, got '
            f'{custom_id.__class__.__name__}.')
    
    return custom_ids


class ComponentCommand:
    """
    A command, which is called if a command interaction is executed wit ha specific `custom_id`.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _parameter_parsers : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    custom_ids : `tuple` of `str`
        The custom id-s to wait for.
    """
    __slots__ = ('_command_function', '_parameter_parsers', 'custom_ids')
    
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
        if (func is not None) and isinstance(func, SlashCommandWrapper):
            command, wrappers = func.fetch_function_and_wrappers_back()
        else:
            command = func
            wrappers = None
        
        # Check for routing.
        route_to = 0
        custom_id, route_to = _check_maybe_route('name', custom_id, route_to, _validate_custom_ids)
        
        command, parameter_parsers = generate_parameter_parsers(command, None)
        for parameter_parser in parameter_parsers:
            if not parameter_parser.is_internal:
                raise TypeError(f'{cls.__name__} supports only internal parameters.')
        
        if route_to:
            custom_id = route_value(custom_id, route_to)
            
            router = []
            
            for custom_id in custom_id:
                self = object.__new__(cls)
                self._command_function = command
                self._parameter_parsers = parameter_parsers
                self.custom_ids = custom_id
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            self = object.__new__(cls)
            self._command_function = command
            self._parameter_parsers = parameter_parsers
            self.custom_ids = custom_id
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)

            return self
    
    def __repr__(self):
        """Returns the component command's representation."""
        return f'<{self.__class__.__name__} custom_ids={self.custom_ids!r}.'
    
    async def __call__(self, client, interaction_event):
        """
        Calls the component command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        parameters = []
        
        for parameter_parser in self._parameter_parsers:
            parameter = await parameter_parser(client, interaction_event, None)
            parameters.append(parameter)
        
        command_coroutine = self._command_function(*parameters)
        
        await process_command_coroutine(client, interaction_event, False, command_coroutine)
    
    def __hash__(self):
        """Returns the component command's hash value."""
        hash_value = hash(self.custom_ids)
        
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
        
        if self.custom_ids != other.custom_ids:
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
        new._command_function = self.command
        new._parameter_parsers = self.parameter_parsers
        new.custom_ids = self.custom_id
        return new
