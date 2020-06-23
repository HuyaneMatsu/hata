# -*- coding: utf-8 -*-
__all__ = ('EventBase', 'EventHandlerBase', 'EventWaitforBase', 'GuildUserChunkEvent', 'IntentFlag',
    'ReactionAddEvent', 'ReactionDeleteEvent', 'eventlist', )

import sys, datetime
from time import monotonic
try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ..backend.futures import Future, Task, iscoroutinefunction as iscoro
from ..backend.dereaddons_local import function, RemovedDescriptor, _spaceholder, MethodLike, NEEDS_DUMMY_INIT, \
    WeakKeyDictionary, WeakReferer
from ..backend.analyzer import CallableAnalyzer

from .bases import FlagBase
from .client_core import CACHE_USER, CACHE_PRESENCE, CLIENTS, CHANNELS, GUILDS, MESSAGES, KOKORO
from .user import User, PartialUser, USERS
from .channel import CHANNEL_TYPES, ChannelGuildBase
from .others import Relationship, Gift
from .guild import EMOJI_UPDATE_NEW, EMOJI_UPDATE_DELETE, EMOJI_UPDATE_EDIT, Guild
from .emoji import PartialEmoji
from .role import Role
from .exceptions import DiscordException, ERROR_CODES
from .invite import Invite
from .message import EMBED_UPDATE_NONE

utcfromtimestamp=datetime.datetime.utcfromtimestamp

class EVENT_SYSTEM_CORE(object):
    """
    Stores expected argcount amount and event-parser name relations.
    
    Attributes
    ----------
    defaults : `dict` of (`str`, `int`) items
        Event name - expected argument count relation for checking whether the passed event expects the correct amount
        of arguments.
    parsers : `dict` of (`str`, `tuple` (`str`, `str`)) items
        Event name - tuple of parser names relation for checking which parser is used when an event is added.
    """
    __slots__=('defaults', 'parsers',)
    def __init__(self):
        """
        Creates an ``EVENT_SYSTEM_CORE`` instance. This method is called only once, when creating
        `hata.discord.parsers.EVENTS`.
        """
        self.defaults = {}
        self.parsers = {}
    
    def add_default(self, name, value, parser):
        """
        Adds a new event-name argcount parser names relation to the event system core instance.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        value : `int`
            The amount of arguments what the parser passes the respective event.
        parser : `str` or (`tuple` of `str`)
            The name of parsers, which might call the respective event.
        """
        self.defaults[name] = value
        if (type(parser) is not tuple):
            parser = (parser,)
        self.parsers[name] = parser
    
    def get_argcount(self, name):
        """
        Returns the amount of arguments, what the parsers would pass to the respective event.
        
        Parameters
        ----------
        name : `str`
            The event's name.
        
        Returns
        -------
        argcount : `int`
            The amount of arguments, what to the respective event would be passed.
        
        Raises
        ------
        LookupError
            There is no event defined with the specific name.
        """
        try:
            argcount = self.defaults[name]
        except KeyError:
            raise LookupError(f'Invalid Event name: `{name!r}`.') from None
        return argcount


INTENT_GUILDS             = 0
INTENT_GUILD_USERS        = 1
INTENT_GUILD_BANS         = 2
INTENT_GUILD_EMOJIS       = 3
INTENT_GUILD_INTEGRATIONS = 4
INTENT_GUILD_WEBHOOKS     = 5
INTENT_GUILD_INVITES      = 6
INTENT_GUILD_VOICE_STATES = 7
INTENT_GUILD_PRESENCES    = 8
INTENT_GUILD_MESSAGES     = 9
INTENT_GUILD_REACTIONS    = 10
INTENT_GUILD_TYPINGS      = 11
INTENT_DIRECT_MESSAGES    = 12
INTENT_DIRECT_REACTIONS   = 13
INTENT_DIRECT_TYPINGS     = 14

INTENT_EVENTS = {
    INTENT_GUILDS : (
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
            ),
    INTENT_GUILD_USERS : (
        'GUILD_MEMBER_ADD',
        'GUILD_MEMBER_UPDATE',
        'GUILD_MEMBER_REMOVE',
            ),
    INTENT_GUILD_BANS : (
        'GUILD_BAN_ADD',
        'GUILD_BAN_REMOVE',
            ),
    INTENT_GUILD_EMOJIS : (
        'GUILD_EMOJIS_UPDATE',
            ),
    INTENT_GUILD_INTEGRATIONS : (
        'GUILD_INTEGRATIONS_UPDATE',
            ),
    INTENT_GUILD_WEBHOOKS : (
        'WEBHOOKS_UPDATE',
            ),
    INTENT_GUILD_INVITES : (
        'INVITE_CREATE',
        'INVITE_DELETE',
            ),
    INTENT_GUILD_VOICE_STATES : (
        'VOICE_STATE_UPDATE',
            ),
    INTENT_GUILD_PRESENCES : (
        'PRESENCE_UPDATE',
            ),
    INTENT_GUILD_MESSAGES : (
        'MESSAGE_CREATE',
        'MESSAGE_UPDATE',
        'MESSAGE_DELETE',
        'MESSAGE_DELETE_BULK', # Not listed by Discord, yayyyy
            ),
    INTENT_GUILD_REACTIONS : (
        'MESSAGE_REACTION_ADD',
        'MESSAGE_REACTION_REMOVE',
        'MESSAGE_REACTION_REMOVE_ALL',
        'MESSAGE_REACTION_REMOVE_EMOJI',
            ),
    INTENT_GUILD_TYPINGS : (
        'TYPING_START',
            ),
    INTENT_DIRECT_MESSAGES : (
        'CHANNEL_CREATE',
        'CHANNEL_PINS_UPDATE',
        'MESSAGE_CREATE',
        'MESSAGE_UPDATE',
        'MESSAGE_DELETE',
            ),
    INTENT_DIRECT_REACTIONS : (
        'MESSAGE_REACTION_ADD',
        'MESSAGE_REACTION_REMOVE',
        'MESSAGE_REACTION_REMOVE_ALL',
        'MESSAGE_REACTION_REMOVE_EMOJI',
            ),
    INTENT_DIRECT_TYPINGS : (
        'TYPING_START',
            ),
        }

GLOBAL_INTENT_EVENTS = (
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
    'USER_ACHIEVEMENT_UPDATE', # User acount only
    'MESSAGE_ACK', # User account only
    'SESSIONS_REPLACE', # User account only
        )

class IntentFlag(FlagBase, enable_keyword='allow', disable_keyword='deny'):
    """
    An `int` subclass representing the intents to receive specific events. The wrapper picks these up as well and
    optimizes the dispatch events' parsers.
    
    Each flag specifies which parser's dispatch event is received from Discord. Not mentioned parsers do not depend
    on intent flags and they are expected to be received independently.
    
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | Intent flag position's    | Shift value   | Intent name           | Coresponding parser               |
    | respective name           |               |                       |                                   |
    +===========================+===============+=======================+===================================+
    | INTENT_GUILDS             | 0             | guilds                | GUILD_CREATE                      |
    |                           |               |                       | GUILD_DELETE                      |
    |                           |               |                       | GUILD_UPDATE                      |
    |                           |               |                       | GUILD_ROLE_CREATE                 |
    |                           |               |                       | GUILD_ROLE_UPDATE                 |
    |                           |               |                       | GUILD_ROLE_DELETE                 |
    |                           |               |                       | CHANNEL_CREATE                    |
    |                           |               |                       | CHANNEL_UPDATE                    |
    |                           |               |                       | CHANNEL_DELETE                    |
    |                           |               |                       | CHANNEL_PINS_UPDATE               |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_USERS        | 1             | guild_users           | GUILD_MEMBER_ADD                  |
    |                           |               |                       | GUILD_MEMBER_UPDATE               |
    |                           |               |                       | GUILD_MEMBER_REMOVE               |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_BANS         | 2             | guild_bans            | GUILD_BAN_ADD                     |
    |                           |               |                       | GUILD_BAN_REMOVE                  |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_EMOJIS       | 3             | guild_emojis          | GUILD_EMOJIS_UPDATE               |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_INTEGRATIONS | 4             | guild_integrations    | GUILD_INTEGRATIONS_UPDATE         |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_WEBHOOKS     | 5             | guild_webhooks        | WEBHOOKS_UPDATE                   |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_INVITES      | 6             | guild_invites         | INVITE_CREATE                     |
    |                           |               |                       | INVITE_DELETE                     |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_VOICE_STATES | 7             | guild_voice_states    | VOICE_STATE_UPDATE                |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_PRESENCES    | 8             | guild_presences       | PRESENCE_UPDATE                   |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_MESSAGES     | 9             | guild_messages        | MESSAGE_CREATE                    |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    |                           |               |                       | MESSAGE_UPDATE                    |
    |                           |               |                       | MESSAGE_DELETE                    |
    |                           |               |                       | MESSAGE_DELETE_BULK               |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_REACTIONS    | 10            | guild_reactions       | MESSAGE_REACTION_ADD              |
    |                           |               |                       | MESSAGE_REACTION_REMOVE           |
    |                           |               |                       | MESSAGE_REACTION_REMOVE_ALL       |
    |                           |               |                       | MESSAGE_REACTION_REMOVE_EMOJI     |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_GUILD_TYPINGS      | 11            | guild_typings         | TYPING_START                      |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_DIRECT_MESSAGES    | 12            | direct_messages       | CHANNEL_CREATE                    |
    |                           |               |                       | CHANNEL_PINS_UPDATE               |
    |                           |               |                       | MESSAGE_CREATE                    |
    |                           |               |                       | MESSAGE_UPDATE                    |
    |                           |               |                       | MESSAGE_DELETE                    |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_DIRECT_REACTIONS   | 13            | direct_reactions      | MESSAGE_REACTION_ADD              |
    |                           |               |                       | MESSAGE_REACTION_REMOVE           |
    |                           |               |                       | MESSAGE_REACTION_REMOVE_ALL       |
    |                           |               |                       | MESSAGE_REACTION_REMOVE_EMOJI     |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    | INTENT_DIRECT_TYPINGS     | 14            | direct_typings        | TYPING_START                      |
    +---------------------------+---------------+-----------------------+-----------------------------------+
    """
    __keys__ = {
        'guilds'            : INTENT_GUILDS,
        'guild_users'       : INTENT_GUILD_USERS,
        'guild_bans'        : INTENT_GUILD_BANS,
        'guild_emojis'      : INTENT_GUILD_EMOJIS,
        'guild_integrations': INTENT_GUILD_INTEGRATIONS,
        'guild_webhooks'    : INTENT_GUILD_WEBHOOKS,
        'guild_invites'     : INTENT_GUILD_INVITES,
        'guild_voice_states': INTENT_GUILD_VOICE_STATES,
        'guild_presences'   : INTENT_GUILD_PRESENCES,
        'guild_messages'    : INTENT_GUILD_MESSAGES,
        'guild_reactions'   : INTENT_GUILD_REACTIONS,
        'guild_typings'     : INTENT_GUILD_TYPINGS,
        'direct_messages'   : INTENT_DIRECT_MESSAGES,
        'direct_reactions'  : INTENT_DIRECT_REACTIONS,
        'direct_typings'    : INTENT_DIRECT_TYPINGS,
            }
    
    def __new__(cls, int_ = -1):
        """
        Creates a new ``IntentFlag`` instance from the passed `int_`. If any invalid intent flag is passed, those
        will be removed. If the wrapper is started up without presence caching, then `.guild_presences` will be
        set to `False` by default.
        
        Parameters
        ----------
        int_ : `int` instance, Optional
            The value what will be converted ``IntentFlag`` instance. If not passed or passed as a negative value,
            then returns an ``IntentFlag`` what contains all the enabled flags.
        
        Returns
        -------
        inetnt_flag : ``IntentFlag``
        
        Raises
        ------
        TypeError
            If `int_` was not passed as `int` instance.
        
        Notes
        -----
        The defaultly created intent flags contain the privileged gateway intents, so if you have those disabled, or
        if those are not allowed for you, then make sure, you specify them.
        """
        if not isinstance(int_, int):
            raise TypeError(f'{cls.__name__} expected `int` instance, got `{int_!r}')
        
        inetnt_flag = 0
        if int_ < 0:
            for value in cls.__keys__.values():
                inetnt_flag = inetnt_flag|(1<<value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                inetnt_flag = inetnt_flag^(1<<INTENT_GUILD_PRESENCES)
        else:
            for value in cls.__keys__.values():
                if (int_>>value)&1:
                    inetnt_flag = inetnt_flag|(1<<value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                if (inetnt_flag>>INTENT_GUILD_PRESENCES)&1:
                    inetnt_flag = inetnt_flag^(1<<INTENT_GUILD_PRESENCES)
        
        return int.__new__(cls, inetnt_flag)
    
    def iterate_parser_names(self):
        """
        Yields every parser's name, what the intent flag allows to be received.

        Yields
        ------
        parser_name : `str`
        """
        for shift in self.__keys__.values():
            if (self>>shift)&1:
                yield from INTENT_EVENTS[shift]
        
        yield from GLOBAL_INTENT_EVENTS

def filter_clients(clients, flag_shift):
    """
    Filters the clients whether their intents allows the specific flag.
    
    First yields the first client from `clients` what allows the specified flag. If non, then yields `None`.
    If a `None` or not the expected client was yielded, then the generator should be closed.
    
    If the correct client was yielded, then the generator is used at a for loop yielding all the clients from `clients`
    which allow the specified flag including the firstly yielded one.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        The clients to filter.
    flag_shift : `int`
        The intent flag's shift based on what the clients will be filtered.
    
    yields
    -------
    client : ``Client`` or `None`
    """
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            yield None
            return
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            yield client
            break
        
        index=index+1
        continue
        
    yield client
    index=index+1
    
    while True:
        if index==limit:
            return
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            yield client
        
        index=index+1
        continue

def filter_clients_or_me(clients, flag_shift, me):
    """
    Filters the clients whether their intents allow the specific flag. This filter is used, when the clients receive
    the respective event for themselves even if they have the intent disabled.
    
    First yields the first client from `clients` what allows the specified flag.
    
    If non of the clients allow it, then yields `me` (so the source client), what received the event, then expects
    a `user` to be yielded back. At the end when the generator is iterated over inside of a for loop, then it yields
    `me` again (expect if `me` is not the same as the back yielded `user`, but that should not happen, but making sure).
    
    If any of the source clients allow the specified intent flag, then yields the first client what allows it.
    If not the correct client was yielded back, then the generator should be closed. Meanwhile if the correct client
    was yielded, then the generator expects a `user` to be yielded back. After it, the generator is used inside
    of a for loop yielding all the clients from `clients` which allow the specified intent flag including the firstly
    yielded one. At the end yields the received `user` if it is type ``Client`` and it's specified intent flag is not
    allowed.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        The clients to filter.
    flag_shift : `int`
        The intent flag's shift based on what the clients will be filtered.
    me : ``Client``
        The source client, what received the respective event.
    
    yields
    -------
    client : ``Client`` or `None`
    """
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            # If non of the clients have the intent, then yield `me`
            user = yield me
            yield
            if user is me:
                yield me
            return
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            user = yield client
            break
        
        index=index+1
        continue
    
    yield
    
    yield client
    index=index+1
    
    while True:
        if index==limit:
            break
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            yield client
        
        index=index+1
        continue
    
    # Whether the user is type Client and we did not yield it, yield it.
    if type(user) is User:
        return
    
    if (user.intents>>flag_shift)&1:
        return
    
    yield user

def first_client(clients, flag_shift):
    """
    Returns the first client what allows the specified intent flag. If no client allows it, then returns `None`.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    flag_shift : `int`
        The intent flag's shift based on what the clients will be filtered.
    
    Returns
    -------
    client : ``Client`` or `None`
    """
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            return None
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            return client
            break
        
        index=index+1
        continue

def first_client_or_me(clients, flag_shift, me):
    """
    Returns the first client what allows the specified intent flag. If non of the clients allow it, then returns `me`.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        A list of client to search from.
    flag_shift : `int`
        The intent flag's shift based on what the clients will be filtered.
    me : ``Client``
        The source client, what received the respective event.
    
    Returns
    -------
    client : ``Client``
    """
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            return me
        
        client=clients[index]
        if (client.intents>>flag_shift)&1:
            return client
            break
        
        index=index+1
        continue

PARSERS={}

class PARSER_DEFAULTS(object):
    """
    Stores the parsers for each dispatch events.
    
    Each dispatch event calls it coresponding parser, what can be 1 of up to 4 different parsers depending what is the
    optimal way of parsing that specific event. The called parser depends on the running client's intent values and
    whether they have a handler for the respective event. The parser are changed on change, so do not worry, there are
    no useless checks done every time a dispatch event is received.
    
    Attributes
    ----------
    name : `str`
        The parser's name also known as the dispatch event's.
    cal_sc : `function`
        Single client parser what calculates the differences between the previous and the current state and calls
        the client's event.
    cal_mc : `function`
        Multy client parser what calculates the differences between the previous and the current state and calls
        the clients' events.
    opt_sc : `function`
        Single client optimized parser.
    opt_mc : `function`
        Multy client optimized parsers.
    mention_count : `int`
        How much events of the running clients expect to be called by the respective parser. Used for `opt` - `cal`
        optimalizations.
    client_count : `int`
        How much running clients expect the respective parser to call their events. Used in `sc` - `mc` optimalization.
    
    Class Attributes
    ----------------
    all : `dict` of (`str`, `PARSER_DEFAULTS`) items
        A `dict` containing all the parser defaults in `parser name` - `parser default` relation
    registered : `WeakSet`
        A weakreference set of all the running clients, which' events are included in the parser optimalization
        process.
    """
    all={}
    registered=WeakSet()
    
    __slots__=('mention_count', 'client_count', 'cal_sc', 'name', 'opt_sc', 'cal_mc', 'opt_mc',)
    def __init__(self, name, cal_sc, cal_mc, opt_sc, opt_mc):
        """
        Creates a new parser defaults object with the given name and with the given parsers.
        
        The created parser defaults are stored at teh classe's `.all` attribute and also the default parser, so
        `opt_sc` is set to the global `PARSERS` variable.
        
        Parameters
        ----------
        name : `str`
            The parser's name also known as the dispatch event's.
        cal_sc : `function`
            Single client parser what calculates the differences between the previous and the current state and calls
            the client's event.
        cal_mc : `function`
            Multy client parser what calculates the differences between the previous and the current state and calls
            the clients' events.
        opt_sc : `function`
            Single client optimized parser.
        opt_mc : `function`
            Multy client optimized parsers.
        """
        self.name=name
        self.cal_sc=cal_sc
        self.cal_mc=cal_mc
        self.opt_sc=opt_sc
        self.opt_mc=opt_mc
        self.mention_count=0
        self.client_count=0
        self.all[name]=self
        PARSERS[name]=opt_sc
    
    @classmethod
    def register(cls, client):
        """
        Registers the given client as a running one. It means it's used events will be registered and their
        change will be handled to optimize the used parsers.
        
        Parameters
        ----------
        client : ``Client``
        """
        registered=cls.registered
        if client in registered:
            return
        
        registered.add(client)
        
        enabled_parsers=set()
        
        if client.is_bot:
            for parser_name in client.intents.iterate_parser_names():
                enabled_parsers.add(parser_name)
        else:
            for parser_name in cls.all.keys():
                enabled_parsers.add(parser_name)
        
        for parser_name in enabled_parsers:
            parser_default=cls.all[parser_name]
            parser_default.client_count+=1
            parser_default._recalculate()
        
        for event_name in EVENTS.parsers.keys():
            event = getattr(client.events,event_name)
            if event is DEFAULT_EVENT:
                continue
            
            parser_names = EVENTS.parsers[event_name]
            for parser_name in parser_names:
                if parser_name not in enabled_parsers:
                    continue
                
                parser_default=cls.all[parser_name]
                parser_default.mention_count+=1
                parser_default._recalculate()
            
    
    @classmethod
    def unregister(cls, client):
        """
        Unregisters the given client, so it's event be unregistered and their change will not be handled anymore to
        optimize the used parsers.
        
        Parameters
        ----------
        client : ``Client``
        """
        registered=cls.registered
        if client not in registered:
            return
        
        registered.remove(client)
        
        enabled_parsers=set()
        
        if client.is_bot:
            for parser_name in client.intents.iterate_parser_names():
                enabled_parsers.add(parser_name)
        else:
            for parser_name in cls.all.keys():
                enabled_parsers.add(parser_name)
        
        for parser_name in enabled_parsers:
            parser_default=cls.all[parser_name]
            parser_default.client_count-=1
            parser_default._recalculate()
        
        for event_name in EVENTS.parsers.keys():
            event = getattr(client.events,event_name)
            if event is DEFAULT_EVENT:
                continue
            
            parser_names = EVENTS.parsers[event_name]
            for parser_name in parser_names:
                if parser_name not in enabled_parsers:
                    continue
                
                parser_default=cls.all[parser_name]
                parser_default.mention_count-=1
                parser_default._recalculate()
                continue
    
    def add_mention(self, client):
        """
        If the client is already registered, mentions the respective parser defaults and optimizes the used parsers.
        
        Parameters
        ----------
        client : ``Client``
        """
        if client is None:
            return
        
        if client not in self.registered:
            return
        self.mention_count+=1
        self._recalculate()
    
    def remove_mention(self, client):
        """
        If the client is registered to the parser defaults, removes it's mention from the respective parser defaults
        and optimizes the used parsers.
        
        Parameters
        ----------
        client : ``Client``
        """
        if client is None:
            return
        
        if client not in self.registered:
            return
        self.mention_count-=1
        self._recalculate()
        
    def _recalculate(self):
        """
        Chooses the optimal parsers for each dispatch event.
        """
        mention_count=self.mention_count
        client_count=self.client_count
        
        if mention_count==0:
            if client_count<2:
                parser = self.opt_sc
            else:
                parser = self.opt_mc
        else:
            if client_count<2:
                parser = self.cal_sc
            else:
                parser = self.cal_mc
        
        PARSERS[self.name]=parser

SYNC_REQUESTS = {}

async def sync_task(queue_id, coro, queue):
    """
    Syncer task ensured if a guild related dispatch event fails, when any expected entity mentioned by it was not
    found.
    
    Parameters
    ----------
    queue_id : `int`
        The respective guild's id to identify queued up unhandled dispatch event when desync happened.
    coro : `coroutine`
        ``Client.guild_sync`` coroutine.
    queue : `list` of `tuple` (``Client``, `Any`, (`str` or `tuple` (`str`, `function`, `Any`)))
        A queue of parsers to call with the specified arguments.
        
        First element of the queue is always the respective client of the received dispatch event. The second is the
        payload of the dispatch event, meanwhile the third can be the name of it (parser name case), or a `tuple` of
        3 elements (checker case), where the first is the name of the parser, the second is a checker and the third is
        an additonal value to check with.
        
        At the parser name case, the parser will be called at every case, meanwhile at the checker case, the checker
        will be called with the synced guild and with the passed value, and then the parser will be called only, if the
        the checker returned `True`.
    """
    try:
        guild = await coro
    except (DiscordException, ConnectionError):
        return
    else:
        for client, data, parser_and_checker in queue:
            if type(parser_and_checker) is str:
                PARSERS[parser_and_checker](client,data)
                continue
            
            parser_name, checker, value = parser_and_checker
            if checker(guild,value):
                PARSERS[parser_name](client,data)
    finally:
        del SYNC_REQUESTS[queue_id]

def check_channel(guild, channel_id):
    """
    Checks whether the given guild has a channel with the specified id.
    
    This function is a checker used at guild syncing.
    
    Parameters
    ----------
    guild : ``Guild``
    channel_id : `int`
    """
    return (channel_id in guild.all_channel)

def guild_sync(client, data, parser_and_checker):
    """
    Syncer function what is called when any expected entity mentioned by a dispatch event's parser was not found.
    
    Looks up whether the given guild has already a syncer task, if it has not, then creates a new ``sync_task`` for it.
    If `parser_and_checker` is given as not `None`, then the respective failed parser will be called when the syncer
    finished.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the dispatch event.
    data : `Any`
        The payload of the dispatch event.
    parser_and_checker : `None` or `str` or `tuple` (`str`, `function`, `Any`)
        - Is passed as `None` if only the syncer task should run.
        - Is passed as `str`, if the respective parser should be called when syncing is done.
        - Is passed as `tuple` of 3 elements : `str`, `function`, `Any`; if the respective parser's calling is bound to
            a condition. The passed `function` should contain the condition and accept the respective guild and the
            third value (the type `Any` one) as arguments and return the condition's result.
    """
    try:
        guild_id=int(data['guild_id'])
    except KeyError:
        return
    
    try:
        queue=SYNC_REQUESTS[guild_id]
    except KeyError:
        queue=[]
        Task(sync_task(guild_id, client.guild_sync(guild_id), queue), KOKORO)
        SYNC_REQUESTS[guild_id]=queue
    
    if parser_and_checker is None:
        return
    queue.append((client,data,parser_and_checker),)

class EventBase(object):
    """
    Base class for events.
    """
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f'Create {cls.__name__} with `object.__new__(cls)` and asign variables from outside.')
    
    def __repr__(self):
        """Retrurns the event's representation."""
        return f'<{self.__class__.__name__}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 0
    
    def __iter__(self):
        """Unpacks the event."""
        return
        yield # This is intentional. Python stuff... Do not ask, just accept.

#we dont call ready from this function directly
def READY(client,data):
    ready_state=client.ready_state
    guild_datas=data['guilds']
    
    if ready_state is None:
        ready_state=ReadyState(client,guild_datas)
        client.ready_state=ready_state
        Task(client._delay_ready(), KOKORO)
    else:
        ready_state.shard_ready(data)
    
    client._init_on_ready(data['user'])
    
    # if the client is bot, we get only partial guilds,
    # and those disappear so there is not reason to create them
    if not client.is_bot:
        for guild_data in guild_datas:
            guild=Guild(guild_data,client)
            ready_state.feed(guild)
    
    try:
        relationship_datas=data['relationships']
    except KeyError:
        pass
    else:
        for relationship_data in relationship_datas:
            Relationship(client, relationship_data, int(relationship_data['id']))
    
    try:
        channel_private_datas=data['private_channels']
    except KeyError:
        pass
    else:
        for channel_private_data in channel_private_datas:
            CHANNEL_TYPES[channel_private_data['type']](channel_private_data,client)
    
    # ignore `'user_settings'`
    
    #"client.events.ready" gonna be called by _delay_ready at the end
    
    return _spaceholder

PARSER_DEFAULTS('READY',READY,READY,READY,READY)
del READY

def RESUMED(client,data):
    return _spaceholder

PARSER_DEFAULTS('RESUMED',RESUMED,RESUMED,RESUMED,RESUMED)
del RESUMED

def USER_UPDATE__CAL(client,data):
    old_attributes = client._update(data)
    if not old_attributes:
        return
    
    Task(client.events.client_edit(client,old_attributes), KOKORO)

def USER_UPDATE__OPT(client,data):
    client._update_no_return(data)

PARSER_DEFAULTS('USER_UPDATE',USER_UPDATE__CAL,USER_UPDATE__CAL,USER_UPDATE__OPT,USER_UPDATE__OPT)
del USER_UPDATE__CAL, USER_UPDATE__OPT

def MESSAGE_CREATE__CAL(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('MESSAGE_CREATE',check_channel,channel_id))
        return

    message = channel._create_new_message(data)
    
    Task(client.events.message_create(client,message), KOKORO)

def MESSAGE_CREATE__OPT(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('MESSAGE_CREATE',check_channel,channel_id))
        return
    
    channel._create_new_message(data)

PARSER_DEFAULTS('MESSAGE_CREATE',MESSAGE_CREATE__CAL,MESSAGE_CREATE__CAL,MESSAGE_CREATE__OPT,MESSAGE_CREATE__OPT)
del MESSAGE_CREATE__CAL, MESSAGE_CREATE__OPT

def MESSAGE_DELETE__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['id'])
    message=channel._pop_message(message_id)
    if message is None:
        return
    
    Task(client.events.message_delete(client,message), KOKORO)

def MESSAGE_DELETE__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_MESSAGES if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_MESSAGES)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_id=int(data['id'])
    message=channel._pop_message(message_id)
    if message is None:
        return
    
    for client_ in clients:
        Task(client_.events.message_delete(client_,message),KOKORO)
    
def MESSAGE_DELETE__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['id'])
    channel._pop_message(message_id)

def MESSAGE_DELETE__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_MESSAGES if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_MESSAGES) is not client:
        return
    
    message_id=int(data['id'])
    channel._pop_message(message_id)

PARSER_DEFAULTS('MESSAGE_DELETE',MESSAGE_DELETE__CAL_SC,MESSAGE_DELETE__CAL_MC,MESSAGE_DELETE__OPT_SC,MESSAGE_DELETE__OPT_MC)
del MESSAGE_DELETE__CAL_SC, MESSAGE_DELETE__CAL_MC, MESSAGE_DELETE__OPT_SC, MESSAGE_DELETE__OPT_MC

def MESSAGE_DELETE_BULK__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_ids=[int(message_id) for message_id in data['ids']]
    messages=channel._pop_multiple(message_ids)
    
    event = client.events.message_delete
    for message in messages:
        Task(client.events.message_delete(client, message), KOKORO)

def MESSAGE_DELETE_BULK__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_MESSAGES)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_ids=[int(message_id) for message_id in data['ids']]
    messages=channel._pop_multiple(message_ids)
    
    for client_ in clients:
        event = client_.events.message_delete
        if event is DEFAULT_EVENT:
            continue
        
        for message in messages:
            Task(event(client_, message), KOKORO)

def MESSAGE_DELETE_BULK__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return

    message_ids=[int(message_id) for message_id in data['ids']]
    channel._pop_multiple(message_ids)

def MESSAGE_DELETE_BULK__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return

    if first_client(channel.clients,INTENT_GUILD_MESSAGES) is not client:
        return

    message_ids=[int(message_id) for message_id in data['ids']]
    channel._pop_multiple(message_ids)

PARSER_DEFAULTS('MESSAGE_DELETE_BULK',MESSAGE_DELETE_BULK__CAL_SC,MESSAGE_DELETE_BULK__CAL_MC,MESSAGE_DELETE_BULK__OPT_SC,MESSAGE_DELETE_BULK__OPT_MC)
del MESSAGE_DELETE_BULK__CAL_SC, MESSAGE_DELETE_BULK__CAL_MC, MESSAGE_DELETE_BULK__OPT_SC, MESSAGE_DELETE_BULK__OPT_MC

def MESSAGE_UPDATE__CAL_SC(client,data):
    message_id=int(data['id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        old_attributes = message._update(data)
        if not old_attributes:
            return
        
        Task(client.events.message_edit(client,message,old_attributes), KOKORO)
    else:
        change_state = message._update_embed(data)
        if change_state == EMBED_UPDATE_NONE:
            return
        
        Task(client.events.embed_update(client, message, change_state), KOKORO)

def MESSAGE_UPDATE__CAL_MC(client,data):
    message_id=int(data['id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    clients=filter_clients(channel.clients,INTENT_GUILD_MESSAGES if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_MESSAGES)
    if clients.send(None) is not client:
        clients.close()
        return
    
    if 'edited_timestamp' in data:
        old_attributes = message._update(data)
        if not old_attributes:
            return
        
        for client_ in clients:
            Task(client_.events.message_edit(client_,message,old_attributes), KOKORO)
    else:
        result=message._update_embed(data)
        if not result:
            return
            
        for client_ in clients:
            Task(client_.events.embed_update(client_,message,result), KOKORO)

def MESSAGE_UPDATE__OPT_SC(client,data):
    message_id=int(data['id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        message._update_no_return(data)
    else:
        message._update_embed_no_return(data)

def MESSAGE_UPDATE__OPT_MC(client,data):
    message_id=int(data['id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    if first_client(channel.clients,INTENT_GUILD_MESSAGES if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_MESSAGES) is not client:
        return
    
    if 'edited_timestamp' in data:
        message._update_no_return(data)
    else:
        message._update_embed_no_return(data)


PARSER_DEFAULTS('MESSAGE_UPDATE',MESSAGE_UPDATE__CAL_SC,MESSAGE_UPDATE__CAL_MC,MESSAGE_UPDATE__OPT_SC,MESSAGE_UPDATE__OPT_MC)
del MESSAGE_UPDATE__CAL_SC, MESSAGE_UPDATE__CAL_MC, MESSAGE_UPDATE__OPT_SC, MESSAGE_UPDATE__OPT_MC

class ReactionAddEvent(EventBase):
    """
    Represents a processed `MESSAGE_REACTION_ADD` dispatch event.
    
    Attributes
    ----------
    message : ``Message``
        The message on what the reaction is added.
    emoji : ``Emoji``
        The emoji used as reaction.
    user : ``User`` or ``Client``
        The user who added the reaction.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message. Not applicable for
        ``ReactionAddEvent``.
    """
    __slots__ = ('message', 'emoji', 'user')
    
    def __repr__(self):
        """Returns the representation of the event."""
        return (f'<{self.__class__.__name__} message={self.message!r}, emoji={self.emoji!r}, '
            f'user={self.user.full_name!r}>')
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """Unpacks the event."""
        yield self.message
        yield self.emoji
        yield self.user
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identificator number of the action what will be executed.
            
            Can be one of the following:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DELETE_REACTION_OK    | 0     |
            +-----------------------+-------+
            | DELETE_REACTION_PERM  | 1     |
            +-----------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client).can_manage_messages:
            Task(_delete_reaction_with_task(self, client), KOKORO)
            result = self.DELETE_REACTION_OK
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
    
    DELETE_REACTION_OK = 0
    DELETE_REACTION_PERM = 1
    DELETE_REACTION_NOT_ADDED = 2
    
async def _delete_reaction_with_task(reaction_add_event, client):
    try:
        await client.reaction_delete(reaction_add_event.message, reaction_add_event.emoji, reaction_add_event.user)
    except BaseException as err:
        
        if isinstance(err, ConnectionError):
            # no internet
            return
        
        if isinstance(err, DiscordException):
            if err.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # channel deleted
                    ERROR_CODES.invalid_access, # client removed
                    ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                        ):
                return
        
        await client.events.error(client, f'_delete_reaction_with_task called from {reaction_add_event!r}', err)
        return

def MESSAGE_REACTION_ADD__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)
    
    event = object.__new__(ReactionAddEvent)
    event.message = message
    event.emoji = emoji
    event.user = user
    
    Task(client.events.reaction_add(client, event), KOKORO)

def MESSAGE_REACTION_ADD__CAL_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)
    
    event = object.__new__(ReactionAddEvent)
    event.message = message
    event.emoji = emoji
    event.user = user
    
    for client_ in clients:
        Task(client_.events.reaction_add(client_, event), KOKORO)

def MESSAGE_REACTION_ADD__OPT_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)

def MESSAGE_REACTION_ADD__OPT_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)

PARSER_DEFAULTS('MESSAGE_REACTION_ADD',MESSAGE_REACTION_ADD__CAL_SC,MESSAGE_REACTION_ADD__CAL_MC,MESSAGE_REACTION_ADD__OPT_SC,MESSAGE_REACTION_ADD__OPT_MC)
del MESSAGE_REACTION_ADD__CAL_SC, MESSAGE_REACTION_ADD__CAL_MC, MESSAGE_REACTION_ADD__OPT_SC, MESSAGE_REACTION_ADD__OPT_MC

def MESSAGE_REACTION_REMOVE_ALL__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    old_reactions=message.reactions
    if not old_reactions:
        return
    
    message.reactions=type(old_reactions)(None)
    
    Task(client.events.reaction_clear(client,message,old_reactions), KOKORO)

def MESSAGE_REACTION_REMOVE_ALL__CAL_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    old_reactions=message.reactions
    if not old_reactions:
        return
    
    message.reactions=type(old_reactions)(None)
    for client_ in clients:
        Task(client_.events.reaction_clear(client_,message,old_reactions),KOKORO)
    
def MESSAGE_REACTION_REMOVE_ALL__OPT_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return

    message.reactions=type(message.reactions)(None)

def MESSAGE_REACTION_REMOVE_ALL__OPT_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    message.reactions=type(message.reactions)(None)

PARSER_DEFAULTS('MESSAGE_REACTION_REMOVE_ALL',MESSAGE_REACTION_REMOVE_ALL__CAL_SC,MESSAGE_REACTION_REMOVE_ALL__CAL_MC,MESSAGE_REACTION_REMOVE_ALL__OPT_SC,MESSAGE_REACTION_REMOVE_ALL__OPT_MC)
del MESSAGE_REACTION_REMOVE_ALL__CAL_SC, MESSAGE_REACTION_REMOVE_ALL__CAL_MC, MESSAGE_REACTION_REMOVE_ALL__OPT_SC, MESSAGE_REACTION_REMOVE_ALL__OPT_MC


class ReactionDeleteEvent(ReactionAddEvent):
    """
    Represents a processed `MESSAGE_REACTION_REMOVE` dispatch event.
    
    Attributes
    ----------
    message : ``Message``
        The message from what the reaction was removed.
    emoji : ``Emoji``
        The removed emoji.
    user : ``User`` or ``Client``
        The user who's reaction was removed.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove. Not
        applicable on ``ReactionDeleteEvent``.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message.
    """
    __slots__ = ReactionAddEvent.__slots__
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction. Because the event is ``ReactionDeleteEvent``, it will not remvoe any reaction, but
        only check the permissions.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identificator number of the action what will be executed.
            
            Can be one of the following:
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | DELETE_REACTION_PERM      | 1     |
            +---------------------------+-------+
            | DELETE_REACTION_NOT_ADDED | 2     |
            +---------------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client).can_manage_messages:
            result = self.DELETE_REACTION_NOT_ADDED
        else:
            result = self.DELETE_REACTION_PERM
        
        return result

def MESSAGE_REACTION_REMOVE__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)
    
    event = object.__new__(ReactionDeleteEvent)
    event.message = message
    event.emoji = emoji
    event.user = user
    
    Task(client.events.reaction_delete(client,event), KOKORO)

def MESSAGE_REACTION_REMOVE__CAL_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)
    
    event = object.__new__(ReactionDeleteEvent)
    event.message = message
    event.emoji = emoji
    event.user = user
    
    for client_ in clients:
        Task(client_.events.reaction_delete(client_, event),KOKORO)

def MESSAGE_REACTION_REMOVE__OPT_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)

def MESSAGE_REACTION_REMOVE__OPT_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)

PARSER_DEFAULTS('MESSAGE_REACTION_REMOVE',MESSAGE_REACTION_REMOVE__CAL_SC,MESSAGE_REACTION_REMOVE__CAL_MC,MESSAGE_REACTION_REMOVE__OPT_SC,MESSAGE_REACTION_REMOVE__OPT_MC)
del MESSAGE_REACTION_REMOVE__CAL_SC, MESSAGE_REACTION_REMOVE__CAL_MC, MESSAGE_REACTION_REMOVE__OPT_SC, MESSAGE_REACTION_REMOVE__OPT_MC

def MESSAGE_REACTION_REMOVE_EMOJI__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    emoji=PartialEmoji(data['emoji'])
    users=message.reactions.remove_emoji(emoji)
    if users is None:
        return
    
    Task(client.events.reaction_delete_emoji(client,message,emoji,users), KOKORO)

def MESSAGE_REACTION_REMOVE_EMOJI__CAL_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    emoji=PartialEmoji(data['emoji'])
    users=message.reactions.remove_emoji(emoji)
    if users is None:
        return
    
    for client_ in clients:
        Task(client_.events.reaction_delete_emoji(client_,message,emoji,users),KOKORO)

def MESSAGE_REACTION_REMOVE_EMOJI__OPT_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove_emoji(emoji)

def MESSAGE_REACTION_REMOVE_EMOJI__OPT_MC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    channel = message.channel
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove_emoji(emoji)

PARSER_DEFAULTS('MESSAGE_REACTION_REMOVE_EMOJI',MESSAGE_REACTION_REMOVE_EMOJI__CAL_SC,MESSAGE_REACTION_REMOVE_EMOJI__CAL_MC,MESSAGE_REACTION_REMOVE_EMOJI__OPT_SC,MESSAGE_REACTION_REMOVE_EMOJI__OPT_MC)
del MESSAGE_REACTION_REMOVE_EMOJI__CAL_SC, MESSAGE_REACTION_REMOVE_EMOJI__CAL_MC, MESSAGE_REACTION_REMOVE_EMOJI__OPT_SC, MESSAGE_REACTION_REMOVE_EMOJI__OPT_MC


if CACHE_PRESENCE:
    def PRESENCE_UPDATE__CAL_SC(client,data):
        user_data=data['user']
        user_id=int(user_data.pop('id'))
        try:
            user=USERS[user_id]
        except KeyError:
            return #pretty much we dont care
        
        while True:
            if user_data:
                old_attributes = user._update(user_data)
                if old_attributes:
                    presence=False
                    break
            
            old_attributes = user._update_presence(data)
            if old_attributes:
                presence=True
                break
            
            return
        
        if presence:
            coro=client.events.user_presence_update
        else:
            coro=client.events.user_edit
        
        Task(coro(client,user,old_attributes), KOKORO)
    
    def PRESENCE_UPDATE__CAL_MC(client,data):
        user_data=data['user']
        user_id=int(user_data.pop('id'))
        try:
            user=USERS[user_id]
        except KeyError:
            return #pretty much we dont care 
        
        while True:
            if user_data:
                old_attributes=user._update(user_data)
                if old_attributes:
                    presence=False
                    break
            
            old_attributes=user._update_presence(data)
            if old_attributes:
                presence=True
                break
            
            return
        
        for client_ in CLIENTS:
            if (client_.intents>>INTENT_GUILD_PRESENCES)&1==0:
                continue
            
            if presence:
                coro=client_.events.user_presence_update
            else:
                coro=client_.events.user_edit
            
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client_,user,old_attributes),KOKORO)
            continue
    
    def PRESENCE_UPDATE__OPT(client,data):
        user_data=data['user']
        user_id=int(user_data.pop('id'))
        try:
            user=USERS[user_id]
        except KeyError:
            return #pretty much we dont care
        
        if user_data:
            user._update_no_return(user_data)
        
        user._update_presence_no_return(data)

else:
    def PRESENCE_UPDATE__CAL_SC(client,data):
        return
    PRESENCE_UPDATE__CAL_MC=PRESENCE_UPDATE__CAL_SC
    PRESENCE_UPDATE__OPT=PRESENCE_UPDATE__CAL_SC

PARSER_DEFAULTS('PRESENCE_UPDATE',PRESENCE_UPDATE__CAL_SC,PRESENCE_UPDATE__CAL_MC,PRESENCE_UPDATE__OPT,PRESENCE_UPDATE__OPT)
del PRESENCE_UPDATE__CAL_SC, PRESENCE_UPDATE__CAL_MC, PRESENCE_UPDATE__OPT

if CACHE_USER:
    def GUILD_MEMBER_UPDATE__CAL_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        user, old_attributes = User._update_profile(data,guild)
        
        if not old_attributes:
            return
        
        Task(client.events.user_profile_edit(client, user, guild, old_attributes), KOKORO)
    
    def GUILD_MEMBER_UPDATE__CAL_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        clients=filter_clients_or_me(guild.clients,INTENT_GUILD_USERS,client)
        if clients.send(None) is not client:
            clients.close()
            return
        
        user, old_attributes = User._update_profile(data,guild)
        
        if not old_attributes:
            return
        
        clients.send(user)
        for client_ in clients:
            Task(client_.events.user_profile_edit(client_, user, guild, old_attributes),KOKORO)
    
    def GUILD_MEMBER_UPDATE__OPT_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        User._update_profile_no_return(data,guild)

    def GUILD_MEMBER_UPDATE__OPT_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        if first_client_or_me(guild.clients,INTENT_GUILD_USERS,client) is not client:
            return
        
        User._update_profile_no_return(data,guild)

else:
    def GUILD_MEMBER_UPDATE__CAL_SC(client,data):
        user_id=int(data['user']['id'])
        if user_id!=client.id:
            return
        
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        old_attributes = client._update_profile_only(data,guild)
        
        if not old_attributes:
            return
        
        Task(client.events.user_profile_edit(client, client, guild, old_attributes), KOKORO)

    GUILD_MEMBER_UPDATE__CAL_MC=GUILD_MEMBER_UPDATE__CAL_SC

    def GUILD_MEMBER_UPDATE__OPT_SC(client,data):
        user_id=int(data['user']['id'])
        if user_id!=client.id:
            return
        
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        client._update_profile_only_no_return(data,guild)
    
    GUILD_MEMBER_UPDATE__OPT_MC=GUILD_MEMBER_UPDATE__OPT_SC

PARSER_DEFAULTS('GUILD_MEMBER_UPDATE',GUILD_MEMBER_UPDATE__CAL_SC,GUILD_MEMBER_UPDATE__CAL_MC,GUILD_MEMBER_UPDATE__OPT_SC,GUILD_MEMBER_UPDATE__OPT_MC)
del GUILD_MEMBER_UPDATE__CAL_SC, GUILD_MEMBER_UPDATE__CAL_MC, GUILD_MEMBER_UPDATE__OPT_SC, GUILD_MEMBER_UPDATE__OPT_MC

def CHANNEL_DELETE__CAL_SC(client, data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if isinstance(channel, ChannelGuildBase):
        guild = channel.guild
        if guild is None:
            return
        
        channel._delete()
    else:
        channel._delete(client)
        guild = None
    
    Task(client.events.channel_delete(client, channel, guild), KOKORO)

def CHANNEL_DELETE__CAL_MC(client, data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if isinstance(channel, ChannelGuildBase):
        guild = channel.guild
        if guild is None:
            return
        
        channel._delete()
        
        for client in guild.clients:
            if (client.intents>>INTENT_GUILDS)&1:
                Task(client.events.channel_delete(client, channel, guild), KOKORO)
    else:
        channel._delete(client)
        Task(client.events.channel_delete(client, channel, None), KOKORO)

def CHANNEL_DELETE__OPT(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if isinstance(channel, ChannelGuildBase):
        channel._delete()
    else:
        channel._delete(client)

PARSER_DEFAULTS('CHANNEL_DELETE',CHANNEL_DELETE__CAL_SC,CHANNEL_DELETE__CAL_MC,CHANNEL_DELETE__OPT,CHANNEL_DELETE__OPT)
del CHANNEL_DELETE__CAL_SC, CHANNEL_DELETE__CAL_MC, CHANNEL_DELETE__OPT

def CHANNEL_UPDATE__CAL_SC(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    old_attributes = channel._update(data)
    if not old_attributes:
        return
    
    Task(client.events.channel_edit(client,channel,old_attributes), KOKORO)

def CHANNEL_UPDATE__CAL_MC(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILDS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    old_attributes = channel._update(data)
    if not old_attributes:
        return
    
    for client_ in clients:
        Task(client_.events.channel_edit(client_,channel,old_attributes),KOKORO)

def CHANNEL_UPDATE__OPT_SC(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    channel._update_no_return(data)

def CHANNEL_UPDATE__OPT_MC(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILDS) is not client:
        return
    
    channel._update_no_return(data)

PARSER_DEFAULTS('CHANNEL_UPDATE',CHANNEL_UPDATE__CAL_SC,CHANNEL_UPDATE__CAL_MC,CHANNEL_UPDATE__OPT_SC,CHANNEL_UPDATE__OPT_MC)
del CHANNEL_UPDATE__CAL_SC, CHANNEL_UPDATE__CAL_MC, CHANNEL_UPDATE__OPT_SC, CHANNEL_UPDATE__OPT_MC

def CHANNEL_CREATE__CAL(client,data):
    channel_type=data['type']
    if channel_type in (1,3):
        channel=CHANNEL_TYPES[channel_type]._dispatch(data,client)
        if channel is None:
            return
    else:
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'CHANNEL_CREATE')
            return
        
        channel=CHANNEL_TYPES[channel_type](data,client,guild)
    
    Task(client.events.channel_create(client,channel), KOKORO)

def CHANNEL_CREATE__OPT(client,data):
    channel_type=data['type']
    if channel_type in (1,3):
        CHANNEL_TYPES[channel_type]._dispatch(data,client)
        return
    
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'CHANNEL_CREATE')
        return
    
    CHANNEL_TYPES[channel_type](data,client,guild)

PARSER_DEFAULTS('CHANNEL_CREATE',CHANNEL_CREATE__CAL,CHANNEL_CREATE__CAL,CHANNEL_CREATE__OPT,CHANNEL_CREATE__OPT)
del CHANNEL_CREATE__CAL, CHANNEL_CREATE__OPT

def CHANNEL_PINS_UPDATE__CAL(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('CHANNEL_PINS_UPDATE',check_channel,channel_id))
        return
    
    #ignoring message search
    Task(client.events.channel_pin_update(client,channel), KOKORO)

def CHANNEL_PINS_UPDATE__OPT(client,data):
    pass

PARSER_DEFAULTS('CHANNEL_PINS_UPDATE',CHANNEL_PINS_UPDATE__CAL,CHANNEL_PINS_UPDATE__CAL,CHANNEL_PINS_UPDATE__OPT,CHANNEL_PINS_UPDATE__OPT)
del CHANNEL_PINS_UPDATE__CAL, CHANNEL_PINS_UPDATE__OPT

def CHANNEL_RECIPIENT_ADD_CAL(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        return
    
    user=User(data['user'])
    users=channel.users
    if user not in users:
        users.append(user)
    
    Task(client.events.channel_group_user_add(client,channel,user), KOKORO)

def CHANNEL_RECIPIENT_ADD__OPT(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        return
    
    user=User(data['user'])
    users=channel.users
    if user not in users:
        users.append(user)

PARSER_DEFAULTS('CHANNEL_RECIPIENT_ADD',CHANNEL_RECIPIENT_ADD_CAL,CHANNEL_RECIPIENT_ADD_CAL,CHANNEL_RECIPIENT_ADD__OPT,CHANNEL_RECIPIENT_ADD__OPT)
del CHANNEL_RECIPIENT_ADD_CAL, CHANNEL_RECIPIENT_ADD__OPT

def CHANNEL_RECIPIENT_REMOVE__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        return
    
    user=User(data['user'])
    try:
        channel.users.remove(user)
    except ValueError:
        return
    
    if client!=user:
        Task(client.events.channel_group_user_delete(client,channel,user), KOKORO)

def CHANNEL_RECIPIENT_REMOVE__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        return
    
    user=User(data['user'])
    try:
        channel.users.remove(user)
    except ValueError:
        return
    
    for client_ in channel.clients:
        if (client_ is client) or (client_!=user):
            Task(client_.events.channel_group_user_delete(client_,channel,user),KOKORO)

def CHANNEL_RECIPIENT_REMOVE__OPT(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        return

    user=User(data['user'])
    try:
        channel.users.remove(user)
    except ValueError:
        pass

PARSER_DEFAULTS('CHANNEL_RECIPIENT_REMOVE',CHANNEL_RECIPIENT_REMOVE__CAL_SC,CHANNEL_RECIPIENT_REMOVE__CAL_MC,CHANNEL_RECIPIENT_REMOVE__OPT,CHANNEL_RECIPIENT_REMOVE__OPT)
del CHANNEL_RECIPIENT_REMOVE__CAL_SC, CHANNEL_RECIPIENT_REMOVE__CAL_MC, CHANNEL_RECIPIENT_REMOVE__OPT

def GUILD_EMOJIS_UPDATE__CAL_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return

    changes=guild._update_emojis(data['emojis'])
    
    if not changes:
        return
    
    for action, emoji, old_attributes in changes:
        if action==EMOJI_UPDATE_EDIT:
            coro=client.events.emoji_edit
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,emoji,old_attributes), KOKORO)
            continue
            
        if action==EMOJI_UPDATE_NEW:
            coro=client.events.emoji_create
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,emoji), KOKORO)
            continue
        
        if action==EMOJI_UPDATE_DELETE:
            coro=client.events.emoji_delete
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,emoji,guild), KOKORO)
            continue
        
        # no more case

def GUILD_EMOJIS_UPDATE__CAL_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILD_EMOJIS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    changes=guild._update_emojis(data['emojis'])
    
    if not changes:
        return
    
    for client_ in clients:
        for action, emoji, old_attributes in changes:
            if action==EMOJI_UPDATE_EDIT:
                coro=client_.events.emoji_edit
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji,old_attributes),KOKORO)
                continue
                
            if action==EMOJI_UPDATE_NEW:
                coro=client_.events.emoji_create
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji),KOKORO)
                continue
            
            if action==EMOJI_UPDATE_DELETE:
                coro=client_.events.emoji_delete
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji),KOKORO)
                continue
            
            continue
            # no more case

def GUILD_EMOJIS_UPDATE__OPT_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    guild._sync_emojis(data['emojis'])

def GUILD_EMOJIS_UPDATE__OPT_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(guild.clients,INTENT_GUILD_EMOJIS) is not client:
        return
    
    guild._sync_emojis(data['emojis'])

PARSER_DEFAULTS('GUILD_EMOJIS_UPDATE',GUILD_EMOJIS_UPDATE__CAL_SC,GUILD_EMOJIS_UPDATE__CAL_MC,GUILD_EMOJIS_UPDATE__OPT_SC,GUILD_EMOJIS_UPDATE__OPT_MC)
del GUILD_EMOJIS_UPDATE__CAL_SC, GUILD_EMOJIS_UPDATE__CAL_MC, GUILD_EMOJIS_UPDATE__OPT_SC, GUILD_EMOJIS_UPDATE__OPT_MC

def GUILD_MEMBER_ADD__CAL_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    user=User(data,guild)
    guild.user_count+=1
    
    Task(client.events.guild_user_add(client,guild,user), KOKORO)

def GUILD_MEMBER_ADD__CAL_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILD_USERS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    user=User(data,guild)
    guild.user_count+=1
    
    for client_ in clients:
        Task(client_.events.guild_user_add(client_,guild,user),KOKORO)

if CACHE_USER:
    def GUILD_MEMBER_ADD__OPT_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,None)
            return
        
        User(data,guild)
        guild.user_count+=1

    def GUILD_MEMBER_ADD__OPT_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,None)
            return

        if first_client(guild.clients,INTENT_GUILD_USERS) is not client:
            return

        User(data,guild)
        guild.user_count+=1
else:
    def GUILD_MEMBER_ADD__OPT_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,None)
            return
        
        guild.user_count+=1

    def GUILD_MEMBER_ADD__OPT_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,None)
            return
        
        if first_client(guild.clients,INTENT_GUILD_USERS) is not client:
            return
        
        guild.user_count+=1

PARSER_DEFAULTS('GUILD_MEMBER_ADD',GUILD_MEMBER_ADD__CAL_SC,GUILD_MEMBER_ADD__CAL_MC,GUILD_MEMBER_ADD__OPT_SC,GUILD_MEMBER_ADD__OPT_MC)
del GUILD_MEMBER_ADD__CAL_SC, GUILD_MEMBER_ADD__CAL_MC, GUILD_MEMBER_ADD__OPT_SC, GUILD_MEMBER_ADD__OPT_MC

if CACHE_USER:
    def GUILD_MEMBER_REMOVE__CAL_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        user=User(data['user'])
        
        try:
            del guild.users[user.id]
        except KeyError:
            profile=None
        else:
            if type(user) is User:
                profile=user.guild_profiles.pop(guild,None)
            else:
                profile=user.guild_profiles.get(guild,None)
        
        guild.user_count-=1
        
        Task(client.events.guild_user_delete(client,guild,user,profile), KOKORO)

    def GUILD_MEMBER_REMOVE__CAL_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        clients=filter_clients(guild.clients,INTENT_GUILD_USERS)
        if clients.send(None) is not client:
            clients.close()
            return
        
        user=User(data['user'])
        
        try:
            del guild.users[user.id]
        except KeyError:
            profile=None
        else:
            if type(user) is User:
                profile=user.guild_profiles.pop(guild,None)
            else:
                profile=user.guild_profiles.get(guild,None)
        
        guild.user_count-=1
        
        for client_ in clients:
            Task(client_.events.guild_user_delete(client_,guild,user,profile),KOKORO)
    
    def GUILD_MEMBER_REMOVE__OPT_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        user=User(data['user'])
        
        try:
            del guild.users[user.id]
        except KeyError:
            pass
        else:
            if type(user) is User:
                user.guild_profiles.pop(guild,None)
        
        guild.user_count-=1
    
    def GUILD_MEMBER_REMOVE__OPT_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        if first_client(guild.clients,INTENT_GUILD_USERS) is not client:
            return
        
        user=User(data['user'])
        
        try:
            del guild.users[user.id]
        except KeyError:
            pass
        else:
            if type(user) is User:
                user.guild_profiles.pop(guild,None)
        
        guild.user_count-=1

else:
    def GUILD_MEMBER_REMOVE__CAL_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        user=User(data['user'])
        guild.user_count-=1
        
        Task(client.events.guild_user_delete(client,guild,user,None), KOKORO)

    def GUILD_MEMBER_REMOVE__CAL_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        clients=filter_clients(guild.clients,INTENT_GUILD_USERS)
        if clients.send(None) is not client:
            clients.close()
            return
        
        user=User(data['user'])
        guild.user_count-=1
        
        for client_ in clients:
            Task(client_.events.guild_user_delete(client_,guild,user,None),KOKORO)
    
    def GUILD_MEMBER_REMOVE__OPT_SC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        guild.user_count-=1
    
    def GUILD_MEMBER_REMOVE__OPT_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_REMOVE')
            return
        
        if first_client(guild.clients,INTENT_GUILD_USERS) is not client:
            return
        
        guild.user_count-=1

PARSER_DEFAULTS('GUILD_MEMBER_REMOVE',GUILD_MEMBER_REMOVE__CAL_SC,GUILD_MEMBER_REMOVE__CAL_MC,GUILD_MEMBER_REMOVE__OPT_SC,GUILD_MEMBER_REMOVE__OPT_MC)
del GUILD_MEMBER_REMOVE__CAL_SC, GUILD_MEMBER_REMOVE__CAL_MC, GUILD_MEMBER_REMOVE__OPT_SC, GUILD_MEMBER_REMOVE__OPT_MC

if CACHE_PRESENCE:
    def GUILD_CREATE__CAL(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            if guild.is_large:
                Task(client._request_members(guild), KOKORO)
            Task(client.events.guild_create(client,guild), KOKORO)
            return
        
        ready_state.feed(guild)

    def GUILD_CREATE__OPT(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            if guild.is_large:
                Task(client._request_members(guild), KOKORO)
            return
        
        ready_state.feed(guild)

elif CACHE_USER:
    def GUILD_CREATE__CAL(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            Task(client._request_members(guild), KOKORO)
            Task(client.events.guild_create(client,guild), KOKORO)
            return
        
        ready_state.feed(guild)

    def GUILD_CREATE__OPT(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            Task(client._request_members(guild), KOKORO)
            return
        
        ready_state.feed(guild)

else:
    def GUILD_CREATE__CAL(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            Task(client.events.guild_create(client,guild), KOKORO)
            return
        
        ready_state.feed(guild)
    
    def GUILD_CREATE__OPT(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            return
        
        ready_state.feed(guild)

PARSER_DEFAULTS('GUILD_CREATE',GUILD_CREATE__CAL,GUILD_CREATE__CAL,GUILD_CREATE__OPT,GUILD_CREATE__OPT)
del GUILD_CREATE__CAL, GUILD_CREATE__OPT

def GUILD_UPDATE__CAL_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    old_attributes = guild._update(data)
    if not old_attributes:
        return
    
    Task(client.events.guild_edit(client,guild,old_attributes), KOKORO)

def GUILD_UPDATE__CAL_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILDS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    old_attributes = guild._update(data)
    if not old_attributes:
        return
    
    for client_ in clients:
        Task(client_.events.guild_edit(client_,guild,old_attributes),KOKORO)

def GUILD_UPDATE__OPT_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    guild._update_no_return(data)

def GUILD_UPDATE__OPT_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(guild.clients,INTENT_GUILDS) is not client:
        return
    
    guild._update_no_return(data)

PARSER_DEFAULTS('GUILD_UPDATE',GUILD_UPDATE__CAL_SC,GUILD_UPDATE__CAL_MC,GUILD_UPDATE__OPT_SC,GUILD_UPDATE__OPT_MC)
del GUILD_UPDATE__CAL_SC, GUILD_UPDATE__CAL_MC, GUILD_UPDATE__OPT_SC, GUILD_UPDATE__OPT_MC

def GUILD_DELETE__CAL(client,data):
    guild_id=int(data['id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        return
    
    if data.get('unavailable',2)==1:
        return
    
    profile=client.guild_profiles.pop(guild,None)
    
    guild._delete(client)
    
    Task(client.events.guild_delete(client,guild,profile), KOKORO)

def GUILD_DELETE__OPT(client,data):
    guild_id=int(data['id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        return
    
    if data.get('unavailable',2)==1:
        return
    
    client.guild_profiles.pop(guild,None)
    
    guild._delete(client)

PARSER_DEFAULTS('GUILD_DELETE',GUILD_DELETE__CAL,GUILD_DELETE__CAL,GUILD_DELETE__OPT,GUILD_DELETE__OPT)
del GUILD_DELETE__CAL, GUILD_DELETE__OPT

def GUILD_BAN_ADD__CAL(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_BAN_ADD')
        return
    
    user=User(data['user'])
    
    Task(client.events.guild_ban_add(client,guild,user), KOKORO)

def GUILD_BAN_ADD__OPT(client,data):
    pass

PARSER_DEFAULTS('GUILD_BAN_ADD',GUILD_BAN_ADD__CAL,GUILD_BAN_ADD__CAL,GUILD_BAN_ADD__OPT,GUILD_BAN_ADD__OPT)
del GUILD_BAN_ADD__CAL, GUILD_BAN_ADD__OPT

def GUILD_BAN_REMOVE__CAL(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_BAN_REMOVE')
        return
    
    user=User(data['user'])
    Task(client.events.guild_ban_delete(client,guild,user), KOKORO)

def GUILD_BAN_REMOVE__OPT(client,data):
    pass

PARSER_DEFAULTS('GUILD_BAN_REMOVE',GUILD_BAN_REMOVE__CAL,GUILD_BAN_REMOVE__CAL,GUILD_BAN_REMOVE__OPT,GUILD_BAN_REMOVE__OPT)
del GUILD_BAN_REMOVE__CAL, GUILD_BAN_REMOVE__OPT

class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    guild : ``Guild``
        The guild what received the user chunk.
    users : `list` of (``User`` or ``Client``)
        The received users.
    nonce : `None` or `str`
        A nonce to identify guild user chunk response.
    index : `int`
        The index of the received chunk response (0 <= index < count).
    count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    """
    __slots__ = ('guild', 'users', 'nonce', 'index', 'count')
    
    def __repr__(self):
        """Returns the representation of the guild user chunk event."""
        return f'<{self.__class__.__name__} guild={self.guild}, users={len(self.users)}, nonce={self.nonce!r}, index={self.index}, count={self.count}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 5
    
    def __iter__(self):
        """Unpacks the guild user chunk event."""
        yield self.guild
        yield self.users
        yield self.nonce
        yield self.index
        yield self.count

if CACHE_PRESENCE:
    def GUILD_MEMBERS_CHUNK(client, data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            return
        
        users=[]
        for user_data in data['members']:
            user = User(user_data,guild)
            users.append(user)
        
        try:
            presence_datas=data['presences']
        except KeyError:
            pass
        else:
            guild._apply_presences(presence_datas)
        
        event = object.__new__(GuildUserChunkEvent)
        event.guild = guild
        event.users = users
        event.nonce = data.get('nonce')
        event.index = data['chunk_index']
        event.count = data['chunk_count']
        
        Task(client.events.guild_user_chunk(client, event), KOKORO)
else:
    def GUILD_MEMBERS_CHUNK(client, data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            return
        
        users = []
        for user_data in data['members']:
            user = User(user_data,guild)
            users.append(user)
        
        event = object.__new__(GuildUserChunkEvent)
        event.guild = guild
        event.users = users
        event.nonce = data.get('nonce')
        event.index = data['chunk_index']
        event.count = data['chunk_count']
        
        Task(client.events.guild_user_chunk(client,event), KOKORO)

PARSER_DEFAULTS('GUILD_MEMBERS_CHUNK',GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK)
del GUILD_MEMBERS_CHUNK

def GUILD_INTEGRATIONS_UPDATE__CAL(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_INTEGRATIONS_UPDATE')
        return
    
    Task(client.events.integration_update(client,guild), KOKORO)

def GUILD_INTEGRATIONS_UPDATE__OPT(client,data):
    pass

PARSER_DEFAULTS('GUILD_INTEGRATIONS_UPDATE',GUILD_INTEGRATIONS_UPDATE__CAL,GUILD_INTEGRATIONS_UPDATE__CAL,GUILD_INTEGRATIONS_UPDATE__OPT,GUILD_INTEGRATIONS_UPDATE__OPT)
del GUILD_INTEGRATIONS_UPDATE__CAL, GUILD_INTEGRATIONS_UPDATE__OPT

def GUILD_ROLE_CREATE__CAL_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_ROLE_CREATE')
        return
    
    role=Role(data['role'],guild)
    
    Task(client.events.role_create(client,role), KOKORO)

def GUILD_ROLE_CREATE__CAL_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_ROLE_CREATE')
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILDS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    role=Role(data['role'],guild)
    
    for client_ in clients:
        Task(client_.events.role_create(client_,role),KOKORO)

def GUILD_ROLE_CREATE__OPT_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_ROLE_CREATE')
        return
    
    Role(data['role'],guild)

def GUILD_ROLE_CREATE__OPT_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_ROLE_CREATE')
        return
    
    if first_client(guild.clients,INTENT_GUILDS) is not client:
        return
    
    Role(data['role'],guild)

PARSER_DEFAULTS('GUILD_ROLE_CREATE',GUILD_ROLE_CREATE__CAL_SC,GUILD_ROLE_CREATE__CAL_MC,GUILD_ROLE_CREATE__OPT_SC,GUILD_ROLE_CREATE__OPT_MC)
del GUILD_ROLE_CREATE__CAL_SC, GUILD_ROLE_CREATE__CAL_MC, GUILD_ROLE_CREATE__OPT_SC, GUILD_ROLE_CREATE__OPT_MC

def GUILD_ROLE_DELETE__CAL_SC(client, data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role_id=int(data['role_id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._delete()
    
    Task(client.events.role_delete(client,role,guild), KOKORO)

def GUILD_ROLE_DELETE__CAL_MC(client, data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILDS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    role_id=int(data['role_id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._delete()
    
    for client_ in clients:
        Task(client_.events.role_delete(client_,role, guild),KOKORO)

def GUILD_ROLE_DELETE__OPT_SC(client, data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role_id=int(data['role_id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._delete()

def GUILD_ROLE_DELETE__OPT_MC(client, data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(guild.clients,INTENT_GUILDS) is not client:
        return
    
    role_id=int(data['role_id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._delete()

PARSER_DEFAULTS('GUILD_ROLE_DELETE',GUILD_ROLE_DELETE__CAL_SC,GUILD_ROLE_DELETE__CAL_MC,GUILD_ROLE_DELETE__OPT_SC,GUILD_ROLE_DELETE__OPT_MC)
del GUILD_ROLE_DELETE__CAL_SC, GUILD_ROLE_DELETE__CAL_MC, GUILD_ROLE_DELETE__OPT_SC, GUILD_ROLE_DELETE__OPT_MC

def GUILD_ROLE_UPDATE__CAL_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role_data=data['role']
    role_id=int(role_data['id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    old_attributes = role._update(data['role'])
    if not old_attributes:
        return
    
    Task(client.events.role_edit(client,role,old_attributes), KOKORO)

def GUILD_ROLE_UPDATE__CAL_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(guild.clients,INTENT_GUILDS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    role_data=data['role']
    role_id=int(role_data['id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    old_attributes=role._update(data['role'])
    if not old_attributes:
        return
    
    for client_ in clients:
        Task(client_.events.role_edit(client_,role,old_attributes),KOKORO)

def GUILD_ROLE_UPDATE__OPT_SC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role_data=data['role']
    role_id=int(role_data['id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._update_no_return(data['role'])

def GUILD_ROLE_UPDATE__OPT_MC(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(guild.clients,INTENT_GUILDS) is not client:
        return
    
    role_data=data['role']
    role_id=int(role_data['id'])
    try:
        role=guild.all_role[role_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    role._update_no_return(data['role'])

PARSER_DEFAULTS('GUILD_ROLE_UPDATE',GUILD_ROLE_UPDATE__CAL_SC,GUILD_ROLE_UPDATE__CAL_MC,GUILD_ROLE_UPDATE__OPT_SC,GUILD_ROLE_UPDATE__OPT_MC)
del GUILD_ROLE_UPDATE__CAL_SC, GUILD_ROLE_UPDATE__CAL_MC, GUILD_ROLE_UPDATE__OPT_SC, GUILD_ROLE_UPDATE__OPT_MC

def WEBHOOKS_UPDATE__CAL(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'WEBHOOKS_UPDATE')
        return
    
    guild.webhooks_uptodate=False
    
    channel_id=int(data['channel_id'])
    channel=guild.all_channel.get(channel_id,None)
    
    #if this happens the client might ask for update.
    Task(client.events.webhook_update(client,channel,), KOKORO)

def WEBHOOKS_UPDATE__OPT(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'WEBHOOKS_UPDATE')
        return
    
    guild.webhooks_uptodate=False

PARSER_DEFAULTS('WEBHOOKS_UPDATE',WEBHOOKS_UPDATE__CAL,WEBHOOKS_UPDATE__CAL,WEBHOOKS_UPDATE__OPT,WEBHOOKS_UPDATE__OPT)
del WEBHOOKS_UPDATE__CAL, WEBHOOKS_UPDATE__OPT

def VOICE_STATE_UPDATE__CAL_SC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        # Do not handle outside of guild calls
        return
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=guild._update_voice_state(data,user)
    
    if result is None:
        return
    
    #need to comapre id, because if caching is disabled,
    #the objects will be different.
    if user==client:
        try:
            voice_client=client.voice_clients[id_]
        except KeyError:
            pass
        else:
            if result[1]=='l':
                Task(voice_client.disconnect(force=True,terminate=False), KOKORO)
            else:
                voice_client.channel=result[0].channel
    
    Task(client.events.voice_state_update(client,*result), KOKORO)

def VOICE_STATE_UPDATE__CAL_MC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        # Do not handle outside of guild calls
        return
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
    
    clients=filter_clients(guild.clients,INTENT_GUILD_VOICE_STATES)
    if clients.send(None) is not client:
        clients.close()
        return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=guild._update_voice_state(data,user)
    
    if result is None:
        return
    
    for client_ in clients:
        #need to comapre id, because if caching is disabled,
        #the objects will be different.
        if user==client_:
            try:
                voice_client=client_.voice_clients[id_]
            except KeyError:
                pass
            else:
                if result[1]=='l':
                    Task(voice_client.disconnect(force=True,terminate=False),KOKORO)
                else:
                    voice_client.channel=result[0].channel
        
        Task(client_.events.voice_state_update(client_,*result),KOKORO)

def VOICE_STATE_UPDATE__OPT_SC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        # Do not handle outside of guild calls
        return
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    
    result=guild._update_voice_state_restricted(data,user)
    
    if result is None:
        return
    
    #need to comapre id, because if caching is disabled,
    #the objects will be different.
    if user!=client:
        return
    
    try:
        voice_client=client.voice_clients[id_]
    except KeyError:
        return
    
    if result is _spaceholder:
        Task(voice_client.disconnect(force=True,terminate=False), KOKORO)
    else:
        voice_client.channel=result

def VOICE_STATE_UPDATE__OPT_MC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        # Do not handle outside of guild calls
        return
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
    
    if first_client(guild.clients,INTENT_GUILD_VOICE_STATES) is not client:
        return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=guild._update_voice_state_restricted(data,user)
    
    if result is None:
        return
    
    for client in guild.clients:
        #need to comapre id, because if caching is disabled,
        #the objects will be different.
        if user==client:
            break
    else:
        return
    
    try:
        voice_client=client.voice_clients[id_]
    except KeyError:
        return
    
    if result is _spaceholder:
        Task(voice_client.disconnect(force=True,terminate=False), KOKORO)
    else:
        voice_client.channel=result

PARSER_DEFAULTS('VOICE_STATE_UPDATE',VOICE_STATE_UPDATE__CAL_SC,VOICE_STATE_UPDATE__CAL_MC,VOICE_STATE_UPDATE__OPT_SC,VOICE_STATE_UPDATE__OPT_MC)
del VOICE_STATE_UPDATE__CAL_SC, VOICE_STATE_UPDATE__CAL_MC, VOICE_STATE_UPDATE__OPT_SC, VOICE_STATE_UPDATE__OPT_MC

def VOICE_SERVER_UPDATE(client,data):
    try:
        voice_client_id=int(data['guild_id'])
    except KeyError:
        voice_client_id=int(data['channel_id'])
    try:
        voice_client=client.voice_clients[voice_client_id]
    except KeyError:
        return
    
    Task(voice_client._create_socket(data), KOKORO)
    #should we add event to this?

PARSER_DEFAULTS('VOICE_SERVER_UPDATE',VOICE_SERVER_UPDATE,VOICE_SERVER_UPDATE,VOICE_SERVER_UPDATE,VOICE_SERVER_UPDATE)
del VOICE_SERVER_UPDATE

if CACHE_PRESENCE:
    def TYPING_START__CAL(client,data):
        channel_id=int(data['channel_id'])
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            guild_sync(client,data,('TYPING_START',check_channel,channel_id))
            return
        
        user_id=int(data['user_id'])
        user=PartialUser(user_id)
        
        timestamp=utcfromtimestamp(data.get('timestamp'))
        
        Task(client.events.typing(client,channel,user,timestamp), KOKORO)
    
    def TYPING_START__OPT(client,data):
        return
else:
    def TYPING_START__CAL(client,data):
        return
    TYPING_START__OPT=TYPING_START__CAL

PARSER_DEFAULTS('TYPING_START',TYPING_START__CAL,TYPING_START__CAL,TYPING_START__OPT,TYPING_START__OPT)
del TYPING_START__CAL, TYPING_START__OPT

def INVITE_CREATE__CAL(client,data):
    invite = Invite(data)
    Task(client.events.invite_create(client,invite), KOKORO)

def INVITE_CREATE__OPT(client,data):
    pass

PARSER_DEFAULTS('INVITE_CREATE',INVITE_CREATE__CAL,INVITE_CREATE__CAL,INVITE_CREATE__OPT,INVITE_CREATE__OPT)
del INVITE_CREATE__CAL, INVITE_CREATE__OPT

def INVITE_DELETE__CAL(client,data):
    invite = Invite(data)
    Task(client.events.invite_delete(client,invite), KOKORO)

def INVITE_DELETE__OPT(client,data):
    pass

PARSER_DEFAULTS('INVITE_DELETE',INVITE_DELETE__CAL,INVITE_DELETE__CAL,INVITE_DELETE__OPT,INVITE_DELETE__OPT)
del INVITE_DELETE__CAL, INVITE_DELETE__OPT

def RELATIONSHIP_ADD__CAL(client,data):
    user_id=int(data['id'])
    try:
        old_relationship=client.relationships.pop(user_id)
    except KeyError:
        old_relationship=None
    
    new_relationship=Relationship(client, data, user_id)
    
    if old_relationship is None:
        coro=client.events.relationship_add(client,new_relationship)
    else:
        coro=client.events.relationship_change(client,old_relationship,new_relationship)
    Task(coro, KOKORO)

def RELATIONSHIP_ADD__OPT(client,data):
    user_id=int(data['id'])
    try:
        del client.relationships[user_id]
    except KeyError:
        pass
    
    Relationship(client, data, user_id)

PARSER_DEFAULTS('RELATIONSHIP_ADD',RELATIONSHIP_ADD__CAL,RELATIONSHIP_ADD__CAL,RELATIONSHIP_ADD__OPT,RELATIONSHIP_ADD__OPT)
del RELATIONSHIP_ADD__CAL, RELATIONSHIP_ADD__OPT

def RELATIONSHIP_REMOVE__CAL(client,data):
    user_id=int(data['id'])
    try:
        old_relationship = client.relationships.pop(user_id)
    except KeyError:
        return
    
    Task(client.events.relationship_delete(client,old_relationship), KOKORO)

def RELATIONSHIP_REMOVE__OPT(client,data):
    user_id=int(data['id'])
    try:
        del client.user.relations[user_id]
    except KeyError:
        pass

PARSER_DEFAULTS('RELATIONSHIP_REMOVE',RELATIONSHIP_REMOVE__CAL,RELATIONSHIP_REMOVE__CAL,RELATIONSHIP_REMOVE__OPT,RELATIONSHIP_REMOVE__OPT)
del RELATIONSHIP_REMOVE__CAL, RELATIONSHIP_REMOVE__OPT

#empty list
def PRESENCES_REPLACE(client,data):
    pass

PARSER_DEFAULTS('PRESENCES_REPLACE',PRESENCES_REPLACE,PRESENCES_REPLACE,PRESENCES_REPLACE,PRESENCES_REPLACE)
del PRESENCES_REPLACE

def USER_SETTINGS_UPDATE(client,data):
    pass

PARSER_DEFAULTS('USER_SETTINGS_UPDATE',USER_SETTINGS_UPDATE, USER_SETTINGS_UPDATE, USER_SETTINGS_UPDATE, USER_SETTINGS_UPDATE)
del USER_SETTINGS_UPDATE

def GIFT_CODE_UPDATE__CAL(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('GIFT_CODE_UPDATE',check_channel,channel_id))
        return
    
    gift=Gift(data)
    Task(client.events.gift_update(client,channel,gift), KOKORO)

def GIFT_CODE_UPDATE__OPT(client,data):
    pass

PARSER_DEFAULTS('GIFT_CODE_UPDATE',GIFT_CODE_UPDATE__CAL,GIFT_CODE_UPDATE__CAL,GIFT_CODE_UPDATE__OPT,GIFT_CODE_UPDATE__OPT)
del GIFT_CODE_UPDATE__CAL, GIFT_CODE_UPDATE__OPT

#hooman only event
def USER_ACHIEVEMENT_UPDATE(client, data):
    pass

PARSER_DEFAULTS('USER_ACHIEVEMENT_UPDATE', USER_ACHIEVEMENT_UPDATE, USER_ACHIEVEMENT_UPDATE, USER_ACHIEVEMENT_UPDATE, USER_ACHIEVEMENT_UPDATE)
del USER_ACHIEVEMENT_UPDATE

#hooman only event
def MESSAGE_ACK(client,data):
    # contains `message_id` and `channel_id`, no clue, how it could be usefull.
    pass

PARSER_DEFAULTS('MESSAGE_ACK',MESSAGE_ACK,MESSAGE_ACK,MESSAGE_ACK,MESSAGE_ACK)
del MESSAGE_ACK

#hooman only event, with the own presence data, what we get anyways.
def SESSIONS_REPLACE(client,data):
    pass

PARSER_DEFAULTS('SESSIONS_REPLACE',SESSIONS_REPLACE,SESSIONS_REPLACE,SESSIONS_REPLACE,SESSIONS_REPLACE)
del SESSIONS_REPLACE

#hooman only event,
def USER_GUILD_SETTINGS_UPDATE(client,data):
    # invidual guild settings data.
    pass

PARSER_DEFAULTS('USER_GUILD_SETTINGS_UPDATE',USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE)
del USER_GUILD_SETTINGS_UPDATE


EVENTS=EVENT_SYSTEM_CORE()

EVENTS.add_default('error'                      , 3 , ()                                        , )

EVENTS.add_default('ready'                      , 1 , 'READY'                                   , )
EVENTS.add_default('client_edit'                , 2 , 'USER_UPDATE'                             , )
EVENTS.add_default('message_create'             , 2 , 'MESSAGE_CREATE'                          , )
EVENTS.add_default('message_delete'             , 2 , ('MESSAGE_DELETE', 'MESSAGE_DELETE_BULK') , )
EVENTS.add_default('message_edit'               , 3 , 'MESSAGE_UPDATE'                          , )
EVENTS.add_default('embed_update'               , 3 , 'MESSAGE_UPDATE'                          , )
EVENTS.add_default('reaction_add'               , 2 , 'MESSAGE_REACTION_ADD'                    , )
EVENTS.add_default('reaction_clear'             , 3 , 'MESSAGE_REACTION_REMOVE_ALL'             , )
EVENTS.add_default('reaction_delete'            , 2 , 'MESSAGE_REACTION_REMOVE'                 , )
EVENTS.add_default('reaction_delete_emoji'      , 4 , 'MESSAGE_REACTION_REMOVE_EMOJI'           , )
EVENTS.add_default('user_edit'                  , 3 , 'PRESENCE_UPDATE'                         , )
EVENTS.add_default('user_presence_update'       , 3 , 'PRESENCE_UPDATE'                         , )
EVENTS.add_default('user_profile_edit'          , 4 , 'GUILD_MEMBER_UPDATE'                     , )
EVENTS.add_default('channel_delete'             , 3 , 'CHANNEL_DELETE'                          , )
EVENTS.add_default('channel_edit'               , 3 , 'CHANNEL_UPDATE'                          , )
EVENTS.add_default('channel_create'             , 2 , 'CHANNEL_CREATE'                          , )
EVENTS.add_default('channel_pin_update'         , 2 , 'CHANNEL_PINS_UPDATE'                     , )
EVENTS.add_default('channel_group_user_add'     , 3 , 'CHANNEL_RECIPIENT_ADD'                   , )
EVENTS.add_default('channel_group_user_delete'  , 3 , 'CHANNEL_RECIPIENT_REMOVE'                , )
EVENTS.add_default('emoji_create'               , 2 , 'GUILD_EMOJIS_UPDATE'                     , )
EVENTS.add_default('emoji_delete'               , 3 , 'GUILD_EMOJIS_UPDATE'                     , )
EVENTS.add_default('emoji_edit'                 , 3 , 'GUILD_EMOJIS_UPDATE'                     , )
EVENTS.add_default('guild_user_add'             , 3 , 'GUILD_MEMBER_ADD'                        , )
EVENTS.add_default('guild_user_delete'          , 4 , 'GUILD_MEMBER_REMOVE'                     , )
EVENTS.add_default('guild_create'               , 2 , 'GUILD_CREATE'                            , )
EVENTS.add_default('guild_edit'                 , 2 , 'GUILD_UPDATE'                            , )
EVENTS.add_default('guild_delete'               , 3 , 'GUILD_DELETE'                            , )
EVENTS.add_default('guild_ban_add'              , 3 , 'GUILD_BAN_ADD'                           , )
EVENTS.add_default('guild_ban_delete'           , 3 , 'GUILD_BAN_REMOVE'                        , )
EVENTS.add_default('guild_user_chunk'           , 2 , 'GUILD_MEMBERS_CHUNK'                     , )
EVENTS.add_default('integration_update'         , 2 , 'GUILD_INTEGRATIONS_UPDATE'               , )
EVENTS.add_default('role_create'                , 2 , 'GUILD_ROLE_CREATE'                       , )
EVENTS.add_default('role_delete'                , 3 , 'GUILD_ROLE_DELETE'                       , )
EVENTS.add_default('role_edit'                  , 3 , 'GUILD_ROLE_UPDATE'                       , )
EVENTS.add_default('webhook_update'             , 2 , 'WEBHOOKS_UPDATE'                         , )
EVENTS.add_default('voice_state_update'         , 4 , 'VOICE_STATE_UPDATE'                      , )
EVENTS.add_default('typing'                     , 4 , 'TYPING_START'                            , )
EVENTS.add_default('invite_create'              , 2 , 'INVITE_CREATE'                           , )
EVENTS.add_default('invite_delete'              , 2 , 'INVITE_DELETE'                           , )
EVENTS.add_default('relationship_add'           , 2 , 'RELATIONSHIP_ADD'                        , )
EVENTS.add_default('relationship_change'        , 3 , 'RELATIONSHIP_ADD'                        , )
EVENTS.add_default('relationship_delete'        , 2 , 'RELATIONSHIP_REMOVE'                     , )
EVENTS.add_default('gift_update'                , 3 , 'GIFT_CODE_UPDATE'                        , )

def _check_name_should_break(name):
    """
    Checks whether the passed `name` is type `str`.
    
    Used inside of ``check_name`` to check whether the given variable is usable, so we should stop checking
    other alternative cases.
    
    Parameters
    ----------
    name : `Any`
    
    Returns
    -------
    should_break : `bool`
        If non empty `str` is received returns `True`, meanwhile if `None` or empty `str` is received `False`.
    
    Raises
    ------
    TypeError
        If `name` was not passed as `None` or type `str`.
    """
    if (name is None):
        return False
        
    if type(name) is not str:
        raise TypeError(f'`name` should be `None` or type `str`, got `{name.__class__.__name__}`.')
        
    if name:
        return True
    
    return False
    
def check_name(func, name):
    """
    Tries to find the given `func`'s preferred name. The check order is the following:
    - Passed `name` argument.
    - `func.__event_name__`.
    - `func.__name__`.
    - `func.__class__.__name__`.
    
    If any of these is set (or passed at the case of `name`) as `None` or as an empty string, then those are ignored.
    
    Parameters
    ----------
    func : `callable`
        The function, what preferred name we are looking for.
    name : `None` or `str`
        A directly gvien name value by the user. Defaults to `None` by caller (or at least sit should).
    
    Returns
    -------
    name : `str`
        The preffered name of `func` with lower case characters only.
    
    Raises
    ------
    TypeError
        - If a checked name is not `None` or `str` instance.
        - If a metaclass was given.
    """
    while True:
        if _check_name_should_break(name):
            break
        
        if hasattr(func,'__event_name__'):
            name = func.__event_name__
            if _check_name_should_break(name):
                break
        
        #func or method
        if hasattr(func,'__name__'):
            name=func.__name__
            if _check_name_should_break(name):
                break
        
        func=type(func)
        if not issubclass(func,type) and hasattr(func,'__name__'):
            name=func.__name__
            if _check_name_should_break(name):
                break
        
        raise TypeError(f'Metaclasses are not allowed, got {func!r}.')
    
    if not name.islower():
        name=name.lower()
    return name

def check_argcount_and_convert(func, expected, errormsg=None):
    """
    If needed converts the given `func` to an async callable and then checks whether it expects the specified
    amount of non reserved positional arguments.
    
    `func` can be either:
    - An async `callable`.
    - A class with non async `__new__` (neither `__init__` of course) accepting no non reserved paremeters,
        meanwhile it's `__call__` is async. This is the convert (or instance) case and it causes the final argument
        count check to be applied on the type's `__call__`.
    - A class with async `__new__`.
    
    After the callable was choosed, then the amount of positional arguments are checked what it expects. Reserved
    arguments, like `self` are ignored and if the callable accepts keyword only argument, then it is a no-go.
    
    If every check passed, then at the convert case instances the type and returns that, meanwhile at the other cases
    it returns the received `func`.
    
    Parameters
    ----------
    func : `callable`
        The callable, what's type and argument count will checked.
    expected : `int`
        The amount of arguments, what would be passed to the given `func` when called at the future.
    errormsg : `str`, Optional
        A specified error message with what a `TypeError` will be raised at the end, if the given `func` is not async
        and neither cannot be converted to an async callable.
    
    Returns
    -------
    func : `callable`
    
    Raises
    ------
    TypeError
        - If `func` was not given as callable.
        - If `func` is not as async and neither cannot be converted to an async one.
        - If `func` expects less or more non reserved positional arguments as `expected` is.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async():
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_>expected:
            raise TypeError(f'`{func!r}` excepts at least `{min_!r}` non reserved arguments, meanwhile the event expects to pass `{expected!r}`.')
        
        if min_==expected:
            return func
        
        #min<expected
        if max_>=expected:
            return func
        
        if analyzer.accepts_args():
            return func
        
        raise TypeError(f'`{func!r}` expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects to pass `{expected!r}`.')
    
    if analyzer.can_instance_to_async_callable():
        sub_analyzer=CallableAnalyzer(func.__call__, as_method=True)
        if sub_analyzer.is_async():
            min_, max_ = sub_analyzer.get_non_reserved_positional_argument_range()
            
            if min_>expected:
                raise TypeError(f'After instancing `{func!r}` would still except at least `{min_!r}` non reserved arguments, meanwhile the event expects to pass `{expected!r}`.')
            
            if min_==expected:
                func = analyzer.instance_to_async_callable()
                return func
            
            #min<expected
            if max_>=expected:
                func = analyzer.instance_to_async_callable()
                return func
            
            if sub_analyzer.accepts_args():
                func = analyzer.instance_to_async_callable()
                return func
            
            raise TypeError(f'After instancing `{func!r}` would still expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects to pass `{expected!r}`.')
            
            func = analyzer.instance_to_async_callable()
            return func
    
    if errormsg is None:
        errormsg=f'Not async callable type, or cannot be instance to async: `{func!r}`.'
    
    raise TypeError(errormsg)

def compare_converted(converted,non_converted):
    # function, both should be functions
    if isinstance(non_converted,function):
        return (converted is non_converted)
    
    # method, both should be methods
    if isinstance(non_converted,MethodLike):
        return (converted is non_converted)
    
    # callable object, both should be the same
    if not isinstance(non_converted,type) and hasattr(type(non_converted),'__call__'):
        return (converted is non_converted)
    
    # type, but not metaclass
    if not issubclass(non_converted,type) and isinstance(non_converted,type):
        
        # async initializer, both is type
        if iscoro(non_converted.__new__):
            return (converted is non_converted)
        
        # async call -> should be initalized already, compare the converted's type
        if hasattr(non_converted,'__call__'):
            return (type(converted) is non_converted)
    
    #meow?
    raise TypeError(f'Expected function, method or a callable object, got {non_converted!r}')

def _convert_unsafe_event_iterable(iterable, type_=None):
    """
    Converts an iterable to a list of ``EventListElement``-s. This function is called to generate a ``eventlist``
    compatible `list` to avoid handling the same cases everywhere.
    
    `iterable`'s element's can be:
    - ``EventListElement`` instance.
    - `type_` instance if given.
    - `tuple` of `1`-`3` elements (`func`, `name`, `kwargs`).
    - `dict` of keyword arguments, what contains at least 1 key: `'func'`.
    - `func` itself.
    
    Parameters
    ----------
    iterable : `iterable`
        The iterable, what's elements will be checked.
    type_ : `None `or `type`
        If `type_` was passed, then each element is prevaidated with the given type. Some extension classes might
        support behaviour.
        
        The given `type_` should implement a `from_kwargs` constructor.
    
    Returns
    -------
    result : `list` of (``EventListElement`` or ``type_``)
    
    Raises
    ------
    ValueError
        If an element of the received iterable does not macthes any of the expected formats.
    """
    result=[]
    for element in iterable:
        if type(element) is EventListElement:
            if (type_ is not None):
                element=type_.from_kwargs(element.func, element.name, element.kwargs)
        if type(element) is type_:
            pass
        else:
            if isinstance(element,tuple):
                element_len=len(element)
                if element_len>3 or element_len==0:
                    raise ValueError(f'Expected `tuple` with length 1 or 2, got `{element!r}`.')
                
                func=element[0]
                if element_len==1:
                    name=None
                    kwargs=None
                else:
                    name=element[1]
                    if (name is not None) and (type(name) is not str):
                        raise ValueError(f'Expected `None` or `str` instance at index 1 at element: `{element!r}`')
                    
                    if element_len==2:
                        kwargs=None
                    else:
                        kwargs=element[2]
                        if (kwargs is not None):
                            if (type(kwargs) is not dict):
                                raise ValueError(f'Expected `None` or `dict` instance at index 1 at element: `{element!r}`')
                            
                            if not kwargs:
                                kwargs=None
            
            elif isinstance(element,dict):
                try:
                    func=element.pop('func')
                except KeyError:
                    raise ValueError(f'Expected all `dict` elements to contain `\'func\'` key, but was not found at `{element!r}`') from None
                
                name=element.pop('name',None)
                
                if element:
                    kwargs=element
                else:
                    kwargs=None
            
            else:
                func=element
                name=None
                kwargs=None
            
            if type_ is None:
                element = EventListElement(func,name,kwargs)
            else:
                element = type_.from_kwargs(func,name,kwargs)
            
        result.append(element)
        continue
        
    return result

class _EventHandlerManager(object):
    """
    Gives a decorator functionality to an event handler, because 'rich' event handlers still can not be used a
    decorator, their `__call__` is already allocated for handling their respective event.
    
    This class is familiar to ``eventlist``, but it directly works with the respective event handler giving an
    easy API to do operations with it.
    
    Attributes
    ----------
    parent : `Any`
        The ``_EventHandlerManager``'s parent event handler.
    _supports_from_class : `bool`
        Whether `.parent` implements `__setevent_from_class__` method.
    """
    __slots__ = ('parent', '_supports_from_class')
    
    def __init__(self, parent):
        """
        Creates an ``_EventHandlerManager`` from the given event handler.
        
        The `parent` event handler should implement the following methods:
        - `.__setevent__(func, name, **kwargs)`
        - `.__delvent__(func, name)`
        And optionally:
        - `.__setevent_from_class__(klass)`
        
        Parameters
        ----------
        parent : `Any`
        """
        self.parent=parent
        self._supports_from_class = hasattr(type(parent),'__setevent_from_class__')
    
    def __repr__(self):
        """Returns the representation of the event handler manager."""
        return f'<{self.__class__.__name__} of {self.parent!r}>'
    
    def __call__(self, func=None, name=None, **kwargs):
        """
        Adds the given `func` to the event handler manager's parent. If `func` is not passed, then returns a
        ``._wrapper` to allow using the manager as a decorator with still passing keyword arguments.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the respective event handler.
        name : `str` or `None`
            A name to be used instead of the passed `func`'s.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be passed with the given `func`to the event handler.
        
        Returns
        -------
        func : `callable`
            - The created instance by the respective event handler.
            - If `func` was not passed, then returns a ``._wrapper`` instance.
        
        Adds the given `func` to the ``eventlist`` with the other given keyword arguments.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the eventlist.
        name : `str` or `None`
            A name to be used instead of the passed `func`'s when adding it.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be used when the passed `func` is used up.
        """
        if func is None:
            return self._wrapper(self,name,kwargs)
        
        name=check_name(func,name)
        
        func=self.parent.__setevent__(func,name,**kwargs)
        return func
    
    def from_class(self, klass):
        """
        Allows the event handler manager to be able to capture a class and create add it to the parent event handler
        from it's attributes.
        
        Parameters
        ----------
        klass : `type`
            The class to capture.
        
        Returns
        -------
        func : `callable`
            The created instance by the respective event handler.
        
        Raises
        ------
        TypeError
            If the parent of the event handler manager has no support for `.from_class`.
        """
        if not self._supports_from_class:
            raise TypeError(f'`.from_class` is not supported by `{self.parent!r}`.')
        
        return self.parent.__setevent_from_class__(klass)
        
    def remove(self,func, name=None, **kwargs):
        name=check_name(func,name)
        
        self.parent.__delevent__(func,name,**kwargs)
    
    class _wrapper(object):
        """
        When the parent ``_EventHandlerManager`` is called and `func` was not passed (so only keyword arguments were
        if any), then an instance of this class is returned to allow using ``_EventHandlerManager`` as a decorator with
        allowing passing additional keyword arguments at the same time.
        
        Attributes
        ----------
        parent : ``_EventHandlerManager``
            The owner event handler manager.
        name : `str` or `None`
            Passed `name` keyword argument, when the wrapper was created.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additionally passed keyword arguments when the wrapper was created.
        """
        __slots__ = ('parent', 'name', 'kwargs')
        def __init__(self, parent, name, kwargs):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``_EventHandlerManager``
                The owner event handler manager.
            name : `str` or `None`
                Passed `name` keyword argument, when the wrapper was created.
            kwargs : `None` or `dict` of (`str`, `Any`) items
                Additionally passed keyword arguments when the wrapper was created.
            """
            self.parent=parent
            self.name=name
            self.kwargs=kwargs
        
        def __call__(self, func,):
            """
            Calls the wrapper's parent event handler manager with the given `func` and with the stored up name and
            with the other stored keyword arguments.
            
            Parameters
            ----------
            func : `callable`
                The function to added to the parent event handler manager's event handler.
            
            Returns
            -------
            func : `callable`
                The created instance by the respective event handler.
            """
            return self.parent(func, self.name, **self.kwargs)
    
    def __getattr__(self, name):
        """Returns the attribute of the event handler manager's parent."""
        return getattr(self.parent, name)
    
    def extend(self, iterable):
        """
        Extends the respective event handler with the given iterable of events.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        TypeError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if type(iterable) is eventlist:
            type_=iterable.type
            if (type_ is not None):
                parent=self.parent
                supported_types=getattr(parent,'SUPPORTED_TYPES',None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                for element in iterable:
                    parent.__setevent__(element,None)
                return
        else:
            iterable=_convert_unsafe_event_iterable(iterable)
        
        parent=self.parent
        for element in iterable:
            func=element.func
            name=element.name
            
            name=check_name(func,name)
            
            kwargs=element.kwargs
            if kwargs is None:
                parent.__setevent__(func,name)
            else:
                parent.__setevent__(func,name,**kwargs)
    
    def unextend(self, iterable):
        """
        Unextends the respective event handler with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
            - If any of the passed element is not stored by the parent event handler. At this case error is raised
                only at the end.
        """
        if type(iterable) is eventlist:
            type_=iterable.type
            if (type_ is not None):
                parent=self.parent
                supported_types=getattr(parent,'SUPPORTED_TYPES',None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                collected=[]
                for element in iterable:
                    try:
                        parent.__delevent__(element,None)
                    except ValueError as err:
                        collected.append(err.args[0])

                if collected:
                    raise ValueError('\n'.join(collected)) from None
                return
        else:
            iterable=_convert_unsafe_event_iterable(iterable)
        
        collected=[]
        parent=self.parent
        for element in iterable:
            func=element.func
            name=element.name
            
            name=check_name(func,name)
            
            kwargs=element.kwargs
            try:
                
                if kwargs is None:
                    parent.__delevent__(func,name)
                else:
                    parent.__delvent__(func,name,**kwargs)
            
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected)) from None
        
class EventListElement(object):
    """
    Represents an element of an ``eventlist``.
    
    Attributes
    ----------
    func : `callable`
        The event of the event-list element.
    name : `None` or `str`
        Alternative name to use instead of `func`'s.
    kwargs : `None` or `dict` of (`str`, `Any`) items
        Additional kwargs for `func`.
    """
    __slots__ = ('func', 'name', 'kwargs', )
    def __init__(self, func, name, kwargs):
        """
        Creates a ``EventListElement` from the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The event of the eventlist element.
        name : `None` or `str`
            Alternative name to use instead of `func`'s.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additional kwargs for `func`.
        """
        self.func  = func
        self.name  = name
        self.kwargs= kwargs
    
    def __repr__(self):
        """Returns the representation of the eeventlist element."""
        return f'{self.__class__.__name__}({self.func!r}, {self.name!r}, kwargs={self.kwargs!r})'
    
    def __len__(self):
        """Additional information for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """Unpacks the eventlist element."""
        yield self.func
        yield self.name
        yield self.kwargs
    
class eventlist(list):
    """
    Represents a container to store events before adding them to a client. Some extension classes might support this
    class as well.
    
    Attributes
    ----------
    _supports_from_class : `bool`
        If `type_` was passed when creating an eventlist and the it supports creation with a `from_class` class method.
    kwargs : `None` or `dict` of (`str`, `Any`) items
        Keyword arguments used for each element when extending teh client's events with the event-list.
    type : `None` or `type`
        If `type_` was passed when creating the eventlist, then each added element is prevaidated with the given type
        before adding them. Some extension classes might support behaviour.
    
    Notes
    -----
    Hata's `commands` extension class supports collecting commands in ``eventlist`` and prevalidating as well with
    passing `type_` as `Command`.
    """
    insert = RemovedDescriptor()
    sort = RemovedDescriptor()
    pop = RemovedDescriptor()
    reverse = RemovedDescriptor()
    remove = RemovedDescriptor()
    index = RemovedDescriptor()
    count = RemovedDescriptor()
    __mul__ = RemovedDescriptor()
    __rmul__ = RemovedDescriptor()
    __imul__ = RemovedDescriptor()
    __add__ = RemovedDescriptor()
    __radd__ = RemovedDescriptor()
    __iadd__ = RemovedDescriptor()
    __setitem__ = RemovedDescriptor()
    __contains__ = RemovedDescriptor()
    
    __slots__ = ('_supports_from_class', 'kwargs', 'type')
    
    def __new__(cls, iterable=None, type_=None, **kwargs):
        """
        Creates a new eventlist from the the given parameters.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            An iterable of events to extend the eventlist with.
        type_ : `type`, Optional
            A type to validate each added element to the eventlist.
        **kwargs : Keyword arguments
            Additional keyword arguments to be used when adding each element.
        
        Raises
        ------
        TypeError
            If `type_` was passed as not as `type` instance, or if it has no `from_kwargs` method.
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if (type_ is None):
            supports_from_class = False
        else:
            if not isinstance(type_,type):
                raise TypeError(f'`type_` should be `type` instance, got `{type!r}`.')
            
            if not hasattr(type_,'from_kwargs'):
                raise TypeError('The passed `type_` has no method called `from_kwargs`.')
            
            supports_from_class = hasattr(type_,'from_class')
        
        if not kwargs:
            kwargs = None
        
        self=list.__new__(cls)
        self.type=type_
        self._supports_from_class = supports_from_class
        self.kwargs = kwargs
        
        if (iterable is not None):
            self.extend(iterable)
        
        return self
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    
    class _wrapper(object):
        """
        When a parent ``eventlist`` is called and `func` was not passed (so only keyword arguments were if any), then
        an instance of this class is returned. It's main purpose is to enable using ``eventlist`` as a decorator with
        allowing passing additional keyword arguments at the same time.
        
        Attributes
        ----------
        parent : ``eventlist``
            The owner eventlist.
        name : `str` or `None`
            Passed `name` keyword argument, when the wrapper was created.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additionally passed keyword arguments when the wrapper was created.
        """
        __slots__ = ('parent', 'name', 'kwargs')
        def __init__(self, parent, name, kwargs):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``eventlist``
                The owner eventlist.
            name : `str` or `None`
                Passed `name` keyword argument, when the wrapper was created by the parent ``eventlist``.
            kwargs : `None` or `dict` of (`str`, `Any`) items
                Additionally passed keyword arguments when the wrapper was created by it's parent.
            """
            self.parent=parent
            self.name=name
            self.kwargs=kwargs
        
        def __call__(self, func):
            """
            Calling an ``eventlist``'s wrapper adds the given `func` to it's parent ``eventlist``.
            
            Parameters
            ----------
            func : `callable`
                The function to add to the parent ``eventlist``.
            
            Returns
            -------
            func : `callable`
                The function if the parent  ``eventlist`` has no `.type` set. If it has then an instance of that type.
            """
            parent=self.parent
            type_ = parent.type
            
            if type_ is None:
                element = EventListElement(func, self.name, self.kwargs)
            else:
                element = func = type_.from_kwargs(func, self.name, self.kwargs)
            
            list.append(self.parent, element)
            return func
    
    def from_class(self, klass):
        """
        Allows the ``eventlist`` to be able to capture a class and create an element from it's attributes.
        
        Parameters
        ----------
        klass : `type`
            The class to capture.
        
        Returns
        -------
        element : `callable`
            The created instance from the eventlist's `.type`.
        
        Raises
        ------
        TypeError
            If the eventlist has no `.type` set, or if it's `.type` is not supporting this method.
        """
        type_=self.type
        if not self._supports_from_class:
            if type_ is None:
                message='On `eventlist` without type `.from_class` method cannot be used.'
            else:
                message=f'The `eventlist`\'s type: `{type!r}` is not supporting `.from_class`.'
            raise TypeError(message)
        
        # kwargs are gonna be emptied, so copy them if needed
        kwargs = self.kwargs
        if (kwargs is not None):
            kwargs = kwargs.copy()
        
        element = type_.from_class(klass, kwargs = kwargs)
        list.append(self,element)
        return element
    
    def extend(self, iterable):
        """
        Extends the ``eventlist`` with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
            An iterable of events to extend the eventlist with.
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if type(iterable) is type(self):
            if self.type is not iterable.type:
                raise ValueError(f'Extensing {self.__class__.__name__} with an other object of the same type, but with a different type, own: `{self.type!r}`, other\'s: `{iterable.type!r}`.')
        else:
            iterable=_convert_unsafe_event_iterable(iterable, self.type)
        
        list.extend(self, iterable)
    
    def unextend(self, iterable):
        """
        Unextends the eventlist with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
            An iterable of events to unextend the eventlist with.
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
            - If any of the passed elements is not at the ``eventlist``. At this case error is raised only at the end.
        """
        if type(iterable) is not type(self):
            iterable=_convert_unsafe_event_iterable(iterable,self.type)
        else:
            if self.type is not iterable.type:
                raise ValueError(f'Extensing {self.__class__.__name__} with an other object of the same type, but with a different type, own: `{self.type!r}`, other\'s: `{iterable.type!r}`.')
        
        collected=[]
        for element in iterable:
            try:
                self.remove(*element)
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected))
        
    def __call__(self, func=None, name=None, **kwargs):
        """
        Adds the given `func` to the ``eventlist`` with the other given keyword arguments. If `func` is not passed,
        then returns a ``._wrapper` to allow using the ``eventlist`` as a decorator with still passing keyword
        arguments.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the eventlist.
        name : `str` or `None`
            A name to be used instead of the passed `func`'s when adding it.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be used when the passed `func` is used up.
        
        Returns
        -------
        func : `callable`
            - If `func` was passed and the eventlist has no `.type` then returns the passed `func`.
            - If `func` was passed and the eventlist has `.type` set, then returns an instance of that.
            - If `func` was not passed, then returns a ``._wrapper`` instance.
        
        Raises
        ------
        TypeError
            If `name` was pased with incorrect type.
        """
        if (name is not None):
            if type(name) is not str:
                raise TypeError(f'`name` should be `None`, or type `str`, got `{name!r}`.')
            
            if name:
                if not name.islower():
                    name=name.lower()
            else:
                name=None
        
        own_kwargs = self.kwargs
        if (own_kwargs is not None) and own_kwargs:
            for name_, value_ in own_kwargs.items():
                kwargs.setdefault(name_, value_)
        
        if func is None:
            return self._wrapper(self,name,kwargs)
        
        type_ = self.type
        if type_ is None:
            element = EventListElement(func,name,kwargs)
        else:
            element = func = type_.from_kwargs(func,name,kwargs)
        
        list.append(self,element)
        return func
        
    def remove(self, func, name=None):
        """
        Removes an element of the eventlist.
        
        Parameters
        ----------
        func : `callable`
            The function to remove.
        name : `str`, Optional
            The name of the function to remove.

        Raises
        ------
        TypeError
            If `name` was passed with incorrect type.
        ValueError
            If the passed `func` - `name` combination was not found.
        """
        if (name is not None):
            if type(name) is not str:
                raise TypeError(f'`name` should be `None`, or type `str`, got `{name!r}`.')
            
            if name:
                if not name.islower():
                    name=name.lower()
            else:
                name=None
            
        # we might overwrite __iter__ later
        for element in list.__iter__(self):
            
            converted_name=element.name
            # `name` can be `None` or `str`
            if converted_name is None:
                if name is not None:
                    continue
            else:
                if name is None:
                    continue
                
                if converted_name!=name:
                    continue
            
            if compare_converted(element.func,func):
                return
        
        raise ValueError(f'Did not find any element, what matched the passed func={func!r}, name={name!r} combination.')
    
    def __repr__(self):
        """Returns the representation of the eventlist."""
        result=[self.__class__.__name__,'([']
        
        limit=list.__len__(self)
        if limit!=0:
            index=0
            
            while True:
                element=list.__getitem__(self,index)
                result.append(repr(element))
                index=index+1
                
                if index==limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(']')
        
        type_=self.type
        if (type_ is not None):
            result.append(', type=')
            result.append(repr(type_))
        
        kwargs = self.kwargs
        if (kwargs is not None):
            result.append(', kwargs=')
            result.append(repr(kwargs))
        
        result.append(')')
        return ''.join(result)
    
    def add_kwargs(self, **kwargs):
        """
        Adds keyword arguments to the ``eventlist`'s.
        
        Parameters
        ----------
        **kwargs : Keyword arguments
            KeyWord arguments to extend the ``eventlist``'s with.
        """
        if not kwargs:
            return
        
        own_kwargs = self.kwargs
        if own_kwargs is None:
            self.kwargs = kwargs
        else:
            own_kwargs.update(kwargs)
    
    def remove_kwargs(self, *names):
        """
        Removes keyword arguments of the ``eventlist`` by their name.
        
        Parameters
        ----------
        *names : Arguemnts
            Keyword argument's name added to the ``eventlist``.
        """
        if not names:
            return
        
        own_kwargs = self.kwargs
        if own_kwargs is None:
            return
        
        for name in names:
            try:
                del own_kwargs[name]
            except KeyError:
                pass
        
        if not own_kwargs:
            self.kwargs = None
    
    def clear_kwargs(self):
        """
        Clears the kwargs of the eventlist.
        """
        self.kwargs = None

# this class is a placeholder for the `with` statemnet support
# also for the `shortcut` propery as well.
class EventHandlerBase(object):
    """
    Base class for event handlers.
    """
    __slots__=()
    
    # subclasses should overwrite it
    async def __call__(self, *args):
        """
        The method what will be called by the respective parser. The first received argument is always a ``Client``
        meanwhile the rest depends on the dispatch event.
        
        Parameters
        ----------
        *args : Additional positional arguments
        """
        pass

    # subclasses should overwrite it
    def __setevent__(self, func, name):
        """
        Adds the specified event to the event handler. Subclasses might add additional keyword arguments as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be added.
        name : `str` or `None`
            The name of the event to use over the `func`'s.
        
        Returns
        -------
        func : `callable`
            The created event.
        """
        pass

    # subclasses should overwrite it
    def __delevent__(self, func, name):
        """
        Removes the specified event from the event handler. Subclasses might add additional keyword arguments as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be removed.
        name : `str` or `None`
            The name of the event when searching for `func`. When `func` was added with `name` passed as non `None`,
            then here `name` should be passed with the same name.
        
        Raises
        ------
        ValueError
            The event handler not contains the given `func` - `name` combination.
        """
        pass

    @property
    def shortcut(self):
        """
        Shortucts the event handler's event adding and removing functionality to make those operations easier.
        
        Returns
        -------
        event_handler_manager : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)

class EventWaitforMeta(type):
    """
    Metaclass for `waitfor` events handlers
    
    The defaultly supported events are the following:
    - `message_create`
    - `message_edit`
    - `message_delete`
    - `channel_create`
    - `channel_edit`
    - `channel_delete`
    - `role_create`
    - `role_edit`
    - `role_delete`
    - `guild_delete`
    - `guild_edit`
    - `emoji_edit`
    - `emoji_delete`
    - `reaction_add`
    - `reaction_delete`
    
    See Also
    --------
    EventWaitforBase : Base class to inherit instead of metaclassing ``EventWaitforMeta``.
    """
    def __call__(cls, *args, **kwargs):
        """
        Instances the type.
        
        Autoadds a `.waitfors` instance attribute to them and also sets it as a `WeakKeyDictionary`, so you would not
        need to bother with that.
        
        Parameters
        ----------
        *args : Additional positional arguments
        **kwargs : Additional keyword arguments
        
        Returns
        -------
        object_ : `Any`
        """
        object_ = cls.__new__(cls, *args, **kwargs)
        if type(object_) is not cls:
            return object_
        
        object_.waitfors = WeakKeyDictionary()
        cls.__init__(object_,*args,**kwargs)
        return object_
    
    _call_waitfors = {}
    
    async def _call_message_create(self, client, message):
        args = (client, message)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
        
    _call_waitfors['message_create'] = _call_message_create
    del _call_message_create
    
    async def _call_message_edit(self, client, message, old_attributes):
        args = (client, message, old_attributes)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['message_edit'] = _call_message_edit
    del _call_message_edit
    
    async def _call_message_delete(self, client, message,):
        args = (client, message)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['message_delete'] = _call_message_delete
    del _call_message_delete
    
    async def _call_channel_create(self, client, channel):
        guild = channel.guild
        if guild is None:
            return
        args = (client, channel)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_create'] = _call_channel_create
    del _call_channel_create
    
    async def _call_channel_edit(self, client, channel, old_attributes):
        args = (client, channel, old_attributes)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, old_attributes)
    
    _call_waitfors['channel_edit'] = _call_channel_edit
    del _call_channel_edit
    
    async def _call_channel_delete(self, client, channel, guild):
        args = (client, channel, guild)
        self._run_waitfors_for(channel, args)
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_delete'] = _call_channel_delete
    del _call_channel_delete
    
    async def _call_role_create(self, client, role):
        args = (client, role)
        guild = role.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_create'] = _call_role_create
    del _call_role_create
    
    async def _call_role_edit(self, client, role, old_attributes):
        args = (client, role, old_attributes)
        self._run_waitfors_for(role, args)
        guild = role.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_edit'] = _call_role_edit
    del _call_role_edit

    async def _call_role_delete(self, client, role, guild):
        args = (client, role, guild)
        self._run_waitfors_for(role, args)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_delete'] = _call_role_delete
    del _call_role_delete
    
    async def _call_guild_delete(self, client, guild, profile):
        args = (client, guild, profile)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_delete'] = _call_guild_delete
    del _call_guild_delete
    
    async def _call_guild_edit(self, client, guild, old_attributes):
        args = (client, guild, old_attributes)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_edit'] = _call_guild_edit
    del _call_guild_edit
    
    async def _call_emoji_create(self, client, emoji):
        args = (client, emoji)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_create'] = _call_emoji_create
    del _call_emoji_create
    
    async def _call_emoji_edit(self, client, emoji, old_attributes):
        args = (client, emoji, old_attributes)
        self._run_waitfors_for(emoji, args)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_edit'] = _call_emoji_edit
    del _call_emoji_edit

    async def _call_emoji_delete(self, client, emoji, guild):
        args = (client, emoji, guild)
        self._run_waitfors_for(emoji, args)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_delete'] = _call_emoji_delete
    del _call_emoji_delete
    
    async def _call_reaction_add(self, client, event):
        args = (client, event)
        self._run_waitfors_for(event.message, args)
    
    _call_waitfors['reaction_add'] = _call_reaction_add
    del _call_reaction_add
    
    async def _call_reaction_delete(self, client, event):
        args = (client, event)
        self._run_waitfors_for(event.message, args)
    
    _call_waitfors['reaction_delete'] = _call_reaction_delete
    del _call_reaction_delete

class EventWaitforBase(EventHandlerBase, metaclass=EventWaitforMeta):
    """
    Base class for event handlers, which implement waiting for a specified action to occure.
    
    Attrbiutes
    ----------
    waitfors : `WeakValueDictionary`
        An autoadded container to store `entity` - `async callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `None` or `str` = `None`
        Predefined name to what the event handler will be added.
    call_waitfors : `None` or `async callable` = `None`
        An added method to subclasses to ensure the waitfors if overwrite `__call__` is overwritten. Subclasses can
        also overwrite `call_waitfors` method as well.
    """
    __slots__ = ('waitfors', )
    __event_name__ = None
    call_waitfors = None
    
    def append(self, target, waiter):
        """
        Adds a new relation to `.waitfors`.
        
        When the respective event is received with the specified `target` entity, then `waiter` will be ensured.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
        waiter : `async callable`
        """
        try:
            actual=self.waitfors[target]
            if type(actual) is asynclist:
                actual.append(waiter)
            else:
                self.waitfors[target]=container=asynclist()
                container.append(actual)
                container.append(waiter)
        except KeyError:
            self.waitfors[target]=waiter
    
    def remove(self, target, waiter):
        """
        Removes the specified relation from `.waitfors`.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
        waiter : `async callable`
        """
        try:
            container=self.waitfors.pop(target)
        except KeyError:
            return
        
        if type(container) is not asynclist:
            return
        
        try:
            container.remove(waiter)
        except ValueError:
            pass
        else:
            if len(container)==1:
                self.waitfors[target]=container[0]
                return
        
        self.waitfors[target]=container
    
    def get_waiter(self, target, waiter, by_type=False, is_method=False):
        """
        Looks up whether any of the given `target` - `waiter` relation is stored inside of `.waiters` and if there is any,
        then returns the first find. If non, then returns `None`.
        
        Parameters
        ----------
        target : ``DiscordEntitiy`` instance
            The target entity.
        waiter : `Any`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiter : `Any`
        """
        try:
            element = self.waitfors[target]
        except KeyError:
            return None
        
        if type(element) is asynclist:
            for element in element:
                if is_method:
                    if not isinstance(element,MethodLike):
                        continue
                    
                    element = element.__self__
                
                if by_type:
                    if type(element) is waiter:
                        return element
                    else:
                        continue
                else:
                    if element == waiter:
                        return element
                    else:
                        continue
            
            return None
        
        else:
            if is_method:
                if not isinstance(element,MethodLike):
                    return None
                
                element = element.__self__
            
            if by_type:
                if type(element) is waiter:
                    return element
                else:
                    return None
            else:
                if element == waiter:
                    return element
                else:
                    return None

    def get_waiters(self, target, waiter, by_type=False, is_method=False):
        """
        Looks up the waiters of `target` - `waiter` relation stored inside of `.waiters` and returns all the matched
        one.
        
        Parameters
        ----------
        target : ``DiscordEntitiy`` instance
            The target entity.
        waiter : `Any`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiters : `list` of `Any`
        """
        result = []
        
        try:
            element = self.waitfors[target]
        except KeyError:
            return result
        
        if type(element) is asynclist:
            for element in element:
                if is_method:
                    if not isinstance(element,MethodLike):
                        continue
                    
                    element = element.__self__
                
                if by_type:
                    if type(element) is not waiter:
                        continue
                else:
                    if element != waiter:
                        continue
                
                result.append(element)
                continue
        
        else:
            if is_method:
                if not isinstance(element,MethodLike):
                    return result
                
                element = element.__self__
            
            if by_type:
                if type(element) is waiter:
                    result.append(element)
            else:
                if element == waiter:
                    result.append(element)
        
        return result
    
    def _run_waitfors_for(self, target, args):
        """
        Runs the waitfors of the given target.
        
        Parameters
        ----------
        target : ``DiscordEntitiy`` instance
            The target entity.
        args : `tuple` of `Any`
            Arguments to ensure the watfors with.
        """
        try:
            event=self.waitfors[target]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(event(*args), KOKORO)
            else:
                Task(event(*args), KOKORO)
        
def EventWaitforMeta__new__(cls, class_name, class_parents, class_attributes):
    """
    Subclasses `EventWaitforBase``.
    
    Parameters
    ----------
    class_name : `str`
        The created classe's name.
    class_parents : `tuple` of `type` instances
        The superclasses of the creates type.
    class_attributes : `dict` of (`str`, `Any`) items
        The class attributes of the created type.
    
    Returns
    -------
    type : ``EventWaitforMeta`` instance
        The created type.
    
    Raises
    ------
    TypeError
        - If the class do not inherits ``EventWaitforBase``.
        - If `.__event_name__` was not set or was no set correctly. (Note that if was not ste, then the classe's name
            is used instead.)
        - If there is no predeifned `call_waitfors` for the class and it does not defines one either.
    """
    for base in class_parents:
        if issubclass(base,EventWaitforBase):
            break
    else:
        raise TypeError(f'`{cls.__name__} should be only the metaclass of `{EventWaitforBase.__name__}`.')
    
    event_name = class_attributes.get('__event_name__')
    if event_name is None:
        event_name = class_name
    
    if event_name not in EVENTS.parsers:
        raise TypeError(f'`{class_name}.__event_name__` is not set, or not set correctly.')
    
    if (class_attributes.get('call_waitfors') is None):
        try:
            call_waitfors = cls._call_waitfors[event_name]
        except KeyError:
            raise TypeError(f'The following event name: `{event_name!r}` has no auto `call_waitfor` added. Please define one.')
        
        class_attributes['call_waitfors'] = call_waitfors
        
        try:
            call = class_attributes.get('__call__')
        except KeyError:
            call = None
        
        if (call is None) or (call is EventHandlerBase.__call__):
            class_attributes['__call__'] = call_waitfors
    
    return type.__new__(cls, class_name, class_parents, class_attributes)

EventWaitforMeta.__new__  = EventWaitforMeta__new__
del EventWaitforMeta__new__

READY_STATE_TIMEOUT = 2.0

class ReadyState(object):
    """
    Client on login in fill up their `.ready_state` with ``Guild`` objects, which will have their members requested.
    
    Attributes
    ----------
    guild_left_counter : `int`
        The amount of guild, what's data is expected to be receiveed.
    ready_left_counter : `int`
        The amount of ready events, for which the ready state should wait.
    guilds : `list of ``Guild``
        A list of guilds, which members will be requested
    last_guild : `float`
        The time when the last guild's data was received.
    last_ready : `float`
        The time when the last shard got a ready event.
    wakeupper : `Future`
        A Future what wakes up the `__await__` generator of the ready state.
    """
    __slots__ = ('guild_left_counter', 'ready_left_counter', 'guilds', 'last_guild', 'last_ready', 'wakeupper', )
    def __init__(self, client, guild_datas):
        """
        Creates a ready state.
        
        Parameters
        ----------
        client : ``Client``
            The parent client.
        guild_datas : `list` of `Any`
            Received guilds' datas.
        """
        self.wakeupper = Future(KOKORO)
        self.guilds = []
        self.guild_left_counter = len(guild_datas)
        
        ready_left_counter = client.shard_count
        if ready_left_counter < 2:
            ready_left_counter = 0
        else:
            ready_left_counter -=1
        self.ready_left_counter = ready_left_counter
        
        now=monotonic()
        self.last_guild = now
        self.last_ready = now
    
    def shard_ready(self, guild_datas):
        """
        Sets the ready state's `.last_ready` to the current time and increases it's `.guild_left_counter` by the
        length of the given data.
        
        Parameters
        ----------
        guild_datas : `list` of `Any`
            Received guild datas.
        """
        self.last_ready = monotonic()
        self.ready_left_counter -=1
        self.guild_left_counter += len(guild_datas)
    
    if CACHE_PRESENCE:
        def feed(self, guild):
            if guild.is_large:
                self.guilds.append(guild)
            
            self.last_guild = monotonic()
            guild_left_counter = self.guild_left_counter = self.guild_left_counter-1
            if (not guild_left_counter) and (not self.ready_left_counter):
                self.wakeupper.set_result_if_pending(True)
    
    elif CACHE_USER:
        def feed(self, guild):
            self.guilds.append(guild)
            
            self.last_guild = monotonic()
            guild_left_counter = self.guild_left_counter = self.guild_left_counter-1
            if (not guild_left_counter) and (not self.ready_left_counter):
                self.wakeupper.set_result_if_pending(True)
    
    else:
        def feed(self, guild):
            self.last_guild = monotonic()
            guild_left_counter = self.guild_left_counter = self.guild_left_counter-1
            if (not guild_left_counter) and (not self.ready_left_counter):
                self.wakeupper.set_result_if_pending(True)
    
    if (shard_ready.__doc__ is not None):
        feed.__doc__ = (
        """
        Feeds the given `guild` to the ready state. Sets the last received guild's time to the current time and ends
        the ready state if there are no more guilds to receive.
        
        Parameters
        ----------
        guild : ``Guild``
        """)
    
    def __iter__(self):
        """
        Waits till the ready state receives all of it's shards and guilds, or till timeout occures.
        """
        wakeupper = self.wakeupper
        
        last_guild = self.last_guild
        last_shard = self.last_ready
        if last_guild > last_shard:
            last_wakeup = last_guild
        else:
            last_wakeup = last_shard
        
        while True:
            wakeupper._loop.call_at(last_wakeup+READY_STATE_TIMEOUT, wakeupper.__class__.set_result_if_pending, wakeupper, False)
            last = yield from wakeupper
            if last:
                break
            
            wakeupper.clear()
            
            last_guild = self.last_guild
            last_shard = self.last_ready
            if last_guild > last_shard:
                next_wakeup = last_guild
            else:
                next_wakeup = last_shard
            
            if next_wakeup == last_wakeup:
                break
            
            last_wakeup = next_wakeup
            continue
    
    __await__=__iter__


class ChunkWaiter(EventHandlerBase):
    __slots__=('waiters',)
    __event_name__='guild_user_chunk'
    def __init__(self):
        self.waiters={}
    
    # Interact directly with `self.waiters` instead.
    def __setevent__(self, waiter, nonce):
        """
        Raises
        ------
        RuntimeError
            Interact with self.waiters instead.
        """
        raise RuntimeError('Interact with self.waiters instead.')
    
    def __delevent__(self, waiter, nonce):
        """
        Raises
        ------
        RuntimeError
            Interact with self.waiters instead.
        """
        raise RuntimeError('Interact with self.waiters instead.')
    
    async def __call__(self, client, event):
        """
        Ensures that the chunk waiter for the specifed nonce is called and if it returns `True` it is removed from the
        waiters.
        
        Parameters
        ----------
        client : ``Client``
            The cleint, who received the respective dispatch event.
        event : ``GuildUserChunkEvent``
            The received guild user chunk event.
        """
        nonce = event.nonce
        if nonce is None:
            return
        
        waiters = self.waiters
        try:
            waiter = waiters[nonce]
        except KeyError:
            return
        
        if waiter(event):
            del waiters[nonce]


async def default_error_event(client, name, err):
    """
    Defaults error event for client. Renders the given exception to `sys.stderr`.
    
    Parameters
    ----------
    client : ``client``
        The client who caught the error.
    name : `str`
        Identificator name of the palce where the error occured.
    err : `Any`
        The caught exception. Can be given as non `BaseException` instance as well.
    """
    extracted=[
        client.full_name,
        ' ignores occurred Exception at ',
        name,
        '\n'
            ]
    
    if isinstance(err,BaseException):
        await KOKORO.render_exc_async(err,extracted)
        return
    
    if not isinstance(err,str):
        err=repr(err)
    extracted.append(err)
    
    sys.stderr.write(''.join(extracted))

class asynclist(list):
    """
    Container used by parsers to call more events and by waitfor events to call more waiters.
    """
    __slots__ = ('_attribute_cache')
    
    def __init__(self, iterable=None):
        """
        Creates a new asynclist from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
        """
        if (iterable is not None):
            list.extend(self, iterable)
    
    async def __call__(self, *args):
        """
        Ensures the contained async callables on the client's loop.
        
        Parameters
        ----------
        *args : Additional position arguments
            Arguments to call with the contained async callables.
        """
        for coro in self:
            Task(coro(*args), KOKORO)
    
    def __repr__(self):
        """Returns the asynclist's representation."""
        result = [
            self.__class__.__name__,
            '([']
        
        index=0
        limit=len(self)
        if index!=limit:
            while True:
                element=self[index]
                result.append(repr(element))
                if index==limit:
                    break
                
                result.append(', ')
                index=index+1
        
        result.append('])')
        
        return ''.join(result)
        
    def __getattr__(self, name):
        """Gets the given attribute from the elements of the asynclist."""
        if not isinstance(name, str):
            raise TypeError(f'Attribute name must be string, not `{type(name).__name__}`.')
        
        for coro in self:
            attribute = getattr(coro,name,_spaceholder)
            if attribute is _spaceholder:
                continue
            
            return attribute
        
        raise AttributeError(f'`{self.__class__.__name__}` object has no attribte `{name}`.')
    
async def DEFAULT_EVENT(*args):
    """
    Default event handler what is set under events if there is no specified event handler to use.
    
    Parameters
    ----------
    *args : Positional arguments
    """
    pass
    
class EventDescriptor(object):
    """
    After a client gets a dispatch event from Discord, it's parser might ensure an event. These events are stored
    inside of a ``EventDescriptor`` and can be accessed through `client.events`.
    
    Each added event should be an async callable accepting a predifind amount of positional arguments.
    
    Attributes
    ----------
    client_reference : `WeakReferer`
        Weak reference to the parent client to avoid reference loops.
    
    Additonal event Attributes
    ----------------
    channel_create(client: Client, channel: ChannelBase)
        Called when a channel is created.
        
        > At hata wrapper this event is called only the first time when a private (or group) channel is created.
    
    channel_delete(client: Client, channel: ChannelBase)
        Called when a channel is deleted.
    
    channel_edit(client: Client, channel: Channel, old_attributes: dict)
        Called when a channel is edited. The passed `old_attributes` argument contains the channel's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------+---------------------------------------+
        | Keys          | Values                                |
        +===============+=======================================+
        | bitrate       | `int`                                 |
        +---------------+---------------------------------------+
        | category      | ``ChannelCategory`` or ``Guild``      |
        +---------------+---------------------------------------+
        | icon          | ``Icon``                              |
        +---------------+---------------------------------------+
        | name          | `str`                                 |
        +---------------+---------------------------------------+
        | nsfw          | `bool`                                |
        +---------------+---------------------------------------+
        | overwrites    | `list` of ``PermOW``                  |
        +---------------+---------------------------------------+
        | owner         | ``User`` or ``Client``                |
        +---------------+---------------------------------------+
        | position      | `int`                                 |
        +---------------+---------------------------------------+
        | slowmode      | `int`                                 |
        +---------------+---------------------------------------+
        | topic         | `str`                                 |
        +---------------+---------------------------------------+
        | type          | `int`                                 |
        +---------------+---------------------------------------+
        | user_limit    | `int`                                 |
        +---------------+---------------------------------------+
        | users         | `list` of (``User`` or ``Client``)    |
        +---------------+---------------------------------------+
    
    channel_group_user_add(client: Client, channel: ChannelGroup, user: UserBase):
        Called when a user is added to a group channel.
    
    channel_group_user_delete(client: Client, channel: ChanneGroup, user: UserBase):
        Called when a user is removed from a group channel.
    
    channel_pin_update(client: Client, channel: ChannelTextBase):
        Called when a channel's pins are updated.
    
    client_edit(client: Client, old_attributes: dict):
        Called when the client is edited. The passed `old_attributes` argument contains the client's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-----------------------+-------------------+
        | Keys                  | Values            |
        +=======================+===================+
        | avatar                | ``Icon``          |
        +-----------------------+-------------------+
        | discriminator         | `int`             |
        +-----------------------+-------------------+
        | email                 | `str`             |
        +-----------------------+-------------------+
        | flags                 | ``UserFlag``      |
        +-----------------------+-------------------+
        | locale                | `str              |
        +-----------------------+-------------------+
        | mfa                   | `bool`            |
        +-----------------------+-------------------+
        | name                  | `str              |
        +-----------------------+-------------------+
        | premium_type          | ``PremiumType``   |
        +-----------------------+-------------------+
        | verified              | `bool`            |
        +-----------------------+-------------------+
    
    embed_update(client: Client, message: Message, change_state: int):
        Called when a mesasge is not edited, only it's embeds are updated.
        
        Possible `change_state` values:
        
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | EMBED_UPDATE_NONE         | 0     |
        +---------------------------+-------+
        | EMBED_UPDATE_SIZE_UPDATE  | 1     |
        +---------------------------+-------+
        | EMBED_UPDATE_EMBED_ADD    | 2     |
        +---------------------------+-------+
        | EMBED_UPDATE_EMBED_REMOVE | 3     |
        +---------------------------+-------+
        
        > At the case of `EMBED_UPDATE_NONE` the event is of cource not called.
    
    emoji_create(client: Client, emoji: Emoji):
        Called when an emoji is created at a guild.
    
    emoji_delete(client: Client, emoji: Emoji, guild: Guild):
        Called when an emoji is deleted.
        
        > Deleted emoji's `.guild` attribute is set to `None`.
        
    emoji_edit(client : Client, emoji: Emoji, old_attributes: dict):
        Called when an emoji is edited. The passed `old_attributes` argument contains the emoji's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | animated          | `bool`                        |
        +-------------------+-------------------------------+
        | available         | `bool`                        |
        +-------------------+-------------------------------+
        | managed           | `bool`                        |
        +-------------------+-------------------------------+
        | name              | `int`                         |
        +-------------------+-------------------------------+
        | require_colons    | `bool`                        |
        +-------------------+-------------------------------+
        | roles             | `None` or `set` of ``Role``   |
        +-------------------+-------------------------------+
    
    error(client: Client, name: str, err: Any):
        Called when an unexpected error happens. Mostly the user itself should define where it is called, because
        it is not Discord event bound, but an internal event.
        
        The `name` argument should be a `str` what tell where the error occured, and `err` should be a `BaseException`
        instance or an error message (can be other as type `str` as well.)
        
        This event has a default handler called ``default_error_event``, what writes an error message to `sys.stderr`.
    
    gift_update(client: Client, gift: Gift):
        Called when a gift code is sent to a channel.
    
    guild_ban_add(client: Client, guild:Guild, user:UseBase):
        Called when a user is banned from a guild.
    
    guild_ban_delete(client: Client, guild: Guild, user:UseBase):
        Called when a user is unbanned at a guild.
    
    guild_create(client: Client, guild: Guild):
        Called when a client joins or creates a guild.
    
    guild_delete(client: Client, guild: Guild, profile: GuildProfile):
        Called when the guild is deleted or just the client left (kicked or banned as well) from it. The `profile`
        argument is the client's respective guild profile for the guild.
    
    guild_edit(client: Client, guild: Guild, old_attributes: dict):
        Called when a guild is edited. The passed `old_attributes` argument contains the guild's overwritten attributes
        in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------------------+-------------------------------+
        | Keys                      | Values                        |
        +===========================+===============================+
        | afk_channel               | `None` or ``ChannelVoice`     |
        +---------------------------+-------------------------------+
        | afk_timeout               | `int`                         |
        +---------------------------+-------------------------------+
        | available                 | `bool`                        |
        +---------------------------+-------------------------------+
        | banner                    | ``Icon``                      |
        +---------------------------+-------------------------------+
        | booster_count             | `int`                         |
        +---------------------------+-------------------------------+
        | content_filter            | ``ContentFilterLevel``        |
        +---------------------------+-------------------------------+
        | description               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | discovery_splash          | ``Icon``                      |
        +---------------------------+-------------------------------+
        | embed_channel             | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | embed_enabled             | `bool`                        |
        +---------------------------+-------------------------------+
        | features                  | `list` of ``GuildFeature``    |
        +---------------------------+-------------------------------+
        | icon                      | ``Icon``                      |
        +---------------------------+-------------------------------+
        | invite_splash             | ``Icon``                      |
        +---------------------------+-------------------------------+
        | max_presences             | `int`                         |
        +---------------------------+-------------------------------+
        | max_users                 | `int`                         |
        +---------------------------+-------------------------------+
        | max_video_channel_users   | `int`                         |
        +---------------------------+-------------------------------+
        | message_notification      | ``MessageNotificationLevel``  |
        +---------------------------+-------------------------------+
        | mfa                       | ``MFA``                       |
        +---------------------------+-------------------------------+
        | name                      | `str`                         |
        +---------------------------+-------------------------------+
        | owner                     | ``User`` or ``Client``        |
        +---------------------------+-------------------------------+
        | preferred_locale          | `str`                         |
        +---------------------------+-------------------------------+
        | premium_tier              | `int`                         |
        +---------------------------+-------------------------------+
        | public_updates_channel    | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | region                    | ``VoiceRegion``               |
        +---------------------------+-------------------------------+
        | rules_channel             | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | system_channel            | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | system_channel_flags      | ``SystemChannelFlag``         |
        +---------------------------+-------------------------------+
        | vanity_code               | `None` or `str`               |
        +---------------------------+-------------------------------+
        | verification_level        | ``VerificationLevel``         |
        +---------------------------+-------------------------------+
        | widget_channel            | `None` or ``ChannelText``     |
        +---------------------------+-------------------------------+
        | widget_enabled            | `bool`                        |
        +---------------------------+-------------------------------+
    
    guild_user_add(client: Client, guild: Guild, user: UserBase):
        Called when a user jois a guild.
    
    guild_user_chunk(client: Client, event: GuildUserChunkEvent):
        Called when a client receives a chunk of users from Discord requested by through it's gateway.
        
        The event has a default handler called ``ChunkWaiter``.
    
    guild_user_delete(client: Client, guild: Guild, user: UserBase, profile: GuildProfile):
        Called when a user left (kicked or banned counts as well) from a guild. The `profile` argument is the user's
        respective guild profile for the guild.
    
    integration_update(client, Client, guild: Guild):
        Called when an ``Integration`` of a guild is updated.
        
        > No integration data is included with the received dispatch event, so it cannot be passed to the event
        > handler either.
    
    invite_create(client: Client, invite: Invite):
        Called when an invite is created  at a guild.
    
    invite_delete(client: Client, invite: Invite):
        Called when an invite is deleted at a guild.
    
    message_create(client: Client, message: Message):
        Called when a message is sent to any of the client's text channels.
    
    message_delete(client: Client, message: Message):
        Called when a loaded message is deleted.
    
    message_edit(client: Client, message: Message, old_attributes: dict):
        Called when a loaded message is edited. The passed `old_attributes` argument contains the message's overwritten
        attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-----------------------------------------------------------------------+
        | Keys              | Values                                                                |
        +===================+=======================================================================+
        | activity          | `None` or ``MessageActivity``                                         |
        +-------------------+-----------------------------------------------------------------------+
        | application       | `None` or ``MessageApplication``                                      |
        +-------------------+-----------------------------------------------------------------------+
        | attachments       | `None` or (`list` of ``Attachment``)                                  |
        +-------------------+-----------------------------------------------------------------------+
        | content           | `str                                                                  |
        +-------------------+-----------------------------------------------------------------------+
        | cross_mentions    | `None` or (`list` of (``ChannelBase`` or ``UnknownCrossMention``))    |
        +-------------------+-----------------------------------------------------------------------+
        | edited            | `None`  or `datetime`                                                 |
        +-------------------+-----------------------------------------------------------------------+
        | embeds            | `None`  or `(list` of ``EmbedCore``)                                  |
        +-------------------+-----------------------------------------------------------------------+
        | flags             | `UserFlag`                                                            |
        +-------------------+-----------------------------------------------------------------------+
        | mention_everyone  | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | pinned            | `bool`                                                                |
        +-------------------+-----------------------------------------------------------------------+
        | user_mentions     | `None` or (`list` of (``User`` or ``Client``))                        |
        +-------------------+-----------------------------------------------------------------------+
        | role_mentions     | `None` or (`list` of ``Role``)                                        |
        +-------------------+-----------------------------------------------------------------------+
        
        A special case is if a message is (un)pinned or (un)suppressed, because then the `old_attributes` argument is
        not going to contain `edited`, only `pinned` or `flags`. If the embeds are (un)suppressed of the message, then
        `old_attributes` might contain also `embeds`.
    
    reaction_add(client: Client, event: ReactionAddEvent):
        Called when a user reacts on a message with the given emoji.
    
    reaction_clear(client: Client, message: Message, old_reactions: reaction_mapping):
        Called when the reactions of a message are cleared. The passed `old_reactions` argument are the old reactions
        of the message.
    
    reaction_delete(client: Client, event: ReactionDeleteEvent):
        Called when a user removes it's reaction from a message.
    
    reaction_delete_emoji(client: Client, message: Message, users: reaction_mapping_line):
        Called when all the reactions of a specified emoji are removed from a message. The passed `users` argument
        are the old reacter users of the given emoji.
    
    ready(client: Client):
        Called when the client finishes logging in. The event might be called more times, because the clients might
        dis- and reconnect.
    
    relationship_add(client: Client, new_relationship: Relationship):
        Called when the client gets a new relationship independetly from it's type.
    
    relationship_change(client: Client, old_relationship: Relationship, new_relationship: Relationship):
        Called when one of the client's relationships change.
    
    relationship_delete(client: Client, old_relationship: Relationship):
        Called when a relationship of a client is removed.
    
    role_create(client: Client, role: Role):
        Called whne a role is created at a guild.
    
    role_delete(client: Client, role: Role, guild: Guild):
        Called when a role is deleted from a guild.
        
        > Deleted role's `.guild` attrbiute is set as `None`.
    
    typing(client: Client, channel: ChannelTextBase, user: UserBase, timestamp: datetime):
        Called when a user is typing at a channel. The `timestamp` argument represents when the typing started.
        
        > However a typing requests stands for 8 seconds, but the official Discord client usually just spams it.
    
    user_edit(client: Client, user: User, old_attributes: dict):
        Called when a user is edited This event not includes guild profile changes. The passed `old_attributes`
        argument contains the message's overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +---------------+---------------+
        | Keys          | Values        |
        +===============+===============+
        | avatar        | ``Icon``      |
        +---------------+---------------+
        | discriminator | `int          |
        +---------------+---------------+
        | flags         | ``UserFlag``  |
        +---------------+---------------+
        | name          | `str`         |
        +---------------+---------------+
    
    user_presence_update(client: Client, user: UserBase, old_attributes: dict):
        Called when a user's presence is updated.
        
        The passed `old_attributes` argument contain the user's changed presence related attributes in `attribute-name`
        - `old-value` relation. An exception from this is `activities`. If an activity is not removed, but updated, then
        it will show up as an ``ActivityChange`` instance.
        
        +---------------+-------------------------------------------------------+
        | Keys          | Values                                                |
        +===============+=======================================================+
        | activities    | `list` of (``ActivityBase`` or ``ActivityChange``)    |
        +---------------+-------------------------------------------------------+
        | status        | ``Status``                                            |
        +---------------+-------------------------------------------------------+
        | statuses      | `dict` of (`str`, `str`) items                        |
        +---------------+-------------------------------------------------------+
        
    user_profile_edit(client : Client, user: UserBase, guild: Guild, old_attributes: dict):
        Called when a user's ``GuildProfile`` is updated. The passed `old_attributes` argument contains the message's
        overwritten attributes in `attribute-name` - `old-value` relation.
        
        Every item in `old_attributes` is optional and it's items can be any of the following:
        
        +-------------------+-----------------------+
        | Keys              | Values                |
        +===================+=======================+
        | boosts_since      | `None` or `datetime`  |
        +-------------------+-----------------------+
        | nick              | `None` or `str`       |
        +-----------------------+-------------------+
        | roles             | `list` of ``Role``    |
        +-------------------+-----------------------+
    
    voice_state_update(client: Client, state: VoiceState, action: str, old_attributes: Union[None, dict]):
        Called when a voice state is updated inside of a ``ChannelVoice``.
        
        The `action` argument can be any of the following:
        
        +-------------------+-------+
        | Respective name   | Value |
        +===================+=======+
        | leave             | `'l'` |
        +-------------------+-------+
        | join              | `'j`' |
        +-------------------+-------+
        | update            | `'u'` |
        +-------------------+-------+
    
        If `action` is given as `'u'`, then the `old_attributes` argument will be given as a `dict` with the voice
        state's updated attributes within `attribute-name` - `old-attribute` relation.
        
        Every item in `old_attributes` is optional and they can be the following:
        
        +---------------+-------------------+
        | Keys          | Values            |
        +===============+===================+
        | channel       | ``ChannelVoice``  |
        +---------------+-------------------+
        | deaf          | `str`             |
        +---------------+-------------------+
        | mute          | `bool`            |
        +---------------+-------------------+
        | self_deaf     | `bool`            |
        +---------------+-------------------+
        | self_mute     | `bool`            |
        +---------------+-------------------+
        | self_stream   | `bool`            |
        +---------------+-------------------+
        | self_video    | `bool`            |
        +---------------+-------------------+
    
    webhook_update(client: Client, channel: ChannelGuildBase):
        Called when a webhook of a channel is updated. Discord not provides further details tho.
    """
    __slots__=('client_reference',*sorted(EVENTS.defaults))
    
    def __init__(self, client):
        """
        Creates an ``EventDescriptor`` for the given client.
        
        Parameters
        ----------
        client : ``Client``
        """
        client_reference=WeakReferer(client)
        object.__setattr__(self,'client_reference',client_reference)
        for name in EVENTS.defaults:
            object.__setattr__(self,name,DEFAULT_EVENT)
        object.__setattr__(self,'error',default_error_event)
        object.__setattr__(self,'guild_user_chunk',ChunkWaiter())
    
    def __call__(self, func=None, name=None, overwrite=False):
        """
        Adds the given `func` to the event descriptor as en event handler.
        
        Parameters
        ----------
        func : `callable`, Optional
            The async callable to add as an event handler.
        name : `None` or `str`, Optional
            A name to be used instead of the passed `func`'s when adding it.
        overwrite : `bool`, Optional
            Whether the passed `func` should overwrite the already added ones with the same name or extend them.
        
        Returns
        -------
        func : `callable`
            The added callable or ``._wrapper` if `func` was not given.
        
        Raises
        ------
        AttributeError
            Invalid event name.
        TypeError
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional arguments as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """
        if func is None:
            return self._wrapper(self, (name,overwrite))
        
        name=check_name(func,name)
        argcount=EVENTS.get_argcount(name)
        func=check_argcount_and_convert(func,argcount)
        
        if overwrite:
            setattr(self,name,func)
            return func
        
        parser_names=EVENTS.parsers.get(name,None)
        if (parser_names is None):
            raise AttributeError(f'Event name: {name!r} is invalid.')
        
        if func is DEFAULT_EVENT:
            return func
        
        actual=getattr(self,name)
        if actual is DEFAULT_EVENT:
            object.__setattr__(self,name,func)
            for parser_name in parser_names:
                parser_default=PARSER_DEFAULTS.all[parser_name]
                parser_default.add_mention(self.client_reference())
            return func
        
        if type(actual) is asynclist:
            actual.append(func)
            return func
        
        new=asynclist()
        new.append(actual)
        new.append(func)
        object.__setattr__(self,name,new)
        return func
    
    class _wrapper(object):
        """
        When the parent ``EventDescriptor`` is called without passing `func`, then a instance of this class is
        returned to enable using ``EventDescriptor`` as a decorator with passing additional keyword arguments at the
        same time.
        
        Attributes
        ----------
        parent : ``EventDescriptor``
            The owner event descriptor.
        args: `tuple` of `Any`
            Additonal keyword arguments (in order) passed when the wrapper was created.
        """
        __slots__ = ('parent', 'args',)
        def __init__(self, parent, args):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``EventDescriptor``
                The owner event descriptor.
            args: `tuple` of `Any`
                Additonal keyword arguments (in order) passed when the wrapper was created.
            """
            self.parent = parent
            self.args = args
        
        def __call__(self, func):
            """
            Adds the given `func` to the parent event handler with the stored up arguments.
            
            Parameters
            ----------
            func : `callable`
                The event handler to add to the event descriptor.
            
            Returns
            -------
            func : `callable`
                The added callable.
            
            Raises
            ------
            AttributeError
                Invalid event name.
            TypeError
                - If `func` was not given as callable.
                - If `func` is not as async and neither cannot be converted to an async one.
                - If `func` expects less or more non reserved positional arguments as `expected` is.
                - If `name` was not passed as `None` or type `str`.
            """
            return self.parent(func, *self.args)
    
    def clear(self):
        """
        Cleares the ``EventDescriptor`` to the same state as it were just created.
        """
        delete=type(self).__delattr__
        for name in EVENTS.defaults:
            delete(self,name)
            
        object.__setattr__(self,'error',default_error_event)
        object.__setattr__(self,'guild_user_chunk',ChunkWaiter())
    
    def __setattr__(self, name, value):
        """
        Sets the given event handler under the speciifed event name. Updates the respective event's parser(s) if needed.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        value : `callable`
            The event handler.
        
        Raises
        ------
        AttributeError
            The ``EventDescriptor`` has no attribute named as the given `name`.
        """
        parser_names=EVENTS.parsers.get(name,None)
        if (parser_names is None):
            object.__setattr__(self,name,value)
            return
        
        for parser_name in parser_names:
            parser_default=PARSER_DEFAULTS.all[parser_name]
            actual=getattr(self,name)
            object.__setattr__(self,name,value)
            if actual is DEFAULT_EVENT:
                if value is DEFAULT_EVENT:
                    continue
                
                parser_default.add_mention(self.client_reference())
                continue
            
            if value is DEFAULT_EVENT:
                parser_default.remove_mention(self.client_reference())
            continue
    
    def __delattr__(self, name):
        """
        Removes the event with switching it to `DEFAULT_EVENT`, and updates the event's parser if needed.
        
        Parameters
        ----------
        name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            The ``EventDescriptor`` has no attribute named as the given `name`.
        """
        actual=getattr(self, name)
        if actual is DEFAULT_EVENT:
            return
        
        object.__setattr__(self,name,DEFAULT_EVENT)
        
        parser_names=EVENTS.parsers.get(name,None)
        if (parser_names is None) or (not parser_names):
            # parser name can be an empty string as well for internal events
            return
        
        for parser_name in parser_names:
            parser_default=PARSER_DEFAULTS.all[parser_name]
            parser_default.remove_mention(self.client_reference())
    
    def remove(self, func, name=None, by_type=False, count=-1):
        """
        Removes the given event handler from the the event descriptor.
        
        Parameters
        ----------
        func : `Any`
            The event handler to remove.
        name : `str`, Optional
            The event's name.
        by_type : `bool`, Optional
            Whether `func` was given as the type of the real event handler. Defaults to `False`.
        count : `int`, Optional
            The maximal amount of the same events to remove. Negative numbers count as unlimited. Defaults to `-1`.
        """
        if count==0 or name=='client':
            return
        
        name=check_name(func,name)
        
        try:
            actual=getattr(self,name)
        except AttributeError:
            return
        
        if actual is DEFAULT_EVENT:
            return
        
        if type(actual) is asynclist:
            for index in reversed(range(len(asynclist))):
                element = actual[index]
                if by_type:
                    element = type(element)
                
                if element != func:
                    continue
                
                del actual[index]
                count = count-1
                if count==0:
                    break
                
                continue
            
            if len(actual)>1:
                return
            
            if len(actual)==0:
                actual=actual[0]
                object.__setattr__(self,name,actual)
                return
        
        else:
            if by_type:
                actual = type(actual)
            
            if actual != func:
                return
        
        object.__setattr__(self,name,DEFAULT_EVENT)
        
        parser_names=EVENTS.parsers.get(name,None)
        if (parser_names is None):
            return
        
        for parser_name in parser_names:
            parser_default=PARSER_DEFAULTS.all[parser_name]
            parser_default.remove_mention(self.client_reference())
        return

async def _with_error(client, task):
    """
    Runs the given awaitable and if it raises, calls `client.events.error` with the exception.
    
    Parameters
    ----------
    client : ``Client``
        The client, who's `client.events.error` will be called.
    task : `awaitable`
        The awaitable to run.
    """
    try:
        await task
    except BaseException as err:
        await client.events.error(client,repr(task),err)

del RemovedDescriptor
del datetime
del FlagBase
del NEEDS_DUMMY_INIT
