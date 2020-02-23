# -*- coding: utf-8 -*-
__all__ = ('DiscordHTTPClient', )
import sys, re
from .dereaddons_local import multidict_titled, modulize
from .futures import sleep
from .py_http import HTTPClient
from .py_reqrep import Request_CM

from .py_hdrs import METH_PATCH, METH_GET, METH_DELETE, METH_POST, METH_PUT,\
    CONTENT_TYPE, USER_AGENT, AUTHORIZATION

from .exceptions import DiscordException, ERROR_CODES
from .others import to_json, from_json, quote, Discord_hdrs

AUDIT_LOG_REASON    = Discord_hdrs.AUDIT_LOG_REASON
RATELIMIT_REMAINING = Discord_hdrs.RATELIMIT_REMAINING
RATELIMIT_PRECISION = Discord_hdrs.RATELIMIT_PRECISION

from .ratelimit import ratelimit_handler,ratelimit_global,GLOBALLY_LIMITED

#this file contains every link needed to communicate with discord
VALID_ICON_FORMATS   = ('jpg','jpeg','png','webp')
VALID_ICON_SIZES     = {1<<x for x in range(4,13)}
VALID_ICON_FORMATS_EXTENDED = (*VALID_ICON_FORMATS,'gif',)

API_ENDPOINT='https://discordapp.com/api/v7' #v7 includes special error messages
CDN_ENDPOINT='https://cdn.discordapp.com'
DIS_ENDPOINT='https://discordapp.com'

@modulize
class URLS:
    style_pattern=re.compile('(^shield$)|(^banner[1-4]$)')
    #returns a URL that allows the client to jump to this message
    #guild is guild's id, or @me if there is no guild
    def message_jump_url(message):
        channel=message.channel
        guild=channel.guild
        guild_id='@me' if guild is None else str(guild.id)
        return f'{DIS_ENDPOINT}/channels/{guild_id}/{channel.id}/{message.id}'

    def guild_icon_url(guild):
        icon=guild.icon
        if not icon:
            return None
        
        if guild.has_animated_icon:
            start='a_'
            ext='gif'
        else:
            start=''
            ext='png'

        return f'{CDN_ENDPOINT}/icons/{guild.id}/{start}{icon:0>32x}.{ext}'

    def guild_icon_url_as(guild,ext='png',size=None):
        icon=guild.icon
        if not icon:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if guild.has_animated_icon:
                start='a_'
                ext='gif'
            else:
                start=''
                ext='png'
        else:
            if guild.has_animated_icon:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
                start='a_'
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
                start=''
    
        return f'{CDN_ENDPOINT}/icons/{guild.id}/{start}{icon:0>32x}.{ext}{end}'

    def guild_splash_url(guild):
        splash=guild.splash
        if splash:
            return f'{CDN_ENDPOINT}/splashes/{guild.id}/{splash:0>32x}.png'
        return None
        
    def guild_splash_url_as(guild,ext='png',size=None):
        splash=guild.splash
        if not splash:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/splashes/{guild.id}/{splash:0>32x}.{ext}{end}'

    def guild_discovery_splash_url(guild):
        discovery_splash=guild.discovery_splash
        if discovery_splash:
            return f'{CDN_ENDPOINT}/discovery-splashes/{guild.id}/{discovery_splash:0>32x}.png'
        return None
        
    def guild_discovery_splash_url_as(guild,ext='png',size=None):
        discovery_splash=guild.discovery_splash
        if not discovery_splash:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/discovery-splashes/{guild.id}/{discovery_splash:0>32x}.{ext}{end}'
    
    def guild_banner_url(guild):
        banner=guild.banner
        if not banner:
            return None
            
        return f'{CDN_ENDPOINT}/banners/{guild.id}/{banner:0>32x}.png'
    
    
    def guild_banner_url_as(guild,ext='png',size=None):
        banner=guild.banner
        if not banner:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/banners/{guild.id}/{banner:0>32x}.{ext}{end}'


    def guild_embed_url(guild,style='shield'):
        if URLS.style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        return f'{API_ENDPOINT}/guilds/{guild.id}/embed.png?style={style}'

    def guild_widget_url(guild,style='shield'):
        if URLS.style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        return f'{API_ENDPOINT}/guilds/{guild.id}/widget.png?style={style}'

    def guild_widget_json_url(guild):
        return  f'{API_ENDPOINT}/guilds/{guild.id}/widget.json'

    def channel_group_icon_url(channel):
        icon=channel.icon
        if not icon:
            return None
        
        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{icon:0>32x}.png'
        
    def channel_group_icon_url_as(channel,ext='png',size=None):
        icon=channel.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{icon:0>32x}.{ext}{end}'

    def emoji_url(emoji):
        if emoji.is_unicode_emoji():
            return None
        
        if emoji.animated:
             ext='gif'
        else:
             ext='png'
            
        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}'

    def emoji_url_as(emoji,ext=None,size=None):
        if emoji.is_unicode_emoji():
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if emoji.animated:
                ext='gif'
            else:
                ext='png'
        else:
            if emoji.animated:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
            else:
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}{end}'

    def webhook_url(webhook):
        return f'{API_ENDPOINT}/webhooks/{webhook.id}/{webhook.token}'

    webhook_urlpattern=re.compile('(?:https://)?discordapp.com/api/(?:v\d/)?webhooks/([0-9]{17,21})/([a-zA-Z0-9\.\-\_]{60,68})(?:/.*)?')

    def webhook_avatar_url(webhook):
        avatar=webhook.avatar
        if not avatar:
            #default avatar
            return f'{CDN_ENDPOINT}/embed/avatars/0.png'
            
        return f'{CDN_ENDPOINT}/avatars/{webhook.id}/{avatar:0>32x}.png'
        
    def webhook_avatar_url_as(webhook,ext='png',size=None):
        avatar=webhook.avatar
        if not avatar:
            #default avatar
            return '{CDN_ENDPOINT}/embed/avatars/0.png'

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
        
        return f'{CDN_ENDPOINT}/avatars/{webhook.id}/{avatar:0>32x}.{ext}{end}'

    def invite_url(invite):
        return f'http://discord.gg/{invite.code}'

    def activity_asset_image_large_url(activity):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.png'

    def activity_asset_image_large_url_as(activity,ext='png',size=None):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.{ext}{end}'
        
    def activity_asset_image_small_url(activity):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.png'

    def activity_asset_image_small_url_as(activity,ext='png',size=None):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.png'

    def user_avatar_url(user):
        avatar=user.avatar
        if not avatar:
            return user.default_avatar.url
        
        if user.has_animated_avatar:
            start='a_'
            ext='gif'
        else:
            start=''
            ext='png'

        return f'{CDN_ENDPOINT}/avatars/{user.id}/{start}{avatar:0>32x}.{ext}'

    def user_avatar_url_as(user,ext=None,size=None):
        avatar=user.avatar
        if not avatar:
            return user.default_avatar.url

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if user.has_animated_avatar:
                start='a_'
                ext='gif'
            else:
                start=''
                ext='png'
        else:
            if user.has_animated_avatar:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
                start='a_'
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
                start=''

        return f'{CDN_ENDPOINT}/avatars/{user.id}/{start}{avatar:0>32x}.{ext}{end}'

    def default_avatar_url(default_avatar):
        return f'{CDN_ENDPOINT}/embed/avatars/{default_avatar.value}.png'

    def application_icon_url(application):
        icon=application.icon
        if not icon:
            return None
            
        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{icon:0>32x}.png'
        
    def application_icon_url_as(application,ext='png',size=None):
        icon=application.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{icon:0>32x}.{ext}{end}'

    def application_cover_url(application):
        cover=application.cover
        if not cover:
            return None
        
        return f'{CDN_ENDPOINT}/app-assets/{application.id}/store/{cover:0>32x}.png'
        
    def application_cover_url_as(application,ext='png',size=None):
        cover=application.cover
        if not cover:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
        
        return f'{CDN_ENDPOINT}/app-assets/{application.id}/store/{cover:0>32x}.{ext}{end}'
    
    def team_icon_url(team):
        icon=team.icon
        if not icon:
            return None
        
        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{icon:0>32x}.png'
        
    def team_icon_url_as(team,ext='png',size=None):
        icon=team.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{icon:0>32x}.{ext}{end}'

    def achievement_icon_url(achievement):
        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{achievement.icon:0>32x}.png'
    
    
    def achievement_icon_url_as(achievement,ext='png',size=None):
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{achievement.icon:0>32x}.{ext}{end}'

implement=sys.implementation
version_l=['Discordclient (HuyaneMatsu) Python (',implement.name,' ',str(implement.version[0]),'.',str(implement.version[1]),' ']
if implement.version[3]!='final':
    version_l.append(implement.version[3])
version_l.append(')')
LIB_USER_AGENT=''.join(version_l)

del implement
del version_l

del sys

class DiscordHTTPClient(HTTPClient):
    __slots__=('connector', 'cookie_jar', 'global_lock', 'header', 'locks',
        'loop', 'proxy_auth', 'proxy_url',)
    def __init__(self,client,proxy_url=None,proxy_auth=None):
        loop = client.loop
        HTTPClient.__init__(self,loop,proxy_url,proxy_auth)
        
        header=multidict_titled()
        header[USER_AGENT]=LIB_USER_AGENT
        header[AUTHORIZATION]=f'Bot {client.token}' if client.is_bot else client.token
        header[RATELIMIT_PRECISION]='millisecond'
        
        self.header     = header
        self.global_lock= None
        self.locks      = {}

    async def discord_request(self,handler,method,url,data=None,params=None,header=None,reason=None):
        if header is None:
            #normal request
            header=self.header.copy()

            if type(data) in (dict,list):
                header[CONTENT_TYPE]='application/json'
                data=to_json(data)

            if reason is not None:
                header[AUDIT_LOG_REASON]=quote(reason)
        else:
            #bearer or webhook request
            if type(data) in (dict,list) and CONTENT_TYPE not in header:
                header[CONTENT_TYPE]='application/json'
                data=to_json(data)
            
        #handling ratelimit
        if self.global_lock is not None:
            await self.global_lock

        if handler.group_id:
            try:
                old_handler=self.locks[handler]
            except KeyError:
                self.locks[handler]=handler
            else:
                self.locks[handler]=handler
                if old_handler.is_active():
                    await old_handler

        with handler:
            try_again=4
            while True:
                try:
                    async with Request_CM(self._request(method,url,header,data,params)) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if try_again:
                        #os cant handle more, need to wait for the blocking job to be done
                        await sleep(.5/try_again,self.loop)
                        #invalid adress causes OSError too, but we will let it run 5 times, then raise a ConnectionError
                        try_again-=1
                        continue
                    raise ConnectionError('Invalid adress or no connection with Discord') from err
                headers=response.headers
                status=response.status
                
                if headers[CONTENT_TYPE]=='application/json':
                    response_data=from_json(response_data)
                
                if 199<status<305:
                    if headers.get(RATELIMIT_REMAINING,'1')=='0':
                        handler.set_delay(headers)
                    return response_data
                
                if status==429:
                    retry_after=response_data['retry_after']/1000.
                    if response_data['global']:
                        await ratelimit_global(self,retry_after)
                    else:
                        await sleep(retry_after,self.loop)
                    continue
                
                if (status==500 or status==502) and try_again:
                    await sleep(10./try_again,self.loop)
                    try_again-=1
                    continue
                
                raise DiscordException(response,response_data)

    #client
    
    async def client_edit(self,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,59136),METH_PATCH,
            f'{API_ENDPOINT}/users/@me',data)

    async def client_edit_nick(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,48384),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick',data,reason=reason)

    async def client_user(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me')

    #hooman only
    async def client_get_settings(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/settings')
    
    #hooman only
    async def client_edit_settings(self,data):
        return self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/users/@me/settings',data=data)

    async def client_logout(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/auth/logout')

    async def guild_get_all(self,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,62720),METH_GET,
            f'{API_ENDPOINT}/users/@me/guilds',params=data)

    async def channel_private_get_all(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/channels')

    #hooman only
    async def client_gateway_hooman(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/gateway')

    #bot only
    async def client_gateway_bot(self):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,41216),METH_GET,
            f'{API_ENDPOINT}/gateway/bot')
    
    #bot only
    async def client_application_info(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/oauth2/applications/@me')

    async def client_connections(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/connections')

    #oauth2
    
    async def oauth2_token(self,data): #UNLIMITED
        header=multidict_titled()
        dict.__setitem__(header,CONTENT_TYPE,['application/x-www-form-urlencoded'])
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{DIS_ENDPOINT}/api/oauth2/token',data,header=header)
    
    async def user_info(self,header):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me',header=header)
    
    async def user_connections(self,header):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/connections',header=header)

    async def guild_user_add(self,guild_id,user_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,53760),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data)
        
    async def user_guilds(self,header):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,60928),METH_GET,
            f'{API_ENDPOINT}/users/@me/guilds',header=header)
    
    #channel
    async def channel_private_create(self,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/@me/channels',data)

    async def channel_group_create(self,user_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/{user_id}/channels',data)        

    async def channel_group_leave(self,channel_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}')

    async def channel_group_user_add(self,channel_id,user_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')

    async def channel_group_user_delete(self,channel_id,user_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')

    async def channel_group_edit(self,channel_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',data)
    
    async def channel_move(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',data,reason=reason)

    async def channel_edit(self,channel_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',data,reason=reason)

    async def channel_create(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',data,reason=reason)

    async def channel_delete(self,channel_id,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}',reason=reason)

    async def channel_follow(self,channel_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/followers',data)

    async def permission_ow_create(self,channel_id,overwrite_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',data,reason=reason)

    async def permission_ow_delete(self,channel_id,overwrite_id,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',reason=reason)

    #messages

    #hooman only
    async def message_mar(self,channel_id,message_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/ack',data)

    async def message_get(self,channel_id,message_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}')

    async def message_logs(self,channel_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',params=data)

    async def message_create(self,channel_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,28672),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',data)

    async def message_delete(self,channel_id,message_id,reason):
        try:
            result = await self.discord_request(ratelimit_handler(self.loop,channel_id,71680),METH_DELETE,
                f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',reason=reason)
            return result
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_message: # already deleted
                return
            raise
    
    # after 2 week else
    async def message_delete_b2wo(self,channel_id,message_id,reason):
        try:
            result = await self.discord_request(ratelimit_handler(self.loop,channel_id,87808),METH_DELETE,
                f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',reason=reason)
            return result
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_message: # already deleted
                return
            raise
    
    async def message_delete_multiple(self,channel_id,data,reason):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,30464),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk_delete',data,reason=reason)

    async def message_edit(self,channel_id,message_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,32256),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',data)

    async def message_suppress_embeds(self,channel_id,message_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,73472),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds',data)

    async def message_pin(self,channel_id,message_id):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,34048),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')

    async def message_unpin(self,channel_id,message_id):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,34048),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')

    async def channel_pins(self,channel_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,35840),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/pins')

    #typing
    
    async def typing(self,channel_id):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,37632),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/typing')

    #reactions

    async def reaction_add(self,channel_id,message_id,reaction):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,26880),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
            
    async def reaction_delete(self,channel_id,message_id,reaction,user_id):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}')

    async def reaction_delete_emoji(self,channel_id,message_id,reaction):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}')

    async def reaction_delete_own(self,channel_id,message_id,reaction):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')

    async def reaction_clear(self,channel_id,message_id):
        return await self.discord_request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions')

    async def reaction_users(self,channel_id,message_id,reaction,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',params=data)

    #guild
    
    async def guild_get(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}')

    async def guild_user_delete(self,guild_id,user_id,reason):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,50176),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',reason)

    async def guild_ban_add(self,guild_id,user_id,data,reason):
        if (reason is not None) and reason:
            data['reason']=quote(reason)
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',params=data)

    async def guild_ban_delete(self,guild_id,user_id,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',reason=reason)

    async def user_edit(self,guild_id,user_id,data,reason):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,51968),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data,reason=reason)

    #hooman only
    async def guild_mar(self,guild_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/ack',data)

    async def guild_leave(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/users/@me/guilds/{guild_id}')

    async def guild_delete(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}')

    async def guild_create(self,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds',data)

    async def guild_prune(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune',params=data,reason=reason)

    async def guild_prune_estimate(self,guild_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune',params=data)

    async def guild_edit(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}',data,reason=reason)

    async def guild_bans(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans')

    async def guild_ban_get(self,guild_id,user_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}')
    
    async def vanity_get(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url')

    async def vanity_edit(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url',data,reason=reason)

    async def audit_logs(self,guild_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs',params=data)

    async def user_role_add(self,guild_id,user_id,role_id,reason):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,55552),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',reason=reason)

    async def user_role_delete(self,guild_id,user_id,role_id,reason):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,55552),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',reason=reason)

    async def user_move(self,guild_id,user_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,51968),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data)

    async def integration_get_all(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations')

    async def integration_create(self,guild_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations',data)

    async def integration_edit(self,guild_id,integration_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}',data)

    async def integration_delete(self,guild_id,integration_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}')

    async def integration_sync(self,guild_id,integration_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}/sync')

    async def guild_embed_get(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed')

    async def guild_embed_edit(self,guild_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed',data)

    async def guild_widget_get(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/widget.json',header={})
    
    async def guild_users(self,guild_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,68096),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members',params=data)

    async def guild_regions(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/regions')

    async def guild_channels(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels')

    async def guild_roles(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles')

    #invite

    async def invite_create(self,channel_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,39424),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/invites',data)
    
    async def invite_get(self,invite_code,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,57344),METH_GET,
            f'{API_ENDPOINT}/invites/{invite_code}',params=data)

    async def invite_get_guild(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/invites')
    
    async def invite_get_channel(self,channel_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/invites')

    async def invite_delete(self,invite_code,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/invites/{invite_code}',reason=reason)


    #role

    async def role_edit(self,guild_id,role_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',data,reason=reason)

    async def role_delete(self,guild_id,role_id,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',reason=reason)

    async def role_create(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',data,reason=reason)

    async def role_move(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',data,reason=reason)

    #emoji

    async def emoji_get(self,guild_id,emoji_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}')

    async def guild_emojis(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis')
        
    async def emoji_edit(self,guild_id,emoji_id,data,reason):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,46592),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',data,reason=reason)

    async def emoji_create(self,guild_id,data,reason):
        return await self.discord_request(ratelimit_handler(self.loop,guild_id,43008),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis',data,reason=reason)

    async def emoji_delete(self,guild_id,emoji_id,reason):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,44800),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',reason=reason)

    #relations

    async def relationship_delete(self,user_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}')

    async def relationship_create(self,user_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}',data)

    async def relationship_friend_request(self,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/@me/relationships',data)

    #webhook
    
    async def webhook_create(self,channel_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks',data)

    async def webhook_get(self,webhook_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/webhooks/{webhook_id}')

    async def webhook_get_channel(self,channel_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks')

    async def webhook_get_guild(self,guild_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/webhooks')
    
    async def webhook_get_token(self,webhook):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            webhook.url,header={})
    
    async def webhook_delete_token(self,webhook):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            webhook.url,header={})

    async def webhook_delete(self,webhook_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/webhooks/{webhook_id}')

    async def webhook_edit_token(self,webhook,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            webhook.url,data,header={})

    async def webhook_edit(self,webhook_id,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/webhooks/{webhook_id}',data)

    async def webhook_send(self,webhook,data,wait):
        return await self.discord_request(ratelimit_handler(self.loop,webhook.id,66304),METH_POST,
            f'{webhook.url}?wait={wait:d}',data,header={})
    
    #user

    async def user_get(self,user_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,64512),METH_GET,
            f'{API_ENDPOINT}/users/{user_id}')

    async def guild_user_get(self,guild_id,user_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,69888),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}')
    
    #hooman only
    async def user_profile(self,user_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/{user_id}/profile')


    #hypesquad

    async def hypesquad_house_change(self,data):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/hypesquad/online',data)

    async def hypesquad_house_leave(self):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/hypesquad/online')

    #achievements
    
    async def achievement_get_all(self,application_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,75264),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements')

    async def achievement_get(self,application_id,achievement_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,77056),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')

    async def achievement_create(self,application_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,78848),METH_POST,
            f'{API_ENDPOINT}/applications/{application_id}/achievements',data)

    async def achievement_edit(self,application_id,achievement_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,80640),METH_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',data)

    async def achievement_delete(self,application_id,achievement_id):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,82432),METH_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')

    async def user_achievements(self,application_id,header):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,84224),METH_GET,
            f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements',header=header)
    
    async def user_achievement_update(self,user_id,application_id,achievement_id,data):
        return await self.discord_request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,86016),METH_PUT,
            f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}',data)

    #random
    
    #hooman only sadly, but this would be nice to be allowed, to get name and icon at least
    async def application_get(self,application_id):
        return await self.discord_request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}')

del re
del modulize
del Discord_hdrs
