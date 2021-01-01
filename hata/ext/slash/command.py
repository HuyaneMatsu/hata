# -*- coding: utf-8 -*-
__all__ = ('SlashCommand', 'Slasher')

from ...backend.futures import Task, is_coroutine_generator, WaitTillAll
from ...backend.utils import DOCS_ENABLED
from ...backend.event_loop import LOOP_TIME
from ...backend.analyzer import CallableAnalyzer

from ...discord.client_core import KOKORO, ROLES, CHANNELS
from ...discord.parsers import route_value, EventHandlerBase, InteractionEvent, check_name, Router, route_name
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.embed import EmbedBase
from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake, preconvert_bool
from ...discord.client import Client
from ...discord.user import UserBase, User
from ...discord.role import Role
from ...discord.channel import ChannelBase
from ...discord.preinstanced import ApplicationCommandOptionType
from ...discord.interaction import ApplicationCommandOption, ApplicationCommandOptionChoice, ApplicationCommand


COMMAND_TYPE_GLOBAL = 0
COMMAND_TYPE_NONGLOBAL = 1
COMMAND_TYPE_GUILD = 2

IGNORED_COMMAND_CLEANUP_CYCLE_TIME = 3615.0


def is_only_embed(maybe_embeds):
    """
    Checks whether the given value is a `tuple` or `list` containing only `embed-like`-s.
    
    Parameters
    ----------
    maybe_embeds : (`tuple` or `list`) of `EmbedBase` or `Any`
        The value to check whether is a `tuple` or `list` containing only `embed-like`-s.
    
    Returns
    -------
    is_only_embed : `bool`
    """
    if not isinstance(maybe_embeds, (list, tuple)):
        return False
    
    for maybe_embed in maybe_embeds:
        if not isinstance(maybe_embed, EmbedBase):
            return False
    
    return True


async def process_command_coro(client, interaction_event, show_source, coro):
    """
    Processes a slash command coroutine.
    
    If the coroutine returns or yields a string or an embed like then sends it to the respective channel.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who will send the responses if applicable.
    interaction_event : ``InteractionEvent``
        The respective event to respond on.
    show_source : `bool`
        Whether the source message should be shown.
    coro : `coroutine`
        A coroutine with will send command response.
    
    Raises
    ------
    BaseException
        Any exception raised by `coro`.
    """
    if is_coroutine_generator(coro):
        response_message = None
        response_exception = None
        while True:
            if response_exception is None:
                step = coro.asend(response_message)
            else:
                step = coro.athrow(response_exception)
            
            try:
                response = await step
            except StopAsyncIteration as err:
                # catch `StopAsyncIteration` only if it is a new one.
                if (response_exception is not None) and (response_exception is not err):
                    raise
                
                args = err.args
                if args:
                    response = args[0]
                else:
                    response = None
                break
            except BaseException as err:
                if (response_exception is None) or (response_exception is not err):
                    raise
                
                if isinstance(err, ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # Message's channel deleted; Can we get this?
                            ERROR_CODES.invalid_access, # Client removed.
                            ERROR_CODES.invalid_permissions, # Permissions changed meanwhile; Can we get this?
                            ERROR_CODES.invalid_message_send_user, # User has dm-s disallowed; Can we get this?
                            ERROR_CODES.unknown_interaction, # We times out, do not drop error.
                                ):
                        return
                
                raise
            
            else:
                if (response is None):
                    if interaction_event._responded:
                        request_coro = None
                    else:
                        request_coro = client.interaction_response_message_create(interaction_event,
                            show_source=show_source)
                elif isinstance(response, (str, EmbedBase)) or is_only_embed(response):
                    if interaction_event._responded:
                        request_coro = client.interaction_followup_message_create(interaction_event, response)
                    else:
                        request_coro = client.interaction_response_message_create(interaction_event, response,
                            show_source=show_source)
                else:
                    if interaction_event._responded:
                        request_coro = None
                    else:
                        request_coro = client.interaction_response_message_create(interaction_event,
                            show_source=show_source)
                
                
                if request_coro is None:
                    response_message = None
                    response_exception = None
                else:
                    try:
                        response_message = await request_coro
                    except BaseException as err:
                        response_message = None
                        response_exception = err
                    else:
                        response_exception = None
    
    else:
        response = await coro
    
    if (response is None):
        if interaction_event._responded:
            request_coro = None
        else:
            request_coro = client.interaction_response_message_create(interaction_event, show_source=show_source)
    elif isinstance(response, (str, EmbedBase)) or is_only_embed(response):
        if interaction_event._responded:
            request_coro = client.interaction_followup_message_create(interaction_event, response)
        else:
            request_coro = client.interaction_response_message_create(interaction_event, response,
                show_source=show_source)
    else:
        if interaction_event._responded:
            request_coro = None
        else:
            request_coro = client.interaction_response_message_create(interaction_event, show_source=show_source)
    
    if (request_coro is not None):
        try:
            await request_coro
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted; Can we get this?
                        ERROR_CODES.invalid_access, # client removed.
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile; Can we get this?
                        ERROR_CODES.invalid_message_send_user, # user has dm-s disallowed; Can we get this?
                        ERROR_CODES.unknown_interaction, # we times out, do not drop error.
                            ):
                    return
            
            raise


async def converter_int(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `int`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `int`
        If conversion fails, then returns `None`.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = None
    
    return value


async def converter_str(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `str`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `str`
        If conversion fails, then returns `None`.
    """
    return str(value)


async def converter_bool(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `bool`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `bool`
        If conversion fails, then returns `None`.
    """
    if not isinstance(value, bool):
        value = None
    
    return value


async def converter_snowflake(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to a snowflake.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    snowflake : `None` or ``int``
        If conversion fails, then returns `None`.
    """
    try:
        snowflake = int(value)
    except (TypeError, ValueError):
        snowflake = None
    else:
        if (snowflake < (1<<22)) or (snowflake > ((1<<64)-1)):
            snowflake = None
    
    return snowflake


async def converter_user(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``UserBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    user : `None`, ``User`` or ``Client``
        If conversion fails, then returns `None`.
    """
    user_id = await converter_snowflake(client, value)
    
    if user_id is None:
        user = None
    else:
        try:
            user = await client.user_get(user_id)
        except ConnectionError:
            user = 0
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_user:
                user = None
            else:
                raise
    
    return user


async def converter_role(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``Role`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``Role``
        If conversion fails, then returns `None`.
    """
    role_id = await converter_snowflake(client, value)
    
    if role_id is None:
        role = None
    else:
        role = ROLES.get(role_id)
    
    return role


async def converter_channel(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to ``ChannelBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `Any`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``ChannelBase`` instance
        If conversion fails, then returns `None`.
    """
    channel_id = await converter_snowflake(client, value)
    
    if channel_id is None:
        channel = None
    else:
        channel = CHANNELS.get(channel_id)
    
    return channel

ANNOTATION_TYPE_STR        = 0
ANNOTATION_TYPE_INT        = 1
ANNOTATION_TYPE_BOOL       = 2
ANNOTATION_TYPE_USER       = 3
ANNOTATION_TYPE_USER_ID    = 4
ANNOTATION_TYPE_ROLE       = 5
ANNOTATION_TYPE_ROLE_ID    = 6
ANNOTATION_TYPE_CHANNEL    = 7
ANNOTATION_TYPE_CHANNEL_ID = 8

STR_ANNOTATION_TO_ANNOTATION_TYPE = {
    'str'        : ANNOTATION_TYPE_STR        ,
    'int'        : ANNOTATION_TYPE_INT        ,
    'bool'       : ANNOTATION_TYPE_BOOL       ,
    'user'       : ANNOTATION_TYPE_USER       ,
    'user_id'    : ANNOTATION_TYPE_USER_ID    ,
    'role'       : ANNOTATION_TYPE_ROLE       ,
    'role_id'    : ANNOTATION_TYPE_ROLE_ID    ,
    'channel'    : ANNOTATION_TYPE_CHANNEL    ,
    'channel_id' : ANNOTATION_TYPE_CHANNEL_ID ,
        }

TYPE_ANNOTATION_TO_ANNOTATION_TYPE = {
    str          : ANNOTATION_TYPE_STR     ,
    int          : ANNOTATION_TYPE_INT     ,
    bool         : ANNOTATION_TYPE_BOOL    ,
    UserBase     : ANNOTATION_TYPE_USER    ,
    User         : ANNOTATION_TYPE_USER    ,
    Role         : ANNOTATION_TYPE_ROLE    ,
    ChannelBase  : ANNOTATION_TYPE_CHANNEL ,
        }

ANNOTATION_TYPE_TO_CONVERTER = {
    ANNOTATION_TYPE_STR        : converter_str       ,
    ANNOTATION_TYPE_INT        : converter_int       ,
    ANNOTATION_TYPE_BOOL       : converter_bool      ,
    ANNOTATION_TYPE_USER       : converter_user      ,
    ANNOTATION_TYPE_USER_ID    : converter_snowflake ,
    ANNOTATION_TYPE_ROLE       : converter_role      ,
    ANNOTATION_TYPE_ROLE_ID    : converter_snowflake ,
    ANNOTATION_TYPE_CHANNEL    : converter_channel   ,
    ANNOTATION_TYPE_CHANNEL_ID : converter_snowflake ,
        }

ANNOTATION_TYPE_TO_OPTION_TYPE = {
    ANNOTATION_TYPE_STR        : ApplicationCommandOptionType.STRING  ,
    ANNOTATION_TYPE_INT        : ApplicationCommandOptionType.INTEGER ,
    ANNOTATION_TYPE_BOOL       : ApplicationCommandOptionType.BOOLEAN ,
    ANNOTATION_TYPE_USER       : ApplicationCommandOptionType.USER    ,
    ANNOTATION_TYPE_USER_ID    : ApplicationCommandOptionType.USER    ,
    ANNOTATION_TYPE_ROLE       : ApplicationCommandOptionType.ROLE    ,
    ANNOTATION_TYPE_ROLE_ID    : ApplicationCommandOptionType.ROLE    ,
    ANNOTATION_TYPE_CHANNEL    : ApplicationCommandOptionType.CHANNEL ,
    ANNOTATION_TYPE_CHANNEL_ID : ApplicationCommandOptionType.CHANNEL ,
        }


def parse_annotation_type_and_choice(annotation_value, annotation_name):
    """
    Parses annotation type and choices out from an an annotation value.
    
    Parameters
    ----------
    annotation_value : `str`, `type`, `list`, `dict`
        The annotation's value.
    annotation_name : `str`
        The annotation's name.
    
    Returns
    -------
    annotation_type : `int`
        Internal identifier about the annotation.
    choices : `None` or `dict` of (`int` or `str`, `str`)
        Choices if applicable.
    
    TypeError
        - If `annotation_value` is `list` instance, but it's elements do not match the `tuple` (`str`, `str` or `int`)
            pattern.
        - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
        - If `annotation_value` is unexpected.
    ValueError
        - If `annotation_value` is `str` instance, but not any of the expected ones.
        - If `annotation_value` is `type` instance, but not any of the expected ones.
        - If `choice` amount is out of the expected range [1:10].
        - If a `choice` name is duped.
        - If a `choice` values are mixed types.
    """
    if isinstance(annotation_value, str):
        annotation_value = annotation_value.lower()
        try:
            annotation_type = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Argument `{annotation_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    elif isinstance(annotation_value, type):
        try:
            annotation_type = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Argument `{annotation_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    else:
        if isinstance(annotation_value, list):
            for index, annotation_choice in enumerate(annotation_value):
                if (not isinstance(annotation_choice, tuple)) or (len(annotation_choice) != 2):
                    raise TypeError(f'Argument `{annotation_name}` was given as a `list` annotation, but it\'s element '
                        f'{index} not matches the expected structure: `tuple` (`str`, `str` or `int`), got '
                        f'{annotation_choice!r}.')
        
        elif isinstance(annotation_value, dict):
            annotation_value = list(annotation_value.items())
        else:
            raise TypeError(f'Argument `{annotation_name}` has annotation not set neither as `tuple`, `str`, `type`, '
                f'`list` or `dict`, got {annotation_value.__class__.__name__}.')
        
        choices_length = len(annotation_value)
        if choices_length < 1 or choices_length > 10:
            raise ValueError(f'Argument `{annotation_name}` choice length out of expected range [1:10], got '
                f'{choices_length!r}.')
        
        names = []
        values = []
        
        for index, annotation_choice in enumerate(annotation_value):
            name, value = annotation_choice
            if (not isinstance(name, str)) or (not isinstance(value, (str, int))):
                raise TypeError(f'Argument `{annotation_name}` was given as a `list` or `dict` annotation, but it\'s '
                    f'element {index} not matches the expected structure: `tuple` (`str`, `str` or `int`), got '
                    f'{annotation_choice!r}.')
            
            names.append(name)
            values.append(value)
        
        # Filter dupe names
        length = 0
        dupe_checker = set()
        for name in names:
            dupe_checker.add(name)
            new_length = len(dupe_checker)
            if new_length == length:
                raise ValueError(f'Duped choice name in annotation: `{annotation_name}`.')
            
            length = new_length
        
        # Filter dupe types
        expected_type = None
        for value in values:
            if isinstance(value, str):
                type_ = str
            else:
                type_ = int
            
            if expected_type is None:
                expected_type = type_
                continue
            
            if expected_type is not type_:
                raise ValueError(f'Mixed choice value types in annotation: `{annotation_name}`.')
        
        if expected_type is str:
            annotation_type = ANNOTATION_TYPE_STR
        else:
            annotation_type = ANNOTATION_TYPE_INT
        
        choices = {value:name for value, name in zip(values, names)}
    
    return annotation_type, choices


class ArgumentConverter(object):
    """
    Converter class for choice based converters.
    
    Parameters
    ----------
    choices : `None` or `dict` of (`str` or `int`, `str`)
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    converter : `func`
        The converter to use to convert a value to it's desired type.
    default : `bool`
        Default value of the parameter.
    description : `None` or `str`
        The parameter's description.
    name : `str`
        The parameter's description.
    required : `bool`
        Whether the the parameter is required.
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = ('choices', 'converter', 'default', 'description', 'name', 'required', 'type')

    def __new__(cls, argument):
        """
        Creates a new argument converter from the given argument.
        
        Parameters
        ----------
        argument : ``Argument``
            The argument to create converter from.
        
        Raises
        ------
        TypeError
            - if the `argument` has no annotation.
            - If `annotation_value` is `list` instance, but it's elements do not match the `tuple`
                (`str`, `str` or `int`) pattern.
            - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
            - If `annotation_value` is unexpected.
            - If `annotation` is not `tuple`.
            - If `annotation` 1st element is not `str` instance.
        ValueError
            - If `annotation` is a `tuple`, but it's length is not 2.
            - If `annotation_value` is `str` instance, but not any of the expected ones.
            - If `annotation_value` is `type` instance, but not any of the expected ones.
            - If `choice` amount is out of the expected range [1:10].
            - If a `choice` name is duped.
            - If a `choice` values are mixed types.
            - If `annotation` 1st element's range is out of the expected range [2:100].
        """
        name = argument.name
        if not argument.has_annotation:
            raise TypeError(f'Argument `{name}` has no annotation.')
        
        annotation = argument.annotation
        if not isinstance(annotation, tuple):
            raise TypeError(f'Argument `{name}` is not `tuple` instances, got {annotation.__class__.__name__}.')
            
        annotation_tuple_length = len(annotation)
        if annotation_tuple_length != 2:
            raise ValueError(f'Argument `{name}` has annotation as `tuple`, but it\'s length is not 2, got '
                f'{annotation_tuple_length!r}, {annotation_tuple_length!r}.')
        
        annotation_value, description = annotation
        annotation_type, choices = parse_annotation_type_and_choice(annotation_value, name)
        
        if (description is not None) and (not isinstance(description, str)):
            raise TypeError(f'Argument `{name}` has annotation description is not `str` instance, got '
                f'{description.__class__.__name__}.')
        
        description_length = len(description)
        if description_length < 2 or description_length > 100:
            raise ValueError(f'Argument `{name}` has annotation description\'s length is out of the expected range '
                f'[2:100], got {description_length}; {description!r}.')
        
        if argument.has_default:
            default = argument.default
            required = False
        else:
            default = None
            required = True
        
        self = object.__new__(cls)
        self.choices = choices
        self.converter = ANNOTATION_TYPE_TO_CONVERTER[annotation_type]
        self.default = default
        self.description = description
        self.name = name
        self.required = required
        self.type = annotation_type
        return self
    
    async def __call__(self, client, value):
        """
        Calls the argument converter to convert the given `value` to it's desired state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective ``InteractionEvent``.
        value : `Any`
            ``ApplicationCommandInteractionOption.value``.
        
        Returns
        -------
        passed : `bool`
            Whether the conversion passed.
        value : `None` or ``Any`` instance
            If conversion fails, always returns `None`.
        """
        if value is None:
            if self.required:
                passed = False
            else:
                passed = True
                value = self.default
        else:
            value = await self.converter(client, value)
            if value is None:
                if self.required:
                    passed = False
                else:
                    passed = True
                    value = self.default
            else:
                choices = self.choices
                if choices is None:
                    passed = True
                else:
                    if value in choices:
                        passed = True
                    else:
                        passed = False
                        value = None
        
        return passed, value
    
    def as_option(self):
        """
        Converts the argument to an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        choices = self.choices
        if choices is None:
            option_choices = None
        else:
            option_choices = [ApplicationCommandOptionChoice(name, value) for value, name in choices.items()]
        
        option_type = ANNOTATION_TYPE_TO_OPTION_TYPE[self.type]
        
        return ApplicationCommandOption(self.name, self.description, option_type, required=self.required,
            choices=option_choices)


def generate_argument_parsers(func):
    """
    Parses the given `func`'s arguments.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    argument_parsers : `tuple` of ``ArgumentConverter``
        Argument converters for teh given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only arguments.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
        - If `func` accepts less than `2` arguments.
        - If `func` accepts more than `12` arguments.
        - If `func`'s 0th argument is annotated, but not as ``Client``.
        - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
        - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
            `tuple` (`str`, `str` or `int`) pattern.
        - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
            (`str`, `str` or `int`) pattern.
        - If an argument's `annotation_value` is unexpected.
        - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
    ValueError
        - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
        - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
        - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
        - If an argument's `choice` amount is out of the expected range [1:10].
        - If an argument's `choice` name is duped.
        - If an argument's `choice` values are mixed types.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async() or analyzer.is_async_generator():
        real_analyzer = analyzer
        should_instance = False
    
    elif analyzer.can_instance_to_async_callable() or analyzer.can_instance_to_async_generator():
        real_analyzer = CallableAnalyzer(func.__call__, as_method=True)
        if (not real_analyzer.is_async()) and (not real_analyzer.is_async_generator()):
            raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got '
                f'{func!r}.')
        
        should_instance = True
    
    else:
        raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.')
    
    
    keyword_only_argument_count = real_analyzer.get_non_default_keyword_only_argument_count()
    if keyword_only_argument_count:
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts keyword only arguments.')
    
    if real_analyzer.accepts_args():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts *args.')
    
    if real_analyzer.accepts_kwargs():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts **kwargs.')

    
    arguments = real_analyzer.get_non_reserved_positional_arguments()
    
    argument_count = len(arguments)
    if argument_count < 2:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at least 2 arguments: '
            f'`client` and `interaction_event`, meanwhile it accepts only {argument_count}.')
    
    if argument_count > 12:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at maximum 12 arguments: '
            f', meanwhile it accepts up to {argument_count}.')
    
    client_argument = arguments[0]
    if client_argument.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            'reserved, meanwhile it should not have.')
    
    if client_argument.has_annotation and (client_argument.annotation is not Client):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the client\'s argument slot, '
            f'what is not `{Client.__name__}`.')
    
    
    message_argument = arguments[1]
    if message_argument.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            f'reserved, meanwhile it should not have.')
    
    if message_argument.has_annotation and (message_argument.annotation is not InteractionEvent):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the interaction_event\'s argument '
            f'slot what is not `{InteractionEvent.__name__}`.')
    
    argument_parsers = []
    
    for argument in arguments[2:]:
        argument_parser = ArgumentConverter(argument)
        argument_parsers.append(argument_parser)
    
    argument_parsers = tuple(argument_parsers)
    
    if should_instance:
        func = analyzer.insatnce()
    
    return func, argument_parsers


def normalize_description(description):
    """
    Normalizes a docstrings.
    
    Parameters
    ----------
    description : `str` or `None`
        The docstring to clear.
    
    Returns
    -------
    cleared : `str` or `None`
        The cleared docstring. If `docstring` was given as `None` or is detected as empty, will return `None`.
    """
    if description is None:
        return None
    
    lines = description.splitlines()
    for index in reversed(range(len(lines))):
        line = lines[index]
        line = line.strip()
        if line:
            lines[index] = line
        else:
            del lines[index]
    
    if not lines:
        return None
    
    return ' '.join(lines)


def create_schema(name, description, argument_parsers):
    """
    Creates application schema from processed slash command parameters.
    
    Parameters
    ----------
    name : `str`
        Command name.
    description : `str`
        Command description.
    argument_parsers : `tuple` of ``ArgumentConverter``
    
    Returns
    -------
    schema : ``ApplicationCommand``
    """
    if argument_parsers:
        options = [argument_parser.as_option() for argument_parser in argument_parsers]
    else:
        options = None
    
    return ApplicationCommand(name, description, options=options)



class SlashCommand(object):
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _registered_application_command_ids : `None` or `set` of `int`
        The registered application command ids, which are matched by the command's schema.
    argument_parsers : `tuple` of ``ArgumentConverter``
        Parsers to parse command parameters.
    command : `async-callable˛
        The command's function to call.
    description : `str`
        Application command description. It\'s length can be in range [2:100].
    guild_ids : `None` or `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    name : `str`
        Application command name. It\'s length can be in range [3:32].
    schema : ``ApplicationCommand``
        The application command schema of the slash command.
    show_source : `bool`
        Whether the source message should be shown when using the command.
    """
    __slots__ = ('_registered_application_command_ids', 'argument_parsers', 'command', 'description', 'guild_ids',
        'is_global', 'name', 'schema', 'show_source')
    
    def register_application_command_id(self, application_command_id):
        """
        Registers an application command's identifier to the ``SlashCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            registered_application_command_ids = self._registered_application_command_ids = set()
        
        registered_application_command_ids.add(application_command_id)
    
    def unregister_application_command_id(self, application_command_id):
        """
        Unregisters an application command's identifier from the ``SlashCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            registered_application_command_ids.discard(application_command_id)
            if not registered_application_command_ids:
                self._registered_application_command_ids = None
    
    def unregister_guild_id(self, guild_id):
        """
        Unregisters an application command's guild's identifier from the ``SlashCommand`.
        
        Parameters
        ----------
        guild_id : `int`
            The application command's guild's identifier.
        """
        guild_ids = self.guild_ids
        if guild_ids is not None:
            guild_ids.discard(guild_id)
    
    
    @classmethod
    def from_class(cls, klass, kwargs=None):
        """
        The method use when creating a ``SlashCommand`` instance from a class.
        
        Extra `kwargs` are supported as well for special the use cases.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether when responding the source message should be shown. Defaults to `True`.


        kwargs, `None` or `dict` of (`str`, `Any`) items, Optional
            Additional parameters arguments. Defaults to `None`.
            
            The expected keyword arguments are the following:
            
            - guild
            - is_global
            - name
            - show_source
        
        Returns
        -------
        self : ``SlashCommand`` or ``Router``
        
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_source` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `tuple`, `set`) of
                (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `12` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:10].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [3:32].
        """
        klass_type = klass.__class__
        if not issubclass(klass_type, type):
            raise TypeError(f'Expected `type` instance, got {klass_type.__name__}.')
        
        name = getattr(klass, 'name', None)
        if name is None:
            name = klass.__name__
        
        command = getattr(klass, 'command', None)
        if command is None:
            while True:
                command = getattr(klass, name, None)
                if (command is not None):
                    break
                
                raise ValueError('`command` class attribute is missing.')
        
        description = getattr(klass, 'description', None)
        if description is None:
            description = klass.__doc__
        
        is_global = getattr(klass, 'is_global', None)
        guild = getattr(klass, 'guild', None)
        show_source = getattr(klass, 'show_source', None)
        
        if (kwargs is not None) and kwargs:
            if (description is None):
                description = kwargs.pop('description', None)
            else:
                try:
                    del kwargs['description']
                except KeyError:
                    pass
            
            if (is_global is None):
                is_global = kwargs.pop('is_global', None)
            else:
                try:
                    del kwargs['is_global']
                except KeyError:
                    pass
            
            if (show_source is None):
                show_source = kwargs.pop('show_source', None)
            else:
                try:
                    del kwargs['show_source']
                except KeyError:
                    pass
            
            if (guild is None):
                guild = kwargs.pop('guild', None)
            else:
                try:
                    del kwargs['guild']
                except KeyError:
                    pass
            
            if kwargs:
                raise TypeError(f'`{cls.__name__}.from_class` did not use up some kwargs: `{kwargs!r}`.')
        
        return cls(command, name, description, show_source, is_global, guild)
    
    @classmethod
    def from_kwargs(cls, command, name, kwargs):
        """
        Called when a slash command is created before adding it..
        
        Parameters
        ----------
        command : `async-callable`
            The async callable added as the command itself.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The name to be used instead of the passed `command`'s.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additional keyword arguments.
            
            The expected keyword arguments are the following:
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            - show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
        
        Returns
        -------
        self : ``Command`` or ``Router``
        
        Raises
        ------
        TypeError
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_source` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `tuple`, `set`) of
                (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `12` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:10].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [3:32].
        """
        if (kwargs is None) or (not kwargs):
            description = None
            show_source = None
            is_global = None
            guild = None
        else:
            description = kwargs.pop('description', None)
            show_source = kwargs.pop('show_source', None)
            is_global = kwargs.pop('is_global', None)
            guild = kwargs.pop('checks', None)
            
            if kwargs:
                raise TypeError(f'type `{cls.__name__}` not uses: `{kwargs!r}`.')
        
        return cls(command, name, description, show_source, is_global, guild)
    
    @classmethod
    def _check_maybe_route(cls, variable_name, variable_value, route_to, validator):
        """
        Helper class of ``SlashCommand`` parameter routing.
        
        Parameters
        ----------
        variable_name : `str`
            The name of the respective variable
        variable_value : `Any`
            The respective value to route maybe.
        route_to : `int`
            The value how much times the routing should happen. by default should be given as `0` if no routing was
            done yet.
        validator : `callable` or `None`
            A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
        
        Returns
        -------
        processed_value : `Any`
            Processed value returned by the `validator`. If routing is happening, then a `tuple` of those values is
            returned.
        route_to : `int`
            The amount of values to route to.
        
        Raises
        ------
        ValueError
            Value is routed but to a bad count amount.
        BaseException
            Any exception raised by `validator`.
        """
        if (variable_value is not None) and isinstance(variable_value, tuple):
            route_count = len(variable_value)
            if route_count == 0:
                processed_value = None
            elif route_count == 1:
                variable_value = variable_value[0]
                if variable_value is ...:
                    variable_value = None
                
                if validator is None:
                    processed_value = variable_value
                else:
                    processed_value = validator(variable_value)
            else:
                if route_to == 0:
                    route_to = route_count
                elif route_to == route_count:
                    pass
                else:
                    raise ValueError(f'{cls.__class__.__name__} `{variable_name}` is routed to `{route_count}`, '
                        f'meanwhile something else is already routed to `{route_to}`.')
                
                if validator is None:
                    processed_value = variable_value
                else:
                    processed_values = []
                    for value in variable_value:
                        if (value is not ...):
                            value = validator(value)
                        
                        processed_values.append(value)
                    
                    processed_value = tuple(processed_values)
        
        else:
            if validator is None:
                processed_value = variable_value
            else:
                processed_value = validator(variable_value)
        
        return processed_value, route_to
    
    @staticmethod
    def _validate_show_source(show_source):
        """
        Validates the given `show_source` value.
        
        Parameters
        ----------
        show_source : `None` or `bool`
            The `show_source` value to validate.
        
        Returns
        -------
        show_source : `bool`
            The validated `show_source` value.
        
        Raises
        ------
        TypeError
            If `show_source` was not given as `bool` instance.
        """
        if show_source is None:
            show_source = True
        else:
            show_source = preconvert_bool(show_source, 'show_source')
        
        return show_source
    
    @staticmethod
    def _validate_is_global(is_global):
        """
        Validates the given `is_global` value.
        
        Parameters
        ----------
        is_global : `None` or `bool`
            The `is_global` value to validate.
        
        Returns
        -------
        is_global : `bool`
            The validated `is_global` value.
        
        Raises
        ------
        TypeError
            If `is_global` was not given as `bool` instance.
        """
        if is_global is None:
            is_global = False
        else:
            is_global = preconvert_bool(is_global, 'is_global')
        
        return is_global
    
    @staticmethod
    def _validate_1_guild(guild):
        """
        Validates 1 guild value.
        
        Parameters
        ----------
        guild : ``Guild`` or `int`
            The guild value to validate.
        
        Returns
        -------
        guild_id : `int`
            Validated guild value converted to `int` instance.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int` instance.
        ValueError
            If `guild` is an integer out of uint64 value range.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(f'`guild` was not given neither as `{Guild.__class__.__name__}`, neither as `int` '
                f'instance, got {guild.__class__.__name__}.')
        
        return guild_id
    
    @classmethod
    def _validate_guild(cls, guild):
        """
        Validates the given `guild` value.
        
        Parameters
        ----------
        guild : `None`, `int`, ``Guild``, (`list`, `set`) of (`int`, ``Guild``
            The `is_global` value to validate.
        
        Returns
        -------
        guild_ids : `None` or `set` of `int`
            The validated `guild` value.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
        ValueError
            - If `guild` is given as an empty container.
            - If `guild` is or contains an integer out of uint64 value range.
        """
        if guild is None:
            guild_ids = None
        else:
            guild_ids = set()
            if isinstance(guild, (list, set)):
                for guild_value in guild:
                    guild_id = cls._validate_1_guild(guild_value)
                    guild_ids.add(guild_id)
            else:
                guild_id = cls._validate_1_guild(guild)
                guild_ids.add(guild_id)
            
            if not guild_ids:
                raise ValueError(f'`guild` cannot be given as empty container, got {guild!r}.')
        
        return guild_ids
    
    @staticmethod
    def _validate_name(name):
        """
        Validates the given name.
        
        Parameters
        ----------
        name : `None` or `str`
            A command's respective name.
        
        Returns
        -------
        name : `None` or `str`
            The validated name.
        
        Raises
        ------
        TypeError
            - If `name` is not given as `str` instance.
        ValueError
            - If `name` length is out of the expected range [1:32].
        """
        if name is not None:
            name_type = name.__class__
            if name_type is str:
                pass
            elif issubclass(name_type, str):
                name = str(name)
            else:
                raise TypeError(f'`name` can be only given as `None` or as `str` instance, got {name_type.__name__}; '
                    f'{name!r}.')
            
            name_length = len(name)
            if name_length < 3 or name_length > 32:
                raise ValueError(f'`name` length is out of the expected range [3:32], got {name_length!r}; {name!r}.')
        
        return name
    
    @staticmethod
    def _generate_description_from(command, description):
        """
        Generates description from the command and it's maybe given description.
        
        Parameters
        ----------
        command : `str`
            The command's function.
        description : `Any`
            The command's description.
        
        Returns
        -------
        description : `str`
            The generated description.
        
        Raises
        ------
        TypeError
            If `str` description could not be detected.
        ValueError
            If `description` length is out of range [2:100].
        """
        if description is None:
            description = getattr(command, '__doc__', None)
        
        if (description is None) or (not isinstance(description, str)):
            raise TypeError(f'`description` or `command.__doc__` is not given or is given as `None`')
            
        description = normalize_description(description)
        
        if description is None:
            description_length = 0
        else:
            description_length = len(description)
        
        if description_length < 2 or description_length > 100:
            raise ValueError(f'`description` length is out of the expected range [2:100], got {description_length!r}; '
                f'{description!r}.')
        
        return description
    
    def __new__(cls, command, name, description, show_source, is_global, guild):
        """
        Creates a new ``SlashCommand`` instance with the given parameters.
        
        Parameters
        ----------
        command : `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
            Description to use instead of the function's docstring.
        show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            Whether when responding the source message should be shown. Defaults to `True`.
        is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
            To which guild(s) the command is bound to.
        
        Raises
        ------
        TypeError
            - If a value is routed but to a bad count amount.
            - If `show_source` was not given as `None` or `bool` instance.
            - If `is_global` was not given as 7None` or `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `12` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:10].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [3:32].
        """
        # Check for routing
        route_to = 0
        name, route_to = cls._check_maybe_route('name', name, route_to, cls._validate_name)
        description, route_to = cls._check_maybe_route('description', description, route_to, None)
        show_source, route_to = cls._check_maybe_route('show_source', show_source, route_to, cls._validate_show_source)
        is_global, route_to = cls._check_maybe_route('is_global', is_global, route_to, cls._validate_is_global)
        guild_ids, route_to = cls._check_maybe_route('guild', guild, route_to, cls._validate_guild)
        
        
        if route_to:
            name = route_name(command, name, route_to)
            
            for sub_name in name:
                sub_name_length = len(sub_name)
                if sub_name_length < 3 or sub_name_length > 32:
                    raise ValueError(f'`name` length is out of the expected range [3:32], got {sub_name_length!r}; '
                        f'{name!r}.')
            
            default_description = cls._generate_description_from(command, None)
            show_source = route_value(show_source, route_to)
            is_global = route_value(is_global, route_to)
            guild_ids = route_value(guild_ids, route_to)
            
            description = [
                cls._generate_description_from(command, description)
                    if ((description is None) or (description is not default_description)) else default_description
                for description in description]
        else:
            name = check_name(command, name)
            
            sub_name_length = len(name)
            if sub_name_length < 3 or sub_name_length > 32:
                raise ValueError(f'`name` length is out of the expected range [3:32], got {sub_name_length!r}; '
                    f'{name!r}.')
            
            description = cls._generate_description_from(command, description)
        
        command, argument_parsers = generate_argument_parsers(command)
        
        if route_to:
            router = []
            
            for name, description, show_source, is_global, guild_ids in zip(
                name, description, show_source, is_global, guild_ids):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                        f'guild={guild!r}')
                
                schema = create_schema(name, description, argument_parsers)
                
                self = object.__new__(cls)
                self.show_source = show_source
                self.argument_parsers = argument_parsers
                self.description = description
                self.name = name
                self.command = command
                self.guild_ids = guild_ids
                self.is_global = is_global
                self.schema = schema
                self._registered_application_command_ids = None
                
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                    f'guild={guild!r}')
        
            schema = create_schema(name, description, argument_parsers)
            
            self = object.__new__(cls)
            self.show_source = show_source
            self.argument_parsers = argument_parsers
            self.description = description
            self.name = name
            self.command = command
            self.guild_ids = guild_ids
            self.is_global = is_global
            self.schema = schema
            self._registered_application_command_ids = None
            
            return self
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slash command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        """
        parameters = []
        
        parameter_relation = {}
        options = interaction_event.interaction.options
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for argument_parser in self.argument_parsers:
            value = parameter_relation.get(argument_parser.name)
            
            passed, parameter = await argument_parser(client, value)
            if not passed:
                return
            
            parameters.append(parameter)
        
        coro = self.command(client, interaction_event, *parameters)
        await process_command_coro(client, interaction_event, self.show_source, coro)
    
    def exhaust_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command and removes them.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            while registered_application_command_ids:
                yield registered_application_command_ids.pop()
            
            self._registered_application_command_ids = None


class Slasher(EventHandlerBase):
    """
    Slash command processor.
    
    Attributes
    ----------
    _ignored_missing_commands : `dict` of (`int`, `float`) items
        The id-s of the commands, which should be ignored as keys. The values are the monotonic time when their id
        should uncached.
    _ignored_missing_commands_handle : `None` or ``TimerWeakHandle``
        Handle for clearing ``_ignored_missing_commands``.
    _sync_task : `None` or ``Task``
        The actual sync task of the slasher to avoid parallel syncing.
    guild_requests_done : `set` of `int`
        The done guild requests. Each element of the set is the respective ``Guild``'s id.
        
        If the slasher finished syncing global commands, then it will have an element `0` present as well.
    registered_commands : `list` of ``SlashCommand``
        Registered command schemas to the slash command processer.
    registered_commands_by_id : `dict` of (`int`, ``SlashCommand``) items
        Registered commands by id.
    
    Class Attributes
    ----------------
    __event_name__ : `str` = 'interaction_create'
        Tells for the ``EventDescriptor`` that ``Slasher`` is a `interaction_create` event handler.
    SUPPORTED_TYPES : `tuple` (``SlashCommand``, )
        Tells to ``eventlist`` what exact types the ``Slasher`` accepts.
    
    Notes
    -----
    ``Slasher`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_ignored_missing_commands', '_ignored_missing_commands_handle', '_sync_task',
        'guild_requests_done', 'registered_commands', 'registered_commands_by_id', )
    
    __event_name__ = 'interaction_create'
    
    SUPPORTED_TYPES = (SlashCommand, )
    
    def __new__(cls):
        """
        Creates a new slash command processer with the given parameters.
        """
        self = object.__new__(cls)
        self.registered_commands_by_id = {}
        self.guild_requests_done = set()
        self.registered_commands = []
        self._ignored_missing_commands = {}
        self._ignored_missing_commands_handle = None
        self._sync_task = None
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
        try:
            command = await self.try_get_command_by_id(client, interaction_event)
        except ConnectionError:
            return
        except BaseException as err:
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if command is None:
            await self._command_missing(client, interaction_event)
        else:
            await command(client, interaction_event)
    
    def add_ignored_missing_command_by_id(self, application_command_id):
        """
        Adds a command id, what should be ignored from now on from calling ``._command_missing`` and
        ``._command_missing_id`` on it for at least one hour.
        
        It is expected to be called after a success full ``Client.application_command_global_delete`` or
        ``Client.application_command_guild_delete`` call.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's id.
        """
        self._ignored_missing_commands[application_command_id] = LOOP_TIME()
        
        if self._ignored_missing_commands_handle is None:
            self._ignored_missing_commands_handle = \
                KOKORO.call_later_weak(IGNORED_COMMAND_CLEANUP_CYCLE_TIME, self._ignored_missing_commands_cleanup)
    
    def _ignored_missing_commands_cleanup(self):
        """
        Clears up the `application_command_id`-s from ``._ignored_missing_commands``, which were added before 1 hour
        scope.
        """
        ignored_missing_commands = self._ignored_missing_commands
        
        to_clear = []
        time_limit = LOOP_TIME()-3600.0
        
        for application_command_id, addition_time in ignored_missing_commands.items():
            if addition_time <= time_limit:
                to_clear.append(application_command_id)
        
        for application_command_id in to_clear:
            try:
                del ignored_missing_commands[application_command_id]
            except KeyError:
                pass
        
        
        if ignored_missing_commands:
            handle = KOKORO.call_later_weak(IGNORED_COMMAND_CLEANUP_CYCLE_TIME, self._ignored_missing_commands_cleanup)
        else:
            handle = None
        
        self._ignored_missing_commands_handle = handle
    
    
    async def _command_missing(self, client, interaction_event):
        """
        called when a command is missing.
        
        Deletes the interaction event's respective command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client instance, who received the interaction event.
        interaction_event : ``InteractionEvent``
            The invoked interaction.
        """
        application_command_id = interaction_event.interaction.id
        
        guild = interaction_event.guild
        if (guild is not None):
            guild_id = guild.id
            # We will get passed by this check only if we already did a guild request.
            if guild_id in self.guild_requests_done:
                try:
                    await client.application_command_guild_delete(guild, application_command_id)
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        # Try next time
                        return
                    
                    if isinstance(err, DiscordException) and  err.code == ERROR_CODES.unknown_application_command:
                        pass
                    else:
                        await client.events.error(client, f'{self!r}._command_missing', err)
                        return
                else:
                    self.add_ignored_missing_command_by_id(application_command_id)
                    return
            
        try:
            await client.application_command_global_delete(application_command_id)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # Try next time
                return
            if isinstance(err, DiscordException) and  err.code == ERROR_CODES.unknown_application_command:
                pass
            else:
                await client.events.error(client, f'{self!r}._command_missing', err)
                return
        
        self.add_ignored_missing_command_by_id(application_command_id)
        return
    
    async def _command_missing_id(self, client, guild, application_command_id):
        """
        Called when a missing command is detected but only by it's id.
        
        Deletes the respective application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client instance, who received the interaction event.
        guild : `None` or ``Guild``
            The respective guild if the command is guild bound.
        application_command_id : `int`
            The application command's id.
        """
        if guild is None:
            coro = await client.application_command_global_delete(application_command_id)
        else:
            coro = await client.application_command_guild_delete(guild, application_command_id)
        
        try:
            await coro
        except ConnectionError:
            # Try next time
            return
        except DiscordException as err:
            # NANI ?
            if err.code == ERROR_CODES.unknown_application_command:
                pass
            else:
                raise
        else:
            self.add_ignored_missing_command_by_id(application_command_id)
            return
    
    async def try_get_command_by_id(self, client, interaction_event):
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
            command = self.registered_commands_by_id[interaction_id]
        except KeyError:
            pass
        else:
            return command
        
        detected_missing_ids = None
        
        # First request guild commands
        guild = interaction_event.guild
        if (guild is not None):
            guild_id = guild.id
            if guild_id not in self.guild_requests_done:
                application_commands = await client.application_command_guild_get_all(guild)
                
                # We did it, so mark it as done.
                self.guild_requests_done.add(guild_id)
                
                # Match nonglobal and guild bound commands
                for application_command in application_commands:
                    for command in self.registered_commands:
                        if ( (command.type == COMMAND_TYPE_NONGLOBAL) or \
                             ((command.type == COMMAND_TYPE_GUILD) and (guild_id in command.guild_ids))) \
                                and (command.schema == application_command):
                            
                            self.registered_commands_by_id[application_command.id] = command
                            command.register_application_command_id(application_command.id)
                            break
                    else:
                        if detected_missing_ids is None:
                            detected_missing_ids = []
                        detected_missing_ids.append(application_command.id)
                
                # Cleanup if applicable
                if (detected_missing_ids is not None):
                    for application_command_id in detected_missing_ids:
                        Task(self._command_missing_id(client, guild, application_command_id), KOKORO)
                    
                    detected_missing_ids = None
                    
                # Try to get it again
                try:
                    command = self.registered_commands_by_id[interaction_id]
                except KeyError:
                    pass
                else:
                    return command
        
        if 0 in self.guild_requests_done:
            return None
        
        # Global check
        application_commands = await client.application_command_global_get_all()
        
        for application_command in application_commands:
            for command in self.registered_commands:
                if (command.type == COMMAND_TYPE_GLOBAL) and (command.schema == application_command):
                    self.registered_commands_by_id[application_command.id] = command
                    command.register_application_command_id(application_command.id)
                    break
            else:
                if detected_missing_ids is None:
                    detected_missing_ids = []
                detected_missing_ids.append(application_command.id)
        
        if (detected_missing_ids is not None):
            for application_command_id in detected_missing_ids:
                Task(self._command_missing_id(client, guild, application_command_id), KOKORO)
            
            detected_missing_ids = None
        
        return client.registered_commands_by_id.get(interaction_id)
    
    
    def _maybe_register_guild_command(self, application_command, guild_id):
        """
        Tries to register the given guild bound (can be nonglobal) application command to the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just added application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        for command in self.registered_commands:
            if command.type == COMMAND_TYPE_NONGLOBAL:
                pass
            elif command.type == COMMAND_TYPE_GUILD:
                if (guild_id not in command.guild_ids):
                    continue
            else:
                continue
            
            if command.schema == application_command:
                self.registered_commands_by_id[application_command.id] = command
                command.register_application_command_id(application_command.id)
                break
    
    def _maybe_unregister_guild_command(self, application_command, guild_id):
        """
        Tries to unregister the given guild bound (can be nonglobal) application command from the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just deleted application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        for command in self.registered_commands:
            if command.type == COMMAND_TYPE_NONGLOBAL:
                pass
            elif command.type == COMMAND_TYPE_GUILD:
                if (guild_id not in command.guild_ids):
                    continue
            else:
                continue
            
            if not command.schema == application_command:
                continue
            
            try:
                self.registered_commands_by_id[application_command.id]
            except KeyError:
                pass
            
            command.unregister_application_command_id(application_command.id)
            command.unregister_guild_id(guild_id)
    
    def __setevent__(self, func, name, description=None, show_source=None, is_global=None, guild=None):
        """
        Adds a slash command.
        
        Parameters
        ----------
        func : `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description to use instead of the function's docstring.
        show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether when responding the source message should be shown. Defaults to `True`.
        is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`), Optional
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``)), Optional
            To which guild(s) the command is bound to.
        
        Returns
        -------
        func : ``SlashCommand``
             The created or added command.
        
        Raises
        ------
        TypeError
            - If `show_source` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` argument.
            - If `func` accepts more than `12` argument.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:10].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [3:32].
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlashCommand):
            self._add_command(func)
            return func
        
        command = SlashCommand(func, name, description, show_source, is_global, guild)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return command
        
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add is as a slash command.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
            
            The expected attributes of the given `klass` are the following:
            
            - description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
                Description of the command.
            - command : `async-callable`
                If no description was provided, then the class's `.__doc__` will be picked up.
            - guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                    `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
                To which guild(s) the command is bound to.
            - is_global : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
                Whether when responding the source message should be shown. Defaults to `True`.
        
        Returns
        -------
        func : ``SlashCommand``
             The created or added command.
         
        Raises
        ------
        TypeError
            - If `klass` was not given as `type` instance.
            - If `kwargs` was not given as `None` and not all of it's items were used up.
            - If a value is routed but to a bad count amount.
            - If `show_source` was not given as `bool` instance.
            - If `global_` was not given as `bool` instance.
            - If `guild` was not given neither as `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``)
            - If `func` is not async callable, neither cannot be instanced to async.
            - If `func` accepts keyword only arguments.
            - If `func` accepts `*args`.
            - If `func` accepts `**kwargs`.
            - If `func` accepts less than `2` arguments.
            - If `func` accepts more than `12` arguments.
            - If `func`'s 0th argument is annotated, but not as ``Client``.
            - If `func`'s 1th argument is annotated, but not as ``InteractionEvent``.
            - If `name` was not given neither as `None` or `str` instance.
            - If an argument's `annotation_value` is `list` instance, but it's elements do not match the
                `tuple` (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is `dict` instance, but it's items do not match the
                (`str`, `str` or `int`) pattern.
            - If an argument's `annotation_value` is unexpected.
            - If an argument's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
            - If `description` or `func.__doc__` is not given or is given as `None` or empty string.
            - If `is_global` and `guild` contradicts each other.
        ValueError
            - If `guild` is or contains an integer out of uint64 value range.
            - If an argument's `annotation` is a `tuple`, but it's length is out of the expected range [0:2].
            - If an argument's `annotation_value` is `str` instance, but not any of the expected ones.
            - If an argument's `annotation_value` is `type` instance, but not any of the expected ones.
            - If an argument's `choice` amount is out of the expected range [1:10].
            - If an argument's `choice` name is duped.
            - If an argument's `choice` values are mixed types.
            - If `description` length is out of range [2:100].
            - If `guild` is given as an empty container.
            - If `name` length is out of the expected range [3:32].
            -  If an already added command's name conflicts with the added one's.
        """
        command = SlashCommand.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return command
    
    def _add_command(self, command):
        """
        Adds a slash command to the ``Slasher``.
        
        Parameters
        ---------
        command : ``SlashCommand``
            The command to add.
        
        Raises
        ------
        ValueError
            If an already added command's name conflicts with the added one's.
        """
        # Check for intersection commands
        if command.is_global:
            command_iterator = self.iter_global_commands()
        else:
            guild_ids = command.guild_ids
            if guild_ids:
                command_iterator = self.iter_guild_commands_intersection(guild_ids)
            else:
                command_iterator = self.iter_non_global_commands()
        
        for added_command in command_iterator:
            if added_command.name == command.name:
                raise ValueError(f'The added command: `{command!r}`\s name conflicts with an already added '
                    f'command\'s: `{added_command!r}`')
        
        # Add command
        self.registered_commands.append(command)
    
    def iter_global_commands(self):
        """
        Iterates over the ``Slasher``'s global commands.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        command : ``SlashCommand``
        """
        for command in self.registered_commands:
            if command.is_global:
                yield command
    
    def iter_non_global_commands(self):
        """
        Iterates over the ``Slasher``'s non global commands.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        command : ``SlashCommand``
        """
        for command in self.registered_commands:
            if (not command.is_global) and (command.guild_ids is None):
                yield command
        
    def iter_guild_commands(self, guild_id):
        """
        Iterates over the ``Slasher``'s guild bound commands.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's id.
        
        Yields
        ------
        command : ``SlashCommand``
        """
        for command in self.registered_commands:
            command_guild_ids = command.guild_ids
            if (command_guild_ids is not None) and (guild_id in command_guild_ids):
                yield command
    
    def iter_guild_commands_intersection(self, guild_ids):
        """
        Iterates over the ``Slasher``'s guild bound commands.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Parameters
        ----------
        guild_ids : `container` of `int`
            The respective guilds' id.
        
        Yields
        ------
        command : ``SlashCommand``
        """
        for command in self.registered_commands:
            command_guild_ids = command.guild_ids
            if (command_guild_ids is not None) and command_guild_ids.intersection(guild_ids):
                yield command
    
    def _remove_command(self, func, name=None):
        """
        tries to the given command from the ``Slasher``.
        
        Parameters
        ----------
        func : ``Command``
            The command to remove.
        name : `None` or  `str`, Optional
            The command's respective name. Defaults to `None`.
        """
        if isinstance(func, SlashCommand):
            try:
                self.registered_commands.remove(func)
            except ValueError:
                pass
        else:
            for index, registered_command in enumerate(self.registered_commands):
                if (registered_command.command == func) and (True if name is None else (registered_command.name==name)):
                    func = registered_command
                    del registered_command[index]
            else:
                return
        
        registered_commands_by_id = self.registered_commands_by_id
        for application_command_id in func.exhaust_application_command_ids:
            try:
                del registered_commands_by_id[application_command_id]
            except KeyError:
                pass
    
    def __delevent__(self, func, name, **kwargs):
        """
        A method to remove a command by itself, or by it's function and name combination if defined.
        
        Parameters
        ----------
        func : ``SlashCommand``, ``Router``, `async-callable` or instantiable to `async-callable`
            The command to remove.
        name : `None` or `str`
            The command's name to remove.
        **kwargs : Keyword Arguments
            Other keyword only arguments are ignored.
        """
        if isinstance(func, Router):
            for sub_func in func:
                self._remove_command(sub_func, name)
        else:
            self._remove_command(func, name)
    
    async def do_initial_sync(self, client):
        """
        Syncs the slash commands with the client.
        
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
        sync_task = self._sync_task
        if sync_task is None:
            self._sync_task = sync_task = Task(self._do_initial_sync(client), KOKORO)
        
        try:
            return await sync_task
        finally:
            self._sync_task = None
    
    
    async def _do_initial_sync(self, client):
        """
        Syncs the slash commands with the client. This method is the internal coroutine of the ``.do_initial_sync``
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
        global_commands = []
        non_global_commands = []
        guild_commands_per_guild = {}
        
        for command in self.registered_commands:
            if command.is_global:
                global_commands.append(command)
                continue
            
            guild_ids = command.guild_ids
            if guild_ids is None:
                non_global_commands.append(command)
                continue
            
            for guild_id in guild_ids:
                try:
                    guild_commands = guild_commands_per_guild[guild_id]
                except KeyError:
                    guild_commands = guild_commands_per_guild[guild_id] = []
                
                guild_commands.append(command)
        
        tasks = []
        if global_commands and (0 not in self.guild_requests_done):
            task = Task(self._sync_global_commands(client, global_commands), KOKORO)
            tasks.append(task)
        
        for guild_id, guild_commands in guild_commands_per_guild.items():
            if (guild_id not in self.guild_requests_done):
                task = Task(self._sync_guild_commands(client, guild_id, guild_commands, non_global_commands), KOKORO)
                tasks.append(task)
        
        done, pending = await WaitTillAll(tasks, KOKORO)
        
        success = True
        for future in done:
            if not future.result():
                success = False
        
        return success
    
    async def _sync_global_commands(self, client, commands):
        """
        Syncs the global commands off the ``Slasher``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        commands : `list` of ``SlashCommand``
            A list of global slash commands of the client.
        
        Returns
        -------
        success : `bool`
            Whether the commands where synced with success.
        """
        try:
            application_commands = await client.application_command_global_get_all()
        except BaseException as err:
            # No internet connection
            if isinstance(err, ConnectionError):
                return False
            
            await client.events.error(client, f'{self!r}._sync_global_commands', err)
            return False
        
        to_remove = []
        missing = set(commands)
        
        for application_command in application_commands:
            for command in commands:
                if command.schema == application_command:
                    self.registered_commands_by_id[application_command.id] = command
                    command.register_application_command_id(application_command.id)
                    missing.discard(command)
                    break
            else:
                to_remove.append(application_command)
        
        tasks = []
        # First do update tasks!
        for application_command_index in reversed(range(len(to_remove))):
            application_command = to_remove[application_command_index]
            for command in missing:
                if application_command.name == command.name:
                    break
            else:
                continue
            
            del to_remove[application_command_index]
            missing.discard(command)
            
            task = Task(self._update_global_command(client, application_command, command), KOKORO)
            tasks.append(task)
        
        for application_command in to_remove:
            task = Task(self._delete_global_command(client, application_command), KOKORO)
            tasks.append(task)
        
        for command in missing:
            task = Task(self._create_global_command(client, command), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillAll(tasks, KOKORO)
        
        success = True
        for future in done:
            if not future.result():
                success = False
        
        if success:
            self.guild_requests_done.add(0)
            
        return success
    
    async def _update_global_command(self, client, application_command, command):
        """
        Updates the given application command.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        application_command : ``ApplicationCommand``
            The respective application command.
        command : ``SlashCommand``
            The slash command to update the application command to.

        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            await client.application_command_global_edit(application_command, command.schema)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                return await self._create_global_command(client, command)
            
            await client.events.error(client, f'{self!r}._delete_global_command', err)
            return False
        
        self.registered_commands_by_id[application_command.id] = command
        command.register_application_command_id(application_command.id)
        return True
    
    
    async def _delete_global_command(self, client, application_command):
        """
        Deletes the given global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was deleted successfully.
        """
        try:
            await client.application_command_global_delete(application_command)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted
                pass
            else:
                await client.events.error(client, f'{self!r}._delete_global_command', err)
                return False
        
        self.add_ignored_missing_command_by_id(application_command.id)
        return True
    
    async def _create_global_command(self, client, command):
        """
        Adds the given command to the client as a global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        command : ``SlashCommand``
            The respective command to add.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            application_command = await client.application_command_global_create(command.schema)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(client, f'{self!r}._add_global_command', err)
            return False
        
        self.registered_commands_by_id[application_command.id] = command
        command.register_application_command_id(application_command.id)
        return True
    
    async def _sync_guild_commands(self, client, guild_id, guild_commands, non_global_commands):
        """
        Syncs a guild's commands off the ``Slasher``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier number.
        guild_commands : `list` of ``SlashCommand``
            A list of guild specific slash commands of the client.
        non_global_commands : `list` of ``SlashCommand``
            A list of non global slash commands of the client.
        
        Returns
        -------
        success : `bool`
            Whether the commands where synced with success.
        """
        try:
            application_commands = await client.application_command_guild_get_all(guild_id)
        except BaseException as err:
            # No internet connection
            if isinstance(err, ConnectionError):
                return False
            
            await client.events.error(client, f'{self!r}._sync_guild_commands', err)
            return False
        
        to_remove = []
        missing = set(guild_commands)
        
        for application_command in application_commands:
            for command in guild_commands:
                if command.schema == application_command:
                    self.registered_commands_by_id[application_command.id] = command
                    command.register_application_command_id(application_command.id)
                    missing.discard(command)
                    break
            else:
                to_remove.append(application_command)

        tasks = []
        # First do update tasks!
        for application_command_index in reversed(range(len(to_remove))):
            application_command = to_remove[application_command_index]
            for command in missing:
                if application_command.name == command.name:
                    break
            else:
                continue
            
            del to_remove[application_command_index]
            missing.discard(command)
            
            task = Task(self._update_guild_command(client, guild_id, application_command, command), KOKORO)
            tasks.append(task)
        
        # Second step at our case is checking for non global commands.
        for application_command_index in reversed(range(len(to_remove))):
            application_command = to_remove[application_command_index]
            for command in non_global_commands:
                if command.schema == application_command:
                    self.registered_commands_by_id[application_command.id] = command
                    command.register_application_command_id(application_command.id)
                    
                    del to_remove[application_command_index]
        
        for application_command in to_remove:
            task = Task(self._delete_guild_command(client, guild_id, application_command), KOKORO)
            tasks.append(task)
        
        for command in missing:
            task = Task(self._create_guild_command(client, guild_id, command), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillAll(tasks, KOKORO)
        
        success = True
        for future in done:
            if not future.result():
                success = False
        
        if success:
            self.guild_requests_done.add(guild_id)
        
        return success
    
    async def _update_guild_command(self, client, guild_id, application_command, command):
        """
        Updates the given guild bound application command.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        application_command : ``ApplicationCommand``
            The respective application command.
        command : ``SlashCommand``
            The slash command to update the application command to.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            await client.application_command_guild_edit(guild_id, application_command, command.schema)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                return await self._create_guild_command(client, guild_id, command)
            
            await client.events.error(client, f'{self!r}._delete_global_command', err)
            return False
        
        self.registered_commands_by_id[application_command.id] = command
        command.register_application_command_id(application_command.id)
        return True
    
    async def _delete_guild_command(self, client, guild_id, application_command):
        """
        Deletes the given application command.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The command's guild's identifier.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was deleted successfully.
        """
        try:
            await client.application_command_guild_delete(guild_id, application_command)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted
                pass
            else:
                await client.events.error(client, f'{self!r}._delete_guild_command', err)
                return False
        
        self.add_ignored_missing_command_by_id(application_command.id)
        return True
    
    async def _create_guild_command(self, client, guild_id, command):
        """
        Creates a new guild bound application command.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The command's guild's identifier.
        command : ``SlashCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            application_command = await client.application_command_guild_create(guild_id, command.schema)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(client, f'{self!r}._create_guild_command', err)
            return False
        
        self.registered_commands_by_id[application_command.id] = command
        command.register_application_command_id(application_command.id)
        return True


del EventHandlerBase
del DOCS_ENABLED
