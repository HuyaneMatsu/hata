# -*- coding: utf-8 -*-
__all__ = ('Invite', )

from .others import parse_time, InviteTargetType
from .http import URLS
from .user import User,ZEROUSER
from .guild import PartialGuild
from .channel import PartialChannel

class Invite(object):
    __slots__=('channel', 'code', 'created_at', 'guild', 'inviter', 'max_age',
        'max_uses', 'online_count','target_type', 'target_user', 'temporary',
        'total_count', 'uses',)

    def __init__(self,data):
        self.code           = data['code']
        guild               = PartialGuild(data.get('guild',None))
        self.guild          = guild
        self.channel        = PartialChannel(data['channel'],guild)
        self.online_count   = data.get('approximate_presence_count',0)
        self.total_count    = data.get('approximate_member_count',0)
        
        try:
            inviter_data=data['inviter']
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
