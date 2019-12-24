# -*- coding: utf-8 -*-
__all__ = ('Attachment', 'Message', 'MessageActivity', 'MessageActivityType',
    'MessageApplication', 'MessageFlag', 'MessageReference', 'MessageType',
    'UnknownCrossMention', )

import re
from datetime import datetime

from .dereaddons_local import any_to_any, autoposlist, cached_property,     \
    _spaceholder

from .others import parse_time, CHANNEL_MENTION_RP, id_to_time, VoiceRegion
from .client_core import MESSAGES, CHANNELS, GUILDS
from .user import USERS, ZEROUSER, User, PartialUser, VoiceState
from .emoji import reaction_mapping
from .embed import EmbedCore, EXTRA_EMBED_TYPES
from .webhook import WebhookRepr, PartialWebhook, WebhookType

where=autoposlist.where

ChannelBase=NotImplemented

class MessageFlag(int):
    __slots__=()

    @property
    def crossposted(self):
        return self&1

    @property
    def is_crosspost(self):
        return (self>>1)&1

    @property
    def embeds_suppressed(self):
        return (self>>2)&1

    
    @property
    def source_message_deleted(self):
        return (self>>3)&1
    
    @property
    def urgent(self):
        return (self>>4)&1
    
    def __iter__(self):
        if self&1:
            yield 'crossposted'
            
        if (self>>1)&1:
            yield 'is_crosspost'
            
        if (self>>2)&1:
            yield 'embeds_suppressed'

        if (self>>3)&1:
            yield 'source_message_deleted'

        if (self>>4)&1:
            yield 'urgent'
            
    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

class MessageActivityType(object):
    # class related
    INSTANCES = [NotImplemented] * 6
    
    # object related
    __slots__=('name', 'value', )
    
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none        = NotImplemented
    join        = NotImplemented
    spectate    = NotImplemented
    listen      = NotImplemented
    join_request= NotImplemented

MessageActivityType.none           = MessageActivityType(0,'none')
MessageActivityType.join           = MessageActivityType(1,'join')
MessageActivityType.spectate       = MessageActivityType(2,'spectate')
MessageActivityType.listen         = MessageActivityType(3,'listen')
MessageActivityType.join_request   = MessageActivityType(5,'join_request')

class MessageActivity(object):
    __slots__ = ('party_id', 'type',)
    def __init__(self,data):
        self.party_id=data.get('party_id','')
        self.type=MessageActivityType.INSTANCES[data['type']]

    def __eq__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.party_id!=other.party_id:
            return False
        
        return True
    
    def __repr__(self):
        return f'<{self.__class__.__name__} type={self.type.name} ({self.type.value}), party_id={self.party_id!r}>'
    
class Attachment(object):
    __slots__=('name', 'height', 'id', 'proxy_url', 'size', 'url', 'width',)
    def __init__(self,data):
        self.name       = data['filename']
        self.id         = int(data['id'])
        self.proxy_url  = data['proxy_url']
        self.size       = data['size']
        self.url        = data['url']
        self.height     = data.get('height',0)
        self.width      = data.get('width',0)

    def __gt__(self,other):
        if type(self) is type(other):
            return self.id>other.id
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.id>=other.id
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.id!=other.id
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.id<=other.id
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.id<other.id
        return NotImplemented

    def __hash__(self):
        return self.id
    
class MessageApplication(object):
    __slots__=('cover', 'description', 'icon', 'id', 'name',)
    def __init__(self,data):
        cover = data.get('cover_image',None)
        self.cover      = 0 if cover is None else int(cover,16)
        self.description= data['description']
        icon=data['icon']
        self.icon       = 0 if icon is None else int(icon,16)
        self.id         = int(data['id'])
        self.name       = data['name']

    def __gt__(self,other):
        if type(self) is type(other):
            return self.id>other.id
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.id>=other.id
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.id!=other.id
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.id<=other.id
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.id<other.id
        return NotImplemented

    def __hash__(self):
        return self.id

class MessageReference(object):
    __slots__=('_cache', 'data',)
    def __init__(self,data):
        self._cache={}
        self.data=data

    @cached_property
    def channel_id(self):
        channel_id=self.data.get('channel_id')
        if channel_id is None:
            return 0
        return int(channel_id)

    @cached_property
    def guild_id(self):
        guild_id=self.data.get('guild_id')
        if guild_id is None:
            return 0
        return int(guild_id)

    @cached_property
    def message_id(self):
        message_id=self.data.get('message_id')
        if message_id is None:
            return 0
        return int(message_id)

    @cached_property
    def channel(self):
        try:
            channel_id=self._cache['channel_id']
        except KeyError:
            channel_id=self.data.get('channel_id')
            if channel_id is None:
                self._cache['channel_id']=0
                return
            channel_id=int(channel_id)
            self._cache['channel_id']=channel_id
        else:
            if channel_id==0:
                return
        return CHANNELS.get(channel_id)

    @cached_property
    def guild(self):
        try:
            guild_id=self._cache['guild_id']
        except KeyError:
            guild_id=self.data.get('guild_id')
            if guild_id is None:
                self._cache['guild_id']=0
                return
            guild_id=int(guild_id)
            self._cache['guild_id']=guild_id
        else:
            if guild_id==0:
                return
        return GUILDS.get(guild_id)

    @cached_property
    def message(self):
        channel=self.channel
        if channel is None:
            return None

        try:
            message_id=self._cache['message_id']
        except KeyError:
            message_id=self.data.get('message_id')
            if message_id is None:
                self._cache['message_id']=0
                return
            message_id=int(message_id)
            self._cache['message_id']=message_id
        else:
            if message_id==0:
                return

        return channel._mc_find(message_id)

class UnknownCrossMention(object):
    __slots__=('guild_id', 'id', 'name', 'type',)
    def __new__(cls,data):
        channel_id=int(data['id'])
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            channel.guild_id=int(data['guild_id'])
            channel.type=data['type']
            channel.name=data['name']

        return channel

    def __init__(self,data):
        pass

    def __gt__(self,other):
        if type(other) is UnknownCrossMention:
            return self.id>other.id
        return NotImplemented

    def __ge__(self,other):
        if type(other) is type(self) or isinstance(other,ChannelBase):
            return self.id>=other.id
        return NotImplemented

    def __eq__(self,other):
        if type(other) is type(self) or isinstance(other,ChannelBase):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if type(other) is type(self) or isinstance(other,ChannelBase):
            return self.id!=other.id
        return NotImplemented

    def __le__(self,other):
        if type(other) is type(self) or isinstance(other,ChannelBase):
            return self.id<=other.id
        return NotImplemented

    def __lt__(self,other):
        if type(other) is type(self) or isinstance(other,ChannelBase):
            return self.id<other.id
        return NotImplemented

class Message(object):
    __slots__=('__weakref__', '_channel_mentions', 'activity', 'application',
        'attachments', 'author', 'call', 'channel', 'content',
        'cross_mentions', 'cross_reference', 'edited', 'embeds',
        'everyone_mention', 'flags', 'id', 'nonce', 'pinned', 'reactions',
        'reference', 'role_mentions', 'tts', 'type', 'user_mentions',)
    
    def __init__(self,data,channel):
        raise RuntimeError(f'`{self.__class__.__name__}` should not be created like this.')

    def weakrefer(self):
        MESSAGES[self.id]=self

    @classmethod
    def new(cls,data,channel):
        new=object.__new__(cls)
        new.id=int(data['id'])
        if channel._mc_gc_limit:
            self=channel._mc_insert_new_message(new)
            if new is self:
                self._finish_init(data,channel)
                if channel.message_history_reached_end:
                    if channel.messages.maxlen is not None and len(channel.messages)==channel._mc_gc_limit:
                        channel.message_history_reached_end=False
            return self
        new._finish_init(data,channel)
        return new
    
    @classmethod
    def old(cls,data,channel):
        new=object.__new__(cls)
        new.id=int(data['id'])
        self=channel._mc_insert_old_message(new)
        if new is self:
            self._finish_init(data,channel)
        return self
    
    #this is a safe method to not get duped messages.
    #1st it tries to find it. If it finds nothing, return a new,
    #w/o addding it to the channel history
    @classmethod
    def fromchannel(cls,data,channel):
        message_id=int(data['id'])
        message=channel._mc_find(message_id)
        if message:
            return message
        message=object.__new__(cls)
        message.id=message_id
        message._finish_init(data,channel)
        return message

    #called, when we wanna know if the message existed before or not
    @classmethod
    def exists(cls,data,channel):
        message_id=int(data['id'])
        message=channel._mc_find(message_id)
        if message is not None:
            return message,True
        message=object.__new__(cls)
        message.id=message_id
        message._finish_init(data,channel)
        return message,False

    #we call this only if we know our messae never existed
    @classmethod
    def onetime(cls,data,channel):
        message_id=int(data['id'])
        message=object.__new__(cls)
        message.id=message_id
        message._finish_init(data,channel)
        return message

    def _finish_init(self,data,channel):
        self.channel=channel
        guild=channel.guild
        webhook_id=data.get('webhook_id',None)
        author_data=data.get('author',None)
        if webhook_id is None:
            self.cross_reference=None
            self.cross_mentions=None
            if author_data is None:
                self.author=ZEROUSER
            else:
                try:
                     author_data['member']=data['member']
                except KeyError:
                    pass
                self.author=User(author_data,guild)
        else:
            cross_reference_data=data.get('message_reference',None)
            is_cross=(cross_reference_data is not None)
            if is_cross:
                self.cross_reference=MessageReference(cross_reference_data)
                
                cross_mention_datas=data.get('mention_channels',None)
                if cross_mention_datas is None:
                    self.cross_mentions=None
                else:
                    self.cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
                    self.cross_mentions.sort()
                webhook_type=WebhookType.server
            else:
                self.cross_reference=None
                self.cross_mentions=None
                webhook_type=WebhookType.bot
            
            if author_data is None:
                self.author=PartialWebhook(int(webhook_id),'',type_=webhook_type)
            else:
                self.author=WebhookRepr(author_data,int(webhook_id),type_=webhook_type)

        #the message might contain guild member data too
        #but we just gonna ignore that

        self.reactions=reaction_mapping(data.get('reactions',None))

        try:
            self.application=MessageApplication(data['application'])
        except KeyError:
            self.application=None

        try:
            activity_data=data['activity']
        except KeyError:
            self.activity=None
        else:
            self.activity=MessageActivity(activity_data)

        edited=data['edited_timestamp']
        if edited is not None:
            edited=parse_time(edited)
        self.edited=edited
            
        self.pinned=data.get('pinned',False)
        self.everyone_mention=data.get('mention_everyone',False)
        self.tts=data.get('tts',False)
        self.type=MessageType.INSTANCES[data['type']]
        
        attachments=data['attachments']
        if attachments:
            self.attachments=[Attachment(attachment) for attachment in attachments]
        else:
            self.attachments=None
            
        embed_datas=data['embeds']
        if embed_datas:
            self.embeds=[EmbedCore.from_data(embed) for embed in embed_datas]
        else:
            self.embeds=None

        self.nonce=data.get('nonce',None)
        self.content=data['content']
        self.flags=MessageFlag(data.get('flags',0))

        call_data=data.get('call',None)
        if call_data is None or self.type is not MessageType.call:
            self.call=None
        else:
            self.call=MessageCall(self,call_data)
        
        user_mention_datas=data['mentions']
        if user_mention_datas:
            self.user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
            self.user_mentions.sort()
        else:
            self.user_mentions=None

        if guild is None:
            self._channel_mentions=None
            self.role_mentions=None
            self.cross_mentions=None
            self.cross_reference=None
            return
        
        self._channel_mentions=_spaceholder

        try:
            role_mention_ids=data['mention_roles']
        except KeyError:
            role_mentions=None
        else:
            if role_mention_ids:
                roles=guild.all_role
                role_mentions=[]
                for role_id in role_mention_ids:
                    try:
                        role_mentions.append(roles[int(role_id)])
                    except KeyError:
                        continue
                role_mentions.sort()
            else:
                role_mentions=None
                
        self.role_mentions=role_mentions
        
    def _parse_channel_mentions(self):
        content=self.content
        channel_mentions=[]
        channels=self.channel.guild.all_channel
        cross_mentions=self.cross_mentions

        for channel_id in CHANNEL_MENTION_RP.findall(content):
            channel_id=int(channel_id)
            try:
                channel=channels[channel_id]
            except KeyError:
                if cross_mentions is None:
                    continue
                try:
                    channel=cross_mentions[channel_id]
                except KeyError:
                    continue
            if channel not in channel_mentions:
                channel_mentions.append(channel)
        channel_mentions.sort()

        if channel_mentions:
            self._channel_mentions=channel_mentions
            return channel_mentions
        self._channel_mentions=None
    
    @property
    def channel_mentions(self):
        result=self._channel_mentions
        if result is _spaceholder:
            return self._parse_channel_mentions()
        return result
    
    def __gt__(self,other):
        if type(self) is type(other):
            return self.id>=other.id
        return NotImplemented
    
    def __ge__(self,other):
        if type(self) is type(other):
            return self.id>=other.id
        return NotImplemented
    
    def __eq__(self,other):
        if type(self) is type(other):
            return self.id==other.id
        return NotImplemented
    
    def __ne__(self,other):
        if type(self) is type(other):
            return self.id!=other.id
        return NotImplemented
    
    def __le__(self,other):
        if type(self) is type(other):
            return self.id<=other.id
        return NotImplemented
    
    def __lt__(self,other):
        if type(self) is type(other):
            return self.id<other.id
        return NotImplemented

    def __hash__(self):
        return self.id
    
    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} ln={len(self)} author={self.author:f}>'

    def __format__(self,code):
        if not code:
            return self.__repr__()
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        if code=='e':
            if self.edited:
               return f'{self.edited:%Y.%m.%d-%H:%M:%S}'
            return 'never'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')

        
    def _update(self,data):
        old={}

        pinned=data['pinned']
        if self.pinned!=pinned:
            old['pinned']=self.pinned
            self.pinned=pinned

        flags=MessageFlag(data.get('flags',0))
        if self.flags!=flags:
            old['flags'] = self.flags
            self.flags = flags
            value = (flags&0b00000100)>>2
            embeds=self.embeds
            if embeds is not None:
                for embed in self.embeds:
                    embed.suppressed=value
                
        #at the case of pin update edited is None
        edited_timestamp=data['edited_timestamp']
        if edited_timestamp is None:
            return old
        
        edited=parse_time(edited_timestamp)
        if self.edited==edited:
            return old
        
        old['edited']=self.edited
        self.edited=edited

        try:
            application=MessageApplication(data['application'])
        except KeyError:
            application=None
        
        if self.application!=application:
            old['application']=self.application
            self.application=self.application
        
        try:
            activity_data=data['activity']
        except KeyError:
            activity=None
        else:
            activity=MessageActivity(activity_data)
        
        if self.activity is None:
            if (activity is not None):
                old['activity']=None
                self.activity=activity
        else:
            if activity is None:
                old['activity']=self.activity
                self.activity=None
            elif self.activity!=activity:
                old['activity']=self.activity
                self.activity=activity
                    
        everyone_mention=data.get('mention_everyone',False)
        if self.everyone_mention!=everyone_mention:
            old['everyone_mention']=self.everyone_mention
            self.everyone_mention=everyone_mention

        #ignoring tts
        #ignoring type
        #ignoring nonce
        #ignoring attachments

        embed_datas=data['embeds']
        if embed_datas:
            embeds=[EmbedCore.from_data(embed) for embed in embed_datas]
        else:
            embeds=None
        if self.embeds!=embeds:
            old['embeds']=self.embeds
            self.embeds=embeds
            
        content=data['content']
        if self.content!=content:
            old['content']=self.content
            self.content=content

        user_mention_datas=data['mentions']

        guild=self.channel.guild
        
        if user_mention_datas:
            user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
            user_mentions.sort()
        else:
            user_mentions=None

        if self.user_mentions is None:
            if (user_mentions is not None):
                old['user_mentions']=None
                self.user_mentions=user_mentions
        else:
            if user_mentions is None:
                old['user_mentions']=self.user_mentions
                self.user_mentions=None
            else: 
                if self.user_mentions!=user_mentions:
                    old['user_mentions']=self.user_mentions
                    self.user_mentions=user_mentions
        
        if guild is None:
            return old

        self._channel_mentions=_spaceholder

        cross_mention_datas=data.get('mention_channels',None)
        if cross_mention_datas is None:
            cross_mentions=None
        else:
            cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
            cross_mentions.sort()

        if self.cross_mentions is None:
            if (cross_mentions is not None):
                old['cross_mentions']=None
                self.cross_mentions=cross_mentions
        else:
            if cross_mentions is None:
                old['cross_mentions']=self.cross_mentions
                self.cross_mentions=None
            else:
                if self.cross_mentions!=cross_mentions:
                    old['cross_mentions']=self.cross_mentions
                    self.cross_mentions=cross_mentions

        try:
            role_mention_ids=data['mention_roles']
        except KeyError:
            role_mentions=None
        else:
            if role_mention_ids:
                roles=guild.all_role
                role_mentions=[]
                for role_id in role_mention_ids:
                    try:
                        role_mentions.append(roles[int(role_id)])
                    except KeyError:
                        continue
                role_mentions.sort()
            else:
                role_mentions=None

        if self.role_mentions is None:
            if (role_mentions is not None):
                old['role_mentions']=None
                self.role_mentions=role_mentions
        else:
            if role_mentions is None:
                old['role_mentions']=self.role_mentions
                self.role_mentions=None
            else:
                if self.role_mentions!=role_mentions:
                    old['role_mentions']=self.role_mentions
                    self.role_mentions=role_mentions

        return old     
    
    @property
    def guild(self):
        return self.channel.guild

    @property
    def clean_content(self):
        return self.type.convert(self)
    
    @property
    def created_at(self):
        return id_to_time(self.id)

    def _update_no_return(self,data):
        self.pinned=data['pinned']
        flags=MessageFlag(data.get('flags',0))
        if self.flags!=flags:
            self.flags = flags
            value = (flags&0b00000100)>>2
            embeds=self.embeds
            if embeds is not None:
                for embed in self.embeds:
                    embed.suppressed=value

        edited_timestamp=data['edited_timestamp']
        if edited_timestamp is None:
            return
        
        edited=parse_time(edited_timestamp)
        if self.edited==edited:
            return
        self.edited=edited

        try:
            self.application=MessageApplication(data['application'])
        except KeyError:
            self.application=None

        try:
            activity_data=data['activity']
        except KeyError:
            self.activity=None
        else:
            self.activity=MessageActivity(activity_data)

        self.everyone_mention=data['mention_everyone']

        #ignoring tts
        #ignoring type
        #ignoring nonce
        #ignoring attachments

        embed_datas=data['embeds']
        if embed_datas:
            embeds=self.embeds
            if embeds is None:
                embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
                self.embeds=embeds
            else:
                embeds.clear()
                embeds.extend(EmbedCore.from_data(embed_data) for embed_data in embed_datas)
        else:
            self.embeds=None

        self.content=data['content']

        user_mention_datas=data['mentions']

        guild=self.channel.guild
        
        if user_mention_datas:
            user_mentions=self.user_mentions
            if user_mentions is None:
                user_mentions=[User(user_mention_data,guild) for user_mention_data in user_mention_datas]
                self.user_mentions=user_mentions
            else:
                user_mentions.clear()
                user_mentions.extend(User(user_mention_data,guild) for user_mention_data in user_mention_datas)
            user_mentions.sort()
        else:
            self.user_mentions=None

        if guild is None:
            return

        self._channel_mentions=_spaceholder

        cross_mention_datas=data.get('mention_channels',None)
        if cross_mention_datas is None:
            self.cross_mentions=None
        else:
            cross_mentions=[UnknownCrossMention(cross_mention_data) for cross_mention_data in cross_mention_datas]
            cross_mentions.sort()
            self.cross_mentions=cross_mentions
        
        try:
            role_mention_ids=data['role_mentions']
        except KeyError:
            self.role_mentions=None
        else:
            if role_mention_ids:
                role_mentions=self.role_mentions
                if role_mentions is None:
                    role_mentions=[]
                    self.role_mentions=role_mentions
                else:
                    role_mentions.clear()
                
                roles=guild.all_role
                for role_id in role_mention_ids:
                    try:
                        role_mentions.append(roles[int(role_id)])
                    except KeyError:
                        continue
                role_mentions.sort()
            else:
                self.role_mentions=None
        
    def _update_embed(self,data):
        #this function gets called after embed message. Propably only auto
        #sizes get updated, so we gonna do the same
        try:
            embed_datas=data['embeds']
        except KeyError:
            return 0

        embeds=self.embeds
        if embeds is None:
            self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return 2|((self.flags>>2)&1)
        
        ln1=len(embeds)
        
        changed=0
        for index in range(ln1):
            changed|=embeds[index]._update_sizes(embed_datas[index])

        ln2=len(embed_datas)
        if ln1==ln2:
            return changed
        
        for index in range(ln1,ln2):
            embeds.append(EmbedCore.from_data(embed_datas[index]))
        
        return 2

    def _update_embed_no_return(self,data):
        try:
            embed_datas=data['embeds']
        except KeyError:
            return

        embeds=self.embeds
        if embeds is None:
            self.embeds=[EmbedCore.from_data(embed_data) for embed_data in embed_datas]
            return

        ln1=len(embeds)

        for index in range(ln1):
            embeds[index]._update_sizes_no_return(embed_datas[index])

        ln2=len(embed_datas)
        if ln1==ln2:
            return

        for index in range(ln1,ln2):
            embeds.append(EmbedCore.from_data(embed_datas[index]))


    @property
    def contents(self):
        result=[]
        if self.content:
            result.append(self.content)
        
        if self.embeds is not None:
            for embed in self.embeds:
                result.extend(embed.contents)

        return result

    @property
    def mentions(self):
        result=[]
        if self.everyone_mention:
            result.append(None)
            
        if self.user_mentions is not None:
            result.extend(self.user_mentions)
            
        if self.role_mentions is not None:
            result.extend(self.role_mentions)
            
        channel_mentions=self.channel_mentions
        if channel_mentions is not None:
            result.extend(channel_mentions)

        return result  
        
    def __len__(self):
        if self.type is MessageType.default:
            result=len(self.content)
        else:
            result=len(self.clean_content)

        if self.embeds is not None:
            for embed in self.embeds:
                if embed.type in EXTRA_EMBED_TYPES:
                    break
                result+=len(embed)
        return result

    @property
    def clean_embeds(self):
        result=[]
        embeds=self.embeds
        if embeds is None:
            return result
        for embed in embeds:
            if embed.type in EXTRA_EMBED_TYPES:
                continue
            result.append(embed._clean_copy(self))
        return result

    @property
    def could_suppress_embeds(self):
        embeds=self.embeds
        if embeds is None:
            return 0

        can_suppress=len(embeds)
        for embed in embeds:
            can_suppress-=embed.suppressed
        return can_suppress

    def did_react(self,emoji,user):
        try:
            reacters=self.reactions[emoji]
        except KeyError:
            return False
        return (user in reacters)

class MessageType(object):
    # class related
    INSTANCES = [NotImplemented] * 14
    
    # object related
    __slots__=('name', 'value', 'convert',)
    
    def __init__(self,value,name,converter):
        self.value  = value
        self.name   = name
        self.convert= converter

        self.INSTANCES[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    # predefined
    default                 = NotImplemented
    add_user                = NotImplemented
    remove_user             = NotImplemented
    call                    = NotImplemented
    channel_name_change     = NotImplemented
    channel_icon_change     = NotImplemented
    new_pin                 = NotImplemented
    new_member              = NotImplemented
    new_guild_sub           = NotImplemented
    new_guild_sub_t1        = NotImplemented
    new_guild_sub_t2        = NotImplemented
    new_guild_sub_t3        = NotImplemented
    new_follower_channel    = NotImplemented
    stream                  = NotImplemented

def convert_default(self):
    escape=re.escape
    transformations = {
        '@everyone':'@\u200beveryone',
        '@here':'@\u200bhere'
            }
    
    guild=self.channel.guild
    if guild is None:
        if self.user_mentions is not None:
            for user in self.user_mentions:
                transformations[escape(f'<@{user.id}>')]=f'@{user.name}'
    else:
        if self.channel_mentions is not None:
            for channel in self.channel_mentions:
                transformations[escape(f'<#{channel.id}>')]=f'#{channel.name}'
        
        if self.user_mentions is not None:
            for user in self.user_mentions:
                profile=user.guild_profiles.get(guild,None)
                if (profile is None) or (profile.nick is None):
                    name=f'@{user.name}'
                else:
                    name=f'@{profile.nick}'
                    
                transformations[escape(f'<@!{user.id}>')]=name
                transformations[escape(f'<@{user.id}>')]=name
        
        if self.role_mentions is not None:
            for role in self.role_mentions:
                transformations[escape(f'<@&{role.id}>')]=f'@{role.name}'

    return re.compile("|".join(transformations)).sub(lambda mention:transformations[escape(mention.group(0))],self.content)

def convert_add_user(self):
    return f'{self.author.name} added {self.user_mentions[0].name} to the group.'

def convert_remove_user(self):
    return f'{self.author.name} removed {self.user_mentions[0].name} from the group.'

def convert_call(self):
    if any_to_any(self.channel.clients,self.call.users):
        return f'{self.author.name} started a call.'
    if self.call.ended_timestamp is None:
        return f'{self.author.name} started a call \N{EM DASH} Join the call.'
    return f'You missed a call from {self.author.name}'

def convert_channel_name_change(self):
    return f'{self.author.name} changed the channel name: {self.content}'

def convert_channel_icon_change(self):
    return f'{self.author.name} changed the channel icon.'

def convert_new_pin(self):
    return f'{self.author.name} pinned a message to this channel.'

#TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_new_member(self):
    #tuples with immutable elements are stored directly
    join_messages=(
        '{0} just joined the server - glhf!',
        '{0} just joined. Everyone, look busy!',
        '{0} just joined. Can I get a heal?',
        '{0} joined your party.',
        '{0} joined. You must construct additional pylons.',
        'Ermagherd. {0} is here.',
        'Welcome, {0}. Stay awhile and listen.',
        'Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)',
        'Welcome, {0}. We hope you brought pizza.',
        'Welcome {0}. Leave your weapons by the door.',
        'A wild {0} appeared.',
        'Swoooosh. {0} just landed.',
        'Brace yourselves. {0} just joined the server.',
        '{0} just joined... or did they?',
        '{0} just arrived. Seems OP - please nerf.',
        '{0} just slid into the server.',
        'A {0} has spawned in the server.',
        'Big {0} showed up!',
        'Where’s {0}? In the server!',
        '{0} hopped into the server. Kangaroo!!',
        '{0} just showed up. Hold my beer.',
        'Challenger approaching - {0} has appeared!',
        'It\'s a bird! It\'s a plane! Nevermind, it\'s just {0}.',
        'It\'s {0}! Praise the sun! [T]/',
        'Never gonna give {0} up. Never gonna let {0} down.',
        '{0} has joined the battle bus.',
        'Cheers, love! {0}\'s here!',
        'Hey! Listen! {0} has joined!',
        'We\'ve been expecting you {0}',
        'It\'s dangerous to go alone, take {0}!',
        '{0} has joined the server! It\'s super effective!',
        'Cheers, love! {0} is here!',
        '{0} is here, as the prophecy foretold.',
        '{0} has arrived. Party\'s over.',
        'Ready player {0}',
        '{0} is here to kick butt and chew bubblegum. And {0} is all out of gum.',
        'Hello. Is it {0} you\'re looking for?',
        '{0} has joined. Stay a while and listen!',
        'Roses are red, violets are blue, {0} joined this server with you',
            )

    return join_messages[int(self.created_at.timestamp())%len(join_messages)].format(self.author.name)

def convert_new_guild_sub(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
    return f'{self.author.name} boosted {guild_name} with Nitro!'

def convert_new_guild_sub_t1(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 1!'

def convert_new_guild_sub_t2(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
    
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 2!'

def convert_new_guild_sub_t3(self):
    guild=self.channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 3!'

def convert_new_follower_channel(self):
    channel=self.channel
    guild=channel.guild
    if guild is None:
        guild_name='None'
    else:
        guild_name=guild.name
    
    return f'{self.author.name} has added {guild_name} #{channel.name} to this channel. Its most important updates will show up here.'

#TODO
def convert_stream(self):
    return ''

MessageType.default               = MessageType(0   , 'default'             , convert_default               , )
MessageType.add_user              = MessageType(1   , 'add_user'            , convert_add_user              , )
MessageType.remove_user           = MessageType(2   , 'remove_user'         , convert_remove_user           , )
MessageType.call                  = MessageType(3   , 'call'                , convert_call                  , )
MessageType.channel_name_change   = MessageType(4   , 'channel_name_change' , convert_channel_name_change   , )
MessageType.channel_icon_change   = MessageType(5   , 'channel_icon_change' , convert_channel_icon_change   , )
MessageType.new_pin               = MessageType(6   , 'new_pin'             , convert_new_pin               , )
MessageType.new_member            = MessageType(7   , 'new_member'          , convert_new_member            , )
MessageType.new_guild_sub         = MessageType(8   , 'new_guild_sub'       , convert_new_guild_sub         , )
MessageType.new_guild_sub_t1      = MessageType(9   , 'new_guild_sub_t1'    , convert_new_guild_sub_t1      , )
MessageType.new_guild_sub_t2      = MessageType(10  , 'new_guild_sub_t2'    , convert_new_guild_sub_t2      , )
MessageType.new_guild_sub_t3      = MessageType(11  , 'new_guild_sub_t3'    , convert_new_guild_sub_t3      , )
MessageType.new_follower_channel  = MessageType(12  , 'new_follower_channel', convert_new_follower_channel  , )
MessageType.new_follower_channel  = MessageType(13  , 'stream'              , convert_stream                , )

del convert_default
del convert_add_user
del convert_remove_user
del convert_call
del convert_channel_name_change
del convert_channel_icon_change
del convert_new_pin
del convert_new_member
del convert_new_guild_sub
del convert_new_guild_sub_t1
del convert_new_guild_sub_t2
del convert_new_guild_sub_t3
del convert_new_follower_channel
del convert_stream

#TODO:test
class MessageCall(object):
    __slots__=('ended_timestamp', 'message', 'users',)
    def __init__(self,message,call_data):

        users=[]
        try:
            user_ids=call_data['participants']
        except KeyError:
            pass
        else:
            author_id=message.author.id
            for user_id in user_ids:
                user_id=int(user_id)
                if user_id==author_id:
                    users.append(message.author)
                    continue
                try:
                    users.append(USERS[user_id])
                except KeyError:
                    pass
            
        self.message=message
        self.users=users
        ended_timestamp=call_data.get('ended_timestamp',None)
        self.ended_timestamp=None if ended_timestamp is None else parse_time(ended_timestamp)
        
    @property
    def call_ended(self):
        return self.ended_timestamp is not None

    @property
    def channel(self):
        return self.message.channel

    @property
    def duration(self):
        if self.ended_timestamp is None:
            return datetime.utcnow()-self.message.created_at
        else:
            return self.ended_timestamp-self.message.created_at

#TODO:test
class GroupCall(object):
    __slots__=('available', 'call', 'channel', 'region', 'ringing', 'voice_states',)

    def __new__(cls,data,call,channel):
        if channel.call is None:
            self=object.__new__(cls)
            channel.call=self
            self.voice_states={}
            self.channel=channel
        else:
            self=channel.call

        self.call=call
        self.available=not data['unavailable']
        self.region=VoiceRegion.get(data['region'])
        
        unmentioned_ids=set(self.voice_states)
        for voice_state_data in data['voice_states']:
            user_id=int(voice_state_data['user_id'])
            unmentioned_ids.remove(user_id)
            self._update_voice_state(voice_state_data,PartialUser(user_id))

        for user_id in unmentioned_ids:
            del self.voice_states[user_id]
        
        self.ringing=[]
        try:
            ringing_data=data['ringing']
        except KeyError:
            pass
        else:
            for user_id in ringing_data:
                self.ringing.append(where(channel.users,lambda user,id_=int(user_id):user.id==id_))

    def _update_voice_state(self,data,user):
        while True:
            channel_id=data.get('channel_id',None)
            if channel_id is None:
                try:
                    state=self.voice_states.pop(user.id)
                except KeyError:
                    return
                old=None
                action='l'
                break
            
            channel=self.channel
            
            try:
                state=self.voice_states[user.id]
            except KeyError:
                state=self.voice_states[user.id]=VoiceState(data,channel)
                old=None
                action='j'
                break

            old=state._update(data,channel)
            if old:
                action='u'
                break
            return
        
        return state,action,old

    def _update_voice_state_restricted(self,data,user):
        channel_id=data.get('channel_id',None)
        if channel_id is None:
            try:
                del self.voice_states[user.id]
            except KeyError:
                return
            return _spaceholder

        channel=self.channel

        try:
            state=self.voice_states[user.id]
        except KeyError:
            self.voice_states[user.id]=VoiceState(data,channel)
            return channel

        state._update_no_return(data,channel)
        return channel

del autoposlist
