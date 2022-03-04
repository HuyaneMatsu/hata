__all__ = (
    'CHANNEL_TYPE_MAP', 'cr_pg_channel_object', 'create_partial_channel_from_data', 'create_partial_channel_from_id'
)

import reprlib
from datetime import datetime

from scarletio import export, include

from ..bases import maybe_snowflake
from ..core import CHANNELS
from ..permission import PermissionOverwrite
from ..utils import datetime_to_timestamp

from . import channel_types as CHANNEL_TYPES
from .channel_base import ChannelBase
from .channel_guild_base import ChannelGuildBase
from .channel_guild_category import ChannelCategory
from .channel_guild_directory import ChannelDirectory
from .channel_guild_forum import ChannelForum
from .channel_guild_store import ChannelStore
from .channel_guild_text import ChannelText
from .channel_guild_undefined import ChannelGuildUndefined
from .channel_guild_voice import ChannelStage, ChannelVoice, ChannelVoiceBase
from .channel_private import ChannelGroup, ChannelPrivate
from .channel_thread import AUTO_ARCHIVE_OPTIONS
from .channel_thread import ChannelThread
from .preinstanced import VideoQualityMode


VoiceRegion = include('VoiceRegion')
Guild = include('Guild')

CHANNEL_TYPE_MAP = {
    CHANNEL_TYPES.guild_text: ChannelText,
    CHANNEL_TYPES.private: ChannelPrivate,
    CHANNEL_TYPES.guild_voice: ChannelVoice,
    CHANNEL_TYPES.private_group: ChannelGroup,
    CHANNEL_TYPES.guild_category: ChannelCategory,
    CHANNEL_TYPES.guild_announcements: ChannelText,
    CHANNEL_TYPES.guild_store: ChannelStore,
    CHANNEL_TYPES.guild_thread_announcements: ChannelThread,
    CHANNEL_TYPES.guild_thread_public: ChannelThread,
    CHANNEL_TYPES.guild_thread_private: ChannelThread,
    CHANNEL_TYPES.guild_stage: ChannelStage,
    CHANNEL_TYPES.guild_directory: ChannelDirectory,
    CHANNEL_TYPES.guild_forum: ChannelForum,
}

export(CHANNEL_TYPE_MAP, 'CHANNEL_TYPE_MAP')


def create_partial_channel_from_data(data, guild_id):
    """
    Creates a partial channel from partial channel data.
    
    Parameters
    ----------
    data : `None`, `dict` of (`str`, `Any`) items
        Partial channel data received from Discord.
    guild_id : `int`
        The channel's guild's identifier.
    
    Returns
    -------
    channel : `None`, ``ChannelBase``
        The created partial channel, or `None`, if no data was received.
    """
    if (data is None) or (not data):
        return None
    
    channel_id = int(data['id'])
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    channel = CHANNEL_TYPE_MAP.get(data['type'], ChannelGuildUndefined)._from_partial_data(data, channel_id, guild_id)
    CHANNELS[channel_id] = channel
    
    return channel


@export
def create_partial_channel_from_id(channel_id, channel_type, guild_id):
    """
    Creates a new partial channel from the given identifier.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    channel_type : `int`
        The channel's type identifier.
    guild_id : `int`
        A guild's identifier of the created channel.
    """
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    channel_type = CHANNEL_TYPE_MAP.get(channel_type, ChannelGuildUndefined)
    channel = channel_type._create_empty(channel_id, channel_type, guild_id)
    CHANNELS[channel_id] = channel
    
    return channel


def cr_pg_channel_object(name, type_, *, permission_overwrites=..., topic=..., nsfw=..., slowmode=..., bitrate=...,
        user_limit=..., region=..., video_quality_mode=..., archived=..., archived_at=...,
        auto_archive_after=..., open_=..., default_auto_archive_after=..., banner=..., parent=..., guild=None,
        overwrites=...):
    """
    Creates a json serializable object representing a ``GuildChannelBase``.
    
    Parameters
    ----------
    name : `str`
        The name of the channel. Can be between `1` and `100` characters.
    type_ : `int`, ``ChannelGuildBase`` subclass
        The channel's type.
    permission_overwrites : `None`, `list` of ``cr_p_permission_overwrite_object`` returns, Optional (Keyword only)
        A list of permission overwrites of the channel. The list should contain json serializable permission
        overwrites made by the ``cr_p_permission_overwrite_object`` function.
    topic : `None`, `str`, Optional (Keyword only)
        The channel's topic.
    nsfw : `None`, `bool`, Optional (Keyword only)
        Whether the channel is marked as nsfw.
    slowmode : `None`, `int`, Optional (Keyword only)
        The channel's slowmode value.
    bitrate : `None`, `int`, Optional (Keyword only)
        The channel's bitrate.
    user_limit : `int`, Optional (Keyword only)
        The channel's user limit.
    region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
        The channel's voice region.
    video_quality_mode : `None`, ``VideoQualityMode``, `int`, Optional (Keyword only)
        The channel's video quality mode.
    archived : `None`, `bool`, Optional (Keyword only)
        Whether the thread channel is archived.
    archived_at : `None`, `datetime`, Optional (Keyword only)
        When the thread's archive status was last changed.
    auto_archive_after : `None`, `int`, Optional (Keyword only)
        Duration in minutes to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    open_ : `None`, `bool`, Optional (Keyword only)
        Whether the thread channel is open.
    default_auto_archive_after : `None`, `int`, Optional (Keyword only)
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Can be
        one of: `3600`, `86400`, `259200`, `604800`.
    banner : `None`, `bytes-like`, Optional (Keyword only)
         The new banner of the channel. Can be `'jpg'`, `'png'`, `'webp'` image's raw data.
    parent : `None`, ``ChannelCategory``, `int`, Optional (Keyword only)
        The channel's parent. If the parent is under a guild, leave it empty.
    category : `None`, ``ChannelCategory``, `int`, Optional (Keyword only)
        Deprecated, please use `parent` parameter instead.
    guild : `None`, ``Guild`` = `None`, Optional (Keyword only)
        Reference guild used for validation purposes. Defaults to `None`.
    
    Returns
    -------
    channel_data : `dict` of (`str`, `Any`) items
    
    Raises
    ------
    TypeError
        - If `type_` was not passed as `int`, ``ChannelGuildBase``.
        - If `parent` was not given as `None`, ``ChannelCategory``, `int`.
        - If `region` was not given either as `None`, `str` nor ``VoiceRegion``.
        - If `video_quality_mode` was not given neither as `None`, `VideoQualityMode`` nor as `int`.
    AssertionError
        - if `guild` is given, but not as `None` nor ``Guild``.
        - If `type_` was given as `int`, and is less than `0`.
        - If `type_` was given as `int` and exceeds the defined channel type limit.
        - If `name` was not given as `str`.
        - If `name`'s length is under `1` or over `100`.
        - If `permission_overwrites` was not given as `None`, neither as `list` of `dict`-s.
        - If `topic` was not given as `str`.
        - If `topic`'s length is over `1024`, `120` depending on channel type.
        - If `topic` was given, but the respective channel type is not ``ChannelText`` nor ``ChannelStage``.
        - If `nsfw` was given meanwhile the respective channel type is not ``ChannelText``, ``ChannelStore``.
        - If `nsfw` was not given as `bool`.
        - If `slowmode` was given, but the respective channel type is not ``ChannelText``, ``ChannelThread``.
        - If `slowmode` was not given as `int`.
        - If `slowmode` was given, but it's value is less than `0` or greater than `21600`.
        - If `bitrate` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `bitrate` was not given as `int`.
        - If `bitrate`'s value is out of the expected range.
        - If `user_limit` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `user_limit` was not given as `int`.
        - If `user_limit`' was given, but is out of the expected [0:99] range.
        - If `parent` was given, but the respective channel type cannot be put under other categories.
        - If `region` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `video_quality_mode` was given, but the respective channel is not ``ChannelVoice``.
        - If `archived` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `archived` was given, but not as `None`, `bool`.
        - If `archived_at` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `archived_at` was given, but not as `None`, `datetime`.
        - If `auto_archive_after` was given, but the respective channel's type is not ``ChannelThread``.
        - If `auto_archive_after` was given, but not as `None`, `int`.
        - If `auto_archive_after` is not any of the expected values.
        - If `open_` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `open_` was given, but not as `None`, `bool`.
        - If `default_auto_archive_after` was given as non `None`, but the respective channel type is not `ChannelText`.
        - If `default_auto_archive_after` was not given neither as `None`, `int`.
        - If `default_auto_archive_after` is not any of the expected values.
    """
    if __debug__:
        if (guild is not None) and (not isinstance(guild, Guild)):
            raise AssertionError(
                '`guild` is given, but not as `None` nor `Guild`, got '
                f'{guild.__class__.__name__}; {guild!r}.'
            )
    
    if isinstance(type_, int):
        if __debug__:
            if type_ < 0:
                raise AssertionError(
                    f'`type_` cannot be negative value, got {type_!r}.'
                )
            if type_ not in CHANNEL_TYPE_MAP.keys():
                raise AssertionError(
                    f'`type_` is not in an of the existing channel types: {set(CHANNEL_TYPE_MAP.keys())!r}, got '
                    f'{type_!r}.'
                )
        
        channel_type = CHANNEL_TYPE_MAP.get(type_, ChannelGuildUndefined)
        channel_type_value = type_
    
    elif issubclass(type_, ChannelBase):
        channel_type = type_
        channel_type_value = type_.INTERCHANGE[0]
    else:
        raise TypeError(
            f'The given `type_` is not, neither refers to a channel a type, got {type_!r}.'
        )
    
    if not issubclass(channel_type, ChannelGuildBase):
        raise TypeError(
            f'`type_` not refers to a `{ChannelGuildBase.__name__}`, but to {channel_type.__name__}. Got '
            f'{type_!r}.'
        )
    
    
    if __debug__:
        if not isinstance(name, str):
            raise AssertionError(
                f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
            )
        
        name_length = len(name)
        
        if name_length < 1 or name_length > 100:
            raise AssertionError(
                f'`name` length can be in range [1:100], got {name_length}; {name!r}.'
            )
    
    channel_data = {
        'name': name,
        'type': channel_type_value,
    }
    
    if not issubclass(channel_type, ChannelThread):
        if permission_overwrites is ...:
            permission_overwrites = []
        else:
            if __debug__:
                if not isinstance(permission_overwrites, list):
                    raise AssertionError(
                        f'`permission_overwrites` can be `None`, `list` of '
                        f'`cr_p_permission_overwrite_object` returns, got {permission_overwrites.__class__.__name__}; '
                        f'{permission_overwrites!r}.'
                    )
                
                for index, element in enumerate(permission_overwrites):
                    if not isinstance(element, dict):
                        raise AssertionError(
                            f'`permission_overwrites`\'s element {index} should be `dict`, '
                            f'but got {element.__class__.__name__}; {element!r}.'
                        )
        
        channel_data['permission_overwrites'] = permission_overwrites
    
    
    if (topic is not ...):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelStage)):
                raise AssertionError(
                    f'`topic` is a valid parameter only for `{ChannelText.__name__}` and for '
                    f'{ChannelStage.__name__} instances, got {channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(topic, str):
                raise AssertionError(
                    f'`topic` can be `str`, got {topic.__class__.__name__}; {topic!r}.'
                )
            
            if issubclass(channel_type, ChannelText):
                topic_length_limit = 1024
            else:
                topic_length_limit = 120
            
            topic_length = len(topic)
            if topic_length > topic_length_limit:
                raise AssertionError(
                    f'`topic` length can be in range [0:{topic_length_limit}], got {topic_length}; {topic!r}.'
                )
        
        channel_data['topic'] = topic
    
    
    if (nsfw is not ...):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelStore)):
                raise AssertionError(
                    f'`nsfw` is a valid parameter only for `{ChannelText.__name__}` and '
                    f'`{ChannelStore.__name__}`, got {channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(nsfw, bool):
                raise AssertionError(
                    f'`nsfw` can be `bool`, got {nsfw.__class__.__name__}; {nsfw!r}.'
                )
        
        channel_data['nsfw'] = nsfw
    
    
    if (slowmode is not ...):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelThread)):
                raise AssertionError(
                    f'`slowmode` is a valid parameter only for `{ChannelText.__name__}` and for '
                    f'`{ChannelThread.__name__}`, got {channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(slowmode, int):
                raise AssertionError(
                    f'`slowmode` can be `int`, got {slowmode.__class__.__name__}; {slowmode!r}.'
                )
            
            if slowmode < 0 or slowmode > 21600:
                raise AssertionError(
                    f'`slowmode` can be in range [0:21600], got: {slowmode!r}.'
                )
        
        channel_data['rate_limit_per_user'] = slowmode
    
    
    if (banner is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelText):
                raise AssertionError(
                    f'`banner` is a valid parameter only for `{ChannelText.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
        if not isinstance(banner, (bytes, bytearray, memoryview)):
            raise TypeError(
                f'`banner` can be `None`, `bytes-like`, got '
                f'{banner.__class__.__name__}; got {reprlib.repr(banner)}.'
            )
        
        if __debug__:
            media_type = get_image_media_type(banner)
            if media_type not in VALID_ICON_MEDIA_TYPES:
                raise AssertionError(
                    f'Invalid `banner` type: {media_type}; got {reprlib.repr(banner)}.'
                )
        
        banner_data = image_to_base64(banner)
    
        data['banner'] = banner_data
    
    
    if (bitrate is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(
                    f'`bitrate` is a valid parameter only for `{ChannelVoiceBase.__name__}`, '
                    f'got {channel_type.__name__}; {type_!r}.'
                )
                
            if not isinstance(bitrate, int):
                raise AssertionError(
                    f'`bitrate` can be `int`, got {bitrate.__class__.__name__}; {bitrate!r}.'
                )
            
            # Get max bitrate
            if guild is None:
                bitrate_limit = 384000
            else:
                bitrate_limit = guild.bitrate_limit
            
            if bitrate < 8000 or bitrate > bitrate_limit:
                raise AssertionError(
                    f'`bitrate` is out of the expected [8000:{bitrate_limit}] range, got {bitrate!r}.'
                )
        
        channel_data['bitrate'] = bitrate
    
    
    if (user_limit is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(
                    f'`user_limit` is a valid parameter only for `{ChannelVoiceBase.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(user_limit, int):
                raise AssertionError(
                    f'`user_limit` can be `int`, got {user_limit.__class__.__name__}; '
                    f'{user_limit!r}.'
                )
            
            if user_limit < 0 or user_limit > 99:
                raise AssertionError(
                    '`user_limit`\'s value is out of the expected [0:99] range, got '
                    f'{user_limit!r}.'
                )
        
        channel_data['user_limit'] = user_limit
    
    
    if (region is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(
                    f'`region` is a valid parameter only for `{ChannelVoiceBase.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
        
        if isinstance(region, VoiceRegion):
            region_value = region.value
        elif isinstance(region, str):
            region_value = region
        else:
            raise TypeError(
                f'`region` can be `None`, `str`, `{VoiceRegion.__name__}`, got '
                f'{region.__class__.__name__}; {region!r}.'
            )
        
        channel_data['rtc_region'] = region_value
    
    
    if (video_quality_mode is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelVoice):
                raise AssertionError(
                    f'`video_quality_mode` is a valid parameter only for `{ChannelVoice.__name__}` got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
        
        if isinstance(video_quality_mode, VideoQualityMode):
            video_quality_mode_value = video_quality_mode.value
        elif isinstance(video_quality_mode, int):
            video_quality_mode_value = video_quality_mode
        else:
            raise TypeError(
                f'`video_quality_mode` can be `None`, `str`, `{VideoQualityMode.__name__}`, got '
                f'{video_quality_mode.__class__.__name__}; {video_quality_mode!r}.'
            )
        
        channel_data['video_quality_mode'] = video_quality_mode_value
    
    
    if (archived is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(
                    f'`archived` is a valid parameter only for `{ChannelThread.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(archived, bool):
                raise AssertionError(
                    f'`archived` can be `None`, `bool`, got {archived.__class__.__name__}; {archived!r}.'
                )
        
        channel_data['archived'] = archived
    
    
    if (archived_at is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(
                    f'`archived_at` is a valid parameter only for `{ChannelThread.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(archived_at, datetime):
                raise AssertionError(
                    f'`archived_at` can be `None`, `datetime`, got {archived_at.__class__.__name__}; {archived_at!r}.'
                )
        
        channel_data['archive_timestamp'] =  datetime_to_timestamp(archived_at)
    
    
    if (auto_archive_after is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(
                    f'`auto_archive_after` is a valid parameter only for `{ChannelThread.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(auto_archive_after, int):
                raise AssertionError(
                    f'`auto_archive_after` can be `None`, `datetime`, got {auto_archive_after.__class__.__name__}; '
                    f'{auto_archive_after!r}.'
                )
            
            if auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                raise AssertionError(
                    f'`auto_archive_after` can be any of: {AUTO_ARCHIVE_OPTIONS}, got {auto_archive_after}.'
                )
        
        channel_data['auto_archive_duration'] = auto_archive_after // 60
    
    
    if (default_auto_archive_after is not ...):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelForum)):
                raise AssertionError(
                    f'`default_auto_archive_after` is a valid parameter only for `{ChannelText.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(default_auto_archive_after, int):
                raise AssertionError(
                    f'`default_auto_archive_after` can be `None`, `datetime`, got '
                    f'{default_auto_archive_after.__class__.__name__}; {default_auto_archive_after!r}.'
                )
            
            if default_auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                raise AssertionError(
                    f'`default_auto_archive_after` can be any of: {AUTO_ARCHIVE_OPTIONS}, got '
                    f'{default_auto_archive_after}.'
                )
        
        channel_data['default_auto_archive_duration'] = default_auto_archive_after // 60
    
    
    if (open_ is not ...):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(
                    f'`open_` is a valid parameter only for `{ChannelThread.__name__}`, got '
                    f'{channel_type.__name__}; {type_!r}.'
                )
            
            if not isinstance(open_, bool):
                raise AssertionError(
                    f'`open_` can be `None`, `bool`, got {open_.__class__.__name__}; {open_!r}.'
                )
        
        channel_data['locked'] = not open_
    
    
    if parent is None:
        parent_id = 0
    elif isinstance(parent, ChannelCategory):
        parent_id = parent.id
    else:
        parent_id = maybe_snowflake(parent)
        if parent_id is None:
            raise TypeError(
                f'`parent` can be `{ChannelCategory.__name__}`, `{Guild.__name__}`, `int`, got '
                f'{parent.__class__.__name__}; {parent!r}.'
            )
    
    if parent_id:
        if __debug__:
            if issubclass(channel_type, ChannelCategory):
                raise AssertionError(
                    f'`parent` was given, but the respective channel type is '
                    f'{channel_type.__name__}; {type_!r}, which cannot be put under other categories.'
                )
        
        channel_data['parent_id'] = parent_id
    
    
    return channel_data


@export
def parse_permission_overwrites(data):
    """
    Parses the permission overwrites from the given data and returns them.
    
    Parameters
    ----------
    data : `list` of (`dict` of (`str`, `Any`) items) elements
        A list of permission overwrites' data.
    
    Returns
    -------
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
    """
    permission_overwrites = {}
    
    permission_overwrites_datas = data.get('permission_overwrites', None)
    if (permission_overwrites_datas is not None) and permission_overwrites_datas:
        for permission_overwrite_data in permission_overwrites_datas:
            permission_overwrite = PermissionOverwrite(permission_overwrite_data)
            permission_overwrites[permission_overwrite.target_id] = permission_overwrite
    
    return permission_overwrites
