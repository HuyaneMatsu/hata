__all__ = ()

from ...integration import IntegrationType
from ...integration.integration.fields import validate_type as validate_integration_type

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup


# ---- count ----

COUNT_CONVERSION = AuditLogEntryDetailConversion(
    'count',
    'count',
)

@COUNT_CONVERSION.set_validator
def validate_count(value):
    if not isinstance(value, int):
        raise TypeError(f'`count` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`count` cannot be negative, got {value!r}.')
    
    return value


# ---- integration_type ----

INTEGRATION_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'integration_type', 'integration_type', validator = validate_integration_type
)


@INTEGRATION_TYPE_CONVERSION.set_get_converter
def integration_type_get_converter(value):
    return IntegrationType.get(value)


@INTEGRATION_TYPE_CONVERSION.set_put_converter
def integration_type_put_converter(value):
    return value.value


# ---- Construct ----

USER_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    COUNT_CONVERSION,
    INTEGRATION_TYPE_CONVERSION,
)
