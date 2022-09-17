__all__ = ()

from ....scheduled_event import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ....scheduled_event.metadata.utils import try_get_scheduled_event_metadata_type_from_data

from ..audit_log_change import AuditLogChange

from .shared import (
    _convert_preinstanced, convert_icon, convert_nothing, convert_snowflake, convert_snowflake_array,
    convert_timestamp
)


def convert_scheduled_event_entity_metadata(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        metadata_type = try_get_scheduled_event_metadata_type_from_data(before)
        if metadata_type is None:
            before = None
        else:
            before = metadata_type.from_data(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        metadata_type = try_get_scheduled_event_metadata_type_from_data(after)
        if metadata_type is None:
            after = None
        else:
            after = metadata_type.from_data(after)
    
    return AuditLogChange('entity_metadata', before, after)


def convert_scheduled_event_entity_type(name, data):
    return _convert_preinstanced('entity_type', data, ScheduledEventEntityType)


def convert_timestamp__end(name, data):
    return convert_timestamp('end', data)


def convert_timestamp__start(name, data):
    return convert_timestamp('start', data)


def convert_scheduled_event_status(name, data):
    return _convert_preinstanced('status', data, ScheduledEventStatus)


def convert_privacy_level(name, data):
    return _convert_preinstanced('privacy_level', data, PrivacyLevel)


SCHEDULED_EVENT_CONVERTERS = {
    'channel_id': convert_snowflake,
    'description': convert_nothing,
    'entity_id': convert_snowflake,
    'entity_metadata' : convert_scheduled_event_entity_metadata,
    'entity_type': convert_scheduled_event_entity_type,
    'image': convert_icon,
    'location': convert_nothing,
    'name': convert_nothing,
    'privacy_level': convert_privacy_level,
    'scheduled_end_time': convert_timestamp__end,
    'scheduled_start_time': convert_timestamp__start,
    'send_start_notification': convert_nothing,
    'sku_ids': convert_snowflake_array,
    'status': convert_scheduled_event_status,
}
