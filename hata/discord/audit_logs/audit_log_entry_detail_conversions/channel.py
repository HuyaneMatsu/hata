__all__ = ()

from ...channel.channel.fields import validate_id
from ...channel.channel_metadata.fields import validate_status

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import (
    get_converter_description, get_converter_id, put_converter_description, put_converter_id
)


# ---- id ----

ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'id',
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_id,
)


# ---- status ----

STATUS_CONVERSION = AuditLogEntryDetailConversion(
    'status',
    'status',
    get_converter = get_converter_description,
    put_converter = put_converter_description,
    validator = validate_status,
)


# ---- Construct ----

CHANNEL_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    ID_CONVERSION,
    STATUS_CONVERSION,
)
