__all__ = ()

from .fields import (
    put_cancelled, put_end, put_start, put_timestamp, validate_cancelled, validate_end, validate_start,
    validate_timestamp
)


SCHEDULED_EVENT_OCCASION_OVERWRITE_CREATE_FIELD_CONVERTERS = {
    'cancelled': (validate_cancelled, put_cancelled),
    'end': (validate_end, put_end),
    'start': (validate_start, put_start),
    'timestamp': (validate_timestamp, put_timestamp),
}

SCHEDULED_EVENT_OCCASION_OVERWRITE_EDIT_FIELD_CONVERTERS = SCHEDULED_EVENT_OCCASION_OVERWRITE_CREATE_FIELD_CONVERTERS
