__all__ = ()

from ...channel.channel.fields import validate_id
from ...channel.channel_metadata.fields import validate_status

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_serializer_description, value_serializer_id
)


# ---- id ----

ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_id,
)


# ---- status ----

STATUS_CONVERSION = AuditLogEntryDetailConversion(
    'status',
    'status',
    value_deserializer = value_deserializer_description,
    value_serializer = value_serializer_description,
    value_validator = validate_status,
)


# ---- Construct ----

CHANNEL_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    ID_CONVERSION,
    STATUS_CONVERSION,
)
