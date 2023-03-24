__all__ = ('SlashCommandParameterConversionError', 'SlasherCommandError', 'SlasherSyncError')

from random import choice

from scarletio import CallableAnalyzer, include
from scarletio import copy_docs

from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.interaction import InteractionType


SlashCommand = include('SlashCommand')
Slasher = include('Slasher')

class SlasherCommandError(Exception):
    """
    Base class for slash command internal errors.
    """
    pass

    @property
    def pretty_repr(self):
        """
        Returns the pretty representation of the exception.
        
        Returns
        -------
        representation : `str`
        """
        return ''


class SlashCommandParameterConversionError(SlasherCommandError):
    """
    Exception raised when a command's parameter's parsing fails.
    
    Attributes
    ----------
    _pretty_repr : `None`, `str`
        generated pretty representation of the exception.
    _repr : `None`, `str`
        The generated error message.
    parameter_name : `None`, `str`
        The parameter's name, which failed to be parsed.
    received_value : `None`, `str`
        The parameter's received value.
    excepted_type : `None`, `str`
        The parameter's expected type's name.
    expected_values : `None`, `list` of `Any`
        Expected values.
    """
    def __init__(self, parameter_name, received_value, excepted_type, expected_values):
        """
        Creates a new ``SlashCommandParameterConversionError`` with the given parameters.
        
        Parameters
        ----------
        parameter_name : `None`, `str`
            The parameter's name, which failed to be parsed.
        received_value : `None`, `str`
            The parameter's received value.
        excepted_type : `None`, `str`
            The parameter's expected type's name.
        expected_values : `None`, `list` of `Any`
            Expected values.
        """
        self.parameter_name = parameter_name
        self.received_value = received_value
        self.excepted_type = excepted_type
        self.expected_values = expected_values
        self._repr = None
        self._pretty_repr = None
        Exception.__init__(self, parameter_name, received_value, excepted_type, expected_values)
    
    def __repr__(self):
        """Returns the representation of the parameter conversion error."""
        repr_ = self._repr
        if repr_ is None:
            repr_ = self._create_repr()
        
        return repr_

    def _create_repr(self):
        """
        Creates the representation of the parsing syntax error.
        
        Returns
        -------
        repr_ : `str`
            The representation of the syntax error.
        """
        repr_parts = [self.__class__.__name__]
        
        parameter_name = self.parameter_name
        if (parameter_name is not None):
            repr_parts.append('\n')
            repr_parts.append('parameter name: ')
            repr_parts.append(repr(parameter_name))
        
        excepted_type = self.excepted_type
        if (excepted_type is not None):
            repr_parts.append(
                '\n'
                'expected type: '
            )
            repr_parts.append(excepted_type)
        
        expected_values = self.expected_values
        if (expected_values is not None):
            repr_parts.append(
                '\n'
                'expected value(s):'
            )
            
            index = 0
            limit = len(expected_values)
            while True:
                value = expected_values[index]
                index += 1
                
                repr_parts.append(repr(value))
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(
            '\n'
            'received value: '
        )
        received_value = self.received_value
        if (received_value is None):
            repr_parts.append('N/A')
        else:
            repr_parts.append(repr(received_value))
        
        repr_ = ''.join(repr_parts)
        self._repr = repr_
        return repr_
    
    
    @property
    @copy_docs(SlasherCommandError.pretty_repr)
    def pretty_repr(self):
        pretty_repr = self._pretty_repr
        if pretty_repr is None:
            pretty_repr = self._create_pretty_repr()
        
        return pretty_repr
    
    
    def _create_pretty_repr(self):
        """
        Creates the pretty representation of the parameter conversion error.
        
        Returns
        -------
        repr_ : `str`
            The representation of the parameter conversion error.
        """
        repr_parts = ['Parameter conversion failed\n']
        
        parameter_name = self.parameter_name
        if (parameter_name is not None):
            repr_parts.append('\n')
            repr_parts.append('Name: `')
            repr_parts.append(parameter_name)
            repr_parts.append('`')
        
        excepted_type = self.excepted_type
        if (excepted_type is not None):
            repr_parts.append(
                '\n'
                'Excepted type: `'
            )
            repr_parts.append(excepted_type)
            repr_parts.append('`')
    
        
        expected_values = self.expected_values
        if (expected_values is not None):
            repr_parts.append(
                '\n'
                'Expected value(s):'
            )
            
            for expected_value in expected_values:
                repr_parts.append('\n- `')
                repr_parts.append(str(expected_value))
                repr_parts.append('`')
        
        repr_parts.append(
            '\n'
            'Received: '
        )
        received_value = self.received_value
        if (received_value is None):
            repr_parts.append('N/A')
        else:
            repr_parts.append('`')
            repr_parts.append(repr(received_value))
            repr_parts.append('`')
        
        pretty_repr = ''.join(repr_parts)
        self._pretty_repr = pretty_repr
        return pretty_repr



ERROR_MESSAGES = [
    (
       'Exception occurred meanwhile processing your interaction.\n'
       'Our highly educated Cirno-s are already working on the problem.'
    ), (
        'Your command\'s execution failed.\n'
        'We are putting Reimu to investigate about the issue.'
    ), (
        'The command died out.\n'
        'Maybe Izaoyi love-shop has some antidote.'
    ), (
        'Something went wrong.\n'
        'Do you need driver license for broom riding?'
    ),
]

def default_slasher_random_error_message_getter():
    """
    Returns random error message getter of ``Slasher``.
    
    Returns
    -------
    error_message : `str`
    """
    return choice(ERROR_MESSAGES)


def _validate_random_error_message_getter(random_error_message_getter):
    """
    Validates the given `random_error_message_getter`. It should accept no parameters and return a string.
    
    Parameters
    ----------
    random_error_message_getter : `callable`
        The random message getter to validate.
    
    Raises
    ------
    TypeError
        - If `random_error_message_getter` is not callable.
        - If `random_error_message_getter` is not async.
        - If `random_error_message_getter` excepts not `0` parameters.
    """
    analyzer = CallableAnalyzer(random_error_message_getter)
    if analyzer.is_async():
        raise TypeError(
            f'`random_error_message_getter` cannot be async, got {random_error_message_getter!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if (min_ > 0):
        raise TypeError(
            f'A `random_error_message_getter` should accept `0` parameters, meanwhile '
            f'{random_error_message_getter!r} accepts between `{min_}` and `{max_}`.'
        )


async def default_slasher_exception_handler(client, interaction_event, command, exception):
    """
    Default ``Slasher`` exception handler.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    interaction_event : ``InteractionEvent``
        The received interaction event.
    command : ``SlashCommand``, ``ComponentCommand``
        The command, which raised.
    exception : `BaseException`
        The occurred exception.
    
    Returns
    -------
    handled : `bool`
        Whether the error handler handled the exception.
    """
    if isinstance(exception, SlasherCommandError):
        forward = exception.pretty_repr
        render = False
        create_new_message = False
    
    elif isinstance(exception, DiscordException) and (exception.status == 500):
        forward = None
        render = True
        create_new_message = False
    
    elif (interaction_event.type is InteractionType.application_command) and interaction_event.is_unanswered():
        forward = client.slasher._random_error_message_getter()
        render = True
        create_new_message = False
    
    elif (interaction_event.type is InteractionType.message_component) and interaction_event.is_unanswered():
        forward = client.slasher._random_error_message_getter()
        render = True
        create_new_message = True
        
        try:
            await client.interaction_component_acknowledge(interaction_event)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                forward = None
            
            elif (
                isinstance(err, DiscordException) and
                (
                    (err.status == 500) or
                    (err.code == ERROR_CODES.unknown_interaction)
                )
            ):
                forward = None
            
            else:
                raise
    
    else:
        forward = None
        render = True
        create_new_message = False
    
    
    if (forward is not None):
        if create_new_message:
            function = type(client).interaction_followup_message_create
        else:
            function = type(client).interaction_response_message_create
        
        try:
            await function(
                client,
                interaction_event,
                forward,
                show_for_invoking_user_only = True,
            )
        except BaseException as err:
            if isinstance(err, ConnectionError):
                pass
            
            elif (
                isinstance(err, DiscordException) and
                (
                    (err.status == 500) or
                    (err.code == ERROR_CODES.unknown_interaction)
                )
            ):
                pass
            
            else:
                raise
    
    if render:
        await _render_application_command_exception(client, command, exception)
    
    return True


async def _render_application_command_exception(client, command, exception):
    """
    Renders interaction command exception.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    command : ``SlashCommand``, ``ComponentCommand``
        The command, which raised.
    exception : `BaseException`
        The occurred exception.
    """
    await client.events.error(client, f'`Slasher` while calling `{command!r}`', exception)


async def handle_command_exception(entity, client, interaction_event, exception):
    """
    handles slash command exception.
    
    This function is a coroutine.

    Parameters
    ----------
    entity : ``ComponentCommand``, ``Slasher``, ``SlashCommand``, ``SlashCommandCategory``,
            ``SlashCommandFunction``, ``SlashCommandParameterAutoCompleter``
        The entity to iterate it's exception handlers.
    client : ``Client``
        The respective client.
    interaction_event : ``InteractionEvent``
        The received interaction event.
    exception : `BaseException`
        The occurred exception.
    """
    for exception_handler in _iter_exception_handlers(entity):
        try:
            handled = await exception_handler(client, interaction_event, entity, exception)
        except GeneratorExit:
            raise
        
        except BaseException as err:
            await client.events.error(client, 'handle_command_exception', err)
            return
        
        if handled:
            return
    
    if not isinstance(exception, SlasherCommandError):
        await _render_application_command_exception(client, entity, exception)


def test_exception_handler(exception_handler):
    """
    Tests whether the given exception handler accepts the expected amount of parameters.
    
    Parameters
    ----------
    exception_handler : `CoroutineFunction`
        A function, which handles an exception and returns whether handled it.
        
        The following parameters are passed to it:
        
        +-------------------+-------------------------------------------------------------------------------+
        | Name              | Type                                                                          |
        +===================+===============================================================================+
        | client            | ``Client``                                                                    |
        +-------------------+-------------------------------------------------------------------------------+
        | interaction_event | ``InteractionEvent``                                                          |
        +-------------------+-------------------------------------------------------------------------------+
        | command           | ``ComponentCommand``, ``SlashCommand``,                                       |
        |                   | ``SlashCommandFunction``, ``SlashCommandCategory``,                           |
        |                   | ``SlashCommandParameterAutoCompleter``                                        |
        +-------------------+-------------------------------------------------------------------------------+
        | exception         | `BaseException`                                                               |
        +-------------------+-------------------------------------------------------------------------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | handled           | `bool`    |
        +-------------------+-----------+
    
    Raises
    ------
    TypeError
        - If `exception_handler` accepts bad amount of parameters.
        - If `exception_handler` is not a coroutine function.
    """
    analyzer = CallableAnalyzer(exception_handler)
    if not analyzer.is_async():
        raise TypeError(
            f'`exception_handler` can be `async` function, got {exception_handler!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 4:
        raise TypeError(
            f'`exception_handler` should accept `4` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got {exception_handler!r}.'
        )
    
    if min_ != 4:
        if max_ < 4:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`exception_handler` should accept `4` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got {exception_handler!r}.'
                )


def _register_exception_handler(parent, first, exception_handler):
    """
    Registers an exception handler to the respective entity. This function is wrapped inside of
    `functools.partial` with it's `parent` and `first` parameters.
    
    Parameters
    ----------
    parent : ``Slasher``, ``SlashCommand`, ``SlashCommandCategory``, ``ComponentCommand``,
            ``SlashCommandFunction``, ``SlashCommandParameterAutoCompleter``
        The slasher to register the exception handler to.
    first : `bool`
        Whether the exception handler should run first.
    exception_handler : `CoroutineFunction`
        Exception handler to register.
    
    Returns
    -------
    exception_handler : `CoroutineFunction`
    
    Raises
    ------
    RuntimeError
        If `exception_handler` is given as `None`.
    """
    if (exception_handler is None):
        raise RuntimeError('`exception_handler` cannot be `None`.')
    
    return parent._register_exception_handler(exception_handler, first)


def _iter_exception_handlers(entity):
    """
    Iterates the given entity's exception handlers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    entity : ``ComponentCommand``, ``Slasher``, ``SlashCommand``, ``SlashCommandCategory``,
            ``SlashCommandFunction``, ``SlashCommandParameterAutoCompleter``
        The entity to iterate it's exception handlers.
    
    Yields
    ------
    exception_handler : `CoroutineFunction`
    """
    while True:
        exception_handlers = entity._exception_handlers
        if (exception_handlers is not None):
            yield from exception_handlers
        
        if isinstance(entity, Slasher):
            break
        
        parent_reference = entity._parent_reference
        if parent_reference is None:
            break
        
        entity = parent_reference()
        if entity is None:
            break


class SlasherSyncError(BaseException):
    """
    Raised when syncing an application command or it's permission fails.
    
    The main purpose of the exception is to include the entity in context within the traceback.
    
    Attributes
    ----------
    entity: ``SlashCommand``
        The entity, who's sync failed.
    """
    def __init__(self, entity, err):
        """
        Creates a new slasher sync error exception.
        
        Parameters
        ----------
        entity: ``SlashCommand``
            The entity, who's sync failed.
        err : ``BaseException``
            Source exception.
        """
        self.entity = entity
        BaseException.__init__(self, entity)
        self.__cause__ = err
