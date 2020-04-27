# -*- coding: utf-8 -*-
__all__ = ('GWChannelReflection', 'GWUserReflection', 'Guild', 'GuildEmbed', 'GuildFeature', 'GuildPreview',
    'GuildWidget', 'SystemChannelFlag', )

import re

from ..backend.dereaddons_local import autoposlist, cached_property, weakposlist, _spaceholder
from ..backend.futures import Task

from .bases import DiscordEntity, ReverseFlagBase
from .client_core import CACHE_PRESENCE, GUILDS
from .others import EMOJI_NAME_RP, VoiceRegion, Status, VerificationLevel, MessageNotificationLevel, MFA, \
    ContentFilterLevel
from .user import User, PartialUser, VoiceState, UserBase, ZEROUSER
from .role import Role
from .channel import CHANNEL_TYPES, ChannelCategory
from .http import URLS
from .permission import Permission
from .activity import Activity, ActivityUnknown
from .emoji import Emoji
from .webhook import Webhook
from .oauth2 import parse_preferred_locale, DEFAULT_LOCALE
from .preconverters import preconvert_snowflake, preconvert_image_hash, preconvert_animated_image_hash, preconvert_str

from . import ratelimit

VoiceClient=NotImplemented

LARGE_LIMIT=250 #can be between 50 and 250

EMOJI_UPDATE_NEW    = 0
EMOJI_UPDATE_DELETE = 1
EMOJI_UPDATE_EDIT   = 2

class GuildFeature(object):
    # class related
    INSTANCES={}
    
    @classmethod
    def get(cls,value):
        try:
            guild_feature=cls.INSTANCES[value]
        except KeyError:
            guild_feature=cls(value)
        
        return guild_feature
    
    # object related
    __slots__=('value',)
    
    def __init__(self,value):
        self.value=value
        self.INSTANCES[value]=self
    
    def __str__(self):
        return self.value

    name=property(__str__)
    
    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def __gt__(self,other):
        if type(self) is type(other):
            return self.value>other.value
        if isinstance(other,str):
            return self.value>other
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.value>=other.value
        if isinstance(other,str):
            return self.value>=other
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.value==other.value
        if isinstance(other,str):
            return self.value==other
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.value!=other.value
        if isinstance(other,str):
            return self.value!=other
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.value<=other.value
        if isinstance(other,str):
            return self.value<=other
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.value<other.value
        if isinstance(other,str):
            return self.value<other
        return  NotImplemented
    
    # predefined
    animated_icon               = NotImplemented
    banner                      = NotImplemented
    commerce                    = NotImplemented
    discoverable                = NotImplemented
    enabled_discoverable_before = NotImplemented
    featurable                  = NotImplemented
    member_list_disabled        = NotImplemented
    more_emoji                  = NotImplemented
    news                        = NotImplemented
    partnered                   = NotImplemented
    public                      = NotImplemented
    public_disabled             = NotImplemented
    relay_enabled               = NotImplemented
    splash                      = NotImplemented
    vanity                      = NotImplemented
    verified                    = NotImplemented
    vip                         = NotImplemented
    welcome_screen              = NotImplemented


GuildFeature.animated_icon              = GuildFeature('ANIMATED_ICON')
GuildFeature.banner                     = GuildFeature('BANNER')
GuildFeature.commerce                   = GuildFeature('COMMERCE')
GuildFeature.discoverable               = GuildFeature('DISCOVERABLE')
GuildFeature.enabled_discoverable_before= GuildFeature('ENABLED_DISCOVERABLE_BEFORE')
GuildFeature.featurable                 = GuildFeature('FEATURABLE')
GuildFeature.member_list_disabled       = GuildFeature('MEMBER_LIST_DISABLED')
GuildFeature.more_emoji                 = GuildFeature('MORE_EMOJI')
GuildFeature.news                       = GuildFeature('NEWS')
GuildFeature.partnered                  = GuildFeature('PARTNERED')
GuildFeature.public                     = GuildFeature('PUBLIC')
GuildFeature.public_disabled            = GuildFeature('PUBLIC_DISABLED')
GuildFeature.relay_enabled              = GuildFeature('RELAY_ENABLED')
GuildFeature.splash                     = GuildFeature('INVITE_SPLASH')
GuildFeature.vanity                     = GuildFeature('VANITY_URL')
GuildFeature.verified                   = GuildFeature('VERIFIED')
GuildFeature.vip                        = GuildFeature('VIP_REGIONS')
GuildFeature.welcome_screen             = GuildFeature('WELCOME_SCREEN_ENABLED')

class SystemChannelFlag(ReverseFlagBase):
    __keys__ = {
        'welcome': 0,
        'boost' : 1,
            }
    
    @property
    def none(self):
        return self==self.NONE
    
    @property
    def all(self):
        return self==self.ALL
    
    NONE    = NotImplemented
    ALL     = NotImplemented

SystemChannelFlag.NONE  = SystemChannelFlag(0b11)
SystemChannelFlag.ALL   = SystemChannelFlag(0b00)

class GuildEmbed(object):
    __slots__=('channel', 'enabled', 'guild',)
    def __init__(self,data,guild):
        self.guild  = guild
        self.enabled= guild.embed_enabled=data['enabled']
        channel_id=data['channel_id']
        if channel_id is not None:
            channel=guild.all_channel[int(channel_id)]
        else:
            channel=None
        self.channel= guild.embed_channel=channel
    
    @classmethod
    def from_guild(cls,guild):
        self=object.__new__(cls)
        self.enabled= guild.embed_enabled
        self.channel= guild.embed_channel
        self.guild  = guild
        return self

    def __repr__(self):
        return f'<{self.__class__.__name__} of guild {self.guild!r}>'

class GWUserReflection(DiscordEntity):
    __slots__ = ('activity_name', 'avatar_url', 'discrimintator', 'name', 'status')
    
    def __init__(self,data):
        self.name           = data['username']
        self.id             = int(data['id'])
        self.discrimintator = int(data['discriminator'])
        self.avatar_url     = data['avatar_url']
        self.status         = Status.INSTANCES[data['status']]
        try:
            activity_data = data['game']
        except KeyError:
            activity_name = None
        else:
            activity_name = activity_data['name']
        
        self.activity_name  = activity_name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name} ({self.id})>'

class GWChannelReflection(DiscordEntity):
    __slots__  = ('name', 'position')
    
    def __init__(self,data):
        self.id = int(data['id'])
        self.name = data['name']
        self.position=data['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name} ({self.id})>'
    
    def __gt__(self,other):
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id > other.id:
                    return True
        
        return NotImplemented
    
    def __ge__(self,other):
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id >= other.id:
                    return True
        
        return NotImplemented
    
    def __le__(self,other):
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id <= other.id:
                    return True
        
        return NotImplemented
    
    def __lt__(self,other):
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id < other.id:
                    return True
        
        return NotImplemented

class GuildWidget(object):
    __slots__=('_cache', '_data', 'guild',)
                 
    def __init__(self,data):
        self.guild=Guild._from_GW_data(data)
        self._data=data
        self._cache={}
    
    json_url=property(URLS.guild_widget_json_url)
    
    @property
    def id(self):
        return self.guild.id
    
    @property
    def name(self):
        return self.guild.name
    
    @property
    def invite_url(self):
        invite_url=self._data.get('instant_invite',None)
        if invite_url is None:
            return ''
        return invite_url
    
    @property
    def presence_count(self):
        return self._data['presence_count']
    
    @cached_property
    def users(self):
        return [GWUserReflection(GWU_data) for GWU_data in self._data['members']]

    @cached_property
    def channels(self):
        return [GWChannelReflection(GWC_data) for GWC_data in self._data['channels']]
    
    def __repr__(self):
        return f'<{self.__class__.__name__} of guild {self.guild.name}>'
    
#we need to ignore client adding, because clients count to being not
#partial. If a guild is not partial it wont get update on Guild.__new__
def PartialGuild(data):
    if (data is None) or (not data):
        return None
    guild_id=int(data['id'])
    try:
        return GUILDS[guild_id]
    except KeyError:
        pass

    guild=object.__new__(Guild)
    GUILDS[guild_id]=guild
    guild.id=guild_id
    guild.available=not data.pop('unavailable',False)

    # set default values
    guild._boosters = None
    guild._cache_perm={}
    guild.afk_channel=None
    guild.afk_timeout=0
    guild.all_channel={}
    guild.all_role={}
    #available set up
    guild.banner=0
    guild.booster_count=-1
    guild.channels=weakposlist()
    guild.clients=[]
    guild.content_filter=ContentFilterLevel.disabled
    # description will be set down
    guild.discovery_splash=0
    guild.embed_channel=None
    guild.embed_enabled=False
    guild.emojis={}
    guild.features=[]
    # has_animated_icon will be set down
    # icon will be set down
    # id is set up
    guild.is_large=False
    guild.max_presences=5000
    guild.max_users=250000
    guild.max_video_channel_users=25
    guild.message_notification=MessageNotificationLevel.only_mentions
    guild.mfa=MFA.none
    # name will be set down
    guild.owner=ZEROUSER
    guild.preferred_locale=DEFAULT_LOCALE
    guild.premium_tier=0
    guild.public_updates_channel=None
    guild.region=VoiceRegion.eu_central
    guild.roles=autoposlist()
    guild.rules_channel=None
    # splash will be set down
    guild.system_channel=None
    guild.system_channel_flags=SystemChannelFlag.NONE
    guild.user_count=1
    guild.users={}
    guild.vanity_code=None
    guild.verification_level=VerificationLevel.none
    guild.voice_states={}
    guild.webhooks={}
    guild.webhooks_uptodate=False
    guild.widget_channel=None
    guild.widget_enabled=False

    if len(data)<2:
        guild.name=''
        guild.icon=0
        guild.has_animated_icon=False
        guild.splash=0
        guild.description=None
        return guild
    
    guild.name=data.get('name','')
    
    icon=data.get('icon',None)
    if icon is None:
        guild.icon=0
        guild.has_animated_icon=False
    elif icon.startswith('a_'):
        guild.icon=int(icon[2:],16)
        guild.has_animated_icon=True
    else:
        guild.icon=int(icon,16)
        guild.has_animated_icon=False
    
    splash=data.get('splash',None)
    guild.splash=0 if splash is None else int(splash,16)
    
    guild.description=data.get('description',None)
    
    try:
        verification_level=data['verification_level']
    except KeyError:
        pass
    else:
        guild.verification_level=VerificationLevel.INSTANCES[verification_level]
    
    try:
        features=data['features']
    except KeyError:
        guild.features.clear()
    else:
        features=[GuildFeature.get(feature) for feature in features]
        features.sort()
        guild.features=features
        
    return guild

#discord does not sends `embed_channel`, `embed_enabled`, `widget_channel`,
#`widget_enabled`, `max_presences`, `max_users` correctly and thats sad.
class Guild(DiscordEntity, immortal=True):
    __slots__ = ('_boosters', '_cache_perm', 'afk_channel', 'afk_timeout', 'all_channel', 'all_role', 'available',
        'banner', 'booster_count', 'channels', 'clients', 'content_filter', 'description', 'discovery_splash',
        'embed_channel', 'embed_enabled', 'emojis', 'features', 'has_animated_icon', 'icon',  'is_large',
        'max_presences', 'max_users', 'max_video_channel_users', 'message_notification', 'mfa', 'name', 'owner',
        'preferred_locale', 'premium_tier', 'public_updates_channel', 'region', 'roles', 'rules_channel', 'splash',
        'system_channel', 'system_channel_flags', 'user_count', 'users', 'vanity_code', 'verification_level',
        'voice_states', 'webhooks', 'webhooks_uptodate', 'widget_channel', 'widget_enabled',)
    
    def __new__(cls,data,client):
        guild_id=int(data['id'])
        
        try:
            guild=GUILDS[guild_id]
            update= (not guild.clients)
        except KeyError:
            guild=object.__new__(cls)
            GUILDS[guild_id]=guild
            guild.id=guild_id

            guild.clients=[]
            guild.users={}
            guild.emojis={}
            guild.voice_states={}
            guild.all_role={}
            guild.roles=autoposlist()
            guild.channels=weakposlist()
            guild.all_channel={}
            guild.features=[]
            guild.webhooks={}
            guild.webhooks_uptodate=False
            guild._cache_perm={}
            
            update=True
        
        guild.available = (not data.get('unavailable',False))
        
        if update:
            guild.user_count=data.get('member_count',1)
            guild.booster_count=-1
            
            try:
                guild.is_large=data['large']
            except KeyError:
                guild.is_large=guild.user_count>=LARGE_LIMIT
            
            try:
                role_datas=data['roles']
            except KeyError:
                pass
            else:
                for role_data in role_datas:
                    Role(role_data,guild)
            
            try:
                emoji_datas=data['emojis']
            except KeyError:
                pass
            else:
                emojis=guild.emojis
                for emoji_data in emoji_datas:
                    emoji=Emoji(emoji_data,guild)
                    emojis[emoji.id]=emoji
            
            try:
                channel_datas=data['channels']
            except KeyError:
                pass
            else:
                later=[]
                for channel_data in channel_datas:
                    channel_type=CHANNEL_TYPES[channel_data['type']]
                    if channel_type is ChannelCategory:
                        channel_type(channel_data,client,guild)
                    else:
                        later.append((channel_type,channel_data),)
                for channel_type,channel_data in later:
                    channel_type(channel_data,client,guild)
            
            guild._update_no_return(data)
            
            if CACHE_PRESENCE:
                try:
                    user_datas=data['members']
                except KeyError:
                    pass
                else:
                    for user_data in user_datas:
                        User(user_data,guild)
                #if user caching is disabled, then presence caching is too.
                try:
                    presence_data=data['presences']
                except KeyError:
                    pass
                else:
                    guild._apply_presences(presence_data)
            
            try:
                voice_state_datas=data['voice_states']
            except KeyError:
                pass
            else:
                for voice_state_data in voice_state_datas:
                    user=PartialUser(int(voice_state_data['user_id']))
                    if user.id in guild.voice_states:
                        continue
                    
                    channel_id=voice_state_data.get('channel_id',None)
                    if channel_id is None:
                        continue
                    channel=guild.all_channel[int(channel_id)]
                    
                    guild.voice_states[user.id]=VoiceState(voice_state_data,channel)

        if (not CACHE_PRESENCE):
            #we get information about the client here
            try:
                user_datas=data['members']
            except KeyError:
                pass
            else:
                for user_data in user_datas:
                    User._bypass_no_cache(user_data,guild)
        
        if client not in guild.clients:
            try:
                ghost_state=guild.voice_states[client.id]
            except KeyError:
                pass
            else:
                Task(VoiceClient._kill_ghost(client,ghost_state.channel),client.loop)
            guild.clients.append(client)
        
        return guild

    @classmethod
    def precreate(cls, guild_id, **kwargs):
        guild_id = preconvert_snowflake(guild_id, 'guild_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            for key in ('banner', 'splash', 'discovery_splash'):
                try:
                    value = kwargs.pop('key')
                except KeyError:
                    pass
                else:
                    value = preconvert_image_hash(value, key)
                    processable.append((key, value))
            
            try:
                icon = kwargs.pop('icon')
            except KeyError:
                if 'has_animated_icon' in kwargs:
                    raise TypeError('`has_animated_icon` was passed without passing `icon`.')
            else:
                has_animated_icon = kwargs.pop('has_animated_icon', False)
                icon, has_animated_icon = preconvert_animated_image_hash(icon, has_animated_icon, 'icon', 'has_animated_icon')
                processable.append(('icon', icon))
                processable.append(('has_animated_icon', has_animated_icon))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            guild=object.__new__(cls)
            guild._boosters=None
            guild._cache_perm={}
            guild.afk_channel=None
            guild.afk_timeout=0
            guild.all_channel={}
            guild.all_role={}
            guild.available=False
            guild.banner=0
            guild.booster_count=-1
            guild.channels=weakposlist()
            guild.clients=[]
            guild.content_filter=ContentFilterLevel.disabled
            guild.description=None
            guild.discovery_splash=0
            guild.embed_channel=None
            guild.embed_enabled=False
            guild.emojis={}
            guild.features=[]
            guild.has_animated_icon=False
            guild.icon=0
            guild.id=guild_id
            guild.is_large=False
            guild.max_presences=5000
            guild.max_users=250000
            guild.max_video_channel_users=25
            guild.message_notification=MessageNotificationLevel.only_mentions
            guild.mfa=MFA.none
            guild.name=''
            guild.owner=ZEROUSER
            guild.preferred_locale=DEFAULT_LOCALE
            guild.premium_tier=0
            guild.public_updates_channel=None
            guild.region=VoiceRegion.eu_central
            guild.roles=autoposlist()
            guild.rules_channel=None
            guild.splash=0
            guild.system_channel=None
            guild.system_channel_flags=SystemChannelFlag.NONE
            guild.user_count=1
            guild.users={}
            guild.vanity_code=None
            guild.verification_level=VerificationLevel.none
            guild.voice_states={}
            guild.webhooks={}
            guild.webhooks_uptodate=False
            guild.widget_channel=None
            guild.widget_enabled=False
            GUILDS[guild_id]=guild
        else:
            if guild.clients:
                return guild
        
        if (processable is not None):
            for item in processable:
                setattr(guild, *item)
        
        return guild

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name if self.clients else "Partial"} ({self.id})>'
    
    def __format__(self,code):
        if not code:
            return self.name
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')

    banner_url=property(URLS.guild_banner_url)
    banner_url_as=URLS.guild_banner_url_as
    icon_url=property(URLS.guild_icon_url)
    icon_url_as=URLS.guild_icon_url_as
    splash_url=property(URLS.guild_splash_url)
    splash_url_as=URLS.guild_splash_url_as
    discovery_splash_url=property(URLS.guild_discovery_splash_url)
    discovery_splash_url_as=URLS.guild_discovery_splash_url_as
    embed_url=URLS.guild_embed_url
    widget_url=URLS.guild_widget_url

    def _update_embed(self,data):
        self.embed_enabled=data.get('enabled',False)

        channel_id=data.get('id',None)
        if channel_id is None:
            self.embed_channel=None
        else:
            self.embed_channel=self.all_channel[int(channel_id)]
    
    @property
    def embed(self):
        return GuildEmbed.from_guild(self)

    def _delete(self,client=None):
        if client is not None:
            try:
                self.clients.remove(client)
            except ValueError:
                pass

        if self.clients:
            return

        categories=self.channels
        for category_index in range(len(categories)-1,-1,-1):
            category=categories[category_index]
            if type(category) is ChannelCategory:
                channels=category.channels
                for channel_index in range(len(channels)-1,-1,-1):
                    channel=channels[channel_index]
                    channel._delete(client)
            category._delete(client)

        for emoji in list(self.emojis.values()):
            emoji._delete()

        self.voice_states.clear()
        
        users=self.users

        for user in list(users.values()):
            if type(user) is User:
                del user.guild_profiles[self]
            del self.users[user.id]

        roles=self.roles
        for index in range(len(roles)-1,-1,-1):
            roles[index]._delete()

        self.webhooks.clear()
        self.webhooks_uptodate=False
        self._boosters=None

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

            channel=self.all_channel[int(channel_id)]

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
                state=self.voice_states.pop(user.id)
            except KeyError:
                return
            return _spaceholder

        channel=self.all_channel[int(channel_id)]

        try:
            state=self.voice_states[user.id]
        except KeyError:
            self.voice_states[user.id]=VoiceState(data,channel)
            return channel

        state._update_no_return(data,channel)
        return channel

    @property
    def text_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type==0]

    @property
    def voice_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type==2]

    @property
    def category_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type==4]

    @property
    def news_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type==5]

    @property
    def store_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type==6]

    @property
    def messageable_channels(self):
        return [channel for channel in self.all_channel.values() if channel.type in (0,5)]
    
    @property
    def default_role(self):
        return self.roles[0]
    
    @property
    def partial(self):
        return (not self.clients)
    
    def _sync(self,data,client):
        try:
            self.is_large=data['large']
        except KeyError:
            self.is_large=self.user_count>=LARGE_LIMIT
        
        self._update_no_return(data)
        
        try:
            role_datas=data['roles']
        except KeyError:
            pass
        else:
            self._sync_roles(role_datas)
        
        try:
            emoji_datas=data['emojis']
        except KeyError:
            pass
        else:
            self._sync_emojis(emoji_datas)

##        #sadly we dont get voice states with guild_get
##        try:
##            voice_state_datas=data['voice_states']
##        except KeyError:
##            self.voice_states.clear()
##        else:
##            old_voice_states=self.voice_states
##            new_voice_states=self.voice_states={}
##
##            for voice_state_data in voice_state_datas:
##                user=PartialUser(int(voice_state_data['user_id']))
##
##                channel_id=voice_state_data.get('channel_id',None)
##                if channel_id is None:
##                    continue
##                channel=self.all_channel[int(channel_id)]
##
##                try:
##                    voice_state=old_voice_states[user.id]
##                except KeyError:
##                    new_voice_states[user.id]=VoiceState(voice_state_data,channel)
##                    continue
##
##                voice_state._update_no_return(voice_state_data,channel)
##                new_voice_states[user.id]=voice_state

    def _apply_presences(self,data):
        users=self.users
        for presence in data:
            user_id=int(presence['user']['id'])
            try:
                user=users[user_id]
            except KeyError:
                pass
            else:
                user.status=Status.INSTANCES[presence['status']]
                user.statuses=presence['client_status']
                user.activities=[Activity(activity_data) for activity_data in presence['activities']]

    def _sync_channels(self,data,client):
        channels=self.all_channel
        old_ids=set(channels)

        later=[]
        for channel_data in data:
            channel_type=CHANNEL_TYPES[channel_data['type']]
            if channel_type is ChannelCategory:
                #categories
                channel=channel_type(channel_data,client,self)
                channel_id=channel.id
                try:
                    old_ids.remove(channel_id)
                except KeyError:
                    #new channel -> add to other clients too
                    for client_ in self.clients:
                        if client_ is not client:
                            client_.channels[channel_id]=channel
                else:
                    #old channel -> update
                    channel._update_no_return(channel_data)
            else:
                later.append((channel_type,channel_data),)
        #non category channels
        for channel_type,channel_data in later:
            channel=channel_type(channel_data,client,self)
            channel_id=channel.id
            try:
                old_ids.remove(channel_id)
            except KeyError:
                #new channel -> add to other clients too
                for client_ in self.clients:
                    if client_ is not client:
                        client_.channels[channel_id]=channel
            else:
                #old channel -> update
                channel._update_no_return(channel_data)
        #deleting
        for channel_id in old_ids:
            for client_ in self.clients:
                channels[channel_id]._delete(client_)

    def _sync_roles(self,data):
        roles=self.all_role
        old_ids=set(roles)
        #every new role can cause mass switchings at the role orders, can it mess up the order tho?
        for role_data in data:
            role=Role(role_data,self)
            try:
                old_ids.remove(role.id)
                # self._cache_perm.clear() will be called by this at least for the default role.
                role._update_no_return(role_data)
            except KeyError:
                pass

        for role_id in old_ids:
            roles[role_id]._delete()

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
                for user in users.values():
                    if user.discriminator==discriminator and user.name==name:
                        return user

        if len(name)>32:
            return default
        for user in users.values():
            if user.name==name:
                return user
        for user in users.values():
            nick=user.guild_profiles[self].nick
            if nick is None:
                continue
            if nick==name:
                return user
        return default

    def get_user_like(self,name,default=None):
        if not 1<len(name)<33:
            return default
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users.values():
            if pattern.match(user.name) is not None:
                return user
            nick=user.guild_profiles[self].nick
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
        for user in self.users.values():
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            nick=user.guild_profiles[self].nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            result.append(user)
        return result

    def get_users_like_ordered(self,name):
        to_sort=[]
        if not 1<len(name)<33:
            return to_sort
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users.values():
            profile=user.guild_profiles[self]
            if pattern.match(user.name) is not None:
                to_sort.append((profile.joined_at,user,),)
                continue
            nick=profile.nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            joined_at=profile.joined_at
            if joined_at is None:
                to_sort.append((user.created_at,user,),)
            else:
                to_sort.append((profile.joined_at,user,),)

        if not to_sort:
            return to_sort

        to_sort.sort(key=lambda x:x[0])
        return [x[1] for x in to_sort]

    def get_emoji(self,name,default=None):
        emoji=EMOJI_NAME_RP.fullmatch(name)
        if emoji is None:
            return default
        name=emoji.groups()[0]
        for emoji in self.emojis.values():
            if emoji.name==name:
                return emoji
        return default
    
    def get_emoji_like(self,name,default=None):
        target_name_length=len(name)
        if target_name_length<2 or target_name_length>32:
            return default
        pattern=re.compile(re.escape(name),re.I)
        
        accurate_emoji=default
        accurate_name_length=33
        
        for emoji in self.emojis.values():
            emoji_name=emoji.name
            name_length=len(emoji_name)
            if name_length>accurate_name_length:
                continue
            
            if pattern.match(emoji_name) is None:
                continue
            
            if name_length<accurate_name_length:
                accurate_emoji=emoji
                accurate_name_length=name_length
            
            if name_length==target_name_length and name==emoji_name:
                return emoji
            
            continue
        
        return accurate_emoji
    
    def get_channel(self,name,default=None):
        if name.startswith('#'):
            name=name[1:]
        for channel in self.all_channel.values():
            if channel.display_name==name:
                return channel
        for channel in self.all_channel.values():
            if channel.name==name:
                return channel
        return default
    
    def get_channel_like(self, name, default=None):
        if name.startswith('#'):
            name=name[1:]
        
        target_name_length = len(name)
        if target_name_length<2 or target_name_length>100:
            return default
        
        pattern=re.compile(re.escape(name),re.I)
        
        accurate_channel = default
        accurate_name_length = 101
        
        for channel in self.all_role.values():
            channel_name=channel.name
            name_length=len(channel_name)
            if name_length>accurate_name_length:
                continue
            
            if pattern.match(channel_name) is None:
                continue
            
            if name_length<accurate_name_length:
                accurate_channel=channel
                accurate_name_length=name_length
            
            # Compare with display name
            if name_length==target_name_length and name==channel.display_name:
                return channel
            
            continue
        
        return accurate_channel
    
    def get_role(self,name,default=None):
        for role in self.all_role.values():
            if role.name==name:
                return role
        return default
    
    def get_role_like(self, name, default=None):
        target_name_length = len(name)
        if target_name_length<2 or target_name_length>32:
            return default
        
        pattern=re.compile(re.escape(name),re.I)
        
        accurate_role = default
        accurate_name_length = 33
        
        for role in self.all_role.values():
            role_name=role.name
            name_length=len(role_name)
            if name_length>accurate_name_length:
                continue
            
            if pattern.match(role_name) is None:
                continue
            
            if name_length<accurate_name_length:
                accurate_role=role
                accurate_name_length=name_length
            
            if name_length==target_name_length and name==role_name:
                return role
            
            continue
        
        return accurate_role
    
    def permissions_for(self,user):
        if user==self.owner:
            return Permission.permission_all
        
        base=self.roles[0].permissions
        
        try:
            roles=user.guild_profiles[self].roles
        except KeyError:
            if type(user) is Webhook and user.guild is self:
                return base
            return Permission.permission_none
        
        roles.sort()
        for role in roles:
            base|=role.permissions
        
        if Permission.can_administrator(base):
            return Permission.permission_all
        
        return Permission(base)
    
    def cached_permissions_for(self,user):
        try:
            return self._cache_perm[user.id]
        except KeyError:
            permissions=self.permissions_for(user)
            self._cache_perm[user.id]=permissions
            return permissions
    
    def _update(self,data):
        old={}
        
        #ignoring 'roles'
        #ignoring 'emojis'
        #ignoring 'members'
        #ignoring 'presence'
        #ignoring 'channels'
        #ignoring 'voice_states'
        #ignoring 'member_count'
        #ignoring 'large'
        
        name=data['name']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        icon=data.get('icon',None)
        if icon is None:
            icon=0
            has_animated_icon=False
        elif icon.startswith('a_'):
            icon=int(icon[2:],16)
            has_animated_icon=True
        else:
            icon=int(icon,16)
            has_animated_icon=False
        
        if self.icon!=icon:
            old['icon']=self.icon
            self.icon=icon
        
        if self.has_animated_icon!=has_animated_icon:
            old['has_animated_icon']=self.has_animated_icon
            self.has_animated_icon=has_animated_icon
        
        splash=data.get('splash',None)
        splash=0 if splash is None else int(splash,16)
        if self.splash!=splash:
            old['splash']=self.splash
            self.splash=splash
        
        discovery_splash=data.get('discovery_splash',None)
        discovery_splash=0 if discovery_splash is None else int(discovery_splash,16)
        if self.discovery_splash!=discovery_splash:
            old['discovery_splash']=self.discovery_splash
            self.discovery_splash=discovery_splash
        
        region=VoiceRegion.get(data['region'])
        if self.region is not region:
            old['region']=region
            self.region=region

        afk_timeout=data['afk_timeout']
        if self.afk_timeout!=afk_timeout:
            old['afk_timeout']=self.afk_timeout
            self.afk_timeout=afk_timeout

        verification_level=VerificationLevel.INSTANCES[data['verification_level']]
        if self.verification_level is not verification_level:
            old['verification_level']=self.verification_level
            self.verification_level=verification_level

        message_notification=MessageNotificationLevel.INSTANCES[data['default_message_notifications']]
        if self.message_notification is not message_notification:
            old['message_notification']=self.message_notification
            self.message_notification=message_notification

        mfa=MFA.INSTANCES[data['mfa_level']]
        if self.mfa!=mfa:
            old['mfa']=self.mfa
            self.mfa=mfa

        content_filter=ContentFilterLevel.INSTANCES[data.get('explicit_content_filter',0)]
        if self.content_filter is not content_filter:
            old['content_filter']=self.content_filter
            self.content_filter=content_filter

        available=not data.get('unavailable',False)
        if self.available!=available:
            old['available']=self.available
            self.available=available

        try:
            features=data['features']
        except KeyError:
            features=[]
        else:
            features=[GuildFeature.get(feature) for feature in features]
            features.sort()
        if self.features!=features:
            old['features']=self.features
            self.features=features

        system_channel_id=data['system_channel_id']
        if system_channel_id is None:
            system_channel=None
        else:
            system_channel=self.all_channel[int(system_channel_id)]
        if self.system_channel is not system_channel:
            old['system_channel']=self.system_channel
            self.system_channel=system_channel
        
        try:
            system_channel_flags=SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            system_channel_flags=SystemChannelFlag.ALL
        if self.system_channel_flags!=system_channel_flags:
            old['system_channel_flags']=self.system_channel_flags
            self.system_channel_flags=system_channel_flags
        
        public_updates_channel_id=data.get('public_updates_channel_id',None)
        if public_updates_channel_id is None:
            public_updates_channel=None
        else:
            public_updates_channel=self.all_channel[int(public_updates_channel_id)]
        if self.public_updates_channel is not public_updates_channel:
            old['public_updates_channel']=self.public_updates_channel
            self.public_updates_channel=public_updates_channel
        
        owner=PartialUser(int(data['owner_id']))
        if self.owner is not owner:
            old['owner']=self.owner
            self.owner=owner

        afk_channel_id=data['afk_channel_id']
        if afk_channel_id is None:
            afk_channel=None
        else:
            afk_channel=self.all_channel[int(afk_channel_id)]
        if self.afk_channel is not afk_channel:
            old['afk_channel']=self.afk_channel
            self.afk_channel=afk_channel

        widget_enabled=data.get('widget_enabled',False)
        if self.widget_enabled!=widget_enabled:
            old['widget_enabled']=self.widget_enabled
            self.widget_enabled=widget_enabled

        widget_channel_id=data.get('widget_channel_id',None)
        if widget_channel_id is None:
            widget_channel=None
        else:
            widget_channel=self.all_channel[int(widget_channel_id)]

        if self.widget_channel is not widget_channel:
            old['widget_channel']=self.widget_channel
            self.widget_channel=widget_channel

        embed_enabled=data.get('embed_enabled',False)
        if self.embed_enabled!=embed_enabled:
            old['embed_enabled']=self.embed_enabled
            self.embed_enabled=embed_enabled

        embed_channel_id=data.get('embed_channel_id',None)
        if embed_channel_id is None:
            embed_channel=None
        else:
            embed_channel=self.all_channel[int(embed_channel_id)]
        if self.embed_channel is not embed_channel:
            old['embed_channel']=self.embed_channel
            self.embed_channel=embed_channel
        
        rules_channel_id=data.get('rules_channel_id',None)
        if rules_channel_id is None:
            rules_channel=None
        else:
            rules_channel=self.all_channel[int(rules_channel_id)]
        if self.rules_channel is not rules_channel:
            old['rules_channel']=self.rules_channel
            self.rules_channel=rules_channel
        
        description=data.get('description',None)
        if self.description is None:
            if (description is not None):
                old['description']=None
                self.description=description
        else:
            if description is None:
                old['description']=self.description
                self.description=None
            elif self.description!=description:
                old['description']=self.description
                self.description=description
        
        vanity_code=data.get('vanity_url_code',None)
        if self.vanity_code is None:
            if vanity_code is not None:
                old['vanity_code']=None
                self.vanity_code=vanity_code
        else:
            if vanity_code is None:
                old['vanity_code']=self.vanity_code
                self.vanity_code=None
            elif self.vanity_code!=vanity_code:
                old['vanity_code']=self.vanity_code
                self.vanity_code=vanity_code

        banner=data['banner']
        banner=0 if banner is None else int(banner,16)
        if self.banner!=banner:
            old['banner']=self.banner
            self.banner=banner
        
        max_users=data.get('max_members',250000)
        if self.max_users!=max_users:
            old['max_users']=self.max_users
            self.max_users=max_users
        
        max_presences=data.get('max_presences',None)
        if max_presences is None:
            max_presences=5000
        if self.max_presences!=max_presences:
            old['max_presences']=self.max_presences
            self.max_presences=max_presences
        
        max_video_channel_users = data.get('max_video_channel_users', 25)
        if self.max_video_channel_users!=max_video_channel_users:
            old['max_video_channel_users'] = self.max_video_channel_users
            self.max_video_channel_users = max_video_channel_users
        
        premium_tier=data['premium_tier']
        if self.premium_tier!=premium_tier:
            old['premium_tier']=self.premium_tier
            self.premium_tier=premium_tier

        booster_count=data.get('premium_subscription_count',None)
        if booster_count is None:
            booster_count=0
        if self.booster_count!=booster_count:
            old['booster_count']=self.booster_count
            self.booster_count=booster_count
            self._boosters=None

        preferred_locale=parse_preferred_locale(data)
        if self.preferred_locale!=preferred_locale:
            old['preferred_locale']=self.preferred_locale
            self.preferred_locale=preferred_locale
        
        return old
    
    def _update_no_return(self,data):

        #ignoring 'roles'
        #ignoring 'emojis'
        #ignoring 'members'
        #ignoring 'presence'
        #ignoring 'channels'
        #ignoring 'voice_states'
        
        self.name=data['name']
        
        icon=data.get('icon',None)
        if icon is None:
            self.icon=0
            self.has_animated_icon=False
        elif icon.startswith('a_'):
            self.icon=int(icon[2:],16)
            self.has_animated_icon=True
        else:
            self.icon=int(icon,16)
            self.has_animated_icon=False
        
        splash=data.get('splash',None)
        self.splash=0 if splash is None else int(splash,16)
        
        discovery_splash=data.get('discovery_splash',None)
        self.discovery_splash=0 if discovery_splash is None else int(discovery_splash,16)
        
        self.region=VoiceRegion.get(data['region'])
            
        self.afk_timeout=data['afk_timeout']
                
        self.verification_level=VerificationLevel.INSTANCES[data['verification_level']]

        self.message_notification=MessageNotificationLevel.INSTANCES[data['default_message_notifications']]

        self.mfa=MFA.INSTANCES[data['mfa_level']]

        self.content_filter=ContentFilterLevel.INSTANCES[data.get('explicit_content_filter',0)]

        self.available=not data.get('unavailable',False)               

        try:
            features=data['features']
        except KeyError:
            self.features.clear()
        else:
            features=[GuildFeature.get(feature) for feature in features]
            features.sort()
            self.features=features
            
        system_channel_id=data['system_channel_id']
        if system_channel_id is None:
            self.system_channel=None
        else:
            self.system_channel=self.all_channel[int(system_channel_id)]

        try:
            self.system_channel_flags=SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            self.system_channel_flags=SystemChannelFlag.ALL
        
        public_updates_channel_id=data.get('public_updates_channel_id',None)
        if public_updates_channel_id is None:
            self.public_updates_channel=None
        else:
            self.public_updates_channel=self.all_channel[int(public_updates_channel_id)]
        
        self.owner=PartialUser(int(data['owner_id']))
        
        afk_channel_id=data['afk_channel_id']
        if afk_channel_id is None:
            self.afk_channel=None
        else:
            self.afk_channel=self.all_channel[int(afk_channel_id)]
        
        self.widget_enabled=data.get('widget_enabled',False)

        widget_channel_id=data.get('widget_channel_id',None)
        if widget_channel_id is None:
            self.widget_channel=None
        else:
            self.widget_channel=self.all_channel[int(widget_channel_id)]

        self.embed_enabled=data.get('embed_enabled',False)

        embed_channel_id=data.get('embed_channel_id',None)
        if embed_channel_id is None:
            self.embed_channel=None
        else:
            self.embed_channel=self.all_channel[int(embed_channel_id)]
        
        rules_channel_id=data.get('rules_channel_id',None)
        if rules_channel_id is None:
            self.rules_channel=None
        else:
            self.rules_channel=self.all_channel[int(rules_channel_id)]
        
        self.description=data.get('description',None)
        
        self.vanity_code=data.get('vanity_url_code',None)
            
        banner=data['banner']
        self.banner=0 if banner is None else int(banner,16)
        
        self.max_users=data.get('max_members',250000)
        
        max_presences=data.get('max_presences',None)
        self.max_presences=5000 if max_presences is None else max_presences
        
        self.max_video_channel_users = data.get('max_video_channel_users', 25)
        
        self.premium_tier=data['premium_tier']

        booster_count=data.get('premium_subscription_count',None)
        if booster_count is None:
            booster_count=0
        if self.booster_count!=booster_count:
            self.booster_count=booster_count
            self._boosters=None

        self.preferred_locale       = parse_preferred_locale(data)

    def _update_emojis(self,data):
        emojis=self.emojis
        changes=[]
        old_ids=set(emojis)

        for emoji_data in data:
            emoji_id=int(emoji_data['id'])
            try:
                emoji=emojis[emoji_id]
            except KeyError:
                emoji=Emoji(emoji_data,self)
                emojis[emoji_id]=emoji
                changes.append((EMOJI_UPDATE_NEW,emoji,None),)
            else:
                old=emoji._update(emoji_data)
                if old:
                    changes.append((EMOJI_UPDATE_EDIT,emoji,old),)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            emoji=emojis[emoji_id]
            emoji._delete()
            changes.append((EMOJI_UPDATE_DELETE,emoji,None),)

        return changes

    def _sync_emojis(self,data):
        emojis=self.emojis
        old_ids=set(emojis)

        for emoji_data in data:
            emoji_id=int(emoji_data['id'])
            try:
                emoji=emojis[emoji_id]
            except KeyError:
                emoji=Emoji(emoji_data,self)
                emojis[emoji_id]=emoji
            else:
                emoji._update_no_return(emoji_data)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            emoji=emojis[emoji_id]
            emoji._delete()
    
    @property
    def emoji_limit(self):
        limit=(50,100,150,250)[self.premium_tier]
        if limit<200 and (GuildFeature.more_emoji in self.features):
            limit=200
        return limit

    @property
    def bitrate_limit(self):
        limit=(96000,128000,256000,384000)[self.premium_tier]
        if limit<128000 and (GuildFeature.vip in self.features):
            limit=128000
        return limit

    @property
    def upload_limit(self):
        return (8388608,8388608,52428800,104857600)[self.premium_tier]

    widget_json_url=property(URLS.guild_widget_json_url)

    @property
    def boosters(self):
        boosters=self._boosters
        if boosters is None:
            if self.booster_count:
                boosters_ordered=[]
                for user in self.users.values():
                    boosts_since=user.guild_profiles[self].boosts_since
                    if boosts_since is None:
                        continue
                    boosters_ordered.append((boosts_since,user),)
                    
                boosters_ordered.sort(key=lambda element:element[0])
                boosters=[element[1] for element in boosters_ordered]
            else:
                boosters=[]
            
            self._boosters=boosters

        return boosters

    @classmethod
    def _from_GW_data(cls,data):
        guild_id=int(data['id'])
        try:
            return GUILDS[guild_id]
        except KeyError:
            pass
        
        guild=object.__new__(cls)
        guild.id=guild_id
        guild.clients=[]
        guild.name=data['name']
        
        GUILDS[guild_id]=guild

        return guild

class GuildPreview(DiscordEntity):
    __slots__ = ('description', 'discovery_splash', 'emojis', 'features', 'has_animated_icon', 'icon', 'name',
        'online_count', 'splash', 'user_count', )
    
    def __init__(self,data):
        self.description = data.get('description',None)
        
        discovery_splash=data.get('discovery_splash',None)
        self.discovery_splash=0 if discovery_splash is None else int(discovery_splash,16)
        
        emojis={}
        self.emojis=emojis
        try:
            emoji_datas=data['emojis']
        except KeyError:
            pass
        else:
            for emoji_data in emoji_datas:
                emoji=Emoji(emoji_data,None)
                emojis[emoji.id]=emoji
        
        features=[]
        self.features=features
        try:
            feature_datas=data['features']
        except KeyError:
            pass
        else:
            for feature_data in feature_datas:
                feature=GuildFeature.get(feature_data)
                features.append(feature)
            
            features.sort()
        
        icon=data.get('icon',None)
        if icon is None:
            self.icon=0
            self.has_animated_icon=False
        elif icon.startswith('a_'):
            self.icon=int(icon[2:],16)
            self.has_animated_icon=True
        else:
            self.icon=int(icon,16)
            self.has_animated_icon=False
        
        self.id=int(data['id'])
        
        self.name=data['name']
        
        self.online_count=data['approximate_presence_count']
        
        splash=data.get('splash',None)
        self.splash=0 if splash is None else int(splash,16)
        
        self.user_count=data['approximate_member_count']
    
    icon_url=property(URLS.guild_icon_url)
    icon_url_as=URLS.guild_icon_url_as
    splash_url=property(URLS.guild_splash_url)
    splash_url_as=URLS.guild_splash_url_as
    discovery_splash_url=property(URLS.guild_discovery_splash_url)
    discovery_splash_url_as=URLS.guild_discovery_splash_url_as
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} ({self.id})>'
    
    def __format__(self,code):
        if not code:
            return self.name
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')

ratelimit.Guild = Guild

del URLS
del cached_property
del ActivityUnknown
del UserBase
del ratelimit
del DiscordEntity
del ReverseFlagBase
