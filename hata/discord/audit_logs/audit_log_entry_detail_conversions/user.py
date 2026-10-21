__all__ = ()

from ...integration import IntegrationType
from ...integration.integration.fields import validate_type as validate_integration_type
from ...user.voice_state.fields import validate_channel_id, validate_user_id

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_serializer_id

from .helpers import (
    convert_string_to_boolean, convert_string_to_integer, serialise_boolean_to_string, serialise_integer_to_string
)


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
    value_deserializer = convert_string_to_integer,
    value_serializer = serialise_integer_to_string,
)


@COUNT_CONVERSION.set_value_validator
def validate_count(value):
    if not isinstance(value, int):
        raise TypeError(f'`count` can be `int`, got {type(value).__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`count` cannot be negative, got {value!r}.')
    
    return value


# ---- delete_message_duration ----

DELETE_MESSAGE_DURATION_CONVERSION = AuditLogEntryDetailConversion(
    'delete_message_seconds',
    'delete_message_duration',
    value_deserializer = convert_string_to_integer,
    value_serializer = serialise_integer_to_string,
)


@DELETE_MESSAGE_DURATION_CONVERSION.set_value_validator
def validate_delete_message_duration(value):
    if not isinstance(value, int):
        raise TypeError(f'`delete_message_duration` can be `int`, got {type(value).__name__}; {value!r}.')
    
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
    return convert_string_to_integer(value) * (24 * 60 * 60)


@DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION.set_value_serializer
def delete_message_days_value_serializer(value):
    return str(value // (24 * 60 * 60))


# ---- integration_type ----

INTEGRATION_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'integration_type', 'integration_type', value_validator = validate_integration_type
)


@INTEGRATION_TYPE_CONVERSION.set_value_deserializer
def integration_type_value_deserializer(value):
    return IntegrationType(value)


@INTEGRATION_TYPE_CONVERSION.set_value_serializer
def integration_type_value_serializer(value):
    return value.value


# ---- unique_count ----

UNIQUE_COUNT_CONVERSION = AuditLogEntryDetailConversion(
    'unique_count',
    'unique_count',
    value_deserializer = convert_string_to_integer,
    value_serializer = serialise_integer_to_string,
)


@UNIQUE_COUNT_CONVERSION.set_value_validator
def validate_unique_count(value):
    if not isinstance(value, int):
        raise TypeError(f'`unique_count` can be `int`, got {type(value).__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`unique_count` cannot be negative, got {value!r}.')
    
    return value


# ---- unique_count_overflown ----

UNIQUE_COUNT_OVERFLOWN_CONVERSION = AuditLogEntryDetailConversion(
    'unique_overflow',
    'unique_count_overflown',
    value_deserializer = convert_string_to_boolean,
    value_serializer = serialise_boolean_to_string,
)


@UNIQUE_COUNT_OVERFLOWN_CONVERSION.set_value_validator
def validate_unique_count_overflown(value):
    if not isinstance(value, bool):
        raise TypeError(f'`unique_count_overflown` can be `bool`, got {type(value).__name__}; {value!r}.')
    
    return value


# ---- user_id ----

USER_ID_CONVERSION = AuditLogEntryDetailConversion(
    'member_id',
    'user_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_user_id,
)

# ---- Construct ----

USER_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    CHANNEL_ID_CONVERSION,
    COUNT_CONVERSION,
    DELETE_MESSAGE_DURATION_CONVERSION,
    INTEGRATION_TYPE_CONVERSION,
    UNIQUE_COUNT_CONVERSION,
    UNIQUE_COUNT_OVERFLOWN_CONVERSION,
    USER_ID_CONVERSION,
    
    # Deprecations
    DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION,
)
