__all__ = ()

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup


# ---- days ----

DAYS_CONVERSION = AuditLogEntryDetailConversion(
    'delete_member_days',
    'days',
)


@DAYS_CONVERSION.set_value_deserializer
def days_value_deserializer(value):
    if value is None:
        value = 0
    return value


@DAYS_CONVERSION.set_value_validator
def days_value_validator(value):
    if not isinstance(value, int):
        raise TypeError(f'`days` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`days` cannot be negative, got {value!r}.')
    
    return value


# ---- users_removed ----

USERS_REMOVED_CONVERSION = AuditLogEntryDetailConversion(
    'members_removed',
    'users_removed',
)


@USERS_REMOVED_CONVERSION.set_value_deserializer
def users_removed_value_deserializer(value):
    if value is None:
        value = 0
    return value


@USERS_REMOVED_CONVERSION.set_value_validator
def users_removed_value_validator(value):
    if not isinstance(value, int):
        raise TypeError(f'`users_removed` can be `int`, got {value.__class__.__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`users_removed` cannot be negative, got {value!r}.')
    
    return value


# Construct

GUILD_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    DAYS_CONVERSION,
    USERS_REMOVED_CONVERSION,
)
