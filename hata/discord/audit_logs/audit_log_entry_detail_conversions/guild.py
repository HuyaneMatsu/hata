__all__ = ()

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup


# ---- delete_message_duration ----

DELETE_MESSAGE_DURATION_CONVERSION = AuditLogEntryDetailConversion(
    'delete_message_seconds',
    'delete_message_duration',
)


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


# ---- users_removed ----

USERS_REMOVED_CONVERSION = AuditLogEntryDetailConversion(
    'members_removed',
    'users_removed',
)


@USERS_REMOVED_CONVERSION.set_validator
def validate_delete_message_duration(value):
    if not isinstance(value, int):
        raise TypeError(f'`users_removed` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`users_removed` cannot be negative, got {value!r}.')
    
    return value


# Construct

GUILD_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    DELETE_MESSAGE_DURATION_CONVERSION,
    USERS_REMOVED_CONVERSION,
    
    # Deprecations
    DELETE_MESSAGE_DURATION_DEPRECATED_DAYS_CONVERSION,
)
