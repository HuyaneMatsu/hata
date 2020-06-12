# -*- coding: utf-8 -*-
__all__ = ('eventlist', 'EventHandlerBase', 'EventWaitforBase', 'IntentFlag', )

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
from .exceptions import DiscordException
from .invite import Invite

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
        Single client optimalized parser.
    opt_mc : `function`
        Multy client optimalized parsers.
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
    def __init__(self,name,cal_sc,cal_mc,opt_sc,opt_mc):
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
    def register(cls,client):
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
    def unregister(cls,client):
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
    
    def add_mention(self,client):
        if client is None:
            return
        
        if client not in self.registered:
            return
        self.mention_count+=1
        self._recalculate()
    
    def remove_mention(self,client):
        if client is None:
            return
        
        if client not in self.registered:
            return
        self.mention_count-=1
        self._recalculate()
        
    def _recalculate(self):
        mention_count=self.mention_count
        client_count=self.client_count
        
        if mention_count==0:
            if client_count<2:
                parser=self.opt_sc
            else:
                parser=self.opt_mc
        else:
            if client_count<2:
                parser=self.cal_sc
            else:
                parser=self.cal_mc
        
        PARSERS[self.name]=parser

SYNC_REQUESTS={}

async def sync_task(queue_id,coro,queue):
    try:
        guild = await coro
    except DiscordException:
        return
    finally:
        del SYNC_REQUESTS[queue_id]

    for client,data,parser_and_checker in queue:
        if type(parser_and_checker) is str:
            PARSERS[parser_and_checker](client,data)
            continue

        parser_name,checker,value=parser_and_checker
        if checker(guild,value):
            PARSERS[parser_name](client,data)

def check_channel(guild,channel_id):
    return (channel_id in guild.all_channel)

def guild_sync(client,data,parser_and_checker):
    try:
        guild_id=int(data['guild_id'])
    except KeyError:
        return
    
    try:
        queue=SYNC_REQUESTS[guild_id]
    except KeyError:
        queue=[]
        Task(sync_task(guild_id,client.guild_sync(guild_id),queue), KOKORO)
        SYNC_REQUESTS[guild_id]=queue
    
    if parser_and_checker is None:
        return
    queue.append((client,data,parser_and_checker),)

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
    old=client._update(data)
    if not old:
        return
    
    Task(client.events.client_edit(client,old), KOKORO)

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
        old=message._update(data)
        if not old:
            return
        
        Task(client.events.message_edit(client,message,old), KOKORO)
    else:
        result=message._update_embed(data)
        if not result:
            return
        
        Task(client.events.embed_update(client,message,result), KOKORO)

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
        old=message._update(data)
        if not old:
            return
        
        for client_ in clients:
            Task(client_.events.message_edit(client_,message,old), KOKORO)
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

def MESSAGE_REACTION_ADD__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)
    
    Task(client.events.reaction_add(client,message,emoji,user), KOKORO)

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
    
    for client_ in clients:
        Task(client_.events.reaction_add(client_,message,emoji,user), KOKORO)

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

def MESSAGE_REACTION_REMOVE__CAL_SC(client,data):
    message_id=int(data['message_id'])
    message=MESSAGES.get(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)
    
    Task(client.events.reaction_delete(client,message,emoji,user), KOKORO)

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
    
    for client_ in clients:
        Task(client_.events.reaction_delete(client_,message,emoji,user),KOKORO)

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
                old=user._update(user_data)
                if old:
                    presence=False
                    break
            
            old=user._update_presence(data)
            if old:
                presence=True
                break
            
            return
        
        if presence:
            coro=client.events.user_presence_update
        else:
            coro=client.events.user_edit
        
        Task(coro(client,user,old), KOKORO)
    
    def PRESENCE_UPDATE__CAL_MC(client,data):
        user_data=data['user']
        user_id=int(user_data.pop('id'))
        try:
            user=USERS[user_id]
        except KeyError:
            return #pretty much we dont care 
        
        while True:
            if user_data:
                old=user._update(user_data)
                if old:
                    presence=False
                    break
                
            old=user._update_presence(data)
            if old:
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
            
            Task(coro(client_,user,old),KOKORO)
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
        
        user,old=User._update_profile(data,guild)
        
        if not old:
            return
        
        Task(client.events.user_profile_edit(client,user,old,guild), KOKORO)

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
        
        user,old=User._update_profile(data,guild)
        
        if not old:
            return
        
        clients.send(user)
        for client_ in clients:
            Task(client_.events.user_profile_edit(client_,user,old,guild),KOKORO)
    
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
        
        old=client._update_profile_only(data,guild)
        
        if not old:
            return
        
        Task(client.events.user_profile_edit(client,client,old,guild), KOKORO)

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
    
    old=channel._update(data)
    if not old:
        return
    
    Task(client.events.channel_edit(client,channel,old), KOKORO)

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
    
    old=channel._update(data)
    if not old:
        return
    
    for client_ in clients:
        Task(client_.events.channel_edit(client_,channel,old),KOKORO)

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
    
    for action, emoji, old in changes:
        if action==EMOJI_UPDATE_EDIT:
            coro=client.events.emoji_edit
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,emoji,old), KOKORO)
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
        for action, emoji, old in changes:
            if action==EMOJI_UPDATE_EDIT:
                coro=client_.events.emoji_edit
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji,old),KOKORO)
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
    
    old=guild._update(data)
    if not old:
        return
    
    Task(client.events.guild_edit(client,guild,old), KOKORO)

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
    
    old=guild._update(data)
    if not old:
        return
    
    for client_ in clients:
        Task(client_.events.guild_edit(client_,guild,old),KOKORO)

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

class GuildUserChunkEvent(object):
    __slots__ = ('guild', 'users', 'nonce', 'index', 'count')
    
    def __repr__(self):
        return f'<{self.__class__.__name__} guild={self.guild}, users={len(self.users)}, nonce={self.nonce!r}, index={self.index}, count={self.count}>'

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
        
        event = GuildUserChunkEvent()
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
        
        event = GuildUserChunkEvent()
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
    
    old=role._update(data['role'])
    if not old:
        return
    
    Task(client.events.role_edit(client,role,old), KOKORO)

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
    
    old=role._update(data['role'])
    if not old:
        return
    
    for client_ in clients:
        Task(client_.events.role_edit(client_,role,old),KOKORO)

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

#hooman only event, needs futher testing, there is no real documentation on this
def USER_ACHIEVEMENT_UPDATE__CAL(client,data):
    Task(client.events.achievement(client,data), KOKORO)

def USER_ACHIEVEMENT_UPDATE__OPT(client,data):
    pass

PARSER_DEFAULTS('USER_ACHIEVEMENT_UPDATE',USER_ACHIEVEMENT_UPDATE__CAL,USER_ACHIEVEMENT_UPDATE__CAL,USER_ACHIEVEMENT_UPDATE__OPT,USER_ACHIEVEMENT_UPDATE__OPT)
del USER_ACHIEVEMENT_UPDATE__CAL, USER_ACHIEVEMENT_UPDATE__OPT

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
EVENTS.add_default('reaction_add'               , 4 , 'MESSAGE_REACTION_ADD'                    , )
EVENTS.add_default('reaction_clear'             , 3 , 'MESSAGE_REACTION_REMOVE_ALL'             , )
EVENTS.add_default('reaction_delete'            , 4 , 'MESSAGE_REACTION_REMOVE'                 , )
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
EVENTS.add_default('achievement'                , 2 , 'USER_ACHIEVEMENT_UPDATE'                 , )

def _check_name_should_break(name):
    if (name is None):
        return False
        
    if type(name) is not str:
        raise TypeError(f'`name` should be type `str`, got `{name!r}`.')
        
    if name:
        return True
    
    return False
    
def check_name(func,name):
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
        
        raise TypeError('The class must have \'__name__\' attribute and metaclasses are not allowed')
    
    if not name.islower():
        name=name.lower()
    return name

def check_argcount_and_convert(func, expected, errormsg=None):
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async():
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_>expected:
            raise ValueError(f'`{func!r}` excepts at least `{min_!r}` non reserved arguments, meanwhile the event expects to pass `{expected!r}`.')
        
        if min_==expected:
            return func
        
        #min<expected
        if max_>=expected:
            return func
        
        if analyzer.accepts_args():
            return func
        
        raise ValueError(f'`{func!r}` expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects to pass `{expected!r}`.')
    
    if analyzer.can_instance_to_async_callable():
        sub_analyzer=CallableAnalyzer(func.__call__, as_method=True)
        if sub_analyzer.is_async():
            min_, max_ = sub_analyzer.get_non_reserved_positional_argument_range()
            
            if min_>expected:
                raise ValueError(f'After instancing `{func!r}` would still except at least `{min_!r}` non reserved arguments, meanwhile the event expects to pass `{expected!r}`.')
            
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
            
            raise ValueError(f'After instancing `{func!r}` would still expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects to pass `{expected!r}`.')
            
            func = analyzer.instance_to_async_callable()
            return func
    
    if errormsg is None:
        errormsg=f'Not async callable type, or cannot be instance to async: `{func!r}`.'
    
    raise ValueError(errormsg)

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

def _convert_unsafe_event_iterable(iterable,type_=None):
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
                element = EventListElement(element,name,kwargs)
            else:
                element = type_.from_kwargs(element,name,kwargs)
            
        result.append(element)
        continue
        
    return result

class _EventCreationManager(object):
    __slots__=('parent', '_supports_from_class')
    
    def __init__(self,parent):
        self.parent=parent
        self._supports_from_class = hasattr(type(parent),'__setevent_from_class__')
        
    def __repr__(self):
        return f'<{self.__class__.__name__} of {self.parent!r}>'
    
    def __call__(self,func=None,name=None,**kwargs):
        if func is None:
            return self._wrapper(self,name,kwargs)
        
        name=check_name(func,name)
        
        func=self.parent.__setevent__(func,name,**kwargs)
        return func
    
    def from_class(self,klass):
        if not self._supports_from_class:
            raise TypeError(f'`.from_class` is not supported by `{self.parent!r}`.')
        
        return self.parent.__setevent_from_class__(klass)
        
    def remove(self,func,name=None,**kwargs):
        name=check_name(func,name)
        
        self.parent.__delevent__(func,name,**kwargs)
    
    class _wrapper(object):
        __slots__=('parent', 'name', 'kwargs')
        def __init__(self,parent,name,kwargs):
            self.parent=parent
            self.name=name
            self.kwargs=kwargs
        
        def __call__(self,func,):
            return self.parent(func,self.name,**self.kwargs)
    
    def __getattr__(self,name):
        return getattr(self.parent,name)
    
    def extend(self,iterable):
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
    
    def unextend(self,iterable):
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
        When a parent ``eventlist`` is called and `func` was not passed (so only keyword arguments were), if any, then
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
            Calling an ``eventlist``'s wrapper enables to add the given `func` to be added to the parent ``eventlist``.
            
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
    __slots__=()
    
    # subclasses should overwrite it
    async def __call__(self, *args):
        return

    # subclasses should overwrite it
    def __setevent__(self, func, name):
        pass

    # subclasses should overwrite it
    def __delevent__(self, func, name):
        pass

    @property
    def shortcut(self):
        return _EventCreationManager(self)

class EventWaitforMeta(type):
    def __call__(cls, *args, **kwargs):
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
    
    async def _call_message_edit(self, client, message, old):
        args = (client, message, old)
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
    
    async def _call_channel_edit(self, client, channel, old):
        args = (client, channel, old)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, old)
    
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
    
    async def _call_role_edit(self, client, role, old):
        args = (client, role, old)
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
    
    async def _call_guild_edit(self, client, guild, old):
        args = (client, guild, old)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_edit'] = _call_guild_edit
    del _call_guild_edit
    
    async def _call_emoji_create(self, client, emoji):
        args = (client, emoji)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_create'] = _call_emoji_create
    del _call_emoji_create
    
    async def _call_emoji_edit(self, client, emoji, old):
        args = (client, emoji, old)
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
    
    async def _call_reaction_add(self, client, message, emoji, user):
        args = (client, message, emoji, user)
        self._run_waitfors_for(message, args)
    
    _call_waitfors['reaction_add'] = _call_reaction_add
    del _call_reaction_add
    
    async def _call_reaction_delete(self, client, message, emoji, user):
        args = (client, message, emoji, user)
        self._run_waitfors_for(message, args)
    
    _call_waitfors['reaction_delete'] = _call_reaction_delete
    del _call_reaction_delete

class EventWaitforBase(EventHandlerBase, metaclass=EventWaitforMeta):
    __slots__ = ('waitfors', )
    __event_name__ = None
    call_waitfors = None
    
    def append(self, target, waiter):
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
    
    def remove(self, target, waiter,):
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
    
    def _run_waitfors_for(self, key, args):
        try:
            event=self.waitfors[key]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(event(*args), KOKORO)
            else:
                Task(event(*args), KOKORO)
        
def EventWaitforMeta__new__(cls, class_name, class_bases, class_dict):
    for base in class_bases:
        if issubclass(base,EventWaitforBase):
            break
    else:
        raise TypeError(f'`{cls.__name__} should be only the metaclass of `{EventWaitforBase.__name__}`.')
    
    event_name = class_dict.get('__event_name__')
    if event_name is None:
        event_name = class_name
    
    if event_name not in EVENTS.parsers:
        raise ValueError(f'`{class_name}.__event_name__` is not set, or not set correctly.')
    
    if (class_dict.get('call_waitfors') is None):
        try:
            call_waitfors = cls._call_waitfors[event_name]
        except KeyError:
            raise TypeError(f'The following event name: `{event_name!r}` has no auto `call_waitfor` added. Please define one.')
        
        class_dict['call_waitfors'] = call_waitfors
        
        try:
            call = class_dict.get('__call__')
        except KeyError:
            call = None
        
        if (call is None) or (call is EventHandlerBase.__call__):
            class_dict['__call__'] = call_waitfors
    
    return type.__new__(cls, class_name, class_bases, class_dict)

EventWaitforMeta.__new__  = EventWaitforMeta__new__
del EventWaitforMeta__new__

class ReadyState(object):
    __slots__=('counter', 'guilds', 'last_guild', 'last_ready', 'waiter', )
    def __init__(self,client,guild_datas):
        self.waiter     = Future(KOKORO)
        self.guilds     = []
        self.counter    = guild_datas.__len__()
        now=monotonic()
        self.last_guild = now
        if client.shard_count<2:
            now=now-1.0
        self.last_ready = now
    
    def shard_ready(self,guild_datas):
        self.last_ready = monotonic()
        self.counter   += guild_datas.__len__()
        
    if CACHE_PRESENCE:
        def feed(self,guild):
            if guild.is_large:
                self.guilds.append(guild)
            
            counter=self.counter=self.counter+1
            if counter:
                self.last_guild=monotonic()
                return
            
            last_ready=self.last_ready
            self.last_guild=last_ready
            waiter=self.waiter
            waiter._loop.call_at(last_ready+1.0,waiter.__class__.set_result_if_pending,waiter,None)
    
    elif CACHE_USER:
        def feed(self,guild):
            self.guilds.append(guild)
            
            counter=self.counter=self.counter+1
            if counter:
                self.last_guild=monotonic()
                return
            
            last_ready=self.last_ready
            self.last_guild=last_ready
            waiter=self.waiter
            waiter._loop.call_at(last_ready+1.0,waiter.__class__.set_result_if_pending,waiter,None)
                
    else:
        def feed(self,guild):
            counter=self.counter=self.counter+1
            if counter:
                self.last_guild=monotonic()
                return
            
            last_ready=self.last_ready
            self.last_guild=last_ready
            waiter=self.waiter
            waiter._loop.call_at(last_ready+1.0,waiter.__class__.set_result_if_pending,waiter,None)
    
    def __iter__(self):
        waiter=self.waiter
        last_guild=self.last_guild
        
        while True:
            
            waiter._loop.call_at(last_guild+1.0,waiter.__class__.set_result_if_pending,waiter,None)
            yield from waiter
            waiter.clear()
            
            new_guild=self.last_guild
            if new_guild>last_guild:
                last_guild=new_guild
                continue
            
            break
    
    __await__=__iter__


class ChunkWaiter(EventHandlerBase):
    __slots__=('waiters',)
    __event_name__='guild_user_chunk'
    def __init__(self):
        self.waiters={}
    
    # Interact directly with `self.waiters` instead.
    def __setevent__(self, waiter, nonce):
        pass
    
    def __delevent__(self, waiter, nonce):
        pass
    
    async def __call__(self, client, event):
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


async def default_error_event(client,event_name,err):
    extracted=[
        client.full_name,
        ' ignores occurred Exception at ',
        event_name,
        '\n'
            ]
    
    if isinstance(err,BaseException):
        await KOKORO.render_exc_async(err,extracted)
        return
    
    if type(err) is str:
        extracted.append(err)
    else:
        extracted.append(err.__repr__())
    
    sys.stderr.write(''.join(extracted))

class asynclist(list):
    __slots__ = ('_attribute_cache')
    
    def __init__(self,iterable=None):
        self._attribute_cache={}
        if iterable is not None:
            list.extend(self,iterable)
    
    async def __call__(self,*args):
        for coro in self:
            Task(coro(*args), KOKORO)
    
    def __repr__(self):
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
        if not isinstance(name,str):
            raise TypeError(f'attribute name must be string, not `{type(name).__name__}`')
        
        attribute = self._attribute_cache.get(name,_spaceholder)
        if attribute is not _spaceholder:
            return attribute
        
        for coro in self:
            attribute = getattr(coro,name,_spaceholder)
            if attribute is _spaceholder:
                continue
            
            self._attribute_cache[name]=attribute
            return attribute
        
        raise AttributeError(f'`{self.__class__.__name__}` object has no attribte `{name}`')
    
    def __delitem__(self,index):
        list.__delitem__(self,index)
        self._attribute_cache.clear()
    
    def clear(self):
        list.clear(self)
        self._attribute_cache.clear()
    
    def append(self,object_):
        list.append(self,object_)
        self._attribute_cache.clear()
    
    def extend(self,iterable):
        self._attribute_cache.clear()
        list.extend(self,iterable)
    
    def insert(self,index,object_):
        list.insert(self,index,object_)
        self._attribute_cache.clear()
    
async def DEFAULT_EVENT(*args):
    pass
    
class EventDescriptor(object):
    __slots__=('client_reference',*sorted(EVENTS.defaults))
    
    def __init__(self,client):
        client_reference=WeakReferer(client)
        object.__setattr__(self,'client_reference',client_reference)
        for name in EVENTS.defaults:
            object.__setattr__(self,name,DEFAULT_EVENT)
        object.__setattr__(self,'error',default_error_event)
        object.__setattr__(self,'guild_user_chunk',ChunkWaiter())
    
    def __call__(self,func=None,name=None,pass_to_handler=False,passed_name=None,overwrite=False):
        if func is None:
            return self._wrapper(self,(name,pass_to_handler,passed_name),)
        
        if pass_to_handler:
            if name is None:
                raise ValueError('\'name\' can not be None if `pass_to_handler` is set to True')
            
            if passed_name is None:
                passed_name=check_name(func,None)
            
            if (not passed_name.islower()):
                passed_name=passed_name.lower()
            
            event_handler=getattr(self,name)
            func=event_handler.__setevent__(func,passed_name)
            return func
        
        name=check_name(func,name)
        argcount=EVENTS.get_argcount(name)
        func=check_argcount_and_convert(func,argcount)
        
        if overwrite:
            setattr(self,name,func)
            return func
        
        parser_names=EVENTS.parsers.get(name,None)
        if (parser_names is None):
            raise AttributeError(f'Event name: \'{name}\' is invalid')
        
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
        __slots__=('parent', 'args',)
        def __init__(self,parent,args):
            self.parent=parent
            self.args=args
        def __call__(self,func):
            return self.parent(func,*self.args)

    def clear(self):
        delete=type(self).__delattr__
        for name in EVENTS.defaults:
            delete(self,name)
            
        object.__setattr__(self,'error',default_error_event)
        object.__setattr__(self,'guild_user_chunk',ChunkWaiter())
    
    def __setattr__(self,name,value):
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
    
    def __delattr__(self,name):
        actual=getattr(self,name)
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
        if count==0:
            return
        
        name=check_name(func,name)
        
        actual=getattr(self,name)
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

async def _with_error(client,task):
    try:
        await task
    except BaseException as err:
        await client.events.error(client,repr(task),err)

del RemovedDescriptor
del datetime
del FlagBase
del NEEDS_DUMMY_INIT
