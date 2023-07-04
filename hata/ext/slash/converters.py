__all__ = ('SlashParameter', )

import reprlib
from enum import Enum

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType, copy_docs, include, un_map_pack

from ...discord.application_command import (
    ApplicationCommandOption, ApplicationCommandOptionChoice, ApplicationCommandOptionType
)
from ...discord.application_command.application_command.constants import (
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN,
    APPLICATION_COMMAND_OPTIONS_MAX
)
from ...discord.application_command.application_command_option_metadata.constants import (
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
)
from ...discord.application_command.application_command_option_metadata.fields import (
    validate_max_length, validate_min_length
)
from ...discord.channel import Channel, ChannelType
from ...discord.client import Client
from ...discord.core import CHANNELS, ROLES
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.interaction import InteractionEvent, InteractionType
from ...discord.message import Attachment
from ...discord.role import Role
from ...discord.user import ClientUserBase, User, UserBase

from .exceptions import SlashCommandParameterConversionError
from .expression_parser import evaluate_text
from .utils import normalize_description, raw_name_to_display


try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern

SlashCommandParameterAutoCompleter = include('SlashCommandParameterAutoCompleter')
APPLICATION_COMMAND_FUNCTION_DEEPNESS = include('APPLICATION_COMMAND_FUNCTION_DEEPNESS')

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE = InteractionType.application_command_autocomplete



async def converter_self_client(client, interaction_event):
    """
    Internal converter for returning the client who received an interaction event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    
    Returns
    -------
    client : ``Client``
    """
    return client


async def converter_self_interaction_event(client, interaction_event):
    """
    Internal converter for returning the received interaction event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    
    Returns
    -------
    interaction_event : ``ApplicationCommandInteraction``
    """
    return interaction_event


async def converter_self_interaction_target(client, interaction_event):
    """
    Internal converter for returning the received interaction event's target. Applicable for context application
    commands.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    
    Returns
    -------
    target : `None`, ``DiscordEntity``
        The resolved entity if any.
    """
    if interaction_event.type is not INTERACTION_TYPE_APPLICATION_COMMAND:
        return None
    
    return interaction_event.target
    

async def converter_self_interaction_value(client, interaction_event):
    """
    Internal converter for returning the received interaction event's value. Applicable for auto completed application
    commands parameters.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    
    Returns
    -------
    target : `None`, `str`
        The received value if any.
    """
    if interaction_event.type is not INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE:
        return None
    
    return interaction_event.value


async def converter_int(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `int`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, `int`
        If conversion fails, then returns `None`.
    """
    if not isinstance(value, int):
        try:
            value = int(value)
        except ValueError:
            value = None
    
    return value


async def converter_float(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `float`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `float`, `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, `float`
        If conversion fails, then returns `None`.
    """
    if not isinstance(value, float):
        try:
            value = float(value)
        except ValueError:
            value = None
    
    return value


async def converter_str(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `str`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, `str`
        If conversion fails, then returns `None`.
    """
    return value

BOOL_TABLE = {
    'true': True,
    'false': False,
}

async def converter_bool(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to `bool`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, `bool`
        If conversion fails, then returns `None`.
    """
    if not isinstance(value, bool):
        value =  BOOL_TABLE.get(value, None)
    
    return value


async def converter_attachment(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``Attachment``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : ``Attachment``
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : ``Attachment``
        If conversion fails, then returns `None`.
    """
    attachment_id = await converter_snowflake(client, interaction_event, value)
    if (attachment_id is not None):
        return interaction_event.resolve_attachment(attachment_id)


async def converter_snowflake(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to a snowflake.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    snowflake : `None`, ``int``
        If conversion fails, then returns `None`.
    """
    try:
        snowflake = int(value)
    except ValueError:
        snowflake = None
    else:
        if (snowflake < (1 << 22)) or (snowflake > ((1 << 64) - 1)):
            snowflake = None
    
    return snowflake


async def converter_user(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``UserBase``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    user : `None`, ``ClientUserBase``
        If conversion fails, then returns `None`.
    """
    user_id = await converter_snowflake(client, interaction_event, value)
    if (user_id is not None):
        user = interaction_event.resolve_user(user_id)
        if user is None:
            try:
                user = await client.user_get(user_id)
            except ConnectionError:
                user = None
            except DiscordException as err:
                if err.code == ERROR_CODES.unknown_user:
                    user = None
                else:
                    raise
        
        return user


async def converter_role(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``Role``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, ``Role``
        If conversion fails, then returns `None`.
    """
    role_id = await converter_snowflake(client, interaction_event, value)
    if (role_id is not None):
        role = interaction_event.resolve_role(role_id)
        if role is None:
            role = ROLES.get(role_id, None)
        
        return role


async def converter_channel(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``Channel``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, ``Channel``
        If conversion fails, then returns `None`.
    """
    channel_id = await converter_snowflake(client, interaction_event, value)
    if (channel_id is not None):
        channel = interaction_event.resolve_channel(channel_id)
        if channel is None:
            channel = CHANNELS.get(channel_id, None)
        
        return channel


async def converter_mentionable(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to mentionable ``DiscordEntity``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None`, ``DiscordEntity``
        If conversion fails, then returns `None`.
    """
    mentionable_id = await converter_snowflake(client, interaction_event, value)
    if (mentionable_id is not None):
        return interaction_event.resolve_mentionable(mentionable_id)


async def converter_expression(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to evaluable expression to an integer or to a float.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective ``InteractionEvent``.
    interaction_event : ``InteractionEvent``
        The received application command interaction.
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `int`, `float`
    
    Raises
    ------
    EvaluationError
        If evaluation failed for any reason.
    """
    return evaluate_text(value)


ANNOTATION_TYPE_STR = 1
ANNOTATION_TYPE_INT = 2
ANNOTATION_TYPE_BOOL = 3
ANNOTATION_TYPE_USER = 4
ANNOTATION_TYPE_USER_ID = 5
ANNOTATION_TYPE_ROLE = 6
ANNOTATION_TYPE_ROLE_ID = 7
ANNOTATION_TYPE_CHANNEL = 8
ANNOTATION_TYPE_CHANNEL_ID = 9
ANNOTATION_TYPE_NUMBER = 10
ANNOTATION_TYPE_MENTIONABLE = 11
ANNOTATION_TYPE_MENTIONABLE_ID = 12
ANNOTATION_TYPE_SELF_CLIENT = 13
ANNOTATION_TYPE_SELF_INTERACTION_EVENT = 14
ANNOTATION_TYPE_EXPRESSION = 15
ANNOTATION_TYPE_FLOAT = 16
ANNOTATION_TYPE_SELF_TARGET = 17
ANNOTATION_TYPE_SELF_VALUE = 18
ANNOTATION_TYPE_ATTACHMENT = 19

ANNOTATION_NAMES_CLIENT = frozenset((
    'c',
    'client',
))

ANNOTATION_NAMES_INTERACTION_EVENT = frozenset((
    'e',
    'event',
    'interaction_event',
))

ANNOTATION_NAMES_TARGET = frozenset((
    't',
    'target',
))


ANNOTATION_NAMES_VALUE = frozenset((
    'v',
    'val',
    'value',
))

CHANNEL_TYPES_FORBIDDEN = (
    ChannelType.unknown,
    ChannelType.thread,
)

CHANNEL_TYPES_GROUP_GUILD = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.guild
)
CHANNEL_TYPES_GUILD_CATEGORY = (ChannelType.guild_category, )
CHANNEL_TYPES_GUILD_DIRECTORY = (ChannelType.guild_directory, )
CHANNEL_TYPES_GUILD_STORE = (ChannelType.guild_store, )
CHANNEL_TYPES_GUILD_SYSTEM = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.guild_system
)
CHANNEL_TYPES_GUILD_TEXT = (ChannelType.guild_text, )
CHANNEL_TYPES_GUILD_ANNOUNCEMENTS = (ChannelType.guild_announcements, )
CHANNEL_TYPES_GUILD_CONNECTABLE = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.guild and channel_type.flags.connectable
)
CHANNEL_TYPES_GUILD_VOICE = (ChannelType.guild_voice, )
CHANNEL_TYPES_GUILD_STAGE = (ChannelType.guild_stage, )
CHANNEL_TYPES_GROUP_PRIVATE = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.private
)
CHANNEL_TYPES_PRIVATE = (ChannelType.private, )
CHANNEL_TYPES_PRIVATE_GROUP = (ChannelType.private_group, )
CHANNEL_TYPES_GROUP_THREAD = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.thread
)
CHANNEL_TYPES_THREAD_ANNOUNCEMENTS = (ChannelType.guild_thread_announcements, )
CHANNEL_TYPES_THREAD_PUBLIC = (ChannelType.guild_thread_public, )
CHANNEL_TYPES_THREAD_PRIVATE = (ChannelType.guild_thread_private, )
CHANNEL_TYPES_GROUP_TEXTUAL = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.textual
)
CHANNEL_TYPES_GROUP_GUILD_TEXTUAL = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.guild and channel_type.flags.textual
)
CHANNEL_TYPES_GROUP_CONNECTABLE = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.connectable
)
CHANNEL_TYPES_GROUP_THREADABLE = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.threadable
)
CHANNEL_TYPES_GUILD_FORUM = (ChannelType.guild_forum, )
CHANNEL_TYPES_GUILD_MEDIA = (ChannelType.guild_media, )

CHANNEL_TYPES_GROUP_FORUM = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.forum
)

CHANNEL_TYPES_GROUP_INVITABLE = tuple(
    channel_type for channel_type in ChannelType.INSTANCES.values()
    if (channel_type not in CHANNEL_TYPES_FORBIDDEN) and channel_type.flags.invitable
)

STR_ANNOTATION_TO_ANNOTATION_TYPE = {
    # Generic
    'str': (ANNOTATION_TYPE_STR, None),
    'int': (ANNOTATION_TYPE_INT, None),
    'bool': (ANNOTATION_TYPE_BOOL, None),
    'user': (ANNOTATION_TYPE_USER, None),
    'user_id': (ANNOTATION_TYPE_USER_ID, None),
    'role': (ANNOTATION_TYPE_ROLE, None),
    'role_id': (ANNOTATION_TYPE_ROLE_ID, None),
    'channel': (ANNOTATION_TYPE_CHANNEL, None),
    'channel_id': (ANNOTATION_TYPE_CHANNEL_ID, None),
    'number': (ANNOTATION_TYPE_NUMBER, None),
    'mentionable': (ANNOTATION_TYPE_MENTIONABLE, None),
    'mentionable_id': (ANNOTATION_TYPE_MENTIONABLE_ID, None),
    'expression': (ANNOTATION_TYPE_EXPRESSION, None),
    'float': (ANNOTATION_TYPE_FLOAT, None),
    'attachment': (ANNOTATION_TYPE_ATTACHMENT, None),
    
    # Channel type specific
    # - by channel name
    f'{"channel"}{"guild"}{"base"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_GUILD),
    f'{"channel"}{"guild"}{"main"}{"base"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_GUILD),
    f'{"channel"}{"category"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CATEGORY),
    f'{"channel"}{"directory"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_DIRECTORY),
    f'{"channel"}{"store"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STORE),
    f'{"channel"}{"text"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_SYSTEM),
    f'{"channel"}{"voice"}{"base"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CONNECTABLE),
    f'{"channel"}{"voice"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_VOICE),
    f'{"channel"}{"stage"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STAGE),
    f'{"channel"}{"private"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE),
    f'{"channel"}{"group"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE_GROUP),
    f'{"channel"}{"thread"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_THREAD),
    f'{"channel"}{"text"}{"base"}': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_GUILD_TEXTUAL),
    f'{"channel"}{"forum"}':(ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_FORUM),
    f'{"channel"}{"media"}':(ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_MEDIA),
    f'{"channel"}{"forum"}{"base"}':(ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_FORUM),
    # - by generic name
    'channel_guild_text': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_TEXT),
    'channel_private': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE),
    'channel_guild_voice': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_VOICE),
    'channel_private_group': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE_GROUP),
    'channel_guild_category': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CATEGORY),
    'channel_guild_announcements': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_ANNOUNCEMENTS),
    'channel_guild_store': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STORE),
    'channel_guild_thread_announcements': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_ANNOUNCEMENTS),
    'channel_guild_thread_public': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_PUBLIC),
    'channel_guild_thread_private': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_PRIVATE),
    'channel_guild_stage': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STAGE),
    'channel_guild_directory': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_DIRECTORY),
    'channel_group_messageable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_TEXTUAL),
    'channel_group_guild_messageable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_GUILD_TEXTUAL),
    'channel_group_guild_main_text': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_SYSTEM),
    'channel_group_connectable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_CONNECTABLE),
    'channel_group_private': (ANNOTATION_TYPE_CHANNEL, ),
    'channel_group_guild_connectable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CONNECTABLE),
    'channel_group_guild': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_GUILD),
    'channel_group_thread': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_THREAD),
    'channel_group_can_contain_threads': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_THREADABLE),
    'channel_guild_forum': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_FORUM),
    'channel_guild_media': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_MEDIA),
    'channel_group_forum': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_FORUM),
    'channel_group_invitable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GROUP_INVITABLE),
    # - id + by generic name
    'channel_id_guild_text': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_TEXT),
    'channel_id_private': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_PRIVATE),
    'channel_id_guild_voice': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_VOICE),
    'channel_id_private_group': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_PRIVATE_GROUP),
    'channel_id_guild_category': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_CATEGORY),
    'channel_id_guild_announcements': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_ANNOUNCEMENTS),
    'channel_id_guild_store': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_STORE),
    'channel_id_guild_thread_announcements': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_THREAD_ANNOUNCEMENTS),
    'channel_id_guild_thread_public': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_THREAD_PUBLIC),
    'channel_id_guild_thread_private': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_THREAD_PRIVATE),
    'channel_id_guild_stage': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_STAGE),
    'channel_id_guild_directory': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_DIRECTORY),
    'channel_id_group_messageable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_TEXTUAL),
    'channel_id_group_guild_messageable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_GUILD_TEXTUAL),
    'channel_id_group_guild_main_text': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_SYSTEM),
    'channel_id_group_connectable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_CONNECTABLE),
    'channel_id_group_private': (ANNOTATION_TYPE_CHANNEL_ID, ),
    'channel_id_group_guild_connectable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_CONNECTABLE),
    'channel_id_group_guild': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_GUILD),
    'channel_id_group_thread': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_THREAD),
    'channel_id_group_can_contain_threads': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_THREADABLE),
    'channel_id_guild_forum': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_FORUM),
    'channel_id_guild_media': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_MEDIA),
    'channel_id_group_forum': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_FORUM),
    'channel_id_group_invitable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GROUP_INVITABLE),
    
    # Internal
    **un_map_pack((
        (name, (ANNOTATION_TYPE_SELF_CLIENT, None))
        for name in ANNOTATION_NAMES_CLIENT
    )),
    **un_map_pack((
        (name, (ANNOTATION_TYPE_SELF_INTERACTION_EVENT, None))
        for name in ANNOTATION_NAMES_INTERACTION_EVENT
    )),
    **un_map_pack((
        (name, (ANNOTATION_TYPE_SELF_TARGET, None))
        for name in ANNOTATION_NAMES_TARGET
    )),
    **un_map_pack((
        (name, (ANNOTATION_TYPE_SELF_VALUE, None))
        for name in ANNOTATION_NAMES_VALUE
    )),
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
    ANNOTATION_TYPE_EXPRESSION: 'expression',
    ANNOTATION_TYPE_FLOAT: 'float',
    ANNOTATION_TYPE_ATTACHMENT : 'attachment',
    
    ANNOTATION_TYPE_SELF_CLIENT: 'client',
    ANNOTATION_TYPE_SELF_INTERACTION_EVENT: 'interaction_event',
    ANNOTATION_TYPE_SELF_TARGET: 'target',
    ANNOTATION_TYPE_SELF_VALUE: 'value',
}

TYPE_ANNOTATION_TO_ANNOTATION_TYPE = {
    # Generic
    str: (ANNOTATION_TYPE_STR, None),
    int: (ANNOTATION_TYPE_INT, None),
    bool: (ANNOTATION_TYPE_BOOL, None),
    ClientUserBase: (ANNOTATION_TYPE_USER, None),
    UserBase: (ANNOTATION_TYPE_USER, None),
    User: (ANNOTATION_TYPE_USER, None),
    Role: (ANNOTATION_TYPE_ROLE, None),
    Channel: (ANNOTATION_TYPE_CHANNEL, None),
    float: (ANNOTATION_TYPE_FLOAT, None),
    Attachment: (ANNOTATION_TYPE_ATTACHMENT, None),
    
    # Internal
    Client: (ANNOTATION_TYPE_SELF_CLIENT, None),
    InteractionEvent: (ANNOTATION_TYPE_SELF_INTERACTION_EVENT, None),
}

ANNOTATION_TYPE_TO_CONVERTER = {
    ANNOTATION_TYPE_STR: (converter_str, False),
    ANNOTATION_TYPE_INT: (converter_int, False),
    ANNOTATION_TYPE_BOOL: (converter_bool, False),
    ANNOTATION_TYPE_USER: (converter_user, False),
    ANNOTATION_TYPE_USER_ID: (converter_snowflake, False),
    ANNOTATION_TYPE_ROLE: (converter_role, False),
    ANNOTATION_TYPE_ROLE_ID: (converter_snowflake, False),
    ANNOTATION_TYPE_CHANNEL: (converter_channel, False),
    ANNOTATION_TYPE_CHANNEL_ID: (converter_snowflake, False),
    ANNOTATION_TYPE_NUMBER: (converter_int, False),
    ANNOTATION_TYPE_MENTIONABLE: (converter_mentionable, False),
    ANNOTATION_TYPE_MENTIONABLE_ID: (converter_snowflake, False),
    ANNOTATION_TYPE_EXPRESSION: (converter_expression, False),
    ANNOTATION_TYPE_FLOAT: (converter_float, False),
    ANNOTATION_TYPE_ATTACHMENT: (converter_attachment, False),
    
    ANNOTATION_TYPE_SELF_CLIENT: (converter_self_client, True),
    ANNOTATION_TYPE_SELF_INTERACTION_EVENT: (converter_self_interaction_event, True),
    ANNOTATION_TYPE_SELF_TARGET: (converter_self_interaction_target, True),
    ANNOTATION_TYPE_SELF_VALUE: (converter_self_interaction_value, True)
}

INTERNAL_ANNOTATION_TYPES = frozenset((
    ANNOTATION_TYPE_SELF_CLIENT,
    ANNOTATION_TYPE_SELF_INTERACTION_EVENT,
))

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
    ANNOTATION_TYPE_EXPRESSION: ApplicationCommandOptionType.string,
    ANNOTATION_TYPE_FLOAT: ApplicationCommandOptionType.float,
    ANNOTATION_TYPE_ATTACHMENT: ApplicationCommandOptionType.attachment,
    
    ANNOTATION_TYPE_SELF_CLIENT: ApplicationCommandOptionType.none,
    ANNOTATION_TYPE_SELF_INTERACTION_EVENT: ApplicationCommandOptionType.none,
    ANNOTATION_TYPE_SELF_TARGET: ApplicationCommandOptionType.none,
    ANNOTATION_TYPE_SELF_VALUE: ApplicationCommandOptionType.none,
}

ANNOTATION_TYPE_TO_REPRESENTATION = {
    ANNOTATION_TYPE_STR: 'string',
    ANNOTATION_TYPE_INT: 'integer',
    ANNOTATION_TYPE_BOOL: 'bool',
    ANNOTATION_TYPE_USER: 'user',
    ANNOTATION_TYPE_USER_ID: 'user',
    ANNOTATION_TYPE_ROLE: 'role',
    ANNOTATION_TYPE_ROLE_ID: 'role',
    ANNOTATION_TYPE_CHANNEL: 'channel',
    ANNOTATION_TYPE_CHANNEL_ID: 'channel',
    ANNOTATION_TYPE_NUMBER: 'integer',
    ANNOTATION_TYPE_MENTIONABLE: 'mentionable',
    ANNOTATION_TYPE_MENTIONABLE_ID : 'mentionable',
    ANNOTATION_TYPE_EXPRESSION: 'expression',
    ANNOTATION_TYPE_FLOAT: 'float',
    ANNOTATION_TYPE_ATTACHMENT: 'attachment',
}


ANNOTATION_AUTO_COMPLETE_AVAILABILITY = frozenset((
    ANNOTATION_TYPE_STR,
    ANNOTATION_TYPE_INT,
    ANNOTATION_TYPE_EXPRESSION,
    ANNOTATION_TYPE_NUMBER,
    ANNOTATION_TYPE_FLOAT,
))


class RegexMatcher(RichAttributeErrorBaseType):
    """
    `custom_id` matcher for component commands.
    
    Attributes
    ----------
    pattern : `Re.Pattern`
        The used regex pattern.
    is_group_dict_pattern : `bool`
        Whether the regex pattern is group dict based.
    """
    __slots__ = ('pattern', 'is_group_dict_pattern')
    
    def __new__(cls, regex_pattern):
        """
        Creates a ``RegexMatcher`` from the given parameters.
        
        Parameters
        ----------
        regex_pattern : `re.Pattern`
            Regex pattern to get details of.
        
        Raises
        ------
        ValueError
            Regex pattern with mixed dict groups and non-dict groups are disallowed.
        """
        group_count = regex_pattern.groups
        group_dict = regex_pattern.groupindex
        group_dict_length = len(group_dict)
        
        if group_dict_length and (group_dict_length != group_count):
            raise ValueError(
                f'Regex patterns with mixed dict groups and non-dict groups are disallowed, got '
                f'{regex_pattern!r}.'
            )
        
        if group_dict_length:
            is_group_dict_pattern = True
        else:
            is_group_dict_pattern = False
        
        self = object.__new__(cls)
        self.pattern = regex_pattern
        self.is_group_dict_pattern = is_group_dict_pattern
        return self
    
    
    def __call__(self, string):
        """
        Tries to math the string.
        
        Parameters
        ----------
        string : `str`
            The string to match.
        
        Returns
        -------
        regex_match : `None`, ``RegexMatch``
            The matched regex if any.
        """
        matched = self.pattern.fullmatch(string)
        if matched is None:
            return None
        
        is_group_dict_pattern = self.is_group_dict_pattern
        if is_group_dict_pattern:
            groups = matched.groupdict()
        else:
            groups = matched.groups()
        
        return RegexMatch(groups, is_group_dict_pattern)
    
    
    def __repr__(self):
        """Returns the pattern's representation."""
        return f'<{self.__class__.__name__} pattern={self.pattern.pattern}>'
    
    
    def __hash__(self):
        """Returns the regex matcher's hash value."""
        return hash(self.pattern)
    
    
    def __eq__(self, other):
        """Returns whether the two regex matchers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.pattern == other.pattern:
            return True
        
        return False


def check_component_converters_satisfy_string(parameter_converters):
    """
    Checks whether the given parameter converters satisfy string.
    
    Parameters
    ----------
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters to check.
    
    Raises
    -------
    ValueError
        If a converter is not satisfied.
    """
    for parameter_converter in parameter_converters:
        if isinstance(parameter_converter, InternalParameterConverter):
            continue
        
        if not parameter_converter.required:
            continue
        
        raise ValueError(
            f'Parameter {parameter_converter.parameter_name!r} is not satisfied by string `custom_id`-s.'
        )
    
    return True


def check_component_converters_satisfy_regex(parameter_converters, regex_matcher):
    """
    Checks whether the given parameter converters satisfy a regex matcher.
    
    Parameters
    ----------
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters to check.
    regex_matcher : ``RegexMatcher``
        The matcher to check whether is satisfied.
    
    Raises
    -------
    ValueError
        If a converter is not satisfied.
    """
    if regex_matcher.is_group_dict_pattern:
        required_parameters = set(regex_matcher.pattern.groupindex)
        for parameter_converter in parameter_converters:
            if isinstance(parameter_converter, InternalParameterConverter):
                continue
            
            if not parameter_converter.required:
                continue
            
            try:
                required_parameters.remove(parameter_converter.name)
            except KeyError:
                pass
            else:
                continue
            
            unsatisfied = parameter_converter
            break
        else:
            unsatisfied = None
    else:
        parameters_to_satisfy = regex_matcher.pattern.groups
        for parameter_converter in parameter_converters:
            if isinstance(parameter_converter, InternalParameterConverter):
                continue
            
            if not parameter_converter.required:
                continue
            
            if parameters_to_satisfy == 0:
                unsatisfied = parameter_converter
                break
            
            parameters_to_satisfy -= 1
            continue
        else:
            unsatisfied = None
    
    if (unsatisfied is not None):
        raise ValueError(
            f'Parameter {unsatisfied.parameter_name!r} is not satisfied by regex pattern: '
            f'{regex_matcher.pattern.pattern!r}.'
        )


class RegexMatch(RichAttributeErrorBaseType):
    """
    Matched regex pattern by ``RegexMatcher``.
    
    Attributes
    ----------
    is_group_dict : `bool`
        Whether `groups` is a dictionary.
    groups : `tuple` of `str`, `dict` of (`str`, `str`) items
        The matched groups.
    """
    __slots__ = ('is_group_dict', 'groups')
    
    def __new__(cls, groups, is_group_dict):
        """
        Creates a new ``RegexMatcher`` from the given parameters.
    
        Parameters
        ----------
        is_group_dict : `bool`
            Whether `groups` is a dictionary.
        groups : `tuple` of `str`, `dict` of (`str`, `str`) items
            The matched groups.
        """
        self = object.__new__(cls)
        self.groups = groups
        self.is_group_dict = is_group_dict
        return self
    
    def __repr__(self):
        """Returns the regex match's representation."""
        return f'<{self.__class__.__name__} groups={self.groups!r}>'


class SlashParameter(RichAttributeErrorBaseType):
    """
    A class, which can be used familiarly to tuples as an annotation, but it supports rich parameters as well.
    
    Attributes
    ----------
    autocomplete : `None`, `CoroutineFunction`
        Auto complete function for the parameter.
    channel_types : `None`, `iterable` of (`int`, ``ChannelType``)
        The accepted channel types.
    description : `None`, `str` = `None`, Optional
        Description for the annotation.
    max_length : `None`, `int`
        The maximum input length allowed for this option.
    max_value : `None`, `int`, `float`
        The maximal accepted value by the parameter.
    min_length : `None`, `int`
        The minimum input length allowed for this option.
    min_value : `None`, `int`, `float`
        The minimal accepted value by the parameter.
    name : `None`, `str` = `None`, Optional
        Name to use instead of the parameter's.
    type_or_choice : `None`, `str`, `type`, `list`, `dict`
        The annotation's value to use.
    """
    __slots__ = (
        'autocomplete', 'channel_types', 'description', 'max_length', 'max_value', 'min_length', 'min_value', 'name',
        'type_or_choice'
    )
    
    def __new__(
        cls,
        type_or_choice = None,
        description = None,
        name = None,
        *,
        autocomplete = None,
        channel_types = None,
        max_length = None,
        max_value = None,
        min_length = None,
        min_value = None,
    ):
        """
        Creates a new ``Parameter``.
        
        Parameters
        ----------
        type_or_choice : `None`, `str`, `type`, `list`, `dict` = `None`, Optional
            The annotation's value to use.
        description : `None`, `str` = `None`, Optional
            Description for the annotation.
        name : `None`, `str` = `None`, Optional
            Name to use instead of the parameter's.
        autocomplete : `None`, `CoroutineFunction` = `None`, Optional (Keyword only)
            Auto complete function for the parameter.
        channel_types : `None`, `iterable` of (`int`, ``ChannelType``) = `None`, Optional (Keyword only)
            The accepted channel types.
        max_length : `None`, `int` = `None`, Optional (Keyword only)
            The maximum input length allowed for this option.
        max_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The maximal accepted value by the parameter.
        min_length : `None`, `int` = `None`, Optional (Keyword only)
            The minimum input length allowed for this option.
        min_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The minimal accepted value by the parameter.
        """
        self = object.__new__(cls)
        self.autocomplete = autocomplete
        self.channel_types = channel_types
        self.description = description
        self.max_length = max_length
        self.max_value = max_value
        self.min_length = min_length
        self.min_value = min_value
        self.name = name
        self.type_or_choice = type_or_choice
        return self
    
    
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        autocomplete = self.autocomplete
        if (autocomplete is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' autocomplete = ')
            repr_parts.append(repr(autocomplete))
        
        channel_types = self.channel_types
        if (channel_types is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' channel_types = ')
            repr_parts.append(repr(channel_types))
        
        description = self.description
        if (description is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' description = ')
            repr_parts.append(repr(description))
        
        # max_length
        max_length = self.max_length
        if (max_length is not None) and (max_length != 0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' max_length = ')
            repr_parts.append(repr(max_length))
        
        max_value = self.max_value
        if (max_value is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' max_value = ')
            repr_parts.append(repr(max_value))
        
        # min_length
        min_length = self.min_length
        if (min_length is not None) and (min_length != 0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' min_length = ')
            repr_parts.append(repr(min_length))
        
        min_value = self.min_value
        if (min_value is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' min_value = ')
            repr_parts.append(repr(min_value))
        
        name = self.name
        if (name is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' name = ')
            repr_parts.append(repr(name))
        
        type_or_choice = self.type_or_choice
        if (type_or_choice is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' type_or_choice = ')
            repr_parts.append(repr(type_or_choice))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def preprocess_channel_types(channel_types):
    """
    Preprocesses the given channel type values.
    
    Parameters
    ----------
    channel_types : `None`, `iterable` of (`int`, ``ChannelType``)
        Channel types to limit a slash command parameter to.
    
    Returns
    -------
    processed_channel_types : `None`, `tuple` of ``ChannelType``
    
    Raises
    ------
    TypeError
        If `channel_types` is neither `None` nor `iterable` of `int`.
    ValueError
        If received `channel_types` from both `type_or_choice` and `channel_types` parameters.
    """
    if (channel_types is None):
        processed_channel_types = None
    else:
        processed_channel_types = None
        
        if (getattr(type(channel_types), '__iter__', None) is None):
            raise TypeError(
                f'`channel_types` can be `None`, `iterable`, got '
                f'{channel_types.__class__.__anme__}; {channel_types!r}.'
            )
        
        for channel_type in channel_types:
            if isinstance(channel_type, ChannelType):
                pass
            
            elif isinstance(channel_type, int):
                channel_type = ChannelType.get(channel_type)
            
                pass
            
            else:
                raise TypeError(
                    f'`channel_types` can contain `int`, `{ChannelType.__name__}` elements, got '
                    f'{channel_type.__class__.__name__}; {channel_type!r}; channel_types = {channel_types!r}.'
                )
            
            if processed_channel_types is None:
                processed_channel_types = set()
            
            processed_channel_types.add(channel_type)
    
        if processed_channel_types:
            processed_channel_types = tuple(sorted(processed_channel_types))
        else:
            processed_channel_types = None
    
    return processed_channel_types


def postprocess_channel_types(processed_channel_types, parsed_channel_types):
    """
    Selects which channel type should be used from the processed ones by using the `channel_types` field` or by the
    ones processed from the `type_or_choice` field.
    
    Parameters
    ----------
    processed_channel_types : `None`, `tuple` of ``ChannelType``
        Channel types detected from `channel_types` field.
    parsed_channel_types : `None`, `tuple` of ``ChannelType``
        Channel types processed from the `type_or_choice` field.
    
    Returns
    -------
    channel_types : `None`, `tuple` of ``ChannelType``
        The selected channel types.
    
    Raises
    ------
    ValueError
        If both `processed_channel_types` and `parsed_channel_types` define channel types.
    """
    if (parsed_channel_types is not None):
        if (processed_channel_types is not None):
            raise ValueError(
                f'`received `channel_types` from both `type_or_choice` and `channel_types` '
                f'parameters, got {parsed_channel_types!r} and {processed_channel_types!r}.'
            )
        
        channel_types = parsed_channel_types
    else:
        channel_types = processed_channel_types
    
    return channel_types


def process_max_and_min_value(type_, value, value_name):
    """
    Processes max and min values.
    
    Since the library defaults `integer` fields to `string` ones, `integer` fields are translated to `number` to
    enable using `min_value` and `max_value` with them.
    
    Parameters
    ----------
    type_ : `int`
        The value's type's respective internal identifier.
    value : `None`, `int`, `float`
        The given value.
    value_name : `str`
        The value's name. Used when generating. exception messages.
    
    Returns
    -------
    type_ : `int`
        The value's type's respective internal identifier.
    value : `None`, `int`, `float`
        The min or max value.
    
    Raises
    ------
    TypeError
        If `type_`'s value is incorrect.
    ValueError
        The respective `type_` do not supports max and min values.
    """
    if (value is not None):
        if type_ == ANNOTATION_TYPE_NUMBER:
            expected_type = int
        
        elif type_ == ANNOTATION_TYPE_FLOAT:
            expected_type = float
        
        elif type_ == ANNOTATION_TYPE_INT:
            expected_type = int
            type_ = ANNOTATION_TYPE_NUMBER
        
        else:
            raise ValueError(
                f'`{value_name}` is not applicable for `{ANNOTATION_TYPE_TO_REPRESENTATION[type_]}` parameters.'
            )
        
        if type(value) is expected_type:
            pass
        elif isinstance(value, expected_type):
            value = expected_type(value)
        else:
            raise TypeError(
                f'`{value_name}` is accepted as {expected_type.__name__} instance if type is specified '
                f'as `{ANNOTATION_TYPE_TO_REPRESENTATION[type_]}`, got {value.__class__.__name__}; {value!r}.'
            )
    
    return type_, value


def process_max_length(max_length, option_type):
    """
    Processes the given `max_length` field.
    
    Parameters
    ----------
    max_length : `None`, `int`
        The maximum input length allowed for this option.
    
    option_type : ``ApplicationCommandOptionType``
        The respective option's type.
    
    Returns
    -------
    max_length : `int`
        The processed value.
    
    Raises
    ------
    TypeError
        - If `max_length`'s type is incorrect.
    ValueError
        - If `max_length`'s value is incorrect.
    """
    max_length = validate_max_length(max_length)
    if (
        (max_length != APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT) and
        (option_type is not ApplicationCommandOptionType.string)
    ):
        raise ValueError(
            f'`max_length` is only applicable for `{ApplicationCommandOptionType.__name__}.string`, got '
            f'max_length = {max_length!r}, option_type = {option_type.name}.'
        )
    
    return max_length


def process_min_length(min_length, option_type):
    """
    Processes the given `min_length` field.
    
    Parameters
    ----------
    min_length : `None`, `int`
        The minimum input length allowed for this option.
    
    option_type : ``ApplicationCommandOptionType``
        The respective option's type.
    
    Returns
    -------
    min_length : `int`
        The processed value.
    
    Raises
    ------
    TypeError
        - If `min_length`'s type is incorrect.
    ValueError
        - If `min_length`'s value is incorrect.
    """
    min_length = validate_min_length(min_length)
    if (
        (min_length != APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT) and
        (option_type is not ApplicationCommandOptionType.string)
    ):
        raise ValueError(
            f'`min_length` is only applicable for `{ApplicationCommandOptionType.__name__}.string`, got '
            f'min_length = {min_length!r}, option_type = {option_type.name}.'
        )
    
    return min_length


def create_annotation_choice_from_int(value):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    value : `int`
        The validated annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `int`)
        The validated annotation choice.
    """
    return (str(value), value)


def create_annotation_choice_from_float(value):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    value : `int`
        The validated annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, `float`)
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
    choice : `tuple` (`str`, `str`)
        The validated annotation choice.
    """
    # make sure
    return (value, value)


def parse_annotation_choice_from_enum_member(enum_member):
    """
    Creates a choice form an enum member.
    
    Parameters
    -------
    enum_member : `Enum`
        The member of an enum.
    
    Returns
    -------
    choice : `tuple` (`str`, `Enum`)
        The validated choice.
    
    Raises
    ------
    TypeError
        - If the choice's name's type is incorrect.
        - If the choice's value's type is incorrect.
    ValueError
        - If the choice's length is invalid.
    """
    _validate_choice_name(enum_member.name)
    _validate_choice_value(enum_member.value)
    
    return enum_member.name, enum_member


def _validate_choice_name(name):
    """
    Validates the given choice's name.
    
    Parameters
    ----------
    name : `str`
        The choice's name.
    
    Raises
    ------
    TypeError
        - If the `name`'s type is incorrect.
    """
    if not isinstance(name, str):
        raise TypeError(
            f'`annotation-name` can be `str`, got {name.__class__.__name__}; {name!r}.'
        )


def _validate_choice_value(value):
    """
    Validates the given choice's value.
    
    Parameters
    ----------
    value : `str`, `int`, `float`
        The choice's value.
    
    Raises
    ------
    TypeError
        - If the `value`'s type is incorrect.
    """

    if not isinstance(value, (str, int, float)):
        raise TypeError(
            f'`annotation-value` can be `str`, `int`, `float`, got {value.__class__.__name__}; {value!r}.'
        )


def parse_annotation_choice_from_tuple(annotation):
    """
    Creates an annotation choice form a tuple.
    
    Parameters
    -------
    annotation : `tuple`
        Annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, (`str`, `int`, `float`))
        The validated annotation choice.
    
    Raises
    ------
    TypeError
        - If the choice's name's type is incorrect.
        - If the choice's value's type is incorrect.
    ValueError
        - If the choice's length is invalid.
    """
    annotation_length = len(annotation)
    if (annotation_length < 1 or annotation_length > 2):
        raise ValueError(
            f'`tuple` annotation length can be in range [1:2], got {annotation_length!r}; {annotation!r}.'
        )
    
    if annotation_length == 1:
        value = annotation[0]
        if isinstance(value, str):
            return create_annotation_choice_from_str(value)
        
        if isinstance(value, int):
            return create_annotation_choice_from_int(value)
        
        if isinstance(value, float):
            return create_annotation_choice_from_float(value)
        
        raise TypeError(
            f'`annotation-value` can be `str`, `int`, `float`, got {value.__class__.__name__}; {value!r}.'
        )
    
    # if annotation_length == 2:
    name, value = annotation
    
    _validate_choice_name(name)
    _validate_choice_value(value)
    
    return (name, value)


def parse_annotation_choice(annotation_choice):
    """
    Parses annotation choice.
    
    Parameters
    ----------
    annotation_choice : `tuple`, `str`, `int`, `float`
        A choice.
    
    Returns
    -------
    choice : `tuple` (`str`, (`str`, `int`, `float`))
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
    
    if isinstance(annotation_choice, float):
        return create_annotation_choice_from_float(annotation_choice)
    
    raise TypeError(
        f'`annotation-choice` can be `tuple`, `str`, `int`  or `float`, got '
        f'{annotation_choice.__class__.__name__}; {annotation_choice!r}.'
    )


def parse_annotation_type_and_choice(annotation_value, parameter_name):
    """
    Parses annotation type and choices out from an annotation value.
    
    Parameters
    ----------
    annotation_value : `str`, `type`, `list`, `dict`, `iterable`.
        The annotation's value.
    parameter_name : `str`
        The parameter's name.
    
    Returns
    -------
    annotation_type : `int`
        Internal identifier about the annotation.
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        Choices if applicable.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    
    TypeError
        - If `annotation_value` is `list`, but it's elements do not match the `tuple`
            (`str`, `str`, `int`, `float`) pattern.
        - If `annotation_value` is `dict`, but it's items do not match the
            (`str`, `str`, `int`, `float`) pattern.
        - If `annotation_value` is unexpected.
    ValueError
        - If `annotation_value` is `str`, but not any of the expected ones.
        - If `annotation_value` is `type`, but not any of the expected ones.
        - If `choice` amount is out of the expected range [1:25].
        - If a `choice` name is duped.
        - If a `choice` values are mixed types.
    """
    if isinstance(annotation_value, str):
        annotation_value = annotation_value.lower()
        try:
            annotation_type, channel_types = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(
                f'Parameter `{parameter_name}` has annotation not referring to any expected type, '
                f'got {annotation_value!r}.'
            ) from None
        
        choices = None
        choice_enum_type = None
    
    elif (isinstance(annotation_value, type) and not issubclass(annotation_value, Enum)):
        try:
            annotation_type, channel_types = TYPE_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(
                f'Parameter `{parameter_name}` has annotation not referring to any expected type, '
                f'got {annotation_value!r}.'
            ) from None
        
        choices = None
        choice_enum_type = None
    
    else:
        choice_elements = []
        if isinstance(annotation_value, list):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_enum_type = None
        
        elif isinstance(annotation_value, set):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_elements.sort()
            
            choice_enum_type = None
        
        elif isinstance(annotation_value, dict):
            for annotation_choice in annotation_value.items():
                choice_element = parse_annotation_choice_from_tuple(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_elements.sort()
            
            choice_enum_type = None
        
        elif isinstance(annotation_value, type) and issubclass(annotation_value, Enum):
            for enum_member in annotation_value.__members__.values():
                choice_element = parse_annotation_choice_from_enum_member(enum_member)
                choice_elements.append(choice_element)
            
            choice_elements.sort()
            
            choice_enum_type = annotation_value
        
        elif hasattr(type(annotation_value), '__iter__'):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
            
            choice_enum_type = None
        
        else:
            raise TypeError(
                f'Parameter `{parameter_name}` has annotation not set neither as `tuple`, `str`, `type`, '
                f'`list`, `set`, `dict`, got {annotation_value.__class__.__name__}; {annotation_value!r}.'
            )
        
        # Filter dupe names
        dupe_checker = set()
        length = 0
        for name, value in choice_elements:
            dupe_checker.add(name)
            new_length = len(dupe_checker)
            if new_length == length:
                raise ValueError(
                    f'Duped choice name in annotation: {parameter_name!r}.'
                )
            
            length = new_length
        
        # Check annotation type
        expected_type = None
        for name, value in choice_elements:
            if (choice_enum_type is not None):
                value = value.value
            
            if isinstance(value, str):
                type_ = str
            
            elif isinstance(value, int):
                type_ = int
            
            else:
                type_ = float
            
            if expected_type is None:
                expected_type = type_
                continue
            
            if expected_type is not type_:
                raise ValueError(
                    f'Mixed choice value types in annotation: {parameter_name!r}.'
                )
        
        if expected_type is str:
            annotation_type = ANNOTATION_TYPE_STR
        elif expected_type is int:
            annotation_type = ANNOTATION_TYPE_INT
        else:
            annotation_type = ANNOTATION_TYPE_FLOAT
        
        choices = {value: name for name, value in choice_elements}
        
        channel_types = None
    
    return annotation_type, choice_enum_type, choices, channel_types


def parse_annotation_description(description, parameter_name):
    """
    Parses an annotation's description.
    
    Parameters
    ----------
    description : `str`
        The description of an annotation.
    parameter_name : `str`
        The parameter's name.
    
    Returns
    -------
    description : `str`
    
    Raises
    ------
    TypeError
        - If `description`'s is not `str`.
    ValueError
        - If `description`'s length is out of the expected range [2:100].
    """
    if type(description) is str:
        pass
    elif isinstance(description, str):
        description = str(description)
    else:
        raise TypeError(
            f'Parameter `{parameter_name}` has annotation description not as `str`, got '
            f'{description.__class__.__name__}; {description!r}.'
        )
    
    description_length = len(description)
    if (
        description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN or
        description_length > APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX
    ):
        raise ValueError(
            f'Parameter `{parameter_name}` annotation\'s description\'s length is out of the expected '
            f'range [{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:'
            f'{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], got {description_length}; {description!r}.'
        )
    
    description = normalize_description(description)
    return description


def parse_annotation_name(name, parameter_name):
    """
    Parses an annotation's name.
    
    Parameters
    ----------
    name : `str`
        The name of an annotation.
    parameter_name : `None`, `str`
        The parameter's name.
    
    Returns
    -------
    name : `str`
    
    Raises
    ------
    TypeError
        If `name`'s is neither `None`, `str`.
    """
    if name is None:
        name = parameter_name
    elif type(name) is str:
        pass
    elif isinstance(name, str):
        name = str(name)
    else:
        raise TypeError(
            f'`Parameter `{parameter_name}` has `name` given as non `str`, got '
            f'{name.__class__.__name__}; {name!r}.'
        )
    
    name = raw_name_to_display(name)
    
    return name


def parse_annotation_tuple(parameter, annotation_tuple):
    """
    Parses an annotated tuple.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    annotation_tuple : `tuple`
        The annotated tuple.
    
    Returns
    -------
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        Parameter's choices.
    description : `str`
        Parameter's description.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    max_value : `None`, `int`, `float`
        The maximal accepted value.
    min_value : `None`, `int`, `float`
        The minimal accepted value.
    autocomplete : `None`, `CoroutineFunction`
        Autocomplete function.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    max_length : `int`
        The maximum input length allowed for this option.
    min_length : `int`
        The minimum input length allowed for this option.
    
    Raises
    ------
    ValueError
        - If `parameter` annotation tuple's length is out of range [2:3].
        - If `parameter` annotation's refers to an internal type.
    """
    annotation_tuple_length = len(annotation_tuple)
    if annotation_tuple_length not in (1, 2, 3):
        raise ValueError(
            f'Parameter `{parameter.name}` has annotation as `tuple`, but it\'s length is not in '
            f'range [1:3], got {annotation_tuple_length!r}; {annotation_tuple!r}.'
        )
    
    annotation_value = annotation_tuple[0]
    annotation_type, choice_enum_type, choices, channel_types = parse_annotation_type_and_choice(
        annotation_value, parameter.name
    )
    
    if annotation_type in INTERNAL_ANNOTATION_TYPES:
        raise ValueError(
            f'`Internal annotations cannot be given inside of a tuple, got annotation for: '
            f'{ANNOTATION_TYPE_TO_STR_ANNOTATION[annotation_type]!r}; annotation={annotation_tuple!r}.'
        )
    
    if annotation_tuple_length > 1:
        description = annotation_tuple[1]
    else:
        description = None
    
    if (description is not None):
        description = parse_annotation_description(description, parameter.name)
    
    if annotation_tuple_length > 2:
        name = annotation_tuple[2]
    else:
        name = None
    
    name = parse_annotation_name(name, parameter.name)
    return choices, description, name, annotation_type, channel_types, None, None, None, choice_enum_type, 0, 0


def parse_annotation_slash_parameter(parameter, slash_parameter):
    """
    Parses an annotated ``SlashParameter``.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    slash_parameter : ``SlashParameter``
        The respective parameter's representation.
    
    Returns
    -------
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`)) items
        Parameter's choices.
    description : `str`
        Parameter's description.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    max_value : `None`, `int`, `float`
        The maximal accepted value.
    min_value : `None`, `int`, `float`
        The minimal accepted value.
    autocomplete : `None`, `CoroutineFunction`
        Autocomplete function.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    max_length : `int`
        The maximum input length allowed for this option.
    min_length : `int`
        The minimum input length allowed for this option.
    
    Raises
    ------
    TypeError
        - If a parameter's type is unexpected.
        - If `parameter_type_or_choice` is unexpected.
    ValueError
        - If a parameter's value is unexpected.
        - If received `channel_types` from both `type_or_choice` and `channel_types` parameters.
    """
    type_or_choice = slash_parameter.type_or_choice
    if type_or_choice is None:
        type_or_choice = parameter.name
    
    type_, choice_enum_type, choices, parsed_channel_types = parse_annotation_type_and_choice(
        type_or_choice, parameter.name
    )
    
    processed_channel_types = preprocess_channel_types(slash_parameter.channel_types)
    channel_types = postprocess_channel_types(processed_channel_types, parsed_channel_types)
    
    max_length = process_max_length(slash_parameter.max_length, ANNOTATION_TYPE_TO_OPTION_TYPE[type_])
    min_length = process_min_length(slash_parameter.min_length, ANNOTATION_TYPE_TO_OPTION_TYPE[type_])
    
    type_, max_value = process_max_and_min_value(type_, slash_parameter.max_value, 'max_value')
    type_, min_value = process_max_and_min_value(type_, slash_parameter.min_value, 'min_value')
    
    description = slash_parameter.description
    if (description is not None):
        description = parse_annotation_description(description, parameter.name)
    
    name = parse_annotation_name(slash_parameter.name, parameter.name)
    
    return (
        choices, description, name, type_, channel_types, max_value, min_value, slash_parameter.autocomplete,
        choice_enum_type, max_length, min_length
    )


def is_pep_593_typing(annotation_value):
    """
    Returns whether the given annotation is a rich shit typing.
    
    Parameters
    ----------
    annotation_value : `object`
        The parameter to decide whether it is a ``pep 593 typing:https://peps.python.org/pep-0593/``.
    
    Returns
    -------
    is_pep_593_typing : `bool`
    """
    try:
        parameters = getattr(annotation_value, '__args__')
    except AttributeError:
        return False
    
    if not isinstance(parameters, tuple):
        return False
    
    try:
        metadata = getattr(annotation_value, '__metadata__')
    except AttributeError:
        return False
    
    if not isinstance(metadata, tuple):
        return False
    
    return True


def parse_pep_593_typing(parameter, annotation_value):
    """
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    annotation_value : `object`
        The parameter's annotation's value.
    
    Returns
    -------
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        Parameter's choices.
    description : `str`
        Parameter's description.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    max_value : `None`, `int`, `float`
        The maximal accepted value.
    min_value : `None`, `int`, `float`
        The minimal accepted value.
    autocomplete : `None`, `CoroutineFunction`
        Autocomplete function.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    max_length : `int`
        The maximum input length allowed for this option.
    min_length : `int`
        The minimum input length allowed for this option.
    
    Raises
    ------
    ValueError
        - If `parameter` annotation tuple's length  is out of range [2:3].
        - If `parameter` annotation tuple refers to an internal type.
    TypeError
        - If the parameter's type refers to an unknown type or string value.
    """
    metadata = annotation_value.__metadata__
    metadata_length = len(metadata)
    
    if metadata_length == 0:
        # Nice try, wont work!
        return parse_annotation_fallback(parameter, None)
    
    if metadata_length == 1:
        metadata_value = metadata[0]
        if isinstance(metadata_value, tuple):
            if len(metadata_value) == 0:
                return parse_annotation_fallback(parameter, None)
            else:
                return parse_annotation_tuple(parameter, metadata_value)
        
        elif isinstance(metadata_value, SlashParameter):
            return parse_annotation_slash_parameter(parameter, metadata_value)
        
        return parse_annotation_fallback(parameter, metadata_value)
    
    return parse_annotation_tuple(parameter, metadata)


def parse_annotation_fallback(parameter, annotation_value):
    """
    Tries to parse annotation from the given value.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    annotation_value : `None`, `object`
        The annotated value to interpret.
    
    Returns
    -------
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        Parameter's choices.
    description : `None`, `str`
        Parameter's description.
        
        > Returned as `None` for internal parameters or if `description` could not be detected.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    max_value : `None`, `int`, `float`
        The maximal accepted value.
    min_value : `None`, `int`, `float`
        The minimal accepted value.
    autocomplete : `None`, `CoroutineFunction`
        Autocomplete function.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    max_length : `int`
        The maximum input length allowed for this option.
    min_length : `int`
        The minimum input length allowed for this option.
    
    Raises
    ------
    TypeError
        Parameter's type refers to an unknown type or string value.
    """
    if annotation_value is None:
        annotation_value = parameter.name
    
    if not isinstance(annotation_value, (str, type)):
        raise TypeError(
            f'Parameter `{parameter.name}` is not `tuple`, `str`, `str`, got '
            f'{annotation_value.__class__.__name__}; {annotation_value!r}.'
        )
    else:
        annotation_type = parse_annotation_internal(annotation_value)
        if annotation_type is None:
            annotation_type, choice_enum_type, choices, channel_types = parse_annotation_type_and_choice(
                annotation_value, parameter.name
            )
        else:
            choice_enum_type = None
            choices = None
            channel_types = None
    
    return choices, None, parameter.name, annotation_type, channel_types, None, None, None, choice_enum_type, 0, 0


def parse_annotation_internal(annotation):
    """
    Tries to check whether the given annotation refers to an internal type or not.
    
    Parameters
    ----------
    annotation : `str`, `type`
        The annotation to check.
    
    Returns
    -------
    annotation_type : `None`, `int`
        The parsed annotation type. Returns `None` if the annotation type not refers to an internal type.
    """
    if isinstance(annotation, type):
        if issubclass(annotation, Client):
            annotation_type = ANNOTATION_TYPE_SELF_CLIENT
        elif issubclass(annotation, InteractionEvent):
            annotation_type = ANNOTATION_TYPE_SELF_INTERACTION_EVENT
        else:
            annotation_type = None
    else:
        annotation = annotation.lower()
        if annotation in ANNOTATION_NAMES_CLIENT:
            annotation_type = ANNOTATION_TYPE_SELF_CLIENT
        elif annotation in ANNOTATION_NAMES_INTERACTION_EVENT:
            annotation_type = ANNOTATION_TYPE_SELF_INTERACTION_EVENT
        else:
            annotation_type = None
    
    return annotation_type


def parse_annotation(parameter):
    """
    Tries to parse an internal annotation referencing ``Client``, ``InteractionEvent``.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    
    Returns
    -------
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        Parameter's choices.
    description : `None`, `str`
        Parameter's description.
        
        > Returned as `None` for internal parameters or if `description` could not be detected.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    max_value : `None`, `int`, `float`
        The maximal accepted value.
    min_value : `None`, `int`, `float`
        The minimal accepted value.
    autocomplete : `None`, `CoroutineFunction`
        Autocomplete function.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    max_length : `int`
        The maximum input length allowed for this option.
    min_length : `int`
        The minimum input length allowed for this option.
    
    Raises
    ------
    ValueError
        - If `parameter` annotation tuple's length  is out of range [2:3].
        - If `parameter` annotation tuple refers to an internal type.
    TypeError
        - If the parameter's type refers to an unknown type or string value.
    """
    if not parameter.has_annotation:
        return parse_annotation_fallback(parameter, None)
        
    annotation_value = parameter.annotation
    if isinstance(annotation_value, tuple):
        if len(annotation_value) == 0:
            return parse_annotation_fallback(parameter, None)
        else:
            return parse_annotation_tuple(parameter, annotation_value)
    
    elif isinstance(annotation_value, SlashParameter):
        return parse_annotation_slash_parameter(parameter, annotation_value)
    
    elif is_pep_593_typing(annotation_value):
        return parse_pep_593_typing(parameter, annotation_value)
    
    return parse_annotation_fallback(parameter, annotation_value)


class ParameterConverter(RichAttributeErrorBaseType):
    """
    Base class for parameter converters.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    """
    __slots__ = ('parameter_name',)
    
    def __new__(cls, parameter_name):
        """
        Creates a new parameter converter from the given parameter.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter_name
        return self
    
    
    async def __call__(self, client, interaction_event, value):
        """
        Calls the parameter converter to convert the given `value` to it's desired state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective ``InteractionEvent``.
        interaction_event : ``InteractionEvent``
            The received application command interaction.
        value : `object`
            ``ApplicationCommandInteractionOption.value``.
        
        Returns
        -------
        converted_value : `None`, ``object``
            If conversion fails, always returns `None`.
        
        Raises
        ------
        SlashCommandParameterConversionError
            The parameter cannot be parsed.
        """
        pass
    
    
    def __repr__(self):
        """Returns the parameter converter's representation."""
        return f'<{self.__class__.__name__}, parameter_name = {self.parameter_name!r}>'
    
    
    def as_option(self):
        """
        Converts the parameter to an application command option if applicable.
        
        Returns
        -------
        option : `None`, ``ApplicationCommandOption``
        """
        pass
    
    
    def bind_parent(self, parent):
        """
        Binds the parent command to self.
        
        This method might be called for a few types of command functions to bind themselves to a few interactive
        parameters.
        
        Parameters
        ----------
        parent : `None`, ``SlashCommandFunction``
            The slasher application command function to bind to self.
        """
        pass


class RegexParameterConverter(ParameterConverter):
    """
    Regex parameter parsing for component `custom_id`.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    default : `object`
        Default value of the parameter.
    index : `int`
        the index of the regex pattern to take.
    required : `bool`
        Whether the parameter is required.
    """
    __slots__ = ('default', 'index', 'required')
    
    def __new__(cls, parameter, index):
        """
        Creates a new parameter converter from the given parameter.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The parameter to create converter from.
        index : `int`
            The parameter's index.
        """
        self = object.__new__(cls)
        self.index = index
        self.parameter_name = parameter.name
        self.required = parameter.has_default
        self.default = parameter.default
        return self
    
    
    @copy_docs(ParameterConverter.__call__)
    async def __call__(self, client, interaction_event, value):
        if value is None:
            converted_value = self.default
        else:
            groups = value.groups
            if value.is_group_dict:
                parameter_name = self.parameter_name
                try:
                    converted_value = groups[parameter_name]
                except KeyError:
                    converted_value = self.default
            else:
                index = self.index
                if index < len(groups):
                    converted_value = groups[index]
                else:
                    converted_value = self.default
        
        return converted_value
    
    
    @copy_docs(ParameterConverter.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' parameter_name = ',
            repr(self.parameter_name),
            ', index = ',
            repr(self.index),
        ]
        
        if not self.required:
            repr_parts.append(', default = ')
            repr_parts.append(repr(self.default))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class FormFieldKeywordParameterConverter(ParameterConverter):
    """
    Regex and string matcher and `custom_id` matching parameter parser for forms.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    annotation : `str`, `Pattern`
        Annotation defaulting to the parameter's name if required.
    default : `object`
        Default value of the parameter.
    matcher : `FunctionType`
        Matches interaction options based on their `custom_id`.
    """
    __slots__ = ('annotation', 'default', 'matcher')
    
    def __new__(cls, parameter):
        """
        Creates a new parameter converter used by form submit fields.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The parameter to create converter from.
        """
        # Default annotation to parameter name
        annotation = parameter.annotation
        if (annotation is None) or (not isinstance(annotation, (str, Pattern))):
            annotation = parameter.name
        
        if isinstance(annotation, str):
            matcher = cls._converter_string
        else:
            group_count = annotation.groups
            group_dict = annotation.groupindex
            group_dict_length = len(group_dict)
            
            if group_dict_length and (group_dict_length != group_count):
                raise ValueError(
                    f'Regex patterns with mixed dict groups and non-dict groups are disallowed, got '
                    f'{annotation!r}.'
                )
            
            if group_count:
                if group_dict_length:
                    matcher = cls._converter_regex_group_dict
                else:
                    matcher = cls._converter_regex_group_tuple
            else:
                matcher = cls._converter_regex
        
        self = object.__new__(cls)
        self.parameter_name = parameter.name
        self.annotation = annotation
        self.default = parameter.default
        self.matcher = matcher
        return self
    
    
    @copy_docs(ParameterConverter.__call__)
    async def __call__(self, client, interaction_event, value):
        return self.matcher(self, interaction_event)
    
    
    @copy_docs(ParameterConverter.__repr__)
    def __repr__(self):
        repr_parts =[
            '<',
            self.__class__.__name__,
            ' parameter_name = ',
            repr(self.parameter_name),
        ]
        
        repr_parts.append(', annotation = ')
        repr_parts.append(repr(self.annotation))
        
        repr_parts.append(', default = ')
        repr_parts.append(repr(self.default))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @staticmethod
    def _converter_string(converter, interaction_event):
        """
        String form submit interaction option value matcher.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        """
        value = interaction_event.get_value_for(converter.annotation)
        if (value is None):
            value = converter.default
        
        return value
    
    
    @staticmethod
    def _converter_regex(converter, interaction_event):
        """
        Regex form submit interaction option value matcher.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        return value
    
    
    @staticmethod
    def _converter_regex_group_dict(converter, interaction_event):
        """
        Regex form submit interaction option value matcher returning the matched group dictionary as well.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        groups : `dict` of (`str`, `str`) items
            The matched values by the regex pattern.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        groups = match.groupdict()
        return groups, value
    
    
    @staticmethod
    def _converter_regex_group_tuple(converter, interaction_event):
        """
        Regex form submit interaction option value matcher returning the matched group tuple as well.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        value : `object`
            The matched value or the converter's default value.
        groups : `tuple` of `str`
            The matched values by the regex pattern.
        """
        match, value = interaction_event.get_match_and_value(converter.annotation.fullmatch)
        if (value is None):
            value = converter.default
        
        groups = match.groups()
        return groups, value


class FormFieldMultiParameterConverter(FormFieldKeywordParameterConverter):
    """
    Regex and string matcher and `custom_id` matching multi parameter parser for forms.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    annotation : `str`, `Pattern`
        Annotation defaulting to the parameter's name if required.
    default : `object`
        Default value of the parameter.
    matcher : `FunctionType`
        Matches interaction options based on their `custom_id`.
    """
    __slots__ = ()
    
    @staticmethod
    def _converter_string(converter, interaction_event):
        """
        String form submit interaction option multi value matcher.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        values : `None`, `list` of `object`
            The matched values.
        """
        value = interaction_event.get_value_for(converter.annotation)
        
        if (value is None):
            values = None
        else:
            values = [value]
        
        return values
    
    
    @staticmethod
    def _converter_regex(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        values : `None`, `list` of `object`
            The matched values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            if (value is not None):
                if (values is None):
                    values = []
                
                values.append(value)
        
        return values
    
    
    @staticmethod
    def _converter_regex_group_dict(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher returning the matched group dictionaries as well.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups_and_values : `None`, `list` of `tuple` (`dict` of (`str`, `str`) items, `object`)
            The matched values from the field's `custom_id` and their values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            
            groups = match.groupdict()
            
            if (values is None):
                values = []
            
            values.append((groups, value))
       
        return values
    
    
    @staticmethod
    def _converter_regex_group_tuple(converter, interaction_event):
        """
        Regex form submit interaction option multi value matcher returning the matched group tuples as well.
        
        Parameters
        ----------
        converter : ``FormFieldKeywordParameterConverter``
            The parent converter instance using this function.
        interaction_event : ``InteractionEvent``
            A received interaction event.
        
        Returns
        -------
        groups_and_values : `None`, `list` of `tuple` (`tuple` of `str`, `object`)
            The matched values from the field's `custom_id` and their values.
        """
        values = None
        
        for match, value in interaction_event.iter_matches_and_values(converter.annotation.fullmatch):
            
            groups = match.groups()
            
            if (values is None):
                values = []
            
            values.append((groups, value))
       
        return values


class InternalParameterConverter(ParameterConverter):
    """
    Internal parameter converter.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = ('converter', 'type')
    
    def __new__(cls, parameter_name, type_, converter):
        """
        Creates a new ``InternalParameterConverter`` with the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        type_ : `int`
            Internal identifier of the converter.
        converter : `CoroutineFunctionType`
            The converter to use to convert a value to it's desired type.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter_name
        self.type = type_
        self.converter = converter
        return self
    
    
    @copy_docs(ParameterConverter.__call__)
    async def __call__(self, client, interaction_event, value):
        return await self.converter(client, interaction_event)
    
    
    @copy_docs(ParameterConverter.__repr__)
    def __repr__(self):
        return ''.join([
            '<',
            self.__class__.__name__,
            'parameter_name = ',
            repr(self.parameter_name),
            ', type = ',
            ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type],
            '>',
        ])


class SlashCommandParameterConverter(ParameterConverter):
    """
    Converter class for slash command options.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's internal name.
    auto_completer : `None`, ``SlashCommandParameterAutoCompleter``
        Auto completer if registered.
    channel_types : `None`, `tuple` of ``ChannelType``
        The accepted channel types.
    choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    default : `object`
        Default value of the parameter.
    description : `None`, `str`
        The parameter's description.
    max_length : `int`
        The maximum input length allowed for this option.
    max_value : `None`, `int`, `float`
        The maximal accepted value by the converter.
    min_length : `int`
        The minimum input length allowed for this option.
    min_value : `None`, `int`, `float`
        The minimal accepted value by the converter.
    name : `str`
        The parameter's name.
    required : `bool`
        Whether the the parameter is required.
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = (
        'auto_completer', 'channel_types', 'choice_enum_type', 'choices', 'converter', 'default', 'description',
        'max_length', 'max_value', 'min_length', 'min_value', 'name', 'required', 'type'
    )
    
    def __new__(
        cls, parameter_name, type_, converter, name, description, default, required, choice_enum_type, choices,
        channel_types, max_value, min_value, autocomplete, max_length, min_length
    ):
        """
        Creates a new ``SlashCommandParameterConverter`` from the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        type_ : `int`
            Internal identifier of the converter.
        converter : `CoroutineFunctionType`
            The converter to use to convert a value to it's desired type.
        name : `str`
            The parameter's internal name.
        description : `None`, `str`
            The parameter's description.
        default : `bool`
            Default value of the parameter.
        required : `bool`
            Whether the the parameter is required.
        choice_enum_type : `None`, `type`
            Enum type of `choices` if applicable.
        choices : `None`, `dict` of ((`int`, `float`, `str`, `Enum`), `str`) items
            The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
        channel_types : `None`, `tuple` of ``ChannelType``
            The accepted channel types.
        max_value : `None`, `int`, `float`
            The maximal accepted value by the converter.
        min_value : `None`, `int`, `float`
            The minimal accepted value by the converter.
        autocomplete : `None`, ``SlashCommandParameterAutoCompleter``
            Auto completer if defined.
        max_length : `int`
            The maximum input length allowed for this option.
        min_length : `int`
            The minimum input length allowed for this option.
        """
        self = object.__new__(cls)
        
        self.parameter_name = parameter_name
        self.auto_completer = None
        self.choice_enum_type = choice_enum_type
        self.choices = choices
        self.converter = converter
        self.default = default
        self.description = description
        self.name = name
        self.required = required
        self.type = type_
        self.channel_types = channel_types
        self.max_value = max_value
        self.min_value = min_value
        self.max_length = max_length
        self.min_length = min_length
        
        if (autocomplete is not None):
            auto_completer = SlashCommandParameterAutoCompleter(
                autocomplete, [parameter_name], APPLICATION_COMMAND_FUNCTION_DEEPNESS, None
            )
            self.register_auto_completer(auto_completer)
        
        return self
    
    
    @copy_docs(ParameterConverter.__call__)
    async def __call__(self, client, interaction_event, value):
        choices = self.choices
        
        if (value is None):
            if not self.required:
                return self.default
        
        else:
            converted_value = await self.converter(client, interaction_event, value)
            if (converted_value is not None):
                if (choices is None):
                    return converted_value
                
                choice_enum_type = self.choice_enum_type
                if (choice_enum_type is None):
                    if (converted_value in choices):
                        return converted_value
                
                else:
                    try:
                        converted_value = choice_enum_type(converted_value)
                    except ValueError:
                        pass
                    else:
                        return converted_value
        
        
        raise SlashCommandParameterConversionError(
            self.name,
            value,
            ANNOTATION_TYPE_TO_REPRESENTATION.get(self.type, '???'),
            None if choices is None else list(choices.keys()),
        )
    
    @copy_docs(ParameterConverter.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        parameter_name = self.parameter_name
        repr_parts.append(' parameter_name = ')
        repr_parts.append(repr(self.parameter_name))
        
        name = self.name
        if (parameter_name != name):
            repr_parts.append(', name = ')
            repr_parts.append(repr(self.name))
        
        repr_parts.append(', type = ')
        repr_parts.append(ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type])
        
        repr_parts.append(', description = ')
        repr_parts.append(reprlib.repr(self.description))
        
        if not self.required:
            repr_parts.append(', default = ')
            repr_parts.append(repr(self.default))
        
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices = ')
            repr_parts.append(repr(choices))
        
        auto_completer = self.auto_completer
        if (auto_completer is not None):
            repr_parts.append(', auto_completer = ')
            repr_parts.append(repr(auto_completer))
        
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types = ')
            repr_parts.append(repr(channel_types))
        
        min_value = self.min_value
        if (min_value is not None):
            repr_parts.append(', min_value = ')
            repr_parts.append(repr(min_value))
        
        max_value = self.max_value
        if (max_value is not None):
            repr_parts.append(', max_value = ')
            repr_parts.append(repr(max_value))
        
        min_length = self.min_length
        if (min_length != 0):
            repr_parts.append(', min_length = ')
            repr_parts.append(repr(min_length))
        
        max_length = self.max_length
        if (max_length != 0):
            repr_parts.append(', max_length = ')
            repr_parts.append(repr(max_length))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ParameterConverter.as_option)
    def as_option(self):
        choices = self.choices
        if choices is None:
            option_choices = None
        else:
            is_enum = (self.choice_enum_type is not None)
            
            option_choices = [
                ApplicationCommandOptionChoice(name, str(value.value if is_enum else value))
                for value, name in choices.items()
            ]
        
        option_type = ANNOTATION_TYPE_TO_OPTION_TYPE[self.type]
        
        return ApplicationCommandOption(
            self.name,
            self.description,
            option_type,
            autocomplete = (self.auto_completer is not None),
            channel_types = self.channel_types,
            choices = option_choices,
            required = self.required,
            min_value = self.min_value,
            max_value = self.max_value,
            min_length = self.min_length,
            max_length = self.max_length,
        )
    
    
    def can_auto_complete(self):
        """
        Returns whether the parameter can be auto completed.
        
        Returns
        -------
        can_be_auto_completed : `bool`
            Whether the parameter can be auto completed.
        """
        if (self.type not in ANNOTATION_AUTO_COMPLETE_AVAILABILITY):
            return False
        
        if (self.choices is not None):
            return False
        
        return True
    
    
    def is_auto_completed(self):
        """
        Returns whether the parameter is already auto completed.
        
        Returns
        -------
        is_auto_completed : `bool`
        """
        if self.auto_completer is None:
            return False
        
        return True
    
    
    def register_auto_completer(self, auto_completer):
        """
        Registers an auto completer to the slash command parameter converter.
        
        Parameters
        ----------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The auto completer to register.
        
        Returns
        -------
        resolved : `int`
            Whether the parameter was resolved.
        
        Raises
        ------
        RuntimeError
            If the parameter cannot be auto completed.
        """
        if (self.type not in ANNOTATION_AUTO_COMPLETE_AVAILABILITY):
            raise RuntimeError(
                f'Parameter `{self.name}` can not be auto completed. Only string base type parameters '
                f'can be (str, int, expression).'
            )
        
        if (self.choices is not None):
            raise RuntimeError(
                f'Parameter `{self.name}` can not be auto completed. `choices` and `autocomplete` are'
                f'mutually exclusive.'
            )
        
        self_auto_completer = self.auto_completer
        if (self_auto_completer is None) or auto_completer._is_deeper_than(self_auto_completer):
            self.auto_completer = auto_completer
            resolved = 1
        else:
            resolved = 0
        
        return resolved
    
    
    @copy_docs(ParameterConverter.bind_parent)
    def bind_parent(self, parent):
        auto_completer = self.auto_completer
        if (auto_completer is not None):
            self.auto_completer = auto_completer._bind_parent(parent)


def create_parameter_converter(parameter, parameter_configurer):
    """
    Creates a new parameter converter from the given parameter.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The parameter to create converter from.
    parameter_configurer : `None`, ``ApplicationCommandParameterConfigurerWrapper``
        Parameter configurer for the parameter if any.
    
    Returns
    -------
    parameter_converter : ``ParameterConverter``
    
    Raises
    ------
    TypeError
        - if the `parameter` has no annotation.
        - If `annotation_value` is `list`, but it's elements do not match the `tuple`
            (`str`, `str`, `int`) pattern.
        - If `annotation_value` is `dict`, but it's items do not match the (`str`, `str`, `int`) pattern.
        - If `annotation_value` is unexpected.
        - If `annotation` is not `tuple`, `type` nor `str`.
        - If `annotation` 1st element (description) is not `str`.
    ValueError
        - If `annotation` is a `tuple`, but it's length is not range [2:3].
        - If `annotation_value` is `str`, but not any of the expected ones.
        - If `annotation_value` is `type`, but not any of the expected ones.
        - If `choice` amount is out of the expected range [1:25].
        - If a `choice` name is duped.
        - If a `choice` values are mixed types.
        - If `annotation`'s 1st element's (description's) length is out of the expected range [2:100].
        - If a slash parameter's final description's length is out of the expected range.
    """
    if parameter_configurer is None:
        (
            choices, description, name, annotation_type, channel_types, max_value, min_value, autocomplete,
            choice_enum_type, max_length, min_length
        ) = parse_annotation(parameter)
    else:
        choice_enum_type = parameter_configurer._choice_enum_type
        choices = parameter_configurer._choices
        description = parameter_configurer._description
        name = parameter_configurer._name
        annotation_type = parameter_configurer._type
        channel_types = parameter_configurer._channel_types
        max_value = parameter_configurer._max_value
        min_value = parameter_configurer._min_value
        autocomplete = parameter_configurer._autocomplete
        max_length = parameter_configurer._max_length
        min_length = parameter_configurer._min_length
    
    if description is None:
        description = raw_name_to_display(name)
    
    if parameter.has_default:
        default = parameter.default
        required = False
    else:
        default = None
        required = True
    
    converter, is_internal = ANNOTATION_TYPE_TO_CONVERTER[annotation_type]
    
    if is_internal:
        parameter_converter = InternalParameterConverter(parameter.name, annotation_type, converter)
    
    else:
        # Rare error case when the parameter has no description defined, so it defaults back to its name, that is
        # outside of the expected range.
        description_length = len(description)
        if (description_length < APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN) and (name == description):
            raise ValueError(
                f'`{parameter.name}` parameter\'s description\'s length is out of the expected range: '
                f'[{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN}:{APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX}], '
                f'got {description_length!r}; {description!r}.\n'
                f'This happened because the parameter has no description specified so it tried to default to its '
                f'name.\n'
                f'Note that the required minimal name length is lower than the required minimal description length.'
            )
        
        parameter_converter = SlashCommandParameterConverter(
            parameter.name, annotation_type, converter, name, description, default, required, choice_enum_type,
            choices, channel_types, max_value, min_value, autocomplete, max_length, min_length
        )
    
    return parameter_converter


def create_internal_parameter_converter(parameter):
    """
    Creates an internal parameter converter.

    Parameters
    ----------
    parameter : ``Parameter``
        The parameter to create converter from.
    
    Returns
    -------
    parameter_converter : ``ParameterConverter``, `None`
    """
    if parameter.has_annotation:
        annotation_value = parameter.annotation
        if isinstance(annotation_value, tuple):
            if len(annotation_value) == 0:
                annotation_value = parameter.name
            else:
                annotation_value = annotation_value[0]
    else:
        annotation_value = parameter.name
    
    annotation_type = parse_annotation_internal(annotation_value)
    if annotation_type is None:
        return None
    
    converter, is_internal = ANNOTATION_TYPE_TO_CONVERTER[annotation_type]
    return InternalParameterConverter(parameter.name, annotation_type, converter)


def create_target_parameter_converter(parameter):
    """
    Creates an internal target parameter converter.
    
    Applicable for context application commands.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The parameter to create converter from.
    
    Returns
    -------
    parameter_converter : ``ParameterConverter``
    """
    return InternalParameterConverter(parameter.name, ANNOTATION_TYPE_SELF_TARGET, converter_self_interaction_target)


def create_value_parameter_converter(parameter):
    """
    Creates an internal value parameter converter.
    
    Applicable for application command parameters with auto completion enabled.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The parameter to create converter from.
    
    Returns
    -------
    parameter_converter : ``ParameterConverter``
    """
    return InternalParameterConverter(parameter.name, ANNOTATION_TYPE_SELF_VALUE, converter_self_interaction_value)


def check_command_coroutine(
    func,
    allow_coroutine_generator_functions,
    allow_args_parameters,
    allow_keyword_only_parameters,
    allow_kwargs_parameters,
):
    """
    Checks whether the given `func` is a coroutine and whether it accepts only positional only parameters.
    
    Parameters
    ----------
    func : `async-callable`
        Command coroutine.
    allow_coroutine_generator_functions : `bool`
        Whether coroutine generator functions are allowed.
    allow_args_parameters : `bool`
        Whether `*args` parameters are allowed.
    allow_keyword_only_parameters : `bool`
        Whether keyword parameters are allowed.
    allow_kwargs_parameters : `bool`
        Whether `**kwargs` parameters are allowed.
    
    Returns
    -------
    analyzer : ``CallableAnalyzer``
        Analyzer called on `func`.
    real_analyzer : ``CallableAnalyzer``
        Analyzer called on the real called function.
    should_instance : `bool`
        Whether `func` should be instanced.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only parameters.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async() or (allow_coroutine_generator_functions and analyzer.is_async_generator()):
        real_analyzer = analyzer
        should_instance = False
    
    elif (
        analyzer.can_instance_to_async_callable() or
        (allow_coroutine_generator_functions and analyzer.can_instance_to_async_generator())
    ):
        real_analyzer = CallableAnalyzer(func.__call__, as_method=True)
        if (not real_analyzer.is_async()) and (not real_analyzer.is_async_generator()):
            raise TypeError(
                f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.'
            )
        
        should_instance = True
    
    else:
        raise TypeError(
            f'`func` is not `async-callable` '
            f'{"nor a coroutine generator function " if allow_coroutine_generator_functions else ""}'
            f'and cannot be instanced to `async` either, got {func!r}.'
        )
    
    
    if (not allow_keyword_only_parameters):
        keyword_only_parameter_count = real_analyzer.get_non_default_keyword_only_parameter_count()
        if keyword_only_parameter_count:
            raise TypeError(
                f'`{real_analyzer.real_function!r}` accepts keyword only parameters.'
            )
    
    if (not allow_args_parameters):
        if real_analyzer.accepts_args():
            raise TypeError(
                f'`{real_analyzer.real_function!r}` accepts `*args`.'
            )
    
    if (not allow_kwargs_parameters):
        if real_analyzer.accepts_kwargs():
            raise TypeError(
                f'`{real_analyzer.real_function!r}` accepts `**kwargs`.'
            )
    
    return analyzer, real_analyzer, should_instance


def get_slash_command_parameter_converters(func, parameter_configurers):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    parameter_configurers : `None`, `dict` of (`str`, ``ApplicationCommandParameterConfigurerWrapper``) items
        Parameter configurers to overwrite annotations.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only parameters.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
        - If `func` accepts more than `27` parameters.
        - If a parameter's `annotation_value` is `list`, but it's elements do not match the
            `tuple` (`str`, `str`, `int`) pattern.
        - If a parameter's `annotation_value` is `dict`, but it's items do not match the
            (`str`, `str`, `int`) pattern.
        - If a parameter's `annotation_value` is unexpected.
        - If a parameter's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str`.
    ValueError
        - If a parameter's `annotation` is a `tuple`, but it's length is out of the expected range [0:3].
        - If a parameter's `annotation_value` is `str`, but not any of the expected ones.
        - If a parameter's `annotation_value` is `type`, but not any of the expected ones.
        - If a parameter's `choice` amount is out of the expected range [1:25].
        - If a parameter's `choice` name is duped.
        - If a parameter's `choice` values are mixed types.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True, False, False, False)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    for parameter in parameters:
        if parameter_configurers is None:
            parameter_configurer = None
        else:
            parameter_configurer = parameter_configurers.get(parameter.name, None)
        
        parameter_converter = create_parameter_converter(parameter, parameter_configurer)
        parameter_converters.append(parameter_converter)
    
    slash_command_option_count = 0
    for parameter_converter in parameter_converters:
        if isinstance(parameter_converter, SlashCommandParameterConverter):
            slash_command_option_count += 1
        
    if slash_command_option_count > APPLICATION_COMMAND_OPTIONS_MAX:
        raise TypeError(
            f'`{real_analyzer.real_function!r}` should accept at maximum '
            f'`{APPLICATION_COMMAND_OPTIONS_MAX}` slash command options,  meanwhile it accepts '
            f'{slash_command_option_count}.'
        )
    
    parameter_converters = tuple(parameter_converters)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, parameter_converters


def get_component_command_parameter_converters(func):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``ComponentCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only parameters.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True, False, False, False)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    for parameter in parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        parameter_converters.append(parameter_converter)
    
    parameter_index = 0
    for index in range(len(parameter_converters)):
        parameter_converter = parameter_converters[index]
        if (parameter_converter is not None):
            continue
        
        parameter = parameters[index]
        parameter_converter = RegexParameterConverter(parameter, parameter_index)
        parameter_converters[index] = parameter_converter
        parameter_index += 1
    
    parameter_converters = tuple(parameter_converters)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, parameter_converters


def get_context_command_parameter_converters(func):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only parameters.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
    ValueError
        - If any parameter is not internal.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True, False, False, False)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    target_converter_detected = False
    for parameter in parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        
        if (parameter_converter is None):
            if target_converter_detected:
                raise TypeError(
                    f'`{real_analyzer.real_function!r}`\'s `{parameter.name}` do not refers to any of the '
                    f'expected internal parameters. Context commands do not accept any additional parameters.'
                )
            else:
                parameter_converter = create_target_parameter_converter(parameter)
                target_converter_detected = True
        
        parameter_converters.append(parameter_converter)
    
    
    parameter_converters = tuple(parameter_converters)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, parameter_converters


def get_application_command_parameter_auto_completer_converters(func):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlashCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` in order.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts keyword only parameters.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
    ValueError
        - If any parameter is not internal.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True, False, False, False)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    value_converter_detected = False
    for parameter in parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        
        if (parameter_converter is None):
            if value_converter_detected:
                raise TypeError(
                    f'`{real_analyzer.real_function!r}`\'s `{parameter.name}` do not refers to any of the '
                    f'expected internal parameters. Context commands do not accept any additional parameters.'
                )
            else:
                parameter_converter = create_value_parameter_converter(parameter)
                value_converter_detected = True
        
        parameter_converters.append(parameter_converter)
    
    
    parameter_converters = tuple(parameter_converters)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, parameter_converters


def get_form_submit_command_parameter_converters(func):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``FormSubmitCommand``.
    
    Returns
    -------
    func : `async-callable`
        The converted function.
    positional_parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` in order.
    multi_parameter_converter : ``ParameterConverter``
         Parameter converter for `*args` parameter.
    keyword_parameter_converters : `tuple` of ``ParameterConverter``
        Parameter converters for the given `func` for it's keyword parameters.
    
    Raises
    ------
    TypeError
        - If `func` is not async callable, neither cannot be instanced to async.
        - If `func` accepts `*args`.
        - If `func` accepts `**kwargs`.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True, True, True, False)
    
    positional_parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    positional_parameter_converters = []
    
    for parameter in positional_parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        positional_parameter_converters.append(parameter_converter)
    
    parameter_index = 0
    for index in range(len(positional_parameter_converters)):
        parameter_converter = positional_parameter_converters[index]
        if (parameter_converter is not None):
            continue
        
        parameter = positional_parameters[index]
        parameter_converter = RegexParameterConverter(parameter, parameter_index)
        positional_parameter_converters[index] = parameter_converter
        parameter_index += 1
    
    positional_parameter_converters = tuple(positional_parameter_converters)
    
    keyword_parameters = real_analyzer.get_non_reserved_keyword_only_parameters()
    keyword_parameter_converters = tuple(FormFieldKeywordParameterConverter(parameter) for parameter in keyword_parameters)
    
    args_parameter = real_analyzer.args_parameter
    if (args_parameter is None):
        multi_parameter_converter = None
    else:
        multi_parameter_converter = FormFieldMultiParameterConverter(args_parameter)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, positional_parameter_converters, multi_parameter_converter, keyword_parameter_converters
