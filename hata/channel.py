# -*- coding: utf-8 -*-
__all__ = ('ChannelBase', 'ChannelCategory', 'ChannelGroup', 'ChannelPrivate',
    'ChannelStore', 'ChannelText', 'ChannelTextBase', 'ChannelVoice',
    'MessageIterator', 'cr_pg_channel_object', )

import re
from collections import deque
from time import monotonic

from .dereaddons_local import weakposlist
from .futures import sleep

from .client_core import CHANNELS
from .others import id_to_time, _parse_ih_fs
from .permission import Permission
from .http import URLS
from .message import Message, MESSAGES
from .user import User, ZEROUSER
from .role import PermOW
from .client_core import GC_cycler
from .webhook import Webhook

from . import webhook, message

Q_on_GC=deque()

def GC_messages(cycler):
    now=monotonic()
    for index in reversed(range(len(Q_on_GC))):
        channel=Q_on_GC[index]
        if channel._turn_gc_on_at<now:
            switch_to_limited(channel)
            del Q_on_GC[index]

GC_cycler.append(GC_messages)

del GC_messages,GC_cycler

def switch_to_limited(channel):
    old=channel.messages
    limit=channel._mc_gc_limit
    if len(old)>limit:
        channel.messages=deque((old[i] for i in range(limit)),maxlen=limit)
    else:
        channel.messages=deque(old,maxlen=limit)

    channel._turn_gc_on_at=0.
    channel.message_history_reached_end=False
    
def PartialChannel(data,partial_guild=None):
    if (data is None) or (not data):
        return None
    channel_id=int(data['id'])
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass

    try:
        cls=CHANNEL_TYPES[data['type']]
    except IndexError:
        return None

    channel=cls._from_partial_data(data,channel_id,partial_guild)
    CHANNELS[channel_id]=channel
    
    return channel
    
class ChannelBase(object):
    __slots__=('__weakref__', 'id')
    INTERCHANGE=(0,)

    def __new__(cls,data,client=None,guild=None):
        channel_id=int(data['id'])
        try:
            channel=CHANNELS[channel_id]
            update= (not channel.clients)
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            CHANNELS[channel_id]=channel
            update=True
        
        if update:
            #make sure about this
            channel._finish_init(data,client,guild)
                
        if cls is ChannelPrivate:
            if channel.users[0] is client:
                user=channel.users[1]
            else:
                user=channel.users[0]
                
            client.private_channels[user.id]=channel
            client.channels[channel_id]=channel
        elif cls is ChannelGroup:
            client.channels[channel_id]=channel
        
        return channel

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, name={self!s}>'

    def __hash__(self):
        return self.id

    def __format__(self,code):
        if not code:
            return self.__str__()
        if code=='m':
            return f'<#{self.id}>'
        if code=='d':
            return self.display_name
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')

    @property
    def mention(self):
        return f'<#{self.id}>'
    
    @property
    def created_at(self):
        return id_to_time(self.id)

    @property
    def partial(self):
        return (not self.clients)

    def get_user(self,name,default=None):
        if len(name)>37:
            return default
        users=self.users

        if len(name)>6 and name[-5]=='#':
            try:
                discriminator=int(name[-4:])
            except ValueError:
                pass
            else:
                name=name[:-5]
                for user in users:
                    if user.discriminator==discriminator and user.name==name:
                        return user

        if len(name)>32:
            return default

        for user in users:
            if user.name==name:
                return user
        
        return default

    def get_user_like(self,name,default=None):
        if not 1<len(name)<33:
            return default
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users:
            if pattern.match(user.name) is None:
                continue
            return user
        return default
    
    def get_users_like(self,name):
        result=[]
        if not 1<len(name)<33:
            return result
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users:
            if pattern.match(user.name) is None:
                continue
            result.append(user)
        return result
                
    @property
    def clients(self):
        result=[]
        for user in self.users:
            if type(user) is User:
                continue
            result.append(user)
        return result

    #for sorting channels
    def __gt__(self,other):
        if isinstance(other,ChannelBase):
            return self.id>other.id
        return NotImplemented

    def __ge__(self,other):
        if isinstance(other,ChannelBase):
            return self.id>=other.id
        return NotImplemented

    def __eq__(self,other):
        if isinstance(other,ChannelBase):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if isinstance(other,ChannelBase):
            return self.id!=other.id
        return NotImplemented

    def __le__(self,other):
        if isinstance(other,ChannelBase):
            return self.id<=other.id
        return NotImplemented

    def __lt__(self,other):
        if isinstance(other,ChannelBase):
            return self.id<other.id
        return NotImplemented
    
async def _load_till(client,channel,index):
    if index>=channel._mc_gc_limit:
        if channel.messages.maxlen is not None:
            channel._turn_gc_on_at=monotonic()+((channel._mc_gc_limit+100)<<2)
            channel.messages=deque(channel.messages)
            Q_on_GC.append(channel)
        elif channel._turn_gc_on_at:
            channel._turn_gc_on_at+=(index+100)<<2

    while True:
        ln=len(channel.messages)
        loadto=index-ln
        if loadto<0:
            break
        if loadto<98:
            planed=loadto+3
        else:
            planed=100
        
        if ln>2:
            result = await client.message_logs(channel,planed,before=channel.messages[ln-2].id)
        else:
            result = await client.message_logs_fromzero(channel,planed)
        
        if len(result)<planed:
            channel.message_history_reached_end=True
            raise IndexError

        await sleep(0.1,client.loop) #sometimes deque can not keep up?


#sounds funny, but this is a class
#the chunksize is 97, because it means 1 request for _load_till
class MessageIterator(object):
    __slots__=('_index', '_permission', 'channel', 'chunksize', 'client',)
    def __init__(self,client,channel,chunksize=97):
        self.client     = client
        self.channel    = channel
        self.chunksize  = chunksize
        self._index     = 0
        self._permission= not channel.cached_permissions_for(client).can_read_message_history
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        channel=self.channel
        index=self._index
        if len(channel.messages)>index:
            self._index=index+1
            return channel.messages[index]

        if channel.message_history_reached_end or self._permission:
            raise StopAsyncIteration
        
        try:
            await _load_till(self.client,channel,index+self.chunksize)
        except IndexError:
            pass

        if len(channel.messages)>index:
            self._index=index+1
            return channel.messages[index]
        
        raise StopAsyncIteration
    
    def __repr__(self):
        return f'<{self.__class__.__name__} of client {self.client.full_name}, at channel {self.channel.name} ({self.channel.id})>'
    
async def message_at_index(client,channel,index):
    if index<len(channel.messages):
        return channel.messages[index]

    if channel.message_history_reached_end:
        raise IndexError(index)

    if not channel.cached_permissions_for(client).can_read_message_history:
        raise PermissionError('Client cant read message history')
    
    await _load_till(client,channel,index)
    return channel.messages[index]

async def messages_till_index(client,channel,start=0,end=100):
    if end>=len(channel.messages) and \
           not channel.message_history_reached_end and \
           channel.cached_permissions_for(client).can_read_message_history:
        try:
            await _load_till(client,channel,end)
        except IndexError:
            pass

    result=[]
    messages=channel.messages
    for index in range(start,min(end,len(messages))):
        result.append(messages[index])
        
    return result
            
    
    
#searches the relative index of a message in a list
def message_relativeindex(self,message_id):
    bot=0
    top=len(self)
    while True:
        if bot<top:
            half=(bot+top)>>1
            if self[half].id>message_id:
                bot=half+1
            else:
                top=half
            continue
        break
    return bot
    
class ChannelTextBase(object):
#do not call any functions from this if u dunno anything about them!
#the message history is basically sorted by message_id, what can be translated to real time
#the newer messages are at the start meanwhile the olders at the end
#do not try to delete not existing message's id, or it will cause desync
#this class is propably slow as fork at cpython, use pypy?
    MC_GC_LIMIT=10
    __slots__=()
    def _mc_init(channel):
        #discord side bug: we cant check last message
        channel.message_history_reached_end=False
        channel._turn_gc_on_at=0
        limit=channel.MC_GC_LIMIT
        channel._mc_gc_limit=limit
        channel.messages=deque(maxlen=limit)
        
    def _get_mc_gc_limit(channel):
        return channel._mc_gc_limit
    
    def _set_mc_gc_limit(channel,limit):
        if channel._mc_gc_limit==limit:
            return
        if limit<=0:
            channel._mc_gc_limit=0
            channel.messages=deque(maxlen=0)
            return
        
        old=channel.messages
        if len(old)>limit:
            channel.messages=deque((old[i] for i in range(limit)),maxlen=limit)
        channel._mc_gc_limit=limit

    mc_gc_limit=property(_get_mc_gc_limit,_set_mc_gc_limit)
    del _get_mc_gc_limit, _set_mc_gc_limit

    def _mc_find(channel,message_id):
        if channel._mc_gc_limit==0:
            return MESSAGES.get(message_id)
        self=channel.messages
        index=message_relativeindex(self,message_id)
        if index==len(self):
            return MESSAGES.get(message_id)
        potential=self[index]
        if potential.id!=message_id:
            return MESSAGES.get(message_id)
        return potential

    #we always return the message, at the case of dupe, we return the original
    def _mc_insert_new_message(channel,message):
        self=channel.messages
        if not self:
            self.append(message)
            return message
    
        last_message_id=self[0].id
        if message.id>last_message_id:
            self.appendleft(message)
            return message
        
        if message.id==last_message_id:
            return self[0]
        
        return channel._mc_insert_asynced_message(message)
    
    def _mc_insert_old_message(channel,message):
        self=channel.messages
        if self:
            if message.id<self[-1]:
                self.append(message)
            else:
                message=channel._mc_insert_asynced_message(message)
        else:
            self.append(message)
        return message
    
    def _mc_insert_asynced_message(channel,message):
        self=channel.messages
        index=message_relativeindex(self,message.id)
        if index!=len(self):
            actual=self[index]
            if actual.id==message.id:
                return actual
        if self.maxlen is not None and self.maxlen==len(self):
            self.pop()
        self.insert(index,message)
        return message

    def _mc_pop(channel,message_id):
        if channel._mc_gc_limit==0:
            return MESSAGES.pop(message_id,None)
        self=channel.messages
        index=message_relativeindex(self,message_id)
        if index==len(self):
            return MESSAGES.pop(message_id,None)
        message=self[index]
        if message.id!=message_id:
            return MESSAGES.pop(message_id,None)
        
        del self[index]
        if channel._turn_gc_on_at:
            if len(channel.messages)<channel._mc_gc_limit:
                Q_on_GC.remove(channel)
                channel._turn_gc_on_at=0.
                switch_to_limited(channel)
                    
        return message

    def _mc_pop_multiple(channel,message_ids):
        self=channel.messages
        message_ids.sort(reverse=True)
        ln=len(self)
        result=[]
        if not ln:
            return result

        message_index=message_relativeindex(self,message_ids[0])
        if message_index==ln:
            return result

        delete_index=0
        delete_ln=len(message_ids)
        
        while True:
            message=self[message_index]
            delete_id=message_ids[delete_index]
            if message.id==delete_id:
                del self[message_index]
                result.append(message)
                ln=ln-1
                delete_index=delete_index+1
                
                if delete_index==delete_ln:
                    break
                
                if message_index==ln:
                    while True:
                        delete_id=message_ids[delete_index]
                        try:
                            message=MESSAGES[delete_id]
                        except KeyError:
                            pass
                        else:
                            result.append(message)
                        delete_index=delete_index+1
                        if delete_index==delete_ln:
                            break
                    break

                continue

            if message.id>delete_id:
                message_index=message_index+1
                if message_index==ln:
                    break
                continue

            delete_index=delete_index+1
            
            try:
                message=MESSAGES[delete_id]
            except KeyError:
                pass
            else:
                result.append(message)
            if delete_index==delete_ln:
                break

        if channel._turn_gc_on_at:
            if len(channel.messages)<channel._mc_gc_limit:
                Q_on_GC.remove(channel)
                channel._turn_gc_on_at=0.
                switch_to_limited(channel)
                
        return result
    
    def _mc_process_chunk(channel,data):
        self=channel.messages
        result=[]
        index=0
        limit=len(data)
                
        if limit<2:
            if limit==1:
                result.append(Message.fromchannel(data[0],channel))
            return result

        
        message,exists=Message.exists(data[index],channel)
        result.append(message)
        
        if exists:
            while True:
                if index==limit:
                    break
                message,exists=Message.exists(data[index],channel)
                result.append(message)
                index+=1
                if exists:
                    continue
                
                self.append(message)
                
                while True:
                    if index==limit:
                        break
                    message=Message.onetime(data[index],channel)
                    self.append(message)
                    result.append(message)
                    index+=1
                break
        else:
            while True:
                if index==limit:
                    break
                message=Message.onetime(data[index],channel)
                result.append(message)
                index+=1
        return result
    
    def _mc_generator(channel,after,before,limit):
        self=channel.messages
        if not self:
            return
        after=message_relativeindex(self,after)
        before=message_relativeindex(self,before)
        while True:
            if before==after or limit==0:
                return
            value=self[before]
            yield value
            before=before+1
            limit=limit-1

class ChannelGuildBase(ChannelBase):
    __slots__=('_cache_perm', 'category', 'guild', 'name', 'overwrites', 'position',)

    ORDER_GROUP=0

    def __gt__(self,other):
        if isinstance(other,ChannelGuildBase):
            return (
                self.ORDER_GROUP>other.ORDER_GROUP or ( \
                    self.ORDER_GROUP==other.ORDER_GROUP and ( \
                        self.position>other.position or ( \
                            self.position==other.position and self.id>other.id
                                ))))

        if isinstance(other,ChannelBase):
            return self.id>other.id

        return NotImplemented

    def __ge__(self,other):
        if isinstance(other,ChannelGuildBase):
            return (
                self.ORDER_GROUP>other.ORDER_GROUP or ( \
                    self.ORDER_GROUP==other.ORDER_GROUP and ( \
                        self.position>other.position or ( \
                            self.position==other.position and self.id>other.id
                                )) or (self.id==other.id) ))

        if isinstance(other,ChannelBase):
            return self.id>=other.id

        return NotImplemented

        
    def __le__(self,other):
        if isinstance(other,ChannelGuildBase):
            return (
                self.ORDER_GROUP<other.ORDER_GROUP or ( \
                    self.ORDER_GROUP==other.ORDER_GROUP and ( \
                        self.position<other.position or ( \
                            self.position==other.position and self.id<other.id
                                )) or (self.id==other.id) ))

        if isinstance(other,ChannelBase):
            return self.id<=other.id

        return NotImplemented
        
    def __lt__(self,other):
        if isinstance(other,ChannelGuildBase):
            return (
                self.ORDER_GROUP<other.ORDER_GROUP or ( \
                    self.ORDER_GROUP==other.ORDER_GROUP and ( \
                        self.position<other.position or ( \
                            self.position==other.position and self.id<other.id
                                ))))

        if isinstance(other,ChannelBase):
            return self.id<other.id

        return NotImplemented

    def _init_catpos(self,data,guild):
        self.guild=guild
        self.guild.all_channel[self.id]=self
        
        parent_id=data.get('parent_id',None)

        if parent_id is None:
            self.category=guild
        else:
            self.category=guild.all_channel[int(parent_id)]

        self.position=data.get('position',0)
        self.category.channels.append(self)
    
    def _set_catpos(self,data):
        position=data.get('position',0)
        parent_id=data.get('parent_id',None)
            
        if parent_id is None:
            if self.category is self.guild:
                self.category.channels.switch(self,position)
            else:
                self.category.channels.remove(self)
                self.category=self.guild
                self.position=position
                self.category.channels.append(self)
        else:
            parent_id=int(parent_id)
            if self.category.id==parent_id:
                self.category.channels.switch(self,position)
            else:
                self.category.channels.remove(self)
                self.category=self.guild.all_channel[parent_id]
                self.position=position
                self.category.channels.append(self)
                
    def _update_catpos(self,data,old):
        position=data.get('position',0)
        parent_id=data.get('parent_id',None)
        
        if parent_id is None:
            category=self.guild
        else:
            parent_id=int(parent_id)
            category=self.guild.all_channel[parent_id]

        if self.category is not category:
            old['category']=self.category
            old['position']=self.position
            
            self.category.channels.remove(self)
            self.category=category
            self.position=position
            self.category.channels.append(self)

        elif self.position!=position:
            old['position']=self.position
            self.category.channels.switch(self,position)
            
    def _permissions_for(self,user):
        guild=self.guild
        default_role=guild.roles[0]
        base=default_role.permissions
        
        try:
            roles=user.guild_profiles[guild].roles
        except KeyError:
            if type(user) is Webhook and user.channel is self:
                if self.overwrites:
                    overwrite=self.overwrites[0]

                    if overwrite.target is default_role:
                        base=(base&~overwrite.deny)|overwrite.allow
                
                return base
            
            return Permission.none
        
        else:
            for role in roles:
                base|=role.permissions
        
        if Permission.can_administrator.fget(base):
            return Permission.all
        
        overwrites=self.overwrites
        if overwrites:
            overwrite=overwrites[0]

            if overwrite.target is default_role:
                base=(base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                if overwrite.target in roles or overwrite.target is user:
                    base=(base&~overwrite.deny)|overwrite.allow

        return base

    def permissions_for(self,user):
        if user==self.guild.owner:
            return Permission.permission_all

        result=self._permissions_for(user)
        if not Permission.can_view_channel.fget(result):
            return Permission.permission_none

        return Permission(result)

    def _parse_overwrites(self,data):
        overwrites=[]
        try:
            overwrites_data=data['permission_overwrites']
        except KeyError:
            return overwrites
        if not overwrites_data:
            return overwrites
        
        default_role=self.guild.default_role
        
        for overwrite_data in overwrites_data:
            overwrite=PermOW(overwrite_data)
            if overwrite.target is default_role:
                overwrites.insert(0,overwrite)
            else:
                overwrites.append(overwrite)
        
        return overwrites
    
    def __str__(self):
        return self.name

    @property
    def users(self):
        return [user for user in self.guild.users.values() if self.permissions_for(user).can_view_channel]

    def get_user(self,name,default=None):
        if len(name)>37:
            return default
        users=self.users
        
        if len(name)>6 and name[-5]=='#':
            try:
                discriminator=int(name[-4:])
            except ValueError:
                pass
            else:
                name=name[:-5]
                for user in users:
                    if user.discriminator==discriminator and user.name==name:
                        return user
        
        if len(name)>32:
            return default

        for user in users:
            if user.name==name:
                return user
            
        guild=self.guild
        
        for user in users:
            if user.guild_profiles[guild].nick==name:
                return user
        
        return default

    def get_user_like(self,name,default=None):
        if not 1<len(name)<33:
            return default
        pattern=re.compile(re.escape(name),re.I)
        guild=self.guild
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            if pattern.match(user.name) is not None:
                return user
            nick=user.guild_profiles[guild].nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            return user
        
        return default
    
    def get_users_like(self,name):
        result=[]
        if not 1<len(name)<33:
            return result
        pattern=re.compile(re.escape(name),re.I)
        guild=self.guild
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            nick=user.guild_profiles[guild].nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            result.append(user)

        return result

    @property
    def clients(self):
        guild=self.guild
        if guild is None:
            return []
        return guild.clients

    def cached_permissions_for(self,user):
        try:
            return self._cache_perm[user.id]
        except KeyError:
            permissions=self.permissions_for(user)
            self._cache_perm[user.id]=permissions
            return permissions


class ChannelText(ChannelGuildBase,ChannelTextBase):
    __slots__=('nsfw', 'slowmode', 'topic', 'type', #guild text channel related
        '_mc_gc_limit', '_turn_gc_on_at', 'message_history_reached_end', 'messages',) #text channel related

    ORDER_GROUP=0
    INTERCHANGE=(0,5,)

    def _finish_init(self,data,client,parent):
        self._cache_perm={}
        self.name=data['name']
        self.type=data['type']
        
        self._init_catpos(data,parent)
        self.overwrites=self._parse_overwrites(data)

        self._mc_init()

        self.topic=data.get('topic','')
        self.nsfw=data.get('nsfw',False)
        self.slowmode=int(data.get('rate_limit_per_user',0))

    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        self._mc_init()
        
        self._cache_perm= {}
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.nsfw       = False
        self.overwrites = []
        self.position   = 0
        self.slowmode   = 0
        self.topic      = ''
        self.type       = int(data['type'])
        
        return self
    
    @property
    def display_name(self):
        return self.name.lower()
    
    def _update_no_return(self,data):
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.type=data['type']
        self.topic=data.get('topic','')
        self.nsfw=data.get('nsfw',False)
        self.slowmode=int(data.get('rate_limit_per_user',0))


    def _update(self,data):
        self._cache_perm.clear()
        old={}

        type_=data['type']
        if self.type!=type_:
            old['type']=self.type
            self.type=type_
            
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
                
        topic=data.get('topic','')
        if self.topic!=topic:
            old['topic']=self.topic
            self.topic=topic

        nsfw=data.get('nsfw',False)
        if self.nsfw!=nsfw:
            old['nsfw']=self.nsfw
            self.nsfw=nsfw

        slowmode=int(data.get('rate_limit_per_user',0))
        if self.slowmode!=slowmode:
            old['slowmode']=self.slowmode
            self.slowmode=slowmode

        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old['overwrites']=self.overwrites
            self.overwrites=overwrites

        self._update_catpos(data,old)
        
        return old
    
    def _delete(self,client):
        clients=self.clients
        if (not clients) or (client is not clients[0]):
            return

        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]

        if self is guild.system_channel:
            guild.system_channel=None
        if self is guild.widget_channel:
            guild.widget_channel=None    
        if self is guild.embed_channel:
            guild.embed_channel=None
        if self is guild.rules_channel:
            guild.rules_channel=None
        if self is guild.public_updates_channel:
            guild.public_updates_channel=None
        
        self.category.channels.remove(self)
        self.category=None
        
        self.overwrites.clear()
        self._cache_perm.clear()
        
    def permissions_for(self,user):
        if user==self.guild.owner:
            return Permission.permission_all_deny_voice
        
        result=self._permissions_for(user)
        if not Permission.can_view_channel.fget(result):
            return Permission.permission_none
        
        #text channels dont have voice permissions
        result&=Permission.deny_voice
        
        if self.type and (not Permission.can_manage_messages.fget(result)):
            result=result&Permission.deny_text
            return Permission(result)
        
        if not Permission.can_send_messages.fget(result):
            result=result&Permission.deny_text
        
        return Permission(result)

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        processable={}
        for key in ('name','nsfw','slowmode','topic','type_'):
            try:
                value=kwargs.pop(key)
            except KeyError:
                pass
            else:
                processable[key]=value

        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''

            channel.nsfw        = False
            channel.slowmode    = 0
            channel.topic       = ''

            channel._mc_init()
            CHANNELS[channel_id]=channel
        else:
            if not channel.partial:
                return channel

        try:
            channel.name=processable['name']
        except KeyError:
            pass

        try:
            channel.nsfw=processable['nsfw']
        except KeyError:
            pass

        try:
            channel.slowmode=processable['slowmode']
        except KeyError:
            pass

        try:
            channel.topic=processable['topic']
        except KeyError:
            pass

        try:
            type_=processable['type_']
        except KeyError:
            type_=0
        else:
            if type_ not in cls.INTERCHANGE:
                raise ValueError(f'Invalid passed type: {type_}')
        channel.type=type_
        
        return channel


class ChannelPrivate(ChannelBase,ChannelTextBase):
    __slots__=('call', 'users', #private related
        '_mc_gc_limit', '_turn_gc_on_at',  'message_history_reached_end', 'messages',) # text channel related

    INTERCHANGE=(1,)
    type=1

    def _finish_init(self,data,client,guild):
        self.users=[User(data['recipients'][0]),client]
        self.users.sort()
        self.call=None
        
        self._mc_init()

    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        self._mc_init()
        self.id         = channel_id
        #what data does this contain?
        self.call       = None
        self.users      = []
        
        return self
    
    def __str__(self):
        return f'Direct Message {self.users[0]:f} with {self.users[1]:f}'

    def _delete(self,client):
        del client.channels[self.id]

        users=self.users
        if client is users[0]:
            user=users[1]
        else:
            user=users[0]
        
        del client.private_channels[user.id]

    name=property(__str__)
    display_name=name
    
    def permissions_for(self,user):
        if user in self.users:
            if user.is_bot:
                return Permission.permission_private_bot
            else:
                return Permission.permission_private
            
        return Permission.permission_none

    cached_permissions_for=permissions_for

    @property
    def guild(self):
        return None

    @classmethod
    def _dispatch(cls,data,client):
        channel_id=int(data['id'])
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            CHANNELS[channel_id]=channel
            client.channels[channel_id]=channel
            channel._finish_init(data,client,None)
            result=channel
        else:
            result=None #returning None is intended.

        if channel.users[0] is client:
            user=channel.users[1]
        else:
            user=channel.users[0]
        client.private_channels[user.id]=channel

        return result

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel.call        = None
            channel.users       = []

            channel._mc_init()
            CHANNELS[channel_id]=channel
        
        return channel


class ChannelVoice(ChannelGuildBase):
    __slots__=('bitrate',  'user_limit') #Voice channel related

    ORDER_GROUP=2
    INTERCHANGE=(2,)
    type=2

    def _finish_init(self,data,client,parent):
        self._cache_perm={}
        self.name=data['name']
        
        self._init_catpos(data,parent)
        self.overwrites=self._parse_overwrites(data)
        
        self.bitrate=data['bitrate']
        self.user_limit=data['user_limit']

    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.bitrate    = 0
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.overwrites = []
        self.position   = 0
        self.user_limit = 0
        
        return self
    
    @property
    def display_name(self):
        return self.name.capitalize()
    
    def _delete(self,client):
        clients=self.clients
        if (not clients) or (client is not clients[0]):
            return
        
        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
        #safe delete

        if self is guild.afk_channel:
            guild.afk_channel=None
            
        self.overwrites.clear()
        self._cache_perm.clear()
        
    def _update_no_return(self,data):
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.bitrate=data['bitrate']
        self.user_limit=data['user_limit']

    def _update(self,data):
        self._cache_perm.clear()
        old={}

        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
                
        bitrate=data['bitrate']
        if self.bitrate!=bitrate:
            old['bitarate']=self.bitrate
            self.bitrate=bitrate

        user_limit=data['user_limit']
        if self.user_limit!=user_limit:
            old['user_limit']=self.user_limit
            self.user_limit=user_limit

        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old['overwrites']=self.overwrites
            self.overwrites=overwrites

        self._update_catpos(data,old)
        
        return old

    def permissions_for(self,user):
        if user==self.guild.owner:
            return Permission.permission_all_deny_text
        
        result=self._permissions_for(user)
        if not Permission.can_view_channel.fget(result):
            return Permission.permission_none

        #voice channels dont have text permissions
        result&=Permission.deny_text

        if not Permission.can_connect.fget(result):
            result&=Permission.deny_voice_con
        
        return Permission(result)
        
    @property
    def voice_users(self):
        result=[]
        for state in self.guild.voice_states.values():
            if state.channel is self:
                result.append(state.user)
        return result

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        processable={}
        for key in ('name', 'bitrate', 'user_limit'):
            try:
                value=kwargs.pop(key)
            except KeyError:
                pass
            else:
                processable[key]=value

        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''

            channel.bitrate     = 64000
            channel.user_limit  = 0
            CHANNELS[channel_id]=channel
        else:
            if not channel.partial:
                return channel

        try:
            channel.name=processable['name']
        except KeyError:
            pass

        try:
            channel.bitrate=processable['bitrate']
        except KeyError:
            pass

        try:
            channel.user_limit=processable['user_limit']
        except KeyError:
            pass
        
        return channel


class ChannelGroup(ChannelBase,ChannelTextBase):
    __slots__=('call', 'users', # private channel related
        'icon', 'name', 'owner', #group channel related
        '_mc_gc_limit', '_turn_gc_on_at', 'message_history_reached_end', 'messages') # text channel related

    INTERCHANGE=(3,)
    type=3

    def _finish_init(self,data,client,parent):
        self._mc_init()
        
        name=data.get('name',None)
        self.name = '' if name is None else name
        
        icon=data.get('icon')
        self.icon=0 if icon is None else int(icon,16)
        self.call=None
        
        users=[User(user_data) for user_data in data['recipients']]
        users.sort()
        self.users=users
        
        owner_id=int(data['owner_id'])
        for user in users:
            if user.id==owner_id:
                self.owner=user
                break
        else:
            self.owner=ZEROUSER
        
    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        self._mc_init()
        self.id         = channel_id
        self.call       = None
        # even if we get recipients, we will ignore them
        self.users      = []
        
        icon=data.get('icon')
        self.icon=0 if icon is None else int(icon,16)
        
        name=data.get('name',None)
        #should we transfer the recipients to name?
        self.name='' if name is None else name
        
        self.owner=ZEROUSER
        
        return self
    
    def _delete(self,client):
        del client.channels[self.id]

    def _update_no_return(self,data):
        name=data.get('name',None)
        self.name = '' if name is None else name

        icon=data.get('icon',None)
        self.icon=0 if icon is None else int(icon,16)
        
        self.users=[User(user) for user in data['recipients']]
        self.users.sort()

        owner_id=int(data['owner_id'])
        for user in self.users:
            if user.id==owner_id:
                self.owner=user
                break

    def _update(self,data):
        old={}
        
        name=data.get('name',None)
        if name is None:
            name=''
        if self.name!=name:
            old['name']=self.name
            self.name=name

        icon=data.get('icon',None)
        icon=0 if icon is None else int(icon,16)
        if self.icon!=icon:
            old['icon']=self.icon
            self.icon=icon
        
        users=[User(user) for user in data['recipeents']]
        if self.users!=users:
            old['users']=self.users
            self.users=users
        
        owner_id=int(data['owner_id'])
        if self.owner.id!=owner_id:
            for user in self.users:
                if user.id==owner_id:
                    owner=user
                    break
            else:
                owner=ZEROUSER
            old['owner']=self.owner
            self.owner=owner

        return old

    def __str__(self):
        name=self.name
        if name:
            return name
        
        users=self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'

    display_name=property(__str__)

    def permissions_for(self,user):
        if self.owner==user:
            return Permission.permission_group_owner
        elif user in self.users:
            return Permission.permission_group
        else:
            return Permission.permission_none

    cached_permissions_for=permissions_for
    
    guild=ChannelPrivate.guild

    @classmethod
    def _dispatch(cls,data,client):
        channel_id=int(data['id'])
        if channel_id in CHANNELS:
            return

        channel=object.__new__(cls)
        channel.id=channel_id
        CHANNELS[channel_id]=channel
        client.channels[channel_id]=channel
        channel._finish_init(data,client,None)
        return channel

    icon_url=property(URLS.channel_group_icon_url)
    icon_url_as=URLS.channel_group_icon_url_as

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        processable={}
        for key in ('icon', 'name', 'owner'):
            try:
                value=kwargs.pop(key)
            except KeyError:
                pass
            else:
                processable[key]=value

        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel.call        = None
            channel.users       = []

            channel.name        = ''
            channel.icon        = 0
            channel.owner       = None
            CHANNELS[channel_id]=channel
        else:
            if not channel.partial:
                return channel

        try:
            channel.name=processable['name']
        except KeyError:
            pass

        icon=_parse_ih_fs(kwargs.pop('icon',None))
        if icon:
            channel.icon=icon

        try:
            channel.owner=processable['owner']
        except KeyError:
            pass
        
        return channel

class ChannelCategory(ChannelGuildBase):
    __slots__=('channels',) #channel category related

    ORDER_GROUP=4
    INTERCHANGE=(4,)
    type=4

    def _finish_init(self,data,client,parent):
        self._cache_perm={}
        self.name=data['name']
        
        self._init_catpos(data,parent)
        self.overwrites=self._parse_overwrites(data)
        
        self.channels=weakposlist()
    
    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.category   = None
        self.channels   = weakposlist()
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.overwrites = []
        self.position   = 0
        
        return self
        
    @property
    def display_name(self):
        return self.name.upper()
    
    def _delete(self,client):
        clients=self.clients
        if (not clients) or (client is not clients[0]):
            return

        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
        
        #self.channels.clear() #if this really happens we will know it
        self.overwrites.clear()
        self._cache_perm.clear()
        
    def _update_no_return(self,data):
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        
    def _update(self,data):
        self._cache_perm.clear()
        old={}

        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name

        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old['overwrites']=self.overwrites
            self.overwrites=overwrites

        self._update_catpos(data,old)
        
        return old

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        processable={}
        for key in ('name',):
            try:
                value=kwargs.pop(key)
            except KeyError:
                pass
            else:
                processable[key]=value

        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''
            CHANNELS[channel_id]=channel
        else:
            if not channel.partial:
                return channel

        try:
            channel.name=processable['name']
        except KeyError:
            pass
        
        return channel


class ChannelStore(ChannelGuildBase):
    __slots__=('nsfw',) #guild channel store related

    ORDER_GROUP=0
    INTERCHANGE=(6,)
    type=6

    def _finish_init(self,data,client,parent):
        self._cache_perm={}
        self.name=data['name']
        self.nsfw=data.get('nsfw',False)
        
        self._init_catpos(data,parent)
        self.overwrites=self._parse_overwrites(data)
    
    @classmethod
    def _from_partial_data(cls,data,channel_id,partial_guild):
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.nsfw       = False
        self.overwrites = []
        self.position   = 0
        
        return self
        
    @property
    def display_name(self):
        return self.name.lower()
    
    def _update_no_return(self,data):
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.nsfw=data.get('nsfw',False)
        
    def _update(self,data):
        self._cache_perm.clear()
        old={}

        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name

        nsfw=data.get('nsfw',False)
        if self.nsfw!=nsfw:
            old['nsfw']=self.nsfw
            self.nsfw=nsfw

        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old['overwrites']=self.overwrites
            self.overwrites=overwrites

        self._update_catpos(data,old)
        
        return old
    
    def _delete(self,client):
        clients=self.clients
        if (not clients) or (client is not clients[0]):
            return

        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
            
        self.overwrites.clear()
        self._cache_perm.clear()

    def permissions_for(self,user):
        if user==self.guild.owner:
            return Permission.permission_all_deny_both
        
        result=self._permissions_for(user)
        if not Permission.can_view_channel.fget(result):
            return Permission.permission_none

        #store channels do not have text and voice related permissions
        result&=Permission.deny_both
        
        return Permission(result)

    @classmethod
    def precreate(cls,channel_id,**kwargs):
        processable={}
        for key in ('name','nsfw'):
            try:
                value=kwargs.pop(key)
            except KeyError:
                pass
            else:
                processable[key]=value

        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')

        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''

            channel.nsfw        = False
            CHANNELS[channel_id]=channel
        else:
            if not channel.partial:
                return channel

        try:
            channel.name=processable['name']
        except KeyError:
            pass

        try:
            channel.nsfw=processable['nsfw']
        except KeyError:
            pass
        
        return channel

CHANNEL_TYPES = (
    ChannelText,
    ChannelPrivate,
    ChannelVoice,
    ChannelGroup,
    ChannelCategory,
    ChannelText,
    ChannelStore,
        )

def cr_pg_channel_object(name, type_, overwrites=None, topic=None, nsfw=False,
        slowmode=0, bitrate=64000, user_limit=0, bitrate_limit=96000,
        category_id=None):
    
    if type(type_) is int:
        if type_<0:
            raise ValueError(f'`type_` cannot be negative value, got `{type_!r}`')
        if type_>=len(CHANNEL_TYPES):
            raise ValueError(f'`type_` exceeded the defined channel type limit. Limit: `{len(CHANNEL_TYPES)-1!r}`, got `{type_}`')
        
        if not isinstance(CHANNEL_TYPES[type_],ChannelGuildBase):
            raise ValueError(f'The function accepts only guild channel types, got `{type_!r}`')
            
        type_value=CHANNEL_TYPES[type_]
    
    elif isinstance(type_,type) and issubclass(type_,ChannelBase):
        if not isinstance(type_,ChannelGuildBase):
            raise ValueError(f'The function accepts only guild channel types, got `{type_!r}`')
        type_value=type_.INTERCHANGE[0]
    
    else:
        raise ValueError(f'\'type_\' argument should be int or Channel type, got {type!r}')
    
    name_ln=len(name)
    if name_ln<2 or name_ln>100:
        raise ValueError(f'`name` length should be between 2-100, got `{name_ln}`')
    
    if overwrites is None:
        overwrites=[]
    
    result = {
        'name'                  : name,
        'type'                  : type_value,
        'permission_overwrites' : overwrites,
            }
    
    # any Guild Text channel type
    if type_value in ChannelText.INTERCHANGE:
        if (topic is not None):
            topic_ln=len(topic)
            if topic_ln>1024:
                raise ValueError(f'`topic` length can be betwen 0-1024, got `{topic_ln}`')
            if topic_ln!=0:
                result['topic']=topic
    
    # any Guild Text or any Guild Store channel type
    if (type_value in ChannelText.INTERCHANGE) or (type_value in ChannelStore.INTERCHANGE):
        if nsfw:
            result['nsfw']=nsfw
    
    # Guild Text channel type only
    if type_value == ChannelText.INTERCHANGE[0]:
        if slowmode<0 or slowmode>21600:
            raise ValueError(f'Invalid `slowmode`, should be 0-21600, got `{slowmode!r}`')
        result['rate_limit_per_user']=slowmode
    
    # any Guild Voice channel type
    if type_value in ChannelVoice.INTERCHANGE:
        if bitrate<8000 or bitrate>bitrate_limit:
            raise ValueError(f'`bitrate` should be 8000-96000. 128000 max for vip, or 128000, 256000, 384000 max depends on premium tier. Got `{bitrate!r}`,')
        result['bitrate']=bitrate

        if user_limit<0 or user_limit>99:
            raise ValueError(f'`user_limit` should be 0 for unlimited or 1-99, got `{user_limit!r}`')
        result['user_limit']=user_limit
    
    if type_value not in ChannelCategory.INTERCHANGE[0]:
        if (category_id is not None):
            result['parent_id']=category_id
    
    return result

#scopes

webhook.ChannelText=ChannelText
message.ChannelBase=ChannelBase
message.ChannelTextBase=ChannelTextBase
message.ChannelGuildBase=ChannelGuildBase
message.ChannelText=ChannelText
message.ChannelPrivate=ChannelPrivate
message.ChannelGroup=ChannelGroup

del message
del webhook
del URLS
