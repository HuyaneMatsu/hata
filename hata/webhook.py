# -*- coding: utf-8 -*-
__all__ = ('Webhook', 'WebhookRepr', 'WebhookType')

from .http import URLS
from .others import _parse_ih_fsa
from .user import User, ZEROUSER, USERS, UserBase
from .exceptions import DiscordException

ChannelText=NotImplemented

class WebhookType(object):
    __slots__=('name', 'value')
    INSTANCES=[NotImplemented] * 3
    
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

def PartialWebhook(webhook_id,token,type_=WebhookType.bot):
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
        webhook.channel = None
        
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
        return (self.channel is None)

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
    def precreate(cls,webhook_id,**kwargs):
        try:
            webhook=USERS[webhook_id]
        except KeyError:
            webhook=object.__new__(cls)
            
            if kwargs:
                webhook.token   = kwargs.pop('token','')
                webhook.name    = kwargs.pop('name','')
                webhook.discriminator=0
                webhook.avatar,webhook.has_animated_avatar=_parse_ih_fsa(
                    kwargs.pop('avatar',None),
                    kwargs.pop('has_animated_avatar',False))
                webhook.user    = kwargs.pop('user',ZEROUSER)
                webhook.channel = kwargs.pop('channel',None)
                type_           = kwargs.pop('type_',1)
                if type(type_) is int:
                    try:
                        type_=WebhookType.INSTANCES[type_]
                    except IndexError as err:
                        raise ValueError(f'Invalid WebhookType : {type_}') from err
                elif type(type_) is WebhookType:
                    pass
                else:
                    raise TypeError('Expected \'int\' or \'WebhookTyp\' for \'type_\', received {type_}')
                webhook.type    = type_
                
                if kwargs:
                    for name,value in kwargs.items():
                        if name=='id':
                            raise AttributeError(f'Cannot set {name!r} attribute with precreate!')
                        setattr(kwargs,name,value)
                    
            else:
                webhook.token   = ''
                webhook.name    = ''
                webhook.discriminator=0
                webhook.avatar  = 0
                webhook.has_animated_avatar=False
                webhook.user    = ZEROUSER
                webhook.channel = None
                webhook.type    =WebhookType.bot
                
            webhook.id      = webhook_id
            
            USERS[webhook_id]=webhook
        
        else:
            if kwargs:
                try:
                    webhook.avatar,webhook.has_animated_avatar=_parse_ih_fsa(
                        kwargs.pop('avatar',None),
                        kwargs.pop('has_animated_avatar',False))
                except KeyError:
                    pass

                if kwargs:
                    for name,value in kwargs.items():
                        if name=='id':
                            raise AttributeError(f'Cannot set {name!r} attribute with precreate!')
                        setattr(kwargs,name,value)
        
        return webhook

    @property
    def guild(self):
        channel=self.channel
        if self.channel is None:
            return
        return channel.guild

    def _delete(self):
        if self.channel is None:
            return
        del self.channel.guild.webhooks[self.id]
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
        if guild is not None:
            guild.webhooks[webhook_id]=webhook
        
        USERS[webhook_id]=webhook

        return webhook

class WebhookRepr(UserBase):
    __slots__=('type')

    def __init__(self,data,webhook_id,type_):
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
        
    @property
    def webhook(self):
        return PartialWebhook(self.id,'',self.type)

    @property
    def partial(self):
        return False

    @property
    def is_bot(self):
        return True
    
del URLS
del UserBase
