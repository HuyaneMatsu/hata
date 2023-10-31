__all__ = ()

from ...message.message.fields import validate_channel_id, validate_id

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import get_converter_id, put_converter_id


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryDetailConversion(
    'channel_id',
    'channel_id',
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_channel_id,
)


# ---- count ----

COUNT_CONVERSION = AuditLogEntryDetailConversion(
    'count',
    'count',
)

@COUNT_CONVERSION.set_get_converter
def count_get_converter(value):
    if value is None:
        value = 0
    return value


@COUNT_CONVERSION.set_validator
def validate_count(value):
    if not isinstance(value, int):
        raise TypeError(f'`count` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`count` cannot be negative, got {value!r}.')
    
    return value


# ---- id ----

ID_CONVERSION = AuditLogEntryDetailConversion(
    'message_id',
    'id',
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_id,
)


# ---- Construct ----

MESSAGE_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
    COUNT_CONVERSION,
    ID_CONVERSION,
)
