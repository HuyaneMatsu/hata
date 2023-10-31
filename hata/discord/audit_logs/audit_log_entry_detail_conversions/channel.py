__all__ = ()

from ...channel.channel_metadata.fields import validate_status

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import get_converter_description, put_converter_description


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
    STATUS_CONVERSION,
)
