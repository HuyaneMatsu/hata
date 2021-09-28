__all__ = ()

import reprlib

from ...backend.analyzer import CallableAnalyzer
from ...backend.utils import un_map_pack, copy_docs

from ...discord.core import ROLES, CHANNELS
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.client import Client
from ...discord.user import UserBase, User
from ...discord.role import Role
from ...discord.channel import ChannelBase, ChannelGuildBase, CHANNEL_TYPES, ChannelCategory, ChannelDirectory, \
    ChannelGuildMainBase, ChannelStore, ChannelText, ChannelVoiceBase, ChannelVoice, ChannelStage, ChannelPrivate, \
    ChannelGroup, ChannelThread, ChannelTextBase
from ...discord.interaction import ApplicationCommandOption, ApplicationCommandOptionChoice, InteractionType, \
    ApplicationCommandOptionType, InteractionEvent
from ...discord.interaction.application_command import APPLICATION_COMMAND_OPTIONS_MAX, \
    APPLICATION_COMMAND_DESCRIPTION_LENGTH_MIN, APPLICATION_COMMAND_DESCRIPTION_LENGTH_MAX

from .utils import raw_name_to_display, normalize_description
from .exceptions import SlasherApplicationCommandParameterConversionError
from .expression_parser import evaluate_text

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
    target : `None` or ``DiscordEntity``
        The resolved entity if any.
    """
    if interaction_event.type is not INTERACTION_TYPE_APPLICATION_COMMAND:
        return None
    
    return interaction_event.interaction.target
    

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
    target : `None` or `str`
        The received value if any.
    """
    if interaction_event.type is not INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE:
        return None
    
    return interaction_event.interaction.value


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
    value : `None` or `int`
        If conversion fails, then returns `None`.
    """
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
    value : `str`
        ``ApplicationCommandInteractionOption.value``.
    
    Returns
    -------
    value : `None` or `float`
        If conversion fails, then returns `None`.
    """
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
    value : `None` or `str`
        If conversion fails, then returns `None`.
    """
    return value

BOOL_TABLE = {
    str(True): True,
    str(False): False,
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
    value : `None` or `bool`
        If conversion fails, then returns `None`.
    """
    return BOOL_TABLE.get(value, None)


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


async def converter_user(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``UserBase`` instance.
    
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
    
    if user_id is None:
        user = None
    else:
        resolved_users = interaction_event.interaction.resolved_users
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


async def converter_role(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``Role`` instance.
    
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
    value : `None` or ``Role``
        If conversion fails, then returns `None`.
    """
    role_id = await converter_snowflake(client, interaction_event, value)
    
    if role_id is None:
        role = None
    else:
        resolved_roles = interaction_event.interaction.resolved_roles
        if resolved_roles is None:
            role = None
        else:
            role = resolved_roles.get(role_id, None)
        
        if role is None:
            role = ROLES.get(role_id, None)
    
    return role


async def converter_channel(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to ``ChannelBase`` instance.
    
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
    value : `None` or ``ChannelBase`` instance
        If conversion fails, then returns `None`.
    """
    channel_id = await converter_snowflake(client, interaction_event, value)
    
    if channel_id is None:
        channel = None
    else:
        resolved_channels = interaction_event.interaction.resolved_channels
        if resolved_channels is None:
            channel = None
        else:
            channel = resolved_channels.get(channel_id, None)
        
        if channel is None:
            channel = CHANNELS.get(channel_id, None)
    
    return channel


async def converter_mentionable(client, interaction_event, value):
    """
    Converter for ``ApplicationCommandInteractionOption`` value to mentionable ``DiscordEntity`` instance.
    
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
    value : `None` or ``DiscordEntity`` instance
        If conversion fails, then returns `None`.
    """
    entity_id = await converter_snowflake(client, interaction_event, value)
    
    # Use goto
    while True:
        if entity_id is None:
            entity = None
            break
        
        resolved_users = interaction_event.interaction.resolved_users
        if (resolved_users is not None):
            try:
                entity = resolved_users[entity_id]
            except KeyError:
                pass
            else:
                break
        
        resolved_roles = interaction_event.interaction.resolved_roles
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
    value : `int` or `float`
    
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

CHANNEL_TYPES_GUILD = tuple(CHANNEL_TYPES.GROUP_GUILD)
CHANNEL_TYPES_GUILD_CATEGORY = (CHANNEL_TYPES.guild_category, )
CHANNEL_TYPES_GUILD_DIRECTORY = (CHANNEL_TYPES.guild_directory, )
CHANNEL_TYPES_GUILD_STORE = (CHANNEL_TYPES.guild_store, )
CHANNEL_TYPES_GUILD_TEXT_LIKE = tuple(CHANNEL_TYPES.GROUP_GUILD_TEXT_LIKE)
CHANNEL_TYPES_GUILD_TEXT = (CHANNEL_TYPES.guild_text, )
CHANNEL_TYPES_GUILD_ANNOUNCEMENTS = (CHANNEL_TYPES.guild_announcements, )
CHANNEL_TYPES_GUILD_CONNECTABLE = tuple(CHANNEL_TYPES.GROUP_GUILD_CONNECTABLE)
CHANNEL_TYPES_GUILD_VOICE = (CHANNEL_TYPES.guild_voice, )
CHANNEL_TYPES_GUILD_STAGE = (CHANNEL_TYPES.guild_stage, )
CHANNEL_TYPES_PRIVATE_ALL = tuple(CHANNEL_TYPES.GROUP_PRIVATE)
CHANNEL_TYPES_PRIVATE = (CHANNEL_TYPES.private, )
CHANNEL_TYPES_PRIVATE_GROUP = (CHANNEL_TYPES.private_group, )
CHANNEL_TYPES_THREAD_ALL = tuple(CHANNEL_TYPES.GROUP_THREAD)
CHANNEL_TYPES_THREAD_ANNOUNCEMENTS = (CHANNEL_TYPES.guild_thread_announcements, )
CHANNEL_TYPES_THREAD_PUBLIC = (CHANNEL_TYPES.guild_thread_public, )
CHANNEL_TYPES_THREAD_PRIVATE = (CHANNEL_TYPES.guild_thread_private, )
CHANNEL_TYPES_MESSAGEABLE = tuple(CHANNEL_TYPES.GROUP_MESSAGEABLE)
CHANNEL_TYPES_GUILD_MESSAGEABLE = tuple(CHANNEL_TYPES.GROUP_GUILD_MESSAGEABLE)
CHANNEL_TYPES_CONNECTABLE = tuple(CHANNEL_TYPES.GROUP_CONNECTABLE)

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
    
    # Channel type specific
    # - by channel name
    'channelguildbase': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD),
    'channelguildmainbase': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD),
    'channelcategory': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CATEGORY),
    'channeldirectory': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_DIRECTORY),
    'channelstore': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STORE),
    'channeltext': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_TEXT_LIKE),
    'channelvoicebase': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CONNECTABLE),
    'channelvoice': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_VOICE),
    'channelstage': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STAGE),
    'channelprivate': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE),
    'channelgroup': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE_GROUP),
    'channelthread': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_ALL),
    'channeltextbase': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_MESSAGEABLE),
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
    'channel_group_messageable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_MESSAGEABLE),
    'channel_group_guild_messageable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_MESSAGEABLE),
    'channel_group_guild_text_like': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_TEXT_LIKE),
    'channel_group_connectable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_CONNECTABLE),
    'channel_group_private': (ANNOTATION_TYPE_CHANNEL, ),
    'channel_group_guild_connectable': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CONNECTABLE),
    'channel_group_guild': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD),
    'channel_group_thread': (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_ALL),
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
    'channel_id_group_messageable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_MESSAGEABLE),
    'channel_id_group_guild_messageable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_MESSAGEABLE),
    'channel_id_group_guild_text_like': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_TEXT_LIKE),
    'channel_id_group_connectable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_CONNECTABLE),
    'channel_id_group_private': (ANNOTATION_TYPE_CHANNEL_ID, ),
    'channel_id_group_guild_connectable': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD_CONNECTABLE),
    'channel_id_group_guild': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_GUILD),
    'channel_id_group_thread': (ANNOTATION_TYPE_CHANNEL_ID, CHANNEL_TYPES_THREAD_ALL),
    
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
    UserBase: (ANNOTATION_TYPE_USER, None),
    User: (ANNOTATION_TYPE_USER, None),
    Role: (ANNOTATION_TYPE_ROLE, None),
    ChannelBase: (ANNOTATION_TYPE_CHANNEL, None),
    float: (ANNOTATION_TYPE_FLOAT, None),
    
    # Channel type specific
    ChannelGuildBase: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD),
    ChannelGuildMainBase: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD),
    ChannelCategory: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CATEGORY),
    ChannelDirectory: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_DIRECTORY),
    ChannelStore: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STORE),
    ChannelText: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_TEXT_LIKE),
    ChannelVoiceBase: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_CONNECTABLE),
    ChannelVoice: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_VOICE),
    ChannelStage: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_STAGE),
    ChannelPrivate: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE),
    ChannelGroup: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_PRIVATE_GROUP),
    ChannelThread: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_THREAD_ALL),
    ChannelTextBase: (ANNOTATION_TYPE_CHANNEL, CHANNEL_TYPES_GUILD_MESSAGEABLE),
    
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
}


ANNOTATION_AUTO_COMPLETE_AVAILABILITY = frozenset((
    ANNOTATION_TYPE_STR,
    ANNOTATION_TYPE_INT,
    ANNOTATION_TYPE_EXPRESSION,
))

class RegexMatcher:
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
        Creates a ``RegexMatcher`` instance from the given parameters.
        
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
            raise ValueError(f'Regex patterns with mixed dict groups and non-dict groups are disallowed, got '
                f'{regex_pattern!r}.')
        
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
    parameter_converters : `tuple` of ``ParameterConverter`` instances
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
        
        raise ValueError(f'Parameter {parameter_converter.name!r} is not satisfied by string `custom_id`-s.')
    
    return True


def check_component_converters_satisfy_regex(parameter_converters, regex_matcher):
    """
    Checks whether the given parameter converters satisfy a regex matcher.
    
    Parameters
    ----------
    parameter_converters : `tuple` of ``ParameterConverter`` instances
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
        raise ValueError(f'Parameter {unsatisfied.name!r} is not satisfied by regex pattern: '
            f'`{regex_matcher.pattern.pattern}`.')


class RegexMatch:
    """
    Matched regex pattern by ``RegexMatcher``.
    
    Attributes
    ----------
    is_group_dict : `bool`
        Whether `groups` is a dictionary.
    groups : `tuple` of `str` or `dict` of (`str`, `str`) items
        The matched groups.
    """
    __slots__ = ('is_group_dict', 'groups')
    
    def __new__(cls, groups, is_group_dict):
        """
        Creates a new ``RegexMatcher`` instance from the given parameters.
    
        Parameters
        ----------
        is_group_dict : `bool`
            Whether `groups` is a dictionary.
        groups : `tuple` of `str` or `dict` of (`str`, `str`) items
            The matched groups.
        """
        self = object.__new__(cls)
        self.groups = groups
        self.is_group_dict = is_group_dict
        return self
    
    def __repr__(self):
        """Returns the regex match's representation."""
        return f'<{self.__class__.__name__} groups={self.groups!r}>'


def create_annotation_choice_from_int(value):
    """
    Creates an annotation choice form an int.
    
    Parameters
    -------
    value : `int`
        The validated annotation choice.
    
    Returns
    -------
    choice : `tuple` (`str`, (`str`, `int`, `float`))
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
    choice : `tuple` (`str`, (`str`, `int`, `float`))
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
    choice : `tuple` (`str`, (`str`, `int`, `float`))
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
    annotation_length = len(annotation)
    if (annotation_length < 1 or annotation_length > 2):
        raise ValueError(f'`tuple` annotation length can be in range [1:2], got {annotation_length!r}; {annotation!r}')
    
    if annotation_length == 1:
        value = annotation[0]
        if isinstance(value, str):
            return create_annotation_choice_from_str(value)
        
        if isinstance(value, int):
            return create_annotation_choice_from_int(value)
        
        if isinstance(value, float):
            return create_annotation_choice_from_float(value)
        
        raise TypeError(f'`annotation-value` can be either `str`, `int` or `float`, got {value.__class__.__name__}.')
    
    # if annotation_length == 2:
    
    name, value = annotation
    if not isinstance(name, str):
        raise TypeError(f'`annotation-name` can be `str` instance, got {name.__class__.__name__}.')
    
    if not isinstance(value, (str, int, float)):
        raise TypeError(f'`annotation-value` can be either `str`, `int` or `float`, got {value.__class__.__name__}.')
    
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
    
    raise TypeError(f'`annotation-choice` can be either given as `tuple`, `str`, `int`  or `float` instance, got '
        f'{annotation_choice.__class__.__name__}.')


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
    choices : `None` or `dict` of (`int` or `str`, `str`) items
        Choices if applicable.
    channel_types : `None` or `tuple` of `int`
        The accepted channel types.
    
    TypeError
        - If `annotation_value` is `list` instance, but it's elements do not match the `tuple`
            (`str`, `str`, `int` or `float`) pattern.
        - If `annotation_value` is `dict` instance, but it's items do not match the
            (`str`, `str`, `int` or `float`) pattern.
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
            annotation_type, channel_types = STR_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Parameter `{parameter_name}` has annotation not referring to any expected type, '
                f'got {annotation_value!r}.') from None
        
        choices = None
    elif isinstance(annotation_value, type):
        try:
            annotation_type, channel_types = TYPE_ANNOTATION_TO_ANNOTATION_TYPE[annotation_value]
        except KeyError:
            raise ValueError(f'Parameter `{parameter_name}` has annotation not referring to any expected type, '
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
        elif hasattr(type(annotation_value), '__iter__'):
            for annotation_choice in annotation_value:
                choice_element = parse_annotation_choice(annotation_choice)
                choice_elements.append(choice_element)
        
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
            elif isinstance(value, int):
                type_ = int
            else:
                type_ = float
            
            if expected_type is None:
                expected_type = type_
                continue
            
            if expected_type is not type_:
                raise ValueError(f'Mixed choice value types in annotation: `{parameter_name}`.')
        
        if expected_type is str:
            annotation_type = ANNOTATION_TYPE_STR
        elif expected_type is int:
            annotation_type = ANNOTATION_TYPE_INT
        else:
            annotation_type = ANNOTATION_TYPE_FLOAT
        
        choices = {value:name for name, value in choice_elements}
        
        channel_types = None
    
    return annotation_type, choices, channel_types


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
        raise ValueError(f'Parameter `{parameter_name}` has annotation description\'s length is out of the expected '
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
    parameter_name : `None` or `str`
        The annotation's name.
    
    Returns
    -------
    name : `str`
    
    Raises
    ------
    TypeError
        If `name`'s is neither `None` or `str` instance.
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


def parse_annotation_tuple(parameter):
    """
    Parses an annotated tuple.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    
    Returns
    -------
    choices : `None` or `dict` of (`str` or `int`, `str`) items
        Parameter's choices.
    description : `str`
        Parameter's description.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None` or `tuple` of `int`
        The accepted channel types.
    
    Raises
    ------
    ValueError
        - If `parameter` annotation tuple's length is out of range [2:3].
        - If `parameter` annotation's refers to an internal type.
    """
    parameter_name = parameter.name
    annotation = parameter.annotation
    annotation_tuple_length = len(annotation)
    if annotation_tuple_length not in (1, 2, 3):
        raise ValueError(f'Parameter `{parameter_name}` has annotation as `tuple`, but it\'s length is not in '
            f'range [1:3], got {annotation_tuple_length!r}, {annotation_tuple_length!r}.')
    
    annotation_value = annotation[0]
    annotation_type, choices, channel_types = parse_annotation_type_and_choice(annotation_value, parameter_name)
    
    if annotation_type in INTERNAL_ANNOTATION_TYPES:
        raise ValueError(f'`Internal annotations cannot be given inside of a tuple, got annotation for: '
            f'{ANNOTATION_TYPE_TO_STR_ANNOTATION[annotation_type]!r}.')
    
    if annotation_tuple_length > 1:
        description = annotation[1]
    else:
        description = None
    
    if (description is not None):
        description = parse_annotation_description(description, parameter_name)
    
    if annotation_tuple_length > 2:
        name = annotation[2]
    else:
        name = None
    
    name = parse_annotation_name(name, parameter_name)
    return choices, description, name, annotation_type, channel_types


def parse_annotation_internal(annotation):
    """
    Tries to check whether the given annotation refers to an internal type or not.
    
    Parameters
    ----------
    annotation : `str`, `type`
        The annotation to check.
    
    Returns
    -------
    annotation_type : `None` or `int`
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
    Tries to parse an internal annotation referencing ``Client`` or ``InteractionEvent``.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The respective parameter's representation.
    
    Returns
    -------
    choices : `None` or `dict` of (`str` or `int`, `str`) items
        Parameter's choices.
    description : `None` or `str`
        Parameter's description.
        
        > Returned as `None` for internal parameters or if `description` could nto be detected.
    name : `str`
        The parameter's name.
    type_ : `int`
        The parameter's internal type identifier.
    channel_types : `None` or `tuple` of `int`
        The accepted channel types.
    
    Raises
    ------
    ValueError
        - If `parameter` annotation tuple's length  is out of range [2:3].
        - If `parameter` annotation tuple refers to an internal type.
    TypeError
        Parameter's type refers to an unknown type or string value.
    """
    if parameter.has_annotation:
        annotation_value = parameter.annotation
        if isinstance(annotation_value, tuple):
            if len(annotation_value) == 0:
                annotation_value = parameter.name
            else:
                return parse_annotation_tuple(parameter)
    else:
        annotation_value = parameter.name
    
    if not isinstance(annotation_value, (str, type)):
        raise TypeError(f'Parameter `{parameter.name}` is not `tuple`, `str`, nor `str` instance '
            f'{annotation_value.__class__.__name__}; {annotation_value!r}.')
    else:
        annotation_type = parse_annotation_internal(annotation_value)
        if annotation_type is None:
            annotation_type, choices, channel_types = parse_annotation_type_and_choice(annotation_value, parameter.name)
        else:
            choices = None
            channel_types = None
    
    return choices, None, parameter.name, annotation_type, channel_types


class ParameterConverter:
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
        value : `Any`
            ``ApplicationCommandInteractionOption.value``.
        
        Returns
        -------
        converted_value : `None` or ``Any`` instance
            If conversion fails, always returns `None`.
        
        Raises
        ------
        SlasherApplicationCommandParameterConversionError
            The parameter cannot be parsed.
        """
        pass
    
    def __repr__(self):
        """Returns the parameter converter's representation."""
        return f'<{self.__class__.__name__}, parameter_name={self.parameter_name!r}>'
    
    def as_option(self):
        """
        Converts the parameter to an application command option if applicable.
        
        Returns
        -------
        option : `None` or ``ApplicationCommandOption``
        """
        pass


class RegexParameterConverter(ParameterConverter):
    """
    Regex parameter parsing for component `custom_id`.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    default : `Any`
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
        repr_parts =[
            '<',
            self.__class__.__name__,
            ' parameter_name=',
            repr(self.parameter_name),
            ', index=',
            repr(self.index),
        ]
        
        if not self.required:
            repr_parts.append(', default=')
            repr_parts.append(repr(self.default))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class InternalParameterConverter(ParameterConverter):
    """
    Internal parameter converter.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    converter : `func`
        The converter to use to convert a value to it's desired type.
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = ('converter', 'type')
    
    def __new__(cls, parameter_name, type_, converter):
        """
        Creates a new ``InternalParameterConverter`` instance with the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        type_ : `int`
            Internal identifier of the converter.
        converter : `func`
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
            'parameter_name=',
            repr(self.parameter_name),
            ', type=',
            ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type],
            '>',
        ])


class SlashCommandParameterConverter(ParameterConverter):
    """
    Converter class for slash command options.
    
    Attributes
    ----------
    parameter_name : `str`
        The parameter's name.
    auto_completer : `None` or ``SlasherApplicationCommandParameterAutoCompleter``
        Auto completer if registered.
    channel_types : `None` or `tuple` of `int`
        The accepted channel types.
    choices : `None` or `dict` of (`str` or `int`, `str`)
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    converter : `func`
        The converter to use to convert a value to it's desired type.
    default : `Any`
        Default value of the parameter.
    description : `None` or `str`
        The parameter's description.
    required : `bool`
        Whether the the parameter is required.
    type : `int`
        Internal identifier of the converter.
    name : `str`
        The parameter's name.
    """
    __slots__ = ('channel_types', 'auto_completer', 'choices', 'converter', 'default', 'description', 'required',
        'type', 'name')
    
    def __new__(cls, parameter_name, type_, converter, name, description, default, required, choices, channel_types):
        """
        Creates a new ``SlashCommandParameterConverter`` instance from the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        type_ : `int`
            Internal identifier of the converter.
        converter : `func`
            The converter to use to convert a value to it's desired type.
        name : `str`
            The parameter's name.
        description : `None` or `str`
            The parameter's description.
        default : `bool`
            Default value of the parameter.
        required : `bool`
            Whether the the parameter is required.
        choices : `None` or `dict` of (`str` or `int`, `str`)
            The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
        channel_types : `None` or `tuple` of `int`
            The accepted channel types.
        """
        self = object.__new__(cls)
        self.parameter_name = parameter_name
        self.auto_completer = None
        self.choices = choices
        self.converter = converter
        self.default = default
        self.description = description
        self.name = name
        self.required = required
        self.type = type_
        self.channel_types = channel_types
        return self
    
    
    @copy_docs(ParameterConverter.__call__)
    async def __call__(self, client, interaction_event, value):
        choices = self.choices
        
        if (value is None):
            if not self.required:
                return self.default
        else:
            converted_value = await self.converter(client, interaction_event, value)
            if (converted_value is not None) and ((choices is None) or (converted_value in choices)):
                return converted_value
        
        raise SlasherApplicationCommandParameterConversionError(
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
        repr_parts.append(' parameter_name=')
        repr_parts.append(repr(self.parameter_name))
        
        name = self.name
        if (parameter_name != name):
            repr_parts.append(', name=')
            repr_parts.append(repr(self.name))
        
        repr_parts.append(', type=')
        repr_parts.append(ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type])
        
        repr_parts.append(', description=')
        repr_parts.append(reprlib.repr(self.description))
        
        if not self.required:
            repr_parts.append(', default=')
            repr_parts.append(repr(self.default))
        
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices=')
            repr_parts.append(repr(choices))
        
        auto_completer = self.auto_completer
        if (auto_completer is not None):
            repr_parts.append(', auto_completer=')
            repr_parts.append(repr(auto_completer))
        
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types=')
            repr_parts.append(repr(channel_types))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ParameterConverter.as_option)
    def as_option(self):
        choices = self.choices
        if choices is None:
            option_choices = None
        else:
            option_choices = [ApplicationCommandOptionChoice(name, str(value)) for value, name in choices.items()]
        
        option_type = ANNOTATION_TYPE_TO_OPTION_TYPE[self.type]
        
        return ApplicationCommandOption(
            self.name,
            self.description,
            option_type,
            autocomplete = (self.auto_completer is not None),
            channel_types = self.channel_types,
            choices = option_choices,
            required = self.required,
        )
    
    
    def check_can_autocomplete(self):
        """
        Checks whether the parameter can be auto completed.
        
        Raises
        ------
        RuntimeError
            - If the parameter already has a auto completer defined.
            - If the parameter cannot be auto completed.
        """
        if (self.auto_completer is not None):
            raise RuntimeError(f'Parameter `{self.name}` already has an auto completer defined.')
        
        if (self.type not in ANNOTATION_AUTO_COMPLETE_AVAILABILITY):
            raise RuntimeError(f'Parameter `{self.name}` can not be auto completed. Only string base type parameters '
                f'can be (str, int, expression).')
        
        if (self.choices is not None):
            raise RuntimeError(f'Parameter `{self.name}` can not be auto completed. `choices` and `autocomplete` are'
               f'mutually exclusive.')


def create_parameter_converter(parameter, parameter_configurer):
    """
    Creates a new parameter converter from the given parameter.
    
    Parameters
    ----------
    parameter : ``Parameter``
        The parameter to create converter from.
    parameter_configurer : `None` or ``SlasherApplicationCommandParameterConfigurerWrapper``
        Parameter configurer for the parameter if any.
    
    Returns
    -------
    parameter_converter : ``ParameterConverter``
    
    Raises
    ------
    TypeError
        - if the `parameter` has no annotation.
        - If `annotation_value` is `list` instance, but it's elements do not match the `tuple`
            (`str`, `str` or `int`) pattern.
        - If `annotation_value` is `dict` instance, but it's items do not match the (`str`, `str` or `int`) pattern.
        - If `annotation_value` is unexpected.
        - If `annotation` is not `tuple`, `type` nor `str` instance.
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
        choices, description, name, annotation_type, channel_types = parse_annotation(parameter)
    else:
        choices = parameter_configurer._choices
        description = parameter_configurer._description
        name = parameter_configurer._name
        annotation_type = parameter_configurer._type
        channel_types = parameter_configurer._channel_types
        
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
        parameter_converter = SlashCommandParameterConverter(parameter.name, annotation_type, converter, name,
            description, default, required, choices, channel_types)
    
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
    parameter_converter : ``ParameterConverter`` or `None`
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


def check_command_coroutine(func, allow_coroutine_generator_functions):
    """
    Checks whether the given `func` is a coroutine and whether it accepts only positional only parameters.
    
    Parameters
    ----------
    func : `async-callable`
        Command coroutine.
    
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
            raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got '
                f'{func!r}.')
        
        should_instance = True
    
    else:
        raise TypeError(
            f'`func` is not `async-callable` '
            f'{"nor a coroutine generator function " if allow_coroutine_generator_functions else ""}'
            f'and cannot be instanced to `async` either, got {func!r}.'
        )
    
    
    keyword_only_parameter_count = real_analyzer.get_non_default_keyword_only_parameter_count()
    if keyword_only_parameter_count:
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts keyword only parameters.')
    
    if real_analyzer.accepts_args():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts *args.')
    
    if real_analyzer.accepts_kwargs():
        raise TypeError(f'`{real_analyzer.real_function!r}` accepts **kwargs.')
    
    return analyzer, real_analyzer, should_instance


def get_slash_command_parameter_converters(func, parameter_configurers):
    """
    Parses the given `func`'s parameters.
    
    Parameters
    ----------
    func : `async-callable`
        The function used by a ``SlasherApplicationCommand``.
    parameter_configurers : `None` or `dict` of (`str`, ``SlasherApplicationCommandParameterConfigurerWrapper``) items
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
        - If a parameter's `annotation_value` is `list` instance, but it's elements do not match the
            `tuple` (`str`, `str` or `int`) pattern.
        - If a parameter's `annotation_value` is `dict` instance, but it's items do not match the
            (`str`, `str` or `int`) pattern.
        - If a parameter's `annotation_value` is unexpected.
        - If a parameter's `annotation` is `tuple`, but it's 1th element is neither `None` nor `str` instance.
    ValueError
        - If a parameter's `annotation` is a `tuple`, but it's length is out of the expected range [0:3].
        - If a parameter's `annotation_value` is `str` instance, but not any of the expected ones.
        - If a parameter's `annotation_value` is `type` instance, but not any of the expected ones.
        - If a parameter's `choice` amount is out of the expected range [1:25].
        - If a parameter's `choice` name is duped.
        - If a parameter's `choice` values are mixed types.
    """
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True)
    
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
        raise TypeError(f'`{real_analyzer.real_function!r}` should accept at maximum '
            f'`{APPLICATION_COMMAND_OPTIONS_MAX}` slash command options,  meanwhile it accepts '
            f'{slash_command_option_count}.')
    
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
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True)
    
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
        The function used by a ``SlasherApplicationCommand``.
    
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
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, True)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    target_converter_detected = False
    for parameter in parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        
        if (parameter_converter is None):
            if target_converter_detected:
                raise TypeError(f'`{real_analyzer.real_function!r}`\'s `{parameter.name}` do not refers to any of the '
                    f'expected internal parameters. Context commands do not accept any additional parameters.')
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
        The function used by a ``SlasherApplicationCommand``.
    
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
    analyzer, real_analyzer, should_instance = check_command_coroutine(func, False)
    
    parameters = real_analyzer.get_non_reserved_positional_parameters()
    
    parameter_converters = []
    
    value_converter_detected = False
    for parameter in parameters:
        parameter_converter = create_internal_parameter_converter(parameter)
        
        if (parameter_converter is None):
            if value_converter_detected:
                raise TypeError(f'`{real_analyzer.real_function!r}`\'s `{parameter.name}` do not refers to any of the '
                    f'expected internal parameters. Context commands do not accept any additional parameters.')
            else:
                parameter_converter = create_value_parameter_converter(parameter)
                value_converter_detected = True
        
        parameter_converters.append(parameter_converter)
    
    
    parameter_converters = tuple(parameter_converters)
    
    if should_instance:
        func = analyzer.instance()
    
    return func, parameter_converters
