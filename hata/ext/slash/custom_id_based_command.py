__all__ = ('CustomIdBasedCommand', )


from functools import partial as partial_func

from ...discord.events.handling_helpers import create_event_from_class
from ...discord.interaction.components.constants import COMPONENT_CUSTOM_ID_LENGTH_MAX

from .converters import (
    RegexMatcher, check_component_converters_satisfy_regex, check_component_converters_satisfy_string
)
from .exceptions import _register_exception_handler, test_exception_handler


try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern


def _validate_custom_id(custom_id):
    """
    Validates a `custom_id` value.
    
    Parameters
    ----------
    custom_id : `str`, `re.Pattern`
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `str`, `re.Pattern`
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
            raise ValueError(
                f'`custom_id` length can be in range [1:{COMPONENT_CUSTOM_ID_LENGTH_MAX}], got '
                f'{custom_id_length}; {custom_id!r}.'
            )
    
    return custom_id


def _validate_custom_ids(custom_id):
    """
    Validates one or more `custom_id` values.
    
    Parameters
    ----------
    custom_id : `str`, (`list`, `set`) of `str`.
        The `custom_id` to validate.
    
    Returns
    -------
    custom_id : `set` of (`str`, `re.Pattern`)
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
        
        if not custom_id:
            raise ValueError(
                f'`custom_id` received as empty {custom_id.__class__.__name__}.'
            )
        
        for sub_custom_id in custom_id:
            if isinstance(sub_custom_id, (str, Pattern)):
                sub_custom_id = _validate_custom_id(sub_custom_id)
                custom_ids.add(sub_custom_id)
                continue
            
            raise TypeError(
                f'`custom_id` contains a non `str` element, got: '
                f'{sub_custom_id.__class__.__name__}; {sub_custom_id!r}; custom_id={custom_id!r}.'
            )
    
    else:
        raise TypeError(
            f'`custom_id` can be `str`, (`list`, `set`) of `str`, got '
            f'{custom_id.__class__.__name__}; {custom_id!r}.'
        )
    
    return custom_ids


def _validate_name(name):
    """
    Validates the given name.
    
    Parameters
    ----------
    name : `None`, `str`
        A command's respective name.
    
    Returns
    -------
    name : `None`, `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` is not given as `None` neither as `str`.
    """
    if name is not None:
        name_type = name.__class__
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(
                f'`name` can be `None`, `str`, got {name_type.__name__}; {name!r}.'
            )
    
    return name


def split_and_check_satisfaction(custom_ids, parameter_converters):
    """
    Splits custom id-s to `str` and to `re.Pattern`-s and validates them.
    
    Parameters
    ----------
    custom_ids : `set` of (`str`, `re.Pattern`)
        The custom-ids to split and validate.
    parameter_converters : `tuple` of ``ParameterConverter``
        The parameter converters generated from a component command.
    
    Returns
    -------
    string_custom_ids : `None`, `tuple` of `str`
        String custom ids.
    regex_custom_ids : `None`, `tuple` of ``RegexMatcher``
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


class CustomIdBasedCommand:
    """
    Base class for commands based on `custom_id` matching.
    
    Attributes
    ----------
    _command_function : `async-callable˛
        The command's function to call.
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``SlasherApplicationCommand``
        The parent slasher of the component command.
    _parameter_converters : `tuple` of ``ParameterConverter``
        Parsers to parse command parameters.
    _string_custom_ids : `None`, `tuple` of `str`
        The custom id-s to wait for.
    _regex_custom_ids : `None`, `tuple` of `re.Pattern`.
        Regex pattern to match custom-ids.
    name : `str`
        The component commands name.
        
        Only used for debugging.

    response_modifier : `None`, ``ResponseModifier``
        Modifies values returned and yielded to command coroutine processor.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : tuple of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's command defining parameter's name.
    """
    __slots__ = (
        '_command_function', '_exception_handlers', '_parent_reference', '_parameter_converters', '_regex_custom_ids',
        '_string_custom_ids', 'name', 'response_modifier',
    )
    
    COMMAND_PARAMETER_NAMES = ('command', 'custom_id', 'name', 'allowed_mentions', 'wait_for_acknowledgement')
    
    COMMAND_NAME_NAME = 'name'
    COMMAND_COMMAND_NAME = 'command'
    
    @classmethod
    def from_class(cls, klass):
        """
        Creates a new command instance from the given `klass`.
        
        Parameters
        ----------
        klass : `type`
            The class to create custom id based command from.
        
        Returns
        -------
        self : ``CustomIdBasedCommand``, ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's type is incorrect.
        ValueError
            If any attribute's value is incorrect.
        """
        return create_event_from_class(cls, klass, cls.COMMAND_PARAMETER_NAMES, cls.COMMAND_NAME_NAME,
            cls.COMMAND_COMMAND_NAME)
    
    
    def __new__(cls, func, custom_id, name=None, **kwargs):
        """
        Creates a new custom_id based command instance.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        func : `None`, `async-callable`
            The function used as the command when using the respective slash command.
        custom_id : `str`, (`list`, `set`) of `str`, `tuple` of (`str`, (`list`, `set`) of `str`)
            Custom id to match by the component command.
        name : `None`, `str` = `None`, Optional
            The name of the component command.
        
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
        self : ``CustomIdBasedCommand``, ``Router``
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    def __repr__(self):
        """Returns the command's representation."""
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
        
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            repr_parts.append(', response_modifier')
            repr_parts.append(repr(response_modifier))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    async def __call__(self, client, interaction_event, regex_match):
        """
        Calls the command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        regex_match : `None`, ``RegexMatch``
            The matched regex if applicable.
        """
        return
    

    def __hash__(self):
        """Returns the command's hash value."""
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
        
        response_modifier = self.response_modifier
        if (response_modifier is not None):
            hash_value ^= hash(response_modifier)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two commands are equal."""
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
        
        if self.response_modifier != other.response_modifier:
            return False
        
        return True

    
    def copy(self):
        """
        Copies the command.
        
        Returns
        -------
        new : ``CustomIdBasedCommand``
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
        new.response_modifier = self.response_modifier
        
        return new
    
    
    def error(self, exception_handler=None, *, first=False):
        """
        Registers an exception handler to the command.
        
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
        Registers an exception handler to the command.
        
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
