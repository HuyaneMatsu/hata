# -*- coding: utf-8 -*-
__all__ = ('DiscordHTTPClient', )

import sys, re

from ..backend.utils import imultidict, modulize, WeakMap, WeakKeyDictionary
from ..backend.futures import sleep
from ..backend.http import HTTPClient, RequestCM
from ..backend.connector import TCPConnector
from ..backend.headers import METHOD_PATCH, METHOD_GET, METHOD_DELETE, METHOD_POST, METHOD_PUT, CONTENT_TYPE, USER_AGENT, \
    AUTHORIZATION
from ..backend.quote import quote

from .. env import API_VERSION

from .exceptions import DiscordException
from .utils import to_json, from_json
from .utils.DISCORD_HEADERS import AUDIT_LOG_REASON, RATE_LIMIT_PRECISION
from .rate_limit import rate_limit_global, RATE_LIMIT_GROUPS, RateLimitHandler, NO_SPECIFIC_RATE_LIMITER, \
    StackedStaticRateLimitHandler


@modulize
class URLS:
    ChannelGuildBase = NotImplemented
    
    VALID_ICON_FORMATS = ('jpg', 'jpeg','png','webp')
    VALID_ICON_SIZES = {1<<x for x in range(4,13)}
    VALID_ICON_FORMATS_EXTENDED = (*VALID_ICON_FORMATS, 'gif',)
    
    from ..env import CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DIS_ENDPOINT, API_VERSION
    
    API_ENDPOINT = f'https://discord.com/api/v{API_VERSION}' if (CUSTOM_API_ENDPOINT is None) else CUSTOM_API_ENDPOINT
    CDN_ENDPOINT = 'https://cdn.discordapp.com' if (CUSTOM_CDN_ENDPOINT is None) else CUSTOM_CDN_ENDPOINT
    DIS_ENDPOINT = 'https://discord.com' if (CUSTOM_DIS_ENDPOINT is None) else CUSTOM_DIS_ENDPOINT
    
    del CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DIS_ENDPOINT, API_VERSION
    
    from .bases import ICON_TYPE_NONE, ICON_TYPE_STATIC
    
    STYLE_PATTERN = re.compile('(^shield$)|(^banner[1-4]$)')
    
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
    
    MESSAGE_JUMP_URL_RP = re.compile(
        '(?:https://)?discord(?:app)?.com/channels/(?:(\d{7,21})|@me)/(\d{7,21})/(\d{7,21})'
            )
    
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
        Returns the guild's invite splash's image's url. If the guild has no invite splash, then returns `None`.
        
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
        Returns the guild's invite splash's image's url. If the guild has no invite splash, then returns `None`.
        
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
        
        return f'{CDN_ENDPOINT}/splashes/{guild.id}/{prefix}{guild.invite_splash_hash:0>32x}.{ext}{end}'

    def guild_discovery_splash_url(guild):
        """
        Returns the guild's discovery splash's image's url. If the guild has no discovery splash, then returns `None`.
        
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
        Returns the guild's discovery splash's image's url. If the guild has no discovery splash, then returns `None`.
        
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
        if STYLE_PATTERN.match(style) is None:
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
    
    WEBHOOK_URL_PATTERN = re.compile(
        '(?:https://)?discord(?:app)?.com/api/(?:v\d/)?webhooks/([0-9]{17,21})/([a-zA-Z0-9\.\-\_%]{60,68})(?:/.*)?'
            )
    
    def invite_url(invite):
        """
        Returns the invite's url.
        
        Returns
        -------
        url : `str`
        """
        return f'http://discord.gg/{invite.code}'
    
    INVITE_URL_PATTERN = re.compile('(?:https?://)?discord(?:\.gg|(?:app)?\.com/invite)/([a-zA-Z0-9-]+)')
    
    def activity_asset_image_large_url(activity):
        """
        Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        application_id = activity.application_id
        if not application_id:
            return None
        
        assets = activity.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.png'
    
    def activity_asset_image_large_url_as(activity, ext='png', size=None):
        """
        Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.

        
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
        application_id = activity.application_id
        if not application_id:
            return None

        assets = activity.assets
        if assets is None:
            return None
        
        image_large = assets.image_large
        if image_large is None:
            return None

        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.{ext}{end}'
        
    def activity_asset_image_small_url(activity):
        """
        Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
        
        Returns
        -------
        url : `str` or `None`
        """
        application_id = activity.application_id
        if not application_id:
            return None
        
        assets = activity.assets
        if assets is None:
            return None
        
        image_small = assets.image_small
        if image_small is None:
            return None
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.png'

    def activity_asset_image_small_url_as(activity, ext='png', size=None):
        """
        Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
        
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
        application_id = activity.application_id
        if not application_id:
            return None
        
        assets = activity.assets
        if assets is None:
            return None
        
        image_small = assets.image_small
        if image_small is None:
            return None
        
        if size is None:
            end = ''
        elif size in VALID_ICON_SIZES:
            end = f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096, got {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.{ext}{end}'
    
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
version_l=['Discord-client (HuyaneMatsu) Python (',implement.name,' ',str(implement.version[0]),'.',str(implement.version[1]),' ']
if implement.version[3] != 'final':
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
        Creates a new connector reference counter with the given connector.
        
        Parameters
        ----------
        connector : `TCPConnector`
            The connector to use on the respective loop.
        """
        self.connector = connector
        self.count = 1

class DiscordHTTPClient(HTTPClient):
    """
    Http session for Discord clients. Implements low level access to Discord endpoints with their rate limit and
    re-try handling, but it can also be used as a normal http session.
    
    Attributes
    ----------
    connector : ``TCPConnector``
        TCP connector of the session. Each Discord Http client shares the same.
    cookie_jar : ``CookieJar``
        Cookie storage of the session.
    global_lock : `None` or ``Future``
        Waiter for Discord requests, set when the respective client gets limited globally.
    handlers : ``WeakMap`` of ``RateLimitHandler``
        Rate limit handlers of the Discord requests.
    headers : `imultidict`
        Headers used by every every Discord request.
    loop : ``EventThread``
        The event loop of the http session.
    proxy_auth :  `str` or `None`
        Proxy authorization.
    proxy_url : `str` or `None`
        Proxy url.
        
    Class Attributes
    ----------------
    CONNECTOR_REFERENCE_COUNTS : ``WeakKeyDictionary`` of (``EventThread``, ``_ConnectorRefCounter``) items
        Container to store the connector(s) for Discord http clients. One connector is used by each Discord http client
        running on the same loop.
    """
    __slots__ = ('connector', 'cookie_jar', 'global_lock', 'handlers', 'headers', 'loop', 'proxy_auth', 'proxy_url',)
    
    CONNECTOR_REFERENCE_COUNTS = WeakKeyDictionary()
    
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
            connector_ref_counter = self.CONNECTOR_REFERENCE_COUNTS[loop]
        except KeyError:
            connector = TCPConnector(loop)
            connector_ref_counter = _ConnectorRefCounter(connector)
            self.CONNECTOR_REFERENCE_COUNTS[loop] = connector_ref_counter
        else:
            connector_ref_counter.count +=1
            connector = connector_ref_counter.connector
        
        HTTPClient.__init__(self, loop, proxy_url, proxy_auth, connector = connector)
        
        headers = imultidict()
        headers[USER_AGENT] = LIB_USER_AGENT
        headers[AUTHORIZATION] = f'Bot {client.token}' if client.is_bot else client.token
        
        if API_VERSION in (6, 7):
            headers[RATE_LIMIT_PRECISION] = 'millisecond'
        
        self.headers = headers
        self.global_lock = None
        self.handlers = WeakMap()
    
    __aenter__ = None
    __aexit__ = None
    
    async def close(self):
        """
        Closes the Discord http Client's connector.
        
        This method is a coroutine.
        """
        self.__del__()
    
    def __del__(self):
        """Closes the Discord http Client's connector."""
        connector = self.connector
        if connector is None:
            return
        
        self.connector = None
        
        try:
            connector_ref_counter = self.CONNECTOR_REFERENCE_COUNTS[self.loop]
        except KeyError:
            pass
        else:
            connector_ref_counter.count = count = connector_ref_counter.count-1
            if count:
                return
            
            del self.CONNECTOR_REFERENCE_COUNTS[self.loop]
        
        if not connector.closed:
            connector.close()
    
    async def discord_request(self, handler, method, url, data=None, params=None, headers=None, reason=None):
        """
        Does a request towards Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        handler : ``RateLimitHandler`` or ``StackedStaticRateLimitHandler``
            rate limit handler for the request.
        method : `str`
            The method of the request.
        url : `str`
            The url to request.
        data : `Any`, Optional
            Payload to request with.
        params : `Any`, Optional
            Query parameters.
        headers : `imultidict`, Optional
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
            headers = self.headers.copy()
            
            if type(data) in (dict, list):
                headers[CONTENT_TYPE] = 'application/json'
                data = to_json(data)
            
            if reason is not None:
                headers[AUDIT_LOG_REASON] = quote(reason, safe='\ ')
        else:
            #bearer or webhook request
            if type(data) in (dict, list) and CONTENT_TYPE not in headers:
                headers[CONTENT_TYPE] = 'application/json'
                data = to_json(data)
        
        if not handler.is_unlimited():
            handler = self.handlers.set(handler)
        
        try_again = 4
        while True:
            global_lock = self.global_lock
            if (global_lock is not None):
                await global_lock
            
            await handler.enter()
            with handler.ctx() as lock:
                try:
                    async with RequestCM(self._request(method, url, headers, data, params)) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if not try_again:
                        raise ConnectionError('Invalid address or no connection with Discord.') from err
                    
                    # os cant handle more, need to wait for the blocking job to be done
                    await sleep(0.5/try_again, self.loop)
                    #invalid address causes OSError too, but we will let it run 5 times, then raise a ConnectionError
                    try_again -= 1
                    continue
                
                response_headers = response.headers
                status = response.status
                
                if response_headers[CONTENT_TYPE] == 'application/json':
                    response_data = from_json(response_data)
                
                if 199 < status < 305:
                    lock.exit(response_headers)
                    return response_data
                
                if status == 429:
                    if 'code' in response_data: # Can happen at the case of rate limit ban
                        raise DiscordException(response, response_data)
                    
                    retry_after = response_data.get('retry_after', 0)/1000.
                    if response_data.get('global', False):
                        await rate_limit_global(self, retry_after)
                    else:
                        await sleep(retry_after, self.loop)
                    continue
                
                if status in (500, 502, 503) and try_again:
                    await sleep(10./try_again, self.loop)
                    try_again -= 1
                    continue
                
                lock.exit(response_headers)
                raise DiscordException(response, response_data)
    
    #client
    
    async def client_edit(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH, f'{API_ENDPOINT}/users/@me', data)
    
    async def client_edit_nick(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_edit_nick, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick', data, reason=reason)
    
    async def client_user_get(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_user_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me')
    
    # hooman only
    async def client_settings_get(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_settings_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/settings')
    
    # hooman only
    async def client_settings_edit(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_settings_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH, f'{API_ENDPOINT}/users/@me/settings', data)
    
    # hooman only
    async def client_logout(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_logout, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/auth/logout')
    
    async def guild_get_all(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/guilds', params=data)
    
    async def channel_private_get_all(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_private_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/channels')
    
    # hooman only
    async def client_gateway_hooman(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_gateway_hooman, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/gateway')
    
    # bot only
    async def client_gateway_bot(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_gateway_bot, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/gateway/bot')
    
    # bot only
    async def client_application_get(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_application_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/oauth2/applications/@me')
    
    async def client_connection_get_all(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.client_connection_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/connections')
    
    # oauth2
    
    async def oauth2_token(self, data, headers): #UNLIMITED
        headers[CONTENT_TYPE] = 'application/x-www-form-urlencoded'
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.oauth2_token, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{DIS_ENDPOINT}/api/oauth2/token', data, headers=headers)
    
    async def user_info_get(self, headers):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_info_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me', headers=headers)
    
    async def user_connection_get_all(self, headers):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_connection_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/connections', headers=headers)
    
    async def guild_user_add(self, guild_id, user_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_add, guild_id),
            METHOD_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', data)
    
    async def user_guild_get_all(self, headers):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/guilds', headers=headers)
    
    #channel
    async def channel_private_create(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_private_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/users/@me/channels', data)
    
    async def channel_group_create(self, user_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/users/{user_id}/channels', data)
    
    async def channel_group_leave(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_leave, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}')
    
    async def channel_group_user_get_all(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_add, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/recipients')
    
    async def channel_group_user_add(self, channel_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_add, channel_id),
            METHOD_PUT, f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')
    
    async def channel_group_user_delete(self, channel_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')
    
    async def channel_group_edit(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_edit, channel_id),
            METHOD_PATCH, f'{API_ENDPOINT}/channels/{channel_id}', data)
    
    async def channel_move(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_move, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/channels', data, reason=reason)
    
    async def channel_edit(self, channel_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_edit, channel_id),
            METHOD_PATCH, f'{API_ENDPOINT}/channels/{channel_id}', data, reason=reason)
    
    async def channel_create(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_create, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/channels', data, reason=reason)
    
    async def channel_delete(self, channel_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}', reason=reason)
    
    async def channel_follow(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_follow, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/followers', data)
    
    async def permission_overwrite_create(self, channel_id, overwrite_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.permission_overwrite_create, channel_id),
            METHOD_PUT, f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}', data, reason=reason)
    
    async def permission_overwrite_delete(self, channel_id, overwrite_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.permission_overwrite_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}', reason=reason)
    
    #messages
    
    #hooman only
    async def message_ack(self, channel_id, message_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_ack, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/ack', data)
    
    async def message_get(self, channel_id, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_get, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}')
    
    async def message_get_chunk(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_get_chunk, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages', params=data)
    
    async def message_create(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_create, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages', data)
    
    async def message_delete(self, channel_id, message_id, reason):
        return await self.discord_request(
            StackedStaticRateLimitHandler(RATE_LIMIT_GROUPS.static_message_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', reason=reason)
    
    # after 2 week else & not own
    async def message_delete_b2wo(self, channel_id, message_id, reason):
        return await self.discord_request(
            StackedStaticRateLimitHandler(RATE_LIMIT_GROUPS.static_message_delete_b2wo, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', reason=reason)
    
    async def message_delete_multiple(self, channel_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_delete_multiple, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk-delete', data, reason=reason)
    
    async def message_edit(self, channel_id, message_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_edit, channel_id),
            METHOD_PATCH, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}', data)
    
    async def message_suppress_embeds(self, channel_id, message_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_suppress_embeds, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds', data)
    
    async def message_crosspost(self, channel_id, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_crosspost, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/crosspost')
    
    async def message_pin(self, channel_id, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_pin, channel_id),
            METHOD_PUT, f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')
    
    async def message_unpin(self, channel_id, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.message_unpin, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')
    
    async def channel_pin_get_all(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_pin_get_all, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/pins')
    
    # hooman only
    async def channel_pin_ack(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.channel_pin_ack, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/pins/ack')
    
    #typing
    
    async def typing(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.typing, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/typing')
    
    #reactions
    
    async def reaction_add(self, channel_id, message_id, reaction):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_add, channel_id),
            METHOD_PUT, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
    
    async def reaction_delete(self, channel_id, message_id, reaction, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}')
    
    async def reaction_delete_emoji(self, channel_id, message_id, reaction):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete_emoji, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}')
    
    async def reaction_delete_own(self, channel_id, message_id, reaction):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete_own, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
    
    async def reaction_clear(self, channel_id, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_clear, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions')
    
    async def reaction_user_get_chunk(self, channel_id, message_id, reaction, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.reaction_user_get_chunk, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}', params=data)
    
    #guild
    
    async def guild_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}')
    
    async def guild_preview_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_preview_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/preview')
    
    async def guild_user_delete(self, guild_id, user_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', reason)
    
    async def guild_ban_add(self, guild_id, user_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_add, guild_id),
            METHOD_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}', data, reason=reason)
    
    async def guild_ban_delete(self, guild_id, user_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}', reason=reason)
    
    async def user_edit(self, guild_id, user_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', data, reason=reason)
    
    async def guild_discovery_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata')
    
    async def guild_discovery_edit(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata', data)
    
    async def guild_discovery_add_subcategory(self, guild_id, category_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_add_subcategory, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')
    
    async def guild_discovery_delete_subcategory(self, guild_id, category_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_delete_subcategory, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')
    
    #hooman only
    async def guild_ack(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_ack, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/ack', data)
    
    async def guild_leave(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_leave, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/users/@me/guilds/{guild_id}')
    
    async def guild_delete(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}')
    
    async def guild_create(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/guilds', data)
    
    async def guild_prune(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_prune, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/prune', params=data, reason=reason)
    
    async def guild_prune_estimate(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_prune_estimate, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/prune', params=data)
    
    async def guild_edit(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}', data, reason=reason)
    
    async def guild_ban_get_all(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/bans')
    
    async def guild_ban_get(self, guild_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}')
    
    async def vanity_invite_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.vanity_invite_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url')
    
    async def vanity_invite_edit(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.vanity_invite_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url', data, reason=reason)
    
    async def audit_log_get_chunk(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.audit_log_get_chunk, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs', params=data)
    
    async def user_role_add(self, guild_id, user_id, role_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_role_add, guild_id),
            METHOD_PUT, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}', reason=reason)
    
    async def user_role_delete(self, guild_id, user_id, role_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_role_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}', reason=reason)
    
    async def user_move(self, guild_id, user_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_move, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}', data)
    
    async def integration_get_all(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.integration_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/integrations', params=data)
    
    async def integration_create(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.integration_create, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/integrations', data)
    
    async def integration_edit(self, guild_id, integration_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.integration_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}', data)
    
    async def integration_delete(self, guild_id, integration_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.integration_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}')
    
    async def integration_sync(self, guild_id, integration_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.integration_sync, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}/sync')
    
    async def guild_embed_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_embed_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/embed')
    
    async def guild_embed_edit(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_embed_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/embed', data)
    
    async def guild_widget_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_widget_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/widget.json', headers=imultidict())
    
    async def guild_user_get_chunk(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_get_chunk, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members', params=data)
    
    async def guild_voice_region_get_all(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_voice_region_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/regions')
    
    async def guild_channel_get_all(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_channel_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/channels')
    
    async def guild_role_get_all(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_role_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/roles')
    
    async def welcome_screen_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.welcome_screen_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen')
    
    async def welcome_screen_edit(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.welcome_screen_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen', data)
    
    async def verification_screen_get(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.verification_screen_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/member-verification')
    
    async def verification_screen_edit(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.verification_screen_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/member-verification', data)
    
    # Invite
    
    async def invite_create(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.invite_create, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/invites', data)
    
    async def invite_get(self,invite_code, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.invite_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/invites/{invite_code}',params=data)
    
    async def invite_get_all_guild(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.invite_get_all_guild, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/invites')
    
    async def invite_get_all_channel(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.invite_get_all_channel, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/invites')
    
    async def invite_delete(self,invite_code, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.invite_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/invites/{invite_code}', reason=reason)
    
    
    #role
    async def role_edit(self, guild_id, role_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.role_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}', data, reason=reason)
    
    async def role_delete(self, guild_id, role_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.role_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}', reason=reason)
    
    async def role_create(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.role_create, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/roles', data, reason=reason)
    
    async def role_move(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.role_move, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/roles', data, reason=reason)
    
    # emoji
    
    async def emoji_get(self, guild_id, emoji_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.emoji_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}')
    
    async def guild_emoji_get_all(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_emoji_get_all, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/emojis')
    
    async def emoji_edit(self, guild_id, emoji_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.emoji_edit, guild_id),
            METHOD_PATCH, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}', data, reason=reason)
    
    async def emoji_create(self, guild_id, data, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.emoji_create, guild_id),
            METHOD_POST, f'{API_ENDPOINT}/guilds/{guild_id}/emojis', data, reason=reason)
    
    async def emoji_delete(self, guild_id, emoji_id, reason):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.emoji_delete, guild_id),
            METHOD_DELETE, f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}', reason=reason)
    
    # relations
    
    async def relationship_delete(self, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.relationship_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/users/@me/relationships/{user_id}')
    
    async def relationship_create(self, user_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.relationship_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT, f'{API_ENDPOINT}/users/@me/relationships/{user_id}', data)
    
    async def relationship_friend_request(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.relationship_friend_request, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/users/@me/relationships', data)
    
    # webhook
    
    async def webhook_create(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_create, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/webhooks', data)
    
    async def webhook_get(self, webhook_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get, webhook_id),
            METHOD_GET, f'{API_ENDPOINT}/webhooks/{webhook_id}')
    
    async def webhook_get_all_channel(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_all_channel, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/webhooks')
    
    async def webhook_get_all_guild(self, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_all_guild, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/webhooks')
    
    async def webhook_get_token(self, webhook):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_token, webhook.id),
            METHOD_GET, webhook.url, headers=imultidict())
    
    async def webhook_delete_token(self, webhook):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_delete_token, webhook.id),
            METHOD_DELETE, webhook.url, headers=imultidict())
    
    async def webhook_delete(self, webhook_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_delete, webhook_id),
            METHOD_DELETE, f'{API_ENDPOINT}/webhooks/{webhook_id}')
    
    async def webhook_edit_token(self, webhook, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_edit_token, webhook.id),
            METHOD_PATCH, webhook.url, data, headers=imultidict())
    
    async def webhook_edit(self, webhook_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_edit, webhook_id),
            METHOD_PATCH, f'{API_ENDPOINT}/webhooks/{webhook_id}', data)
    
    async def webhook_message_create(self, webhook, data, wait):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_create, webhook.id),
            METHOD_POST, f'{webhook.url}?wait={wait:d}', data, headers=imultidict())
    
    async def webhook_message_edit(self, webhook, message_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_edit, webhook.id),
            METHOD_PATCH, f'{webhook.url}/messages/{message_id}', data, headers=imultidict())
    
    async def webhook_message_delete(self, webhook, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_edit, webhook.id),
            METHOD_DELETE, f'{webhook.url}/messages/{message_id}', headers=imultidict())
    
    # user
    
    async def user_get(self, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/{user_id}')
    
    async def guild_user_get(self, guild_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_get, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}')
    
    async def guild_user_search(self, guild_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_search, guild_id),
            METHOD_GET, f'{API_ENDPOINT}/guilds/{guild_id}/members/search', params=data)
    
    #hooman only
    async def user_get_profile(self, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_get_profile, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/{user_id}/profile')
    
    #hypesquad
    
    async def hypesquad_house_change(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.hypesquad_house_change, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/hypesquad/online', data)
    
    async def hypesquad_house_leave(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.hypesquad_house_leave, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/hypesquad/online')
    
    #achievements
    
    async def achievement_get_all(self, application_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.achievement_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/{application_id}/achievements')
    
    async def achievement_get(self, application_id, achievement_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.achievement_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')
    
    async def achievement_create(self, application_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.achievement_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/applications/{application_id}/achievements', data)
    
    async def achievement_edit(self, application_id, achievement_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.achievement_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}', data)
    
    async def achievement_delete(self, application_id, achievement_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.achievement_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')
    
    async def user_achievement_get_all(self, application_id, headers):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_achievement_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements', headers=headers)
    
    async def user_achievement_update(self, user_id, application_id, achievement_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.user_achievement_update, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT, f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}', data)
    
    #random
    
    #hooman only sadly, but this would be nice to be allowed, to get name and icon at least
    async def application_get(self, application_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/{application_id}')
    
    async def application_get_all_detectable(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_get_all_detectable, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/detectable')
    
    async def eula_get(self, eula_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.eula_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/store/eulas/{eula_id}')
    
    async def discovery_category_get_all(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.discovery_category_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/discovery/categories')
    
    async def discovery_validate_term(self, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.discovery_validate_term, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/discovery/valid-term', params=data)
    
    #hooman only
    async def bulk_ack(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.bulk_ack, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/read-states/ack-bulk',)
    
    async def voice_region_get_all(self):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.voice_region_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/voice/regions',)
    
    # thread
    
    # DiscordException Forbidden (403), code=20001: Bots cannot use this endpoint
    async def thread_create(self, channel_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.thread_create, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/threads', data)
    
    # DiscordException Not Found (404): 404: Not Found
    async def thread_user_get_all(self, channel_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_get_all, channel_id),
            METHOD_GET, f'{API_ENDPOINT}/channels/{channel_id}/threads/participants')
    
    # DiscordException Not Found (404): 404: Not Found
    async def thread_user_delete(self, channel_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_delete, channel_id),
            METHOD_DELETE, f'{API_ENDPOINT}/channels/{channel_id}/threads/participants/{user_id}')
    
    # DiscordException Not Found (404): 404: Not Found
    async def thread_user_add(self, channel_id, user_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_add, channel_id),
            METHOD_POST, f'{API_ENDPOINT}/channels/{channel_id}/threads/participants/{user_id}')
    
    
    # application command & interaction
    
    async def application_command_global_get_all(self, application_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/{application_id}/commands')
    
    async def application_command_global_create(self, application_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/applications/{application_id}/commands', data)
    
    async def application_command_global_edit(self, application_id, application_command_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH, f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}', data)
    
    async def application_command_global_delete(self, application_id, application_command_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}')
    
    async def application_command_guild_get_all(self, application_id, guild_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET, f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands')
    
    async def application_command_guild_create(self, application_id,guild_id,  data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands', data)
    
    async def application_command_guild_edit(self, application_id, guild_id, application_command_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH, f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}', data)
    
    async def application_command_guild_delete(self, application_id, guild_id, application_command_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE, f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}')
    
    async def interaction_response_message_create(self, interaction_id, interaction_token, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST, f'{API_ENDPOINT}/interactions/{interaction_id}/{interaction_token}/callback', data)
    
    async def interaction_response_message_edit(self, application_id, interaction_id, interaction_token, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_edit, interaction_id),
            METHOD_PATCH, f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original', data)
    
    async def interaction_response_message_delete(self, application_id, interaction_id, interaction_token):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_delete, interaction_id),
            METHOD_DELETE, f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original')
    
    async def interaction_followup_message_create(self, application_id, interaction_id, interaction_token, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_create, interaction_id),
            METHOD_POST, f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}', data)
    
    async def interaction_followup_message_edit(self, application_id, interaction_id, interaction_token, message_id, data):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_edit, interaction_id),
            METHOD_PATCH, f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}', data)
    
    async def interaction_followup_message_delete(self, application_id, interaction_id, interaction_token, message_id):
        return await self.discord_request(RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_delete, interaction_id),
            METHOD_DELETE, f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}')

del re
del modulize
