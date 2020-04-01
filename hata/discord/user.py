# -*- coding: utf-8 -*-
__all__ = ('GuildProfile', 'User', 'UserBase', 'UserFlag', 'VoiceState', 'ZEROUSER')

from datetime import datetime

from ..backend.dereaddons_local import modulize

from .client_core import CACHE_USER,CACHE_PRESENCE, USERS
from .others import parse_time, Status, DISCORD_EPOCH, id_to_time, _parse_ih_fsa
from .color import Color, DefaultAvatar
from .activity import ActivityUnknown, Activity
from .http import URLS

class UserFlag(int):
    __slots__=()
    
    @property
    def discord_employee(self):
        return self&1
    
    @property
    def discord_partner(self):
        return (self>>1)&1
    
    @property
    def hypesquad_events(self):
        return (self>>2)&1
    
    @property
    def bug_hunter_level_1(self):
        return (self>>3)&1
    
    @property
    def hypesquad_bravery(self):
        return (self>>6)&1
    
    @property
    def hypesquad_brilliance(self):
        return (self>>7)&1
    
    @property
    def hypesquad_balance(self):
        return (self>>8)&1
    
    @property
    def early_supporter(self):
        return (self>>9)&1
    
    @property
    def team_user(self):
        return (self>>10)&1
    
    @property
    def system(self):
        return (self>>12)&1
    
    @property
    def bug_hunter_level_2(self):
        return (self>>14)&1
    
    def __iter__(self):
        if self&1:
            yield 'discord_employee'
            
        if (self>>1)&1:
            yield 'discord_partner'
            
        if (self>>2)&1:
            yield 'bug_hunter_level_1'
            
        if (self>>3)&1:
            yield 'hypesquad_bravery'
            
        if (self>>6)&1:
            yield 'hypesquad_bravery'
            
        if (self>>7)&1:
            yield 'hypesquad_brilliance'
            
        if (self>>8)&1:
            yield 'hypesquad_balance'
            
        if (self>>9)&1:
            yield 'early_supporter'
            
        if (self>>10)&1:
            yield 'team_user'

        if (self>>12)&1:
            yield 'system'
        
        if (self>>14)&1:
            yield 'bug_hunter_level_2'
            
    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

if CACHE_PRESENCE:
    def PartialUser(user_id):
        try:
            return USERS[user_id]
        except KeyError:
            pass
        
        user=object.__new__(User)
        user.id=user_id
        
        user.name=''
        user.discriminator=0
        user.avatar=0
        user.has_animated_avatar=False
        user.is_bot=False

        user.guild_profiles={}
        user.partial=True

        user.status=Status.offline
        user.statuses={}
        user.activities=[]

        USERS[user_id]=user
        
        return user

elif CACHE_USER:
    def PartialUser(user_id):
        try:
            return USERS[user_id]
        except KeyError:
            pass
        
        user=object.__new__(User)
        user.id=user_id

        user.name=''
        user.discriminator=0
        user.avatar=0
        user.has_animated_avatar=False
        user.is_bot=False

        user.guild_profiles={}
        user.partial=True

        USERS[user_id]=user
        
        return user

else:
    def PartialUser(user_id):
        user=object.__new__(User)
        user.id=user_id

        user.name=''
        user.discriminator=0
        user.avatar=0
        user.has_animated_avatar=False
        user.is_bot=False

        user.guild_profiles={}
        user.partial=True
        
        return user

class GuildProfile(object):
    __slots__=('boosts_since', 'joined_at', 'nick', 'roles',)

    @property
    def created_at(self):
        joined_at=self.joined_at
        if joined_at is None:
            return datetime.utcfromtimestamp(DISCORD_EPOCH)
        return joined_at
    
    def __init__(self,data,guild):
        self.roles=[]
        try:
            joined_at_data=data['joined_at']
        except KeyError:
            self.joined_at=None
        else:
            self.joined_at=parse_time(joined_at_data)
        self._update_no_return(data,guild)
    
    def _set_joined(self,data):
        if self.joined_at is None:
            try:
                joined_at_data=data['joined_at']
            except KeyError:
                self.joined_at=None
            else:
                self.joined_at=parse_time(joined_at_data)
    
    def _update_no_return(self,data,guild):
        self.nick=data.get('nick',None)
        
        roles=self.roles
        roles.clear()
        
        guild_roles=guild.all_role
        for role_id in data['roles']:
            role_id=int(role_id)
            try:
                role=guild_roles[role_id]
            except KeyError:
                continue
            roles.append(role)
        
        boosts_since=data.get('premium_since',None)
        if (boosts_since is not None):
            boosts_since=parse_time(boosts_since)
        self.boosts_since=boosts_since
    
    def _update(self,data,guild):
        old={}
        nick=data.get('nick',None)
        if self.nick!=nick:
            old['nick']=self.nick
            self.nick=nick
        
        roles=[]
        
        guild_roles=guild.all_role
        for role_id in data['roles']:
            role_id=int(role_id)
            try:
                role=guild_roles[role_id]
            except KeyError:
                continue
            roles.append(role)
            
        roles.sort()
        own_roles = self.roles
        own_roles.sort()
        if own_roles!=roles:
            old['roles']=self.roles
            self.roles=roles
        
        boosts_since=data.get('premium_since',None)
        if boosts_since is not None:
            boosts_since=parse_time(boosts_since)
        
        if (self.boosts_since is None):
            if boosts_since is not None:
                old['boosts_since']=None
                self.boosts_since=boosts_since
        else:
            if (boosts_since is None):
                old['boosts_since']=self.boosts_since
                self.boosts_since=None
            elif (self.boosts_since!=boosts_since):
                old['boosts_since']=self.boosts_since
                self.boosts_since=boosts_since
        
        return old
    
    def get_top_role(self, default=None):
        roles = self.roles
        if not roles:
            return default
        
        roles.sort()
        return roles[-1]
    
    @property
    def color(self):
        roles = self.roles
        if roles:
            roles.sort()
            for role in reversed(roles):
                color = role.color
                if color:
                    return color
        
        return Color(0)
        
class UserBase(object):
    __slots__=('id', 'name', 'discriminator', 'avatar', 'has_animated_avatar', '__weakref__',)

    def __init_subclass__(cls):
        rich = cls.__rich__
        if 'guild_profiles' in cls.__slots__:
            cls.color_at        = rich.color_at
            cls.name_at         = rich.name_at
            cls.mentioned_in    = rich.mentioned_in
            cls.has_role        = rich.has_role
            cls.top_role_at     = rich.top_role_at
            cls.can_use_emoji   = rich.can_use_emoji
            cls.has_higher_role_than    = rich.has_higher_role_than
            cls.has_higher_role_than_at = rich.has_higher_role_than
        
        if 'activities' in cls.__slots__:
            cls.activity      = rich.activity
        
        if 'statuses' in cls.__slots__:
            cls.platform      = rich.platform
        
        # webhook type
        if hasattr(cls,'guild'):
            cls.can_use_emoji = rich.can_use_emoji__w_guild
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        if self.partial:
            return f'<{self.__class__.__name__} partial id={self.id}>'
        return f'<{self.__class__.__name__} name={self.name}#{self.discriminator:0>4}, id={self.id}>'
    
    def __format__(self,code):
        if not code:
            return self.name
        if code=='f':
            return self.full_name
        if code=='m':
            return self.mention
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def full_name(self):
        return f'{self.name}#{self.discriminator:0>4}'
    
    @property
    def mention(self):
        return f'<@{self.id}>'
    
    @property
    def mention_nick(self):
        return f'<@!{self.id}>'
    
    @property
    def created_at(self):
        return id_to_time(self.id)
    
    def __hash__(self):
        return self.id
    
    avatar_url=property(URLS.user_avatar_url)
    avatar_url_as=URLS.user_avatar_url_as
    
    @property
    def default_avatar_url(self):
        return DefaultAvatar.INSTANCES[self.discriminator%DefaultAvatar.COUNT].url
    
    @property
    def default_avatar(self):
        return DefaultAvatar.INSTANCES[self.discriminator%DefaultAvatar.COUNT]
    
    #for sorting users
    def __gt__(self,other):
        if isinstance(other,UserBase):
            return self.id>other.id
        return NotImplemented

    def __ge__(self,other):
        if isinstance(other,UserBase):
            return self.id>=other.id
        return NotImplemented

    def __eq__(self,other):
        if isinstance(other,UserBase):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if isinstance(other,UserBase):
            return self.id!=other.id
        return NotImplemented

    def __le__(self,other):
        if isinstance(other,UserBase):
            return self.id<=other.id
        return NotImplemented

    def __lt__(self,other):
        if isinstance(other,UserBase):
            return self.id<other.id
        return NotImplemented

    @property
    def activities(self):
        return []

    @property
    def status(self):
        return Status.offline

    @property
    def statuses(self):
        return {}

    @property
    def guild_profiles(self):
        return {}

    @property
    def is_bot(self):
        return False

    @property
    def partial(self):
        return True

    @property
    def activity(self):
        return  ActivityUnknown

    @property
    def platform(self):
        return ''

    def color_at(self,guild):
        return Color(0)

    def name_at(self,guild):
        return self.name
    
    def mentioned_in(self,message):
        if message.everyone_mention:
            return True
        if message.user_mentions is not None and self in message.user_mentions:
            return True
        return False
    
    def has_role(self,role):
        return False
    
    def top_role_at(self, guild, default=None):
        return default
    
    def can_use_emoji(self, emoji):
        if emoji.is_unicode_emoji():
            return True
        
        return False
    
    def has_higher_role_than(self, role):
        return False
    
    def has_higher_role_than_at(self, role, guild):
        return False
    
    @modulize
    class __rich__:
        def color_at(self, guild):
            if (guild is not None):
                try:
                    profile=self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    return profile.color
            
            return Color(0)
        
        def name_at(self,guild):
            if (guild is not None):
                try:
                    profile=self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    nick=profile.nick
                    if nick is not None:
                        return nick
            
            return self.name

        def mentioned_in(self,message):
            if message.everyone_mention:
                return True
            
            user_mentions=message.user_mentions
            if user_mentions is not None and self in user_mentions:
                return True
            
            role_mentions=message.role_mentions
            if role_mentions is not None:
                # if channel is deleted, it's guild is None
                guild = message.channel.guild
                if guild is not None:
                    try:
                        profile=self.guild_profiles[guild]
                    except KeyError:
                        return False
                    
                    for role in profile.roles:
                        if role in role_mentions:
                            return True
            
            return False

        @property
        def activity(self):
            activities=self.activities
            if activities:
                return activities[0]
            return ActivityUnknown

        @property
        def platform(self):
            statuses=self.statuses
            if statuses:
                status=self.status.value
                for platform,l_status in statuses.items():
                    if l_status==status:
                        return platform
            return ''
        
        def has_role(self,role):
            # if role is deleted, it's guild is None
            guild = role.guild
            if guild is None:
                return False
            
            try:
                profile=self.guild_profiles[guild]
            except KeyError:
                return False
            
            return (role in profile.roles)
        
        def top_role_at(self, guild, default=None):
            if (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    return profile.get_top_role(default)
            
            return default
        
        def can_use_emoji(self, emoji):
            if emoji.is_unicode_emoji():
                return True
            
            guild = emoji.guild
            if guild is None:
                return False
            
            try:
                profile = self.guild_profiles[guild]
            except KeyError:
                return False
            
            roles = emoji.roles
            if (roles is None) or (not roles):
                return True
            
            if guild.owner == self:
                return True
            
            if roles.isdisjoint(profile.roles):
                return False
            
            return True
        
        def can_use_emoji__w_guild(self, emoji):
            if emoji.is_unicode_emoji():
                return True
            
            guild = emoji.guild
            if guild is None:
                return False
            
            webhook_guild = self.guild
            if webhook_guild is None:
                return False
            
            roles = emoji.roles
            if (roles is None) or (not roles):
                return True
            
            return False
        
        def has_higher_role_than(self, role):
            guild = role.guild
            if guild is None:
                return False
            
            try:
                profile = self.guild_profiles[guild]
            except KeyError:
                return False
            
            if guild.owner == self:
                return True
            
            top_role = profile.get_top_role()
            if top_role is None:
                return False
            
            if top_role>role:
                return True
            
            return False
        
        def has_higher_role_than_at(self, user, guild):
            if (guild is None):
                return False
            
            try:
                own_profile = self.guild_profiles[guild]
            except KeyError:
                return False
            
            if guild.owner == self:
                return True
            
            try:
                other_profile = user.guild_profiles[guild]
            except KeyError:
                # Is the other user a Webhook?
                webhook_guild = getattr(user, 'guild', None)
                if (webhook_guild is not guild):
                    # Not webhook or partial webhook, or a webhook of a different guild
                    return False
                
                # If we have any roles, we have more role than a webhook with 0
                if own_profile.roles:
                    return True
                
                return False
            
            if guild.owner == user:
                return False
            
            own_top_role = own_profile.get_top_role()
            if own_top_role is None:
                return False
            
            other_top_role = other_profile.get_top_role()
            if other_top_role is None:
                return True
            
            if own_top_role > other_top_role:
                return True
            
            return False


class User(UserBase):
    if CACHE_PRESENCE:
        __slots__=('guild_profiles', 'is_bot', 'partial', #default User
            'activities', 'status', 'statuses') #Presence
    else:
        __slots__=('guild_profiles', 'is_bot', 'partial') #default User
        
    if CACHE_PRESENCE:
        def __new__(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=data.get('member')
                
            user_id=int(user_data['id'])
            
            try:
                user=USERS[user_id]
                update=user.partial
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                user.guild_profiles={}
                user.status=Status.offline
                user.statuses={}
                user.activities=[]
                update=True
                
                USERS[user_id]=user
            
            if update:
                user.partial=False
                user.is_bot=user_data.get('bot',False)
                user._update_no_return(user_data)
            
            if member_data is not None and guild is not None:
                try:
                    profile=user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id]=user
                    user.guild_profiles[guild]=GuildProfile(member_data,guild)
                else:
                    profile._set_joined(member_data)
            
            return user
            
    elif CACHE_USER:
        def __new__(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=data.get('member')
                
            user_id=int(user_data['id'])

            try:
                user=USERS[user_id]
                update=user.partial
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                user.guild_profiles={}
                update=True
                
                USERS[user_id]=user

            if update:
                user.partial=False
                user.is_bot=user_data.get('bot',False)
                user._update_no_return(user_data)

            if member_data is not None and guild is not None:
                try:
                    profile=user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id]=user
                    user.guild_profiles[guild]=GuildProfile(member_data,guild)
                else:
                    profile._set_joined(member_data)
                    
            return user
    
    else:
        def __new__(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=data.get('member')
            
            user_id=int(user_data['id'])
            
            user=object.__new__(cls)
            user.id=user_id
            user.guild_profiles={}
            user.partial=False
            user.is_bot=user_data.get('bot',False)
            user._update_no_return(user_data)
            
            if member_data is not None and guild is not None:
                user.guild_profiles[guild]=GuildProfile(member_data,guild)
            
            return user
    
    if (not CACHE_PRESENCE):
        @staticmethod
        def _bypass_no_cache(data,guild):
            user_data=data['user']
            member_data=data
            
            user_id=int(user_data['id'])
            
            try:
                user=USERS[user_id]
            except KeyError:
                return
            
            try:
                profile=user.guild_profiles[guild]
            except KeyError:
                guild.users[user_id]=user
                user.guild_profiles[guild]=GuildProfile(member_data,guild)
            else:
                profile._set_joined(member_data)
                profile._update_no_return(member_data,guild)
    
    
    if CACHE_PRESENCE:
        @classmethod
        def precreate(cls,user_id,**kwargs):
            processable={}
            for key in ('name', 'discriminator', 'avatar', 'has_animated_avatar', 'is_bot'):
                try:
                    value=kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    processable[key]=value
                    
            if kwargs:
                raise ValueError(f'Unused or unsettable attributes: {kwargs}')
            
            try:
                user=USERS[user_id]
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                
                user.name=''
                user.discriminator=0
                user.avatar=0
                user.has_animated_avatar=False
                user.is_bot=False
                
                user.guild_profiles={}
                user.partial=True
                
                user.status=Status.offline
                user.statuses={}
                user.activities=[]
        
                USERS[user_id]=user
            else:
                if not user.partial:
                    return user
    
            try:
                user.avatar,user.has_animated_avatar=_parse_ih_fsa(
                    processable.get('avatar'),
                    processable.get('has_animated_avatar',False))
            except KeyError:
                pass
            
            for attr in ('name', 'discriminator', 'is_bot'):
                try:
                    value=processable[attr]
                except KeyError:
                    continue
                setattr(user,attr,value)
            
            return user
    
    elif CACHE_USER:
        @classmethod
        def precreate(cls,user_id,**kwargs):
            processable={}
            for key in ('name', 'discriminator', 'avatar', 'has_animated_avatar', 'is_bot'):
                try:
                    value=kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    processable[key]=value
                    
            if kwargs:
                raise ValueError(f'Unused or unsettable attributes: {kwargs}')
            
            try:
                user=USERS[user_id]
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                
                user.name=''
                user.discriminator=0
                user.avatar=0
                user.has_animated_avatar=False
                user.is_bot=False
                
                user.guild_profiles={}
                user.partial=True
        
                USERS[user_id]=user
            else:
                if not user.partial:
                    return user
    
            try:
                user.avatar,user.has_animated_avatar=_parse_ih_fsa(
                    processable.get('avatar'),
                    processable.get('has_animated_avatar',False))
            except KeyError:
                pass
            
            for attr in ('name', 'discriminator', 'is_bot'):
                try:
                    value=processable[attr]
                except KeyError:
                    continue
                setattr(user,attr,value)
            
            return user
    
    else:
        @classmethod
        def precreate(cls,user_id,**kwargs):
            processable={}
            for key in ('name', 'discriminator', 'avatar', 'has_animated_avatar', 'is_bot'):
                try:
                    value=kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    processable[key]=value
                    
            if kwargs:
                raise ValueError(f'Unused or unsettable attributes: {kwargs}')
            
            try:
                user=USERS[user_id]
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                
                user.name=''
                user.discriminator=0
                user.avatar=0
                user.has_animated_avatar=False
                user.is_bot=False
                
                user.guild_profiles={}
                user.partial=True
            else:
                if not user.partial:
                    return user
    
            try:
                user.avatar,user.has_animated_avatar=_parse_ih_fsa(
                    processable.get('avatar'),
                    processable.get('has_animated_avatar',False))
            except KeyError:
                pass
            
            for attr in ('name', 'discriminator', 'is_bot'):
                try:
                    value=processable[attr]
                except KeyError:
                    continue
                setattr(user,attr,value)
            
            return user

    def _update_no_return(self,data):
        self.name=data['username']
        self.discriminator=int(data['discriminator'])

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

    if CACHE_PRESENCE:
        @classmethod
        def _create_and_update(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=None
                
            user_id=int(user_data['id'])

            try:
                user=USERS[user_id]
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                user.guild_profiles={}
                user.status=Status.offline
                user.statuses={}
                user.activities=[]
                
                USERS[user_id]=user

            user.partial=False
            user.is_bot=user_data.get('bot',False)
            user._update_no_return(user_data)

            if member_data is not None and guild is not None:
                try:
                    profile=user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id]=user
                    user.guild_profiles[guild]=GuildProfile(member_data,guild)
                else:
                    profile._set_joined(member_data)
                    profile._update_no_return(member_data,guild)
        
            return user
        
    elif CACHE_USER:
        @classmethod
        def _create_and_update(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=None
                
            user_id=int(user_data['id'])

            try:
                user=USERS[user_id]
            except KeyError:
                user=object.__new__(cls)
                user.id=user_id
                user.guild_profiles={}
                
                USERS[user_id]=user

            user.partial=False
            user.is_bot=user_data.get('bot',False)
            user._update_no_return(user_data)

            if member_data is not None and guild is not None:
                try:
                    profile=user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id]=user
                    user.guild_profiles[guild]=GuildProfile(member_data,guild)
                else:
                    profile._set_joined(member_data)
                    profile._update_no_return(member_data,guild)
        
            return user
        
    else:
        @classmethod
        def _create_and_update(cls,data,guild=None):
            try:
                user_data=data['user']
                member_data=data
            except KeyError:
                user_data=data
                member_data=None
                
            user_id=int(user_data['id'])

            user=object.__new__(cls)
            user.id=user_id
            user.guild_profiles={}
            user.partial=False
            user.is_bot=user_data.get('bot',False)
            user._update_no_return(user_data)

            if member_data is not None and guild is not None:
                user.guild_profiles[guild]=GuildProfile(member_data,guild)
        
            return user
       
    def _delete(self):
        #we cannot full delete a user, because of the mentions, so we delete it only from the guilds
        self.guild_profiles.clear()

    #if CACHE_PRESENCE is False, this should be never called from this class
    def _update_presence(self,data):
        old={}
        
        statuses=data['client_status']
        if self.statuses!=statuses:
            old['statuses']=self.statuses
            self.statuses=statuses

            status=data['status']
            if self.status.value!=status:
                old['status']=self.status
                self.status=Status.INSTANCES[status]
            
        activity_datas=data['activities']
        if activity_datas:
            should_pass=False
            old_activities=self.activities
            self.activities=new_activities=[]

            if old_activities:
                for activity_data in activity_datas:
                    activitiy_type=activity_data['type']
                    for index in range(len(old_activities)):
                        activity=old_activities[index]
                        if type(activity) is dict:
                            continue
                        if activitiy_type==activity.type:
                            if activity_data['id']!=activity.discord_side_id:
                                continue
                            changes=activity._update(activity_data)
                            if changes:
                                should_pass=True
                                changes['activity']=activity
                                old_activities[index]=changes
                            new_activities.append(activity)
                            break
                    else:
                        should_pass=True
                        new_activities.append(Activity(activity_data))
                            
            else:
                should_pass=True
                for activity_data in activity_datas:
                    new_activities.append(Activity(activity_data))

            if should_pass:
                old['activities']=old_activities
                
        elif self.activities:
            old['activities']=self.activities
            self.activities=[]

        return old

    def _update_presence_no_return(self,data):
        self.status=Status.INSTANCES[data['status']]
        
        try:
            # not included sometimes
            self.statuses=data['client_status']
        except KeyError:
            pass
        
        activity_datas=data['activities']
        if activity_datas:
            old_activities=self.activities
            self.activities=new_activities=[]

            if old_activities:
                for activity_data in activity_datas:
                    activitiy_type=activity_data['type']
                    for index in range(len(old_activities)):
                        activity=old_activities[index]
                        if activitiy_type==activity.type:
                            if activity_data['id']!=activity.discord_side_id:
                                continue
                            activity._update_no_return(activity_data)
                            del old_activities[index]
                            new_activities.append(activity)
                            break
                    else:
                        new_activities.append(Activity(activity_data))
            else:
                for activity_data in activity_datas:
                    new_activities.append(Activity(activity_data))
        elif self.activities:
            self.activities.clear()
    
    def _update(self,data):
        old={}
        
        name=data['username']
        if self.name!=name:
            old['name']=self.name
            self.name=name

        discriminator=int(data['discriminator'])
        if self.discriminator!=discriminator:
            old['discriminator']=self.discriminator
            self.discriminator=discriminator

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
                
        if self.avatar!=avatar:
            old['avatar']=self.avatar
            self.avatar=avatar

        if self.has_animated_avatar!=has_animated_avatar:
            old['has_animated_avatar']=self.has_animated_avatar
            self.has_animated_avatar=has_animated_avatar

        return old

    @classmethod
    def _update_profile(cls,data,guild):
        user_id=int(data['user']['id'])
        
        try:
            user=USERS[user_id]
        except KeyError:
            user=cls(data,guild)
            return user,{}
        
        try:
            profile=user.guild_profiles[guild]
        except KeyError:
            user.guild_profiles[guild]=GuildProfile(data,guild)
            guild.users[user_id]=user
            return user,{}

        profile._set_joined(data)
        return user,profile._update(data,guild)

    @classmethod
    def _update_profile_no_return(cls,data,guild):
        user_id=int(data['user']['id'])

        try:
            user=USERS[user_id]
        except KeyError:
            cls(data,guild)
            return

        try:
            profile=user.guild_profiles[guild]
        except KeyError:
            user.guild_profiles[guild]=GuildProfile(data,guild)
            return

        profile._update_no_return(data,guild)


    if CACHE_PRESENCE:
        @classmethod
        def _from_GWU_data(cls,data):
            user_id=int(data['id'])
            try:
                return USERS[user_id]
            except KeyError:
                pass
            user=object.__new__(cls)
            user.id=user_id
            user.guild_profiles={}
            user.is_bot=data.get('bot',False)
            user.status=Status.INSTANCES[data['status']]
            user.statuses={}
            user.activities=[]
            user.partial=False
            user._update_no_return(data)
            USERS[user_id]=user
            return user
    
    elif CACHE_USER:
        @classmethod
        def _from_GWU_data(cls,data):
            user_id=int(data['id'])
            try:
                return USERS[user_id]
            except KeyError:
                pass
            user=object.__new__(cls)
            user.id=user_id
            user.guild_profiles={}
            user.is_bot=data.get('bot',False)
            user.partial=False
            user._update_no_return(data)
            USERS[user_id]=user
            return user
    
    else:
        @classmethod
        def _from_GWU_data(cls,data):
            user_id=int(data['id'])
            user=object.__new__(cls)
            user.id=user_id
            user.guild_profiles={}
            user.is_bot=data.get('bot',False)
            user.partial=False
            user._update_no_return(data)
            return user
        
class VoiceState(object):
    __slots__=('channel', 'deaf', 'mute', 'self_deaf', 'self_mute', 'self_video',
        'session_id', 'user',)
    def __init__(self,data,channel):
        self.channel        = channel
        self.user           = PartialUser(int(data['user_id']))
        self.session_id     = data['session_id']
        self.mute           = data['mute']
        self.deaf           = data['deaf']
        self.self_mute      = data['self_mute']
        self.self_deaf      = data['self_deaf']
        #private or group can be self_video, guild can be stream?
        if data['self_video']:
            self.self_video = True
        else:
            self.self_video = data.get('self_stream',False)

    @property
    def guild(self):
        return self.channel.guild
    
    def _update(self,data,channel):
        old={}

        if self.channel is not channel:
            old['channel']=self.channel
            self.channel=channel

        mute=data['mute']
        if self.mute!=mute:
            old['mute']=self.mute
            self.mute=mute

        deaf=data['deaf']
        if self.deaf!=deaf:
            old['deaf']=self.deaf
            self.deaf=deaf
            
        self_mute=data['self_mute']
        if self.self_mute!=self_mute:
            old['self_mute']=self.self_mute
            self.self_mute=self_mute

        self_deaf=data['self_deaf']
        if self.self_deaf!=self_deaf:
            old['self_deaf']=self.self_deaf
            self.self_deaf=self_deaf

        self_video=data['self_video']
        if not self_video:
            self_video=data.get('self_stream',False)
        if self.self_video!=self_video:
            old['self_video']=self.self_video
            self.self_video=self_video

        return old
    
    def _update_no_return(self,data,channel):
        self.channel    = channel
        self.mute       = data['mute']
        self.deaf       = data['deaf']
        self.self_mute  = data['self_mute']
        self.self_deaf  = data['self_deaf']
        if data['self_video']:
            self.self_video = True
        else:
            self.self_video = data.get('self_stream',False)

    def __repr__(self):
        return f'<{self.__class__.__name__} user={self.user.full_name} channel={self.channel!r}>'
    
ZEROUSER=object.__new__(User)
ZEROUSER.id             = 0
ZEROUSER.name           = ''
ZEROUSER.discriminator  = 0
ZEROUSER.avatar         = 0

ZEROUSER.has_animated_avatar=False
ZEROUSER.guild_profiles = {}
ZEROUSER.is_bot         = True
ZEROUSER.partial        = True

if CACHE_PRESENCE:
    ZEROUSER.activities     = []
    ZEROUSER.status         = Status.offline
    ZEROUSER.statuses       = {}

del URLS
del modulize
del CACHE_USER
del CACHE_PRESENCE
