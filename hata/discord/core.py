"""
Contains core cache and other objects relative to hata.

Caches
------
- `CLIENTS` : ``dict``
    
    Contains the created ``Client``.
    
    Clients are only available for garbage collection after calling ``Client._delete``.


Weak Caches
-----------
- `APPLICATIONS` : ``WeakValueDictionary``
    
    Stores the requested or received ``Application``-s.
    
    Only here to avoid duplication.

- `APPLICATION_COMMANDS` : ``WeakValueDictionary``

    Stores the created ``ApplicationCommand``.

- `AUTO_MODERATION_RULES` : ``WeakValueDictionary``
    
    Stores the created ``AutoModerationRule``.

- `CHANNELS` : ``WeakValueDictionary``
    
    Contains various ``Channel``.

- `EMBEDDED_ACTIVITY_STATES` : ``WeakValueDictionary``
    
    Contains ``EmbeddedActivityState``.
    
- `EMOJIS` : ``WeakValueDictionary``
    
    Contains all the emojis stored by the wrapper. Unicode emojis are never garbage collected, because they are present
    in their own specific containers, like `BUILTIN_EMOJIS` / `UNICODE_TO_EMOJI`.

- `EULAS` : ``WeakValueDictionary``
    
    Stores the ``Eula``.
    
    When requesting an eula, querying from the cache is always preferred over requesting it.

- `FORUM_TAGS` : ``WeakValueDictionary``
    
    Stores the created ``ForumTag`` instances.

- `GUILDS` : ``WeakValueDictionary``

    Contains the created ``Guild``.
    
- `INTEGRATIONS` : ``WeakValueDictionary``
    
    Contains ``Integration``.

- `INVITES` : ``WeakValueDictionary``
    
    Stores the created ``Invite``. They keys are the invites' code.
    
    Only here to avoid duplication.

- `MESSAGES` : ``WeakValueDictionary``

    All non-deleted ``Message`` is stored inside of `MESSAGES`.
    
    Messages hve short life cycle, since their channel stores only a limited amount of instances (or non if configured
    like that). So make sure to store a reference to your message, if you want to keep it alive and receive events
    related to it.

- `ROLES` : ``WeakValueDictionary``
    
    Stores the created ``Role``d.

- `SCHEDULED_EVENTS` : ``WeakValueDictionary``
    
    Storage for ``ScheduledEvent``.
    
- `SOUNDBOARD_SOUNDS` : ``WeakValueDictionary``
    
    Storage for ``SoundboardSound``.

- `STAGES` : ``WeakValueDictionary``
    
    Stores the created ``Stage``d.

- `STICKERS` : ``WeakValueDictionary``
    
    Stores the created ``Sticker``.

- `STICKER_PACKS` : ``WeakValueDictionary``
    
    Storage for ``StickerPack``-s.

- `TEAMS` : ``WeakValueDictionary``
    
    Stores the created application ``Team``.
    
    Only here to avoid duplication.

- `USERS` : ``WeakValueDictionary``
    
    Stores the created user instances.


Resolution Tables
-----------------
- `BUILTIN_EMOJIS` : `dict`
    
    Contains each builtin (unicode) ``Emoji`` by name.
    
    Version selector 16 emojis can be also access by putting `_vs16` postfix after their name.

- `UNICODE_TO_EMOJI` : `dict`
    
    Contains each builtin (unicode) ``Emoji`` by their unicode value.

Internal Resolution Tables
--------------------------
- `APPLICATION_ID_TO_CLIENT` : `dict`
    
    ``Application`` to it's respective ``Client`` relation.

- `INTERACTION_EVENT_RESPONSE_WAITERS` : ``WeakValueDictionary``
    
    Interactions waiting for their response message.
    
    Keys are the identifier of ``InteractionEvent``-s, meanwhile the values are the ``InteractionEvent``-s themselves.
    Used to resolve interaction's first response message, since that is not returned by the API directly.
    

- `INTERACTION_EVENT_MESSAGE_WAITERS` : ``WeakKeyDictionary``
    
    Interaction response message waiters.
    
    When a `INTERACTION_EVENT_RESPONSE_WAITERS` resolution succeeded, the interaction's response waiter future is
    accessed, which are stored in `INTERACTION_EVENT_MESSAGE_WAITERS` within ``InteractionEvent`` - ``Future``
    relation.

Immortal Objects
----------------
- KOKORO : ``EventThread``
    
    The asynchronous event loop & thread running hata clients.
"""

__all__ = (
    'APPLICATIONS', 'APPLICATION_COMMANDS', 'BUILTIN_EMOJIS', 'CHANNELS', 'CLIENTS', 'EMBEDDED_ACTIVITY_STATES',
    'EMOJIS', 'EULAS', 'FORUM_TAGS', 'GUILDS', 'INTEGRATIONS', 'INVITES', 'KOKORO', 'MESSAGES', 'ROLES',
    'SCHEDULED_EVENTS', 'SOUNDBOARD_SOUNDS', 'STAGES', 'STICKERS', 'STICKER_PACKS', 'TEAMS', 'UNICODE_TO_EMOJI',
    'USERS'
)

from scarletio import WeakKeyDictionary, WeakValueDictionary, create_event_loop, get_event_loop


CLIENTS = {}

APPLICATIONS = WeakValueDictionary()
APPLICATION_COMMANDS = WeakValueDictionary()
AUTO_MODERATION_RULES = WeakValueDictionary()
CHANNELS = WeakValueDictionary()
EMBEDDED_ACTIVITY_STATES = WeakValueDictionary()
EMOJIS = WeakValueDictionary()
EULAS = WeakValueDictionary()
FORUM_TAGS = WeakValueDictionary()
GUILDS = WeakValueDictionary()
INTEGRATIONS = WeakValueDictionary()
INVITES = WeakValueDictionary()
MESSAGES = WeakValueDictionary()
ROLES = WeakValueDictionary()
SCHEDULED_EVENTS = WeakValueDictionary()
SOUNDBOARD_SOUNDS = WeakValueDictionary()
STAGES = WeakValueDictionary()
STICKERS = WeakValueDictionary()
STICKER_PACKS = WeakValueDictionary()
TEAMS = WeakValueDictionary()
USERS = WeakValueDictionary()

APPLICATION_ID_TO_CLIENT = {}
INTERACTION_EVENT_RESPONSE_WAITERS = WeakValueDictionary()
INTERACTION_EVENT_MESSAGE_WAITERS = WeakKeyDictionary()

BUILTIN_EMOJIS = {}
UNICODE_TO_EMOJI = {}

try:
    KOKORO = get_event_loop()
except RuntimeError:
    KOKORO = create_event_loop(daemon = False, name = 'KOKORO')
