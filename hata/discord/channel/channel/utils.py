__all__ = (
    'create_partial_channel_data', 'create_partial_channel_from_data', 'create_partial_channel_from_id', 
)

from functools import partial as partial_func
from warnings import warn

from scarletio import export, include

from ...core import CHANNELS

from ..channel_metadata.private_group import CHANNEL_METADATA_ICON
from ..channel_metadata.fields import (
    put_applied_tag_ids, put_auto_archive_after, put_bitrate, put_default_forum_layout,
    put_default_sort_order, put_default_thread_auto_archive_after, put_default_thread_reaction_emoji,
    put_default_thread_slowmode, put_flags, put_invitable, put_name, put_nsfw, put_open,
    put_parent_id, put_permission_overwrites, put_position, put_region, put_slowmode,
    put_topic, put_user_limit, put_video_quality_mode, validate_applied_tag_ids,
    validate_auto_archive_after, validate_bitrate, validate_default_forum_layout, validate_default_sort_order,
    validate_default_thread_auto_archive_after, validate_default_thread_reaction_emoji, validate_default_thread_slowmode,
    validate_flags, validate_invitable, validate_name, validate_nsfw, validate_open, validate_parent_id,
    validate_permission_overwrites, validate_position, validate_region, validate_slowmode, validate_topic,
    validate_user_limit, validate_video_quality_mode
)

from .fields import parse_id, put_guild_id, put_id, put_type, validate_type
from .preinstanced import ChannelType


Channel = include('Channel')


def _deprecated__validate_default_thread_reaction(emoji):
    warn(
        '`default_thread_reaction` parameter is deprecated. Please use `default_thread_reaction_emoji` instead.',
        FutureWarning,
        stacklevel = 4,
    )
    return validate_default_thread_reaction_emoji(emoji)


CHANNEL_GUILD_MAIN_FIELD_CONVERTERS = {
    'bitrate': (validate_bitrate, put_bitrate),
    'channel_type': (validate_type, put_type),
    'default_forum_layout': (validate_default_forum_layout, put_default_forum_layout),
    'default_sort_order': (validate_default_sort_order, put_default_sort_order),
    'default_thread_auto_archive_after': (
        validate_default_thread_auto_archive_after, put_default_thread_auto_archive_after
    ),
    'default_thread_reaction': (_deprecated__validate_default_thread_reaction, put_default_thread_reaction_emoji),
    'default_thread_reaction_emoji': (validate_default_thread_reaction_emoji, put_default_thread_reaction_emoji),
    'default_thread_slowmode': (validate_default_thread_slowmode, put_default_thread_slowmode),
    'flags': (validate_flags, put_flags),
    'name': (validate_name, put_name),
    'nsfw': (validate_nsfw, put_nsfw),
    'parent_id': (validate_parent_id, put_parent_id),
    'permission_overwrites': (validate_permission_overwrites, put_permission_overwrites),
    'position': (validate_position, put_position),
    'region': (validate_region, put_region),
    'slowmode': (validate_slowmode, put_slowmode),
    'topic': (validate_topic, put_topic),
    'user_limit': (validate_user_limit, put_user_limit),
    'video_quality_mode': (validate_video_quality_mode, put_video_quality_mode),
}


CHANNEL_PRIVATE_GROUP_FIELD_CONVERTERS = {
    'icon': (
        CHANNEL_METADATA_ICON.validate_icon,
        partial_func(CHANNEL_METADATA_ICON.put_into, as_data = True),
    ),
    'name': (validate_name, put_name),
}


CHANNEL_GUILD_THREAD_FIELD_CONVERTERS = {
    'applied_tags': (validate_applied_tag_ids, put_applied_tag_ids),
    'applied_tag_ids': (validate_applied_tag_ids, put_applied_tag_ids),
    'auto_archive_after': (
        validate_auto_archive_after, partial_func(put_auto_archive_after, flatten_thread_metadata = True)
    ),
    'flags': (validate_flags, put_flags),
    'invitable': (validate_invitable, partial_func(put_invitable, flatten_thread_metadata = True)),
    'name': (validate_name, put_name),
    'open_': (validate_open, partial_func(put_open, flatten_thread_metadata = True)),
    'slowmode': (validate_slowmode, put_slowmode),
}


CHANNEL_GUILD_FIELD_CONVERTERS = {
    **CHANNEL_GUILD_THREAD_FIELD_CONVERTERS,
    **CHANNEL_GUILD_MAIN_FIELD_CONVERTERS,
}


@export
def create_partial_channel_from_data(data, guild_id = 0):
    """
    Creates a partial channel from partial channel data.
    
    Parameters
    ----------
    data : `None`, `dict<str, object>`
        Partial channel data received from Discord.
    guild_id : `int` = `0`, Optional (Keyword only)
        The channel's guild's identifier.
    
    Returns
    -------
    channel : ``None | Channel``
        The created partial channel, or `None`, if no data was received.
    """
    channel_id = parse_id(data)
    
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    channel = Channel._from_partial_data(data, channel_id, guild_id)
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
    channel_type : ``ChannelType``
        The channel's type.
    guild_id : `int`
        A guild's identifier of the created channel.
    
    Returns
    -------
    channel : ``Channel``
    """
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    channel = Channel._create_empty(channel_id, channel_type, guild_id)
    CHANNELS[channel_id] = channel
    
    return channel


@export
def create_partial_channel_data(channel):
    """
    Creates partial channel data for the given channel.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to create the partial data from.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_id(channel.id, data, True)
    put_guild_id(channel.guild_id, data, True)
    put_type(channel.type, data, True)
    put_name(channel.name, data, True)
    return data


HAS_SLOWMODE = (
    *(
        channel_type for channel_type in ChannelType.INSTANCES.values()
        if channel_type.flags.guild and (channel_type.flags.textual or channel_type.flags.forum)
    ),
)
