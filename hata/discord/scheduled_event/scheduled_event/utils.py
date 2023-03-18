__all__ = ()

from .fields import (
    put_description_into, put_end_into, put_name_into, put_privacy_level_into, put_start_into, put_status_into,
    put_target_into, validate_description, validate_end, validate_name, validate_privacy_level, validate_start,
    validate_status, validate_target_location, validate_target_stage, validate_target_voice
)


SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS = {
    'description': (validate_description, put_description_into),
    'end': (validate_end, put_end_into),
    'location': (validate_target_location, put_target_into),
    'name': (validate_name, put_name_into),
    'privacy_level': (validate_privacy_level, put_privacy_level_into),
    'stage': (validate_target_stage, put_target_into),
    'start': (validate_start, put_start_into),
    'voice': (validate_target_voice, put_target_into),
}

SCHEDULED_EVENT_EDIT_FIELD_CONVERTERS = {
    **SCHEDULED_EVENT_CREATE_FIELD_CONVERTERS,
    'status': (validate_status, put_status_into),
}
