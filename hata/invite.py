# -*- coding: utf-8 -*-
__all__ = ('Invite', 'InviteTargetType')

from .others import parse_time
from .http import URLS
from .client_core import GUILDS, CHANNELS
from .user import User, ZEROUSER
from .guild import PartialGuild
from .channel import PartialChannel

class InviteTargetType(object):
    # class related
    INSTANCES = [NotImplemented] * 2
    
    # object related
    __slots__=('name', 'value')
    
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
    
    # predefined
    NONE    = NotImplemented
    STREAM  = NotImplemented

InviteTargetType.NONE   = InviteTargetType(0,'NONE')
InviteTargetType.STREAM = InviteTargetType(1,'STREAM')

class Invite(object):
    __slots__=('channel', 'code', 'created_at', 'guild', 'inviter', 'max_age',
        'max_uses', 'online_count','target_type', 'target_user', 'temporary',
        'total_count', 'uses',)

    def __init__(self,data):
        self.code = data['code']
        
        try:
            guild_data = data['guild']
        except KeyError:
            try:
                guild_id = data['guild_id']
            except KeyError:
                guild = None
            else:
                guild_id = int(guild_id)
                guild = GUILDS.get(guild_id,None)
        else:
            guild = PartialGuild(guild_data)
        
        self.guild = guild
        
        try:
            channel_data = data['channel']
        except KeyError:
            try:
                channel_id = data['channel_id']
            except KeyError:
                channel = None
            else:
                channel_id = int(channel_id)
                channel = CHANNELS.get(channel_id,None)
        else:
            channel = PartialChannel(channel_data,guild)
        
        self.channel        = channel
        self.online_count   = data.get('approximate_presence_count',0)
        self.total_count    = data.get('approximate_member_count',0)
        
        try:
            inviter_data = data['inviter']
        except KeyError:
            self.inviter    = ZEROUSER
        else:
            self.inviter    = User(inviter_data)
        
        self.uses           = data.get('uses',None)
        self.max_age        = data.get('max_age',None)
        self.max_uses       = data.get('max_uses',None)
        self.temporary      = data.get('temporary',True)
        try:
            created_at_data = data['created_at']
        except KeyError:
            self.created_at = None
        else:
            self.created_at = parse_time(created_at_data)
        
        self.target_type    = InviteTargetType.INSTANCES[data.get('target_user_type',0)]
        
        try:
            target_user_data=data['target_user']
        except KeyError:
            self.target_user=ZEROUSER
        else:
            self.target_user=User(target_user_data)
            
    @classmethod
    def _create_vanity(cls,guild,data):
        invite=object.__new__(cls)
        invite.code         = guild.vanity_code
        invite.inviter      = ZEROUSER
        invite.uses         = None
        invite.max_age      = None
        invite.max_uses     = None
        invite.temporary    = False
        invite.created_at   = None
        invite.guild        = guild
        invite.channel      = guild.all_channel[int(data['channel']['id'])]
        invite.online_count = 0
        invite.total_count  = 0
        invite.target_type  = InviteTargetType.NONE
        invite.target_user  = ZEROUSER
            
        return invite

    @property
    def partial(self):
        return bool(self.inviter.id)
    
    def __str__(self):
        return self.url

    def __repr__(self):
        return f'<{self.__class__.__name__} code={self.code!r}>'

    def __hash__(self):
        return hash(self.code)

    url=property(URLS.invite_url)

    #When we update it we get only a partial invite from Discord. So sad.
    def _update_no_return(self,data):
        #code cant change, i am pretty sure
        try:
            self.online_count=data['approximate_presence_count']
            self.total_count=data['approximate_member_count']
        except KeyError:
            pass
    
    def _update(self,data):
        old={}
        try:
            online_count=data['approximate_presence_count']
            if self.online_count!=online_count:
                old['online_count']=self.online_count
                self.online_count=online_count

            total_count=data['approximate_member_count']
            if self.total_count!=total_count:
                old['total_count']=self.total_count
                self.total_count=total_count
        except KeyError:
            pass
        
        return old

del URLS
