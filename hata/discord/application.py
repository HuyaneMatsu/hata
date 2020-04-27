# -*- coding: utf-8 -*-
__all__ = ('Application', 'Team', 'TeamMember', 'TeamMembershipState', )

from .bases import DiscordEntity
from .http import URLS
from .user import ZEROUSER, User
from .guild import PartialGuild
from .client_core import TEAMS

class Application(DiscordEntity):
    __slots__ = ('bot_public', 'bot_require_code_grant', 'cover', 'description', 'guild', 'icon', 'name', 'owner',
        'primary_sku_id', 'rpc_origins', 'slug', 'summary', 'verify_key',)
    
    def __init__(self,data=None):
        if data is None:
            self._fillup()
        else:
            self(data)
    
    def __hash__(self):
        id_ = self.id
        if id_:
            return id_
        
        raise TypeError(f'Cannot hash partial {self.__class__.__name__} object.')
    
    @property
    def partial(self):
        return (self.id == 0)
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        id_ = self.id
        if id_:
            result.append(' id=')
            result.append(repr(id_))
            result.append(', name=')
            result.append(repr(self.name))
        else:
            result.append(' partial')
        
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        return self.name
    
    def _fillup(self):
        self.id=0
        self.name=''
        self.icon=0
        self.description=''
        self.rpc_origins=[]
        self.bot_public=False
        self.bot_require_code_grant=False
        self.owner=ZEROUSER
        self.summary=''
        self.verify_key=''
        self.guild=None
        self.primary_sku_id=0
        self.slug=''
        self.cover=0
    
    def __call__(self,data):
        self.id=int(data['id'])
        self.name=data['name']
        
        icon=data.get('icon')
        self.icon=0 if icon is None else int(icon,16)
        
        self.description=data['description']
        
        try:
            self.rpc_origins=data['rpc_origins']
        except KeyError:
            self.rpc_origins=[]
            
        self.bot_public=data['bot_public']
        self.bot_require_code_grant=data['bot_require_code_grant']
        self.summary=data['summary']
        self.verify_key=data['verify_key']

        #TODO: do we get owner data if we request other application ?
        team_data=data['team']
        self.owner=User(data['owner']) if team_data is None else Team(team_data)

        guild_id=data.get('guild_id',None)
        self.guild=None if guild_id is None else PartialGuild({'id':guild_id})
        
        primary_sku_id=data.get('primary_sku_id')
        self.primary_sku_id=0 if primary_sku_id is None else int(primary_sku_id)

        self.slug=data.get('slug','')

        cover=data.get('cover_image')
        self.cover=0 if cover is None else int(cover,16)
        
    icon_url=property(URLS.application_icon_url)
    icon_url_as=URLS.application_icon_url_as
    cover_url=property(URLS.application_cover_url)
    cover_url_as=URLS.application_cover_url_as

class Team(DiscordEntity, immortal=True):
    __slots__=('icon', 'members', 'name', 'owner',)
    def __new__(cls,data):
        team_id=int(data['id'])
        try:
            team=TEAMS[team_id]
        except KeyError:
            team=object.__new__(cls)
            team.id=team_id
        
        #update every attribute
        team.name=data['name']
        
        icon=data.get('icon')
        team.icon=0 if icon is None else int(icon,16)
        
        owner_id=int(data['owner_user_id'])
        members=[]
        
        for team_member_data in data['members']:
            team_member=TeamMember(team_member_data)
            members.append(team_member)
            if team_member.user.id==owner_id:
                team.owner=team_member.user

        #sync it later to keep the references meanwhile
        team.members=members
        
        return team
    
    icon_url=property(URLS.team_icon_url)
    icon_url_as=URLS.team_icon_url_as
    
    @property
    def invited(self):
        target_state=TeamMembershipState.INVITED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    @property
    def accepted(self):
        target_state=TeamMembershipState.ACCEPTED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<{self.__class__.__name__} owner={self.owner:f} total members : {len(self.members)}>'
    
class TeamMember(object):
    __slots__=('permissions', 'state', 'user',)
    def __init__(self,data):
        permissions=data['permissions']
        permissions.sort()
        self.permissions=permissions
        self.user=User(data['user'])
        self.state=TeamMembershipState.INSTANCES[data['membership_state']]

    def __repr__(self):
        return f'<{self.__class__.__name__} user={self.user.full_name} state={self.state.name} permissions={self.permissions}>'
    
    def __hash__(self):
        return self.user.id
    
    def __eq__(self,other):
        if type(self) is not type(other):
            return False
        
        if (self.user != other.user):
            return False
        
        if (self.state is not other.state):
            return False
        
        if (self.permissions != other.permissions):
            return False
        
        return True

class TeamMembershipState(object):
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__=('name', 'value',)
    
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
    NONE    = None
    INVITED = None
    ACCEPTED= None

TeamMembershipState.NONE        = TeamMembershipState(1,'NONE')
TeamMembershipState.INVITED     = TeamMembershipState(1,'INVITED')
TeamMembershipState.ACCEPTED    = TeamMembershipState(2,'ACCEPTED')

del URLS
