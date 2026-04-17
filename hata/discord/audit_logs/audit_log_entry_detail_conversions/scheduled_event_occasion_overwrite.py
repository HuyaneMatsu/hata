__all__ = ()

from ...scheduled_event.scheduled_event_occasion_overwrite.fields import validate_timestamp
from ...utils import DISCORD_EPOCH_START, datetime_to_id, id_to_datetime

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_serializer_id


# ---- timestamp ----

TIMESTAMP_CONVERSION = AuditLogEntryDetailConversion(
    'event_exception_id',
    'timestamp',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_timestamp,
)


@TIMESTAMP_CONVERSION.set_value_deserializer
def timestamp_value_deserializer(value):
    if value is None:
        return DISCORD_EPOCH_START

    return id_to_datetime(int(value))


@TIMESTAMP_CONVERSION.set_value_serializer
def timestamp_value_serializer(value):
    return str(datetime_to_id(value))


# ---- Construct ----

SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    TIMESTAMP_CONVERSION,
)
