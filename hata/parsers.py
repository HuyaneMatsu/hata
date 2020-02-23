# -*- coding: utf-8 -*-
__all__ = ('eventlist', 'IntentFlag', )

import sys, datetime
from time import monotonic
from weakref import WeakSet, ref as Weakreferer

from .futures import Future, Task, iscoroutinefunction as iscoro
from .dereaddons_local import function, remove, removemeta, _spaceholder,   \
    MethodLike

from .client_core import CACHE_USER, CACHE_PRESENCE, CLIENTS
from .user import User, PartialUser,USERS
from .channel import CHANNEL_TYPES, CHANNELS, ChannelGuildBase
from .others import Relationship, Gift
from .guild import Guild, GUILDS, EMOJI_UPDATE_NEW, EMOJI_UPDATE_DELETE,    \
    EMOJI_UPDATE_EDIT
from .message import Message
from .emoji import PartialEmoji
from .role import Role
from .exceptions import DiscordException
from .invite import Invite

utcfromtimestamp=datetime.datetime.utcfromtimestamp

class event_system_core(object):
    __slots__=('defaults', 'parsers',)
    def __init__(self):
        self.defaults={}
        self.parsers={}
    def add_default(self,name,value,parser):
        self.defaults[name]=value
        self.parsers[name]=parser

    def get_argcount(self,name):
        try:
            value=self.defaults[name]
        except KeyError:
            raise LookupError(f'Invalid Event name: `{name!r}`.') from None
        return value


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


INTENT_KEYS = {
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


INTENT_EVENTS = {
    INTENT_GUILDS : (
        'GUILD_CREATE',
        'GUILD_DELETE',
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

class IntentFlag(int):
    __slots__ = ()
    
    def __new__(cls,int_):
        if not isinstance(int_,int):
            raise TypeError(f'{cls.__name__} expected `int` instance, got `{int_!r}')
        
        new=0
        if int_ < 0:
            for value in INTENT_KEYS.values():
                new = new|(1<<value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                new = new^(1<<INTENT_GUILD_PRESENCES)
        else:
            for value in INTENT_KEYS.values():
                if (int_>>value)&1:
                    new = new|(1<<value)
            
            # If presence cache is disabled, disable presence updates
            if not CACHE_PRESENCE:
                if (new>>INTENT_GUILD_PRESENCES)&1:
                    new = new^(1<<INTENT_GUILD_PRESENCES)
        
        return int.__new__(cls,new)
    
    def iterate_parser_names(self):
        for position in INTENT_KEYS.values():
            if (self>>position)&1:
                yield from INTENT_EVENTS[position]
            
        yield from GLOBAL_INTENT_EVENTS
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self!s})'
    
    def __getitem__(self,key):
        return (self>>INTENT_KEYS[key])&1
    
    def keys(self):
        for key,position in INTENT_KEYS.items():
            if (self>>position)&1:
                yield key
    
    __iter__=keys
    
    def values(self):
        for position in INTENT_KEYS.values():
            if (self>>position)&1:
                yield position
    
    def items(self):
        for key,index in INTENT_KEYS.items():
            yield key,(self>>index)&1
    
    def __contains__(self,key):
        try:
            position=INTENT_KEYS[key]
        except KeyError:
            return 0
        return (self>>position)&1
    
    # Allows you to update more with 1 call
    def update_by_keys(self,**kwargs):
        new=self
        for key,value in kwargs.items():
            try:
                position=INTENT_KEYS[key]
            except KeyError as err:
                err.args=(f'Invalid key:\'{key}\'',)
                raise

            if value:
                new=new|(1<<position)
            else:
                new=new&(0b11111111111111111111111111111111^(1<<position))
        
        return int.__new__(type(self),new)
    
    
    @property
    def receives_guilds(self):
        return (self>>INTENT_GUILDS)&1
    
    def deny_guilds(self):
        if (self>>INTENT_GUILDS)&1:
            self = type(self)(self^(1<<INTENT_GUILDS))
        return self
    
    def allow_guilds(self):
        return type(self)(self|(1<<INTENT_GUILDS))
    
    
    @property
    def receives_guild_users(self):
        return (self>>INTENT_GUILD_USERS)&1
    
    def deny_guild_users(self):
        if (self>>INTENT_GUILD_USERS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_USERS))
        return self
    
    def allow_guild_users(self):
        return type(self)(self|(1<<INTENT_GUILDS))
    
    
    @property
    def receives_guild_bans(self):
        return (self>>INTENT_GUILD_BANS)&1
    
    def deny_guild_bans(self):
        if (self>>INTENT_GUILD_BANS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_BANS))
        return self
    
    def allow_guild_bans(self):
        return type(self)(self|(1<<INTENT_GUILD_BANS))
    
    
    @property
    def receives_guild_emojis(self):
        return (self>>INTENT_GUILD_EMOJIS)&1
    
    def deny_guild_emojis(self):
        if (self>>INTENT_GUILD_EMOJIS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_EMOJIS))
        return self
    
    def allow_guild_emojis(self):
        return type(self)(self|(1<<INTENT_GUILD_EMOJIS))
    
    
    @property
    def receives_guild_integrations(self):
        return (self>>INTENT_GUILD_INTEGRATIONS)&1
    
    def deny_guild_integrations(self):
        if (self>>INTENT_GUILD_INTEGRATIONS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_INTEGRATIONS))
        return self
    
    def allow_guild_integrations(self):
        return type(self)(self|(1<<INTENT_GUILD_INTEGRATIONS))
    
    
    @property
    def receives_guild_webhooks(self):
        return (self>>INTENT_GUILD_WEBHOOKS)&1
    
    def deny_guild_webhooks(self):
        if (self>>INTENT_GUILD_WEBHOOKS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_WEBHOOKS))
        return self
    
    def allow_guild_webhooks(self):
        return type(self)(self|(1<<INTENT_GUILD_WEBHOOKS))
    
    
    @property
    def receives_guild_invites(self):
        return (self>>INTENT_GUILD_INVITES)&1
    
    def deny_guild_invites(self):
        if (self>>INTENT_GUILD_INVITES)&1:
            self = type(self)(self^(1<<INTENT_GUILD_INVITES))
        return self
    
    def allow_guild_invites(self):
        return type(self)(self|(1<<INTENT_GUILD_INVITES))
    
    
    @property
    def receives_guild_voice_states(self):
        return (self>>INTENT_GUILD_VOICE_STATES)&1
    
    def deny_guild_voice_states(self):
        if (self>>INTENT_GUILD_VOICE_STATES)&1:
            self = type(self)(self^(1<<INTENT_GUILD_VOICE_STATES))
        return self
    
    def allow_guild_voice_states(self):
        return type(self)(self|(1<<INTENT_GUILD_VOICE_STATES))
    
    
    @property
    def receives_guild_presences(self):
        return (self>>INTENT_GUILD_PRESENCES)&1
    
    def deny_guild_presences(self):
        if (self>>INTENT_GUILD_PRESENCES)&1:
            self = type(self)(self^(1<<INTENT_GUILD_PRESENCES))
        return self
    
    def allow_guild_presences(self):
        return type(self)(self|(1<<INTENT_GUILD_PRESENCES))
    
    
    @property
    def receives_guild_messages(self):
        return (self>>INTENT_GUILD_MESSAGES)&1
    
    def deny_guild_messages(self):
        if (self>>INTENT_GUILD_MESSAGES)&1:
            self = type(self)(self^(1<<INTENT_GUILD_MESSAGES))
        return self
    
    def allow_guild_messages(self):
        return type(self)(self|(1<<INTENT_GUILD_MESSAGES))
    
    
    @property
    def receives_guild_reactions(self):
        return (self>>INTENT_GUILD_REACTIONS)&1
    
    def deny_guild_reactions(self):
        if (self>>INTENT_GUILD_REACTIONS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_REACTIONS))
        return self
    
    def allow_guild_reactions(self):
        return type(self)(self|(1<<INTENT_GUILD_REACTIONS))
    
    
    @property
    def receives_guild_typings(self):
        return (self>>INTENT_GUILD_TYPINGS)&1
    
    def deny_guild_typings(self):
        if (self>>INTENT_GUILD_TYPINGS)&1:
            self = type(self)(self^(1<<INTENT_GUILD_TYPINGS))
        return self
    
    def allow_guild_typings(self):
        return type(self)(self|(1<<INTENT_GUILD_TYPINGS))
    
    
    @property
    def receives_direct_messages(self):
        return (self>>INTENT_DIRECT_MESSAGES)&1
    
    def deny_direct_messages(self):
        if (self>>INTENT_DIRECT_MESSAGES)&1:
            self = type(self)(self^(1<<INTENT_DIRECT_MESSAGES))
        return self
    
    def allow_direct_messages(self):
        return type(self)(self|(1<<INTENT_DIRECT_MESSAGES))
    
    
    @property
    def receives_direct_reactions(self):
        return (self>>INTENT_DIRECT_REACTIONS)&1
    
    def deny_direct_reactions(self):
        if (self>>INTENT_DIRECT_REACTIONS)&1:
            self = type(self)(self^(1<<INTENT_DIRECT_REACTIONS))
        return self
    
    def allow_direct_reactions(self):
        return type(self)(self|(1<<INTENT_DIRECT_REACTIONS))
    
    
    @property
    def receives_direct_typings(self):
        return (self>>INTENT_DIRECT_TYPINGS)&1
    
    def deny_direct_typings(self):
        if (self>>INTENT_DIRECT_TYPINGS)&1:
            self = type(self)(self^(1<<INTENT_DIRECT_TYPINGS))
        return self
    
    def allow_direct_typings(self):
        return type(self)(self|(1<<INTENT_DIRECT_TYPINGS))


def filter_clients(clients,flag):
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            yield None
            return
        
        client=clients[index]
        if (client.intents>>flag)&1:
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
        if (client.intents>>flag)&1:
            yield client
        
        index=index+1
        continue

def first_client(clients,flag):
    index=0
    limit=len(clients)
    
    while True:
        if index==limit:
            return None
        
        client=clients[index]
        if (client.intents>>flag)&1:
            return client
            break
        
        index=index+1
        continue

PARSERS={}

class PARSER_DEFAULTS(object):
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
            
            parser_name = EVENTS.parsers[event_name]
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
            
            parser_name = EVENTS.parsers[event_name]
            if parser_name not in enabled_parsers:
                continue
            
            parser_default=cls.all[parser_name]
            parser_default.mention_count-=1
            parser_default._recalculate()
    
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
        Task(sync_task(guild_id,client.guild_sync(guild_id),queue),client.loop)
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
        Task(client._delay_ready(),client.loop)
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
            Relationship(client,PartialUser(int(relationship_data['id'])),relationship_data)
    
    try:
        channel_private_datas=data['private_channels']
    except KeyError:
        pass
    else:
        for channel_private_data in channel_private_datas:
            CHANNEL_TYPES[channel_private_data['type']](channel_private_data,client)
    
    try:
        settings_data=data['user_settings']
    except KeyError:
        pass
    else:
        if settings_data:
            client.settings._update_no_return(settings_data)
    
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
    
    Task(client.events.client_edit(client,old),client.loop)

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

    message=Message.new(data,channel)
    
    Task(client.events.message_create(client,message),client.loop)

def MESSAGE_CREATE__OPT(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('MESSAGE_CREATE',check_channel,channel_id))
        return
    
    Message.new(data,channel)

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
    message=channel._mc_pop(message_id)
    if message is None:
        return
    
    Task(client.events.message_delete(client,message),client.loop)

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
    message=channel._mc_pop(message_id)
    if message is None:
        return
    
    for client_ in clients:
        Task(client_.events.message_delete(client_,message),client_.loop)
    
def MESSAGE_DELETE__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['id'])
    channel._mc_pop(message_id)

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
    channel._mc_pop(message_id)

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
    messages=channel._mc_pop_multiple(message_ids)
    
    Task(client.events.message_delete_multyple(client,channel,messages,message_ids),client.loop)

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
    messages=channel._mc_pop_multiple(message_ids)
    
    for client_ in clients:
        Task(client_.events.message_delete_multyple(client_,channel,messages,message_ids),client_.loop)

def MESSAGE_DELETE_BULK__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return

    message_ids=[int(message_id) for message_id in data['ids']]
    channel._mc_pop_multiple(message_ids)

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
    channel._mc_pop_multiple(message_ids)

PARSER_DEFAULTS('MESSAGE_DELETE_BULK',MESSAGE_DELETE_BULK__CAL_SC,MESSAGE_DELETE_BULK__CAL_MC,MESSAGE_DELETE_BULK__OPT_SC,MESSAGE_DELETE_BULK__OPT_MC)
del MESSAGE_DELETE_BULK__CAL_SC, MESSAGE_DELETE_BULK__CAL_MC, MESSAGE_DELETE_BULK__OPT_SC, MESSAGE_DELETE_BULK__OPT_MC

def MESSAGE_UPDATE__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        old=message._update(data)
        if not old:
            return
        
        Task(client.events.message_edit(client,message,old),client.loop)
    else:
        result=message._update_embed(data)
        if not result:
            return
        
        Task(client.events.embed_update(client,message,result),client.loop)

def MESSAGE_UPDATE__CAL_MC(client,data):
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
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        old=message._update(data)
        if not old:
            return
        
        for client_ in clients:
            Task(client_.events.message_edit(client_,message,old),client_.loop)
    else:
        result=message._update_embed(data)
        if not result:
            return
            
        for client_ in clients:
            Task(client_.events.embed_update(client_,message,result),client_.loop)

def MESSAGE_UPDATE__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        message._update_no_return(data)
    else:
        message._update_embed_no_return(data)

def MESSAGE_UPDATE__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_MESSAGES if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_MESSAGES) is not client:
        return
    
    message_id=int(data['id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    if 'edited_timestamp' in data:
        message._update_no_return(data)
    else:
        message._update_embed_no_return(data)


PARSER_DEFAULTS('MESSAGE_UPDATE',MESSAGE_UPDATE__CAL_SC,MESSAGE_UPDATE__CAL_MC,MESSAGE_UPDATE__OPT_SC,MESSAGE_UPDATE__OPT_MC)
del MESSAGE_UPDATE__CAL_SC, MESSAGE_UPDATE__CAL_MC, MESSAGE_UPDATE__OPT_SC, MESSAGE_UPDATE__OPT_MC

def MESSAGE_REACTION_ADD__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)
    
    Task(client.events.reaction_add(client,message,emoji,user),client.loop)

def MESSAGE_REACTION_ADD__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)
    
    for client_ in clients:
        Task(client_.events.reaction_add(client_,message,emoji,user),client_.loop)

def MESSAGE_REACTION_ADD__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)

def MESSAGE_REACTION_ADD__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.add(emoji,user)

PARSER_DEFAULTS('MESSAGE_REACTION_ADD',MESSAGE_REACTION_ADD__CAL_SC,MESSAGE_REACTION_ADD__CAL_MC,MESSAGE_REACTION_ADD__OPT_SC,MESSAGE_REACTION_ADD__OPT_MC)
del MESSAGE_REACTION_ADD__CAL_SC, MESSAGE_REACTION_ADD__CAL_MC, MESSAGE_REACTION_ADD__OPT_SC, MESSAGE_REACTION_ADD__OPT_MC

def MESSAGE_REACTION_REMOVE_ALL__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    old_reactions=message.reactions
    if not old_reactions:
        return
    
    message.reactions=type(old_reactions)(None)
    Task(client.events.reaction_clear(client,message,old_reactions),client.loop)

def MESSAGE_REACTION_REMOVE_ALL__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    old_reactions=message.reactions
    if not old_reactions:
        return
    
    message.reactions=type(old_reactions)(None)
    for client_ in clients:
        Task(client_.events.reaction_clear(client_,message,old_reactions),client_.loop)
    
def MESSAGE_REACTION_REMOVE_ALL__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return

    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return

    message.reactions=type(message.reactions)(None)

def MESSAGE_REACTION_REMOVE_ALL__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    message.reactions=type(message.reactions)(None)

PARSER_DEFAULTS('MESSAGE_REACTION_REMOVE_ALL',MESSAGE_REACTION_REMOVE_ALL__CAL_SC,MESSAGE_REACTION_REMOVE_ALL__CAL_MC,MESSAGE_REACTION_REMOVE_ALL__OPT_SC,MESSAGE_REACTION_REMOVE_ALL__OPT_MC)
del MESSAGE_REACTION_REMOVE_ALL__CAL_SC, MESSAGE_REACTION_REMOVE_ALL__CAL_MC, MESSAGE_REACTION_REMOVE_ALL__OPT_SC, MESSAGE_REACTION_REMOVE_ALL__OPT_MC

def MESSAGE_REACTION_REMOVE__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)
    
    Task(client.events.reaction_delete(client,message,emoji,user),client.loop)

def MESSAGE_REACTION_REMOVE__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)
    
    for client_ in clients:
        Task(client_.events.reaction_delete(client_,message,emoji,user),client_.loop)

def MESSAGE_REACTION_REMOVE__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)

def MESSAGE_REACTION_REMOVE__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    user_id=int(data['user_id'])
    user=PartialUser(user_id)
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove(emoji,user)

PARSER_DEFAULTS('MESSAGE_REACTION_REMOVE',MESSAGE_REACTION_REMOVE__CAL_SC,MESSAGE_REACTION_REMOVE__CAL_MC,MESSAGE_REACTION_REMOVE__OPT_SC,MESSAGE_REACTION_REMOVE__OPT_MC)
del MESSAGE_REACTION_REMOVE__CAL_SC, MESSAGE_REACTION_REMOVE__CAL_MC, MESSAGE_REACTION_REMOVE__OPT_SC, MESSAGE_REACTION_REMOVE__OPT_MC

def MESSAGE_REACTION_REMOVE_EMOJI__CAL_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    emoji=PartialEmoji(data['emoji'])
    users=message.reactions.remove_emoji(emoji)
    if users is None:
        return
    
    Task(client.events.reaction_delete_emoji(client,message,emoji,users),client.loop)

def MESSAGE_REACTION_REMOVE_EMOJI__CAL_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    clients=filter_clients(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS)
    if clients.send(None) is not client:
        clients.close()
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    emoji=PartialEmoji(data['emoji'])
    users=message.reactions.remove_emoji(emoji)
    if users is None:
        return
    
    for client_ in clients:
        Task(client_.events.reaction_delete_emoji(client_,message,emoji,users),client_.loop)

def MESSAGE_REACTION_REMOVE_EMOJI__OPT_SC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
        return
    
    emoji=PartialEmoji(data['emoji'])
    message.reactions.remove_emoji(emoji)

def MESSAGE_REACTION_REMOVE_EMOJI__OPT_MC(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    if first_client(channel.clients,INTENT_GUILD_REACTIONS if isinstance(channel,ChannelGuildBase) else INTENT_DIRECT_REACTIONS) is not client:
        return
    
    message_id=int(data['message_id'])
    message=channel._mc_find(message_id)
    if message is None:
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
        
        Task(coro(client,user,old),client.loop)
    
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
            
            Task(coro(client_,user,old),client_.loop)
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
        
        Task(client.events.user_profile_edit(client,user,old,guild),client.loop)

    def GUILD_MEMBER_UPDATE__CAL_MC(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild_sync(client,data,'GUILD_MEMBER_UPDATE')
            return
        
        clients=filter_clients(guild.clients,INTENT_GUILD_USERS)
        if clients.send(None) is not client:
            clients.close()
            return
        
        user,old=User._update_profile(data,guild)
        
        if not old:
            return
        
        for client_ in clients:
            Task(client_.events.user_profile_edit(client_,user,old,guild),client_.loop)
    
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
        
        if first_client(guild.clients,INTENT_GUILD_USERS) is not client:
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
        
        Task(client.events.user_profile_edit(client,client,old,guild),client.loop)

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

def CHANNEL_DELETE__CAL(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    channel._delete(client)
    
    #we do this only for the source client, it is handled personally
    Task(client.events.channel_delete(client,channel),client.loop)

def CHANNEL_DELETE__OPT(client,data):
    channel_id=int(data['id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,None)
        return
    
    channel._delete(client)

PARSER_DEFAULTS('CHANNEL_DELETE',CHANNEL_DELETE__CAL,CHANNEL_DELETE__CAL,CHANNEL_DELETE__OPT,CHANNEL_DELETE__OPT)
del CHANNEL_DELETE__CAL, CHANNEL_DELETE__OPT

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
    
    Task(client.events.channel_edit(client,channel,old),client.loop)

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
        Task(client_.events.channel_edit(client_,channel,old),client_.loop)

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
    
    Task(client.events.channel_create(client,channel),client.loop)

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
    Task(client.events.channel_pin_update(client,channel),client.loop)

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
    
    Task(client.events.channel_group_user_add(client,channel,user),client.loop)

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
        Task(client.events.channel_group_user_delete(client,channel,user),client.loop)

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
            Task(client_.events.channel_group_user_delete(client_,channel,user),client_.loop)

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
            
            Task(coro(client,guild,emoji,old),client.loop)
            continue
            
        if action==EMOJI_UPDATE_NEW:
            coro=client.events.emoji_create
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,guild,emoji),client.loop)
            continue
        
        if action==EMOJI_UPDATE_DELETE:
            coro=client.events.emoji_delete
            if coro is DEFAULT_EVENT:
                continue
            
            Task(coro(client,guild,emoji),client.loop)
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
                
                Task(coro(client,guild,emoji,old),client_.loop)
                continue
                
            if action==EMOJI_UPDATE_NEW:
                coro=client_.events.emoji_create
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji),client_.loop)
                continue
            
            if action==EMOJI_UPDATE_DELETE:
                coro=client_.events.emoji_delete
                if coro is DEFAULT_EVENT:
                    continue
                
                Task(coro(client,guild,emoji),client_.loop)
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
    
    Task(client.events.guild_user_add(client,guild,user),client.loop)

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
        Task(client_.events.guild_user_add(client_,guild,user),client_.loop)

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
        
        Task(client.events.guild_user_delete(client,guild,user,profile),client.loop)

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
            Task(client_.events.guild_user_delete(client_,guild,user,profile),client_.loop)
    
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
        
        Task(client.events.guild_user_delete(client,guild,user,None),client.loop)

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
            Task(client_.events.guild_user_delete(client_,guild,user,None),client_.loop)
    
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
                Task(client._request_members(guild),client.loop)
            Task(client.events.guild_create(client,guild),client.loop)
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
                Task(client._request_members(guild),client.loop)
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
            Task(client._request_members(guild),client.loop)
            Task(client.events.guild_create(client,guild),client.loop)
            return
        
        ready_state.feed(guild)

    def GUILD_CREATE__OPT(client,data):
        guild_state=data.get('unavailable',False)
        if guild_state:
            return
        
        guild=Guild(data,client)
        
        ready_state=client.ready_state
        if ready_state is None:
            Task(client._request_members(guild),client.loop)
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
            Task(client.events.guild_create(client,guild),client.loop)
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
    
    Task(client.events.guild_edit(client,guild,old),client.loop)

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
        Task(client_.events.guild_edit(client_,guild,old),client_.loop)

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
    
    Task(client.events.guild_delete(client,guild,profile),client.loop)

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
    
    Task(client.events.guild_ban_add(client,guild,user),client.loop)

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
    Task(client.events.guild_ban_delete(client,guild,user),client.loop)

def GUILD_BAN_REMOVE__OPT(client,data):
    pass

PARSER_DEFAULTS('GUILD_BAN_REMOVE',GUILD_BAN_REMOVE__CAL,GUILD_BAN_REMOVE__CAL,GUILD_BAN_REMOVE__OPT,GUILD_BAN_REMOVE__OPT)
del GUILD_BAN_REMOVE__CAL, GUILD_BAN_REMOVE__OPT

if CACHE_PRESENCE:
    def GUILD_MEMBERS_CHUNK(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            return
        
        collected=[]
        for user_data in data['members']:
            user=User(user_data,guild)
            collected.append(user)
        
        try:
            presence_datas=data['presences']
        except KeyError:
            pass
        else:
            guild._apply_presences(presence_datas)
        
        #this event is called at guild joining, and only 1 client joins at the same time
        Task(client.events.guild_user_chunk(client,guild,collected),client.loop)
else:
    def GUILD_MEMBERS_CHUNK(client,data):
        guild_id=int(data['guild_id'])
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            return
        
        collected=[]
        for user_data in data['members']:
            user=User(user_data,guild)
            collected.append(user)
        #this event is called at guild joining, and only 1 client joins at the same time
        Task(client.events.guild_user_chunk(client,guild,collected),client.loop)

PARSER_DEFAULTS('GUILD_MEMBERS_CHUNK',GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK,GUILD_MEMBERS_CHUNK)
del GUILD_MEMBERS_CHUNK

def GUILD_INTEGRATIONS_UPDATE__CAL(client,data):
    guild_id=int(data['guild_id'])
    try:
        guild=GUILDS[guild_id]
    except KeyError:
        guild_sync(client,data,'GUILD_INTEGRATIONS_UPDATE')
        return
    
    Task(client.events.integration_update(client,guild),client.loop)

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
    
    Task(client.events.role_create(client,role),client.loop)

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
        Task(client_.events.role_create(client_,role),client_.loop)

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
    
    Task(client.events.role_delete(client,role),client.loop)

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
        Task(client_.events.role_delete(client_,role),client_.loop)

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
    
    Task(client.events.role_edit(client,role,old),client.loop)

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
        Task(client_.events.role_edit(client_,role,old),client_.loop)

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
    Task(client.events.webhook_update(client,channel,),client.loop)

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
        id_=int(data['channel_id'])
        try:
            call=client.calls[id_]
        except KeyError:
            return
        guild=None
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
        call=guild
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=call._update_voice_state(data,user)
    
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
                Task(voice_client.disconnect(force=True,terminate=False),client.loop)
            else:
                voice_client.channel=result[0].channel
    
    Task(client.events.voice_state_update(client,*result),client.loop)

def VOICE_STATE_UPDATE__CAL_MC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        id_=int(data['channel_id'])
        try:
            call=client.calls[id_]
        except KeyError:
            return
        clients=call.channel.clients
        guild=None
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
        call=guild
        clients=guild.clients
    
    clients=filter_clients(clients,INTENT_GUILD_VOICE_STATES)
    if clients.send(None) is not client:
        clients.close()
        return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=call._update_voice_state(data,user)
    
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
                    Task(voice_client.disconnect(force=True,terminate=False),client_.loop)
                else:
                    voice_client.channel=result[0].channel
        
        Task(client_.events.voice_state_update(client_,*result),client_.loop)

def VOICE_STATE_UPDATE__OPT_SC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        id_=int(data['channel_id'])
        try:
            call=client.calls[id_]
        except KeyError:
            return
        guild=None
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
        call=guild
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    
    result=call._update_voice_state_restricted(data,user)
    
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
        Task(voice_client.disconnect(force=True,terminate=False),client.loop)
    else:
        voice_client.channel=result

def VOICE_STATE_UPDATE__OPT_MC(client,data):
    try:
        id_=int(data['guild_id'])
    except KeyError:
        id_=int(data['channel_id'])
        try:
            call=client.calls[id_]
        except KeyError:
            return
        clients=call.channel.clients
        guild=None
    else:
        try:
            guild=GUILDS[id_]
        except KeyError:
            guild_sync(client,data,'VOICE_STATE_UPDATE')
            return
        call=guild
        clients=guild.clients
    
    if first_client(clients,INTENT_GUILD_VOICE_STATES) is not client:
        return
    
    try:
        user=User(data['member'],guild)
    except KeyError:
        user=User(data['user'])
    result=call._update_voice_state_restricted(data,user)
    
    if result is None:
        return
    
    for client in clients:
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
        Task(voice_client.disconnect(force=True,terminate=False),client.loop)
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
    
    Task(voice_client._create_socket(data),client.loop)
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
        
        Task(client.events.typing(client,channel,user,timestamp),client.loop)
    
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
    Task(client.events.invite_create(client,invite),client.loop)

def INVITE_CREATE__OPT(client,data):
    pass

PARSER_DEFAULTS('INVITE_CREATE',INVITE_CREATE__CAL,INVITE_CREATE__CAL,INVITE_CREATE__OPT,INVITE_CREATE__OPT)
del INVITE_CREATE__CAL, INVITE_CREATE__OPT

def INVITE_DELETE__CAL(client,data):
    invite = Invite(data)
    Task(client.events.invite_delete(client,invite),client.loop)

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
    
    user=PartialUser(user_id)
    
    new_relationship=Relationship(client,user,data)
    
    if old_relationship is None:
        coro=client.events.relationship_add(client,new_relationship)
    else:
        coro=client.events.relationship_change(client,old_relationship,new_relationship)
    Task(coro,client.loop)

def RELATIONSHIP_ADD__OPT(client,data):
    user_id=int(data['id'])
    try:
        del client.relationships[user_id]
    except KeyError:
        pass
    
    user=PartialUser(user_id)
    
    Relationship(client,user,data)

PARSER_DEFAULTS('RELATIONSHIP_ADD',RELATIONSHIP_ADD__CAL,RELATIONSHIP_ADD__CAL,RELATIONSHIP_ADD__OPT,RELATIONSHIP_ADD__OPT)
del RELATIONSHIP_ADD__CAL, RELATIONSHIP_ADD__OPT

def RELATIONSHIP_REMOVE__CAL(client,data):
    user_id=int(data['id'])
    try:
        old_relationship=client.user.relations.pop(user_id)
    except KeyError:
        coro=client.events.unknown_relationship(client,'relationship_delete',data,)
    else:
        coro=client.events.relationship_delete(client,old_relationship)
    Task(coro,client.loop)

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

def USER_SETTINGS_UPDATE__CAL(client,data):
    old=client.settings._update(data)
    Task(client.events.client_edit_settings(client,old),client.loop)

def USER_SETTINGS_UPDATE__OPT(client,data):
    client.settings._update_no_return(data)

PARSER_DEFAULTS('USER_SETTINGS_UPDATE',USER_SETTINGS_UPDATE__CAL,USER_SETTINGS_UPDATE__CAL,USER_SETTINGS_UPDATE__OPT,USER_SETTINGS_UPDATE__OPT)
del USER_SETTINGS_UPDATE__CAL, USER_SETTINGS_UPDATE__OPT

def GIFT_CODE_UPDATE__CAL(client,data):
    channel_id=int(data['channel_id'])
    try:
        channel=CHANNELS[channel_id]
    except KeyError:
        guild_sync(client,data,('GIFT_CODE_UPDATE',check_channel,channel_id))
        return
    
    gift=Gift(data)
    Task(client.events.gift_update(client,channel,gift),client.loop)

def GIFT_CODE_UPDATE__OPT(client,data):
    pass

PARSER_DEFAULTS('GIFT_CODE_UPDATE',GIFT_CODE_UPDATE__CAL,GIFT_CODE_UPDATE__CAL,GIFT_CODE_UPDATE__OPT,GIFT_CODE_UPDATE__OPT)
del GIFT_CODE_UPDATE__CAL, GIFT_CODE_UPDATE__OPT

#hooman only event, needs futher testing, there is no real documentation on this
def USER_ACHIEVEMENT_UPDATE__CAL(client,data):
    Task(client.events.achievement(client,data),client.loop)

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
    # should we store it at settings?
    pass

PARSER_DEFAULTS('USER_GUILD_SETTINGS_UPDATE',USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE,USER_GUILD_SETTINGS_UPDATE)
del USER_GUILD_SETTINGS_UPDATE


EVENTS=event_system_core()

EVENTS.add_default('error'                      , 3 , ''                                , )

EVENTS.add_default('ready'                      , 1 , 'READY'                           , )
EVENTS.add_default('client_edit'                , 2 , 'USER_UPDATE'                     , )
EVENTS.add_default('message_create'             , 2 , 'MESSAGE_CREATE'                  , )
EVENTS.add_default('message_delete'             , 2 , 'MESSAGE_DELETE'                  , )
EVENTS.add_default('message_delete_multyple'    , 4 , 'MESSAGE_DELETE_BULK'             , )
EVENTS.add_default('message_edit'               , 3 , 'MESSAGE_UPDATE'                  , )
EVENTS.add_default('embed_update'               , 3 , 'MESSAGE_UPDATE'                  , )
EVENTS.add_default('reaction_add'               , 4 , 'MESSAGE_REACTION_ADD'            , )
EVENTS.add_default('reaction_clear'             , 3 , 'MESSAGE_REACTION_REMOVE_ALL'     , )
EVENTS.add_default('reaction_delete'            , 4 , 'MESSAGE_REACTION_REMOVE'         , )
EVENTS.add_default('reaction_delete_emoji'      , 4 , 'MESSAGE_REACTION_REMOVE_EMOJI'   , )
EVENTS.add_default('user_edit'                  , 3 , 'PRESENCE_UPDATE'                 , )
EVENTS.add_default('user_presence_update'       , 3 , 'PRESENCE_UPDATE'                 , )
EVENTS.add_default('user_profile_edit'          , 4 , 'GUILD_MEMBER_UPDATE'             , )
EVENTS.add_default('channel_delete'             , 2 , 'CHANNEL_DELETE'                  , )
EVENTS.add_default('channel_edit'               , 3 , 'CHANNEL_UPDATE'                  , )
EVENTS.add_default('channel_create'             , 2 , 'CHANNEL_CREATE'                  , )
EVENTS.add_default('channel_pin_update'         , 2 , 'CHANNEL_PINS_UPDATE'             , )
EVENTS.add_default('channel_group_user_add'     , 3 , 'CHANNEL_RECIPIENT_ADD'           , )
EVENTS.add_default('channel_group_user_delete'  , 3 , 'CHANNEL_RECIPIENT_REMOVE'        , )
EVENTS.add_default('emoji_create'               , 3 , 'GUILD_EMOJIS_UPDATE'             , )
EVENTS.add_default('emoji_delete'               , 3 , 'GUILD_EMOJIS_UPDATE'             , )
EVENTS.add_default('emoji_edit'                 , 4 , 'GUILD_EMOJIS_UPDATE'             , )
EVENTS.add_default('guild_user_add'             , 3 , 'GUILD_MEMBER_ADD'                , )
EVENTS.add_default('guild_user_delete'          , 4 , 'GUILD_MEMBER_REMOVE'             , )
EVENTS.add_default('guild_create'               , 2 , 'GUILD_CREATE'                    , )
EVENTS.add_default('guild_edit'                 , 2 , 'GUILD_UPDATE'                    , )
EVENTS.add_default('guild_delete'               , 3 , 'GUILD_DELETE'                    , )
EVENTS.add_default('guild_ban_add'              , 3 , 'GUILD_BAN_ADD'                   , )
EVENTS.add_default('guild_ban_delete'           , 3 , 'GUILD_BAN_REMOVE'                , )
EVENTS.add_default('guild_user_chunk'           , 3 , 'GUILD_MEMBERS_CHUNK'             , )
EVENTS.add_default('integration_update'         , 2 , 'GUILD_INTEGRATIONS_UPDATE'       , )
EVENTS.add_default('role_create'                , 2 , 'GUILD_ROLE_CREATE'               , )
EVENTS.add_default('role_delete'                , 2 , 'GUILD_ROLE_DELETE'               , )
EVENTS.add_default('role_edit'                  , 3 , 'GUILD_ROLE_UPDATE'               , )
EVENTS.add_default('webhook_update'             , 2 , 'WEBHOOKS_UPDATE'                 , )
EVENTS.add_default('voice_state_update'         , 4 , 'VOICE_STATE_UPDATE'              , )
EVENTS.add_default('typing'                     , 4 , 'TYPING_START'                    , )
EVENTS.add_default('invite_create'              , 2 , 'INVITE_CREATE'                   , )
EVENTS.add_default('invite_delete'              , 2 , 'INVITE_DELETE'                   , )
EVENTS.add_default('relationship_add'           , 2 , 'RELATIONSHIP_ADD'                , )
EVENTS.add_default('relationship_change'        , 3 , 'RELATIONSHIP_ADD'                , )
EVENTS.add_default('relationship_delete'        , 2 , 'RELATIONSHIP_REMOVE'             , )
EVENTS.add_default('client_edit_settings'       , 2 , 'USER_SETTINGS_UPDATE'            , )
EVENTS.add_default('gift_update'                , 3 , 'GIFT_CODE_UPDATE'                , )
EVENTS.add_default('achievement'                , 2 , 'USER_ACHIEVEMENT_UPDATE'         , )

def check_name(func,name):
    if name is not None and name:
        return name.lower()
    if hasattr(func,'__event_name__'):
        return func.__event_name__
    #func or method
    if hasattr(func,'__name__'):
        return func.__name__.lower()
    func=type(func)
    if not issubclass(func,type) and hasattr(func,'__name__'):
        return func.__name__.lower()

    raise TypeError('The class must have \'__name__\' attribute and metaclasses are not allowed')
        
            
def check_argcount_and_convert(func,expected,errormsg=None):
    while True:
        # func
        if isinstance(func,function):
            result=func
            real_func=func
            ismethod=0
            break
            
        # method
        if isinstance(func,MethodLike):
            result=func
            real_func=func
            ismethod=MethodLike.get_reserved_argcount(real_func)
            break
            
        # callable object
        if not isinstance(func,type) and hasattr(type(func),'__call__'):
            result=func
            real_func=result.__call__
            ismethod=MethodLike.get_reserved_argcount(real_func)
            break
            
        # type, but not metaclass
        if not issubclass(func,type) and isinstance(func,type):
            
            # async initializer
            if iscoro(func.__new__):
                result=func
                real_func=result.__new__
                
                # by default `__new__` is a classmethod, but without a descriptor
                if isinstance(result.__new__,function):
                    ismethod=1
                else:
                    ismethod=MethodLike.get_reserved_argcount(real_func)
                    
                ismethod=True
                break
            
            # async call -> initialize 1st
            if hasattr(func,'__call__'):
                result=func()
                real_func=result.__call__
                ismethod=MethodLike.get_reserved_argcount(real_func)
                break
        # meow?
        raise TypeError(f'Expected function, method or a callable object, got {func!r}')
    
    if not hasattr(real_func,'__code__'):
        raise TypeError(f'expected a function, got : {real_func!r}')
    
    argcount=real_func.__code__.co_argcount-ismethod
    args=real_func.__code__.co_flags&4
    
    if type(expected) is int:
        if argcount==expected or (args and argcount<expected):
            return result
    else:
        for expected_ in expected:
            if argcount==expected_ or (args and argcount<expected_):
                return expected_,result
    
    if errormsg is None:
        errormsg=f'Invalid argcount, expected {expected}, got {argcount} (args={bool(args)}).'
    
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

def just_convert(func):
    if isinstance(func,(function,MethodLike)):
        return func
    if not isinstance(func,type) and hasattr(type(func),'__call__'):
        return func
    if not issubclass(func,type) and isinstance(func,type):
        if iscoro(func.__new__):
            return func
        if hasattr(func,'__call__'):
            return func()
    #nya?
    raise TypeError(f'Expected function, method or callable object, got {func!r}')

def check_coro(func):
    if getattr(func,'__async_call__',False):
        return True
    if isinstance(func,(function,MethodLike)):
        return iscoro(func)
    
    if iscoro(func.__new__):
        return True

    func=getattr(func,'__call__',None)
    return iscoro(func)
    

# 1 line check, so u dont need to write that much
def check_passed(func,expected,errormsg=None):
    func=check_argcount_and_convert(func,expected,errormsg)
    if check_coro(func):
        return func
    raise TypeError(f'Expected coroutine function, got {func!r}')

def check_passed_tuple(func,expected,errormsg=None):
    expected,func=check_argcount_and_convert(func,expected,errormsg)
    if check_coro(func):
        return expected,func
    raise TypeError(f'Expected coroutine function, got {func!r}')

# when every line can raise error, feelsgoodman
def create_valid_event(func,name):
    name=check_name(func,name)
    argcount=EVENTS.get_argcount(name)
    func=check_argcount_and_convert(func,argcount)

    if not check_coro(func):
        raise ValueError(f'Events must be coroutine functions!')
    
    return name,func


def create_valid_case(func,name):
    #a quick check
    if isinstance(func,str):
        return func

    argcount=EVENTS.get_argcount(name)
    func=check_argcount_and_convert(func,argcount)

    if check_coro(func):
        raise ValueError(f'Cases must be NOT coroutine fucntions!')
    
    return func

def _convert_unsafe_event_iterable(iterable):
    result=[]
    for element in iterable:
        if isinstance(element,tuple):
            element_len=len(element)
            if element_len>2 or element_len==0:
                raise ValueError(f'Expected `tuple` with length 1 or 2, got `{element!r}`.')
            
            func=element[0]
            if element_len==1:
                element=EventListElement(func,None,None)
                result.append(element)
                continue
            
            case=element[1]
            if (case is not None) and not isinstance(case,str):
                raise ValueError(f'Expected `None` or `str` instance at index 1 at element: `{element!r}`')
            
            element=EventListElement(func,case,None)
            result.append(element)
            continue
        
        if isinstance(element,dict):
            try:
                func=element.pop('func')
            except KeyError:
                raise ValueError(f'Expected all `dict` elements to contain `\'func\'` key, but was not found at `{element!r}`') from None
            
            case=element.pop('case',None)
            
            if not element:
                element = None
            
            element=EventListElement(func,case,element)
            result.append(element)
            continue
        
        if type(element) is EventListElement:
            result.append(element)
            continue
        
        element=EventListElement(element,None,None)
        result.append(element)
        continue
    
    return result
#autoadds : "client.events.", "name=parent.__name__" and "pass_content=True", basically
class _EventCreationManager(object):
    __slots__=('parent',)
    
    def __init__(self,parent):
        self.parent=parent
    
    def __repr__(self):
        return f'<{self.__class__.__name__} of {self.parent!r}>'
    
    def __call__(self,func=None,case=None,**kwargs):
        if func is None:
            return self._wrapper(self,case,kwargs)
        
        if case is None:
            case=check_name(func,None)
        
        if (not case.islower()):
            case=case.lower()
        
        func=self.parent.__setevent__(func,case,**kwargs)
        return func
    
    def remove(self,func,case=None,**kwargs):
        if case is None:
            case=check_name(func,None)
        
        if (not case.islower()):
            case=case.lower()
        
        self.parent.__delevent__(func,case,**kwargs)
    
    class _wrapper(object):
        __slots__=('parent', 'case', 'kwargs')
        def __init__(self,parent,case,kwargs):
            self.parent=parent
            self.case=case
            self.kwargs=kwargs
        
        def __call__(self,func,):
            return self.parent(func,self.case,**self.kwargs)
    
    def __getattr__(self,name):
        return getattr(self.parent,name)
    
    def extend(self,iterable):
        if type(iterable) is not eventlist:
            iterable=_convert_unsafe_event_iterable(iterable)
        
        for element in iterable:
            case=element.case
            func=element.func
            
            if (case is None):
                case=check_name(func,None)
            
            if (not case.islower()):
                case=case.lower()
            
            kwargs=element.kwargs
            if kwargs is None:
                self.parent.__setevent__(func,case)
            else:
                self.parent.__setevent__(func,case,**kwargs)
    
    def unextend(self,iterable):
        if type(iterable) is not eventlist:
            iterable=_convert_unsafe_event_iterable(iterable)
        
        collected=[]
        for element in iterable:
            kwargs=element.kwargs
            try:
                if kwargs is None:
                    self.remove(element.func,element.case)
                else:
                    self.remove(element.func,element.case,**kwargs)
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected))
        
class EventListElement(object):
    __slots__= ('case', 'kwargs', 'func', )
    def __init__(self,func,case,kwargs):
        self.func  = func
        self.case  = case
        self.kwargs= kwargs
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.func!r}, {self.case!r}, kwargs={self.kwargs!r})'

class eventlist(list,metaclass=removemeta):
    delete=remove('insert','sort','pop','reverse','remove','sort','index',
        'count','__mul__','__rmul__','__imul__','__add__','__radd__','__iadd__',
        '__setitem__','__contains__')
    __slots__=()
    def __init__(self,iterable=None):
        if (iterable is not None) and iterable:
            self.extend(iterable)

    class _wrapper(object):
        __slots__=('parent', 'case', 'kwargs')
        def __init__(self, parent, case, kwargs):
            self.parent=parent
            self.case=case
            self.kwargs=kwargs
        
        def __call__(self,func):
            func=just_convert(func)
            
            list.append(self.parent,EventListElement(func,self.case,self.kwargs))
            return func
    
    def extend(self,iterable):
        if type(iterable) is not type(self):
            iterable=_convert_unsafe_event_iterable(iterable)
            
        list.extend(self,iterable)
    
    def unextend(self,iterable):
        if type(iterable) is not type(self):
            iterable=_convert_unsafe_event_iterable(iterable)
        
        collected=[]
        for element in iterable:
            try:
                self.remove(*element)
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected))
    
    def __call__(self,func=None,case=None,**kwargs):
        if (case is not None) and (not case.islower()):
            case=case.lower()
        
        if not kwargs:
            kwargs=None
        
        if func is None:
            return self._wrapper(self,case,kwargs)
        
        func=just_convert(func)
        
        list.append(self,EventListElement(func,case,kwargs))
        return func
    
    def remove(self,func,case=None):
        if (case is not None) and (not case.islower()):
            case=case.lower()
            
        # we might overwrite __iter__ later
        for element in list.__iter__(self):
            
            converted_case=element.case
            # `case` can be `None` or `str`
            if converted_case is None:
                if case is not None:
                    continue
            else:
                if case is None:
                    continue
                
                if converted_case!=case:
                    continue
            
            if compare_converted(element.func,func):
                return
        
        raise ValueError(f'Did not find any element, what matched the passed func={func!r}, case={case!r} combination.')
    
    def __repr__(self):
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
        
        result.append('])')
        
        return ''.join(result)
        
# this class is a placeholder for the `with` statemnet support
# also for the `shortcut` propery as well.
class EventHandlerBase(object):
    __slots__=()
    
    # subclasses should overwrite it
    async def __call__(self, *args):
        return

    # subclasses should overwrite it
    def __setevent__(self, func, case):
        pass

    # subclasses should overwrite it
    def __delevent__(self, func, case):
        pass

    @property
    def shortcut(self):
        return _EventCreationManager(self)

class ReadyState(object):
    __slots__=('counter', 'guilds', 'last_guild', 'last_ready', 'waiter', )
    def __init__(self,client,guild_datas):
        self.waiter     = Future(client.loop)
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
    

class ChunkQueue(EventHandlerBase):
    __slots__=('default', 'waiters',)
    __event_name__='guild_user_chunk'
    def __init__(self):
        self.default=None
        self.waiters={}
        
    def __setevent__(self,func,guild_id):
        try:
            waiters=self.waiters[guild_id]
        except KeyError:
            self.waiters[guild_id]=waiters=[]
        waiters.append(func)

    def __delevent__(self,func,guild_id):
        pass
            
    async def __call__(self,client,guild,collected):
        if self.default is not None:
            self.default(collected)
        
        try:
            waiters=self.waiters[guild.id]
        except KeyError:
            return

        if waiters[0](collected):
            if len(waiters)==1:
                del self.waiters[guild.id]
            else:
                del waiters[0]
            

async def default_error_event(client,event,err):
    extracted=[
        client.full_name,
        ' ignores occurred Exception at ',
        event,
        '\n'
            ]
    
    if isinstance(err,BaseException):
        await client.loop.render_exc_async(err,extracted)
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
    
    async def __call__(self,client,*args):
        for coro in self:
            Task(coro(client,*args),client.loop)
    
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
        client_reference=Weakreferer(client)
        object.__setattr__(self,'client_reference',client_reference)
        for name in EVENTS.defaults:
            object.__setattr__(self,name,DEFAULT_EVENT)
        object.__setattr__(self,'error',default_error_event)
        object.__setattr__(self,'guild_user_chunk',ChunkQueue())
    
    def __call__(self,func=None,name=None,pass_to_event=False,case=None,overwrite=False):
        if func is None:
            return self._wrapper(self,(name,pass_to_event,case),)
        
        if pass_to_event:
            if name is None:
                raise ValueError('\'name\' can not be None if \'pass_to_event\' is set to True')
            if case is None:
                case=check_name(func,None)
            
            if (not case.islower()):
                case=case.lower()
            
            event_handler=getattr(self,name)
            func=event_handler.__setevent__(func,case)
            return func
        
        name,func=create_valid_event(func,name)
        
        if overwrite:
            setattr(self,name,func)
            return func
        
        parser_name=EVENTS.parsers.get(name,None)
        if (parser_name is None):
            raise AttributeError(f'Event name: \'{name}\' is invalid')
        
        if func is DEFAULT_EVENT:
            return func
        
        parser_default=PARSER_DEFAULTS.all[parser_name]
        actual=getattr(self,name)
        if actual is DEFAULT_EVENT:
            object.__setattr__(self,name,func)
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
        object.__setattr__(self,'guild_user_chunk',ChunkQueue())
    
    def __setattr__(self,name,value):
        parser_name=EVENTS.parsers.get(name,None)
        if (parser_name is None):
            object.__setattr__(self,name,value)
            return
        
        parser_default=PARSER_DEFAULTS.all[parser_name]
        actual=getattr(self,name)
        object.__setattr__(self,name,value)
        if actual is DEFAULT_EVENT:
            if value is DEFAULT_EVENT:
                return
            
            parser_default.add_mention(self.client_reference())
            return
        
        if value is DEFAULT_EVENT:
            parser_default.remove_mention(self.client_reference())
    
    def __delattr__(self,name):
        actual=getattr(self,name)
        if actual is DEFAULT_EVENT:
            return
        
        object.__setattr__(self,name,DEFAULT_EVENT)
        
        parser_name=EVENTS.parsers.get(name,None)
        if (parser_name is None):
            return

        parser_default=PARSER_DEFAULTS.all[parser_name]
        parser_default.remove_mention(self.client_reference())
        
async def _with_error(client,task):
    try:
        await task
    except BaseException as err:
        await client.events.error(client,repr(task),err)

del removemeta
del remove
del datetime
