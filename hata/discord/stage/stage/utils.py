__all__ = ()

from .fields import (
    put_privacy_level, put_scheduled_event_id, put_send_start_notification, put_topic,
    validate_privacy_level, validate_scheduled_event_id, validate_send_start_notification, validate_topic
)


STAGE_CREATE_FIELD_CONVERTERS = {
    'privacy_level': (validate_privacy_level, put_privacy_level),
    'scheduled_event': (validate_scheduled_event_id, put_scheduled_event_id),
    'scheduled_event_id': (validate_scheduled_event_id, put_scheduled_event_id),
    'send_start_notification': (validate_send_start_notification, put_send_start_notification),
    'topic': (validate_topic, put_topic),
}

STAGE_EDIT_FIELD_CONVERTERS = {
    'privacy_level': (validate_privacy_level, put_privacy_level),
    'topic': (validate_topic, put_topic),
}
