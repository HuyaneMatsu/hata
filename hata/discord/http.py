﻿# -*- coding: utf-8 -*-
__all__ = ('DiscordHTTPClient', )

import sys, re

from ..backend.dereaddons_local import multidict_titled, modulize, WeakMap, WeakKeyDictionary
from ..backend.futures import sleep
from ..backend.http import HTTPClient, Request_CM
from ..backend.connector import TCPConnector
from ..backend.hdrs import METH_PATCH, METH_GET, METH_DELETE, METH_POST, METH_PUT, CONTENT_TYPE, USER_AGENT, \
    AUTHORIZATION
from ..backend.quote import quote

from .exceptions import DiscordException, ERROR_CODES
from .others import to_json, from_json, Discord_hdrs
from .ratelimit import ratelimit_global, RATELIMIT_GROUPS, RatelimitHandler, NO_SPECIFIC_RATELIMITER

AUDIT_LOG_REASON    = Discord_hdrs.AUDIT_LOG_REASON
RATELIMIT_PRECISION = Discord_hdrs.RATELIMIT_PRECISION



ChannelGuildBase = NotImplemented

@modulize
class URLS:
    VALID_ICON_FORMATS   = ('jpg','jpeg','png','webp')
    VALID_ICON_SIZES     = {1<<x for x in range(4,13)}
    VALID_ICON_FORMATS_EXTENDED = (*VALID_ICON_FORMATS,'gif',)
    
    API_ENDPOINT='https://discord.com/api/v7' #v7 includes special error messages
    CDN_ENDPOINT='https://cdn.discordapp.com'
    DIS_ENDPOINT='https://discord.com'
    
    from .bases import ICON_TYPE_NONE, ICON_TYPE_STATIC
    
    style_pattern=re.compile('(^shield$)|(^banner[1-4]$)')
    #returns a URL that allows the client to jump to this message
    #guild is guild's id, or @me if there is no guild
    def message_jump_url(message):
        """
        Returns a jump url to the message. If the message's channel is a partial guild channel, returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        channel = message.channel
        if isinstance(channel, ChannelGuildBase):
            guild = channel.guild
            if guild is None:
                return None
            guild_id = str(guild.id)
        else:
            guild_id = '@me'
        
        return f'{DIS_ENDPOINT}/channels/{guild_id}/{channel.id}/{message.id}'
    
    def guild_icon_url(guild):
        """
        Returns the guild's icon's image's url. If the guild has no icon, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = guild.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/icons/{guild.id}/{prefix}{guild.icon_hash:0>32x}.{ext}'
    
    def guild_icon_url_as(guild, ext='png', size=None):
        """
        Returns the guild's icon's url. If the guild has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the guild has
            animated icon, it can `'gif'` as well.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = guild.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/icons/{guild.id}/{prefix}{guild.icon_hash:0>32x}.{ext}{end}'
    
    def guild_invite_splash_url(guild):
        """
        Returns the guild's invite splashe's image's url. If the guild has no invite splash, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = guild.invite_splash_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/splashes/{guild.id}/{prefix}{guild.invite_splash_hash:0>32x}.{ext}'
    
    def guild_invite_splash_url_as(guild, ext='png', size=None):
        """
        Returns the guild's invite splashe's image's url. If the guild has no invite splash, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = guild.invite_splash_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/icons/{guild.id}/{prefix}{guild.invite_splash_hash:0>32x}.{ext}{end}'

    def guild_discovery_splash_url(guild):
        """
        Returns the guild's discovery splashe's image's url. If the guild has no disovery splash, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = guild.discovery_splash_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/discovery-splashes/{guild.id}/{prefix}{guild.discovery_splash_hash:0>32x}.{ext}'
    
    def guild_discovery_splash_url_as(guild, ext='png', size=None):
        """
        Returns the guild's discovery splashe's image's url. If the guild has no discovery splash, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = guild.discovery_splash_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/discovery-splashes/{guild.id}/{prefix}{guild.discovery_splash_hash:0>32x}.{ext}{end}'
    
    def guild_banner_url(guild):
        """
        Returns the guild's banner's image's url. If the guild has no banner, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = guild.banner_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/banners/{guild.id}/{prefix}{guild.banner_hash:0>32x}.{ext}'
    
    def guild_banner_url_as(guild, ext='png', size=None):
        """
        Returns the guild's banner's image's url. If the guild has no banner, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = guild.banner_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'

        return f'{CDN_ENDPOINT}/banners/{guild.id}/{prefix}{guild.banner_hash:0>32x}.{ext}{end}'
    
    def guild_embed_url(guild, style='shield'):
        """
        Returns the guild's embed image's url in `.png` format.
        
        Parameters
        ----------
        style : `str`
            The embed image's style. Can be any of: `'shield'`, `'banner1'`, `'banner2'`, `'banner3'`, `'banner4'`.
        
        Returns
        -------
        url : `str`
        
        Raises
        ------
        ValueError
            If `style` was not passed as any of the expected values.
        """
        if style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        
        return f'{API_ENDPOINT}/guilds/{guild.id}/embed.png?style={style}'
    
    def guild_widget_url(guild, style='shield'):
        """
        Returns the guild's widget image's url in `.png` format.
        
        Parameters
        ----------
        style : `str`
            The widget image's style. Can be any of: `'shield'`, `'banner1'`, `'banner2'`, `'banner3'`, `'banner4'`.
        
        Returns
        -------
        url : `str`
        
        Raises
        ------
        ValueError
            If `style` was not passed as any of the expected values.
        """
        if style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        
        return f'{API_ENDPOINT}/guilds/{guild.id}/widget.png?style={style}'
    
    def guild_widget_json_url(guild):
        """
        Returns an url to request a ``Guild``'s widget data.
        
        Returns
        -------
        url : `str`
        """
        return  f'{API_ENDPOINT}/guilds/{guild.id}/widget.json'

    def channel_group_icon_url(channel):
        """
        Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = channel.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{prefix}{channel.icon_hash:0>32x}.{ext}'
        
    def channel_group_icon_url_as(channel, ext='png', size=None):
        """
        Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = channel.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{prefix}{channel.icon_hash:0>32x}.{ext}{end}'
    
    def emoji_url(emoji):
        """
        Returns the emoji's image's url. If the emoji is unicode emoji, then returns `None` instead.
        
        Returns
        -------
        url : `str` or `None`
        """
        if emoji.is_unicode_emoji():
            return None
        
        if emoji.animated:
             ext = 'gif'
        else:
             ext = 'png'
            
        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}'

    def emoji_url_as(emoji, ext=None, size=None):
        """
        Returns the emoji's image's url. If the emoji is unicode emoji, then returns `None` instead.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If emoji is
            animated, it can `'gif'` as well.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        if emoji.is_unicode_emoji():
            return None

        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if emoji.animated:
                ext = 'gif'
            else:
                ext = 'png'
        else:
            if emoji.animated:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            else:
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
        
        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}{end}'
    
    def webhook_url(webhook):
        """
        Returns the webhook's url.
        
        Returns
        -------
        url : `str`
        """
        return f'{API_ENDPOINT}/webhooks/{webhook.id}/{webhook.token}'
    
    webhook_urlpattern=re.compile('(?:https://)?discord(?:app)?.com/api/(?:v\d/)?webhooks/([0-9]{17,21})/([a-zA-Z0-9\.\-\_%]{60,68})(?:/.*)?')
    
    def invite_url(invite):
        """
        Returns the invite's url.
        
        Returns
        -------
        url : `str`
        """
        return f'http://discord.gg/{invite.code}'
    
    def activity_asset_image_large_url(activity):
        """
        Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
        
        > Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).
        
        Returns
        -------
        url : `str` or `None`
        """
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.png'
    
    def activity_asset_image_large_url_as(activity, ext='png', size=None):
        """
        Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
        
        > Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.{ext}{end}'
        
    def activity_asset_image_small_url(activity):
        """
        Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
        
        > Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).
        
        Returns
        -------
        url : `str` or `None`
        """
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.png'

    def activity_asset_image_small_url_as(activity, ext='png', size=None):
        """
        Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
        
        > Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the image's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.{ext}{end}'
    
    def user_avatar_url(user):
        """
        Returns the user's avatar's url. If the user has no avatar, then returns it's default avatar's url.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = user.avatar_type
        if icon_type is ICON_TYPE_NONE:
            return user.default_avatar.url
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/avatars/{user.id}/{prefix}{user.avatar_hash:0>32x}.{ext}'
    
    def user_avatar_url_as(user, ext=None, size=None):
        """
        Returns the user's avatar's url. If the user has no avatar, then returns it's default avatar's url.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the user has
            animated avatar, it can `'gif'` as well.
        size : `int`, Optional.
            The preferred minimal size of the avatar's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = user.avatar_type
        if icon_type is ICON_TYPE_NONE:
            return user.default_avatar.url
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/avatars/{user.id}/{prefix}{user.avatar_hash:0>32x}.{ext}{end}'
    
    def default_avatar_url(default_avatar):
        """
        Returns the default avatar's url.
        
        Returns
        -------
        url : `str`
        """
        return f'{CDN_ENDPOINT}/embed/avatars/{default_avatar.value}.png'
    
    def application_icon_url(application):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = application.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{prefix}{application.icon_hash:0>32x}.{ext}'
    
    def application_icon_url_as(application, ext='png', size=None):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the icon's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = application.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'

        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{prefix}{application.icon_hash:0>32x}.{ext}{end}'
    
    def application_cover_url(application):
        """
        Returns the application's cover image's url. If the application has no cover image, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = application.cover_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/app-assets/{application.id}/store/{prefix}{application.cover_hash:0>32x}.{ext}'
        
    def application_cover_url_as(application, ext='png', size=None):
        """
        Returns the application's cover image's url. If the application has no cover image, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the cover's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the cover's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = application.cover_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/app-assets/{application.id}/store/{prefix}{application.cover_hash:0>32x}.{ext}{end}'
    
    def team_icon_url(team):
        """
        Returns the team's icon's url. If the team has no icon, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = team.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{prefix}{team.icon_hash:0>32x}.{ext}'
        
    def team_icon_url_as(team, ext='png', size=None):
        """
        Returns the team's icon's url. If the team has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the icon's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = team.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{prefix}{team.icon_hash:0>32x}.{ext}{end}'
    
    def achievement_icon_url(achievement):
        """
        Returns the achievement's icon's url.
        
        Returns
        -------
        url : `str` or `None`
        """
        icon_type = achievement.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
        
        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{prefix}{achievement.icon_hash:0>32x}.{ext}'
    
    def achievement_icon_url_as(achievement, ext='png', size=None):
        """
        Returns the achievement's icon's url.
        
        Parameters
        ----------
        ext : `str`, Optional
            The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        size : `int`, Optional.
            The preferred minimal size of the icon's url. Can be any of: `16`, `32`, `64`, `128`, `256`, `512`,
            `1024`, `2048`, `4096`.
        
        Returns
        -------
        url : `str` or `None`
        
        Raises
        ------
        ValueError
            If `ext` or `size` was not passed as any of the expected values.
        """
        icon_type = achievement.icon_type
        if icon_type is ICON_TYPE_NONE:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext is None:
            if icon_type is ICON_TYPE_STATIC:
                prefix = ''
                ext = 'png'
            else:
                prefix = 'a_'
                ext = 'gif'
        
        else:
            if icon_type is ICON_TYPE_STATIC:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
                prefix = ''
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
                prefix = 'a_'
        
        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{prefix}{achievement.icon_hash:0>32x}.{ext}{end}'


from .http.URLS import API_ENDPOINT, CDN_ENDPOINT, DIS_ENDPOINT

implement=sys.implementation
version_l=['Discordclient (HuyaneMatsu) Python (',implement.name,' ',str(implement.version[0]),'.',str(implement.version[1]),' ']
if implement.version[3]!='final':
    version_l.append(implement.version[3])
version_l.append(')')
LIB_USER_AGENT=''.join(version_l)

del implement
del version_l

del sys

class _ConnectorRefCounter(object):
    """
    Connector reference counter used by ``DiscordHTTPClient`` to limit the connector amount per loop to one.
    
    Attributes
    ----------
    connector : `TCPConnector`
        The connector of the connector counter.
    count : `int`
        The amount of active ``DiscordHTTPClient`` with the specified connector.
    """
    __slots__ = ('connector', 'count')
    def __init__(self, connector):
        """
        Creates a new connector referene counter with the given connector.
        
        Parameters
        ----------
        connector : `TCPConnector`
            The connector to use on the respective loop.
        """
        self.connector = connector
        self.count = 1

class DiscordHTTPClient(HTTPClient):
    """
    Http session for Discord clients. Implements low level access to Discord endpoints with their ratelimit and
    re-try handling, but it can aslo be used as a normal http session.
    
    Attributes
    ----------
    connector : `TCPConnector`
        TCP connector of the session. Each Discord Http client shares the same.
    cookie_jar : `CookieJar`
        Cookie storage of the session.
    global_lock : `None` or `Future`
        Waiter for Discord requests, set when the respective client gets limited globally.
    handlers : `WeakMap` of ``RatelimitHandler``
        Ratelimit handlers of the Discord requests.
    headers : `multidict_titled`
        Headers used by every every Discord request.
    loop : ``EventThread``
        The event loop of the http session.
    proxy_auth :  `str` or `None`
        Proxy authorization.
    proxy_url : `str` or `None`
        Proxy url.
        
    Class Attributes
    ----------------
    CONREFCOUNTS : `WeakKeyDictionary` of (`EventThread`, ``_ConnectorRefCounter``) items
        Container to store the connector(s) for Discord http clients. One connector is used by each Discord http client
        running on the same loop.
    """
    __slots__ = ('connector', 'cookie_jar', 'global_lock', 'handlers', 'headers', 'loop', 'proxy_auth', 'proxy_url',)
    
    CONREFCOUNTS = WeakKeyDictionary()
    
    def __init__(self, client, proxy_url=None, proxy_auth=None):
        """
        Creates a new Discord http client.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the session.
        proxy_auth :  `str`, Optional
            Proxy authorization for the session's requests.
        proxy_url : `str`, Optional
            Proxy url for the session's requests.
        """
        loop = client.loop
        
        try:
            connector_ref_counter = self.CONREFCOUNTS[loop]
        except KeyError:
            connector = TCPConnector(loop)
            connector_ref_counter = _ConnectorRefCounter(connector)
            self.CONREFCOUNTS[loop] = connector_ref_counter
        else:
            connector_ref_counter.count +=1
            connector = connector_ref_counter.connector
        
        HTTPClient.__init__(self, loop, proxy_url, proxy_auth, connector = connector)
        
        headers=multidict_titled()
        headers[USER_AGENT]=LIB_USER_AGENT
        headers[AUTHORIZATION]=f'Bot {client.token}' if client.is_bot else client.token
        headers[RATELIMIT_PRECISION]='millisecond'
        
        self.headers    = headers
        self.global_lock= None
        self.handlers   = WeakMap()
    
    __aenter__ = None
    __aexit__ = None
    
    async def close(self):
        """
        Closes the Discord http Client's connector.
        """
        self.__del__()
    
    def __del__(self):
        """Closes the Discord http Client's connector."""
        connector=self.connector
        if connector is None:
            return
        
        self.connector=None
        
        try:
            connector_ref_counter = self.CONREFCOUNTS[self.loop]
        except KeyError:
            pass
        else:
            connector_ref_counter.count = count = connector_ref_counter.count-1
            if count:
                return
            
            del self.CONREFCOUNTS[self.loop]
        
        if not connector.closed:
            connector.close()
    
    async def discord_request(self, handler, method, url, data=None, params=None, headers=None, reason=None):
        """
        Does a request towards Discord.
        
        Parameters
        ----------
        handler : ``RatelimitHandler``
            Ratlimit handler for the request.
        method : `str`
            The method of the request.
        url : `str`
            The url to request.
        data : `Any`, Optional
            Payload to request with.
        params : `Any`, Optional
            Query parameters.
        headers : `multidict_titled`, Optional
            Headers to do the request with. If passed then the session's own headers wont be used.
        reason : `str`, Optional
            Shows up at the request's respective guild if applicable.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        TypeError
            `data` or `params` type is bad, or they contain object(s) with bad type.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if headers is None:
            #normal request
            headers=self.headers.copy()
            
            if type(data) in (dict,list):
                headers[CONTENT_TYPE]='application/json'
                data=to_json(data)
            
            if reason is not None:
                headers[AUDIT_LOG_REASON]=quote(reason, safe='\ ')
        else:
            #bearer or webhook request
            if type(data) in (dict,list) and CONTENT_TYPE not in headers:
                headers[CONTENT_TYPE]='application/json'
                data=to_json(data)
        
        if handler.parent.group_id:
            handler = self.handlers.set(handler)
        
        try_again=4
        while True:
            global_lock = self.global_lock
            if (global_lock is not None):
                await global_lock
            
            await handler.enter()
            with handler.ctx() as lock:
                try:
                    async with Request_CM(self._request(method,url,headers,data,params)) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if not try_again:
                        raise ConnectionError('Invalid adress or no connection with Discord') from err
                    
                    #os cant handle more, need to wait for the blocking job to be done
                    await sleep(.5/try_again,self.loop)
                    #invalid adress causes OSError too, but we will let it run 5 times, then raise a ConnectionError
                    try_again-=1
                    continue
                
                response_headers=response.headers
                status=response.status
                
                if response_headers[CONTENT_TYPE]=='application/json':
                    response_data=from_json(response_data)
                
                if 199<status<305:
                    lock.exit(response_headers)
                    return response_data
                
                if status==429:
                    retry_after=response_data.get('retry_after',0)/1000.
                    if response_data.get('global',False):
                        await ratelimit_global(self,retry_after)
                    else:
                        await sleep(retry_after,self.loop)
                    continue
                
                if status in (500, 502, 503, ) and try_again:
                    await sleep(10./try_again,self.loop)
                    try_again-=1
                    continue
                
                lock.exit(response_headers)
                raise DiscordException(response,response_data)
    
    #client
    
    async def client_edit(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_edit, NO_SPECIFIC_RATELIMITER),
            METH_PATCH, f'{API_ENDPOINT}/users/@me',data)
    
    async def client_edit_nick(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_edit_nick, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick',data,reason=reason)
    
    async def client_user(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_user, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me')
    
    # hooman only
    async def client_get_settings(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_get_settings, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/settings')
    
    # hooman only
    async def client_edit_settings(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_edit_settings, NO_SPECIFIC_RATELIMITER),
            METH_PATCH, f'{API_ENDPOINT}/users/@me/settings', data)
    
    # hooman only
    async def client_logout(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_logout, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/auth/logout')
    
    async def guild_get_all(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_get_all, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/guilds', params=data)
    
    async def channel_private_get_all(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_private_get_all, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/channels')
    
    # hooman only
    async def client_gateway_hooman(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_gateway_hooman, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/gateway')
    
    # bot only
    async def client_gateway_bot(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_gateway_bot, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/gateway/bot')
    
    # bot only
    async def client_application_info(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_application_info, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/oauth2/applications/@me')
    
    async def client_connections(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.client_connections, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/connections')
    
    #oauth2
    
    async def oauth2_token(self, data, headers): #UNLIMITED
        headers[CONTENT_TYPE] = 'application/x-www-form-urlencoded'
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.oauth2_token, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{DIS_ENDPOINT}/api/oauth2/token', data, headers=headers)
    
    async def user_info(self,headers):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_info, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me', headers=headers)
    
    async def user_connections(self,headers):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_connections, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/connections', headers=headers)
    
    async def guild_user_add(self,guild_id,user_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_user_add, guild_id),
            METH_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', data)
    
    async def user_guilds(self,headers):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_guilds, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/guilds', headers=headers)
    
    #channel
    async def channel_private_create(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_private_create, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/users/@me/channels', data)
    
    async def channel_group_create(self,user_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_group_create, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/users/{user_id}/channels', data)
    
    async def channel_group_leave(self,channel_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_group_leave, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}')
    
    async def channel_group_user_add(self,channel_id,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_group_user_add, channel_id),
            METH_PUT, f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')
    
    async def channel_group_user_delete(self,channel_id,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_group_user_delete, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')
    
    async def channel_group_edit(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_group_edit, channel_id),
            METH_PATCH, f'{API_ENDPOINT}/channels/{channel_id}', data)
    
    async def channel_move(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_move, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/channels', data, reason=reason)
    
    async def channel_edit(self,channel_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_edit, channel_id),
            METH_PATCH, f'{API_ENDPOINT}/channels/{channel_id}', data, reason=reason)
    
    async def channel_create(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_create, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/channels', data, reason=reason)
    
    async def channel_delete(self,channel_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_delete, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}', reason=reason)
    
    async def channel_follow(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_follow, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/followers', data)
    
    async def permission_ow_create(self,channel_id,overwrite_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.permission_ow_create, channel_id),
            METH_PUT, f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}', data, reason=reason)
    
    async def permission_ow_delete(self,channel_id,overwrite_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.permission_ow_delete, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}', reason=reason)
    
    #messages
    
    #hooman only
    async def message_mar(self,channel_id,message_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_mar, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/ack',data)
    
    async def message_get(self,channel_id,message_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_get, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}')
    
    async def message_logs(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_logs, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages', params=data)
    
    async def message_create(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_create, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages', data)
    
    async def message_delete(self,channel_id,message_id,reason):
        try:
            result = await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_delete, channel_id),
                METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', reason=reason)
            return result
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_message: # already deleted
                return
            raise
    
    # after 2 week else
    async def message_delete_b2wo(self,channel_id,message_id,reason):
        try:
            result = await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_delete_b2wo, channel_id),
                METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', reason=reason)
            return result
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_message: # already deleted
                return
            raise
    
    async def message_delete_multiple(self,channel_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_delete_multiple, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk_delete', data, reason=reason)
    
    async def message_edit(self,channel_id,message_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_edit, channel_id),
            METH_PATCH, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', data)
    
    async def message_suppress_embeds(self,channel_id,message_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_suppress_embeds, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds',data)
    
    async def message_crosspost(self, channel_id, message_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_crosspost, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/crosspost')
    
    async def message_pin(self,channel_id,message_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_pin, channel_id),
            METH_PUT, f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')
    
    async def message_unpin(self,channel_id,message_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.message_unpin, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')
    
    async def channel_pins(self,channel_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.channel_pins, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/pins')
    
    #typing
    
    async def typing(self,channel_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.typing, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/typing')
    
    #reactions
    
    async def reaction_add(self,channel_id,message_id,reaction):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_add, channel_id),
            METH_PUT, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
    
    async def reaction_delete(self,channel_id,message_id,reaction,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_delete, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}')
    
    async def reaction_delete_emoji(self,channel_id,message_id,reaction):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_delete_emoji, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}')
    
    async def reaction_delete_own(self,channel_id,message_id,reaction):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_delete_own, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
    
    async def reaction_clear(self,channel_id,message_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_clear, channel_id),
            METH_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions')
    
    async def reaction_users(self,channel_id,message_id,reaction,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.reaction_users, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}', params=data)
    
    #guild
    
    async def guild_get(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}')
    
    async def guild_preview(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_preview, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/preview')
    
    async def guild_user_delete(self,guild_id,user_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_user_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',reason)
    
    async def guild_ban_add(self,guild_id,user_id,data,reason):
        if (reason is not None) and reason:
            data['reason']=quote(reason)
        
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_ban_add, guild_id),
            METH_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}', params=data)
    
    async def guild_ban_delete(self,guild_id,user_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_ban_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}', reason=reason)
    
    async def user_edit(self,guild_id,user_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', data, reason=reason)
    
    async def guild_discovery_get(self, guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_discovery_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata')
    
    async def guild_discovery_edit(self, guild_id, data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_discovery_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata', data)
    
    async def guild_discovery_add_subcategory(self, guild_id, category_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_discovery_add_subcategory, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')
    
    async def guild_discovery_delete_subcategory(self, guild_id, category_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_discovery_delete_subcategory, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')
    
    #hooman only
    async def guild_mar(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_mar, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/ack', data)
    
    async def guild_leave(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_leave, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/users/@me/guilds/{guild_id}')
    
    async def guild_delete(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}')
    
    async def guild_create(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_create, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/guilds', data)
    
    async def guild_prune(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_prune, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/prune', params=data, reason=reason)
    
    async def guild_prune_estimate(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_prune_estimate, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/prune',params=data)
    
    async def guild_edit(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}', data, reason=reason)
    
    async def guild_bans(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_bans, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/bans')
    
    async def guild_ban_get(self,guild_id,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_ban_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}')
    
    async def vanity_get(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.vanity_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url')
    
    async def vanity_edit(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.vanity_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url', data, reason=reason)
    
    async def audit_logs(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.audit_logs, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs', params=data)
    
    async def user_role_add(self,guild_id,user_id,role_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_role_add, guild_id),
            METH_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}', reason=reason)
    
    async def user_role_delete(self,guild_id,user_id,role_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_role_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}', reason=reason)
    
    async def user_move(self,guild_id,user_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_move, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data)
    
    async def integration_get_all(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.integration_get_all, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/integrations')
    
    async def integration_create(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.integration_create, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/integrations', data)
    
    async def integration_edit(self,guild_id,integration_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.integration_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}', data)
    
    async def integration_delete(self,guild_id,integration_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.integration_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}')
    
    async def integration_sync(self,guild_id,integration_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.integration_sync, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}/sync')
    
    async def guild_embed_get(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_embed_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/embed')
    
    async def guild_embed_edit(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_embed_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/embed',data)
    
    async def guild_widget_get(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_widget_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/widget.json', headers=multidict_titled())
    
    async def guild_users(self,guild_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_users, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members', params=data)
    
    async def guild_regions(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_regions, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/regions')
    
    async def guild_channels(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_channels, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/channels')
    
    async def guild_roles(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_roles, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/roles')
    
    #invite
    
    async def invite_create(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.invite_create, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/invites',data)
    
    async def invite_get(self,invite_code,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.invite_get, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/invites/{invite_code}',params=data)
    
    async def invite_get_guild(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.invite_get_guild, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/invites')
    
    async def invite_get_channel(self,channel_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.invite_get_channel, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/invites')
    
    async def invite_delete(self,invite_code,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.invite_delete, NO_SPECIFIC_RATELIMITER),
            METH_DELETE, f'{API_ENDPOINT}/invites/{invite_code}',reason=reason)
    
    
    #role
    
    async def role_edit(self,guild_id,role_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.role_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',data,reason=reason)
    
    async def role_delete(self,guild_id,role_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.role_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',reason=reason)
    
    async def role_create(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.role_create, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/roles', data, reason=reason)
    
    async def role_move(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.role_move, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/roles', data, reason=reason)
    
    #emoji
    
    async def emoji_get(self,guild_id,emoji_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.emoji_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}')
    
    async def guild_emojis(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_emojis, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/emojis')
    
    async def emoji_edit(self,guild_id,emoji_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.emoji_edit, guild_id),
            METH_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',data,reason=reason)
    
    async def emoji_create(self,guild_id,data,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.emoji_create, guild_id),
            METH_POST, f'{API_ENDPOINT}/guilds/{guild_id}/emojis',data,reason=reason)
    
    async def emoji_delete(self,guild_id,emoji_id,reason):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.emoji_delete, guild_id),
            METH_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',reason=reason)
    
    #relations
    
    async def relationship_delete(self,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.relationship_delete, NO_SPECIFIC_RATELIMITER),
            METH_DELETE, f'{API_ENDPOINT}/users/@me/relationships/{user_id}')
    
    async def relationship_create(self,user_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.relationship_create, NO_SPECIFIC_RATELIMITER),
            METH_PUT, f'{API_ENDPOINT}/users/@me/relationships/{user_id}',data)
    
    async def relationship_friend_request(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.relationship_friend_request, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/users/@me/relationships',data)
    
    #webhook
    
    async def webhook_create(self,channel_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_create, channel_id),
            METH_POST, f'{API_ENDPOINT}/channels/{channel_id}/webhooks',data)
    
    async def webhook_get(self,webhook_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_get, webhook_id),
            METH_GET, f'{API_ENDPOINT}/webhooks/{webhook_id}')
    
    async def webhook_get_channel(self,channel_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_get_channel, channel_id),
            METH_GET, f'{API_ENDPOINT}/channels/{channel_id}/webhooks')
    
    async def webhook_get_guild(self,guild_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_get_guild, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/webhooks')
    
    async def webhook_get_token(self,webhook):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_get_token, webhook.id),
            METH_GET, webhook.url, headers=multidict_titled())
    
    async def webhook_delete_token(self,webhook):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_delete_token, webhook.id),
            METH_DELETE, webhook.url, headers=multidict_titled())
    
    async def webhook_delete(self,webhook_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_delete, webhook_id),
            METH_DELETE, f'{API_ENDPOINT}/webhooks/{webhook_id}')
    
    async def webhook_edit_token(self,webhook,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_edit_token, webhook.id),
            METH_PATCH, webhook.url, data, headers=multidict_titled())
    
    async def webhook_edit(self,webhook_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_edit, webhook_id),
            METH_PATCH, f'{API_ENDPOINT}/webhooks/{webhook_id}',data)
    
    async def webhook_send(self,webhook,data,wait):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.webhook_send, webhook.id),
            METH_POST, f'{webhook.url}?wait={wait:d}', data, headers=multidict_titled())
    
    #user
    
    async def user_get(self,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_get, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/{user_id}')
    
    async def guild_user_get(self,guild_id,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_user_get, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}')
    
    async def guild_user_search(self, guild_id, data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.guild_user_search, guild_id),
            METH_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members/search', params=data)
    
    #hooman only
    async def user_get_profile(self,user_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_get_profile, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/{user_id}/profile')
    
    #hypesquad
    
    async def hypesquad_house_change(self,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.hypesquad_house_change, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/hypesquad/online',data)
    
    async def hypesquad_house_leave(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.hypesquad_house_leave, NO_SPECIFIC_RATELIMITER),
            METH_DELETE, f'{API_ENDPOINT}/hypesquad/online')

    #achievements
    
    async def achievement_get_all(self,application_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.achievement_get_all, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/applications/{application_id}/achievements')
    
    async def achievement_get(self,application_id,achievement_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.achievement_get, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')
    
    async def achievement_create(self,application_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.achievement_create, NO_SPECIFIC_RATELIMITER),
            METH_POST, f'{API_ENDPOINT}/applications/{application_id}/achievements',data)
    
    async def achievement_edit(self,application_id,achievement_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.achievement_edit, NO_SPECIFIC_RATELIMITER),
            METH_PATCH, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}', data)
    
    async def achievement_delete(self,application_id,achievement_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.achievement_delete, NO_SPECIFIC_RATELIMITER),
            METH_DELETE, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')
    
    async def user_achievements(self,application_id,headers):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_achievements, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements', headers=headers)
    
    async def user_achievement_update(self,user_id,application_id,achievement_id,data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.user_achievement_update, NO_SPECIFIC_RATELIMITER),
            METH_PUT, f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}', data)
    
    #random
    
    #hooman only sadly, but this would be nice to be allowed, to get name and icon at least
    async def application_get(self, application_id):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.application_get, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/applications/{application_id}')
    
    async def discovery_categories(self):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.discovery_categories, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/discovery/categories')
    
    async def discovery_validate_term(self, data):
        return await self.discord_request(RatelimitHandler(RATELIMIT_GROUPS.discovery_validate_term, NO_SPECIFIC_RATELIMITER),
            METH_GET, f'{API_ENDPOINT}/discovery/valid-term', params=data)

del re
del modulize
del Discord_hdrs
