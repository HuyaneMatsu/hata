# -*- coding: utf-8 -*-
__all__ = ('SlashCommand', 'Slasher')
from threading import current_thread

from ...backend.futures import Task, is_coroutine_generator, WaitTillAll
from ...backend.analyzer import CallableAnalyzer
from ...backend.event_loop import EventThread
from ...backend.utils import WeakReferer

from ...discord.client_core import KOKORO, ROLES, CHANNELS
from ...discord.parsers import route_value, EventHandlerBase, InteractionEvent, check_name, Router, route_name, \
    _EventHandlerManager
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

def raw_name_to_display(raw_name):
    """
    Converts the given raw application command name and converts it to it's display name.
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return raw_name.lower().replace('_', '-')


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
                            ERROR_CODES.cannot_message_user, # User has dm-s disallowed; Can we get this?
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
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed; Can we get this?
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
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `int`
        If conversion fails, then returns `None`.
    """
    try:
        value = int(value)
    except ValueError:
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
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `str`
        If conversion fails, then returns `None`.
    """
    return value

BOOL_TABLE = {
    str(True) : True,
    str(False): False,
        }

async def converter_bool(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to `bool`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `bool`
        If conversion fails, then returns `None`.
    """
    return BOOL_TABLE.get(value)


async def converter_snowflake(client, value):
    """
    Converter ``ApplicationCommandInteractionOption`` value to a snowflake.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    snowflake : `None` or ``int``
        If conversion fails, then returns `None`.
    """
    try:
        snowflake = int(value)
    except ValueError:
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
    value : `str`
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
    value : `str`
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
    value : `str`
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

# `int` Discord fields are broken and they are refusing to fix it, use string instead.
# Reference: https://github.com/discord/discord-api-docs/issues/2448
ANNOTATION_TYPE_TO_OPTION_TYPE = {
    ANNOTATION_TYPE_STR        : ApplicationCommandOptionType.STRING  ,
    ANNOTATION_TYPE_INT        : ApplicationCommandOptionType.STRING  ,
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
        
        name = raw_name_to_display(name)
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
        value : `str`
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
            option_choices = [ApplicationCommandOptionChoice(name, str(value)) for value, name in choices.items()]
        
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
        Argument converters for the given `func` in order.
    
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


class SlashCommand(object):
    """
    Class to wrap an application command providing interface for ``Slasher``.
    
    Attributes
    ----------
    _command : `None` or ``SlashCommandFunction``
        The command of the slash command.
    _registered_application_command_ids : `None` or `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    _schema : `None` or ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    _sub_commands  : `None` or `dict` of (`str`, ``SlashCommandFunction`` or ``SlashSubCommand``) items
        Sub-commands of the slash command.
        
        Mutually exclusive with the ``._command`` parameter.
    description : `str`
        Application command description. It\'s length can be in range [2:100].
    guild_ids : `None` or `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    name : `str`
        Application command name. It's length can be in range [3:32].
    
    Notes
    -----
    ``SlashCommand`` instances are weakreferable.
    """
    __slots__ = ('__weakref__', '_command', '_registered_application_command_ids', '_schema', '_sub_commands',
        'description', 'guild_ids', 'is_global', 'name', )
    
    def _register_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Registers an application command's identifier to the ``SlashCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        guild_id : `int`
            The guild where the application command is in.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            registered_application_command_ids = self._registered_application_command_ids = {}
        
        registered_application_command_ids[guild_id] = application_command_id
    
    def _unregister_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Unregisters an application command's identifier from the ``SlashCommand`.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id, where the application command is in.
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            try:
                maybe_application_command_id = registered_application_command_ids[guild_id]
            except KeyError:
                pass
            else:
                if maybe_application_command_id == application_command_id:
                    del registered_application_command_ids[guild_id]
                    
                    if not registered_application_command_ids:
                        self._registered_application_command_ids = None
    
    def _pop_command_ids_for(self, guild_id):
        """
        Pops the given application command id from the command for the respective guild.
        
        Parameters
        ----------
        guild_id : `int`
            A guild's identifier.
        
        Returns
        -------
        application_command_id : `int`
            The popped application command's identifier. Returns `0` if nothing is matched.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            application_command_id = 0
        else:
            application_command_id = registered_application_command_ids.pop(guild_id, 0)
        
        return application_command_id
    
    def _exhaust_application_command_ids(self):
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
                guild_id, application_command_id = registered_application_command_ids.popitem()
                yield application_command_id
            
            self._registered_application_command_ids = None
    
    def _iter_sync_ids(self):
        """
        Iterates over all the respective sync ids of the command. If the command is a guild bound command, then will
        iterate over it's guild's id-s.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        sync_id : `int`
        """
        if self.is_global:
            yield SYNC_ID_GLOBAL
            return
        
        guild_ids = self.guild_ids
        if guild_ids is None:
            yield SYNC_ID_NON_GLOBAL
            return
        
        yield from guild_ids
    
    def _iter_guild_ids(self):
        """
        Iterates over all the guild identifiers used by the command.
        
        Yields
        ------
        guild_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            for sync_id in registered_application_command_ids:
                if sync_id > (1<<22):
                    yield sync_id
    
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
            - is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
                Whether the slash command is global. Defaults to `False`.
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
                If was not defined, or was defined as `None`, the class's name will be used.
            - show_source : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
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
        self : ``SlashCommand``
        
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
            - If `name` length is out of the expected range [1:32].
        """
        klass_type = klass.__class__
        if not issubclass(klass_type, type):
            raise TypeError(f'Expected `type` instance, got {klass_type.__name__}.')
        
        name = getattr(klass, 'name', None)
        if name is None:
            name = klass.__name__
        
        command = getattr(klass, 'command', None)
        if command is None:
            command = getattr(klass, name, None)
        
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
            - is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            - name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            - show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
        
        Returns
        -------
        self : ``SlashCommand``
        
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
            - If `name` length is out of the expected range [1:32].
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
        variable_value : `str`
            The respective value to route maybe.
        route_to : `int`
            The value how much times the routing should happen. by default should be given as `0` if no routing was
            done yet.
        validator : `callable` or `None`
            A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
        
        Returns
        -------
        processed_value : `str`
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
            If `show_source` was not given as `None` nor as `bool` instance.
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
            If `is_global` was not given as `None` nor as `bool` instance.
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
            If `name` is not given as `None` neither as `str` instance.
        ValueError
            If `name` length is out of the expected range [1:32].
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
            if name_length < 1 or name_length > 32:
                raise ValueError(f'`name` length is out of the expected range [1:32], got '
                    f'{name_length!r}; {name!r}.')
        
        return name
    
    @staticmethod
    def _generate_description_from(command, description):
        """
        Generates description from the command and it's maybe given description.
        
        Parameters
        ----------
        command : `None` or `callable`
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
            - If `str` description could not be detected.
            - If both `command` and `description` are `None`.
        ValueError
            If `description` length is out of range [2:100].
        """
        if description is None:
            if command is None:
                raise TypeError(f'`description` is a required parameter if `command` is given as `None`.')
            
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
        command : `None` or `async-callable`
            The function used as the command when using the respective slash command.
        name : `str`, `None`, `tuple` of (`str`, `Ellipsis`, `None`)
            The command's name if applicable. If not given or if given as `None`, the `func`'s name will be use
            instead.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`)
            Description to use instead of the function's docstring.
        show_source : `None`, `bool` or `tuple` of (`bool`, `Ellipsis`)
            Whether when responding the source message should be shown. Defaults to `True`.
        is_global : `None`, `bool` or `tuple` of (`None`, `bool`, `Ellipsis`)
            Whether the slash command is global. Defaults to `False`.
        guild : `None`, ``Guild``,  `int`, (`list`, `set`) of (`int`, ``Guild``) or \
                `tuple` of (`None`, ``Guild``,  `int`, `Ellipsis`, (`list`, `set`) of (`int`, ``Guild``))
            To which guild(s) the command is bound to.
        
        Returns
        -------
        self : ``SlashCommand``
        
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
            - If `name` length is out of the expected range [1:32].
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
            if sub_name_length < 1 or sub_name_length > 32:
                raise ValueError(f'`name` length is out of the expected range [1:32], '
                    f'got {sub_name_length!r}; {name!r}.')
            
            description = cls._generate_description_from(command, description)
        
        if command is None:
            argument_parsers = None
        else:
            command, argument_parsers = generate_argument_parsers(command)
        
        if route_to:
            router = []
            
            for name, description, show_source, is_global, guild_ids in zip(
                name, description, show_source, is_global, guild_ids):
                
                if is_global and (guild_ids is not None):
                    raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                        f'guild={guild!r}')
                
                name = raw_name_to_display(name)
                
                if (command is None):
                    command_function = None
                    sub_commands = {}
                else:
                    command_function = SlashCommandFunction(command, argument_parsers, name, description, show_source)
                    sub_commands = None
                
                self = object.__new__(cls)
                self._command = command_function
                self._sub_commands = sub_commands
                self.description = description
                self.guild_ids = guild_ids
                self.is_global = is_global
                self.name = name
                self._schema = None
                self._registered_application_command_ids = None
                router.append(self)
            
            return Router(router)
        else:
            if is_global and (guild_ids is not None):
                raise TypeError(f'`is_guild` and `guild` contradict each other, got is_global={is_global!r}, '
                    f'guild={guild!r}')
            
            name = raw_name_to_display(name)
            
            if (command is None):
                sub_commands = {}
                command_function = None
            else:
                command_function = SlashCommandFunction(command, argument_parsers, name, description, show_source)
                sub_commands = None
            
            self = object.__new__(cls)
            self._command = command_function
            self._sub_commands = sub_commands
            self.description = description
            self.guild_ids = guild_ids
            self.is_global = is_global
            self.name = name
            self._schema = None
            self._registered_application_command_ids = None
            return self
    
    def __repr__(self):
        """returns the slash command's representation."""
        result = ['<', self.__class__.__name__, ' name=', repr(self.name), ' type=']
        
        guild_ids  = self.guild_ids
        if guild_ids is None:
            if self.is_global:
                type_name = 'global'
            else:
                type_name = 'non-global'
        else:
            type_name = 'guild bound'
        
        result.append(type_name)
        
        if (guild_ids is not None):
            result.append(', guild_ids=')
            result.append(repr(guild_ids))
            
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        """Returns the slash command's name."""
        return self.name
    
    async def __call__(self, client, interaction_event):
        """
        Calls the slash command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        options = interaction_event.interaction.options
        
        command = self._command
        if (command is not None):
            await command(client, interaction_event, options)
            return
        
        if (options is None) or (len(options) != 1):
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            return
        
        await sub_command(client, interaction_event, option.options)
    
    def get_schema(self):
        """
        Returns an application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        schema = self._schema
        if schema is None:
            schema = self._schema = self.as_schema()
        
        return schema
    
    def as_schema(self):
        """
        Creates a new application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        command = self._command
        if command is None:
            sub_commands = self._sub_commands
            options = [sub_command.as_option() for sub_command in sub_commands.values()]
        else:
            argument_parsers = command._argument_parsers
            if argument_parsers:
                options = [argument_parser.as_option() for argument_parser in argument_parsers]
            else:
                options = None
        
        return ApplicationCommand(self.name, self.description, options=options)
    
    def as_sub(self):
        """
        Returns the slash command as a sub-command or sub-category.
        
        Returns
        -------
        new : ``SlashCommandFunction`` or ``SlashCommandCategory``
        """
        command = self._command
        if command is not None:
            return command
        
        return SlashCommandCategory(self)
        
    def copy(self):
        """
        Copies the slash command.
        
        Returns
        -------
        new : ``ApplicationCommand``
        """
        command = self._command
        if (command is not None):
            command = command.copy()
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            sub_commands = {category_name: category.copy() for category_name, category in sub_commands.items()}
        
        guild_ids = self.guild_ids
        if (guild_ids is not None):
            guild_ids = guild_ids.copy()
        
        new = object.__new__(type(self))
        new._command = command
        new._sub_commands = sub_commands
        new._registered_application_command_ids = None
        new._schema = None
        new.description = self.description
        new.guild_ids = guild_ids
        new.is_global = self.is_global
        new.name = self.name
        
        if (sub_commands is not None):
            parent_reference = None
            for sub_command in sub_commands.values():
                if isinstance(sub_command, SlashCommandCategory):
                    if parent_reference is None:
                        parent_reference = WeakReferer(new)
                    sub_command._parent_reference = parent_reference
        
        return new
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands or sub-categories to the slash command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        
        Raises
        ------
        RuntimeError
            The ``SlashCommand`` is not a category.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        return _EventHandlerManager(self)
    
    def __setevent__(self, func, name, description=None, show_source=None, is_global=None, guild=None):
        """
        Adds a sub-command under the slash command.
        
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
        self : ``SlashCommand``
        
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
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
        """
        if self._command is not None:
            raise RuntimeError(f'The {self.__class__.__name__} is not a category.')
        
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, type(self)):
            self._add_command(func)
            return self
        
        command = type(self)(func, name, description, show_source, is_global, guild)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command or sub-category.
        
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
        self : ``SlashCommand``
         
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
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` is not a category.
            - The ``SlashCommand`` reached the maximal amount of children.
        """
        command = type(self).from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def _add_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Raises
        ------
        RuntimeError
            The ``SlashCommand`` reached the maximal amount of children.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == 10 and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children (10).')
        
        sub_commands[command.name] = command.as_sub()
        self._schema = None

class SlashCommandFunction(object):
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _argument_parsers : `tuple` of ``ArgumentConverter``
        Parsers to parse command parameters.
    _command : `async-callable˛
        The command's function to call.
    description : `str`
        The slash command's description.
    name : `str`
        The name of the slash command. It's length can be in range [1:32].
    show_source : `bool`
        Whether the source message should be shown when using the command.
    """
    __slots__ = ('_argument_parsers', '_command', 'category', 'description', 'name', 'show_source')
    
    def __new__(cls, command, argument_parsers, name, description, show_source):
        """
        Creates a new ``SlashCommandFunction`` instance with the given parameters-
        
        Parameters
        ----------
        command : `async-callable`
            The command's function to call.
        argument_parsers : `tuple` of ``ArgumentConverter``
            Parsers to parse command parameters.
        name : `str`
            The name of the slash command.
        description : `str`
            The slash command's description.
        show_source : `bool`
            Whether the source message should be shown when using the command.
        """
        self = object.__new__(cls)
        self._command = command
        self._argument_parsers = argument_parsers
        self.show_source = show_source
        self.description = description
        self.name = name
        return self
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command function.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the function.
        """
        parameters = []
        
        parameter_relation = {}
        if (options is not None):
            for option in options:
                parameter_relation[option.name] = option.value
        
        for argument_parser in self._argument_parsers:
            value = parameter_relation.get(argument_parser.name)
            
            passed, parameter = await argument_parser(client, value)
            if not passed:
                return
            
            parameters.append(parameter)
        
        coro = self._command(client, interaction_event, *parameters)
        await process_command_coro(client, interaction_event, self.show_source, coro)
    
    def as_option(self):
        """
        Returns the slash command function as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        argument_parsers = self._argument_parsers
        if argument_parsers:
            options = [argument_parser.as_option() for argument_parser in argument_parsers]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.SUB_COMMAND,
            options=options)
    
    def copy(self):
        """
        Copies the slash command function.
        
        They are not mutable, so just returns itself.
        
        Returns
        -------
        self : ``SlashCommandFunction``
        """
        return self


class SlashCommandCategory(object):
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _sub_commands : `dict` of (`str`, ``SlashCommandFunction``) items
        The sub-commands of the category.
    _parent_reference : `None` or ``WeakReferer`` to ``SlashCommand
        The parent slash command of the category if any.
    description : `str`
        The slash command's description.
    name : `str`
        The name of the slash sub-category.
    """
    __slots__ = ('_sub_commands', '_parent_reference', 'description', 'name')
    
    def __new__(cls, slash_command):
        """
        Creates a new ``SlashCommandCategory`` instance with the given parameters.
        
        Parameters
        ----------
        slash_command : ``SlashCommand``
            The parent slash command.
        """
        self = object.__new__(cls)
        self.name = slash_command.name
        self.description = slash_command.description
        self._sub_commands = {}
        self._parent_reference = WeakReferer(slash_command)
        return self
    
    async def __call__(self, client, interaction_event, options):
        """
        Calls the slash command category.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        options : `None` or `list` of ``InteractionEventChoice``
            Options bound to the category.
        """
        if (options is None) or len(options) != 1:
            return
        
        option = options[0]
        
        try:
            sub_command = self._sub_commands[option.name]
        except KeyError:
            return
        
        await sub_command(client, interaction_event, option.options)
    
    def as_option(self):
        """
        Returns the slash command category as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        sub_commands = self._sub_commands
        if sub_commands:
            options = [sub_command.as_option() for sub_command in sub_commands]
        else:
            options = None
        
        return ApplicationCommandOption(self.name, self.description, ApplicationCommandOptionType.SUB_COMMAND_GROUP,
            options=options)
    
    def copy(self):
        """
        Copies the slash command category.
        
        Returns
        -------
        new : ``SlashCommandCategory``
        """
        sub_commands = {category_name: category.copy() for category_name, category in self._sub_commands.items()}
        
        new = object.__new__(type(self))
        new._sub_commands = sub_commands
        new.description = self.description
        new.name = self.name
        new._parent_reference = None
        return new
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands under the sub-category.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)
    
    def __setevent__(self, func, name, description=None, show_source=None, is_global=None, guild=None):
        """
        Adds a sub-command under the slash category.
        
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
        self : ``SlashCommandCategory``
        
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
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
        """
        if isinstance(func, Router):
            func = func[0]
        
        if isinstance(func, SlashCommand):
            self._add_command(func)
            return self
        
        command = SlashCommand(func, name, description, show_source, is_global, guild)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def __setevent_from_class__(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
        
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
        self : ``SlashCommandCategory``
         
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
            - If `name` length is out of the expected range [1:32].
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
        """
        command = SlashCommand.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        self._add_command(command)
        return self
    
    def _add_command(self, command):
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
            - Cannot add anymore sub-category under sub-categories.
        """
        sub_commands = self._sub_commands
        if len(sub_commands) == 10 and (command.name not in sub_commands):
            raise RuntimeError(f'The {self.__class__.__name__} reached the maximal amount of children (10).')
        
        as_sub = command.as_sub()
        if isinstance(as_sub, type(self)):
            raise RuntimeError('Cannot add anymore sub-category under sub-categories.')
        
        sub_commands[command.name] = as_sub
        
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                parent._schema = None

SYNC_ID_GLOBAL = 0
SYNC_ID_MAIN = 1
SYNC_ID_NON_GLOBAL = 2

class Slasher(EventHandlerBase):
    """
    Slash command processor.
    
    Attributes
    ----------
    _sync_should : `set` of `int`
        Set of guild id-s to sync.
    _sync_tasks : `dict` of (`int, `Task`) items
        A dictionary of guilds, which are in sync at the moment.
    _sync_done : `set` of `int`
        A set of guild id-s which are synced.
    _sync_done_commands : `dict` of (`int`, `list` of ``SlashCommand``) items
        The synced commands, where the dictionary keys are their respective guild's id and the values are a list of
        bound commands.
    _sync_should_commands : `dict` of (`int`, `tuple` (`bool`, `list` of ``SlashCommand``)) items
        The synced commands, where the dictionary keys are their respective guild's id and the values are a tuple of 2
        elements, where the 0th is whether the command was added and the 1th is the command itself.
    command_id_to_command : `dict` of (`int`, ``SlashCommand``) items
        A dictionary where the keys are application command id-s and the keys are their respective command.
        
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
    __slots__ = ('__weakref__', '_sync_should', '_sync_tasks', '_sync_done', '_sync_done_commands',
        '_sync_should_commands', 'command_id_to_command')
    
    __event_name__ = 'interaction_create'
    
    SUPPORTED_TYPES = (SlashCommand, )
    
    def __new__(cls):
        """
        Creates a new slash command processer.
        """
        self = object.__new__(cls)
        self._sync_should = set()
        self._sync_tasks = {}
        self._sync_done = set()
        self._sync_done_commands = {}
        self._sync_should_commands = {}
        
        self.command_id_to_command = {}
        
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
            command = await self._try_get_command_by_id(client, interaction_event)
        except ConnectionError:
            return
        except BaseException as err:
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        if command is not None:
            await command(client, interaction_event)
    
    
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
        Breaks down the given class to it's class attributes and tries to add it as a slash command.
        
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
        command_name = command.name
        for sync_id in command._iter_sync_ids():
            if sync_id == SYNC_ID_NON_GLOBAL:
                try:
                    synced_commands = self._sync_done_commands[SYNC_ID_NON_GLOBAL]
                except KeyError:
                    synced_commands = self._sync_done_commands[SYNC_ID_NON_GLOBAL] = []
                
                for synced_command_index in range(len(synced_commands)):
                    synced_command = synced_commands[synced_command_index]
                    if synced_command.name == command_name:
                        synced_commands[synced_command_index] = command
                        for guild_id in synced_command._iter_guild_ids():
                            self._sync_done.discard(guild_id)
                            self._sync_should.add(guild_id)
                        break
                else:
                    synced_commands.append(command)
            else:
                try:
                    sync_commands = self._sync_should_commands[sync_id]
                except KeyError:
                    self._sync_should_commands[sync_id] = [(True, command)]
                else:
                    for sync_command_index in reversed(range(len(sync_commands))):
                        addition, sync_command = sync_commands[sync_command_index]
                        if sync_command.name == command_name:
                            sync_commands[sync_command_index] = (True, command)
                            break
                    else:
                        sync_commands.append((True, command))
                
                self._sync_done.discard(sync_id)
                self._sync_should.add(sync_id)
    
    def _get_commands(self):
        """
        Gets all the commands of the slasher.
        
        Returns
        -------
        commands : `set` of ``SlashCommand``
        
        Notes
        -----
        This operation is pretty costly for big bots with non-global commands.
        """
        commands = set()
        for synced_commands in self._sync_done_commands.values():
            for command in synced_commands:
                commands.add(command)
        
        for sync_commands in self._sync_should_commands.values():
            for addition, command in sync_commands:
                if addition:
                    commands.add(command)
                else:
                    commands.discard(command)
        
        return commands
    
    def _estimate_pending_changes(self):
        """
        Estimates pending changes of the slasher.
        
        Returns
        -------
        estimated_pending_changes : `int`
        """
        estimated_pending_changes = 0
        for sync_commands in self._sync_should_commands.values():
            estimated_pending_changes += len(sync_commands)
        
        return estimated_pending_changes
    
    def _get_global_commands(self):
        """
        Returns the ``Slasher``'s global commands.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        return self._get_guild_commands(SYNC_ID_GLOBAL)
    
    def _get_non_global_commands(self):
        """
        Returns the ``Slasher``'s non global commands.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        return self._get_guild_commands(SYNC_ID_NON_GLOBAL)
    
    def _get_guild_commands(self, guild_id):
        """
        Returns the ``Slasher``'s guild bound commands.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's id.
        
        Returns
        -------
        commands : `list` of ``SlashCommand``
        """
        try:
            commands = self._sync_done_commands[guild_id]
        except KeyError:
            commands = []
        else:
            commands = commands.copy()
        
        return commands
    
    def _get_global_commands_difference(self):
        """
        Gets the global command difference.
        
        Returns
        -------
        added_commands : `list` of ``SlashCommand``
            The commands which are added or should be added.
        removed_commands : `list` of ``SlashCommand``
            The commands which should be removed.
        """
        return self._get_guild_commands_difference(SYNC_ID_GLOBAL)
    
    def _get_guild_commands_difference(self, guild_id):
        """
        Gets the command difference for the given guild id.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's identifier.
        
        Returns
        -------
        added_commands : `list` of ``SlashCommand``
            The commands which are added or should be added.
        removed_commands : `list` of ``SlashCommand``
            The commands which should be removed.
        """
        actual_commands = self._get_guild_commands(guild_id)
        
        added_commands = []
        removed_commands = []
        
        try:
            commands = self._sync_should_commands[guild_id]
        except KeyError:
            pass
        else:
            for addition, command in commands:
                if addition:
                    list_ = added_commands
                else:
                    list_ = removed_commands
                list_.append(command)
        
        for actual_command_index in reversed(range(len(actual_commands))):
            actual_command = actual_commands[actual_command_index]
            
            actual_command_name = actual_command.name
            
            for command in removed_commands:
                if command.name == actual_command_name:
                    break
            else:
                continue
            
            del actual_commands[actual_command_index]
        
        
        for actual_command_index in reversed(range(len(actual_commands))):
            actual_command = actual_commands[actual_command_index]
            
            actual_command_name = actual_command.name
            
            for command in added_commands:
                if command.name == actual_command_name:
                    break
            else:
                continue
            
            del actual_commands[actual_command_index]
        
        added_commands.extend(actual_commands)
        
        return added_commands, removed_commands
    
    def _remove_command(self, command):
        """
        tries to the given command from the ``Slasher``.
        
        Parameters
        ----------
        command : ``Command``
            The command to remove.
        """
        command_name = command.name
        for sync_id in command._iter_sync_ids():
            if sync_id == SYNC_ID_NON_GLOBAL:
                try:
                    synced_commands = self._sync_done_commands[SYNC_ID_NON_GLOBAL]
                except KeyError:
                    synced_commands = self._sync_done_commands[SYNC_ID_NON_GLOBAL] = []
                
                for synced_command_index in range(len(synced_commands)):
                    synced_command = synced_commands[synced_command_index]
                    if synced_command.name == command_name:
                        
                        del synced_commands[synced_command_index]
                        
                        for guild_id in synced_command._iter_guild_ids():
                            self._sync_done.discard(guild_id)
                            self._sync_should.add(guild_id)
                        
                        break
            
            else:
                try:
                    sync_commands = self._sync_should_commands[sync_id]
                except KeyError:
                    self._sync_should_commands[sync_id] = [(False, command)]
                else:
                    for sync_command_index in reversed(range(len(sync_commands))):
                        addition, sync_command = sync_commands[sync_command_index]
                        if sync_command.name == command_name:
                            sync_commands[sync_command_index] = (False, command)
                            break
                    else:
                        sync_commands.append((False, command))
                
                self._sync_should.add(sync_id)
                self._sync_done.discard(sync_id)
    
    def _mark_command_sync_done(self, command, sync_id):
        """
        Marks the given command's sync as done.
        
        Parameters
        ----------
        sync_id : `int`
            The respective guild's id or other identifier.
        command : ``SlashCommand``
            The command which was synced.
        """
        try:
            sync_commands = self._sync_should_commands[sync_id]
        except KeyError:
            return
        
        for sync_command_index in range(len(sync_commands)):
            addition, sync_command = sync_commands[sync_command_index]
            if sync_command is command:
                break
        else:
            return
        
        del sync_commands[sync_command_index]
        if not sync_commands:
            del self._sync_should_commands[sync_id]
        
        if addition:
            try:
                synced_commands = self._sync_done_commands[sync_id]
            except KeyError:
                synced_commands = self._sync_done_commands[sync_id] = []
            
            command_name = command.name
            for synced_command_index in range(len(synced_commands)):
                synced_command = synced_commands[synced_command_index]
                if synced_command.name == command_name:
                    synced_commands[synced_command_index] = command
                    break
            else:
                synced_commands.append(command)
            return
        
        try:
            synced_commands = self._sync_done_commands[sync_id]
        except KeyError:
            return
        
        try:
            synced_commands.remove(command)
        except ValueError:
            return
        
        if not synced_commands:
            del self._sync_done_commands[sync_id]
            
        
    def __delevent__(self, func, name, **kwargs):
        """
        A method to remove a command by itself, or by it's function and name combination if defined.
        
        Parameters
        ----------
        func : ``SlashCommand``, ``Router`` of ``SlashCommand``
            The command to remove.
        name : `None` or `str`
            The command's name to remove.
        **kwargs : Keyword Arguments
            Other keyword only arguments are ignored.
        
        Raises
        ------
        TypeError
            If `func` was not given neither as ``SlashCommand`` not as ``Router`` of ``SlashCommand``.
        """
        if isinstance(func, Router):
            for sub_func in func:
                if not isinstance(sub_func, SlashCommand):
                    raise TypeError(f'`func` was not given neither as `{SlashCommand.__name__}`, or '
                        f'`{Router.__name__}` of `{SlashCommand.__name__}` instances, got {func!r}.')
            
            for sub_func in func:
                self._remove_command(sub_func)
                
        elif isinstance(func, SlashCommand):
            self._remove_command(func)
        else:
            raise TypeError(f'`func` was not given neither as `{SlashCommand.__name__}`, or `{Router.__name__}` of '
                f'`{SlashCommand.__name__}` instances, got {func!r}.')
    
    async def _try_get_command_by_id(self, client, interaction_event):
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
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
        
        # First request guild commands
        guild = interaction_event.guild
        if (guild is not None):
            guild_id = guild.id
            if not await self._sync_guild(client, guild_id):
                return None
            
            try:
                command = self.command_id_to_command[interaction_id]
            except KeyError:
                pass
            else:
                return command
        
        if not await self._sync_global(client):
            return None
        
        try:
            command = self.command_id_to_command[interaction_id]
        except KeyError:
            pass
        else:
            return command
    
    async def _sync_guild(self, client, guild_id):
        """
        Syncs the respective guild's commands if not yet synced.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if guild_id in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[guild_id]
        except KeyError:
            task = self._sync_tasks[guild_id] = Task(self._sync_guild_task(client, guild_id), KOKORO)
        
        return await task
    
    async def _sync_global(self, client):
        """
        Syncs the not yet synced global commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        if SYNC_ID_GLOBAL in self._sync_done:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_GLOBAL]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_GLOBAL] = Task(self._sync_global_task(client), KOKORO)
        
        return await task
    
    def _unregister_helper(self, command, guild_id):
        """
        Unregisters all the call relations of the given command.
        
        Parameters
        ----------
        command : `None` or ``SlashCommand``
            The slash command to unregister.
        guild_id : `int`
            The respective guild's id.
        """
        if (command is not None):
            command_id = command._pop_command_ids_for(guild_id)
            if command_id:
                try:
                    del self.command_id_to_command[command_id]
                except KeyError:
                    pass
    
    def _register_helper(self, command, guild_id, application_command_id):
        """
        Registers the given command, guild id, application command relationship.
        
        Parameters
        ----------
        command : `None` or ``SlashCommand``
            The slash command to register.
        guild_id : `int`
            The respective guild's id.
        application_command_id : `int`
            The respective command's identifier.
        """
        self.command_id_to_command[application_command_id] = command
        command._register_guild_and_application_command_id(guild_id, application_command_id)
    
    async def _sync_guild_task(self, client, guild_id):
        """
        Syncs the respective guild's commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The guild's id to sync.
        
        Returns
        -------
        success : `bool`
            Whether syncing was successful.
        """
        try:
            application_commands = await client.application_command_guild_get_all(guild_id)
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_guild_task', err)
            success = False
        else:
            added_commands, removed_commands = self._get_guild_commands_difference(guild_id)
            non_global_commands = self._get_non_global_commands()
            
            tasks = []
            
            # Check for removed first because that is super easy
            if removed_commands:
                # Create a new list from removed commands, will use up later!
                maybe_removed_application_commands = []
                
                # First case, check to remove
                for application_command_index in reversed(range(len(application_commands))):
                    application_command = application_commands[application_command_index]
                    
                    application_command_name = application_command.name
                    
                    for guild_command_index in reversed(range(len(removed_commands))):
                        guild_command = removed_commands[guild_command_index]
                        
                        if guild_command.name == application_command_name:
                            break
                    else:
                        continue
                    
                    del application_commands[application_command_index]
                    del removed_commands[guild_command_index]
                    
                    maybe_removed_application_commands.append((application_command, guild_command))
                
                
                # Second case, check non_globals
                for maybe_removed_application_command_index in reversed(range(len(maybe_removed_application_commands))):
                    application_command, guild_command = \
                        maybe_removed_application_commands[maybe_removed_application_command_index]
                    
                    application_command_name = application_command.name
                    
                    for non_global_command_index in reversed(range(len(non_global_commands))):
                        non_global_command = non_global_commands[non_global_command_index]
                        
                        if non_global_command == application_command_name:
                            break
                    else:
                        continue
                    
                    
                    del maybe_removed_application_commands[maybe_removed_application_command_index]
                    del non_global_commands[non_global_command_index]
                    
                    if non_global_command.get_schema() == application_command:
                        # Why do you have same non_global as guild command?
                        self._unregister_helper(guild_command, guild_id)
                        self._register_helper(non_global_command, guild_id, application_command.id)
                        self._mark_command_sync_done(guild_command, guild_id)
                    else:
                        # Why do you have same non_global as guild command?
                        del maybe_removed_application_commands[maybe_removed_application_command_index]
                        del non_global_commands[non_global_command_index]
                        
                        task = Task(self._edit_guild_command_to_non_global(client, guild_id, guild_command,
                            non_global_command, application_command), KOKORO)
                        tasks.append(task)
                
                # Third case, remove
                
                for application_command, guild_command in maybe_removed_application_commands:
                    task = Task(self._delete_guild_command(client, guild_id, guild_command, application_command),
                        KOKORO)
                    tasks.append(task)
                
                # 4th case, remove internal
                for guild_command in removed_commands:
                    command_ids = guild_command._pop_command_ids_for(guild_id)
                    for command_id in command_ids:
                        try:
                            del self.command_id_to_command[command_id]
                        except KeyError:
                            pass
                    
                    self._mark_command_sync_done(guild_command, guild_id)
                
            # Check for added, yayyy
            if added_commands:
                
                # First iteration, simple match
                for application_command_index in reversed(range(len(application_commands))):
                    application_command = application_commands[application_command_index]
                    
                    application_command_name = application_command.name
                    
                    for guild_command_index in reversed(range(len(added_commands))):
                        guild_command = added_commands[guild_command_index]
                        
                        if guild_command.name == application_command_name:
                            break
                    else:
                        continue
                    
                    for non_global_command_index in reversed(range(len(non_global_commands))):
                        non_global_command = non_global_commands[non_global_command_index]
                        if non_global_command.name == application_command_name:
                            del non_global_command_index[non_global_command_index]
                    
                    del application_commands[application_command_index]
                    del added_commands[guild_command_index]
                    
                    if guild_command.get_schema() == application_command:
                        self._register_helper(guild_command, guild_id, application_command.id)
                        self._mark_command_sync_done(guild_command, guild_id)
                    else:
                        task = Task(self._edit_guild_command(client, guild_id, guild_command, application_command),
                            KOKORO)
                        tasks.append(task)
                
                # Second case, add
                for guild_command in added_commands:
                    task = Task(self._create_guild_command(client, guild_id, guild_command), KOKORO)
                    tasks.append(task)
            
            # Check for non_globals
            for application_command_index in reversed(range(len(application_commands))):
                application_command = application_commands[application_command_index]
                
                application_command_name = application_command.name
                
                for non_global_command_index in reversed(range(len(non_global_commands))):
                    non_global_command = non_global_commands[non_global_command_index]
                    
                    if non_global_command.name == application_command_name:
                        break
                else:
                    continue
                
                del application_commands[application_command_index]
                del non_global_commands[non_global_command_index]
                
                if non_global_command.get_schema() == application_command:
                    self._register_helper(non_global_command, guild_id, application_command.id)
                else:
                    task = Task(self._edit_non_global_command(client, guild_id, non_global_command, application_command),
                        KOKORO)
                    tasks.append(task)
            
            # The rest of the command is trash, so trash it.
            for application_command in application_commands:
                task = Task(self._delete_guild_command(client, guild_id, None, application_command), KOKORO)
                tasks.append(task)
            
            done, pending = await WaitTillAll(tasks, KOKORO)
            
            success = True
            for future in done:
                if not future.result():
                    success = False
        
        finally:
            try:
                del self._sync_tasks[guild_id]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(guild_id)
            self._sync_done.add(guild_id)
        
        return success
    
    async def _sync_global_task(self, client):
        """
        Syncs the global commands off the ``Slasher``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        success : `bool`
            Whether the commands where synced with success.
        """
        try:
            application_commands = await client.application_command_global_get_all()
        except BaseException as err:
            # No internet connection
            if not isinstance(err, ConnectionError):
                await client.events.error(client, f'{self!r}._sync_global_commands', err)
            success = False
        else:
            added_commands, removed_commands = self._get_global_commands_difference()
            tasks = []
            
            if removed_commands:
                for application_command_index in reversed(range(len(application_commands))):
                    application_command = application_commands[application_command_index]
                    
                    application_command_name = application_command.name
                    
                    for global_command_index in reversed(range(len(removed_commands))):
                        global_command = removed_commands[global_command_index]
                        
                        if global_command.name == application_command_name:
                            break
                    else:
                        continue
                
                    del application_commands[application_command_index]
                    del removed_commands[global_command_index]
                    
                    task = Task(self._delete_global_command(client, global_command, application_command), KOKORO)
                    tasks.append(task)
            
                for global_command in removed_commands:
                    self._unregister_helper(global_command, SYNC_ID_GLOBAL)
                    self._mark_command_sync_done(global_command, SYNC_ID_GLOBAL)
            
            if added_commands:
                for application_command_index in reversed(range(len(application_commands))):
                    application_command = application_commands[application_command_index]
                    application_command_name = application_command.name
                    
                    for global_command_index in reversed(range(len(added_commands))):
                        global_command = added_commands[global_command_index]
                        if global_command.name == application_command_name:
                            break
                    else:
                        continue
                    
                    del added_commands[global_command_index]
                    del application_commands[application_command_index]
                    
                    if global_command.get_schema() == application_command:
                        self._register_helper(global_command, SYNC_ID_GLOBAL, application_command.id)
                        self._mark_command_sync_done(global_command, SYNC_ID_GLOBAL)
                    else:
                        task = Task(self._edit_global_command(client, global_command, application_command),
                            KOKORO)
                        tasks.append(task)
                
                for global_command in added_commands:
                    task = Task(self._create_global_command(client, global_command), KOKORO)
                    tasks.append(task)
            
            
            for application_command in application_commands:
                task = Task(self._delete_global_command(client, None, application_command), KOKORO)
                tasks.append(task)
            
            
            done, pending = await WaitTillAll(tasks, KOKORO)
            success = True
            for future in done:
                if not future.result():
                    success = False
        
        finally:
            try:
                del self._sync_tasks[SYNC_ID_GLOBAL]
            except KeyError:
                pass
        
        if success:
            self._sync_should.discard(SYNC_ID_GLOBAL)
            self._sync_done.add(SYNC_ID_GLOBAL)
        
        return success
    
    async def _edit_guild_command_to_non_global(self, client, guild_id, guild_command, non_global_command,
            application_command):
        """
        Edits the given guild command ot a non local one.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        guild_command : ``SlashCommand``
            The deleted slash command.
        non_global_command : ``SlashCommand``
            The non_global command what replaced the slash command.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            application_command = await client.application_command_guild_edit(guild_id, application_command,
                non_global_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return False
            
            if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_application_command):
                # no command, no problem, lol
                self._unregister_helper(guild_command, guild_id)
                self._mark_command_sync_done(guild_command, guild_id)
                return True
            
            await client.events.error(client, f'{self!r}._edit_guild_command_to_non_global', err)
            return False
        
        self._unregister_helper(guild_command, guild_id)
        self._register_helper(non_global_command, guild_id, application_command.id)
        self._mark_command_sync_done(guild_command, guild_id)
        return True
    
    async def _edit_guild_command(self, client, guild_id, guild_command, application_command):
        """
        Updates the given guild bound application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        guild_command : ``SlashCommand``
            The slash command to update the application command to.
        application_command : ``ApplicationCommand``
            The respective application command.

        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            await client.application_command_guild_edit(guild_id, application_command, guild_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                self._unregister_helper(guild_command, guild_id)
                return await self._create_guild_command(client, guild_id, guild_command)
            
            await client.events.error(client, f'{self!r}._edit_guild_command', err)
            return False
        
        self._register_helper(guild_command, guild_id, application_command.id)
        self._mark_command_sync_done(guild_command, guild_id)
        return True
    
    async def _delete_guild_command(self, client, guild_id, guild_command, application_command):
        """
        Deletes the given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        guild_command : `None` or ``SlashCommand``
            The slash command to delete.
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
                # Already deleted, lul, ok, I guess.
                pass
            else:
                await client.events.error(client, f'{self!r}._edit_guild_command', err)
                return False
        
        self._unregister_helper(guild_command, guild_id)
        self._mark_command_sync_done(guild_command, guild_id)
        return True
    
    async def _create_guild_command(self, client, guild_id, guild_command):
        """
        Creates a given guild bound command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        guild_command : ``SlashCommand``
            The slash command to create.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            application_command = await client.application_command_guild_create(guild_id, guild_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(client, f'{self!r}._edit_guild_command', err)
            return False
        
        self._register_helper(guild_command, guild_id, application_command.id)
        self._mark_command_sync_done(guild_command, guild_id)
        return True
    
    async def _edit_non_global_command(self, client, guild_id, non_global_command, application_command):
        """
        Edits the given non_global command at the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        non_global_command : ``SlashCommand``
            The command to edit to.
        application_command : ``ApplicationCommand``
            The application command to edit to.
        
        Returns
        -------
        success : `bool`
            Whether the command was edited successfully.
        """
        try:
            await client.application_command_guild_edit(guild_id, application_command, non_global_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                self._unregister_helper(non_global_command, guild_id)
                return await self._create_non_global_command(client, guild_id, non_global_command)
            
            await client.events.error(client, f'{self!r}._edit_non_global_command', err)
            return False
        
        self._register_helper(non_global_command, guild_id, application_command.id)
        return True
    
    async def _create_non_global_command(self, client, guild_id, non_global_command):
        """
        Creates a non_global command at the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        guild_id : `int`
            The respective guild's identifier where the command is.
        non_global_command : ``SlashCommand``
            The command to create.
        
        Returns
        -------
        success : `bool`
            Whether the non_global command was created successfully.
        """
        try:
            application_command = await client.application_command_guild_create(guild_id,
                non_global_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return False
            
            await client.events.error(client, f'{self!r}._create_non_global_command', err)
            return False
        
        self._register_helper(non_global_command, guild_id, application_command.id)
        return True
    
    async def _delete_global_command(self, client, global_command, application_command):
        """
        Deletes the given global command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        global_command : `None` or ``SlashCommand``
            The slash command to delete.
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
                # Already deleted, lul, ok, I guess.
                pass
            else:
                await client.events.error(client, f'{self!r}._edit_global_command', err)
                return False
        
        self._unregister_helper(global_command, SYNC_ID_GLOBAL)
        self._mark_command_sync_done(global_command, SYNC_ID_GLOBAL)
        return True
    
    async def _edit_global_command(self, client, global_command, application_command):
        """
        Updates the given global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        global_command : ``SlashCommand``
            The slash command to update the application command to.
        application_command : ``ApplicationCommand``
            The respective application command.
        
        Returns
        -------
        success : `bool`
            Whether the command was updated successfully.
        """
        try:
            await client.application_command_global_edit(application_command, global_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_application_command:
                # Already deleted, lul, add it back!
                self._unregister_helper(global_command, SYNC_ID_GLOBAL)
                return await self._create_global_command(client, global_command)
            
            await client.events.error(client, f'{self!r}._edit_guild_command', err)
            return False
        
        self._register_helper(global_command, SYNC_ID_GLOBAL, application_command.id)
        self._mark_command_sync_done(global_command, SYNC_ID_GLOBAL)
        return True
    
    async def _create_global_command(self, client, global_command):
        """
        Creates the given global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        global_command : ``SlashCommand``
            The respective command to create.
        
        Returns
        -------
        success : `bool`
            Whether the command was created successfully.
        """
        try:
            application_command = await client.application_command_global_create(global_command.get_schema())
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # No internet connection
                return False
            
            await client.events.error(client, f'{self!r}._create_global_command', err)
            return False
        
        self._register_helper(global_command, SYNC_ID_GLOBAL, application_command.id)
        self._mark_command_sync_done(global_command, SYNC_ID_GLOBAL)
        return True
    
    def do_main_sync(self, client):
        """
        Syncs the slash commands with the client.
        
        The return of the method depends on the thread, from which it was called from.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        
        Returns
        -------
        task : `bool`, ``Task`` or ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if syncing was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                ``FutureAsyncWrapper``. The task will return `True`, if syncing was successful.
            - If the method was called from any other thread, then waits for the syncing task to finish and returns
                `True`, if it was successful.
        """
        task = Task(self._do_main_sync(client), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(thread, EventThread):
            # `.async_wrap` wakes up KOKORO
            return task.async_wrap(thread)
        
        KOKORO.wake_up()
        return task.sync_wrap().wait()
    
    async def _do_main_sync(self, client):
        """
        Syncs the slash commands with the client. This method is the internal method of ``.do_main_sync``.
        
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
        if not self._sync_should:
            return True
        
        try:
            task = self._sync_tasks[SYNC_ID_MAIN]
        except KeyError:
            task = self._sync_tasks[SYNC_ID_MAIN] = Task(self._do_main_sync_task(client), KOKORO)
        
        return await task
    
    
    async def _do_main_sync_task(self, client):
        """
        Syncs the slash commands with the client. This method is the internal coroutine of the ``._do_main_sync``
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
        try:
            tasks = []
            for guild_id in self._sync_should:
                if guild_id == SYNC_ID_GLOBAL:
                    coro = self._sync_global(client)
                else:
                    coro = self._sync_guild(client, guild_id)
                
                task = Task(coro, KOKORO)
                tasks.append(task)
            
            done, pending = await WaitTillAll(tasks, KOKORO)
            
            success = True
            for future in done:
                if not future.result():
                    success = False
            
            return success
        finally:
            try:
                del self._sync_tasks[SYNC_ID_MAIN]
            except KeyError:
                pass

    def _maybe_register_guild_command(self, application_command, guild_id):
        """
        Tries to register the given non-global application command to the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just added application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        for command in self._get_non_global_commands():
            if command.get_schema() == application_command:
                self._register_helper(command, guild_id, application_command.id)
                break
    
    def _maybe_unregister_guild_command(self, application_command, guild_id):
        """
        Tries to unregister the given non-global application command from the slasher.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            A just deleted application command.
        guild_id : `int`
            The respective guild's identifier.
        """
        for command in self._get_non_global_commands():
            if command.get_schema() == application_command:
                self._unregister_helper(command, guild_id)
                break
    
    def __repr__(self):
        """Returns the slasher's representation."""
        return f'<{self.__class__.__name__} sync_should={len(self._sync_should)}, sync_done={len(self._sync_done)}>'

del EventHandlerBase
