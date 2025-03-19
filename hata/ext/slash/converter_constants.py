__all__ = ()

from scarletio import un_map_pack

from ...discord.application_command import ApplicationCommandOptionType

from ...discord.channel import Channel, ChannelType
from ...discord.client import Client
from ...discord.interaction import InteractionEvent
from ...discord.message import Attachment
from ...discord.role import Role
from ...discord.user import ClientUserBase, User, UserBase

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

