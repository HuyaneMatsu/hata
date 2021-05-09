__all__ = ()

import reprlib

from ...backend.analyzer import CallableAnalyzer

from ...discord.core import ROLES, CHANNELS
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.client import Client
from ...discord.user import UserBase, User
from ...discord.role import Role
from ...discord.channel import ChannelBase
from ...discord.interaction import ApplicationCommandOption, ApplicationCommandOptionChoice, \
    ApplicationCommandOptionType, InteractionEvent
from ...discord.limits import APPLICATION_COMMAND_OPTIONS_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, \
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX

from .utils import raw_name_to_display, normalize_description

async def converter_int(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `int`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
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


async def converter_str(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `str`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `str`
        If conversion fails, then returns `None`.
    """
    return value

BOOL_TABLE = {
    str(True): True,
    str(False): False,
}

async def converter_bool(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `bool`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `bool`
        If conversion fails, then returns `None`.
    """
    return BOOL_TABLE.get(value, None)


async def converter_snowflake(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to a snowflake.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
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


async def converter_user(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``UserBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    user : `None`, ``User`` or ``Client``
        If conversion fails, then returns `None`.
    """
    user_id = await converter_snowflake(client, interaction, value)
    
    if user_id is None:
        user = None
    else:
        resolved_users = interaction.resolved_users
        if resolved_users is None:
            user = None
        else:
            user = resolved_users.get(user_id, None)
        
        if user is None:
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


async def converter_role(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``Role`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``Role``
        If conversion fails, then returns `None`.
    """
    role_id = await converter_snowflake(client, interaction, value)
    
    if role_id is None:
        role = None
    else:
        resolved_roles = interaction.resolved_roles
        if resolved_roles is None:
            role = None
        else:
            role = resolved_roles.get(role_id, None)
        
        if role is None:
            role = ROLES.get(role_id, None)
    
    return role


async def converter_channel(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``ChannelBase`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``ChannelBase`` instance
        If conversion fails, then returns `None`.
    """
    channel_id = await converter_snowflake(client, interaction, value)
    
    if channel_id is None:
        channel = None
    else:
        resolved_channels = interaction.resolved_channels
        if resolved_channels is None:
            channel = None
        else:
            channel = resolved_channels.get(channel_id, None)
        
        if channel is None:
            channel = CHANNELS.get(channel_id, None)
    
    return channel


async def converter_mentionable(client, interaction, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to mentionable ``DiscordEntity`` instance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction : ``ApplicationCommandInteraction``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or ``DiscordEntity`` instance
        If conversion fails, then returns `None`.
    """
    entity_id = await converter_snowflake(client, interaction, value)
    
    # Use goto
    while True:
        if entity_id is None:
            entity = None
            break
        
        resolved_users = interaction.resolved_users
        if (resolved_users is not None):
            try:
                entity = resolved_users[entity_id]
            except KeyError:
                pass
            else:
                break
        
        resolved_roles = interaction.resolved_roles
        if (resolved_roles is not None):
            try:
                entity = resolved_roles[entity_id]
            except KeyError:
                pass
            else:
                break
        
        entity = None
        break
    
    return entity



ANNOTATION_TYPE_STR = 0
ANNOTATION_TYPE_INT = 1
ANNOTATION_TYPE_BOOL = 2
ANNOTATION_TYPE_USER = 3
ANNOTATION_TYPE_USER_ID = 4
ANNOTATION_TYPE_ROLE = 5
ANNOTATION_TYPE_ROLE_ID = 6
ANNOTATION_TYPE_CHANNEL = 7
ANNOTATION_TYPE_CHANNEL_ID = 8
ANNOTATION_TYPE_NUMBER = 9
ANNOTATION_TYPE_MENTIONABLE = 10
ANNOTATION_TYPE_MENTIONABLE_ID = 11

STR_ANNOTATION_TO_ANNOTATION_TYPE = {
    'str': ANNOTATION_TYPE_STR,
    'int': ANNOTATION_TYPE_INT,
    'bool': ANNOTATION_TYPE_BOOL,
    'user': ANNOTATION_TYPE_USER,
    'user_id': ANNOTATION_TYPE_USER_ID,
    'role': ANNOTATION_TYPE_ROLE,
    'role_id': ANNOTATION_TYPE_ROLE_ID,
    'channel': ANNOTATION_TYPE_CHANNEL,
    'channel_id': ANNOTATION_TYPE_CHANNEL_ID,
    'number': ANNOTATION_TYPE_NUMBER,
    'mentionable': ANNOTATION_TYPE_MENTIONABLE,
    'mentionable_id': ANNOTATION_TYPE_MENTIONABLE_ID
}

# Used at repr
ANNOTATION_TYPE_TO_STR_ANNOTATION = {
    ANNOTATION_TYPE_STR: 'str',
    ANNOTATION_TYPE_INT: 'int',
    ANNOTATION_TYPE_BOOL: 'bool',
    ANNOTATION_TYPE_USER: 'user',
    ANNOTATION_TYPE_USER_ID: 'user_id',
    ANNOTATION_TYPE_ROLE: 'role',
    ANNOTATION_TYPE_ROLE_ID: 'role_id',
    ANNOTATION_TYPE_CHANNEL: 'channel',
    ANNOTATION_TYPE_CHANNEL_ID: 'channel_id',
    ANNOTATION_TYPE_NUMBER: 'number',
    ANNOTATION_TYPE_MENTIONABLE: 'mentionable',
    ANNOTATION_TYPE_MENTIONABLE_ID : 'mentionable_id',
}

TYPE_ANNOTATION_TO_ANNOTATION_TYPE = {
    str: ANNOTATION_TYPE_STR,
    int: ANNOTATION_TYPE_INT,
    bool: ANNOTATION_TYPE_BOOL,
    UserBase: ANNOTATION_TYPE_USER,
    User: ANNOTATION_TYPE_USER,
    Role: ANNOTATION_TYPE_ROLE,
    ChannelBase: ANNOTATION_TYPE_CHANNEL,
}

ANNOTATION_TYPE_TO_CONVERTER = {
    ANNOTATION_TYPE_STR: converter_str,
    ANNOTATION_TYPE_INT: converter_int,
    ANNOTATION_TYPE_BOOL: converter_bool,
    ANNOTATION_TYPE_USER: converter_user,
    ANNOTATION_TYPE_USER_ID: converter_snowflake,
    ANNOTATION_TYPE_ROLE: converter_role,
    ANNOTATION_TYPE_ROLE_ID: converter_snowflake,
    ANNOTATION_TYPE_CHANNEL: converter_channel,
    ANNOTATION_TYPE_CHANNEL_ID : converter_snowflake,
    ANNOTATION_TYPE_NUMBER: converter_int,
    ANNOTATION_TYPE_MENTIONABLE: converter_mentionable,
    ANNOTATION_TYPE_MENTIONABLE_ID: converter_snowflake,
}

# `int` Discord fields are broken and they are refusing to fix it, use string instead.
# Reference: https://github.com/discord/discord-api-docs/issues/2448
ANNOTATION_TYPE_TO_OPTION_TYPE = {
    ANNOTATION_TYPE_STR: ApplicationCommandOptionType.string,
    ANNOTATION_TYPE_INT: ApplicationCommandOptionType.string,
    ANNOTATION_TYPE_BOOL: ApplicationCommandOptionType.boolean,
    ANNOTATION_TYPE_USER: ApplicationCommandOptionType.user,
    ANNOTATION_TYPE_USER_ID: ApplicationCommandOptionType.user,
    ANNOTATION_TYPE_ROLE: ApplicationCommandOptionType.role,
    ANNOTATION_TYPE_ROLE_ID: ApplicationCommandOptionType.role,
    ANNOTATION_TYPE_CHANNEL: ApplicationCommandOptionType.channel,
    ANNOTATION_TYPE_CHANNEL_ID: ApplicationCommandOptionType.channel,
    ANNOTATION_TYPE_NUMBER: ApplicationCommandOptionType.integer,
    ANNOTATION_TYPE_MENTIONABLE: ApplicationCommandOptionType.mentionable,
    ANNOTATION_TYPE_MENTIONABLE_ID: ApplicationCommandOptionType.mentionable,
}


def create_annotation_choice_from_int(value):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    value : `int`
        The validated annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `str` or `int`)
        The validated annotation choice.
    """
    return (str(value), value)

def create_annotation_choice_from_str(value):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    value : `str`
        The validated annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `str` or `int`)
        The validated annotation choice.
    """
    # make sure
    return (value, value)

def parse_annotation_choice_from_tuple(annotation):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    annotation : `tuple`
        Annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `str` or `int`)
        The validated annotation choice.
    
    Raises
    ------
    TypeError
        - `annotation`'s name's type is incorrect.
        - `annotation`'s value's type is incorrect.
    ValueError
        `annotation`'s length is invalid.
    """
    annotation_length = len(annotation)
    if (annotation_length < 1 or annotation_length > 2):
        raise ValueError(f'`tuple` annotation length can be in range [1:2], got {annotation_length!r}; {annotation!r}')
    
    if annotation_length == 1:
        value = annotation[0]
        if isinstance(value, str):
            return create_annotation_choice_from_str(value)
        
        if isinstance(value, int):
            return create_annotation_choice_from_int(value)
        
        raise TypeError(f'`annotation-value` can be either `str` or `int`, got {value.__class__.__name__}.')
    
    # if annotation_length == 2:
    
    name, value = annotation
    if not isinstance(name, str):
        raise TypeError(f'`annotation-name` can be `str` instance, got {name.__class__.__name__}.')
    
    if not isinstance(value, (str, int)):
        raise TypeError(f'`annotation-value` can be either `str` or `int`, got {value.__class__.__name__}.')
    
    return (name, value)


def parse_annotation_choice(annotation_choice):
    """
    Parses annotation choice.
    
    Parameters
    ----------
    annotation_choice : `tuple`, `str`, `int`
        A choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `str` or `int`)
        The validated annotation choice.
    
    Raises
    ------
    TypeError
        - `annotation`'s name's type is incorrect.
        - `annotation`'s value's type is incorrect.
    ValueError
        `annotation`'s length is invalid.
    """
    if isinstance(annotation_choice, tuple):
        return parse_annotation_choice_from_tuple(annotation_choice)
    
    if isinstance(annotation_choice, str):
        return create_annotation_choice_from_str(annotation_choice)
    
    if isinstance(annotation_choice, int):
        return create_annotation_choice_from_int(annotation_choice)
    
    raise TypeError(f'`annotation-choice` can be either given as `tuple`, `str` or `int` instance, got '
        f'{annotation_choice.__class__.__name__}.')


def parse_annotation_type_and_choice(annotation_value, parameter_name):
    """
    Parses annotation type and choices out from an annotation value.
    
    Parameters
    ----------
    annotation_value : `str`, `type`, `list`, `dict`
        The annotation's value.
    parameter_name : `str`
        The parameter's name.
    
    Returns
    -------
    annotation_type : `int`
        Internal identifier about the annotation.
    choices : `None` or `dict` of (`int` or `str`, `str`) items
        Choices if applicable.
    
    TypeError
        - If `annotation_value` is `list` instance, but it's elements do not match the `tuple` (`str`, `str` or `int`)
            pattern.
        - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
        - If `annotation_value` is unexpected.
    ValueError
        - If `annotation_value` is `str` instance, but not any of the expected ones.
        - If `annotation_value` is `type` instance, but not any of the expected ones.
        - If `choice` amount is out of the expected range [1:25].
        - If a `choice` name is duped.
        - If a `choice` values are mixed types.
    """
    if isinstance(annotation_value, str):
        annotation_value = annotation_value.lower()
        try:
            annotation_type = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Parameter `{parameter_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    elif isinstance(annotation_value, type):
        try:
            annotation_type = TYPE_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Parameter `{parameter_name}` has annotation not refers to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    else:
        choice_elements = []
        if isinstance(annotation_value, list):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
        
        elif isinstance(annotation_value, set):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_elements.sort()
        elif isinstance(annotation_value, dict):
            for annotation_choice in annotation_value.items():
                choice_element = parse_annotation_choice_from_tuple(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_elements.sort()
        
        else:
            raise TypeError(f'Parameter `{parameter_name}` has annotation not set neither as `tuple`, `str`, `type`, '
                f'`list`, `set` or `dict`, got {annotation_value.__class__.__name__}.')
        
        # Filter dupe names
        dupe_checker = set()
        length = 0
        for name, value in choice_elements:
            dupe_checker.add(name)
            new_length = len(dupe_checker)
            if new_length == length:
                raise ValueError(f'Duped choice name in annotation: `{parameter_name}`.')
            
            length = new_length
        
        # Check annotation type
        expected_type = None
        for name, value in choice_elements:
            if isinstance(value, str):
                type_ = str
            else:
                type_ = int
            
            if expected_type is None:
                expected_type = type_
                continue
            
            if expected_type is not type_:
                raise ValueError(f'Mixed choice value types in annotation: `{parameter_name}`.')
        
        if expected_type is str:
            annotation_type = ANNOTATION_TYPE_STR
        else:
            annotation_type = ANNOTATION_TYPE_INT
        
        choices = {value:name for name, value in choice_elements}
    
    return annotation_type, choices


def parse_annotation_description(description, parameter_name):
    """
    Parses an annotation's description.
    
    Parameters
    ----------
    description : `str`
        The description of an annotation.
    annotation_name : `str`
        The annotation's name.
    
    Returns
    -------
    description : `str`
    
    Raises
    ------
    TypeError
        - If `description`'s is not `str` instance.
    ValueError
        - If `description`'s length is out of the expected range [2:100].
    """
    if type(description) is str:
        pass
    elif isinstance(description, str):
        description = str(description)
    else:
        raise TypeError(f'Parameter `{parameter_name}` has annotation description not as `str` instance, got '
            f'{description.__class__.__name__}.')
    
    description_length = len(description)
    if description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or \
            description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX:
        raise ValueError(f'Argument `{parameter_name}` has annotation description\'s length is out of the expected '
            f'range [{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:'
            f'{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got {description_length}; {description!r}.')
    
    description = normalize_description(description)
    return description


def parse_annotation_name(name, parameter_name):
    """
    Parses an annotation's name.
    
    Parameters
    ----------
    name : `str`
        The name of an annotation.
    annotation_name : `None` or `str`
        The annotation's name.
    
    Returns
    -------
    name : `str`
    
    Raises
    ------
    TypeError
        - If `name`'s is neither `None` or `str` instance.
    """
    if name is None:
        name = parameter_name
    elif type(name) is str:
        pass
    elif isinstance(name, str):
        name = str(name)
    else:
        raise TypeError(f'`Parameter `{parameter_name}` has `name` given as non `str` instance, got '
            f'{name.__class__.__name__}.')
    
    name = raw_name_to_display(name)
    
    return name


class ParameterConverter:
    """
    Converter class for choice based converters.
    
    Attributes
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
    
    def __new__(cls, parameter, parameter_configurer):
        """
        Creates a new argument converter from the given argument.
        
        Parameters
        ----------
        parameter : ``Argument``
            The argument to create converter from.
        parameter_configurer : `None` or ``SlashCommandParameterConfigurerWrapper``
            Parameter configurer for the parameter if any.
        
        Raises
        ------
        TypeError
            - if the `argument` has no annotation.
            - If `annotation_value` is `list` instance, but it's elements do not match the `tuple`
                (`str`, `str` or `int`) pattern.
            - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
            - If `annotation_value` is unexpected.
            - If `annotation` is not `tuple`.
            - If `annotation` 1st element (description) is not `str` instance.
        ValueError
            - If `annotation` is a `tuple`, but it's length is not range [2:3].
            - If `annotation_value` is `str` instance, but not any of the expected ones.
            - If `annotation_value` is `type` instance, but not any of the expected ones.
            - If `choice` amount is out of the expected range [1:25].
            - If a `choice` name is duped.
            - If a `choice` values are mixed types.
            - If `annotation`'s 1st element's (description's) length is out of the expected range [2:100].
        """
        if parameter_configurer is None:
            parameter_name = parameter.name
            if not parameter.has_annotation:
                raise TypeError(f'Argument `{parameter_name}` has no annotation.')
            
            annotation = parameter.annotation
            if not isinstance(annotation, tuple):
                raise TypeError(f'Argument `{parameter_name}` is not `tuple` instances, got '
                    f'{annotation.__class__.__name__}.')
            
            annotation_tuple_length = len(annotation)
            if annotation_tuple_length not in (2, 3):
                raise ValueError(f'Argument `{parameter_name}` has annotation as `tuple`, but it\'s length is not in '
                    f'range [2:3], got {annotation_tuple_length!r}, {annotation_tuple_length!r}.')
            
            annotation_value, description = annotation[:2]
            annotation_type, choices = parse_annotation_type_and_choice(annotation_value, parameter_name)
            
            description = parse_annotation_description(description, parameter_name)
            
            if len(annotation) == 3:
                name = annotation[2]
            else:
                name = None
            
            name = parse_annotation_name(name, parameter_name)
        else:
            choices = parameter_configurer._choices
            description = parameter_configurer._description
            name = parameter_configurer._name
            annotation_type = parameter_configurer._type
        
        if parameter.has_default:
            default = parameter.default
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
    
    async def __call__(self, client, interaction, value):
        """
        Calls the argument converter to convert the given `value` to it's desired state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective ``InteractionEvent``.
        interaction : ``ApplicationCommandInteraction``
            The received application command interaction.
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
            value = await self.converter(client, interaction, value)
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
    
    def __repr__(self):
        """Returns the argument converter's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ', type=',
            ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type],
            ', description=',
            reprlib.repr(self.description)
        ]
        
        if not self.required:
            result.append(', default=')
            result.append(repr(self.default))
        
        choices = self.choices
        if (choices is not None):
            result.append(', choices=')
            result.append(repr(choices))
        
        result.append('>')
        
        return ''.join(result)
    
    
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


def generate_parameter_parsers(func, parameter_configurers):
    """
    Parses the given `func`'s arguments.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    parameter_configurers : `None` or `dict` of (`str`, ``SlashCommandParameterConfigurerWrapper``) items
        Parameter configurers to overwrite annotations.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    parameter_parsers : `tuple` of ``ParameterConverter``
        Argument converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only arguments.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
        - If `func` accepts less than `2` arguments.
        - If `func` accepts more than `27` arguments.
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
        - If an argument's `choice` amount is out of the expected range [1:25].
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
    
    
    parameters = real_analyzer.get_non_reserved_positional_arguments()
    
    argument_count = len(parameters)
    if argument_count < 2:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at least 2 arguments: '
            f'`client` and `interaction_event`, meanwhile it accepts only {argument_count}.')
    
    if argument_count > 2+APPLICATION_COMMAND_OPTIONS_MAX:
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at maximum `27` arguments: '
            f', meanwhile it accepts up to {argument_count}.')
    
    parameter_parameter = parameters[0]
    if parameter_parameter.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            'reserved, meanwhile it should not have.')
    
    if parameter_parameter.has_annotation and (parameter_parameter.annotation is not Client):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the client\'s argument slot, '
            f'what is not `{Client.__name__}`.')
    
    
    event_parameter = parameters[1]
    if event_parameter.has_default:
        raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
            f'reserved, meanwhile it should not have.')
    
    if event_parameter.has_annotation and (event_parameter.annotation is not InteractionEvent):
        raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the interaction_event\'s argument '
            f'slot what is not `{InteractionEvent.__name__}`.')
    
    parameter_parsers = []
    
    for parameter in parameters[2:]:
        if parameter_configurers is None:
            parameter_configurer = None
        else:
            parameter_configurer = parameter_configurers.get(parameter.name, None)
        
        parameter_parser = ParameterConverter(parameter, parameter_configurer)
        parameter_parsers.append(parameter_parser)
    
    parameter_parsers = tuple(parameter_parsers)
    
    if should_instance:
        func = analyzer.insatnce()
    
    return func, parameter_parsers
