__all__ = ()

from ...integration import IntegrationType
from ...integration.integration.fields import validate_type as validate_integration_type

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup


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



# ---- delete_message_duration ----

DELETE_MESSAGE_DURATION_CONVERSION = AuditLogEntryDetailConversion(
    'delete_message_seconds',
    'delete_message_duration',
)


@DELETE_MESSAGE_DURATION_CONVERSION.set_get_converter
def delete_message_duration_get_converter(value):
    if value is None:
        value = 0
    return value


@DELETE_MESSAGE_DURATION_CONVERSION.set_validator
def validate_delete_message_duration(value):
    if not isinstance(value, int):
        raise TypeError(f'`delete_message_duration` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`delete_message_duration` cannot be negative, got {value!r}.')
    
    return value


# ---- delete_message_duration | deprecated version ----

DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION = AuditLogEntryDetailConversion(
    'delete_message_days',
    'delete_message_duration',
)


@DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION.set_get_converter
def delete_message_days_get_converter(value):
    return value * 24 * 60 * 60


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
    DELETE_MESSAGE_DURATION_CONVERSION,
    INTEGRATION_TYPE_CONVERSION,
    
    # Deprecations
    DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION,
)
