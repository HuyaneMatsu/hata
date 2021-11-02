__all__ = ('APPLICATIONS', 'APPLICATION_COMMANDS', 'BUILTIN_EMOJIS', 'CHANNELS', 'CLIENTS', 'DISCOVERY_CATEGORIES',
    'EMOJIS', 'EULAS', 'GUILDS', 'INTEGRATIONS', 'INVITES', 'KOKORO', 'MESSAGES', 'ROLES', 'SCHEDULED_EVENTS',
    'STAGES', 'STICKERS', 'STICKER_PACKS', 'TEAMS', 'UNICODE_TO_EMOJI', 'USERS')

from ..backend.utils import WeakValueDictionary, WeakKeyDictionary
from ..backend.event_loop import EventThread

__doc__ = """
Contains core cache and other objects relative to hata.

Caches
------
- `CLIENTS` : ``dict``
    
    Contains the created ``Client`` instances.
    
    Clients are only available for garbage collection after calling ``Client._delete``.


Weak Caches
-----------
- `APPLICATIONS` : ``WeakValueDictionary``
    
    Stores the requested or received ``Application`` instanced.
    
    Only here to avoid duplication.

- `APPLICATION_COMMANDS` : ``WeakValueDictionary``

    Stores the created ``ApplicationCommand`` instances.

- `CHANNELS` : ``WeakValueDictionary``
    
    Contains various ``ChannelBase`` instances.

- `DISCOVERY_CATEGORIES` : ``WeakValueDictionary``
    
    Stores the available ``DiscoveryCategory``.
    
    Discovery categories are populated startup time.

- `EMOJIS` : ``WeakValueDictionary``
    
    Contains all the emojis stored by the wrapper. Unicode emojis are never garbage collected, because they are present
    in their own specific containers, like `BUILTIN_EMOJIS` or `UNICODE_TO_EMOJI`.

- `EULAS` : ``WeakValueDictionary``
    
    Stores the ``Eula`` instances.
    
    When requesting an eula, querying from the cache is always preferred over requesting it.

- `GUILDS` : ``WeakValueDictionary``

    Contains the created ``Guild`` instances.
    
- `INTEGRATIONS` : ``WeakValueDictionary``
    
    Contains ``Integration`` instances.

- `INVITES` : ``WeakValueDictionary``
    
    Stores the created ``Invite`` instances. They keys are the invites' code.
    
    Only here to avoid duplication.

- `MESSAGES` : ``WeakValueDictionary``

    All non-deleted ``Message`` is stored inside of `MESSAGES`.
    
    Messages hve short life cycle, since their channel stores only a limited amount of instances (or non if configured
    like that). So make sure to store a reference to your message, if you want to keep it alive and receive events
    related to it.

- `ROLES` : ``WeakValueDictionary``
    
    Stores the created ``Role`` instanced.

- `SCHEDULED_EVENTS` : ``WeakValueDictionary``
    
    Storage for ``ScheduledEvent`` instances.
    
- `STAGES` : ``WeakValueDictionary``
    
    Stores the created ``Stage`` instanced.

- `STICKERS` : ``WeakValueDictionary``
    
    Stores the created ``Sticker`` instances.

- `STICKER_PACKS` : ``WeakValueDictionary``
    
    Storage for ``StickerPack``-s.

- `TEAMS` : ``WeakValueDictionary``
    
    Stores the created application ``Team`` instances.
    
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

CLIENTS = {}

APPLICATIONS = WeakValueDictionary()
APPLICATION_COMMANDS = WeakValueDictionary()
CHANNELS = WeakValueDictionary()
DISCOVERY_CATEGORIES = WeakValueDictionary()
EMOJIS = WeakValueDictionary()
EULAS = WeakValueDictionary()
GUILDS = WeakValueDictionary()
INTEGRATIONS = WeakValueDictionary()
INVITES = WeakValueDictionary()
MESSAGES = WeakValueDictionary()
ROLES = WeakValueDictionary()
SCHEDULED_EVENTS = WeakValueDictionary()
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

KOKORO = EventThread(daemon=False, name='KOKORO')
