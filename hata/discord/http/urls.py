__all__ = (
    'API_ENDPOINT', 'CDN_ENDPOINT', 'DISCORD_ENDPOINT', 'INVITE_URL_RP', 'STATUS_ENDPOINT', 'VALID_ICON_FORMATS',
    'VALID_ICON_FORMATS_EXTENDED', 'VALID_ICON_MEDIA_TYPES', 'VALID_ICON_MEDIA_TYPES_EXTENDED',
    'VALID_IMAGE_MEDIA_TYPES_ALL', 'VALID_STICKER_IMAGE_MEDIA_TYPES', 'is_media_url', 'parse_message_jump_url'
)

import re

from scarletio import export, include

from ...env import (
    API_VERSION, CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DISCORD_ENDPOINT, CUSTOM_INVITE_ENDPOINT,
    CUSTOM_MEDIA_ENDPOINT, CUSTOM_STATUS_ENDPOINT
)


StickerFormat = include('StickerFormat')
_try_get_guild_id = include('_try_get_guild_id')


API_ENDPOINT = f'https://discord.com/api/v{API_VERSION}' if (CUSTOM_API_ENDPOINT is None) else CUSTOM_API_ENDPOINT
CDN_ENDPOINT = 'https://cdn.discordapp.com' if (CUSTOM_CDN_ENDPOINT is None) else CUSTOM_CDN_ENDPOINT
DISCORD_ENDPOINT = 'https://discord.com' if (CUSTOM_DISCORD_ENDPOINT is None) else CUSTOM_DISCORD_ENDPOINT
STATUS_ENDPOINT = 'https://status.discord.com/api/v2' if (CUSTOM_STATUS_ENDPOINT is None) else CUSTOM_STATUS_ENDPOINT
MEDIA_ENDPOINT =  'https://media.discordapp.net' if (CUSTOM_MEDIA_ENDPOINT is None) else CUSTOM_MEDIA_ENDPOINT
INVITE_ENDPOINT = 'https://discord.gg' if (CUSTOM_INVITE_ENDPOINT is None) else CUSTOM_INVITE_ENDPOINT

del CUSTOM_API_ENDPOINT, CUSTOM_CDN_ENDPOINT, CUSTOM_DISCORD_ENDPOINT, CUSTOM_STATUS_ENDPOINT, API_VERSION

VALID_ICON_SIZES = frozenset((
    *( 1 << x      for x in range(4, 13)),
    *((1 << x) * 3 for x in range(9, 11)),
    *((1 << x) * 5 for x in range(2,  9)),
))

VALID_ICON_FORMATS = frozenset(('jpg', 'jpeg', 'png', 'webp'))
VALID_ICON_FORMATS_EXTENDED = frozenset((*VALID_ICON_FORMATS, 'gif',))

VALID_ICON_MEDIA_TYPES = frozenset(('image/jpeg', 'image/png', 'image/webp'))
VALID_ICON_MEDIA_TYPES_EXTENDED = frozenset(('image/gif', *VALID_ICON_MEDIA_TYPES))

VALID_STICKER_IMAGE_MEDIA_TYPES = frozenset(('image/gif', 'image/png', 'application/json'))
VALID_IMAGE_MEDIA_TYPES_ALL = frozenset((*VALID_ICON_MEDIA_TYPES_EXTENDED, *VALID_STICKER_IMAGE_MEDIA_TYPES))


WIDGET_STYLE_RP = re.compile('shield|banner[1-4]')

MESSAGE_JUMP_URL_RP = re.compile(
    '(?:https://)?(?:(?:canary|ptb)\\.)?discord(?:app)?.com/channels/(?:(\\d{7,21})|@me)/(\\d{7,21})/(\\d{7,21})'
)
export(MESSAGE_JUMP_URL_RP, 'MESSAGE_JUMP_URL_RP')


CDN_RP = re.compile(
    'https://(?:'
        'cdn\\.discordapp\\.com|'
        '(?:(?:canary|ptb)\\.)?discord\\.com|'
        '(?:'
            'images-ext-\\d+|'
            'media'
        ')\\.discordapp\\.net'
    ')/'
)


WEBHOOK_URL_PATTERN = re.compile(
    '(?:https://)?discord(?:app)?.com/api/(?:v\\d+/)?webhooks/([0-9]{17,21})/([a-zA-Z0-9.\\-_%]{60,68})(?:/.*)?'
)

INVITE_URL_RP = re.compile('(?:https?://)?discord(?:\\.gg|(?:app)?\\.com/invite)/([a-zA-Z0-9-]+)')


def _validate_extension(icon_type, ext):
    """
    Validates the given icon extension.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The respective icon type.
    
    ext : `None | str`
        The received extension.
    
    Returns
    -------
    ext : `str`
        The validated extension.
    
    Raises
    ------
    ValueError
        - If `ext`'s value is not applicable for the given icon type.
    """
    if ext is None:
        ext = icon_type.default_postfix
    
    else:
        if not icon_type.allows_postfix(ext):
            raise ValueError(
                f'Extension must be one of {icon_type.allowed_postfixes}, got {ext!r}.'
            )
    
    return ext


def _build_end(size, add_animated_query_parameter):
    """
    Validates the given icon size.
    
    Parameters
    ----------
    size : `None | int`
        The received size.
    
    add_animated_query_parameter : `bool`
        Whether `animated=true` query parameter should be added.
    
    Returns
    -------
    end : `str`
        The validated size as query string.
    
    Raises
    ------
    ValueError
        - If `size`'s value is not applicable for the given icon type.
    """
    if size is None:
        end = ''
    
    elif size in VALID_ICON_SIZES:
        end = f'?size={size}'
    
    else:
        raise ValueError(
            f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size!r}.'
        )
    
    if add_animated_query_parameter:
        if end:
            end += '&animated=true'
        else:
            end = '?animated=true'
    
    return end


def build_activity_asset_image_large_url(application_id, image_large):
    """
    Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_large : `None | str`
        The activity's asset's large image's value.
    
    Returns
    -------
    url : `None | str`
    """
    if (not application_id) or (image_large is None) or (not image_large.isdigit()):
        return None
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.png'


def build_activity_asset_image_large_url_as(application_id, image_large, ext, size):
    """
    Returns the activity's large asset image's url. If the activity has no large asset image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_large : `None | str`
        The activity's asset's large image's value.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if (not application_id) or (image_large is None) or (not image_large.isdigit()):
        return None
    
    end = _build_end(size, False)

    if ext is None:
        ext = 'png'
    elif ext not in VALID_ICON_FORMATS:
        raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.{ext}{end}'


def build_activity_asset_image_small_url(application_id, image_small):
    """
    Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_small : `None | str`
        The activity's asset's small image's value.
    
    Returns
    -------
    url : `None | str`
    """
    if (not application_id) or (image_small is None) or (not image_small.isdigit()):
        return None
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.png'


def build_activity_asset_image_small_url_as(application_id, image_small, ext, size):
    """
    Returns the activity's small asset image's url. If the activity has no small asset image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_small : `None | str`
        The activity's asset's small image's value.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if (not application_id) or (image_small is None) or (not image_small.isdigit()):
        return None
    
    end = _build_end(size, False)

    if ext is None:
        ext = 'png'
    elif ext not in VALID_ICON_FORMATS:
        raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.')
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.{ext}{end}'


def build_application_cover_url(application_id, icon_type, icon_hash):
    """
    Returns the application's cover image's url. If the application has no cover image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The application's identifier.
    
    icon_type : ``IconType``
        The application's cover icon's type.
    
    icon_hash : `int`
        The application's cover icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/store/{prefix}{icon_hash:0>32x}.{ext}'


def build_application_cover_url_as(application_id, icon_type, icon_hash, ext, size):
    """
    Returns the application's cover image's url. If the application has no cover image, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The application's identifier.
    
    icon_type : ``IconType``
        The application's cover icon's type.
    
    icon_hash : `int`
        The application's cover icon's hash (uint128).
    
    ext : `None | str`
        The extension of the cover's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the cover's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/app-assets/{application_id}/store/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_application_icon_url(application_id, icon_type, icon_hash):
    """
    Returns the application's icon's url. If the application has no icon, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The application's identifier.
    
    icon_type : ``IconType``
        The application's icon's type.
    
    icon_hash : `int`
        The application's icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/app-icons/{application_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_application_icon_url_as(application_id, icon_type, icon_hash, ext, size):
    """
    Returns the application's icon's url. If the application has no icon, then returns `None`.
    
    Parameters
    ----------
    application_id : `int`
        The application's identifier.
    
    icon_type : ``IconType``
        The application's icon's type.
    
    icon_hash : `int`
        The application's icon's hash (uint128).
    
    ext : `None | str`
        The extension of the icon's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the icon's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/app-icons/{application_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_avatar_decoration_url(icon_type, icon_hash):
    """
    Returns an avatar decoration's url. If the avatar decoration has no url, returns `None`.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/avatar-decoration-presets/{prefix}{icon_hash:0>32x}.{ext}'


def build_avatar_decoration_url_as(icon_type, icon_hash, ext, size):
    """
    Returns an avatar decoration's url. If the avatar decoration has no url, returns `None`.
    
    Parameters
    ----------
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/avatar-decoration-presets/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_channel_group_icon_url(channel_id, icon_type, icon_hash):
    """
    Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/channel-icons/{channel_id}/{prefix}{icon_hash:0>32x}.{ext}'
    
    
def build_channel_group_icon_url_as(channel_id, icon_type, icon_hash, ext, size):
    """
    Returns the group channel's icon's image's url. If the channel has no icon, then returns `None`.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/channel-icons/{channel_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_default_avatar_url(value):
    """
    Returns a default avatar's url.
    
    Parameters
    ----------
    value : `int`
        The value of the default avatar.
    
    Returns
    -------
    url : `str`
    """
    return f'{CDN_ENDPOINT}/embed/avatars/{value}.png'


def build_emoji_url(emoji_id, animated):
    """
    Returns the emoji's image's url. If the emoji is unicode emoji, then returns `None` instead.
    
    Parameters
    ----------
    emoji_id : `int`
        The emoji's identifier.
    
    animated : `bool`
        Whether the emoji is animated.
    
    Returns
    -------
    url : `None | str`
    """
    if emoji_id < (1 << 22):
        return None
    
    if animated:
         ext = 'gif'
    else:
         ext = 'png'
    
    return f'{CDN_ENDPOINT}/emojis/{emoji_id}.{ext}'


def build_emoji_url_as(emoji_id, animated, ext, size):
    """
    Returns the emoji's image's url. If the emoji is unicode emoji, then returns `None` instead.
    
    Parameters
    ----------
    emoji_id : `int`
        The emoji's identifier.
    
    animated : `bool`
        Whether the emoji is animated.
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`, `'avif'`.
        If emoji is animated, it can be `'gif'` as well.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if emoji_id < (1 << 22):
        return None
    
    if ext is None:
        if animated:
            ext = 'gif'
        else:
            ext = 'png'
        
        add_animated_query_parameter = False
    else:
        if ext == 'avif':
            ext = 'webp'
        
        if animated:
            if ext not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(
                    f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, got {ext!r}.'
                )
            
            add_animated_query_parameter = ext == 'webp'
        else:
            if ext not in VALID_ICON_FORMATS:
                raise ValueError(
                    f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.'
                )
            
            add_animated_query_parameter = False
    
    end = _build_end(size, add_animated_query_parameter)
    
    return f'{CDN_ENDPOINT}/emojis/{emoji_id}.{ext}{end}'


def build_guild_badge_icon_url(guild_id, icon_type, icon_hash):
    """
    Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/badge-icons/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_badge_icon_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/badge-icons/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_banner_url(guild_id, icon_type, icon_hash):
    """
    Builds a guild's banner url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/banners/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_banner_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Builds a guild's banner url with the given extension and size.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        - If `ext` or `size` were passed as an unexpected value.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/banners/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_discovery_splash_url(guild_id, icon_type, icon_hash):
    """
    Builds a guild's discovery splash url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/discovery-splashes/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_discovery_splash_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Builds a guild's discovery splash url with the given extension and size.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        - If `ext` or `size` were passed as an unexpected value.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/discovery-splashes/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_home_splash_url(guild_id, icon_type, icon_hash):
    """
    Builds a guild's home splash url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/home-headers/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_home_splash_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Builds a guild's home splash url with the given extension and size.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        - If `ext` or `size` were passed as an unexpected value.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/home-headers/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_icon_url(guild_id, icon_type, icon_hash):
    """
    Builds a guild's icon url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/icons/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_icon_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Builds a guild's icon url with the given extension and size.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        - If `ext` or `size` were passed as an unexpected value.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/icons/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_invite_splash_url(guild_id, icon_type, icon_hash):
    """
    Builds a guild's invite splash url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/splashes/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_guild_widget_json_url(guild_id):
    """
    Returns an url to the guild's widget data.
    
    Returns
    -------
    url : `str`
    """
    return  f'{API_ENDPOINT}/guilds/{guild_id}/widget.json'


def build_guild_widget_url(guild_id):
    """
    Returns the guild's widget image's url in `.png` format.
    
    Returns
    -------
    url : `str`
    """
    return f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=shield'


def build_guild_widget_url_as(guild_id, style = 'shield'):
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
    if WIDGET_STYLE_RP.fullmatch(style) is None:
        raise ValueError(f'Invalid style: {style!r}')
    
    return f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style={style}'


def build_guild_invite_splash_url_as(guild_id, icon_type, icon_hash, ext, size):
    """
    Builds a guild's invite splash url with the given extension and size.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        - If `ext` or `size` were passed as an unexpected value.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/splashes/{guild_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_guild_vanity_invite_url(vanity_code):
    """
    Returns the guild's vanity invite's url.
    
    Parameters
    ----------
    vanity_code : `None | str`
        The guild's vanity invite core.
    
    Returns
    -------
    url : `None | str`
    """
    if (vanity_code is not None):
        return f'{INVITE_ENDPOINT}/{vanity_code}'


def build_invite_url(invite_code):
    """
    Returns the invite's url.
    
    Parameters
    ----------
    invite_code : `None | str`
        The invite's code.
    
    Returns
    -------
    url : `str`
    """
    return f'{INVITE_ENDPOINT}/{invite_code}'


def build_message_jump_url(guild_id, channel_id, message_id):
    """
    Builds a jump url to jump to a message in chat history.
    
    Parameters
    ----------
    guild_id : `int`
        The message's guild's identifier.
    
    channel_id : `int`
        The message's channel's identifier.
    
    message_id : `int`
        The message's identifier.
    
    Returns
    -------
    url : `str`
    """
    if guild_id:
        guild_id = str(guild_id)
    else:
        guild_id = '@me'
        
    return f'{DISCORD_ENDPOINT}/channels/{guild_id}/{channel_id}/{message_id}'


def build_name_plate_url(asset_path):
    """
    Builds name plate url.
    
    Parameters
    ----------
    asset_path : `str`
        Part to the name plate's asset.
    
    Returns
    -------
    url : `str`
    """
    return f'{DISCORD_ENDPOINT}/assets/collectibles/{asset_path}asset.webm'


def build_role_icon_url(role_id, icon_type, icon_hash):
    """
    Returns the role's icon's image's url. If the role has no icon, then returns `None`.
    
    Parameters
    ----------
    role_id : `int`
        The role's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/role-icons/{role_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_role_icon_url_as(role_id, icon_type, icon_hash, ext, size):
    """
    Returns the role's icon's image's url. If the role has no icon, then returns `None`.
    
    Parameters
    ----------
    role_id : `int`
        The role's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/role-icons/{role_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_scheduled_event_image_url(scheduled_event_id, icon_type, icon_hash):
    """
    Returns the scheduled event's image's url. If the scheduled event has no image, then returns `None`.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_scheduled_event_image_url_as(scheduled_event_id, icon_type, icon_hash, ext, size):
    """
    Returns the scheduled event's image's url. If the scheduled event has no image, then returns `None`.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/guild-events/{scheduled_event_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_scheduled_event_url(guild_id, scheduled_event_id):
    """
    Returns the scheduled event's url.
    
    Parameters
    ----------
    guild_id : `int`
        The guild's identifier where the scheduled event is.
    
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    Returns
    -------
    url : `str`
    """
    return f'{DISCORD_ENDPOINT}/events/{guild_id}/{scheduled_event_id}'


def build_soundboard_sound_url(sound_id):
    """
    Returns the url to the sound board sound.
    
    Parameters
    ----------
    sound_id : `int`
        Soundboard sound identifier.
    
    Returns
    -------
    url : `str`
    """
    return f'{CDN_ENDPOINT}/soundboard-sounds/{sound_id}'


def build_sticker_pack_banner_url(sticker_pack_banner_id):
    """
    Returns the sticker pack's banner's url.
    
    Parameters
    ----------
    sticker_pack_banner_id : `int`
        The sticker pack's banner's identifier.
    
    Returns
    -------
    url : `None | str`
    """
    if sticker_pack_banner_id:
        return f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.png'


def build_sticker_pack_banner_url_as(sticker_pack_banner_id, ext, size):
    """
    Returns the sticker pack's banner's url.
    
    Parameters
    ----------
    sticker_pack_banner_id : `int`
        The sticker pack's banner's identifier.
    
    ext : `None | str`
        The extension of the banner's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the banner's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not sticker_pack_banner_id:
        return
    
    end = _build_end(size, False)
    
    if ext is None:
        ext = 'png'
    
    else:
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(
                f'Extension must be one of {VALID_ICON_FORMATS}, got {ext!r}.'
            )
    
    return f'{CDN_ENDPOINT}/app-assets/710982414301790216/store/{sticker_pack_banner_id}.{ext}{end}'


def build_sticker_url(sticker_id, sticker_format):
    """
    Returns the sticker's url.
    
    Parameters
    ----------
    sticker_id : `int`
        The sticker's identifier.
    
    sticker_format : ``StickerFormat``
        The sticker's format.
    
    Returns
    -------
    url : `None | str`
    """
    if sticker_format is StickerFormat.none:
        return None
    
    if sticker_format is StickerFormat.gif:
        endpoint = MEDIA_ENDPOINT
    else:
        endpoint = CDN_ENDPOINT
        
    return f'{endpoint}/stickers/{sticker_id}.{sticker_format.extension}'


def build_sticker_url_as(sticker_id, sticker_format, size, preview):
    """
    Returns the sticker's url.
    
    Parameters
    ----------
    sticker_id : `int`
        The sticker's identifier.
    
    sticker_format : ``StickerFormat``
        The sticker's format.
    
    size : `None | int`
        The preferred minimal size of the icon's url.
    
    preview : `bool`
        Whether preview url should be generated.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `size` was not passed as any of the expected values.
    """
    if sticker_format is StickerFormat.none:
        return None
    
    # Resolve size
    if size is None:
        end = ''
    else:
        if sticker_format is StickerFormat.lottie:
            end = ''
        else:
            if size in VALID_ICON_SIZES:
                end = f'?size={size}'
            else:
                raise ValueError(f'Size must be in {sorted(VALID_ICON_SIZES)!r}, got {size!r}.')
    
    # Resolve preview
    if preview:
        if sticker_format is StickerFormat.apng:
            end = f'{end}{"&" if end else "?"}passthrough=false'
    
    if sticker_format is StickerFormat.gif:
        endpoint = MEDIA_ENDPOINT
    else:
        endpoint = CDN_ENDPOINT
    
    return f'{endpoint}/stickers/{sticker_id}.{sticker_format.extension}{end}'


def build_team_icon_url(team_id, icon_type, icon_hash):
    """
    Returns the team's icon's url. If the team has no icon, then returns `None`.
    
    Parameters
    ----------
    team_id : `int`
        The team's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/team-icons/{team_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_team_icon_url_as(team_id, icon_type, icon_hash, ext, size):
    """
    Returns the team's icon's url. If the team has no icon, then returns `None`.
    
    Parameters
    ----------
    team_id : `int`
        The team's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/team-icons/{team_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_user_avatar_url(user_id, icon_type, icon_hash):
    """
    Returns the user's avatar's url. If the user has no avatar, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
   
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/avatars/{user_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_user_avatar_url_as(user_id, icon_type, icon_hash, ext, size):
    """
    Returns the user's avatar's url. If the user has no avatar, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        If the user has animated avatar, it can be `'gif'` as well.
    
    size : `None | int`
        The preferred minimal size of the avatar's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/avatars/{user_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_user_avatar_url_for(user_id, guild_id, icon_type, icon_hash):
    """
    Returns the user's guild specific avatar. If the user has no guild local avatar, returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/{prefix}{icon_hash:0>32x}.{ext}'


def build_user_avatar_url_for_as(user_id, guild_id, icon_type, icon_hash, ext, size):
    """
    Returns the user's guild specific avatar. If the user has no guild local avatar, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None

    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return (
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/avatars/{prefix}{icon_hash:0>32x}.{ext}{end}'
    )


def build_user_banner_url(user_id, icon_type, icon_hash):
    """
    Returns the user's banner's url. If the user has no banner, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
   
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/banners/{user_id}/{prefix}{icon_hash:0>32x}.{ext}'


def build_user_banner_url_as(user_id, icon_type, icon_hash, ext, size):
    """
    Returns the user's banner's url. If the user has no banner, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        If the user has animated banner, it can be `'gif'` as well.
    
    size : `None | int`
        The preferred minimal size of the banner's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return f'{CDN_ENDPOINT}/banners/{user_id}/{prefix}{icon_hash:0>32x}.{ext}{end}'


def build_user_banner_url_for(user_id, guild_id, icon_type, icon_hash):
    """
    Returns the user's guild specific banner. If the user has no guild local banner, returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    url : `None | str`
    """
    if not icon_type.can_create_url():
        return None
    
    prefix = icon_type.prefix
    ext = icon_type.default_postfix
    
    return f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/{prefix}{icon_hash:0>32x}.{ext}'


def build_user_banner_url_for_as(user_id, guild_id, icon_type, icon_hash, ext, size):
    """
    Returns the user's guild specific banner. If the user has no guild local banner, then returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    guild_id : `int`
        The guild's identifier.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    url : `None | str`
    
    Raises
    ------
    ValueError
        If `ext`, `size` was not passed as any of the expected values.
    """
    if not icon_type.can_create_url():
        return None

    prefix = icon_type.prefix
    ext = _validate_extension(icon_type, ext)
    end = _build_end(size, prefix == 'a_' and ext == 'webp')
    
    return (
        f'{CDN_ENDPOINT}/guilds/{guild_id}/users/{user_id}/banners/{prefix}{icon_hash:0>32x}.{ext}{end}'
    )


def build_webhook_url(webhook_id, webhook_token):
    """
    Returns the webhook's url.
    
    Parameters
    ----------
    webhook_id : `int`
        The webhook's identifier.
    
    webhook_token : `str`
        The webhook's token.
    
    Returns
    -------
    url : `str`
    """
    return f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}'


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


def parse_message_jump_url(message_url):
    """
    Parses the jump url of a message. On failure returns `0`-s.
    
    Parameters
    ----------
    message_url : `str`
        The message url to parse.
    
    Returns
    -------
    guild_id_and_channel_id_and_message_id : `(int, int, int)`
        The message's guild's, channel's and their own identifier.
    """
    parsed = MESSAGE_JUMP_URL_RP.fullmatch(message_url)
    if parsed is None:
        guild_id = 0
        channel_id = 0
        message_id = 0
    else:
        guild_id, channel_id, message_id = parsed.groups()
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        channel_id = int(channel_id)
        message_id = int(message_id)
    
    return guild_id, channel_id, message_id
