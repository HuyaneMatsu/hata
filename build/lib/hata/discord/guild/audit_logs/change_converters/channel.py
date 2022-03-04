__all__ = ()

from ....channel import VideoQualityMode
from ....permission import PermissionOverwrite

from ...preinstanced import VoiceRegion

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_icon, convert_nothing, convert_snowflake


def convert_bool__open(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = not before
    
    after = data.get('new_value', None)
    if (after is not None):
        after = not after
    
    return AuditLogChange('open', before, after)


def convert_int__auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('auto_archive_after', before, after)


def convert_int__default_auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('default_auto_archive_after', before, after)


def convert_int__slowmode(name, data):
    return convert_nothing('slowmode', data)


def convert_overwrites(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = [PermissionOverwrite(overwrite_data) for overwrite_data in before]
    
    after = data.get('new_value', None)
    if (after is not None):
        after = [PermissionOverwrite(overwrite_data) for overwrite_data in after]
    
    return AuditLogChange('overwrites', before, after)


def convert_video_quality_mode(name, data):
    return _convert_preinstanced(name, data, VideoQualityMode)


def convert_voice_region(name, data):
    return _convert_preinstanced('region', data, VoiceRegion)


CHANNEL_CONVERTERS = {
    'archived': convert_nothing,
    'auto_archive_duration': convert_int__auto_archive_after,
    'banner_hash': convert_icon,
    'bitrate': convert_nothing,
    'default_auto_archive_duration': convert_int__default_auto_archive_after,
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
