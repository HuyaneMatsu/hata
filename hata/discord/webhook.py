# -*- coding: utf-8 -*-
__all__ = ('Webhook', 'WebhookRepr', 'WebhookType')

from .http import URLS
from .user import User, ZEROUSER, USERS, UserBase
from .exceptions import DiscordException
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_preinstanced_type, \
    preconvert_animated_image_hash

from . import ratelimit

ChannelText = NotImplemented
Client = NotImplemented

class WebhookType(object):
    __slots__=('name', 'value')
    INSTANCES = [NotImplemented] * 3
    
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
    
    # prefened
    none        = NotImplemented
    bot         = NotImplemented
    server      = NotImplemented

WebhookType.none    = WebhookType(0,'NONE')
WebhookType.bot     = WebhookType(1,'BOT')
WebhookType.server  = WebhookType(2,'SERVER')

def PartialWebhook(webhook_id, token, type_=WebhookType.bot, channel=None):
    try:
        webhook=USERS[webhook_id]
    except KeyError:
        webhook=object.__new__(Webhook)
        
        webhook.id      = webhook_id
        
        webhook.name    = ''
        webhook.discriminator=0
        webhook.avatar  = 0
        webhook.has_animated_avatar=False

        webhook.user    = ZEROUSER
        webhook.channel = channel
        
        webhook.type=type_
        
        USERS[webhook_id]=webhook
    
    webhook.token   = token
    return webhook


class Webhook(UserBase):
    __slots__=('channel', 'token', 'type', 'user', ) #default webhook

    @property
    def is_bot(self):
        return True

    @property
    def partial(self):
        channel = self.channel
        if channel is None:
            return True
        
        if channel.guild is None:
            return True
        
        return False

    avatar_url=property(URLS.webhook_avatar_url)
    avatar_url_as=URLS.webhook_avatar_url_as

    def __new__(cls,data):
        webhook_id=int(data['id'])
        try:
            webhook=USERS[webhook_id]
        except KeyError:
            webhook=object.__new__(cls)
            USERS[webhook_id]=webhook
            webhook.id=webhook_id
        
        webhook._update_no_return(data)
        webhook.type=WebhookType.INSTANCES[data['type']]
        return webhook

    @classmethod
    def from_url(cls,url):
        result=cls.urlpattern.fullmatch(url)
        if result is None:
            return None
        
        webhook_id = int(result.group(1))
        webhook_token = result.group(0)
        
        return PartialWebhook(webhook_id,webhook_token)

    def _update_no_return(self,data):
        self.channel=channel=ChannelText.precreate(int(data['channel_id']))
        if channel.clients:
            channel.guild.webhooks[self.id]=self

        token=data.get('token')
        if token is not None:
            self.token=token

        name=data['name']
        if name is None:
            self.name=''
        else:
            self.name=name

        self.discriminator=0

        avatar=data.get('avatar')
        if avatar is None:
            self.avatar=0
            self.has_animated_avatar=False
        elif avatar.startswith('a_'):
            self.avatar=int(avatar[2:],16)
            self.has_animated_avatar=True
        else:
            self.avatar=int(avatar,16)
            self.has_animated_avatar=False
            
        try:
            user=data['user']
        except KeyError:
            self.user=ZEROUSER
        else:
            self.user=User(user)

    @classmethod
    def precreate(cls, webhook_id, **kwargs):
        webhook_id = preconvert_snowflake(webhook_id, 'webhook_id')
        
        if kwargs:
            processable = []
            
            for key, details in (
                    ('name' , (0 , 80,)),
                    ('token', (60, 68,)),
                        ):
                
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_str(value, key, *details)
                    processable.append((key, value))
            
            try:
                avatar = kwargs.pop('avatar')
            except KeyError:
                if 'has_animated_avatar' in kwargs:
                    raise TypeError('`has_animated_avatar` was passed without passing `avatar`.')
            else:
                has_animated_avatar = kwargs.pop('has_animated_avatar', False)
                avatar, has_animated_avatar = preconvert_animated_image_hash(avatar, has_animated_avatar, 'avatar', 'has_animated_avatar')
                processable.append(('avatar', avatar))
                processable.append(('has_animated_avatar',has_animated_avatar))
            
            for key, type_ in (
                    ('user', (User, Client,)),
                    ('channel', ChannelText),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if not isinstance(value,type_):
                        raise TypeError(f'`{key}` can be instance of: {type_!r}, got: {value.__class__.__name__}.')
                    processable.append((key, value))
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_preinstanced_type(type_, 'type', WebhookType)
                processable.append(('type',type_))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        try:
            webhook=USERS[webhook_id]
        except KeyError:
            webhook=object.__new__(cls)
            
            webhook.id      = webhook_id
            webhook.token   = ''
            webhook.name    = ''
            webhook.discriminator=0
            webhook.avatar  = 0
            webhook.has_animated_avatar=False
            webhook.user    = ZEROUSER
            webhook.channel = None
            webhook.type    = WebhookType.bot
            
            USERS[webhook_id]=webhook
        else:
            if not webhook.partial:
                return webhook
        
        if (processable is not None):
            for item in processable:
                setattr(webhook, *item)
        
        return webhook

    @property
    def guild(self):
        channel=self.channel
        if channel is None:
            return
        return channel.guild

    def _delete(self):
        channel=self.channel
        if channel is None:
            return
        guild=channel.guild
        if (guild is not None):
            try:
                del guild.webhooks[self.id]
            except KeyError:
                pass
        self.channel=None
        self.user=ZEROUSER 
    
    url=property(URLS.webhook_url)
    urlpattern=URLS.webhook_urlpattern
    
    @classmethod
    async def _from_follow_data(cls,data,source_channel,target_channel,client):
        webhook_id=int(data['webhook_id'])
        
        guild=source_channel.guild
        if guild is None:
            try:
                extra_data = await client.http.webhook_get(webhook_id)
            except DiscordException:
                #not lucky
                name=''
                avatar=0
                has_animated_avatar=False
            else:
                name=data['name']
                if name is None:
                    name=''
        
                avatar=data.get('avatar')
                if avatar is None:
                    avatar=0
                    has_animated_avatar=False
                elif avatar.startswith('a_'):
                    avatar=int(avatar[2:],16)
                    has_animated_avatar=True
                else:
                    avatar=int(avatar,16)
                    has_animated_avatar=False
        else:
            avatar      = guild.icon
            name        = f'{guild.name} #{source_channel.name}'
            has_animated_avatar=False
            
        webhook=object.__new__(cls)
        webhook.id          = webhook_id
        webhook.name        = name
        webhook.discriminator=0
        webhook.avatar      = avatar
        webhook.has_animated_avatar=has_animated_avatar #will be always False
        webhook.channel     = target_channel
        webhook.token       = ''
        webhook.user        = client
        webhook.type        = WebhookType.server
        
        guild=target_channel.guild
        if (guild is not None):
            guild.webhooks[webhook_id]=webhook
        
        USERS[webhook_id]=webhook

        return webhook

class WebhookRepr(UserBase):
    __slots__=('type', 'channel')
    
    def __init__(self,data,webhook_id,type_,channel):
        self.id=webhook_id
        self.discriminator=0
        self.name=data['username']
        
        avatar=data.get('avatar')
        if avatar is None:
            self.avatar=0
            self.has_animated_avatar=False
        elif avatar.startswith('a_'):
            self.avatar=int(avatar[2:],16)
            self.has_animated_avatar=True
        else:
            self.avatar=int(avatar,16)
            self.has_animated_avatar=False
        
        self.type=type_
        self.channel = channel
    
    @property
    def webhook(self):
        return PartialWebhook(self.id, '', self.type, self.channel)
    
    @property
    def partial(self):
        return False
    
    @property
    def is_bot(self):
        return True
    
    @property
    def guild(self):
        return self.channel.guild

ratelimit.Webhook = Webhook
ratelimit.WebhookRepr = WebhookRepr

del URLS
del UserBase
del ratelimit
