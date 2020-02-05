# -*- coding: utf-8 -*-
__all__ = ('Client', 'Typer', 'Settings', 'Achievement',)

import re, sys
from math import ceil
from time import monotonic, time as time_now
from collections import deque
from os.path import split as splitpath

from .dereaddons_local import multidict_titled, _spaceholder
from .futures import Future, Task, sleep, CancelledError, WaitTillAll,      \
    WaitTillFirst

from .py_formdata import Formdata
from .py_hdrs import AUTHORIZATION

from .others import Status, id_to_time, log_time_converter, _parse_ih_fsa,  \
    VoiceRegion, ContentFilterLevel, PremiumType, MessageNotificationLevel, \
    bytes_to_base64, FriendRequestFlag, ext_from_base64, Theme, now_as_id,  \
    to_json, VerificationLevel, RelationshipType, random_id, parse_time,    \
    DISCORD_EPOCH

from .user import User, USERS, GuildProfile, UserBase, UserFlag
from .emoji import Emoji, PartialEmoji
from .channel import ChannelCategory, ChannelGuildBase, ChannelPrivate,     \
    ChannelText, ChannelGroup, message_relativeindex, cr_pg_channel_object, \
    message_at_index, messages_till_index, MessageIterator, CHANNEL_TYPES
from .guild import Guild, PartialGuild, GuildEmbed, GuildWidget, GuildFeature
from .http import DiscordHTTPClient, URLS, CDN_ENDPOINT, VALID_ICON_FORMATS,\
    VALID_ICON_FORMATS_EXTENDED
from .role import Role
from .webhook import Webhook,PartialWebhook
from .gateway import DiscordGateway, DiscordGatewaySharder
from .parsers import EventDescriptor, _with_error, IntentFlag, PARSER_DEFAULTS
from .audit_logs import AuditLog, AuditLogIterator
from .invite import Invite
from .message import Message
from .oauth2 import Connection, parse_locale, DEFAULT_LOCALE, AO2Access,    \
    UserOA2, parse_locale_optional
from .exceptions import DiscordException
from .client_core import CLIENTS, start_clients, CACHE_USER, CACHE_PRESENCE,\
    KOKORO, GUILDS
from .voice_client import VoiceClient
from .activity import ActivityUnknown
from .integration import Integration
from .application import Application,Team
from .color import Color

from . import client_core, message

_VALID_NAME_CHARS=re.compile('([0-9A-Za-z_]+)')

class single_user_chunker(object):
    __slots__=('limit', 'timer', 'waiter',)
    def __init__(self,client,limit):
        self.limit=limit
        self.timer=None
        self.waiter=Future(client.loop)

    def start_timer(self,client,timeout):
        if timeout>0.4:
            timeout=0.8
        else:
            timeout+=0.4
        
        self.timer=client.loop.call_later(timeout,self._cancel)
    
    def __call__(self,users):
        if len(users)>self.limit:
            return False
        self.waiter.set_result_if_pending(users)
        timer=self.timer
        if timer is not None:
            timer.cancel()
            self.timer=None
        return True

    def cancel(self):
        timer=self.timer
        if timer is None:
            return
        
        self.waiter.set_result_if_pending(None)
        timer.cancel()
        self.timer=None
        
    def _cancel(self):
        self.waiter.set_result_if_pending(None)
        self.timer=None
        
    def __await__(self):
        return self.waiter.__await__()

class mass_user_chunker(object):
    __slots__=('left', 'timer', 'waiter',)
    def __init__(self,client,left):
        self.left=left
        loop=client.loop
        self.waiter=Future(loop)

        if left<5:
            timeout=0.1
        else:
            timeout=.08*left+0.6

        self.timer=loop.call_later(timeout,self._cancel)

    def __call__(self,users):
        left=self.left-1
        self.left=left
        if left>0:
            return False
        self.waiter.set_result_if_pending(_spaceholder)
        timer=self.timer
        if timer is not None:
            timer.cancel()
            self.timer=None
        return True

    def cancel(self):
        self.left=None
        self.waiter.set_result_if_pending(None)
        timer=self.timer
        if timer is None:
            return
        timer.cancel()
        self.timer=None

    def _cancel(self):
        self.left=0
        self.waiter.set_result_if_pending(None)
        self.timer=None
    
    def __await__(self):
        return self.waiter.__await__()
    
class Client(UserBase):
    __slots__ = (
        'guild_profiles', 'is_bot', 'partial', #default user
        'activities', 'status', 'statuses', #presence
        'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', #OA2
        'verified',
        '__dict__', '_activity', '_gateway_pair', 'application', 'calls', #Client all the way down
        'channels',  'events', 'gateway', 'guild_profiles', 'http', 'intents',
        'loop', 'mar_token', 'private_channels', 'ready_state',
        'relationships', 'running', 'secret', 'settings', 'shard_count',
        'token', 'voice_clients')
    
    def __init__(self,token,secret=None,client_id=0,activity=ActivityUnknown,status=None,is_bot=True,shard_count=0,intents=-1,**kwargs):

        if kwargs:
            self.name=kwargs.pop('name','')
            self.discriminator=int(kwargs.pop('discriminator','0'))
            
            self.avatar,self.has_animated_avatar=_parse_ih_fsa(
                kwargs.pop('avatar',None),
                kwargs.pop('has_animated_avatar',False))

            if kwargs:
                for key,value in kwargs.items():
                    if hasattr(type(self),key):
                        raise AttributeError(key)
                    setattr(self,key,value)
        
        else:
            self.name=''
            self.discriminator=0
            self.avatar=0
            self.has_animated_avatar=False
            
        self.token              = token
        self.secret             = secret
        self.is_bot             = is_bot
        self.shard_count        = shard_count
        self.loop               = KOKORO
        
        if type(intents) is IntentFlag:
            pass
        elif isinstance(intents,int):
            intents=IntentFlag(intents)
        else:
            raise TypeError(f'`intents` should have been passed as `int` or `{IntentFlag.__name__}` instance, got `{intents!r}`')
        
        self.intents            = intents
        self.running            = False
        
        self.mar_token          = None
        
        self.calls              = {} #deprecated ?
        
        self.relationships      = {}
        self.channels           = {}
        
        self.guild_profiles     = {}
        self.status             = Status.offline
        self.statuses           = {}
        self._activity          = activity
        self.activities         = []
        self._gateway_pair      = ('',0.0)
        
        self.private_channels   = {}
        self.voice_clients      = {}

        self.id                 = client_id
        if client_id:
            USERS[client_id]    = self
            
        self.partial            = True
        
        self.ready_state        = None
        
        self.application        = Application()
        self.settings           = Settings()
        
        if shard_count:
            self.gateway        = DiscordGatewaySharder(self)
        else:
            self.gateway        = DiscordGateway(self)
        self.http               = DiscordHTTPClient(self)
        
        if status is not None:
            if type(status) is str:
                try:
                    status=Status.INSTANCES[status]
                except KeyError:
                    raise ValueError(f'Expected status: {", ".join(list(Status.INSTANCES))}; got {status!r}')
            elif type(status) is not Status:
                raise TypeError(f'Expected status types are: str, Status, got {status!r}')
            if status is Status.offline:
                status=Status.invisible
            self.settings.status=status
        
        self.events             = EventDescriptor(self)
        
        CLIENTS.append(self)
        
    def _init_on_ready(self,data):
        client_id           = int(data['id'])
        if self.id!=client_id:
            CLIENTS.update(self,client_id)

        if CACHE_USER:
            try:
                alterego        = USERS[client_id]
            except KeyError:
                pass
            else:
                if alterego is not self:
                    #we already exists, we need to go tru everthing and replace ourself.
                    guild_profiles=alterego.guild_profiles
                    self.guild_profiles=guild_profiles
                    for guild in guild_profiles:
                        guild.users[client_id]=self
                        for channel in guild.channels:
                            for overwrite in channel.overwrites:
                                if overwrite.target is alterego:
                                    overwrite.target=self
                    
                    for client in CLIENTS:
                        if (client is not self) and client.running and (client.loop is not None):
                            for channel in client.channels.values():
                                users=channel.users
                                for index in range(users):
                                    if users[index].id==client_id:
                                        users[index]=self
                                        continue
        else:
            for client in CLIENTS:
                if (client is not self) and client.running and (client.loop is not None):
                    for channel in client.channels.values():
                        users=channel.users
                        for index in range(users):
                            if users[index].id==client_id:
                                users[index]=self
                                continue

                
        self.name           = data['username']
        self.discriminator  = int(data['discriminator'])
        avatar=data['avatar']
        if avatar is None:
            self.avatar     = 0
            self.has_animated_avatar=False
        elif avatar.startswith('a_'):
            self.avatar     = int(avatar[2:],16)
            self.has_animated_avatar=True
        else:
            self.avatar     = int(avatar,16)
            self.has_animated_avatar=False
        self.mfa            = data.get('mfa_enabled',False)
        self.system         = data.get('system',False)
        self.verified       = data.get('verified',False)
        self.email          = data.get('email','')
        self.flags          = UserFlag(data.get('flags',0))
        self.premium_type   = PremiumType.INSTANCES[data.get('premium_type',0)]
        self.locale         = parse_locale(data)

        self.partial        = False

        USERS[client_id]=self

    _update_presence    = User._update_presence
    _update_presence_no_return = User._update_presence_no_return

    @property
    def _platform(self):
        if self.status in (Status.offline,Status.invisible):
            return ''
        return 'web'
        
    #house must be type  HypeSquadHouse
    #avatar is bytes
    async def client_edit(self,password=None,new_password=None,email=None,house=_spaceholder,name=None,avatar=_spaceholder):
        data={}
        
        if (password is None):
            if not self.is_bot:
                raise ValueError('Password is must for non bots!')
        else:
            data['password']=password

        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The length of the name can be between 2-32, got {name_ln}')
            data['username']=name
        
        if avatar is _spaceholder:
            pass
        elif avatar is None:
            data['avatar']=None
        else:
            avatar_data=bytes_to_base64(avatar)
            ext=ext_from_base64(avatar_data)
            if self.premium_type.value:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Invalid image extension: `{ext}`')
            else:
                if ext not in VALID_ICON_FORMATS:
                    if ext=='gif':
                        raise ValueError('Only premium users can have `gif` avatar!')
                    raise ValueError(f'Invalid image extension: `{ext}`')
            data['avatar']=avatar_data
        
        if not self.is_bot:
            if (email is not None):
                data['email']=email
            if (new_password is not None):
                data['new_password']=new_password

        data=await self.http.client_edit(data)
        self._update_no_return(data)
        
        if not self.is_bot:
            self.email=data['email']
            try:
                self.token=data['token']
            except KeyError:
                pass

        if house is _spaceholder:
            pass
        elif house is None:
            await self.hypesquad_house_leave()
        else:
            await self.hypesquad_house_change(house)
        
    #user account only
    #TODO : consider adding folder editing(?)
    async def client_edit_settings(self,**kwargs):
        data={}

        for wrapper_side, discord_side, target_type, transformer in (
                ('accessibility_detection', 'allow_accessibility_detection',bool,                           None,                                       ),
                ('afk_timeout',             'afk_timeout',                  int,                            None,                                       ),
                ('animate_emojis',          'animate_emojis',               bool,                           None,                                       ),
                ('compact_mode',            'message_display_compact',      bool,                           None,                                       ),
                ('content_filter',          'explicit_content_filter',      ContentFilterLevel,             lambda x:x.value,                           ),
                ('convert_emojis',          'convert_emoticons',            bool,                           None,                                       ),
                ('custom_status',           'custom_status',                dict,                           lambda x:Settings.encode_custom_status(x),  ),
                ('detect_platform_accounts','detect_platform_accounts',     bool,                           None,                                       ),
                ('developer_mode',          'developer_mode',               bool,                           None,                                       ),
                ('enable_tts_command',      'enable_tts_command',           bool,                           None,                                       ),
                ('friend_request_flag',     'friend_source_flags',          FriendRequestFlag,              lambda x:x.encode(),                        ),
                ('games_tab',               'disable_games_tab',            bool,                           lambda x:(not x),                           ),
                ('guild_order_ids',         'guild_positions',              list,                           None,                                       ),
                ('locale',                  'locale',                       str,                            None,                                       ),
                ('no_DM_from_new_guilds',   'default_guilds_restricted',    bool,                           None,                                       ),
                ('no_DM_guild_ids',         'restricted_guilds',            list,                           None,                                       ),
                ('play_gifs',               'gif_auto_play',                bool,                           None,                                       ),
                ('render_attachments',      'inline_attachment_media',      bool,                           None,                                       ),
                ('render_embeds',           'render_embeds',                bool,                           None,                                       ),
                ('render_links',            'inline_embed_media',           bool,                           None,                                       ),
                ('render_reactions',        'render_reactions',             bool,                           None,                                       ),
                ('show_current_game',       'show_current_game',            bool,                           None,                                       ),
                ('status',                  'status',                       Status,                         lambda x:x.value,                           ),
                ('stream_notifications',    'stream_notifications_enabled', bool,                           None,                                       ),
                ('theme',                   'theme',                        Theme,                          lambda x:x.value,                           ),
                ('timezone_offset',         'timezone_offset',              int,                            None,                                       ),
                    ):
            try:
                value=kwargs[wrapper_side]
            except KeyError:
                continue

            if type(value) is not target_type:
                raise ValueError(f'Invalid `{wrapper_side}`, expected `{target_type!r}`, got `{value!r}`')
            if transformer is not None:
                value=transformer(value)
            data[discord_side]=value

        data = await self.http.client_edit_settings(data)
        self.settings._update_no_return(data)
    
    #user account only  
    async def client_sync_settings(self):
        data = await self.http.client_get_settings()
        self.settings._update_no_return(data)
        
    async def client_edit_nick(self,guild,nick,reason=None):
        if (nick is not None):
            nick_ln=len(nick)
            if nick_ln>32:
                raise ValueError(f'The length of the nick can be between 1-32, got {nick_ln}')
            if nick_ln==0:
                nick=None
        
        try:
            actual_nick=self.guild_profiles[guild].nick
        except KeyError:
            # we arent at the guild ->  will raise propably
            should_edit_nick=True
        else:
            if nick is None:
                if actual_nick is None:
                    should_edit_nick=False
                else:
                    should_edit_nick=True
            else:
                if actual_nick is None:
                    should_edit_nick=True
                elif nick==actual_nick:
                    should_edit_nick=False
                else:
                    should_edit_nick=True
        
        if should_edit_nick:
            await self.http.client_edit_nick(guild.id,{'nick':nick},reason)

    async def client_connections(self):
        data = await self.http.client_connections()
        return [Connection(connection_data) for connection_data in data]

    async def client_edit_presence(self,activity=None,status=None,afk=False):
        if isinstance(status,str):
            try:
                status=Status.INSTANCES[status]
            except KeyError as err:
                raise ValueError(f'Invalid status {status}') from err
            self.settings.status=status
        elif isinstance(status,Status):
            self.settings.status=status
        elif status is None:
            status=self.settings.status
        else:
            raise TypeError(f'Invalid status type ({type(status)!r}), it must be str or {status!r}')
        
        status=status.value
        
        if activity is None:
            activity=self._activity
        else:
            self._activity=activity
        
        if activity is ActivityUnknown:
            activity=None

        if activity is not None:
            if self.is_bot:
                activity=activity.botdict()
            else:
                activity=activity.hoomandict()

        if status=='idle':
            since=int(time_now()*1000.)
        else:
            since=0.0
        
        data = {
            'op': DiscordGateway.PRESENCE,
            'd' : {
                'game'  : activity,
                'since' : since,
                'status': status,
                'afk'   : afk,
                    },
                }

        await self.gateway.send_as_json(data)

    async def activate_authorization_code(self,redirect_url,code,scopes):
        data = {
            'client_id'     : self.id,
            'client_secret' : self.secret,
            'grant_type'    : 'authorization_code',
            'code'          : code,
            'redirect_uri'  : redirect_url,
            'scope'         : ' '.join(scopes),
                }

        data = await self.http.oauth2_token(data)
        if len(data)==1:
            return
        return AO2Access(data,redirect_url)
    
    # Cannot grant (bug?):
    # - 'activities.read'
    # - 'activities.write'
    # - 'applications.builds.upload'

    async def owners_access(self,scopes):
        data = {
            'client_id'     : self.id,
            'client_secret' : self.secret,
            'grant_type'    : 'client_credentials',
            'scope'         : ' '.join(scopes),
                }

        data = await self.http.oauth2_token(data)
        return AO2Access(data,'')

    #needs `email` or/and `identify` scopes granted for more data
    async def user_info(self,access):
        header=multidict_titled()
        header[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_info(header)
        return UserOA2(data,access)

    #needs `connections` scope granted
    async def user_connections(self,access):
        header=multidict_titled()
        header[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_connections(header)
        return [Connection(connection_data) for connection_data in data]

    async def renew_access_token(self,access):
        redirect_url=access.redirect_url
        if redirect_url:
            data = {
                'client_id'     : self.id,
                'client_secret' : self.secret,
                'grant_type'    : 'refresh_token',
                'refresh_token' : access.refresh_token,
                'redirect_uri'  : redirect_url,
                'scope'         : ' '.join(access.scopes)
                    }
        else:
            data = {
                'client_id'     : self.id,
                'client_secret' : self.secret,
                'grant_type'    : 'client_credentials',
                'scope'         : ' '.join(access.scopes),
                    }

        data = await self.http.oauth2_token(data)

        access._renew(data)

    #needs `guilds.join` scope granted
    async def guild_user_add(self,guild,access_or_compuser,user=None,nick=None,roles=[],mute=False,deaf=False):
        if type(access_or_compuser) is AO2Access:
            access=access_or_compuser
            if user is None:
                raise TypeError('User can not be None if \'access_or_compuser\' is access')
        elif type(access_or_compuser) is UserOA2:
            access=access_or_compuser.access
            if user is None:
                user=access_or_compuser
        else:
            raise TypeError(f'Invalid access_or_compuser type, expected AO2Access or UserOA2, got {access_or_compuser.__class__.__name__}')
        
        data={'access_token':access.access_token}
        if (nick is not None):
            nick_ln=len(nick)
            if nick_ln!=0:
                if nick_ln>32:
                    raise ValueError(f'The length of the nick can be between 1-32, got {nick_ln}')
                data['nick']=nick
                
        if roles:
            data['roles']=[role.id for role in roles]
            
        if mute:
            data['mute']=mute
            
        if deaf:
            data['deaf']=deaf
            
        await self.http.guild_user_add(guild.id,user.id,data)

    #needs `guilds` scope granted
    async def user_guilds(self,access):
        header=multidict_titled()
        header[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_guilds(header)
        return [PartialGuild(guild_data) for guild_data in data]
    
    async def achievement_get_all(self):
        data = await self.http.achievement_get_all(self.application.id)
        return [Achievement(achievement_data) for achievement_data in data]
    
    async def achievement_get(self,achievement_id):
        data = await self.http.achievement_get(self.application.id,achievement_id)
        return Achievement(data)
    
    async def achievement_create(self,name,description,icon,secret=False,secure=False):
        icon_data=bytes_to_base64(icon)
        ext=ext_from_base64(icon_data)
        if ext not in VALID_ICON_FORMATS_EXTENDED:
            raise ValueError(f'Invalid icon type: {ext}')

        data = {
            'name'          : {
                'default'   : name,
                    },
            'description'   : {
                'default'   : description,
                    },
            'secret'        : secret,
            'secure'        : secure,
            'icon'          : icon_data,
                }
        
        data = await self.http.achievement_create(self.application.id,data)
        return Achievement(data)
    
    async def achievement_edit(self,achievement,name=None,description=None,secret=None,secure=None,icon=_spaceholder):
        data={}
        if (name is not None):
            data['name'] = {
                'default'   : name,
                    }
        if (description is not None):
            data['description'] = {
                'default'   : description,
                    }
        if (secret is not None):
            data['secret']=secret
            
        if (secure is not None):
            data['secure']=secure
            
        if (icon is not _spaceholder):
            icon_data=bytes_to_base64(icon)
            ext=ext_from_base64(icon_data)
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Invalid icon type: {ext}')
            data['icon']=icon_data
        
        data = await self.http.achievement_edit(self.application.id,achievement.id,data)
        achievement._update_no_return(data)
        return achievement
    
    async def achievement_delete(self,achievement):
        await self.http.achievement_delete(self.application.id,achievement.id)
    
    # https://github.com/discordapp/discord-api-docs/issues/1230
    # unintentionally documented and will never work.
    
    # DiscordException UNAUTHORIZED (401): 401: Unauthorized
    async def user_achievements(self,access):
        header=multidict_titled()
        header[AUTHORIZATION]=f'Bearer {access.access_token}'
        
        data = await self.http.user_achievements(self.application.id,header)
        return [Achievement(achievement_data) for achievement_data in data]
    
    # https://github.com/discordapp/discord-api-docs/issues/1230
    # Seems like first update must come from game SDK.
    # Only secure updates are supported, if they are even.
    
    # when updating secure achievement:
    #     DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    # when updating non secure:
    #     DiscordException FORBIDDEN (403), code=40001: Unauthorized
    async def user_achievement_update(self,user,achievement,percent_complete):
        data={'percent_complete':percent_complete}
        
        await self.http.user_achievement_update(user.id,self.application.id,achievement.id,data)

    #hooman only
    async def application_get(self,application_id):
        data = await self.http.application_get(application_id)
        return Application(data)
    
    def _delete(self):
        if self.running:
            raise RuntimeError(f'{self.__class__.__name__}._delete called from a running client.')

        CLIENTS.remove(self)
        client_id=self.id
        alterego=object.__new__(User)
        for attrname in User.__slots__:
            if attrname.startswith('__'):
                continue
            setattr(alterego,attrname,getattr(self,attrname))
        
        if CACHE_USER:
            USERS[client_id]=alterego
            guild_profiles=self.guild_profiles
            for guild in guild_profiles:
                guild.users[client_id]=self
                for channel in guild.channels:
                    for overwrite in channel.overwrites:
                        if overwrite.target is alterego:
                            overwrite.target=self
            
            for client in CLIENTS:
                if (client is not self) and client.running and (client.loop is not None):
                    for relationship in client.relationships:
                        if relationship.user is self:
                            relationship.user=alterego
                    
        else:
            try:
                del USERS[client_id]
            except KeyError:
                pass
            guild_profiles=self.guild_profiles
            for guild in guild_profiles:
                try:
                    del guild[client_id]
                except KeyError:
                    pass

        self.relationships.clear()
        for channel in self.channels.values():
            users=channel.users
            for index in range(users):
                if users[index].id==client_id:
                    users[index]=alterego
                    continue

        self.private_channels.clear()
        self.channels.clear()
        self.calls.clear() #deprecated ?
        self.application._fillup()
        self.events.clear()
        
        self.guild_profiles     = {}
        self.status             = Status.offline
        self.statuses           = {}
        self._activity          = ActivityUnknown
        self.activities         = []
        self.ready_state        = None
        
    async def download_url(self,url):
        async with self.http.get(url) as response:
            return (await response.read())

    async def download_attachment(self,attachment):
        if attachment.proxy_url.startswith(CDN_ENDPOINT):
            url=attachment.proxy_url
        else:
            url=attachment.url
        async with self.http.get(url) as response:
            return (await response.read())

    #loggin
        
    async def client_login_static(self):        
        try:
            data = await self.http.client_user()
        except DiscordException as err:
            if err.response.status==401:
                raise ConnectionRefusedError('Invalid token') from err
            raise
            
        return data

    #channels

    async def channel_group_leave(self,channel):
        await self.http.channel_group_leave(channel.id)

    async def channel_group_user_add(self,channel,*users):
        for user in users:
            await self.http.channel_group_user_add(channel.id,user.id)

    async def channel_group_user_delete(self,channel,*users):
        for user in users:
            await self.http.channel_group_user_delete(channel.id,user.id)

    async def channel_group_edit(self,channel,name=_spaceholder,icon=_spaceholder):
        data={}

        if (name is not _spaceholder):
            if (name is not None):
                name_ln=len(name)
                if name_ln==1 or name_ln>100:
                    raise ValueError(f'Channel\'s name\'s length can be between 2-100, got {name_ln}')
                
                if name_ln==0:
                    name=None
            
            data['name']=name
        
        if icon is _spaceholder:
            pass
        elif icon is None:
            data['icon']=None
        else:
            icon_data=bytes_to_base64(icon)
            ext=ext_from_base64(icon_data)
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Invalid icon type: {ext}')
            data['icon']=icon_data
        
        if data:
            await self.http.channel_group_edit(channel.id,data)

    #user only
    async def channel_group_create(self,users):
        if len(users)<2:
            raise ValueError('ChannelGroup must be created with 2 or more users')
        data={'recipients':[user.id for user in users]}
        data=await self.http.channel_group_create(self.id,data)
        return ChannelGroup(data,self)
        
    async def channel_private_create(self,user):
        try:
            channel=self.private_channels[user.id]
        except KeyError:
            data=await self.http.channel_private_create({'recipient_id':user.id})
            channel=ChannelPrivate(data,self)
        return channel

    #returns an empty list for bots
    async def channel_private_get_all(self):
        result=[]
        if self.is_bot:
            return result
        data = await self.http.channel_private_get_all()
        for channel_data in data:
            channel=CHANNEL_TYPES[channel_data['type']](data,self)
            result.append(channel)
        return result

    async def channel_move(self,channel,visual_position,category=_spaceholder,lock_permissions=False,reason=None):
        if category is _spaceholder:
            category=channel.category
        elif category is None:
            category=channel.guild
        elif type(category) is Guild:
            if channel.guild is not category:
                raise ValueError('Can not move channel between guilds!')
        elif type(category) is ChannelCategory:
            if category.guild is not channel.guild:
                raise ValueError('Can not move channel between guilds!')
        else:
            raise TypeError(f'Invalid type {channel!r}')
        
        if type(channel) is type(category):
            raise ValueError('Cant move category under category!')
        
        if channel.category is category and category.channels.index(channel)==visual_position:
            return #saved 1 request

        #making sure
        visual_position=int(visual_position) 

        #quality python code incoming :ok_hand:
        ordered=[]
        indexes=[0,0,0,0,0,0,0] #for the 7 channel type (type 1 and 3 wont be used)

        #loop preparations
        outer_channels=channel.guild.channels
        index_0=0
        limit_0=len(outer_channels)
        #inner loop preparations
        index_1=0
        #loop start
        while True:
            if index_0==limit_0:
                break
            channel_=outer_channels[index_0]
            #loop block start
            
            type_=channel_.type
            type_index=indexes[type_]
            indexes[type_]=type_index+1
            
            ordered.append((index_0,index_1,type_index,channel_),)

            if type_==4:
                #reset type_indexes
                indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
                #loop preparations
                inner_channels=channel_.channels
                limit_1=len(inner_channels)
                #loop start
                while True:
                    if index_1==limit_1:
                        break
                    channel_=inner_channels[index_1]
                    #loop block start
                    
                    type_=channel_.type
                    type_index=indexes[type_]
                    indexes[type_]=type_index+1

                    ordered.append((index_0,index_1,type_index,channel_),)
                    
                    #loop block end
                    index_1=index_1+1
                #reseting inner
                index_1=0
                #loop ended
                
            #loop block end
            index_0=index_0+1
        #loop ended
        
        #prepare loop
        index_0=0
        limit_0=len(ordered)
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            #loop block start
            
            if info_line[3] is channel:
                original_position=index_0
                break

            #loop block end
            index_0=index_0+1
        #loop ended

        restricted_positions=[]
        
        index_0=0
        limit_0=len(ordered)
        last_index=-1
        if type(category) is Guild:
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start
                
                if info_line[0]>last_index:
                    last_index+=1
                    restricted_positions.append(index_0)
                
                #loop block end
                index_0=index_0+1
            #loop ended
        else:
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                category_index=index_0 #we might need it
                #loop block start
                if info_line[3] is category:
                    index_0=index_0+1
                    #loop preapre
                    #loop start
                    while True:
                        if index_0==limit_0:
                            break
                        info_line=ordered[index_0]
                        #loop block start

                        if info_line[3].type==4:
                            break
                        restricted_positions.append(index_0)
                        
                        #loop block end
                        index_0=index_0+1
                    #loop ended
                    break
                
                #loop block end
                index_0=index_0+1
            #loop ended
                
        index_0=(4,2,0).index(channel.ORDER_GROUP)
        before=(4,2,0)[index_0:]
        after =(4,2,0)[:index_0+1]

        possible_indexes=[]
        if restricted_positions:
            #loop prepare
            index_0=0
            limit_0=len(restricted_positions)-1
            info_line=ordered[restricted_positions[index_0]]
            #loop at 0 block start
            
            if info_line[3].ORDER_GROUP in after:
                possible_indexes.append((0,restricted_positions[index_0],),)
                
            #loop at 0 block ended
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[restricted_positions[index_0]]
                #next step mixin
                index_0=index_0+1
                info_line_2=ordered[restricted_positions[index_0]]
                #loop block start

                if info_line[3].ORDER_GROUP in before and info_line_2[3].ORDER_GROUP in after:
                    possible_indexes.append((index_0,restricted_positions[index_0],),)

                #loop block end
            if limit_0:
                info_line=info_line_2
            #loop at -1 block start
            
            if info_line[3].ORDER_GROUP in before:
                possible_indexes.append((index_0+1,restricted_positions[index_0]+1,),)

            #loop at -1 block ended
            #loop ended
        else:
            #empty category
            possible_indexes.append((0,category_index+1,),)
            
        #GOTO start 
        while True:
            #GOTO block start
            
            #loop prepare
            index_0=0
            limit_0=len(possible_indexes)
            info_line=possible_indexes[index_0]
            
            #loop at 0 block start
            if info_line[0]>visual_position:
                result_position=info_line[1]
                
                #GOTO end 
                break
                #GOTO ended
            
            #loop at 0 block ended
            
            #setup GOTO from loop start
            end_goto=False
            #setup GOTO from loop ended
            
            index_0=index_0+1
            while True:
                if index_0==limit_0:
                    break
                info_line=possible_indexes[index_0]
                #loop block start

                if info_line[0]==visual_position:
                    result_position=info_line[1]
                    
                    #GOTO end inner 1
                    end_goto=True
                    break
                    #GOTO ended inner 1

                #loop block end
                index_0=index_0+1
            #loop ended

            #GOTO end
            if end_goto:
                break
            #GOTO ended

            result_position=info_line[1]

            #GOTO block ended
            break
        #GOTO ended
            
        ordered.insert(result_position,ordered[original_position])
        higher_flag=(result_position<original_position)
        if higher_flag:
            original_position=original_position+1
        else:
            result_position=result_position-1
        del ordered[original_position]
        
        if channel.type==4:
            channels_to_move=[]

            #loop prepare
            index_0=original_position
            limit_0=len(ordered)
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start

                if info_line[3].type==4:
                    break
                channels_to_move.append(info_line)
                
                #loop block end
                index_0=index_0+1
            #loop ended

            insert_to=result_position+1
            
            #loop prepare
            index_0=len(channels_to_move)
            limit_0=0
            #loop start
            while True:
                index_0=index_0-1
                info_line=channels_to_move[index_0]
                #loop block start
                
                ordered.insert(insert_to,info_line)
                
                #loop block end
                if index_0==limit_0:
                    break
            #loop ended

            delete_from=original_position
            if higher_flag:
                delete_from=delete_from+len(channels_to_move) #len(channels_to_move)

            #loop prepare
            index_0=0
            limit_0=len(channels_to_move)
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start

                del ordered[delete_from]
                
                #loop block end
                index_0=index_0+1
            #loop ended
                
        indexes[0]=indexes[2]=indexes[4]=indexes[5]=indexes[6]=0 #reset

        #loop preparations
        index_0=0
        limit_0=len(ordered)
        #loop start
        while True:
            if index_0==limit_0:
                break
            channel_=ordered[index_0][3]
            #loop block start
            
            type_=channel_.type
            type_index=indexes[type_]
            indexes[type_]=type_index+1
            
            ordered[index_0]=(type_index,channel_)

            #loop block step
            index_0=index_0+1
            #loop block continue
            
            if type_==4:
                #reset type_indexes
                indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
                #loop preparations
                #loop start
                while True:
                    if index_0==limit_0:
                        break
                    channel_=ordered[index_0][3]
                    #loop block start
                    
                    type_=channel_.type
                    if type_==4:
                        break
                    type_index=indexes[type_]
                    indexes[type_]=type_index+1

                    ordered[index_0]=(type_index,channel_)
                    
                    #loop block end
                    index_0=index_0+1
                
            #loop block end
        #loop ended

        bonus_data={'lock_permissions':lock_permissions}
        if category is channel.guild:
            bonus_data['parent_id']=None
        else:
            bonus_data['parent_id']=category.id
            
        data=[]
        for position,channel_ in ordered:
            if channel is channel_:
                data.append({'id':channel_.id,'position':position,**bonus_data})
                continue
            if channel_.position!=position:
                data.append({'id':channel_.id,'position':position})

        await self.http.channel_move(channel.guild.id,data,reason)

    async def channel_edit(self,channel,name=None,topic=None,nsfw=None,slowmode=None,user_limit=None,bitrate=None,type_=128,reason=None):
        if not isinstance(channel,ChannelGuildBase):
            raise ValueError(f'Only Guild channels can be edited with this method, got {channel!r}')
        
        data={}
        value=channel.type
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>100:
                raise ValueError(f'Invalid name length, can be between 2-100, got {name_ln}')
            data['name']=name
        
        if value in (0,5):
            if (topic is not None):
                topic_ln=len(topic)
                if topic_ln>1024:
                    raise ValueError(f'Invalid topic length can be between 0-1024, go {topic_ln}')
                data['topic']=topic
        
        if type_<128:
            INTERCHANGE=channel.INTERCHANGE
            if len(INTERCHANGE)==1:
                raise ValueError(f'You can not switch channel type of this channel type')
            if type_ not in INTERCHANGE:
                raise ValueError(f'You can switch chanel type from {value} to {type_}')
            if type_!=value:
                data['type']=type_
        
        if value in (0,5,6):
            if (nsfw is not None):
                data['nsfw']=nsfw
                
        if value==0:
            if slowmode is not None:
                if slowmode<0 or slowmode>21600:
                    raise ValueError(f'Invalid slowmode {slowmode}, should be 0-21600')
                data['rate_limit_per_user']=slowmode

        elif value==2:
            if bitrate<8000 or bitrate>channel.guild.bitrate_limit:
                raise ValueError(f'Invalid bitrate {bitrate!r}, should be 8000-96000. 128000 max for vip, or 128000, 256000, 384000 max depends on premium tier.')
            data['bitrate']=bitrate
            
            if user_limit is not None:
                if user_limit<0 or user_limit>99:
                    raise ValueError(f'Invalid user_limit {user_limit!r}, should be 0 for unlimited or 1-99')
                data['user_limit']=user_limit

        await self.http.channel_edit(channel.id,data,reason)

    async def channel_create(self,guild,category=None,*args,reason=None,**kwargs):
        data=cr_pg_channel_object(*args,**kwargs,bitrate_limit=guild.bitrate_limit)
        data['parent_id']=category.id if type(category) is ChannelCategory else None
        data = await self.http.channel_create(guild.id,data,reason)
        return CHANNEL_TYPES[data['type']](data,self,guild)

    async def channel_delete(self,channel,reason=None):
        await self.http.channel_delete(channel.id,reason)

    async def channel_follow(self,source_channel,target_channel):
        if source_channel.type!=5:
            raise ValueError(f'`source_channel` must be type 5, so news (announcements) channel, got `{source_channel}`')
        if target_channel.type not in ChannelText.INTERCHANGE:
            raise ValueError(f'`target_channel` must be type 0 or 5, so any guild text channel, got  `{target_channel}`')

        data = {
            'webhook_channel_id': target_channel.id,
                }

        data = await self.http.channel_follow(source_channel.id,data)
        webhook = await Webhook._from_follow_data(data,source_channel,target_channel,self)
        return webhook

    #messages

    #bots cant do this!
    async def message_mar(self,message):
        data={'token':self.mar_token}
        data = await self.http.message_mar(message.channel.id,message.id,data)
        self.mar_token=data['token']

    async def message_logs(self,channel,limit=100,after=None,around=None,before=None):
        if limit<1 or limit>100:
            raise ValueError(f'limit must be in <1,100>, got {limit}')
        
        data={'limit':limit}
        
        if (after is not None):
            data['after']=log_time_converter(after)
            
        if (around is not None):
            data['around']=log_time_converter(around)
            
        if (before is not None):
            data['before']=log_time_converter(before)
        
        data = await self.http.message_logs(channel.id,data)
        return channel._mc_process_chunk(data)

    #if u have 0-1-2 messages at a channel, and you wanna store the messages.
    #the other wont store it, because it wont see anything what allows channeling
    async def message_logs_fromzero(self,channel,limit=100):
        if limit<1 or limit>100:
            raise ValueError(f'limit must be in <1,100>, got {limit}')
        
        data={'limit':limit,'before':now_as_id()}
        data=await self.http.message_logs(channel.id,data)
        if data:
            Message.new(data[0],channel)
            return channel._mc_process_chunk(data)
        return []

    async def message_get(self,channel,message_id):
        data = await self.http.message_get(channel.id,message_id)
        return Message.onetime(data,channel)
    
    async def message_create(self,channel,content=None,embed=None,file=None,tts=False,nonce=None):
        data={}
        contains_content=False
        
        if (content is not None) and content:
            data['content']=content
            contains_content=True
        
        if (embed is not None):
            data['embed']=embed.to_data()
            contains_content=True
        
        if tts:
            data['tts']=True
        
        if (nonce is not None):
            data['nonce']=nonce

        if file is None:
            to_send=data
        else:
            to_send=self._create_file_form(data,file)
            if to_send is None:
                to_send=data
            else:
                contains_content=True
        
        if not contains_content:
            return None
        
        data = await self.http.message_create(channel.id,to_send)
        return Message.new(data,channel)
    
    @staticmethod
    def _create_file_form(data,file):
        form=Formdata()
        form.add_field('payload_json',to_json(data))
        files=[]

        #checking structure
        
        #case 1 dict like
        if hasattr(file,'items'):
            files.extend(file.items())
                
        #case 2 tuple => file, filename pair
        elif isinstance(file,tuple):
            files.append(file)
        
        #case 3 list like
        elif isinstance(file,(list,deque)):
            for element in file:
                if type(element) is tuple:
                    name,io=element
                else:
                    io=element
                    name=''
                
                if not name:
                    #guessing name
                    name=getattr(io,'name','')
                    if name:
                        _,name=splitpath(name)
                    else:
                        name=str(random_id())
                        
                files.append((name,io),)
        
        #case 4 file itself
        else:
            name=getattr(file,'name','')
            #guessing name
            if name:
                _,name=splitpath(name)
            else:
                name=str(random_id())
            
            files.append((name,file),)

        #checking the amount of files
        #case 1 one file
        if len(files)==1:
            name,io=files[0]
            form.add_field('file',io,filename=name,content_type='application/octet-stream')
        #case 2, no files -> return None, we should use the already existing data
        elif len(files)==0:
            return None
        #case 3 maximum 10 files
        elif len(files)<11:
            for index,(name,io) in enumerate(files):
                form.add_field(f'file{index}s',io,filename=name,content_type='application/octet-stream')
                
        #case 4 more than 10 files
        else:
            raise ValueError('You can send maximum 10 files at once.')
        
        return form

    async def message_delete(self,message,reason=None):
        if (message.author == self) or (message.id > int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22):
            # own or new
            await self.http.message_delete(message.channel.id,message.id,reason)
        else:
            await self.http.message_delete_b2wo(message.channel.id,message.id,reason)
        
    
    async def message_delete_multiple(self,messages,reason=None):
        if not messages:
            return
        
        channel=messages[0].channel
        channel_id=channel.id

        if not isinstance(channel,ChannelGuildBase):
            # Bulk delete is available only at guilds. At private or group
            # channel you can delete only yours tho.
            for message in messages:
                await self.http.message_delete(channel_id,message.id,reason)
                
            return
        
        message_group_new       = deque()
        message_group_old       = deque()
        message_group_old_own   = deque()
        
        bulk_delete_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks
        
        for message in messages:
            message_id=message.id
            own=(message.author==self)
            
            if message_id>bulk_delete_limit:
                message_group_new.append((own,message_id),)
                continue
            
            if own:
                group = message_group_old_own
            else:
                group = message_group_old
            
            group.append(message_id)
            continue
            
        loop = self.loop
        tasks = []
        
        delete_mass_task= None
        delete_new_task = None
        delete_old_task = None
        
        while True:
            if delete_mass_task is None:
                message_limit=len(message_group_new)
                
                # 0 is all good, but if it is more, lets check them
                if message_limit:
                    message_ids=[]
                    message_count=0
                    limit = int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks -10s
                    
                    while message_group_new:
                        own,message_id=message_group_new.popleft()
                        if message_id>limit:
                            message_ids.append(message_id)
                            message_count=message_count+1
                            if message_count==100:
                                break
                            continue
                        
                        if (message_id+20971520000) < limit:
                            continue
                        
                        # If the message is really older than the limit,
                        # with ingoring the 10 second, then we move it.
                        if own:
                            group = message_group_old_own
                        else:
                            group = message_group_old
                        
                        group.appendleft(message_id)
                        continue
                    
                    if message_count:
                        if message_count==1:
                            if (delete_new_task is None):
                                message_id=message_ids[0]
                                delete_new_task = Task(self.http.message_delete(channel_id,message_id,None),loop)
                                tasks.append(delete_new_task)
                        else:
                            delete_mass_task = Task(self.http.message_delete_multiple(channel_id,{'messages':message_ids},None),loop)
                            tasks.append(delete_mass_task)
                
            if delete_old_task is None:
                if message_group_old:
                    message_id=message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason),loop)
                    tasks.append(delete_old_task)
            
            if delete_new_task is None:
                if message_group_new:
                    group = message_group_new
                elif message_group_old_own:
                    group = message_group_old_own
                else:
                    group = None
                
                if (group is not None):
                    message_id=message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason),loop)
                    tasks.append(delete_new_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left,  at that case
                # we check if there is more message left. Only at
                # `message_group_new` can be anymore message, because there is a
                # time intervallum of 10 seconds, what we do not move between
                # categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own,message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make
                # Sure it will not block the other endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,None),loop)
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,None),loop)
                
                tasks.append(delete_old_task)
                
            done, pending = await WaitTillFirst(tasks,loop)
    
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except (DiscordException,ConnectionError):
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is delete_mass_task:
                    delete_mass_task=None
                    continue
                
                if task is delete_new_task:
                    delete_new_task=None
                    continue
                
                if task is delete_old_task:
                    delete_old_task=None
                    continue
                 
                # Should not happen
                continue

    #deletes from more channels
    async def message_delete_multiple2(self,messages,reason=None):
        delete_system={}
        for message in messages:
            channel_id=message.channel.id
            try:
                delete_system[channel_id].append(message)
            except KeyError:
                delete_system[channel_id]=[message]
        
        tasks = []
        loop = self.loop
        for messages in delete_system.values():
            task=Task(self.message_delete_multiple(messages,reason),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
        
        exceptions = []
        for task in tasks:
            exception=task.exception()
            if exception is None:
                continue
            
            exceptions.append(exceptions)
            if  __debug__:
                task.__silence__()
        
        if exceptions:
            return exceptions
        
    async def message_delete_sequence(self,channel,after=None,before=None,limit=None,filter=None,reason=None):
        # Check permissions
        permissions=channel.cached_permissions_for(self)
        if not permissions.can_manage_messages:
            return
        
        before  = 9223372036854775807 if before is None else log_time_converter(before)
        after   = 0 if after is None else log_time_converter(after)
        limit   = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before<after:
            return
        
        # Check if we are done already
        if limit<=0:
            return
        
        message_group_new       = deque()
        message_group_old       = deque()
        message_group_old_own   = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end or (not permissions.can_read_message_history):
            should_request=False
        else:
            should_request=True
        
        last_message_id = before
        
        messages_=channel.messages
        if messages_:
            before_index=message_relativeindex(messages_,before)
            after_index=message_relativeindex(messages_,after)
            if before_index!=after_index:
                time_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22
                while True:
                    if before_index==after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index=before_index+1
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id=message_.id
                    own = (message_.author==self)
                    if last_message_id > time_limit:
                        message_group_new.append((own,last_message_id,),)
                    else:
                        if own:
                            group=message_group_old_own
                        else:
                            group=message_group_old
                        group.append(last_message_id)
                    
                    # Check if we reached the limit
                    limit=limit-1
                    if limit:
                        continue
                    should_request=False
                    break
        
        tasks               = []
        
        get_mass_task       = None
        delete_mass_task    = None
        delete_new_task     = None
        delete_old_task     = None
        
        channel_id=channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                request_data = {
                    'limit' : 100,
                    'before': last_message_id,
                        }
                
                get_mass_task = Task(self.http.message_logs(channel_id,request_data),self.loop)
                tasks.append(get_mass_task)
            
            if (delete_mass_task is None):
                message_limit=len(message_group_new)
                # If there are more messages, we are waiting for other tasks
                if message_limit:
                    time_limit = int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks -10s
                    collected = 0
                    
                    while True:
                        if collected==message_limit:
                            break
                        
                        if collected==100:
                            break
                        
                        own,message_id=message_group_new[collected]
                        if message_id<time_limit:
                            break
                        
                        collected=collected+1
                        continue
                    
                    if collected==0:
                        pass
                    elif collected==1:
                        # Delete the message if we dont delete a new message already
                        if (delete_new_task is None):
                            # We collected 1 message -> We cannot use mass delete on this.
                            own,message_id=message_group_new.popleft()
                            delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason),self.loop)
                            tasks.append(delete_new_task)
                    else:
                        message_ids=[]
                        while collected:
                            collected = collected-1
                            own,message_id=message_group_new.popleft()
                            message_ids.append(message_id)
                        
                        delete_mass_task = Task(self.http.message_delete_multiple(channel_id,{'messages':message_ids},reason=reason),self.loop)
                        tasks.append(delete_mass_task)
                    
                    # After we checked what is at this group, lets move the others from it's end, if needed ofc
                    message_limit=len(message_group_new)
                    if message_limit:
                        # timelimit -> 2 week
                        time_limit = time_limit-20971520000
                        
                        while True:
                            # Cannot start at index = len(...), so we instantly do -1
                            message_limit = message_limit-1
                            
                            own, message_id = message_group_new[message_limit]
                            # Check if we should not move -> leave
                            if message_id>time_limit:
                                break
                            
                            del message_group_new[message_limit]
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                                
                            group.appendleft(message_id)
                            
                            if message_limit:
                                continue
                            
                            break
            
            if (delete_new_task is None):
                # Check old own messages only, mass delete speed is pretty good by itself.
                if message_group_old_own:
                    message_id=message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason),self.loop)
                    tasks.append(delete_new_task)
            
            if (delete_old_task is None):
                if message_group_old:
                    message_id=message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason=reason),self.loop)
                    tasks.append(delete_old_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left,  at that case
                # we check if there is more message left. Only at
                # `message_group_new` can be anymore message, because there is a
                # time intervallum of 10 seconds, what we do not move between
                # categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own,message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make
                # Sure it will not block the other endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason),self.loop)
                    task=delete_new_task
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason=reason),self.loop)
                    task=delete_old_task
                
                tasks.append(task)
            
            done, pending = await WaitTillFirst(tasks,self.loop)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except (DiscordException,ConnectionError):
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task=None
                    
                    received_count=len(result)
                    if received_count<100:
                        should_request=False
                        
                        # We got 0 messages, move on the next task
                        if received_count==0:
                            continue
                    
                    # We dont really care about the limit, because we check
                    # message id when we delete too.
                    time_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id=int(message_data['id'])
    
                            # Did we reach the after limit?
                            if last_message_id<after:
                                should_request=False
                                break
                            
                            # If filter is `None`, we just have to decide, if we
                            # were the author or nope.
                            
                            # Try to get user id, first start it with trying to get
                            # author data. The default author_id will be 0, because
                            # thats sure not the id of the client.
                            try:
                                author_data=message_data['author']
                            except KeyError:
                                author_id=0
                            else:
                                # If we have author data, lets select the user's data
                                # from it
                                try:
                                    user_data=author_data['user']
                                except KeyError:
                                    user_data=author_data
                                
                                try:
                                    author_id=user_data['id']
                                except KeyError:
                                    author_id=0
                                else:
                                    author_id=int(author_id)
                        else:
                            message_=Message.onetime(message_data,channel)
                            last_message_id=message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id<after:
                                should_request=False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id=message_.author.id
                        
                        own = (author_id == self.id)
                        
                        if last_message_id>time_limit:
                            message_group_new.append((own,last_message_id,),)
                        else:
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                            
                            group.append(last_message_id)
                        
                        # Did we reach the amount limit?
                        limit = limit-1
                        if limit:
                            continue
                        
                        should_request=False
                        break
                
                if task is delete_mass_task:
                    delete_mass_task=None
                    continue
                
                if task is delete_new_task:
                    delete_new_task=None
                    continue
                
                if task is delete_old_task:
                    delete_old_task=None
                    continue
                 
                # Should not happen
                continue
    
    async def message_edit(self,message,content=None,embed=_spaceholder,suppress=None):
        data={}
        if (content is not None):
            data['content']=content
        
        if (embed is not _spaceholder):
            if embed is None:
                embed_data=None
            else:
                embed_data=embed.to_data()
            
            data['embed']=embed_data
        
        if (suppress is not None):
            if suppress:
                flags=message.flags|0b00000100
            else:
                flags=message.flags&0b11111011
            data['flags']=flags
            
        await self.http.message_edit(message.channel.id,message.id,data)

    async def message_suppress_embeds(self,message,suppress=True):
        await self.http.message_suppress_embeds(message.channel.id,message.id,{'suppress':suppress})

    async def message_pin(self,message):
        await self.http.message_pin(message.channel.id,message.id)

    async def message_unpin(self,message):
        await self.http.message_unpin(message.channel.id,message.id)

    async def channel_pins(self,channel):
        data= await self.http.channel_pins(channel.id)
        return [Message.fromchannel(message_data,channel) for message_data in data]


    message_at_index=message_at_index
    messages_till_index=messages_till_index
    def message_iterator(self,channel,chunksize=97):
        return MessageIterator(self,channel,chunksize)

    async def typing(self,channel):
        await self.http.typing(channel.id)

    #with context
    def keep_typing(self,channel,timeout=300.):
        return Typer(self,channel,timeout)

    #reactions:

    async def reaction_add(self,message,emoji):
        await self.http.reaction_add(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_delete(self,message,emoji,user):
        if self==user:
            await self.http.reaction_delete_own(message.channel.id,message.id,emoji.as_reaction)
        else:
            await self.http.reaction_delete(message.channel.id,message.id,emoji.as_reaction,user.id)

    async def reaction_delete_emoji(self,message,emoji):
        await self.http.reaction_delete_emoji(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_delete_own(self,message,emoji):
        await self.http.reaction_delete_own(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_clear(self,message):
        await self.http.reaction_clear(message.channel.id,message.id)
    
    # before is not supported
    
    async def reaction_users(self,message,emoji,limit=None,after=None):
        try:
            line=message.reactions[emoji]
        except KeyError:
            return []
        
        if line.unknown:
            data={}
            if (limit is not None):
                if type(limit) is not int:
                    raise TypeError(f'`limit` can be `None` or type `int`, got `{limit!r}`')
                
                if limit<1 or limit>100:
                    raise ValueError(f'`limit` can be between 1-100, got `{limit!r}`')
                
                data['limit']=limit
            
            if (after is not None):
                data['after']=log_time_converter(after)
            #
            #if (before is not None):
            #    data['before']=log_time_converter(before)
                
            data = await self.http.reaction_users(message.channel.id,message.id,emoji.as_reaction,data)
            
            users=[User(user_data) for user_data in data]
            message.reactions._update_some_users(emoji,users)
            
        else:
            #if we know every reacters:
            if limit is None:
                limit=100
            elif type(limit) is not int:
                raise TypeError(f'`limit` can be `None` or type `int`, got `{limit!r}`')
            elif limit<1 or limit>100:
                raise ValueError(f'`limit` can be between 1-100, got `{limit!r}`')
            
            #before = 9223372036854775807 if before is None else log_time_converter(before)
            after = 0 if after is None else log_time_converter(after)
            users=line.filter_after(limit,after)
            
        return users
    
    async def reaction_users_all(self,message,emoji):
        if not message.reactions:
            return []
        
        try:
            line=message.reactions[emoji]
        except KeyError:
            return []
        
        if line.unknown:
            limit=len(line)
            data={'limit':100,'after':0}
            users=[]
            reaction=emoji.as_reaction
            
            while limit>0:
                user_datas = await self.http.reaction_users(message.channel.id,message.id,reaction,data)
                users.extend(User(user_data) for user_data in user_datas)

                data['after']=users[-1].id
                limit-=100
                
            message.reactions._update_all_users(emoji,users)
        else:
            #we copy
            users=list(line)
            
        return users

    async def reaction_load_all(self,message):
        if not message.reactions:
            return
        
        users=[]
        data={'limit':100,'after':0}
        for emoji,line in message.reactions.items():
            if not line.unknown:
                continue
            
            reaction=emoji.as_reaction
            data['after']=0
            limit=len(line)
            while limit>0:
                
                user_datas = await self.http.reaction_users(message.channel.id,message.id,reaction,data)
                users.extend(User(user_data) for user_data in user_datas)
                
                data['after']=users[-1].id
                limit-=100

            message.reactions._update_all_users(emoji,users)
            users.clear()
    
    # Guild

    async def guild_user_delete(self,guild,user,reason=None):
        await self.http.guild_user_delete(guild.id,user.id,reason)

    async def guild_ban_add(self,guild,user,delete_message_days=0,reason=None):
        data={}
        if delete_message_days:
            if delete_message_days<1 or delete_message_days>7:
                raise ValueError('delete_message_days can be between 0-7')
            data['delete-message-days']=delete_message_days
        await self.http.guild_ban_add(guild.id,user.id,data,reason)

    async def guild_ban_delete(self,guild,user,reason=None):
        await self.http.guild_ban_delete(guild.id,user.id,reason)

    async def guild_sync(self,guild_id):
        #sadly guild_get does not returns channel and voice state data
        #at least we can request the channels
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            data = await self.http.guild_get(guild_id)
            channel_data = await self.http.guild_channels(guild_id)
            data['channels']=channel_data
            user_data = await self.http.guild_user_get(guild_id,self.id)
            data['members']=[user_data]
            guild=Guild(data,self)
        else:
            data = await self.http.guild_get(guild_id)
            guild._sync(data,self)
            channel_data = await self.http.guild_channels(guild_id)
            guild._sync_channels(channel_data)
        
            user_data = await self.http.guild_user_get(guild_id,self.id)
            try:
                profile=self.guild_profiles[guild]
            except KeyError:
                self.guild_profiles[guild]=GuildProfile(user_data,guild)
                if guild not in guild.clients:
                    guild.clients.append(self)
            else:
                profile._update_no_return(user_data,guild)
        
        return guild

##    # Disable user syncing, takes too much time
##    async def _guild_sync_postprocess(self,guild):
##        for client in CLIENTS:
##            try:
##                user_data = await self.http.guild_user_get(guild.id,client.id)
##           except (DiscordException, ConnectionError):
##                continue
##            try:
##                profile=client.guild_profiles[guild]
##            except KeyError:
##                client.guild_profiles[guild]=GuildProfile(user_data,guild)
##                if client not in guild.clients:
##                    guild.clients.append(client)
##            else:
##                profile._update_no_return(user_data,guild)
##
##        if not CACHE_USER:
##            return
##
##        old_ids=set(guild.users)
##        data={'limit':1000,'after':'0'}
##        while True:
##            user_datas = await self.http.guild_users(guild.id,data)
##            for user_data in user_datas:
##                user=User._create_and_update(user_data,guild)
##                try:
##                    old_ids.remove(user.id)
##                except KeyError:
##                    pass
##             if len(user_datas)<1000:
##                 break
##             data['after']=user_datas[999]['user']['id']
##        del data
##
##        for id_ in old_ids:
##            try:
##               user=guild.users.pop(id_)
##           except KeyError:
##               continue #huh?
##           try:
##               del user.guild_profiles[guild]
##           except KeyError:
##               pass #huh??

    #user account only
    async def guild_mar(self,guild):
        data= await self.http.guild_mar(guild.id,{'token':self.mar_token})
        self.mar_token=data['token']

    async def guild_leave(self,guild):
        await self.http.guild_leave(guild.id)

    async def guild_delete(self,guild):
        await self.http.guild_delete(guild.id)

    async def guild_create(self         , name                                  ,
            icon                        = None                                  ,
            roles                       = []                                    ,
            channels                    = []                                    ,
            afk_channel_id              = None                                  ,
            system_channel_id           = None                                  ,
            afk_timeout                 = None                                  ,
            region                      = VoiceRegion.eu_central                ,
            verification_level          = VerificationLevel.medium              ,
            message_notification_level  = MessageNotificationLevel.only_mentions,
            content_filter_level        = ContentFilterLevel.disabled           ,
                ):
        
        if len(self.guild_profiles)>(99,9)[self.is_bot]:
            if self.is_bot:
                message='Bots cannot create a new server if they have 10 or more.'
            else:
                message='Hooman cannot have more than 100 guilds.'
            raise ValueError(message)
        
        name_ln=len(name)
        if name_ln<2 or name_ln>100:
            raise ValueError(f'Guild\'s name\'s length can be between 2-100, got {name_ln}')
        
        data = {
            'name'                          : name,
            'icon'                          : None if icon is None else bytes_to_base64(icon),
            'region'                        : region.id,
            'verification_level'            : verification_level.value,
            'default_message_notifications' : message_notification_level.value,
            'explicit_content_filter'       : content_filter_level.value,
            'roles'                         : roles,
            'channels'                      : channels,
                }
        
        if (afk_channel_id is not None):
            data['afk_channel_id'] = afk_channel_id
        
        if (system_channel_id is not None):
            data['system_channel_id'] = system_channel_id
        
        if (afk_timeout is not None):
            if afk_timeout not in (60,300,900,1800,3600):
                raise ValueError(f'Afk timeout should be 60, 300, 900, 1800, 3600 seconds!, got `{afk_timeout!r}`')
            data['afk_timeout']=afk_timeout
        
        data = await self.http.guild_create(data)
        #we can create only partial, because the guild data is not completed usually
        return PartialGuild(data)
    
    #kicks inactive users
    async def guild_prune(self,guild,days,count=False,reason=None):
        if count and guild.is_large:
            count=False
        data= {
            'days'                  : days,
            'compute_prune_count'   : count,
                }
        data = await self.http.guild_prune(guild.id,data,reason)
        return data['pruned']

    async def guild_prune_estimate(self,guild,days):
        data = await self.http.guild_prune_estimate(guild.id,{'days':days})
        return data['pruned']

    # splash is only available for guilds with INVITE_SPLASH feature.
    # banner is only available for guilds with BANNER feature.
    # rules_channel is available only for guilds with DISCOVERABLE feature?
    async def guild_edit(self, guild, name=None, icon=_spaceholder,
            splash=_spaceholder, discovery_splash=_spaceholder,
            banner=_spaceholder, afk_channel=_spaceholder,
            system_channel=_spaceholder, rules_channel=_spaceholder,
            public_updates_channel=_spaceholder, owner=None,region=None,
            afk_timeout=None, verification_level=None, content_filter=None,
            message_notification=None, description=None,
            system_channel_flags=None, reason=None):

        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>100:
                raise ValueError(f'Guild\'s name\'s length can be between 2-100, got {name_ln}')
            data['name']=name
        
        if (icon is not _spaceholder):
            if icon is None:
                data['icon']=None
            else:
                icon_data=bytes_to_base64(icon)
                ext=ext_from_base64(icon_data)
                if ext not in (VALID_ICON_FORMATS_EXTENDED if (GuildFeature.animated_icon in guild.features) else VALID_ICON_FORMATS):
                    raise ValueError(f'Invalid icon type: {ext}')
                data['icon']=icon_data
        
        if (banner is not _spaceholder):
            if GuildFeature.banner not in guild.features:
                raise ValueError('The guild has no `BANNER` feature')
            
            if banner is None:
                 data['banner']=None
            else:
                banner_data=bytes_to_base64(banner)
                ext=ext_from_base64(banner_data)
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid banner type: {ext}')
                data['banner']=banner_data
        
        if (splash is not _spaceholder):
            if GuildFeature.splash not in guild.features:
                raise ValueError('The guild has no `SPLASH` feature')
            if splash is None:
                 data['splash']=None
            else:
                splash_data=bytes_to_base64(splash)
                ext=ext_from_base64(splash_data)
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid splash type: {ext!r}')
                data['splash']=splash_data
        
        if (discovery_splash is not _spaceholder):
            if GuildFeature.discoverable not in guild.features:
                raise ValueError('The guild has no `DISCOVERABLE` feature')
            
            if discovery_splash is None:
                 data['discovery_splash']=None
            else:
                discovery_splash_data=bytes_to_base64(banner)
                ext=ext_from_base64(discovery_splash_data)
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid discovery_splash type: {ext}')
                data['discovery_splash']=discovery_splash_data
        
        if (afk_channel is not _spaceholder):
            data['afk_channel_id']=None if afk_channel is None else afk_channel.id
        
        if (system_channel is not _spaceholder):
            data['system_channel_id']=None if system_channel is None else system_channel.id
        
        if (rules_channel is not _spaceholder):
            if GuildFeature.discoverable not in guild.features:
                raise ValueError('The guild has no `DISCOVERABLE` feature')
            data['rules_channel_id']=None if rules_channel is None else rules_channel.id
        
        if (public_updates_channel is not _spaceholder):
            if GuildFeature.discoverable not in guild.features:
                raise ValueError('The guild has no `DISCOVERABLE` feature')
            data['public_updates_channel_id']=None if public_updates_channel is None else public_updates_channel.id
        
        if (owner is not None):
            if (guild.owner!=self):
                raise ValueError('You must be owner to transfer ownership')
            data['owner_id']=owner.id
        
        if (region is not None):
            data['region']=region.id
        
        if afk_timeout is not None:
            if afk_timeout not in (60,300,900,1800,3600):
                raise ValueError(f'Afk timeout should be 60, 300, 900, 1800, 3600  seconds, got `{afk_timeout!r}`')
            data['afk_timeout']=afk_timeout
        
        if (verification_level is not None):
            data['verification_level']=verification_level.value
        
        if (content_filter is not None):
            data['explicit_content_filter']=content_filter.value

        if (message_notification is not None):
            data['default_message_notifications']=message_notification.value

        if (description is not None):
            data['description']=description if description else None

        if (system_channel_flags is not None):
            data['system_channel_flags']=system_channel_flags
        
        await self.http.guild_edit(guild.id,data,reason)

    async def guild_bans(self,guild):
        data=await self.http.guild_bans(guild.id)
        return [(User(ban_data['user']),ban_data.get('reason',None)) for ban_data in data]

    async def guild_ban_get(self,guild,user_id):
        data = await self.http.guild_ban_get(guild.id,user_id)
        return User(data['user']),data.get('reason',None)
    
    async def guild_embed_get(self,guild):
        data = await self.http.guild_embed_get(guild.id)
        return GuildEmbed(data,guild)
    
    async def guild_embed_edit(self,guild,enabled=None,channel=_spaceholder):
        data={}
        if enabled is not None:
            data['enabled']=enabled
        if channel is not _spaceholder:
            if channel is None:
                data['channel_id']=None
            else:
                data['channel_id']=channel.id
        
        await self.http.guild_embed_edit(guild.id,data)

    async def guild_widget_get(self,guild_or_id):
        if type(guild_or_id) is Guild:
            guild_id=guild_or_id.id
        elif type(guild_or_id) is int:
            guild_id=guild_or_id
        else:
            raise TypeError(f'Excepted `{Guild.__name__}` or `int` (id), got `{guild_or_id!r}`')
        
        try:
            data = await self.http.guild_widget_get(guild_id)
        except DiscordException as err:
            if err.response.status==403: #Widget Disabled -> return None
                return
            raise
        
        return GuildWidget(data)
        
    async def guild_users(self,guild):
        data={'limit':1000,'after':'0'}
        result=[]
        while True:
            user_datas = await self.http.guild_users(guild.id,data)
            for user_data in user_datas:
                user=User(user_data,guild)
                result.append(user)
            if len(user_datas)<1000:
                break
            data['after']=user_datas[999]['user']['id']
        return result

    async def guild_get_all(self):
        #a non bot can join only 100 guilds
        if self.is_bot:
            result=[]
            params={'after':0}
            while True:
                data = await self.http.guild_get_all(params)
                result.extend(PartialGuild(guild_data) for guild_data in data)
                if len(data)<100:
                    break
                params['after']=result[-1].id

        else:
            data = await self.http.guild_get_all({})
            result=[PartialGuild(guild_data) for guild_data in data]
            
        return result

    async def guild_regions(self,guild):
        data = await self.http.guild_regions(guild.id)
        results=[]
        optimals=[]
        for voice_region_data in data:
            region=VoiceRegion.from_data(voice_region_data)
            results.append(region)
            if voice_region_data['optimal']:
                optimals.append(region)
        return results,optimals

    async def guild_sync_channels(self,guild):
        data = await self.http.guild_channels(guild.id)
        guild._sync_channels(data,self)

    async def guild_sync_roles(self,guild):
        data = await self.http.guild_roles(guild.id)
        guild._sync_roles(data)
    
    async def audit_logs(self,guild,limit=100,before=None,after=None,user=None,event=None,):
        if limit<1 or limit>100:
            raise ValueError(f'Limit can be in <1,100>, got {limit}')
        
        data={'limit':limit}
        
        if (before is not None):
            data['before']=log_time_converter(before)
            
        if (after is not None):
            data['after']=log_time_converter(after)
            
        if (user is not None):
            data['user_id']=user.id
        
        if (event is not None):
            data['action_type']=event.value

        data = await self.http.audit_logs(guild.id,data)
        return AuditLog(data,guild)
    
    def audit_log_iterator(self, guild, user=None, event=None):
        return AuditLogIterator(self, guild, user=user, event=event)

    #users

    async def user_edit(self,guild,user,nick=_spaceholder,deaf=None,mute=None,voice_channel=_spaceholder,roles=None,reason=None):
        data={}
        if (nick is not _spaceholder):
            if (nick is not None):
                nick_ln=len(nick)
                if nick_ln>32:
                    raise ValueError(f'The length of the nick can be between 1-32, got {nick_ln}')
                if nick_ln==0:
                    nick=None
            
            should_edit_nick=False
            try:
                actual_nick=user.guild_profiles[guild].nick
            except KeyError:
                # user cache disabled, or the user is not at the guild -> will raise later
                should_edit_nick=True
            else:
                if (nick is None):
                    if (actual_nick is None):
                        should_edit_nick=False
                    else:
                        should_edit_nick=True
                else:
                    if (actual_nick is None):
                        should_edit_nick=True
                    elif actual_nick==nick:
                        should_edit_nick=False
                    else:
                        should_edit_nick=True
            
            if should_edit_nick:
                if self==user:
                    await self.http.client_edit_nick(guild.id,{'nick':nick},reason)
                else:
                    data['nick']=nick
                    
        if (deaf is not None):
            data['deaf']=deaf
            
        if (mute is not None):
            data['mute']=mute
            
        if (voice_channel is not _spaceholder):
            data['channel_id']=None if voice_channel is None else voice_channel.id
            
        if (roles is not None):
            data['roles']=[role.id for role in roles]
            
        await self.http.user_edit(guild.id,user.id,data,reason)

    async def user_role_add(self,user,role,reason=None):
        await self.http.user_role_add(role.guild.id,user.id,role.id,reason)

    async def user_role_delete(self,user,role,reason=None):
        await self.http.user_role_delete(role.guild.id,user.id,role.id,reason)

    async def user_voice_move(self,user,voice_channel):
       await self.http.user_move(voice_channel.guild.id,user.id,{'channel_id':voice_channel.id})

    async def user_voice_kick(self,user,guild):
        await self.http.user_move(guild.id,user.id,{'channel_id':None})
    
    async def user_get(self,user_id):
        data = await self.http.user_get(user_id)
        return User._create_and_update(data)

    async def guild_user_get(self,guild,user_id):
        data = await self.http.guild_user_get(guild.id,user_id)
        return User._create_and_update(data,guild)
        
    #user only, the returned data is unknown actually, propably needs compuser type
    async def user_profile(self,user_id):
        data = await self.http.user_profile(user_id)
        return User._create_and_update(data)
    
    #integrations
    
    #TODO: decide if we should store integrations at Guild objects
    async def integration_get_all(self,guild):
        data = await self.http.integration_get_all(guild.id)
        return [Integration(integration_data) for integration_data in data]

    #TODO: what is integration id?
    async def integration_create(self,guild,integration_id,type_):
        data = {
            'id'    : integration_id,
            'type'  : type_,
                }
        data = await self.http.integration_create(guild.id,data)
        return Integration(data)

    async def integration_edit(self,integration,expire_behavior=None,expire_grace_period=None,enable_emojis=True):

        if expire_behavior is None:
            expire_behavior=integration.expire_behavior
        elif expire_behavior not in (0,1):
            raise ValueError(f'\`expire_behavior\` should be 0 for kick, 1 for remove role, got {expire_behavior!r}')
        if expire_grace_period is None:
            expire_grace_period=integration.expire_grace_period
        elif expire_grace_period not in (1,3,7,14,30):
            raise ValueError(f'\'expire_grace_period\' should be 1, 3, 7, 14, 30, got {expire_grace_period!r}')
                
        data = {
            'expire_behavior'       : expire_behavior,
            'expire_grace_period'   : expire_grace_period,
                }
        
        if integration.type=='twitch' and (enable_emojis is not None):
            if type(enable_emojis) is not bool:
                raise ValueError('\'enable_emojis\' should be True or False, got {enable_emojis!r}')
            data['enable_emoticons']=enable_emojis
        
        await self.http.integration_edit(integration.role.guild.id,integration.id,data)

    async def integration_delete(self,integration):
        await self.http.integration_delete(integration.role.guild.id,integration.id)

    async def integration_sync(self,integration):
        await self.http.integration_sync(integration.role.guild.id,integration.id)

    async def permission_ow_edit(self,channel,overwrite,allow,deny,reason=None):
        data = {
            'allow' : allow,
            'deny'  : deny,
            'type'  : overwrite.type
                }
        await self.http.permission_ow_create(channel.id,overwrite.id,data,reason)

    async def permission_ow_delete(self,channel,overwrite,reason=None):
        await self.http.permission_ow_delete(channel.id,overwrite.id,reason)

    async def permission_ow_create(self,channel,target,allow,deny,reason=None):
        if type(target) is Role:
            type_='role'
        elif type(target) in (User,Client,UserOA2):
            type_='member'
        else:
            raise TypeError(f'Target expected to be Role or User type, got {type(target)!r}')
        data = {
            'target': target.id,
            'allow' : allow,
            'deny'  : deny,
            'type'  : type_,
                }
        await self.http.permission_ow_create(channel.id,target.id,data,reason)

        
    # Webhook management

    async def webhook_create(self,channel,name,avatar=None):
        name_ln=len(name)
        if name_ln==0 or name_ln>80:
            raise ValueError(f'Name length can be between 1-80, got {name_ln}')
        
        data={'name':name}
        
        if (avatar is not None):
            data['avatar']=bytes_to_base64(avatar)

        data = await self.http.webhook_create(channel.id,data)
        return Webhook(data)

    async def webhook_get(self,webhook_id):
        try:
            webhook=USERS[webhook_id]
            channel=webhook.channel
            if channel is not None and channel.guild.webhooks_uptodate:
                return webhook            
        except KeyError:
            data = await self.http.webhook_get(webhook_id)
            return Webhook(data)
        else:
            data = await self.http.webhook_get(webhook_id)
            webhook._update_no_return(data)
            return webhook

    async def webhook_get_token(self,webhook_id,webhook_token):
        try:
            webhook=USERS[webhook_id]
            if webhook.channel.guild.webhooks_uptodate:
                return webhook
        except KeyError:
            webhook = PartialWebhook(webhook_id,webhook_token)
            
        data = await self.http.webhook_get_token(webhook)
        webhook._update_no_return(data)
        
        return webhook

    async def webhook_update(self,webhook):
        data = await self.http.webhook_get(webhook.id)
        webhook._update_no_return(data)

    async def webhook_update_token(self,webhook):
        data = await self.http.webhook_get_token(webhook)
        webhook._update_no_return(data)
        
    async def webhook_get_channel(self,channel):
        if channel.guild.webhooks_uptodate:
            return [webhook for webhook in channel.guild.webhooks.values() if webhook.channel is channel]
        
        data = await self.http.webhook_get_channel(channel.id)
        return [Webhook(data) for data in data]
    
    async def webhook_get_guild(self,guild):
        if guild.webhooks_uptodate:
            return list(guild.webhooks.values())
        
        old_ids=list(guild.webhooks)
        
        result=[]

        data=await self.http.webhook_get_guild(guild.id)
        for webhook_data in data:
            webhook=Webhook(webhook_data)
            result.append(webhook)
            try:
                old_ids.remove(webhook.id)
            except ValueError:
                pass
            
        if old_ids:
            for id_ in old_ids:
                guild.webhooks[id_]._delete()

        guild.webhooks_uptodate=True
        
        return result
        
    async def webhook_delete(self,webhook):
        await self.http.webhook_delete(webhook.id)

    async def webhook_delete_token(self,webhook):
        await self.http.webhook_delete_token(webhook)
            
    #later there gonna be more stuff thats why 2 different
    async def webhook_edit(self,webhook,name=None,avatar=_spaceholder,channel=None):
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln==0 or name_ln>80:
                raise ValueError(f'The length of the name can be between 1-80, got {name_ln}')
            
            data['name']=name
        
        if (avatar is _spaceholder):
            pass
        elif (avatar is None):
            data['avatar']=None
        else:
            data['avatar']=bytes_to_base64(avatar)

        if (channel is not None):
            data['channel_id']=channel.id
            
        if not data:
            return #save 1 request
        
        data = await self.http.webhook_edit(webhook.id,data)
        webhook._update_no_return(data)
        
    async def webhook_edit_token(self,webhook,name=None,avatar=_spaceholder): #channel is ignored!
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln==0 or name_ln>80:
                raise ValueError(f'The length of the name can be between 1-80, got {name_ln}')
            
            data['name']=name
        
        if (avatar is _spaceholder):
            pass
        elif (avatar is None):
            data['avatar']=None
        else:
            data['avatar']=bytes_to_base64(avatar)
        
        if not data:
            return #save 1 request
        
        data = await self.http.webhook_edit_token(webhook,data)
        webhook._update_no_return(data)
   
    async def webhook_send(self,webhook,content=None,embed=None,file=None,tts=False,name=None,avatar_url=None,wait=False):
        data={}
        contains_content=False
        
        if (embed is not None):
            if isinstance(embed,(tuple,list,deque)):
                embed_amount=len(embed)
                if embed_amount>10:
                    raise ValueError(f'There can be only 10 embed maximum, got {embed_amount}.')
                
                if embed_amount!=0:
                    data['embeds']=[embed.to_data() for embed in embed]
                    contains_content=True
            else:
                #check case, when it is not embed like
                converter=getattr(type(embed),'to_data')
                if converter is None:
                    raise TypeError(f'Expected Embed like, tuple, list or deque for embed, got `{embed!r}`')
                
                data['embeds']=[converter(embed)]
                contains_content=True
                
        if (content is not None) and content:
            data['content']=content
            contains_content=True

        if tts:
            data['tts']=True
        
        if (avatar_url is not None):
            data['avatar_url']=avatar_url
            
        if (name is not None):
            name_ln=len(name)
            if name_ln>32:
                raise ValueError(f'The length of the name can be between 1-32, got {name_ln}')
            if name_ln!=0:
                data['username']=name

        if file is None:
            to_send=data
        else:
            to_send=self._create_file_form(data,file)
            if to_send is None:
                to_send=data
            else:
                contains_content=True
        
        if not contains_content:
            return None
        
        data = await self.http.webhook_send(webhook,to_send,wait)
        
        if wait:
            channel=webhook.channel
            if channel is None:
                channel=ChannelText.precreate(int(data['channel_id']))
            return Message.new(data,channel)
        
    async def emoji_get(self,guild,emoji_id):
        data = await self.http.emoji_get(guild.id,emoji_id)
        return Emoji(data,guild)

    async def guild_sync_emojis(self,guild):
        data = await self.http.guild_emojis(guild.id)
        guild._sync_emojis(data)

    async def emoji_create(self,guild,name,image,roles=[],reason=None):
        image=bytes_to_base64(image)
        name=''.join(_VALID_NAME_CHARS.findall(name))
        
        name_ln=len(name)
        if name_ln<2 or name_ln>32:
            raise ValueError(f'The length of the name can be between 2-32, got {name_ln}')
        
        data={
            'name'      : name,
            'image'     : image,
            'role_ids'  : [role.id for role in roles]
                }

        await self.http.emoji_create(guild.id,data,reason)

    async def emoji_delete(self,emoji,reason=None):
        await self.http.emoji_delete(emoji.guild.id,emoji.id,reason=reason)

    async def emoji_edit(self,emoji,name=None,roles=None,reason=None):
        data={}
        
        # name is required
        if (name is None):
            data['name']=emoji.name
        else:
            name=''.join(_VALID_NAME_CHARS.findall(name))
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The length of the name can be between 2-32, got {name_ln}')
            
            data['name']=name
        
        # roles are not required
        if (roles is not None):
            data['roles']=[role.id for role in roles]
        
        await self.http.emoji_edit(emoji.guild.id,emoji.id,data,reason)
        
    # Invite management
        
    async def vanity_invite(self,guild):
        vanity_code=guild.vanity_code
        if not vanity_code:
            return None
        
        data = await self.http.invite_get(vanity_code,{})
        return Invite._create_vanity(guild,data)

    async def vanity_edit(self,guild,code,reason=None):
        await self.http.vanity_edit(guild.id,{code:'code'},reason)
        
    async def invite_create(self,channel,max_age=0,max_uses=0,unique=True,temporary=False):
        if channel.type in (1,4):
            raise ValueError(f'Cannot create invite from {channel.__class__.__name__}')

        data = {
            'max_age'   : max_age,
            'max_uses'  : max_uses,
            'temporary' : temporary,
            'unique'    : unique,
                }
        data = await self.http.invite_create(channel.id,data)
        return Invite(data)

    # 'target_user_id' :
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_type', as 0:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.BASE_TYPE_CHOICES('Value must be one of (1,).')
    # 'target_user_type', as 1:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_id' and 'target_user_type' together:
    #    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    # 'target_user_id' and 'target_user_type' with not correct channel:
    #    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    
    async def stream_invite_create(self,guild,user,max_age=0,max_uses=0,unique=True,temporary=False):
        user_id=user.id
        try:
            voice_state=guild.voice_states[user_id]
        except ValueError:
            raise ValueError('The user must stream at a voice channel of the guild!') from None

        if not voice_state.self_video:
            raise ValueError('The user must stream at a voice channel of the guild!')

        data = {
            'max_age'           : max_age,
            'max_uses'          : max_uses,
            'temporary'         : temporary,
            'unique'            : unique,
            'target_user_id'    : user_id,
            'target_user_type'  : 1,
                }

        data = await self.http.invite_create(voice_state.channel.id,data)
        return Invite(data)

    #u cannot create invite from guild, but this chooses a prefered channel
    async def invite_create_pref(self,guild,*args,**kwargs):
        while True:
            if not guild.channels:
                raise ValueError('The guild has no channels (yet?), try waiting for dispatch or create a channel')

            channel=guild.system_channel
            if channel is not None:
                break
            
            channel=guild.embed_channel
            if channel is not None:
                break
            
            channel=guild.widget_channel
            if channel is not None:
                break
            
            for channel_type in (0,2):
                for channel in guild.channels:
                    if channel.type==4:
                        for channel in channel.channels:
                            if channel.type==channel_type:
                                break
                    if channel.type==channel_type:
                        break
                if channel.type==channel_type:
                    break
            else:
                raise ValueError('The guild has only category channels and cannot create invite from them!')
            break
        
        # Check permission, because it can save a lot of time >.>
        if not channel.cached_permissions_for(self).can_create_instant_invite:
            return None
        
        try:
            return (await self.invite_create(channel,*args,**kwargs))
        except DiscordException as err:
            if err.code in (10003, 50013):
                # 10003 -> unknown channel -> the channel was deleted meanwhile
                # 50013 -> missing permissions -> permissons changed meanwhile
                return None
            raise

    async def invite_get(self,invite_code,with_count=True):
        data = await self.http.invite_get(invite_code,{'with_counts':with_count})
        return Invite(data)
    
    async def invite_update(self,invite,with_count=True):
        data = await self.http.invite_get(invite.code,{'with_counts':with_count})
        invite._update_no_return(data)

    async def invite_get_guild(self,guild):
        data=await self.http.invite_get_guild(guild.id)
        return [Invite(invite_data) for invite_data in data]

    async def invite_get_channel(self,channel):
        data = await self.http.invite_get_channel(channel.id)
        return [Invite(invite_data) for invite_data in data]

    async def invite_delete(self,invite,reason=None):
        await self.http.invite_delete(invite.code,reason)

    async def invite_delete_by_code(self,invite_code,reason=None):
        data = await self.http.invite_delete(invite_code,reason)
        return Invite(data)
    
    # Role management

    async def role_edit(self,role,name=None,color=None,separated=None,
            mentionable=None,permissions=None,position=0,reason=None):

        if position:
            await self.role_move(role,position,reason)

        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The name of the role can be between 2-32, got {name_ln}')
            data['name']=name
        
        if color is not None:
            data['color']=color
            
        if separated is not None:
            data['hoist']=separated

        if mentionable is not None:
            data['mentionable']=mentionable

        if permissions is not None:
            data['permissions']=permissions

        if data:
            await self.http.role_edit(role.guild.id,role.id,data,reason)

    async def role_delete(self,role,reason=None):
        await self.http.role_delete(role.guild.id,role.id,reason)

    async def role_create(self,guild,name=None,permissions=None,color=None,
            separated=None,mentionable=None,reason=None):
        
        data={}
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The name\'s length of the role can be between 2-32, got {name_ln}')
            data['name']=name
            
        if (permissions is not None):
            data['permissions']=permissions
            
        if (color is not None):
            data['color']=color
            
        if (separated is not None):
            data['hoist']=separated
            
        if (mentionable is not None):
            data['mentionable']=mentionable
            
        data = await self.http.role_create(guild.id,data,reason)
        return Role(data,guild)

    async def role_move(self,role,position,reason=None):
        guild=role.guild
        if guild is None:
            # The role is partial, we cannot move it, because there is nowhere to move it >.>
            return
        
        # Is there nothing to move?
        if role.position==position:
            return
        
        # Default role cannot be moved to position not 0
        if role.position==0:
            if position!=0:
                raise ValueError(f'Default role cannot be moved: `{role!r}`')
        # non default role cannot be moved to position 0
        else:
            if position==0:
                raise ValueError(f'Role cannot be moved to position `0`')
        
        data=guild.roles.change_on_switch(role,position,key=lambda role,pos:{'id':role.id,'position':pos})
        if not data:
            return
        
        await self.http.role_move(guild.id,data,reason)
    
    async def role_reorder(self,roles,reason=None):
        # Nothing to move, nice
        if not roles:
            return
        
        # Lets check `roles` structure
        roles_valid=[]
        
        # Is `roles` passed as dictlike?
        if hasattr(type(roles),'items'):
            for item in roles.items():
                if type(item) is not tuple:
                    raise TypeError(f'`roles` passed as dictlike, but when iterating it\'s `.items` returned not a `tuple`, got `{item!r}`')
                
                if len(item)!=2:
                    raise TypeError(f'`roles` passed as dictlike, but when iterating it\'s `.items` returned a `tuple`, but not with length `2`, got `{item!r}`')
                
                if (type(item[0]) is not Role) or (type(item[1]) is not int):
                    raise TypeError(f'Items should be `{Role.__name__}`, `int` pairs, but got `{item!r}`')
                
                roles_valid.append(item)
        
        # Is `roles` passed as other iterable
        elif hasattr(type(roles),'__iter__'):
            for item in roles:
                if type(item) is not tuple:
                    raise TypeError(f'`roles` passed as other iterable, but when iterating returned not a `tuple`, got `{item!r}`')
                
                if len(item)!=2:
                    raise TypeError(f'`roles` passed as other iterable, but when iterating returned a `tuple`, but not with length `2`, got `{item!r}`')
                
                if (type(item[0]) is not Role) or (type(item[1]) is not int):
                    raise TypeError(f'Items should be `{Role.__name__}`, `int` pairs, but got `{item!r}`')
                
                roles_valid.append(item)
        
        # `roles` has an unknown format
        else:
            raise TypeError(
                f'`roles` should have been passed as dictlike with (`{Role.__name__}, `int`) items, or as other '
                f'iterable with (`{Role.__name__}, `int`) elements, but got `{roles!r}`')
        
        # Check default and moving to default position
        index=0
        limit=len(roles_valid)
        while True:
            if index==limit:
                break
            
            role, position = roles_valid[index]
            # Default role cannot be moved
            if role.position==0:
                if position!=0:
                    raise ValueError(f'Default role cannot be moved: `{role!r}`.')
                
                # default and moving to default, lets delete it
                del roles_valid[index]
                limit = limit-1
                continue
                
            else:
                # Role cannot be moved to default position
                if position==0:
                    raise ValueError(f'Role cannot be moved to position `0`.')
            
            index = index+1
            continue
        
        if not limit:
            return
        
        # Check dupe roles
        roles=set()
        ln=0
        
        for role, position in roles_valid:
            roles.add(role)
            if len(roles)==ln:
                raise ValueError(f'{Role.__name__} `{role!r}` is duped.')
            
            ln=ln+1
            continue
        
        # Now that we have the roles, lets order them
        roles_valid.sort(key = lambda item : item[1])
        
        # We have all the roles sorted, but they can have dupe positions too
        index=0
        limit=len(roles_valid)
        last_position=0
        while True:
            role, position = roles_valid[index]
            
            if last_position!=position:
                last_position=position
                
                index=index+1
                if index==limit:
                    break
                
                continue
            
            # Oh no, we need to reorder
            # First role cannot get here, becuase it cannot have position 0.
            roles=[roles_valid[index-1][0],role]
            
            sub_index=index+1
            
            while True:
                if sub_index==limit:
                    break
                
                role, position = roles_valid[sub_index]
                if position!=last_position:
                    break
                
                roles.append(role)
                sub_index=sub_index+1
                continue
            
            # We have all the roles with the same target position.
            # Now we order them by their actual position.
            roles.sort()
            
            index=index-1
            sub_index=0
            sub_limit=len(roles)
            while True:
                real_index=sub_index+index
                role=roles[sub_index]
                real_position=last_position+sub_index
                roles_valid[real_index]=(role,real_position)
                
                sub_index=sub_index+1
                if sub_index==sub_limit:
                    break
                
                continue
            
            added_position=sub_limit-1
            
            real_index=sub_index+index
            while True:
                if real_index==limit:
                    break
                
                role, position = roles_valid[real_index]
                real_position=position+added_position
                roles_valid[real_index]=(role,real_position)
                
                real_index=real_index+1
                continue
            
            
            index=index+sub_limit
            last_position=last_position+added_position
            
            if index==limit:
                break
            
            continue
        
        # We have all the roles in order. Filter out partial roles.
        index=0
        push=0
        while True:
            role, position = roles_valid[index]
            
            if role.guild is None:
                push=push+1
                del roles_valid[index]
                limit=limit-1
            
            else:
                if push:
                    roles_valid[index]=(role,position-push)
                
                index=index+1
            
            if index==limit:
                break
            
            continue
        
        # Did we get down to 0 role?
        if limit==0:
            return
        
        # Check role guild
        guild = roles_valid[0][0].guild
        
        index=1
        while True:
            if index==limit:
                break
            
            guild_ = roles_valid[index][0].guild
            index=index+1
            
            if guild is guild_:
                continue
            
            raise ValueError(f'There were roles passed at least from two different guilds: `{guild!r}` and `{guild_!r}`.')
        
        # Lets cut out every other role from the guild's
        roles_leftover=set(guild.all_role.values())
        for item in roles_valid:
            role=item[0]
            roles_leftover.remove(role)
        
        roles_leftover=sorted(roles_leftover)
    
        target_order=[]
        
        index_valid=0
        index_leftover=0
        limit_valid=len(roles_valid)
        limit_leftover=len(roles_leftover)
        position_target=0
        
        while True:
            if index_valid==limit_valid:
                while True:
                    if index_leftover==limit_leftover:
                        break
                    
                    role = roles_leftover[index_leftover]
                    index_leftover = index_leftover+1
                    target_order.append(role)
                    continue
                
                break
            
            if index_leftover==limit_leftover:
                while True:
                    if index_valid==limit_valid:
                        break
                    
                    role = roles_valid[index_valid][0]
                    index_valid = index_valid+1
                    target_order.append(role)
                    continue
                
                
                break
            
            role, position = roles_valid[index_valid]
            if position==position_target:
                position_target = position_target+1
                index_valid = index_valid+1
                target_order.append(role)
                continue
            
            role = roles_leftover[index_leftover]
            position_target = position_target+1
            index_leftover = index_leftover+1
            target_order.append(role)
            continue
        
        data = []
        
        for index, role in enumerate(target_order):
            position=role.position
            if index==position:
                continue
            
            data.append({'id':role.id,'position':index})
            continue
        
        # Nothing to move
        if not data:
            return
        
        await self.http.role_move(guild.id,data,reason)
        
    # Relationship related
    #hooman only
    async def relationship_delete(self,relationship):
        await self.http.relationship_delete(relationship.user.id)

    #hooman only
    async def relationship_create(self,user,relationship_type=None):
        data={}
        if relationship_type is not None:
            data['type']=relationship_type.value
        await self.http.relationship_create(user.id,data)

    #hooman only
    async def relationship_friend_request(self,user):
        data = {
            'username'      : user.name,
            'discriminator' : user.discriminator
                }
        await self.http.relationship_friend_request(data)

    
    #bot only!
    async def update_application_info(self):
        if self.is_bot:
            data = await self.http.client_application_info()
            self.application(data)
    
    async def client_gateway(self):
        url,time=self._gateway_pair
        if time+60.>monotonic():
            return url
        
        try:
            if self.is_bot:
                data = await self.http.client_gateway_bot()
            else:
                data = await self.http.client_gateway_hooman()
        except DiscordException as err:
            raise ConnectionError from err
        
        #if shard count is 1, lets auto detect shard count
        
        if not self.running:
            old_shard_count=self.shard_count
            if old_shard_count==1:
                shard_count=data['shards']
                
                if old_shard_count==0:
                    return #cannot change
                
                if shard_count<old_shard_count:
                    return #cannot go down
                
                self.shard_count=shard_count
                
                gateways=self.gateway.gateways
                for shard_id in range(old_shard_count,shard_count):
                    gateway=DiscordGateway(self,shard_id)
                    gateways.append(gateway)
            
            
        url=data['url']+'?encoding=json&v=6&compress=zlib-stream'
        self._gateway_pair=(url,monotonic(),)
        
        return url
        
    #user account only
    async def hypesquad_house_change(self,house_id):
        await self.http.hypesquad_house_change({'house_id':house_id})

    #user account only
    async def hypesquad_house_leave(self):
        await self.http.hypesquad_house_leave()
        
    async def connect(self):
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')

        try:
            data = await self.client_login_static()
        except BaseException as err:
            if type(err) is ConnectionError and err.args[0]=='Invalid adress':
                after=(
                    'Connection failed, could not connect to Discord.\n'
                    'Please check your internet connection / has Python rights '
                    'to use it?\n'
                        )
            else:
                after=None
                
            before=[
                'Exception occured at calling ',
                self.__class__.__name__,
                '.connect\n',
                    ]
            
            await self.loop.render_exc_async(err,before,after)
            return
        
        if type(data) is not dict:
            sys.stderr.write(''.join([
                'Connection failed, could not connect to Discord.\n'
                'Received invalid data:\n',
                repr(data),'\n']))
            return
        
        self._init_on_ready(data)
        await self.client_gateway()
        await self.gateway.start(self.loop)
        
        if self.is_bot:
            task = Task(self.update_application_info(),self.loop)
            if __debug__:
                task.__silence__()
        
        # Check it twice, because meanwhile logging on, connect calls are not limited
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        self.running=True
        PARSER_DEFAULTS.register(self)
        Task(self._connect(),self.loop)
    
    async def _connect(self):
        try:
            while True:
                try:
                    no_internet_stop = await self.gateway.run()
                except (GeneratorExit,CancelledError) as err:
                    # For now only here. These errors occured randomly for me since I made the wrapper, only once-once,
                    # and it was not the wrapper causing them, so it is time to say STOP.
                    # I also know `GeneratorExit` will show up as RuntimeError, but it is already a RuntimeError.
                    self._freeze_voice()
                    sys.stderr.write(
                        f'Ignoring unexpected outer Task or coroutine cancellation at {self!r}._connect as {err!r}.\n'
                        'The client will reconnect.\n')
                    continue
                else:
                    if not no_internet_stop:
                        break
                    
                    self._freeze_voice()
                    while True:
                        await self.http.restart()
                        await sleep(5.0,self.loop)
                        self._gateway_pair=(self._gateway_pair[0],0.0)
                        try:
                            await self.client_gateway()
                        except (OSError,ConnectionError,):
                            continue
                        else:
                            break
                    continue
        
        except BaseException as err:
            await self.loop.render_exc_async(err,[
                'Unexpected exception occured at ',
                repr(self),
                '._connect\n',
                    ],
                'If you can reproduce this bug, Please send me a message or open an issue whith your code, and with '
                'every detail how to reproduce it.\n'
                'Thanks!\n')
        
        finally:
            await self.gateway.close()
            
            PARSER_DEFAULTS.unregister(self)
            self.running = False
            
            if not self.guild_profiles:
                return
            
            to_remove=[]
            for guild in self.guild_profiles:
                guild._delete(self)
                if guild.clients:
                    continue
                to_remove.append(guild)

            if to_remove:
                for guild in to_remove:
                    del self.guild_profiles[guild]

            #needs to delete the references for cleanup
            guild=None
            to_remove=None
            
    async def join_voice_channel(self,channel):
        guild_id=channel.guild.id

        try:
            voice_client=self.voice_clients[guild_id]
        except KeyError:
            voice_client = await VoiceClient(self,channel)
        else:
            if voice_client.channel is not channel:
                gateway=self._gateway_for(channel.guild)
                await gateway._change_voice_state(guild_id,channel.id)
        
        return voice_client

    async def _delay_ready(self):
        ready_state=self.ready_state
        try:
            if self.is_bot:
                await ready_state
            
            if ready_state.guilds and CACHE_USER:
                await self._request_members2(ready_state.guilds)
                
            self.ready_state=None

            if not self.is_bot:
                await self.gateway._request_sync()
                
        except CancelledError:
            pass
        else:
            Task(_with_error(self,self.events.ready(self)),self.loop)
        finally:
            start_clients()

    async def _request_members2(self,guilds):
        count=0
        for guild in guilds:
            count+=ceil(guild.user_count/1000.)

        event=self.events.guild_user_chunk
        waiter=event.default
        if waiter is not None:
            waiter.cancel()

        waiter=mass_user_chunker(self,count)
        event.default=waiter

        #we only want to request 75~ guilds per chunk request.
        guild_ids=[]
        data = {
            'op'            : DiscordGateway.REQUEST_MEMBERS,
            'd' : {
                'guild_id'  : guild_ids,
                'query'     : '',
                'limit'     : 0,
                'presences' : CACHE_PRESENCE,
                    },
                }

        shard_count=self.shard_count
        if shard_count:
            guilds_by_shards=[[] for x in range(shard_count)]
            for guild in guilds:
                shard_index=(guild.id>>22)%shard_count
                guilds_by_shards[shard_index].append(guild)

            for index in range(shard_count):
                guild_group=guilds_by_shards[index]
                gateway=self.gateway.gateways[index]
                for guild in guild_group:
                    guild_ids.append(guild.id)
                    if len(guild_ids)==75:
                        await gateway.send_as_json(data)
                        guild_ids.clear()

                if guild_ids:
                    await gateway.send_as_json(data)
                    guild_ids.clear()
        else:
            gateway=self.gateway
            for guild in guilds:
                guild_ids.append(guild.id)
                if len(guild_ids)==75:
                    await gateway.send_as_json(data)
                    guild_ids.clear()

            if guild_ids:
                await gateway.send_as_json(data)

        del guild_ids
        await waiter
        event.default=None

    async def _request_members(self,guild):
        count=ceil(guild.user_count/1000.)

        event=self.events.guild_user_chunk
        if event.default is not None:
            await event.default

        waiter=mass_user_chunker(self,count)
        guild_id=guild.id
        try:
            waiters=event.waiters[guild_id]
        except KeyError:
            waiters=event.waiters[guild_id]=[waiter]
        else:
            for waiter in waiters:
                waiter.cancel()
            waiters.clear()
            waiters.append(waiter)

        data = {
            'op'            : DiscordGateway.REQUEST_MEMBERS,
            'd' : {
                'guild_id'  : guild.id,
                'query'     : '',
                'limit'     : 0,
                'presences' : CACHE_PRESENCE,
                    },
                }


        gateway=self._gateway_for(guild)
        await gateway.send_as_json(data)

        result = await waiter
        if result is None:
            del waiters[0]
            if not waiters:
                del event.waiters[guild_id]


    async def request_member(self,guild,name,limit=1):
        #do we really need these checks?
        if limit>1000:
            limit=1000
        elif limit<1:
            return []
        if not 1<len(name)<33:
            return []

        event=self.events.guild_user_chunk
        if event.default is not None:
            await event.default

        waiter=single_user_chunker(self,limit)
        guild_id=guild.id
        try:
            waiters=event.waiters[guild_id]
        except KeyError:
            waiters=event.waiters[guild_id]=[waiter]
        else:
            waiters.append(waiter)
            await waiters[-2]

        data = {
            'op'            : DiscordGateway.REQUEST_MEMBERS,
            'd' : {
                'guild_id'  : guild_id,
                'query'     : name,
                'limit'     : limit,
                'presences' : CACHE_PRESENCE,
                    },
                }

        gateway=self._gateway_for(guild)

        kokoro=gateway.kokoro
        if kokoro is None:
            latency=1.0 # just a random timeout, we will not return anything anyways
        else:
            latency=kokoro.latency

        waiter.start_timer(self,latency)

        await gateway.send_as_json(data)

        result = await waiter
        if result is None:
            del waiters[0]
            if not waiters:
                del event.waiters[guild_id]
            result=[]
        return result
    
    async def disconnect(self):
        if not self.running:
            return

        self.running=False
        shard_count=self.shard_count
        if shard_count:
            for gateway in self.gateway.gateways:
                gateway.kokoro.cancel()
            
            for voice_client in self.voice_clients.values():
                await voice_client.disconnect()
            
            if (not self.is_bot):
                await self.http.client_logout()
            
            for gateway in self.gateway.gateways:
                websocket=gateway.websocket
                if (websocket is not None) and websocket.open:
                    await gateway.close()
        else:
            self.gateway.kokoro.cancel()
            
            for voice_client in self.voice_clients.values():
                await voice_client.disconnect()
            
            if (not self.is_bot):
                await self.http.client_logout()
            
            websocket=self.gateway.websocket
            if (websocket is not None) and websocket.open:
                await self.gateway.close()
    
    def voice_client_for(self,message):
        guild=message.guild
        if guild is None:
            return
        
        return self.voice_clients.get(guild.id,None)

    def get_guild(self,name):
        if 1<len(name)<101:
            for guild in self.guild_profiles.keys():
                if guild.name==name:
                    return guild

    @property
    def owner(self):
        maybe_owner=self.application.owner
        if type(maybe_owner) is Team:
            return maybe_owner.owner
        return maybe_owner

    def is_owner(self,user):
        maybe_owner=self.application.owner
        if type(maybe_owner) is Team:
            return user in maybe_owner.accepted
        return maybe_owner is user

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

        avatar=data['avatar']
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
        
        email=data.get('email','')
        if self.email!=email:
            old['email']=self.email
            self.email=email
        
        premium_type=PremiumType.INSTANCES[data.get('premium_type',0)]
        if self.premium_type is not premium_type:
            old['premium_type']=premium_type
            self.premium_type=premium_type
        
        system=data.get('system',False)
        if self.system!=system:
            old['system']=self.system
            self.system=system
        
        verified=data.get('verified',False)
        if self.verified!=verified:
            old['verified']=self.verified
            self.verified=verified
        
        mfa=data.get('mfa_enabled',False)
        if self.mfa!=mfa:
            old['mfa']=self.mfa
            self.mfa=mfa

        flags=UserFlag(data.get('flags',0))
        if self.flags!=flags:
            old['flags']=self.flags
            self.flags=flags

        locale=parse_locale(data)
        if self.locale!=locale:
            old['locale']=self.locale
            self.locale=locale

        return old

    def _update_no_return(self,data):
        self.name=data['username']
        
        self.discriminator=int(data['discriminator'])
        
        avatar=data['avatar']
        if avatar is None:
            self.avatar=0
            self.has_animated_avatar=False
        elif avatar.startswith('a_'):
            self.avatar=int(avatar[2:],16)
            self.has_animated_avatar=True
        else:
            self.avatar=int(avatar,16)
            self.has_animated_avatar=False
        
        self.system=data.get('system',False)
        
        self.verified=data.get('verified',False)
        
        self.email=data.get('email','')

        self.premium_type=PremiumType.INSTANCES[data.get('premium_type',0)]
        
        self.mfa=data.get('mfa_enabled',False)

        self.flags=UserFlag(data.get('flags',0))

        self.locale=parse_locale(data)

    def _update_profile_only(self,data,guild):
        try:
            profile=self.guild_profiles[guild]
        except KeyError:
            self.guild_profiles[guild]=GuildProfile(data,guild)
            guild.users[self.id]=self
            return {}
        return profile._update(data,guild)

    def _update_profile_only_no_return(self,data,guild):
        try:
            profile=self.guild_profiles[guild]
        except KeyError:
            self.guild_profiles[guild]=GuildProfile(data,guild)
            guild.users[self.id]=self
            return
        profile._update_no_return(data,guild)

    @property
    def friends(self):
        type_=RelationshipType.friend
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def blocked(self):
        type_=RelationshipType.blocked
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def received_requests(self):
        type_=RelationshipType.received_request
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def sent_requests(self):
        type_=RelationshipType.sent_request
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def guild_order(self):
        guild_ids=self.settings.guild_order_ids
        if guild_ids:
            leftover_guilds=set(self.guild_profiles.keys())
            ordered=[]
            for guild_id in guild_ids:
                
                try:
                    guild=GUILDS[guild_id]
                except KeyError:
                    continue
                
                # already left guilds can show up as well
                try:
                    leftover_guilds.remove(guild)
                except KeyError:
                    continue
                
                ordered.append(guild)
            
            if not leftover_guilds:
                return ordered
            
            orderable=[]
            un_orderable=[]
            
            for guild in leftover_guilds:
                joined_at=self.guild_profiles[guild].joined_at
                
                # joined_at can be None
                if joined_at is None:
                    # we get the guilds in creation order, so it is fine ^^'
                    un_orderable.append(guild)
                else:
                    # newest guild is every time the 1st
                    orderable.append((joined_at,guild),)
            
            orderable.sort(key=lambda x:x[0],reverse=True)
            
            # we want the reversed creation order
            un_orderable.reverse()
            un_orderable.extend(x[1] for x in orderable)
            un_orderable.extend(ordered)
            
            return un_orderable

        orderable=[]
        un_orderable=[]
        
        for guild,profile in self.guild_profiles.items():
            joined_at=profile.joined_at
            
            # joined_at can be None
            if joined_at is None:
                # we get the guilds in creation order, so it is fine ^^'
                un_orderable.append(guild)
            else:
                # newest guild is every time the 1st
                orderable.append((joined_at,guild),)
        
        orderable.sort(key=lambda x:x[0],reverse=True)
        
        # we want the reversed creation order
        un_orderable.reverse()
        un_orderable.extend(x[1] for x in orderable)
        return un_orderable
    
    @property
    def guild_order_with_folders(self):
        guild_folders=self.settings.guild_folders
        
        # you must(?) have at least 1 folder
        if not guild_folders:
            return self.guild_order
        
        leftover_guilds=set(self.guild_profiles.keys())
        ordered=[]
        
        for folder in guild_folders:
            guilds=folder._get_and_filter_guilds(self)
            
            # real folder
            if folder.id:
                for guild in guilds:
                    try:
                        leftover_guilds.remove(guild)
                    except KeyError:
                        continue
                    
                ordered.append(folder)
            # folder placeholder
            else:
                for guild in guilds:
                    try:
                        leftover_guilds.remove(guild)
                    except KeyError:
                        continue
                    
                    ordered.append(guild)
        
        if not leftover_guilds:
            return ordered
        
        orderable=[]
        un_orderable=[]
        
        for guild in leftover_guilds:
            joined_at=self.guild_profiles[guild].joined_at
            
            # joined_at can be None
            if joined_at is None:
                # we get the guilds in creation order, so it is fine ^^'
                un_orderable.append(guild)
            else:
                # newest guild is every time the 1st
                orderable.append((joined_at,guild),)
        
        orderable.sort(key=lambda x:x[0],reverse=True)
        
        # we want the reversed creation order
        un_orderable.reverse()
        un_orderable.extend(x[1] for x in orderable)
        un_orderable.extend(ordered)
        
        return un_orderable
        
    @property
    def no_DM_guilds(self):
        guild_ids=self.settings.no_DM_guild_ids
        
        result=[]
        if not guild_ids:
            return result
            
        for guild_id in guild_ids:
            try:
                guild=GUILDS[guild_id]
            except KeyError:
                continue
            
            if self not in guild.clients:
                continue
            
            result.append(guild)
            
        return result
        

    @property
    def allowed_DM_guilds(self):
        guild_ids=self.settings.no_DM_guild_ids
        
        result=list(self.guild_profiles.keys())
        if not guild_ids:
            return result
        
        for guild_id in guild_ids:
            index=0
            limit=len(result)
            while True:
                if index==limit:
                    break
                
                guild=result[index]
                if guild.id==guild_id:
                    del result[index]
                    limit=limit-1
                    continue
                
                index=index+1
                continue
                
        return result
    
    def _freeze_voice(self):
        voice_clients=self.voice_clients
        if not voice_clients:
            return
        
        for voice_client in self.voice_clients.values():
            voice_client._freeze()
    
    def _freeze_voice_for(self,gateway):
        voice_clients=self.voice_clients
        if not voice_clients:
            return
        
        shard_count=self.shard_count
        if shard_count:
            target_shard_id=gateway.shard_id
            for voice_client in self.voice_clients.values():
                guild_id=voice_client.channel.guild.id
                if (guild_id>>22)%shard_count==target_shard_id:
                    voice_client._freeze()
            return
        
        for voice_client in self.voice_clients.values():
            voice_client._freeze()
    
    
    def _unfreeze_voice(self):
        voice_clients=self.voice_clients
        if not voice_clients:
            return

        for voice_client in voice_clients.values():
            voice_client._unfreeze()
    
    def _unfreeze_voice_for(self,gateway):
        voice_clients=self.voice_clients
        if not voice_clients:
            return
        
        shard_count=self.shard_count
        if shard_count:
            target_shard_id=gateway.shard_id
            for voice_client in voice_clients.values():
                guild_id=voice_client.channel.guild.id
                if (guild_id>>22)%shard_count==target_shard_id:
                    voice_client._unfreeze()
            return
        
        for voice_client in voice_clients.values():
            voice_client._unfreeze()
    
    def _gateway_for(self,guild):
        shard_count=self.shard_count
        if shard_count:
            if guild is None:
                return self.gateway.gateways[0]
            
            guild_id=guild.id
            shard_index=(guild_id>>22)%shard_count
            
            return self.gateway.gateways[shard_index]
        
        return self.gateway
                
class Typer(object):
    __slots__=('channel', 'client', 'timeout', 'waiter',)
    def __init__(self,client,channel,timeout=300.):
        self.client = client
        self.channel= channel
        self.waiter = None
        self.timeout= timeout
    
    def __enter__(self):
        Task(self.run(),self.client.loop)
        return self
    
    async def run(self):
        #js client's typing is 8s
        loop=self.client.loop
        while self.timeout>0.:
            self.timeout-=8.
            self.waiter=sleep(8.,loop)
            await self.client.http.typing(self.channel.id)
            await self.waiter
        self.waiter=None
    
    def cancel(self):
        self.timeout=0.
        if self.waiter is not None:
            self.waiter.set_result(None)
            
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.cancel()

class Settings(object):
    __slots__=('accessibility_detection', 'afk_timeout', 'animate_emojis',
        'compact_mode', 'content_filter', 'convert_emojis', 'custom_status',
        'detect_platform_accounts', 'developer_mode', 'enable_tts_command',
        'friend_request_flag', 'games_tab', 'guild_folders', 'guild_order_ids',
        'locale', 'no_DM_from_new_guilds', 'no_DM_guild_ids', 'play_gifs',
        'render_attachments', 'render_embeds', 'render_links',
        'render_reactions', 'show_current_game', 'status',
        'stream_notifications', 'theme', 'timezone_offset', )
    
    def __init__(self):
        self.accessibility_detection=False
        self.afk_timeout    = 0
        self.animate_emojis = True
        self.compact_mode   = False
        self.content_filter = ContentFilterLevel.disabled
        self.convert_emojis = True
        self.custom_status  = None
        self.detect_platform_accounts=True
        self.developer_mode = False
        self.enable_tts_command=True
        self.friend_request_flag=FriendRequestFlag.all
        self.games_tab      = True
        self.guild_folders  = []
        self.guild_order_ids= []
        self.locale         = DEFAULT_LOCALE
        self.no_DM_from_new_guilds=False
        self.no_DM_guild_ids= []
        self.play_gifs      = True
        self.render_attachments=True
        self.render_embeds  = True
        self.render_links   = True
        self.render_reactions=True
        self.status         = Status.online
        self.stream_notifications=True
        self.show_current_game=True
        self.theme          = Theme.dark
        self.timezone_offset= 0

    def _update(self,data):
        old={}
        
        try:
            accessibility_detection=data['allow_accessibility_detection']
        except KeyError:
            pass
        else:
            if self.accessibility_detection!=accessibility_detection:
                old['accessibility_detection']=self.accessibility_detection
                self.accessibility_detection=accessibility_detection
        
        try:
            afk_timeout=data['afk_timeout']
        except KeyError:
            pass
        else:
            if self.afk_timeout!=afk_timeout:
                old['afk_timeout']=self.afk_timeout
                self.afk_timeout=afk_timeout
        
        try:
            animate_emojis=data['animate_emojis']
        except KeyError:
            pass
        else:
            if self.animate_emojis!=animate_emojis:
                old['animate_emojis']=self.animate_emojis
                self.animate_emojis=animate_emojis
        
        try:
            compact_mode=data['message_display_compact']
        except KeyError:
            pass
        else:
            if self.compact_mode!=compact_mode:
                old['compact_mode']=self.compact_mode
                self.compact_mode=compact_mode
        
        try:
            content_filter=data['explicit_content_filter']
        except KeyError:
            pass
        else:
            content_filter=ContentFilterLevel.INSTANCES[content_filter]
            if self.content_filter is not content_filter:
                old['content_filter']=self.content_filter
                self.content_filter=content_filter
        
        try:
            convert_emojis=data['convert_emoticons']
        except KeyError:
            pass
        else:
            if self.convert_emojis!=convert_emojis:
                old['convert_emojis']=self.convert_emojis
                self.convert_emojis=convert_emojis
        
        try:
            custom_status=data['custom_status']
        except KeyError:
            pass
        else:
            custom_status=self.decode_custom_status(custom_status)
            if self.custom_status is None:
                if custom_status is not None:
                    old['custom_status']=None
            else:
                if custom_status is None:
                    old['custom_status']=self.custom_status
                    self.custom_status=None
                elif self.custom_status!=custom_status:
                    old['custom_status']=self.custom_status
                    self.custom_status=custom_status
        
        try:
            detect_platform_accounts=data['detect_platform_accounts']
        except KeyError:
            pass
        else:
            if self.detect_platform_accounts!=detect_platform_accounts:
                old['detect_platform_accounts']=self.detect_platform_accounts
                self.detect_platform_accounts=detect_platform_accounts
        
        try:
            developer_mode=data['developer_mode']
        except KeyError:
            pass
        else:
            if self.developer_mode!=developer_mode:
                old['developer_mode']=self.developer_mode
                self.developer_mode=developer_mode
        
        try:
            enable_tts_command=data['enable_tts_command']
        except KeyError:
            pass
        else:
            if self.enable_tts_command!=enable_tts_command:
                old['enable_tts_command']=self.enable_tts_command
                self.enable_tts_command=enable_tts_command
        
        try:
            friend_request_flag=data['friend_source_flags']
        except KeyError:
            pass
        else:
            friend_request_flag=FriendRequestFlag.decode(friend_request_flag)
            if self.friend_request_flag is not friend_request_flag:
                old['friend_request_flag']=self.friend_request_flag
                self.friend_request_flag=friend_request_flag
        
        try:
            games_tab=(not data['disable_games_tab'])
        except KeyError:
            pass
        else:
            if self.games_tab!=games_tab:
                old['games_tab']=self.games_tab
                self.games_tab=games_tab
        
        try:
            guild_folders=data['guild_folders']
        except KeyError:
            pass
        else:
            guild_folders=[GuildFolder(guild_folder_data) for guild_folder_data in guild_folders]
            if self.guild_folders!=guild_folders:
                old['guild_folders']=self.guild_folders
                self.guild_folders=guild_folders
        
        try:
            guild_order_ids=data['guild_positions']
        except KeyError:
            pass
        else:
            guild_order_ids=[int(guild_id) for guild_id in guild_order_ids]
            if self.guild_order_ids!=guild_order_ids:
                old['guild_order_ids']=self.guild_order_ids
                self.guild_order_ids=guild_order_ids

        locale=parse_locale_optional(data)
        if (locale is not None):
            if self.locale!=locale:
                old['locale']=self.locale
                self.locale=locale
        
        try:
            no_DM_from_new_guilds=data['default_guilds_restricted']
        except KeyError:
            pass
        else:
            if self.no_DM_from_new_guilds!=no_DM_from_new_guilds:
                old['no_DM_from_new_guilds']=self.no_DM_from_new_guilds
                self.no_DM_from_new_guilds=no_DM_from_new_guilds
        
        try:
            no_DM_guild_ids=data['restricted_guilds']
        except KeyError:
            pass
        else:
            no_DM_guild_ids=[int(guild_id) for guild_id in no_DM_guild_ids]
            if self.no_DM_guild_ids!=no_DM_guild_ids:
                old['no_DM_guild_ids']=self.no_DM_guild_ids
                self.no_DM_guild_ids=no_DM_guild_ids
        
        try:
            play_gifs=data['gif_auto_play']
        except KeyError:
            pass
        else:
            if self.play_gifs!=play_gifs:
                old['play_gifs']=self.play_gifs
                self.play_gifs=play_gifs
        
        try:
            render_attachments=data['inline_attachment_media']
        except KeyError:
            pass
        else:
            if self.render_attachments!=render_attachments:
                old['render_attachments']=self.render_attachments
                self.render_attachments=render_attachments
        
        try:
            render_embeds=data['render_embeds']
        except KeyError:
            pass
        else:
            if self.render_embeds!=render_embeds:
                old['render_embeds']=self.render_embeds
                self.render_embeds=render_embeds
        
        try:
            render_links=data['inline_embed_media']
        except KeyError:
            pass
        else:
            if self.render_links!=render_links:
                old['render_links']=self.render_links
                self.render_links=render_links
        
        try:
            render_reactions=data['render_reactions']
        except KeyError:
            pass
        else:
            if self.render_reactions!=render_reactions:
                old['render_reactions']=self.render_reactions
                self.render_reactions=render_reactions
        
        try:
            show_current_game=data['show_current_game']
        except KeyError:
            pass
        else:
            if self.show_current_game!=show_current_game:
                old['show_current_game']=self.show_current_game
                self.show_current_game=show_current_game

        try:
            status=data['status']
        except KeyError:
            pass
        else:
            status=Status.INSTANCES[status]
            if self.status is not status:
                old['status']=self.status
                self.status=status
        
        try:
            stream_notifications=data['stream_notifications_enabled']
        except KeyError:
            pass
        else:
            if self.stream_notifications!=stream_notifications:
                old['stream_notifications']=self.stream_notifications
                self.stream_notifications=stream_notifications
        
        try:
            theme=data['theme']
        except KeyError:
            pass
        else:
            theme=Theme.INSTANCES[theme]
            if self.theme is not theme:
                old['theme']=self.theme
                self.theme=theme
        
        try:
            timezone_offset=data['timezone_offset']
        except KeyError:
            pass
        else:
            if self.timezone_offset!=timezone_offset:
                old['timezone_offset']=self.timezone_offset
                self.timezone_offset=timezone_offset
        
        return old
        
    def _update_no_return(self,data):
        try:
            self.accessibility_detection=data['allow_accessibility_detection']
        except KeyError:
            pass
        
        try:
            self.afk_timeout=data['afk_timeout']
        except KeyError:
            pass
        
        try:
            self.animate_emojis=data['animate_emojis']
        except KeyError:
            pass
        
        try:
            self.compact_mode=data['message_display_compact']
        except KeyError:
            pass
        
        try:
            content_filter=data['explicit_content_filter']
        except KeyError:
            pass
        else:
            self.content_filter=ContentFilterLevel.INSTANCES[content_filter]
        
        try:
            self.convert_emojis=data['convert_emoticons']
        except KeyError:
            pass
        
        try:
            custom_status=data['custom_status']
        except KeyError:
            pass
        else:
            self.custom_status=self.decode_custom_status(custom_status)
            
        try:
            self.detect_platform_accounts=data['detect_platform_accounts']
        except KeyError:
            pass
        
        try:
            self.developer_mode=data['developer_mode']
        except KeyError:
            pass
        
        try:
            self.enable_tts_command=data['enable_tts_command']
        except KeyError:
            pass
        
        try:
            friend_request_flag=data['friend_request_flag']
        except KeyError:
            pass
        else:
            self.friend_request_flag=FriendRequestFlag.decode(friend_request_flag)
        
        try:
            self.games_tab=(not data['disable_games_tab'])
        except KeyError:
            pass
        
        try:
            guild_folders=data['guild_folders']
        except KeyError:
            pass
        else:
            self.guild_folders=[GuildFolder(guild_folder_data) for guild_folder_data in guild_folders]
            
        try:
            guild_order_ids=data['guild_positions']
        except KeyError:
            pass
        else:
            self.guild_order_ids=[int(guild_id) for guild_id in guild_order_ids]
        
        
        locale = parse_locale_optional(data)
        if locale is not None:
            self.locale=locale
        
        try:
            self.no_DM_from_new_guilds=data['default_guilds_restricted']
        except KeyError:
            pass
        
        try:
            no_DM_guild_ids=data['restricted_guilds']
        except KeyError:
            pass
        else:
            self.no_DM_guild_ids=[int(guild_id) for guild_id in no_DM_guild_ids]
        
        try:
            self.play_gifs=data['gif_auto_play']
        except KeyError:
            pass
        
        try:
            self.render_attachments=data['inline_attachment_media']
        except KeyError:
            pass
        
        try:
            self.render_embeds=data['render_embeds']
        except KeyError:
            pass
        
        try:
            self.render_links=data['inline_embed_media']
        except KeyError:
            pass
        
        try:
            self.render_reactions=data['render_reactions']
        except KeyError:
            pass
        
        try:
            self.show_current_game=data['show_current_game']
        except KeyError:
            pass
        
        try:
            status=data['status']
        except KeyError:
            pass
        else:
            self.status=Status.INSTANCES[status]
        
        try:
            self.stream_notifications=data['stream_notifications_enabled']
        except KeyError:
            pass
        
        try:
            theme=data['theme']
        except KeyError:
            pass
        else:
            self.theme=Theme.INSTANCES[theme]
        
        try:
            self.timezone_offset=data['timezone_offset']
        except KeyError:
            pass
    
    @staticmethod
    def decode_custom_status(data):
        if data is None:
            return None
        
        result={}
        
        result['text']=data['text']
        
        expires_at=data['expires_at']
        if expires_at is not None:
            expires_at=parse_time(expires_at)
        result['expires_at']=expires_at
        
        emoji_id=data['emoji_id']
        emoji_name=data['emoji_name']
        if None is emoji_id is emoji_name:
            emoji=None
        else:
            emoji_data = {
                'id'    : emoji_id,
                'name'  : emoji_name,
                    }
            emoji=PartialEmoji(emoji_data)
        result['emoji']=emoji
        
        return result
    
    @staticmethod
    def encode_custom_status(data):
        result={}
        
        result['text']=data.get('text')
        
        expires_at=data.get('expires_at')
        if expires_at is not None:
            expires_at=expires_at.__format__('%Y-%m-%dT%H:%M:%S+00:00')
        result['expires_at']=expires_at
        
        emoji=data.get('emoji')
        if emoji is None:
            emoji_id    = None
            emoji_name  = None
        elif emoji.is_custom_emoji:
            emoji_id    = None
            emoji_name  = emoji.unicode
        else:
            emoji_id    = emoji.id.__str__()
            emoji_name  = emoji.name
            
        result['emoji_id']  = emoji_id
        result['emoji_name']= emoji_name
        
        return result
    
class GuildFolder(object):
    __slots__=('color', 'guild_ids', 'id', 'name', )
    def __init__(self,data):
        name        = data['name']
        if name is None:
            name    = ''
        self.name   = name
        
        color       = data['color']
        if color is not None:
            color   = Color(color)
        self.color  = color
        
        id_         = data['id']
        if id_ is None:
            id_     = 0
        self.id     = id_
        
        self.guild_ids=[int(guild_id) for guild_id in data['guild_ids']]

    @property
    def guilds(self):
        guilds=[]
        for guild_id in self.guild_ids:
            try:
                guild=GUILDS[guild_id]
            except KeyError:
                continue
            guilds.append(guild)
        
        return guilds
    
    # filter out deleted guilds as well
    def _get_and_filter_guilds(self,client):
        guild_profiles=client.guild_profiles
        guild_ids=self.guild_ids
        
        guilds=[]
        
        index=0
        limit=len(guild_ids)
        while True:
            if index==limit:
                break
            
            guild_id=guild_ids[index]
            
            try:
                guild=GUILDS[guild_id]
            except KeyError:
                del guild_ids[index]
                limit=limit-1
                continue
            
            if client not in guild.clients:
                del guild_ids[index]
                limit=limit-1
                continue
            
            guilds.append(guild)
            index=index+1
            
        return guilds
        
    def copy(self):
        new=object.__new__(type(self))
        
        new.color       = self.color
        new.name        = self.name
        new.id          = self.id
        new.guild_ids   = self.guild_ids.copy()
        
        return new
        
    def __len__(self):
        return len(self.guild_ids)
    
    def __iter__(self):
        return iter(self.guilds)
    
    def __reversed__(self):
        return reversed(self.guilds)
    
    def __repr__(self):
        result=['<',self.__class__.__name__,' length=',self.__len__().__repr__()]
        name=self.name
        if name:
            result.append(', name=\'')
            result.append(name)
            result.append('\'')
        
        color=self.color
        if color is not None:
            result.append(', color=')
            result.append(color.as_html)
        
        result.append('>')
        
        return ''.join(result)
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id!=other.id:
            return False
        
        if self.name!=other.name:
            return False
        
        if self.color is None:
            if other.color is not None:
                return False
        else:
            if other.color is None:
                return False
            elif self.color!=other.color:
                return False
        
        if self.guild_ids!=other.guild_ids:
            return False
        
        return True
    
class Achievement(object):
    __slots__=('application_id', 'description', 'icon', 'id', 'name', 'secret',
        'secure',)
    
    def __init__(self,data):
        self.application_id=int(data['application_id'])
        self.id=int(data['id'])

        self._update_no_return(data)

    icon_url=property(URLS.achievement_icon_url)
    icon_url_as=URLS.achievement_icon_url_as
    
    @property
    def created_at(self):
        return id_to_time(self.id)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    def __str__(self):
        return self.name
    
    def __format__(self,code):
        if not code:
            return self.name
        if code=='c':
            return self.created_at.__format__('%Y.%m.%d-%H:%M:%S')
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _update(self,data):
        old={}
        
        name=data['name']['default']
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        description=data['description']['default']
        if self.description!=description:
            old['description']=self.description
            self.description=description
        
        secret=data['secret']
        if self.secret!=secret:
            old['secret']=self.secret
            self.secret=secret
        
        secure=data['secure']
        if self.secure!=secure:
            old['secure']=self.secure
            self.secure=secure
        
        icon=data.get('icon_hash')
        icon=0 if icon is None else int(icon,16)
        if self.icon!=icon:
            old['icon']=icon
            self.icon=icon
        
        return old
    
    def _update_no_return(self,data):
        self.name=data['name']['default']
        self.description=data['description']['default']
        
        self.secret=data['secret']
        self.secure=data['secure']
        
        icon=data.get('icon_hash')
        self.icon=0 if icon is None else int(icon,16)


client_core.Client=Client
message.Client=Client

del client_core
del re
del URLS
del message_at_index
del messages_till_index
del UserBase
del message
