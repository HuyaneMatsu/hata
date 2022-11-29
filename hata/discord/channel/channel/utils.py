__all__ = ('cr_pg_channel_object', 'create_partial_channel_from_data', 'create_partial_channel_from_id')

import warnings
from functools import partial as partial_func

from scarletio import export, include

from ...core import CHANNELS

from ..channel_metadata.base import CHANNEL_METADATA_ICON_SLOT
from ..channel_metadata.fields import (
    put_applied_tag_ids_into, put_auto_archive_after_into, put_bitrate_into, put_default_thread_auto_archive_after_into,
    put_default_thread_reaction_into, put_default_thread_slowmode_into, put_flags_into, put_invitable_into,
    put_name_into, put_nsfw_into, put_open_into, put_parent_id_into, put_permission_overwrites_into, put_position_into,
    put_region_into, put_slowmode_into, put_topic_into, put_user_limit_into, put_video_quality_mode_into,
    validate_applied_tag_ids, validate_auto_archive_after, validate_bitrate, validate_default_thread_auto_archive_after,
    validate_default_thread_reaction, validate_default_thread_slowmode, validate_flags, validate_invitable,
    validate_name, validate_nsfw, validate_open, validate_parent_id, validate_permission_overwrites, validate_position,
    validate_region, validate_slowmode, validate_topic, validate_user_limit, validate_video_quality_mode,
    validate_default_sort_order, put_default_sort_order_into
)

from .preinstanced import ChannelType


Channel = include('Channel')


CHANNEL_GUILD_MAIN_FIELD_CONVERTERS = {
    'bitrate': (validate_bitrate, put_bitrate_into),
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
    channel : `None`, ``Channel``
        The created partial channel, or `None`, if no data was received.
    """
    if (data is None) or (not data):
        return None
    
    channel_id = int(data['id'])
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
    """
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    channel = Channel._create_empty(channel_id, channel_type, guild_id)
    CHANNELS[channel_id] = channel
    
    return channel


HAS_SLOWMODE = (
    *(
        channel_type for channel_type in ChannelType.INSTANCES.values()
        if channel_type.flags.guild and channel_type.flags.textual
    ),
    ChannelType.guild_forum,
)



def cr_pg_channel_object(name, channel_type, *, guild = None, **keyword_parameters):
    """
    Deprecated, please use `Channel(..).to_data(...)` instead.
    
    Will be removed in 2023 February.
    """
    warnings.warn(
        (
            f'`cr_pg_channel_object` is deprecated and will be removed in 2023 February. '
            f'Please use `Channel(..).to_data(...)` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )
    return Channel(channel_type = channel_type, name = name, **keyword_parameters).to_data()
