__all__ = ()

from ...stage.stage.fields import validate_channel_id

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_serializer_id


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


# ---- Construct ----

STAGE_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
)
