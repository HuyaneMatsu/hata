__all__ = ()

from ...scheduled_event.scheduled_event_occasion_overwrite.fields import (
    validate_cancelled, validate_end, validate_start
)
from ...utils import datetime_to_timestamp, timestamp_to_datetime

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup


# ---- cancelled ----

CANCELLED_CONVERSION = AuditLogEntryChangeConversion(
    ('is_canceled',),
    'cancelled',
    value_validator = validate_cancelled,
)


@CANCELLED_CONVERSION.set_value_deserializer
def cancelled_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- end ----

END_CONVERSION = AuditLogEntryChangeConversion(
    ('scheduled_end_time',),
    'end',
    value_validator = validate_end,
)


# ---- start ----

START_CONVERSION = AuditLogEntryChangeConversion(
    ('scheduled_start_time',),
    'start',
    value_validator = validate_start,
)

# ----

@END_CONVERSION.set_value_deserializer
@START_CONVERSION.set_value_deserializer
def date_time_converter_get(value):
    if (value is not None):
        value = timestamp_to_datetime(value)
    return value

@END_CONVERSION.set_value_serializer
@START_CONVERSION.set_value_serializer
def date_time_converter_put(value):
    if (value is not None):
        value = datetime_to_timestamp(value)
    return value


# ---- Construct ----

SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    CANCELLED_CONVERSION,
    END_CONVERSION,
    START_CONVERSION,
)
