__all__ = ('IntentFlag',)

from ...env import CACHE_PRESENCE

from ..bases import FlagBase


INTENT_SHIFT_GUILDS = 0
INTENT_SHIFT_GUILD_USERS = 1
INTENT_SHIFT_GUILD_MODERATION = 2
INTENT_SHIFT_GUILD_EXPRESSIONS = 3
INTENT_SHIFT_GUILD_INTEGRATIONS = 4
INTENT_SHIFT_GUILD_WEBHOOKS = 5
INTENT_SHIFT_GUILD_INVITES = 6
INTENT_SHIFT_GUILD_VOICE_STATES = 7
INTENT_SHIFT_GUILD_PRESENCES = 8
INTENT_SHIFT_GUILD_MESSAGES = 9
INTENT_SHIFT_GUILD_REACTIONS = 10
INTENT_SHIFT_GUILD_TYPINGS = 11
INTENT_SHIFT_DIRECT_MESSAGES = 12
INTENT_SHIFT_DIRECT_REACTIONS = 13
INTENT_SHIFT_DIRECT_TYPINGS = 14
INTENT_SHIFT_MESSAGE_CONTENT = 15
INTENT_SHIFT_GUILD_SCHEDULED_EVENTS = 16
INTENT_SHIFT_AUTO_MODERATION_CONFIGURATION = 20
INTENT_SHIFT_AUTO_MODERATION_EXECUTION = 21

INTENT_MASK_GUILDS = 1 << INTENT_SHIFT_GUILDS
INTENT_MASK_GUILD_USERS = 1 << INTENT_SHIFT_GUILD_USERS
INTENT_MASK_GUILD_MODERATION = 1 << INTENT_SHIFT_GUILD_MODERATION
INTENT_MASK_GUILD_EXPRESSIONS = 1 << INTENT_SHIFT_GUILD_EXPRESSIONS
INTENT_MASK_GUILD_INTEGRATIONS = 1 << INTENT_SHIFT_GUILD_INTEGRATIONS
INTENT_MASK_GUILD_WEBHOOKS = 1 << INTENT_SHIFT_GUILD_WEBHOOKS
INTENT_MASK_GUILD_INVITES = 1 << INTENT_SHIFT_GUILD_INVITES
INTENT_MASK_GUILD_VOICE_STATES = 1 << INTENT_SHIFT_GUILD_VOICE_STATES
INTENT_MASK_GUILD_PRESENCES = 1 << INTENT_SHIFT_GUILD_PRESENCES
INTENT_MASK_GUILD_MESSAGES = 1 << INTENT_SHIFT_GUILD_MESSAGES
INTENT_MASK_GUILD_REACTIONS = 1 << INTENT_SHIFT_GUILD_REACTIONS
INTENT_MASK_GUILD_TYPINGS = 1 << INTENT_SHIFT_GUILD_TYPINGS
INTENT_MASK_DIRECT_MESSAGES = 1 << INTENT_SHIFT_DIRECT_MESSAGES
INTENT_MASK_DIRECT_REACTIONS = 1 << INTENT_SHIFT_DIRECT_REACTIONS
INTENT_MASK_DIRECT_TYPINGS = 1 << INTENT_SHIFT_DIRECT_TYPINGS
INTENT_MASK_MESSAGE_CONTENT = 1 << INTENT_SHIFT_MESSAGE_CONTENT
INTENT_MASK_GUILD_SCHEDULED_EVENTS = 1 << INTENT_SHIFT_GUILD_SCHEDULED_EVENTS
INTENT_MASK_AUTO_MODERATION_CONFIGURATION = 1 << INTENT_SHIFT_AUTO_MODERATION_CONFIGURATION
INTENT_MASK_AUTO_MODERATION_EXECUTION = 1 << INTENT_SHIFT_AUTO_MODERATION_EXECUTION

INTENT_SHIFT_EVENTS = {
    INTENT_SHIFT_GUILDS: (
        'GUILD_CREATE',
        'GUILD_DELETE',
        'GUILD_UPDATE',
        'GUILD_ROLE_CREATE',
        'GUILD_ROLE_UPDATE',
        'GUILD_ROLE_DELETE',
        'CHANNEL_CREATE',
        'CHANNEL_UPDATE',
        'CHANNEL_DELETE',
        'CHANNEL_PINS_UPDATE',
        'STAGE_INSTANCE_CREATE',
        'STAGE_INSTANCE_UPDATE',
        'STAGE_INSTANCE_DELETE',
        'THREAD_CREATE',
        'THREAD_UPDATE',
        'THREAD_DELETE',
        'THREAD_LIST_SYNC',
        'THREAD_MEMBER_UPDATE',
        'THREAD_MEMBERS_UPDATE',
        'GUILD_APPLICATION_COMMAND_COUNTS_UPDATE',
        'GUILD_JOIN_REQUEST_CREATE',
        'GUILD_JOIN_REQUEST_DELETE',
        'GUILD_JOIN_REQUEST_UPDATE',
        'EMBEDDED_ACTIVITY_UPDATE',
    ),
    INTENT_SHIFT_GUILD_USERS: (
        'GUILD_MEMBER_ADD',
        'GUILD_MEMBER_UPDATE',
        'GUILD_MEMBER_REMOVE',
        'THREAD_MEMBERS_UPDATE',
    ),
    INTENT_SHIFT_GUILD_MODERATION: (
        'GUILD_AUDIT_LOG_ENTRY_CREATE',
        'GUILD_BAN_ADD',
        'GUILD_BAN_REMOVE',
    ),
    INTENT_SHIFT_GUILD_EXPRESSIONS: (
        'GUILD_EMOJIS_UPDATE',
        'GUILD_SOUNDBOARD_SOUND_CREATE',
        'GUILD_SOUNDBOARD_SOUND_DELETE',
        'GUILD_SOUNDBOARD_SOUND_UPDATE',
        'GUILD_SOUNDBOARD_SOUNDS_UPDATE',
        'GUILD_STICKERS_UPDATE',
        'SOUNDBOARD_SOUNDS',
    ),
    INTENT_SHIFT_GUILD_INTEGRATIONS: (
        'INTEGRATION_CREATE',
        'INTEGRATION_DELETE',
        'INTEGRATION_UPDATE',
        'GUILD_INTEGRATIONS_UPDATE',
    ),
    INTENT_SHIFT_GUILD_WEBHOOKS: (
        'WEBHOOKS_UPDATE',
    ),
    INTENT_SHIFT_GUILD_INVITES: (
        'INVITE_CREATE',
        'INVITE_DELETE',
    ),
    INTENT_SHIFT_GUILD_VOICE_STATES: (
        'VOICE_CHANNEL_EFFECT_SEND',
        'VOICE_STATE_UPDATE',
    ),
    INTENT_SHIFT_GUILD_PRESENCES: (
        'PRESENCE_UPDATE',
    ),
    INTENT_SHIFT_GUILD_MESSAGES: (
        'CHANNEL_PINS_UPDATE',
        'MESSAGE_CREATE',
        'MESSAGE_UPDATE',
        'MESSAGE_DELETE',
        'MESSAGE_DELETE_BULK', # Not listed by Discord, yayyyy
    ),
    INTENT_SHIFT_GUILD_REACTIONS: (
        'MESSAGE_REACTION_ADD',
        'MESSAGE_REACTION_REMOVE',
        'MESSAGE_REACTION_REMOVE_ALL',
        'MESSAGE_REACTION_REMOVE_EMOJI',
    ),
    INTENT_SHIFT_GUILD_TYPINGS: (
        'TYPING_START',
    ),
    INTENT_SHIFT_DIRECT_MESSAGES: (
        'CHANNEL_CREATE',
        'CHANNEL_PINS_UPDATE',
        'MESSAGE_CREATE',
        'MESSAGE_UPDATE',
        'MESSAGE_DELETE',
    ),
    INTENT_SHIFT_DIRECT_REACTIONS: (
        'MESSAGE_REACTION_ADD',
        'MESSAGE_REACTION_REMOVE',
        'MESSAGE_REACTION_REMOVE_ALL',
        'MESSAGE_REACTION_REMOVE_EMOJI',
    ),
    INTENT_SHIFT_DIRECT_TYPINGS: (
        'TYPING_START',
    ),
    INTENT_SHIFT_MESSAGE_CONTENT: (
    ),
    INTENT_SHIFT_GUILD_SCHEDULED_EVENTS: (
        'GUILD_SCHEDULED_EVENT_CREATE',
        'GUILD_SCHEDULED_EVENT_UPDATE',
        'GUILD_SCHEDULED_EVENT_DELETE',
        'GUILD_SCHEDULED_EVENT_USER_ADD',
        'GUILD_SCHEDULED_EVENT_USER_REMOVE',
    ),
    INTENT_SHIFT_AUTO_MODERATION_CONFIGURATION: (
        'AUTO_MODERATION_RULE_CREATE',
        'AUTO_MODERATION_RULE_DELETE',
        'AUTO_MODERATION_RULE_UPDATE',
    ),
    INTENT_SHIFT_AUTO_MODERATION_EXECUTION: (
        'AUTO_MODERATION_ACTION_EXECUTION',
    )
}

GLOBAL_INTENT_SHIFT_EVENTS = (
    'READY',
    'RESUMED',
    'USER_UPDATE',
    'CHANNEL_RECIPIENT_ADD', # User account only
    'CHANNEL_RECIPIENT_REMOVE', # User only
    'GUILD_MEMBERS_CHUNK',
    'VOICE_SERVER_UPDATE',
    'RELATIONSHIP_ADD', # User account only
    'RELATIONSHIP_REMOVE', # User account only
    'PRESENCES_REPLACE', # Empty / User account
    'USER_SETTINGS_UPDATE', # User account only
    'GIFT_CODE_UPDATE',
    'USER_ACHIEVEMENT_UPDATE', # User account only
    'MESSAGE_ACK', # User account only
    'SESSIONS_REPLACE', # User account only
    'INTERACTION_CREATE',
    'APPLICATION_COMMAND_CREATE',
    'APPLICATION_COMMAND_UPDATE',
    'APPLICATION_COMMAND_DELETE',
    'APPLICATION_COMMAND_PERMISSIONS_UPDATE',
    'USER_GUILD_SETTINGS_UPDATE', # User account only
    'CHANNEL_UNREAD_UPDATE', # User account only
    'GUILD_APPLICATION_COMMAND_INDEX_UPDATE', # Not documented
)

INTENT_SHIFT_DEFAULT_EVENT = 255
INTENT_SHIFT_MISSING_EVENT = 254


DISPATCH_EVENT_TO_INTENTS = {}

def populate_dispatch_event_intents():
    from itertools import chain
    
    for intent_shift, event_names in chain(
        INTENT_SHIFT_EVENTS.items(), ((INTENT_SHIFT_DEFAULT_EVENT, GLOBAL_INTENT_SHIFT_EVENTS),)
    ):
        
        for event_name in event_names:
            try:
                intent_shifts = DISPATCH_EVENT_TO_INTENTS[event_name]
            except KeyError:
                intent_shifts = (intent_shift, )
            else:
                intent_shifts = (*intent_shifts, intent_shift, )
            
            DISPATCH_EVENT_TO_INTENTS[event_name] = intent_shifts

populate_dispatch_event_intents()
del populate_dispatch_event_intents


class IntentFlag(FlagBase, enable_keyword = 'allow', disable_keyword = 'deny'):
    """
    An `int` subclass representing the intents to receive specific events. The wrapper picks these up as well and
    optimizes the dispatch events' events.
    
    Each flag specifies which parser's dispatch event is received from Discord. Not mentioned events do not depend
    on intent flags and they are expected to be received independently.
    
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | Intent flag position's                        | Shift | Intent name                   | Corresponding parser                        |
    | respective name                               | value |                               |                                             |
    +===============================================+=======+===============================+=============================================+
    | INTENT_SHIFT_GUILDS                           | 0     | guilds                        | GUILD_CREATE,                               |
    |                                               |       |                               | GUILD_DELETE,                               |
    |                                               |       |                               | GUILD_UPDATE,                               |
    |                                               |       |                               | GUILD_ROLE_CREATE,                          |
    |                                               |       |                               | GUILD_ROLE_UPDATE,                          |
    |                                               |       |                               | GUILD_ROLE_DELETE,                          |
    |                                               |       |                               | CHANNEL_CREATE,                             |
    |                                               |       |                               | CHANNEL_UPDATE,                             |
    |                                               |       |                               | CHANNEL_DELETE,                             |
    |                                               |       |                               | CHANNEL_PINS_UPDATE,                        |
    |                                               |       |                               | STAGE_INSTANCE_CREATE,                      |
    |                                               |       |                               | STAGE_INSTANCE_UPDATE,                      |
    |                                               |       |                               | STAGE_INSTANCE_DELETE,                      |
    |                                               |       |                               | THREAD_CREATE,                              |
    |                                               |       |                               | THREAD_UPDATE,                              |
    |                                               |       |                               | THREAD_DELETE,                              |
    |                                               |       |                               | THREAD_LIST_SYNC,                           |
    |                                               |       |                               | THREAD_MEMBER_UPDATE,                       |
    |                                               |       |                               | THREAD_MEMBERS_UPDATE,                      |
    |                                               |       |                               | GUILD_JOIN_REQUEST_CREATE,                  |
    |                                               |       |                               | GUILD_JOIN_REQUEST_DELETE,                  |
    |                                               |       |                               | GUILD_JOIN_REQUEST_UPDATE,                  |
    |                                               |       |                               | EMBEDDED_ACTIVITY_UPDATE                    |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_USERS                      | 1     | guild_users                   | GUILD_MEMBER_ADD,                           |
    |                                               |       |                               | GUILD_MEMBER_UPDATE,                        |
    |                                               |       |                               | GUILD_MEMBER_REMOVE,                        |
    |                                               |       |                               | THREAD_MEMBERS_UPDATE                       |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_MODERATION                 | 2     | guild_bans                    | GUILD_AUDIT_LOG_ENTRY_CREATE,               |
    |                                               |       |                               | GUILD_BAN_ADD,                              |
    |                                               |       |                               | GUILD_BAN_REMOVE                            |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_EXPRESSIONS                | 3     | guild_expressions             | GUILD_EMOJIS_UPDATE,                        |
    |                                               |       |                               | GUILD_SOUNDBOARD_SOUND_CREATE,              |
    |                                               |       |                               | GUILD_SOUNDBOARD_SOUND_DELETE,              |
    |                                               |       |                               | GUILD_SOUNDBOARD_SOUND_UPDATE,              |
    |                                               |       |                               | GUILD_SOUNDBOARD_SOUNDS_UPDATE,             |
    |                                               |       |                               | GUILD_STICKERS_UPDATE,                      |
    |                                               |       |                               | SOUNDBOARD_SOUNDS                           |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_INTEGRATIONS               | 4     | guild_integrations            | INTEGRATION_CREATE,                         |
    |                                               |       |                               | INTEGRATION_DELETE,                         |
    |                                               |       |                               | INTEGRATION_UPDATE,                         |
    |                                               |       |                               | GUILD_INTEGRATIONS_UPDATE                   |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_WEBHOOKS                   | 5     | guild_webhooks                | WEBHOOKS_UPDATE                             |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_INVITES                    | 6     | guild_invites                 | INVITE_CREATE,                              |
    |                                               |       |                               | INVITE_DELETE                               |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_VOICE_STATES               | 7     | guild_voice_states            | VOICE_CHANNEL_EFFECT_SEND,                  |
    |                                               |       |                               | VOICE_STATE_UPDATE                          |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_PRESENCES                  | 8     | guild_presences               | PRESENCE_UPDATE                             |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_MESSAGES                   | 9     | guild_messages                | CHANNEL_PINS_UPDATE,                        |
    |                                               |       |                               | MESSAGE_CREATE,                             |
    |                                               |       |                               | MESSAGE_UPDATE,                             |
    |                                               |       |                               | MESSAGE_DELETE,                             |
    |                                               |       |                               | MESSAGE_DELETE_BULK                         |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_REACTIONS                  | 10    | guild_reactions               | MESSAGE_REACTION_ADD,                       |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE,                    |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE_ALL,                |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE_EMOJI               |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_TYPINGS                    | 11    | guild_typings                 | TYPING_START                                |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_DIRECT_MESSAGES                  | 12    | direct_messages               | CHANNEL_CREATE,                             |
    |                                               |       |                               | CHANNEL_PINS_UPDATE,                        |
    |                                               |       |                               | MESSAGE_CREATE,                             |
    |                                               |       |                               | MESSAGE_UPDATE,                             |
    |                                               |       |                               | MESSAGE_DELETE                              |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_DIRECT_REACTIONS                 | 13    | direct_reactions              | MESSAGE_REACTION_ADD,                       |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE,                    |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE_ALL,                |
    |                                               |       |                               | MESSAGE_REACTION_REMOVE_EMOJI               |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_DIRECT_TYPINGS                   | 14    | direct_typings                | TYPING_START                                |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_MESSAGE_CONTENT                  | 15    | message_content               | N/A                                         |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_GUILD_SCHEDULED_EVENTS           | 16    | guild_scheduled_events        | GUILD_APPLICATION_COMMAND_COUNTS_UPDATE,    |
    |                                               |       |                               | GUILD_SCHEDULED_EVENT_CREATE,               |
    |                                               |       |                               | GUILD_SCHEDULED_EVENT_UPDATE,               |
    |                                               |       |                               | GUILD_SCHEDULED_EVENT_DELETE,               |
    |                                               |       |                               | GUILD_SCHEDULED_EVENT_USER_ADD,             |
    |                                               |       |                               | GUILD_SCHEDULED_EVENT_USER_REMOVE           |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_AUTO_MODERATION_CONFIGURATION    | 20    | auto_moderation_configuration | AUTO_MODERATION_RULE_CREATE                 |
    |                                               |       |                               | AUTO_MODERATION_RULE_DELETE                 |
    |                                               |       |                               | AUTO_MODERATION_RULE_UPDATE                 |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    | INTENT_SHIFT_AUTO_MODERATION_EXECUTION        | 21    | auto_moderation_execution     | AUTO_MODERATION_ACTION_EXECUTION            |
    +-----------------------------------------------+-------+-------------------------------+---------------------------------------------+
    """
    __keys__ = {
        'guilds': INTENT_SHIFT_GUILDS,
        'guild_users': INTENT_SHIFT_GUILD_USERS,
        'guild_moderation': INTENT_SHIFT_GUILD_MODERATION,
        'guild_expressions': INTENT_SHIFT_GUILD_EXPRESSIONS,
        'guild_integrations': INTENT_SHIFT_GUILD_INTEGRATIONS,
        'guild_webhooks': INTENT_SHIFT_GUILD_WEBHOOKS,
        'guild_invites': INTENT_SHIFT_GUILD_INVITES,
        'guild_voice_states': INTENT_SHIFT_GUILD_VOICE_STATES,
        'guild_presences': INTENT_SHIFT_GUILD_PRESENCES,
        'guild_messages': INTENT_SHIFT_GUILD_MESSAGES,
        'guild_reactions': INTENT_SHIFT_GUILD_REACTIONS,
        'guild_typings': INTENT_SHIFT_GUILD_TYPINGS,
        'direct_messages': INTENT_SHIFT_DIRECT_MESSAGES,
        'direct_reactions': INTENT_SHIFT_DIRECT_REACTIONS,
        'direct_typings': INTENT_SHIFT_DIRECT_TYPINGS,
        'message_content': INTENT_SHIFT_MESSAGE_CONTENT,
        'guild_scheduled_events': INTENT_SHIFT_GUILD_SCHEDULED_EVENTS,
        'auto_moderation_configuration': INTENT_SHIFT_AUTO_MODERATION_CONFIGURATION,
        'auto_moderation_execution': INTENT_SHIFT_AUTO_MODERATION_EXECUTION,
    }
    
    __deprecated_keys__ = {
        'guild_bans': (INTENT_SHIFT_GUILD_MODERATION, '2023 Jul', 'guild_moderation'),
        'guild_emojis_and_stickers': (INTENT_SHIFT_GUILD_MODERATION, '2023 Dec', 'guild_expressions'),
    }
    
    def __new__(cls, integer = -1):
        """
        Creates a new ``IntentFlag`` from the passed `integer`. If any invalid intent flag is passed, those
        will be removed. If the wrapper is started up without presence caching, then `.guild_presences` will be
        set to `False` by default.
        
        Parameters
        ----------
        integer : `int` = `-1`, Optional
            The value what will be converted ``IntentFlag``. If not passed or passed as a negative value,
            then returns an ``IntentFlag`` what contains all the enabled flags.
        
        Returns
        -------
        intent_flag : ``IntentFlag``
        
        Raises
        ------
        TypeError
            If `integer` was not passed as `int`.
        
        Notes
        -----
        The default created intent flags contain the privileged gateway intents, so if you have those disabled, or
        if those are not allowed for you, then make sure, you specify them.
        """
        if not isinstance(integer, int):
            raise TypeError(
                f'{cls.__name__} expected `int`, got {integer.__class__.__name__}; {integer!r}.'
            )
        
        intent_flag = 0
        if integer < 0:
            for value in cls.__keys__.values():
                intent_flag = intent_flag | (1 << value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                intent_flag = intent_flag^(1 << INTENT_SHIFT_GUILD_PRESENCES)
        else:
            for value in cls.__keys__.values():
                if (integer >> value) & 1:
                    intent_flag = intent_flag | (1 << value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                if intent_flag & INTENT_MASK_GUILD_PRESENCES:
                    intent_flag = intent_flag^INTENT_MASK_GUILD_PRESENCES
        
        return int.__new__(cls, intent_flag)
    
    
    def iterate_parser_names(self):
        """
        Yields every parser's name, what the intent flag allows to be received.
        
        This method is a generator.
        
        Yields
        ------
        parser_name : `str`
        """
        for shift in self.__keys__.values():
            if (self >> shift) & 1:
                yield from INTENT_SHIFT_EVENTS[shift]
        
        yield from GLOBAL_INTENT_SHIFT_EVENTS
