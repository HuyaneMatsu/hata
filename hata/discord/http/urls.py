__all__ = ('API_ENDPOINT', 'CDN_ENDPOINT', 'DISCORD_ENDPOINT', 'INVITE_URL_RP', 'MESSAGE_JUMP_URL_RP',
    'STATUS_ENDPOINT', 'VALID_ICON_FORMATS', 'VALID_ICON_FORMATS_EXTENDED', 'VALID_ICON_MEDIA_TYPES',
    'VALID_ICON_MEDIA_TYPES_EXTENDED', 'VALID_STICKER_IMAGE_MEDIA_TYPES', 'is_media_url')

import re

from ...env import CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DISCORD_ENDPOINT, CUSTOM_STATUS_ENDPOINT, \
    API_VERSION

from ...backend.export import export, include

from ..bases import ICON_TYPE_NONE, ICON_TYPE_STATIC

ChannelGuildBase = include('ChannelGuildBase')
StickerFormat = include('StickerFormat')

API_ENDPOINT = f'https://discord.com/api/v{API_VERSION}' if (CUSTOM_API_ENDPOINT is None) else CUSTOM_API_ENDPOINT
CDN_ENDPOINT = 'https://cdn.discordapp.com' if (CUSTOM_CDN_ENDPOINT is None) else CUSTOM_CDN_ENDPOINT
DISCORD_ENDPOINT = 'https://discord.com' if (CUSTOM_DISCORD_ENDPOINT is None) else CUSTOM_DISCORD_ENDPOINT
STATUS_ENDPOINT = 'https://status.discord.com/api/v2' if (CUSTOM_STATUS_ENDPOINT is None) else CUSTOM_STATUS_ENDPOINT

del CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DISCORD_ENDPOINT, CUSTOM_STATUS_ENDPOINT, API_VERSION

VALID_ICON_SIZES = frozenset((
    *( 1<<x    for x in range(4, 13)),
    *((1<<x)*3 for x in range(9, 11)),
    *((1<<x)*5 for x in range(2,  9)),
))

VALID_ICON_FORMATS = frozenset(('jpg', 'jpeg', 'png', 'webp'))
VALID_ICON_FORMATS_EXTENDED = frozenset((*VALID_ICON_FORMATS, 'gif',))

VALID_ICON_MEDIA_TYPES = frozenset(('image/jpeg', 'image/png', 'image/webp'))
VALID_ICON_MEDIA_TYPES_EXTENDED = frozenset(('image/gif', *VALID_ICON_MEDIA_TYPES))

VALID_STICKER_IMAGE_MEDIA_TYPES = frozenset(('image/png', 'application/json'))

STYLE_PATTERN = re.compile('(^shield$)|(^banner[1-4]$)')

MESSAGE_JUMP_URL_RP = re.compile('(?:https://)?discord(?:app)?.com/channels/(?:(\d{7,21})|@me)/(\d{7,21})/(\d{7,21})')
export(MESSAGE_JUMP_URL_RP, 'MESSAGE_JUMP_URL_RP')

#returns a URL that allows the client to jump to this message
#guild is guild's id, or @me if there is no guild
def message_jump_url(message):
    """
    Returns a jump url to the message. If the message's channel is a partial guild channel, returns `None`.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    Returns
    -------
    url : `None` or `str`
    """
    channel_id = message.channel_id
    guild_id = message.guild_id
    if guild_id:
        guild_id = str(guild_id)
    else:
        guild_id = '@me'
    
    return f'{DISCORD_ENDPOINT}/channels/{guild_id}/{channel_id}/{message.id}'

CDN_RP = re.compile(
    'https://(?:'
        'cdn\.discordapp\.com|'
        'discord\.com|'
        '(?:'
            'images-ext-\d+|'
            'media'
        ')\.discordapp\.net'
    ')/'
)

def is_cdn_url(url):
    """
    Returns whether the given url a Discord content delivery network url.
    
    Parameters
    ----------
    url : `str`
        The url to check.
    
    Returns
    -------
    is_cdn_url : `bool`
    
    Examples
    --------
    Icons: `https://cdn.discordapp.com/...`
    Assets: `https://discord.com/...`
    Proxy service: `https://images-ext-1.discordapp.net/...`
    Attachments: `https://media.discordapp.net/...`
    ```
    """
    return (CDN_RP.match(url) is not None)


def is_media_url(url):
    """
    Returns whether the given url uses the discord's media content delivery network.
    
    Parameters
    ----------
    url : `str`
        The url to check.
    
    Returns
    -------
    is_media_url : `bool`
    """
    return url.startswith('https://media.discordapp.net/')


def guild_icon_url(guild):
    """
    Returns the guild's icon's image's url. If the guild has no icon, then returns `None`.
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
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


def guild_icon_url_as(guild, ext=None, size=None):
    """
    Returns the guild's icon's url. If the guild has no icon, then returns `None`.
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the guild has
        animated icon, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
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


def guild_invite_splash_url_as(guild, ext=None, size=None):
    """
    Returns the guild's invite splash's image's url. If the guild has no invite splash, then returns `None`.
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
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


def guild_discovery_splash_url_as(guild, ext=None, size=None):
    """
    Returns the guild's discovery splash's image's url. If the guild has no discovery splash, then returns `None`.
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
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


def guild_banner_url_as(guild, ext=None, size=None):
    """
    Returns the guild's banner's image's url. If the guild has no banner, then returns `None`.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`, `'gif'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
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
    
    Parameters
    ----------
    guild : ``Guild`` or ``GuildPreview``
        The respective guild.
    
    Returns
    -------
    url : `str`
    """
    return  f'{API_ENDPOINT}/guilds/{guild.id}/widget.json'


def channel_group_icon_url(channel):
    """
    Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
    
    Parameters
    ----------
    channel : ``ChannelGroup``
        The respective channel.
    
    Returns
    -------
    url : `None` or `str`
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
    
    
def channel_group_icon_url_as(channel, ext=None, size=None):
    """
    Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
    
    Parameters
    ----------
    channel : ``ChannelGroup``
        The respective channel.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    emoji : ``Emoji``
        The respective emoji.
    
    Returns
    -------
    url : `None` or `str`
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
    emoji : ``Emoji``
        The respective emoji.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If emoji is
        animated, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
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
    
    Parameters
    ----------
    webhook : `Webhook``
        The respective webhook.
    
    Returns
    -------
    url : `str`
    """
    return f'{API_ENDPOINT}/webhooks/{webhook.id}/{webhook.token}'


WEBHOOK_URL_PATTERN = re.compile(
    '(?:https://)?discord(?:app)?.com/api/(?:v\d+/)?webhooks/([0-9]{17,21})/([a-zA-Z0-9\.\-\_%]{60,68})(?:/.*)?'
)


def invite_url(invite):
    """
    Returns the invite's url.
    
    Parameters
    ----------
    invite : ``Invite``
        The respective invite.
    
    Returns
    -------
    url : `str`
    """
    return f'http://discord.gg/{invite.code}'


INVITE_URL_RP = re.compile('(?:https?://)?discord(?:\.gg|(?:app)?\.com/invite)/([a-zA-Z0-9-]+)')


def activity_asset_image_large_url(activity):
    """
    Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
    
    Parameters
    ----------
    activity : ``ActivityRich``
        The respective activity.
    
    Returns
    -------
    url : `None` or `str`
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


def activity_asset_image_large_url_as(activity, ext=None, size=None):
    """
    Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.

    
    Parameters
    ----------
    activity : ``ActivityRich``
        The respective activity.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')

    if ext not in VALID_ICON_FORMATS:
        raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')

    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.{ext}{end}'


def activity_asset_image_small_url(activity):
    """
    Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
    
    Parameters
    ----------
    activity : ``ActivityRich``
        The respective activity.
    
    Returns
    -------
    url : `None` or `str`
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


def activity_asset_image_small_url_as(activity, ext=None, size=None):
    """
    Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
    
    Parameters
    ----------
    activity : ``ActivityRich``
        The respective activity.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext not in VALID_ICON_FORMATS:
        raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.{ext}{end}'


def user_avatar_url(user):
    """
    Returns the user's avatar's url. If the user has no avatar, then returns it's default avatar's url.
    
    Parameters
    ----------
    user : ``UserBase``
        The respective user.
    
    Returns
    -------
    url : `None` or `str`
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


def user_avatar_url(user):
    """
    Returns the user's avatar's url. If the user has no avatar, then returns it's default avatar's url.
    
    Parameters
    ----------
    user : ``UserBase``
        The respective user.
    
    Returns
    -------
    url : `None` or `str`
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
    user : ``UserBase``
        The respective user.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the user has
        animated avatar, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the avatar's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
            prefix = ''
        else:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            prefix = 'a_'
    
    return f'{CDN_ENDPOINT}/avatars/{user.id}/{prefix}{user.avatar_hash:0>32x}.{ext}{end}'


def user_banner_url(user):
    """
    Returns the user's banner's url. If the user has no banner, then returns `None`.
    
    Parameters
    ----------
    user : ``UserBase``
        The respective user.
    
    Returns
    -------
    url : `None` or `str`
    """
    icon_type = user.banner_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if icon_type is ICON_TYPE_STATIC:
        prefix = ''
        ext = 'png'
    else:
        prefix = 'a_'
        ext = 'gif'
    
    return f'{CDN_ENDPOINT}/banners/{user.id}/{prefix}{user.banner_hash:0>32x}.{ext}'


def user_banner_url_as(user, ext=None, size=None):
    """
    Returns the user's banner's url. If the user has no banner, then returns `None`.
    
    Parameters
    ----------
    user : ``UserBase``
        The respective user.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the user has
        animated banner, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the avatar's url.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `ext` or `size` was not passed as any of the expected values.
    """
    icon_type = user.banner_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if size is None:
        end = ''
    elif size in VALID_ICON_SIZES:
        end = f'?size={size}'
    else:
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
            prefix = ''
        else:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            prefix = 'a_'
    
    return f'{CDN_ENDPOINT}/banners/{user.id}/{prefix}{user.banner_hash:0>32x}.{ext}{end}'


def user_avatar_url_for(user, guild):
    """
    Returns the user's guild specific avatar. If the user has no guild specific avatar, returns `None`.
    
    Parameters
    ----------
    user : ``UserBase``
        The Respective user.
    guild : ``Guild``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
    """
    if guild is None:
        return None
    
    try:
        guild_profile = user.guild_profiles[guild.id]
    except KeyError:
        return None
    
    icon_type = guild_profile.avatar_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if icon_type is ICON_TYPE_STATIC:
        prefix = ''
        ext = 'png'
    else:
        prefix = 'a_'
        ext = 'gif'
    
    return f'{CDN_ENDPOINT}/guilds/{guild.id}/users/{user.id}/avatars/{prefix}{guild_profile.avatar_hash:0>32x}.{ext}'


def user_avatar_url_for_as(user, guild, ext=None, size=None):
    """
    Returns the user's guild specific avatar. If the user has no avatar, then returns it's default avatar's url.
    
    Parameters
    ----------
    user : ``UserBase``
        The Respective user.
    guild : ``Guild``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the user has
        animated avatar, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the avatar's url.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `ext` or `size` was not passed as any of the expected values.
    """
    if guild is None:
        return None
    
    try:
        guild_profile = user.guild_profiles[guild.id]
    except KeyError:
        return None
    
    icon_type = guild_profile.avatar_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if size is None:
        end = ''
    elif size in VALID_ICON_SIZES:
        end = f'?size={size}'
    else:
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
            prefix = ''
        else:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            prefix = 'a_'
    
    return f'{CDN_ENDPOINT}/guilds/{guild.id}/users/{user.id}/avatars/{prefix}{guild_profile.avatar_hash:0>32x}.' \
           f'{ext}{end}'


def user_avatar_url_at(user, guild):
    """
    Returns the user's avatar's url at the guild.
    
    Parameters
    ----------
    user : ``UserBase``
        The Respective user.
    guild : ``Guild``
        The respective guild.
    
    Returns
    -------
    url : `None` or `str`
    """
    avatar_url = user_avatar_url_for(user, guild)
    if avatar_url is None:
        avatar_url = user_avatar_url(user)
    
    return avatar_url


def user_avatar_url_at_as(user, guild, ext=None, size=None):
    """
    Returns the user's avatar's url at the guild. If the user has no avatar, then returns it's default avatar's url.
    
    Parameters
    ----------
    user : ``UserBase``
        The Respective user.
    guild : ``Guild``
        The respective guild.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`. If the user has
        animated avatar, it can `'gif'` as well.
    size : `int`, Optional
        The preferred minimal size of the avatar's url.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `ext` or `size` was not passed as any of the expected values.
    """
    avatar_url = user_avatar_url_for_as(user, guild, ext=ext, size=size)
    if avatar_url is None:
        avatar_url = user_avatar_url_as(user, ext=ext, size=size)
    
    return avatar_url


def default_avatar_url(default_avatar):
    """
    Returns the user's default avatar's url.
    
    Parameters
    ----------
    user : ``UserBase``
        The Respective user.
    
    Returns
    -------
    url : `str`
    """
    return f'{CDN_ENDPOINT}/embed/avatars/{default_avatar.value}.png'


def application_icon_url(application):
    """
    Returns the application's icon's url. If the application has no icon, then returns `None`.
    
    Parameters
    ----------
    application : ``Application``, ``MessageApplication``, ``IntegrationApplication``
        The respective application.
    
    Returns
    -------
    url : `None` or `str`
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


def application_icon_url_as(application, ext=None, size=None):
    """
    Returns the application's icon's url. If the application has no icon, then returns `None`.
    
    Parameters
    ----------
    application : ``Application``, ``MessageApplication``, ``IntegrationApplication``
        The respective application.
    ext : `str`, Optional
        The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the icon's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    application : ``Application``, ``MessageApplication``
        The respective application.
        
    Returns
    -------
    url : `None` or `str`
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


def application_cover_url_as(application, ext=None, size=None):
    """
    Returns the application's cover image's url. If the application has no cover image, then returns `None`.
    
    Parameters
    ----------
    application : ``Application``, ``MessageApplication``
        The respective application.
    ext : `str`, Optional
        The extension of the cover's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the cover's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    team : ``Team``
        The respective team.
    
    Returns
    -------
    url : `None` or `str`
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


def team_icon_url_as(team, ext=None, size=None):
    """
    Returns the team's icon's url. If the team has no icon, then returns `None`.
    
    Parameters
    ----------
    team : ``Team``
        The respective team.
    ext : `str`, Optional
        The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the icon's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
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
    
    Parameters
    ----------
    achievement : ``Achievement``
        The respective achievements
    
    Returns
    -------
    url : `None` or `str`
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
    
    return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{prefix}' \
           f'{achievement.icon_hash:0>32x}.{ext}'


def achievement_icon_url_as(achievement, ext=None, size=None):
    """
    Returns the achievement's icon's url.
    
    Parameters
    ----------
    achievement : ``Achievement``
        The respective achievements
    ext : `str`, Optional
        The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the icon's url.
    
    Returns
    -------
    url : `None` or `str`
    
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
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
            prefix = ''
        else:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            prefix = 'a_'
    
    return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{prefix}' \
           f'{achievement.icon_hash:0>32x}.{ext}{end}'


def sticker_url(sticker):
    """
    Returns the sticker's url.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The respective sticker.
    
    Returns
    -------
    url : `None` or `str`
    """
    format = sticker.format
    if format is StickerFormat.none:
        return None
    
    return f'{CDN_ENDPOINT}/stickers/{sticker.id}.{format.extension}'


def sticker_url_as(sticker, size=None, preview=False):
    """
    Returns the sticker's url.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The respective sticker.
    size : `int`, Optional
        The preferred minimal size of the icon's url.
    preview : `bool`, Optional
        Whether preview url should be generated.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `size` was not passed as any of the expected values.
    """
    format = sticker.format
    if format is StickerFormat.none:
        return None
    
    # Resolve size
    if size is None:
        end = ''
    else:
        if format is StickerFormat.lottie:
            end = ''
        else:
            if size in VALID_ICON_SIZES:
                end = f'?size={size}'
            else:
                raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    # Resolve preview
    if preview:
        if format is StickerFormat.apng:
            end = f'{end}{"&" if end else "?"}passthrough=false'
    
    return f'{CDN_ENDPOINT}/stickers/{sticker.id}.{format.extension}{end}'


def sticker_pack_banner(sticker_pack):
    """
    Returns the sticker pack banner's url.
    
    Parameters
    ----------
    sticker_pack : `StickerPack``
        The respective sticker pack.
    
    Returns
    -------
    url : `None` or `str`
    """
    return f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack.banner_id}.png'


def sticker_pack_banner_as(sticker_pack, ext=None, size=None):
    """
    Returns the achievement's icon's url.
    
    Parameters
    ----------
    sticker_pack : `StickerPack``
        The respective sticker pack.
    ext : `str`, Optional
        The extension of the banner's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    size : `int`, Optional
        The preferred minimal size of the banner's url.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `ext` or `size` was not passed as any of the expected values.
    """
    if size is None:
        end = ''
    elif size in VALID_ICON_SIZES:
        end = f'?size={size}'
    else:
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        ext = 'png'
    
    else:
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
    
    return f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack.banner_id}.{ext}{end}'


def role_icon_url(role):
    """
    Returns the role's icon's image's url. If the role has no icon, then returns `None`.
    
    Parameters
    ----------
    role : ``Role``
        The respective role.
    
    Returns
    -------
    url : `None` or `str`
    """
    icon_type = role.icon_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if icon_type is ICON_TYPE_STATIC:
        prefix = ''
        ext = 'png'
    else:
        prefix = 'a_'
        ext = 'gif'
    
    return f'{CDN_ENDPOINT}/role-icons/{role.id}/{prefix}{role.icon_hash:0>32x}.{ext}'


def role_icon_url_as(role, ext=None, size=None):
    """
    Returns the role's icon's image's url. If the role has no icon, then returns `None`.
    
    Parameters
    ----------
    role : ``Role``
        The respective role.
    ext : `str`, Optional
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`, `'gif'`.
    size : `int`, Optional
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None` or `str`
    
    Raises
    ------
    ValueError
        If `ext` or `size` was not passed as any of the expected values.
    """
    icon_type = role.icon_type
    if icon_type is ICON_TYPE_NONE:
        return None
    
    if size is None:
        end = ''
    elif size in VALID_ICON_SIZES:
        end = f'?size={size}'
    else:
        raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size}.')
    
    if ext is None:
        if icon_type is ICON_TYPE_STATIC:
            prefix = ''
            ext = 'png'
        else:
            prefix = 'a_'
            ext = 'gif'
    
    else:
        if icon_type is ICON_TYPE_STATIC:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
            prefix = ''
        else:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.')
            prefix = 'a_'

    return f'{CDN_ENDPOINT}/role-icons/{role.id}/{prefix}{role.icon_hash:0>32x}.{ext}{end}'
