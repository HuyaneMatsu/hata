__all__ = ()

from ...integration import IntegrationType
from ...integration.integration.fields import validate_type as validate_integration_type
from ...user.voice_state.fields import validate_channel_id

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


# ---- count ----

COUNT_CONVERSION = AuditLogEntryDetailConversion(
    'count',
    'count',
)

@COUNT_CONVERSION.set_value_deserializer
def count_value_deserializer(value):
    if value is None:
        value = 0
    return value


@COUNT_CONVERSION.set_value_validator
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


@DELETE_MESSAGE_DURATION_CONVERSION.set_value_deserializer
def delete_message_duration_value_deserializer(value):
    if value is None:
        value = 0
    return value


@DELETE_MESSAGE_DURATION_CONVERSION.set_value_validator
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


@DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION.set_value_deserializer
def delete_message_days_value_deserializer(value):
    return value * 24 * 60 * 60


# ---- integration_type ----

INTEGRATION_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'integration_type', 'integration_type', value_validator = validate_integration_type
)


@INTEGRATION_TYPE_CONVERSION.set_value_deserializer
def integration_type_value_deserializer(value):
    return IntegrationType.get(value)


@INTEGRATION_TYPE_CONVERSION.set_value_serializer
def integration_type_value_serializer(value):
    return value.value


# ---- Construct ----

USER_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
    COUNT_CONVERSION,
    DELETE_MESSAGE_DURATION_CONVERSION,
    INTEGRATION_TYPE_CONVERSION,
    
    # Deprecations
    DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION,
)
