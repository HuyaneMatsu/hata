__all__ = ()

from .fields import (
    put_privacy_level_into, put_scheduled_event_id_into, put_send_start_notification_into, put_topic_into,
    validate_privacy_level, validate_scheduled_event_id, validate_send_start_notification, validate_topic
)


STAGE_CREATE_FIELD_CONVERTERS = {
    'privacy_level': (validate_privacy_level, put_privacy_level_into),
    'scheduled_event': (validate_scheduled_event_id, put_scheduled_event_id_into),
    'scheduled_event_id': (validate_scheduled_event_id, put_scheduled_event_id_into),
    'send_start_notification': (validate_send_start_notification, put_send_start_notification_into),
    'topic': (validate_topic, put_topic_into),
}

STAGE_EDIT_FIELD_CONVERTERS = {
    'privacy_level': (validate_privacy_level, put_privacy_level_into),
    'topic': (validate_topic, put_topic_into),
}
