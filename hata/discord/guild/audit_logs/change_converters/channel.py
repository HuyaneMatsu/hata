__all__ = ()

from ....channel import ChannelFlag, ForumTag, SortOrder, VideoQualityMode, VoiceRegion
from ....emoji import create_emoji_from_exclusive_data
from ....permission import PermissionOverwrite

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_nothing, convert_snowflake, convert_snowflake_array


def convert_snowflake_array__applied_tag_ids(name, data):
    return convert_snowflake_array('applied_tag_ids', data)


def convert_bool__open(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = not before
    
    after = data.get('new_value', None)
    if (after is not None):
        after = not after
    
    return AuditLogChange('open', before, after)


def convert_channel_flags(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = ChannelFlag(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = ChannelFlag(after)
    
    return AuditLogChange('flags', before, after)


def convert_int__auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('auto_archive_after', before, after)


def convert_forum_tags(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        if before:
            before = tuple(sorted(ForumTag.from_data(tag_data) for tag_data in before))
        else:
            before = None
    
    after = data.get('new_value', None)
    if (after is not None):
        if after:
            after = tuple(sorted(ForumTag.from_data(tag_data) for tag_data in after))
        else:
            after = None
    
    return AuditLogChange('available_tags', before, after)


def convert_int__default_thread_auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('default_thread_auto_archive_after', before, after)


def convert_int__slowmode(name, data):
    return convert_nothing('slowmode', data)


def convert_int__default_thread_slowmode(name, data):
    return convert_nothing('default_thread_slowmode', data)


def convert_overwrites(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = [PermissionOverwrite.from_data(overwrite_data) for overwrite_data in before]
    
    after = data.get('new_value', None)
    if (after is not None):
        after = [PermissionOverwrite.from_data(overwrite_data) for overwrite_data in after]
    
    return AuditLogChange('overwrites', before, after)


def convert_video_quality_mode(name, data):
    return _convert_preinstanced('video_quality_mode', data, VideoQualityMode)


def convert_voice_region(name, data):
    return _convert_preinstanced('region', data, VoiceRegion)


def convert_default_thread_reaction(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = create_emoji_from_exclusive_data(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = create_emoji_from_exclusive_data(after)
    
    return AuditLogChange('default_thread_reaction', before, after) 


def default_sort_order(name, data):
    return _convert_preinstanced('default_sort_order', data, SortOrder)


CHANNEL_CONVERTERS = {
    'applied_tags': convert_snowflake_array__applied_tag_ids,
    'archived': convert_nothing,
    'auto_archive_duration': convert_int__auto_archive_after,
    'available_tags': convert_forum_tags,
    'bitrate': convert_nothing,
    'default_sort_order': default_sort_order,
    'default_auto_archive_duration': convert_int__default_thread_auto_archive_after,
    'default_reaction_emoji': convert_default_thread_reaction,
    'default_thread_rate_limit_per_user': convert_int__default_thread_slowmode,
    'flags': convert_channel_flags,
    'invitable': convert_nothing,
    'locked': convert_bool__open,
    'name': convert_nothing,
    'nsfw': convert_nothing,
    'rate_limit_per_user': convert_int__slowmode,
    'parent_id': convert_snowflake,
    'permission_overwrites': convert_overwrites,
    'position': convert_nothing,
    'rtc_region': convert_voice_region,
    'topic': convert_nothing,
    'type': convert_nothing,
    'video_quality_mode': convert_video_quality_mode,
    'user_limit': convert_nothing,
}
