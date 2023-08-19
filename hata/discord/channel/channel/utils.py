__all__ = (
    'create_partial_channel_data', 'create_partial_channel_from_data', 'create_partial_channel_from_id', 
)

from functools import partial as partial_func

from scarletio import export, include

from ...core import CHANNELS

from ..channel_metadata.base import CHANNEL_METADATA_ICON_SLOT
from ..channel_metadata.fields import (
    put_applied_tag_ids_into, put_auto_archive_after_into, put_bitrate_into, put_default_forum_layout_into,
    put_default_sort_order_into, put_default_thread_auto_archive_after_into, put_default_thread_reaction_into,
    put_default_thread_slowmode_into, put_flags_into, put_invitable_into, put_name_into, put_nsfw_into, put_open_into,
    put_parent_id_into, put_permission_overwrites_into, put_position_into, put_region_into, put_slowmode_into,
    put_topic_into, put_user_limit_into, put_video_quality_mode_into, validate_applied_tag_ids,
    validate_auto_archive_after, validate_bitrate, validate_default_forum_layout, validate_default_sort_order,
    validate_default_thread_auto_archive_after, validate_default_thread_reaction, validate_default_thread_slowmode,
    validate_flags, validate_invitable, validate_name, validate_nsfw, validate_open, validate_parent_id,
    validate_permission_overwrites, validate_position, validate_region, validate_slowmode, validate_topic,
    validate_user_limit, validate_video_quality_mode
)

from .fields import parse_id, put_guild_id_into, put_id_into, put_type_into, validate_type
from .preinstanced import ChannelType


Channel = include('Channel')


CHANNEL_GUILD_MAIN_FIELD_CONVERTERS = {
    'bitrate': (validate_bitrate, put_bitrate_into),
    'channel_type': (validate_type, put_type_into),
    'default_forum_layout': (validate_default_forum_layout, put_default_forum_layout_into),
    'default_sort_order': (validate_default_sort_order, put_default_sort_order_into),
    'default_thread_auto_archive_after': (
        validate_default_thread_auto_archive_after, put_default_thread_auto_archive_after_into
    ),
    'default_thread_reaction': (validate_default_thread_reaction, put_default_thread_reaction_into),
    'default_thread_slowmode': (validate_default_thread_slowmode, put_default_thread_slowmode_into),
    'flags': (validate_flags, put_flags_into),
    'name': (validate_name, put_name_into),
    'nsfw': (validate_nsfw, put_nsfw_into),
    'parent_id': (validate_parent_id, put_parent_id_into),
    'permission_overwrites': (validate_permission_overwrites, put_permission_overwrites_into),
    'position': (validate_position, put_position_into),
    'region': (validate_region, put_region_into),
    'slowmode': (validate_slowmode, put_slowmode_into),
    'topic': (validate_topic, put_topic_into),
    'user_limit': (validate_user_limit, put_user_limit_into),
    'video_quality_mode': (validate_video_quality_mode, put_video_quality_mode_into),
}


CHANNEL_PRIVATE_GROUP_FIELD_CONVERTERS = {
    'icon': (
        CHANNEL_METADATA_ICON_SLOT.validate_icon,
        partial_func(CHANNEL_METADATA_ICON_SLOT.put_into, as_data = True),
    ),
    'name': (validate_name, put_name_into),
}


CHANNEL_GUILD_THREAD_FIELD_CONVERTERS = {
    'applied_tag_ids': (validate_applied_tag_ids, put_applied_tag_ids_into),
    'auto_archive_after': (
        validate_auto_archive_after, partial_func(put_auto_archive_after_into, flatten_thread_metadata = True)
    ),
    'flags': (validate_flags, put_flags_into),
    'invitable': (validate_invitable, partial_func(put_invitable_into, flatten_thread_metadata = True)),
    'name': (validate_name, put_name_into),
    'open_': (validate_open, partial_func(put_open_into, flatten_thread_metadata = True)),
    'slowmode': (validate_slowmode, put_slowmode_into),
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
    data : `None`, `dict` of (`str`, `object`) items
        Partial channel data received from Discord.
    guild_id : `int` = `0`, Optional (Keyword only)
        The channel's guild's identifier.
    
    Returns
    -------
    channel : `None`, ``Channel``
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
    data : `dict` of (`str`, `object`) items
    """
    data = {}
    put_id_into(channel.id, data, True)
    put_guild_id_into(channel.guild_id, data, True)
    put_type_into(channel.type, data, True)
    put_name_into(channel.name, data, True)
    return data


HAS_SLOWMODE = (
    *(
        channel_type for channel_type in ChannelType.INSTANCES.values()
        if channel_type.flags.guild and (channel_type.flags.textual or channel_type.flags.forum)
    ),
)
