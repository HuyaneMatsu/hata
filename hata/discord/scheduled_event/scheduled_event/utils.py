__all__ = ()

from .fields import (
    put_description, put_end, put_name, put_privacy_level, put_schedule, put_start,
    put_status, put_target, validate_description, validate_end, validate_name, validate_privacy_level,
    validate_schedule, validate_start, validate_status, validate_target_location, validate_target_stage,
    validate_target_voice
)


SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS = {
    'description': (validate_description, put_description),
    'end': (validate_end, put_end),
    'location': (validate_target_location, put_target),
    'name': (validate_name, put_name),
    'privacy_level': (validate_privacy_level, put_privacy_level),
    'schedule': (validate_schedule, put_schedule),
    'stage': (validate_target_stage, put_target),
    'start': (validate_start, put_start),
    'voice': (validate_target_voice, put_target),
}

SCHEDULED_EVENT_EDIT_FIELD_CONVERTERS = {
    **SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS,
    'status': (validate_status, put_status),
}
