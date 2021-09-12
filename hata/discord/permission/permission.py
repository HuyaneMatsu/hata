__all__ = ('Permission', )

import warnings

from ..bases import FlagBase

PERMISSION_SHIFT_CREATE_INSTANT_INVITE = 0
PERMISSION_SHIFT_KICK_USERS = 1
PERMISSION_SHIFT_BAN_USERS = 2
PERMISSION_SHIFT_ADMINISTRATOR = 3
PERMISSION_SHIFT_MANAGE_CHANNEL = 4
PERMISSION_SHIFT_MANAGE_GUILD = 5
PERMISSION_SHIFT_ADD_REACTION = 6
PERMISSION_SHIFT_VIEW_AUDIT_LOGS = 7
PERMISSION_SHIFT_PRIORITY_SPEAKER = 8
PERMISSION_SHIFT_STREAM = 9
PERMISSION_SHIFT_VIEW_CHANNEL = 10
PERMISSION_SHIFT_SEND_MESSAGES = 11
PERMISSION_SHIFT_SEND_TTS_MESSAGES = 12
PERMISSION_SHIFT_MANAGE_MESSAGES = 13
PERMISSION_SHIFT_EMBED_LINKS = 14
PERMISSION_SHIFT_ATTACH_FILES = 15
PERMISSION_SHIFT_READ_MESSAGE_HISTORY = 16
PERMISSION_SHIFT_MENTION_EVERYONE = 17
PERMISSION_SHIFT_USE_EXTERNAL_EMOJIS = 18
PERMISSION_SHIFT_VIEW_GUILD_INSIGHTS = 19
PERMISSION_SHIFT_CONNECT = 20
PERMISSION_SHIFT_SPEAK = 21
PERMISSION_SHIFT_MUTE_USERS = 22
PERMISSION_SHIFT_DEAFEN_USERS = 23
PERMISSION_SHIFT_MOVE_USERS = 24
PERMISSION_SHIFT_USE_VOICE_ACTIVATION = 25
PERMISSION_SHIFT_CHANGE_NICKNAME = 26
PERMISSION_SHIFT_MANAGE_NICKNAMES = 27
PERMISSION_SHIFT_MANAGE_ROLES = 28
PERMISSION_SHIFT_MANAGE_WEBHOOKS = 29
PERMISSION_SHIFT_MANAGE_EMOJIS_AND_STICKERS = 30
PERMISSION_SHIFT_USE_APPLICATION_COMMANDS = 31
PERMISSION_SHIFT_REQUEST_TO_SPEAK = 32
PERMISSION_SHIFT_MANAGE_THREADS = 34
PERMISSION_SHIFT_CREATE_PUBLIC_THREADS = 35
PERMISSION_SHIFT_CREATE_PRIVATE_THREADS = 36
PERMISSION_SHIFT_USE_EXTERNAL_STICKERS = 37
PERMISSION_SHIFT_SEND_MESSAGES_IN_THREADS = 38
PERMISSION_SHIFT_START_EMBEDDED_ACTIVITIES = 39


PERMISSION_MASK_CREATE_INSTANT_INVITE = 1<<PERMISSION_SHIFT_CREATE_INSTANT_INVITE
PERMISSION_MASK_KICK_USERS = 1<<PERMISSION_SHIFT_KICK_USERS
PERMISSION_MASK_BAN_USERS = 1<<PERMISSION_SHIFT_BAN_USERS
PERMISSION_MASK_ADMINISTRATOR = 1<<PERMISSION_SHIFT_ADMINISTRATOR
PERMISSION_MASK_MANAGE_CHANNEL = 1<<PERMISSION_SHIFT_MANAGE_CHANNEL
PERMISSION_MASK_MANAGE_GUILD = 1<<PERMISSION_SHIFT_MANAGE_GUILD
PERMISSION_MASK_ADD_REACTION = 1<<PERMISSION_SHIFT_ADD_REACTION
PERMISSION_MASK_VIEW_AUDIT_LOGS = 1<<PERMISSION_SHIFT_VIEW_AUDIT_LOGS
PERMISSION_MASK_PRIORITY_SPEAKER = 1<<PERMISSION_SHIFT_PRIORITY_SPEAKER
PERMISSION_MASK_STREAM = 1<<PERMISSION_SHIFT_STREAM
PERMISSION_MASK_VIEW_CHANNEL = 1<<PERMISSION_SHIFT_VIEW_CHANNEL
PERMISSION_MASK_SEND_MESSAGES = 1<<PERMISSION_SHIFT_SEND_MESSAGES
PERMISSION_MASK_SEND_TTS_MESSAGES = 1<<PERMISSION_SHIFT_SEND_TTS_MESSAGES
PERMISSION_MASK_MANAGE_MESSAGES = 1<<PERMISSION_SHIFT_MANAGE_MESSAGES
PERMISSION_MASK_EMBED_LINKS = 1<<PERMISSION_SHIFT_EMBED_LINKS
PERMISSION_MASK_ATTACH_FILES = 1<<PERMISSION_SHIFT_ATTACH_FILES
PERMISSION_MASK_READ_MESSAGE_HISTORY = 1<<PERMISSION_SHIFT_READ_MESSAGE_HISTORY
PERMISSION_MASK_MENTION_EVERYONE = 1<<PERMISSION_SHIFT_MENTION_EVERYONE
PERMISSION_MASK_USE_EXTERNAL_EMOJIS = 1<<PERMISSION_SHIFT_USE_EXTERNAL_EMOJIS
PERMISSION_MASK_VIEW_GUILD_INSIGHTS = 1<<PERMISSION_SHIFT_VIEW_GUILD_INSIGHTS
PERMISSION_MASK_CONNECT = 1<<PERMISSION_SHIFT_CONNECT
PERMISSION_MASK_SPEAK = 1<<PERMISSION_SHIFT_SPEAK
PERMISSION_MASK_MUTE_USERS = 1<<PERMISSION_SHIFT_MUTE_USERS
PERMISSION_MASK_DEAFEN_USERS = 1<<PERMISSION_SHIFT_DEAFEN_USERS
PERMISSION_MASK_MOVE_USERS = 1<<PERMISSION_SHIFT_MOVE_USERS
PERMISSION_MASK_USE_VOICE_ACTIVATION = 1<<PERMISSION_SHIFT_USE_VOICE_ACTIVATION
PERMISSION_MASK_CHANGE_NICKNAME = 1<<PERMISSION_SHIFT_CHANGE_NICKNAME
PERMISSION_MASK_MANAGE_NICKNAMES = 1<<PERMISSION_SHIFT_MANAGE_NICKNAMES
PERMISSION_MASK_MANAGE_ROLES = 1<<PERMISSION_SHIFT_MANAGE_ROLES
PERMISSION_MASK_MANAGE_WEBHOOKS = 1<<PERMISSION_SHIFT_MANAGE_WEBHOOKS
PERMISSION_MASK_MANAGE_EMOJIS_AND_STICKERS = 1<<PERMISSION_SHIFT_MANAGE_EMOJIS_AND_STICKERS
PERMISSION_MASK_USE_APPLICATION_COMMANDS = 1<<PERMISSION_SHIFT_USE_APPLICATION_COMMANDS
PERMISSION_MASK_REQUEST_TO_SPEAK = 1<<PERMISSION_SHIFT_REQUEST_TO_SPEAK
PERMISSION_MASK_MANAGE_THREADS = 1<<PERMISSION_SHIFT_MANAGE_THREADS
PERMISSION_MASK_CREATE_PUBLIC_THREADS = 1<<PERMISSION_SHIFT_CREATE_PUBLIC_THREADS
PERMISSION_MASK_CREATE_PRIVATE_THREADS = 1<<PERMISSION_SHIFT_CREATE_PRIVATE_THREADS
PERMISSION_MASK_USE_EXTERNAL_STICKERS = 1<<PERMISSION_SHIFT_USE_EXTERNAL_STICKERS
PERMISSION_MASK_SEND_MESSAGES_IN_THREADS = 1<<PERMISSION_SHIFT_SEND_MESSAGES_IN_THREADS
PERMISSION_MASK_START_EMBEDDED_ACTIVITIES = 1 <<PERMISSION_SHIFT_START_EMBEDDED_ACTIVITIES

class Permission(FlagBase, access_keyword='can', enable_keyword='allow', disable_keyword='deny'):
    """
    Represents a Discord permission.
    
    The implemented permissions are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | create_instant_invite         |  0                |
    +-------------------------------+-------------------+
    | kick_users                    |  1                |
    +-------------------------------+-------------------+
    | ban_users                     |  2                |
    +-------------------------------+-------------------+
    | administrator                 |  3                |
    +-------------------------------+-------------------+
    | manage_channel                |  4                |
    +-------------------------------+-------------------+
    | manage_guild                  |  5                |
    +-------------------------------+-------------------+
    | add_reactions                 |  6                |
    +-------------------------------+-------------------+
    | view_audit_logs               |  7                |
    +-------------------------------+-------------------+
    | priority_speaker              |  8                |
    +-------------------------------+-------------------+
    | stream                        |  9                |
    +-------------------------------+-------------------+
    | view_channel                  | 10                |
    +-------------------------------+-------------------+
    | send_messages                 | 11                |
    +-------------------------------+-------------------+
    | send_tts_messages             | 12                |
    +-------------------------------+-------------------+
    | manage_messages               | 13                |
    +-------------------------------+-------------------+
    | embed_links                   | 14                |
    +-------------------------------+-------------------+
    | attach_files                  | 15                |
    +-------------------------------+-------------------+
    | read_message_history          | 16                |
    +-------------------------------+-------------------+
    | mention_everyone              | 17                |
    +-------------------------------+-------------------+
    | use_external_emojis           | 18                |
    +-------------------------------+-------------------+
    | connect                       | 20                |
    +-------------------------------+-------------------+
    | speak                         | 21                |
    +-------------------------------+-------------------+
    | mute_users                    | 22                |
    +-------------------------------+-------------------+
    | deafen_users                  | 23                |
    +-------------------------------+-------------------+
    | move_users                    | 24                |
    +-------------------------------+-------------------+
    | use_voice_activation          | 25                |
    +-------------------------------+-------------------+
    | change_nickname               | 26                |
    +-------------------------------+-------------------+
    | manage_nicknames              | 27                |
    +-------------------------------+-------------------+
    | manage_roles                  | 28                |
    +-------------------------------+-------------------+
    | manage_webhooks               | 29                |
    +-------------------------------+-------------------+
    | manage_emojis_and_stickers    | 30                |
    +-------------------------------+-------------------+
    | use_application_commands      | 31                |
    +-------------------------------+-------------------+
    | request_to_speak              | 32                |
    +-------------------------------+-------------------+
    | manage_threads                | 34                |
    +-------------------------------+-------------------+
    | create_public_threads         | 35                |
    +-------------------------------+-------------------+
    | create_private_threads        | 36                |
    +-------------------------------+-------------------+
    | use_external_stickers         | 37                |
    +-------------------------------+-------------------+
    | send_messages_in_threads      | 38                |
    +-------------------------------+-------------------+
    | start_embedded_activities     | 39                |
    +-------------------------------+-------------------+
    
    Each permission can be accessed as property with `can_` + it's respective name, meanwhile a new edited permission
    can be created with the `allow_...` and with the `deny_...` methods.
    """
    __keys__ = {
        'create_instant_invite': PERMISSION_SHIFT_CREATE_INSTANT_INVITE,
        'kick_users': PERMISSION_SHIFT_KICK_USERS,
        'ban_users': PERMISSION_SHIFT_BAN_USERS,
        'administrator': PERMISSION_SHIFT_ADMINISTRATOR,
        'manage_channel': PERMISSION_SHIFT_MANAGE_CHANNEL,
        'manage_guild': PERMISSION_SHIFT_MANAGE_GUILD,
        'add_reactions': PERMISSION_SHIFT_ADD_REACTION,
        'view_audit_logs': PERMISSION_SHIFT_VIEW_AUDIT_LOGS,
        'priority_speaker': PERMISSION_SHIFT_PRIORITY_SPEAKER,
        'stream': PERMISSION_SHIFT_STREAM,
        'view_channel': PERMISSION_SHIFT_VIEW_CHANNEL,
        'send_messages': PERMISSION_SHIFT_SEND_MESSAGES,
        'send_tts_messages': PERMISSION_SHIFT_SEND_TTS_MESSAGES,
        'manage_messages': PERMISSION_SHIFT_MANAGE_MESSAGES,
        'embed_links': PERMISSION_SHIFT_EMBED_LINKS,
        'attach_files': PERMISSION_SHIFT_ATTACH_FILES,
        'read_message_history': PERMISSION_SHIFT_READ_MESSAGE_HISTORY,
        'mention_everyone': PERMISSION_SHIFT_MENTION_EVERYONE,
        'use_external_emojis': PERMISSION_SHIFT_USE_EXTERNAL_EMOJIS,
        'view_guild_insights': PERMISSION_SHIFT_VIEW_GUILD_INSIGHTS,
        'connect': PERMISSION_SHIFT_CONNECT,
        'speak': PERMISSION_SHIFT_SPEAK,
        'mute_users': PERMISSION_SHIFT_MUTE_USERS,
        'deafen_users': PERMISSION_SHIFT_DEAFEN_USERS,
        'move_users': PERMISSION_SHIFT_MOVE_USERS,
        'use_voice_activation': PERMISSION_SHIFT_USE_VOICE_ACTIVATION,
        'change_nickname': PERMISSION_SHIFT_CHANGE_NICKNAME,
        'manage_nicknames': PERMISSION_SHIFT_MANAGE_NICKNAMES,
        'manage_roles': PERMISSION_SHIFT_MANAGE_ROLES,
        'manage_webhooks': PERMISSION_SHIFT_MANAGE_WEBHOOKS,
        'manage_emojis_and_stickers': PERMISSION_SHIFT_MANAGE_EMOJIS_AND_STICKERS,
        'use_application_commands': PERMISSION_SHIFT_USE_APPLICATION_COMMANDS,
        'request_to_speak': PERMISSION_SHIFT_REQUEST_TO_SPEAK,
        'manage_threads': PERMISSION_SHIFT_MANAGE_THREADS,
        'create_public_threads': PERMISSION_SHIFT_CREATE_PUBLIC_THREADS,
        'create_private_threads': PERMISSION_SHIFT_CREATE_PRIVATE_THREADS,
        'use_external_stickers': PERMISSION_SHIFT_USE_EXTERNAL_STICKERS,
        'send_messages_in_threads': PERMISSION_SHIFT_SEND_MESSAGES_IN_THREADS,
        'start_embedded_activities': PERMISSION_SHIFT_START_EMBEDDED_ACTIVITIES,
    }
    
    
    @property
    def can_manage_emojis(self):
        """
        The `manage_emojis` permission is deprecated and will be removed in 2021 September.
        Please use ``.manage_emojis_and_stickers`` instead.
        """
        warnings.warn(
            'The `manage_emojis` permission is deprecated and will be removed in 2021 September. '
            'Please use `manage_emojis_and_stickers`. instead',
            FutureWarning)
        
        return self.can_manage_emojis_and_stickers
    
    
    @property
    def allow_manage_emojis(self):
        """
        The `manage_emojis` permission is deprecated and will be removed in 2021 September.
        Please use ``.manage_emojis_and_stickers`` instead.
        """
        warnings.warn(
            'The `manage_emojis` permission is deprecated and will be removed in 2021 September. '
            'Please use `manage_emojis_and_stickers` instead.',
            FutureWarning)
        
        return self.allow_manage_emojis_and_stickers


    @property
    def deny_manage_emojis(self):
        """
        The `manage_emojis` permission is deprecated and will be removed in 2021 September.
        Please use ``.manage_emojis_and_stickers`` instead.
        """
        warnings.warn(
            'The `manage_emojis` permission is deprecated and will be removed in 2021 September. '
            'Please use `.manage_emojis_and_stickers` instead.',
            FutureWarning)
        
        return self.deny_manage_emojis_and_stickers
    
    
    @property
    def can_use_public_threads(self):
        """
        The `can_use_public_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.can_create_public_threads`` instead.
        """
        warnings.warn(
            'The `use_public_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.can_create_public_threads` instead.',
            FutureWarning)
        
        return self.can_create_public_threads
    
    
    @property
    def allow_use_public_threads(self):
        """
        The `use_public_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.allow_create_public_threads`` instead.
        """
        warnings.warn(
            'The `use_public_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.allow_create_public_threads`. instead',
            FutureWarning)
        
        return self.allow_create_public_threads
    
    
    @property
    def deny_use_public_threads(self):
        """
        The `use_public_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.deny_create_public_threads`` instead.
        """
        warnings.warn(
            'The `use_public_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.deny_create_public_threads`. instead',
            FutureWarning)
        
        return self.deny_create_public_threads
    
    
    @property
    def can_use_private_threads(self):
        """
        The `can_use_private_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.can_create_private_threads`` instead.
        """
        warnings.warn(
            'The `use_private_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.can_create_private_threads` instead.',
            FutureWarning)
        
        return self.can_create_private_threads
    
    
    @property
    def allow_use_private_threads(self):
        """
        The `use_private_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.allow_create_private_threads`` instead.
        """
        warnings.warn(
            'The `use_private_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.allow_create_private_threads`. instead',
            FutureWarning)
        
        return self.allow_create_private_threads
    
    
    @property
    def deny_use_private_threads(self):
        """
        The `use_private_threads` permission is deprecated and will be removed in 2021 November.
        Please use ``.deny_create_private_threads`` instead.
        """
        warnings.warn(
            'The `use_private_threads` permission is deprecated and will be removed in 2021 November. '
            'Please use `.deny_create_private_threads`. instead',
            FutureWarning)
        
        return self.deny_create_private_threads




PERMISSION_ALL = Permission().update_by_keys(
    create_instant_invite = True,
    kick_users = True,
    ban_users = True,
    administrator = True,
    manage_channel = True,
    manage_guild = True,
    add_reactions = True,
    view_audit_logs = True,
    priority_speaker = True,
    stream = True,
    view_channel = True,
    send_messages = True,
    send_tts_messages = True,
    manage_messages = True,
    embed_links = True,
    attach_files = True,
    read_message_history = True,
    mention_everyone = True,
    use_external_emojis = True,
    view_guild_insights = True,
    connect = True,
    speak = True,
    mute_users = True,
    deafen_users = True,
    move_users = True,
    use_voice_activation = True,
    change_nickname = True,
    manage_nicknames = True,
    manage_roles = True,
    manage_webhooks = True,
    manage_emojis_and_stickers = True,
    use_application_commands = True,
    request_to_speak = True,
    manage_threads = True,
    create_public_threads = True,
    create_private_threads = True,
    use_external_stickers = True,
    send_messages_in_threads = True,
    start_embedded_activities = True,
)

PERMISSION_NONE = Permission()

PERMISSION_PRIVATE = Permission().update_by_keys(
    create_instant_invite = False,
    kick_users = False,
    ban_users = False,
    administrator = False,
    manage_channel = False,
    manage_guild = False,
    add_reactions = True,
    view_audit_logs = False,
    priority_speaker = False,
    stream = False,
    view_channel = True,
    send_messages = True,
    send_tts_messages = False,
    manage_messages = False,
    embed_links = True,
    attach_files = True,
    read_message_history = True,
    mention_everyone = True,
    use_external_emojis = True,
    view_guild_insights = False,
    connect = False,
    speak = False,
    mute_users = False,
    deafen_users = False,
    move_users = False,
    use_voice_activation = True,
    change_nickname = False,
    manage_nicknames = False,
    manage_roles = False,
    manage_webhooks = False,
    manage_emojis_and_stickers = False,
    manage_threads = False,
    use_application_commands = True,
    request_to_speak = False,
    use_external_stickers = True,
    send_messages_in_threads = False,
    start_embedded_activities = False,
)

PERMISSION_PRIVATE_BOT = PERMISSION_PRIVATE.update_by_keys(
    read_message_history = False,
)

PERMISSION_GROUP = PERMISSION_PRIVATE.update_by_keys(
    create_instant_invite = True,
)

PERMISSION_GROUP_OWNER = PERMISSION_GROUP.update_by_keys(
    kick_users = True,
)

PERMISSION_TEXT_ALL = Permission().update_by_keys(
    create_instant_invite = False,
    kick_users = False,
    ban_users = False,
    administrator = False,
    manage_channel = False,
    manage_guild = False,
    add_reactions = True,
    view_audit_logs = False,
    priority_speaker = False,
    stream = False,
    view_channel = False,
    send_messages = True,
    send_tts_messages = True,
    manage_messages = False,
    embed_links = True,
    attach_files = True,
    read_message_history = False,
    mention_everyone = True,
    use_external_emojis = True,
    view_guild_insights = False,
    connect = False,
    speak = False,
    mute_users = False,
    deafen_users = False,
    move_users = False,
    use_voice_activation = False,
    change_nickname = False,
    manage_nicknames = False,
    manage_roles = False,
    manage_webhooks = False,
    manage_emojis_and_stickers = False,
    use_application_commands = True,
    request_to_speak = False,
    manage_threads = True,
    create_public_threads = True,
    create_private_threads = True,
    use_external_stickers = True,
    send_messages_in_threads = True,
    start_embedded_activities = False,
)

PERMISSION_TEXT_DENY = Permission(~PERMISSION_TEXT_ALL)

PERMISSION_DENY_SEND_MESSAGES_IN_THREADS_ONLY = PERMISSION_ALL.update_by_keys(
    send_messages_in_threads = False,
)

PERMISSION_DENY_SEND_MESSAGES_ONLY = PERMISSION_ALL.update_by_keys(
    send_messages = False,
)

PERMISSION_TEXT_AND_STAGE_DENY = PERMISSION_TEXT_DENY.update_by_keys(
    request_to_speak = False,
)

PERMISSION_VOICE_ALL = Permission().update_by_keys(
    create_instant_invite = False,
    kick_users = False,
    ban_users = False,
    administrator = False,
    manage_channel = False,
    manage_guild = False,
    add_reactions = False,
    view_audit_logs = False,
    priority_speaker = True,
    stream = True,
    view_channel = False,
    send_messages = False,
    send_tts_messages = False,
    manage_messages = False,
    embed_links = False,
    attach_files = False,
    read_message_history = False,
    mention_everyone = False,
    use_external_emojis = False,
    view_guild_insights = False,
    connect = True,
    speak = True,
    mute_users = True,
    deafen_users = True,
    move_users = True,
    use_voice_activation = True,
    change_nickname = False,
    manage_nicknames = False,
    manage_roles = False,
    manage_webhooks = False,
    manage_emojis_and_stickers = False,
    use_application_commands = False,
    request_to_speak = True,
    manage_threads = False,
    create_public_threads = False,
    create_private_threads = False,
    use_external_stickers = False,
    send_messages_in_threads = False,
    start_embedded_activities = True,
)

PERMISSION_VOICE_DENY = Permission(~PERMISSION_VOICE_ALL)

PERMISSION_THREAD_AND_VOICE_DENY = PERMISSION_VOICE_DENY.update_by_keys(
    create_public_threads = False,
    create_private_threads = False,
    use_external_stickers = False,
)

PERMISSION_VOICE_DENY_CONNECTION = PERMISSION_VOICE_DENY.update_by_keys(
    manage_roles = False,
    manage_channel = False,
)

PERMISSION_TEXT_AND_VOICE_DENY = Permission(PERMISSION_THREAD_AND_VOICE_DENY|PERMISSION_VOICE_DENY)

PERMISSION_STAGE_MODERATOR = Permission().update_by_keys(
    create_instant_invite = False,
    kick_users = False,
    ban_users = False,
    administrator = False,
    manage_channel = False,
    manage_guild = False,
    add_reactions = False,
    view_audit_logs = False,
    priority_speaker = False,
    stream = False,
    view_channel = False,
    send_messages = False,
    send_tts_messages = False,
    manage_messages = False,
    embed_links = False,
    attach_files = False,
    read_message_history = False,
    mention_everyone = False,
    use_external_emojis = False,
    view_guild_insights = False,
    connect = False,
    speak = False,
    mute_users = True,
    deafen_users = False,
    move_users = True,
    use_voice_activation = False,
    change_nickname = False,
    manage_nicknames = False,
    manage_roles = False,
    manage_webhooks = False,
    manage_emojis_and_stickers = False,
    use_application_commands = False,
    request_to_speak = True,
    manage_threads = False,
    create_public_threads = False,
    create_private_threads = False,
    use_external_stickers = False,
    send_messages_in_threads = False,
)

PERMISSION_CAN_SEND_MESSAGES_ALL = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,

)
