__all__ = ()

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup

from .helpers import convert_string_to_integer, serialise_integer_to_string

# ---- days ----

DAYS_CONVERSION = AuditLogEntryDetailConversion(
    'delete_member_days',
    'days',
    value_deserializer = convert_string_to_integer,
    value_serializer = serialise_integer_to_string,
)


@DAYS_CONVERSION.set_value_validator
def days_value_validator(value):
    if not isinstance(value, int):
        raise TypeError(f'`days` can be `int`, got {type(value).__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`days` cannot be negative, got {value!r}.')
    
    return value


# ---- users_removed ----

USERS_REMOVED_CONVERSION = AuditLogEntryDetailConversion(
    'members_removed',
    'users_removed',
    value_deserializer = convert_string_to_integer,
    value_serializer = serialise_integer_to_string,
)

@USERS_REMOVED_CONVERSION.set_value_validator
def users_removed_value_validator(value):
    if not isinstance(value, int):
        raise TypeError(f'`users_removed` can be `int`, got {type(value).__name__}; {value!r}.')
    
    if value < 0:
        raise ValueError(f'`users_removed` cannot be negative, got {value!r}.')
    
    return value


# Construct

GUILD_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    DAYS_CONVERSION,
    USERS_REMOVED_CONVERSION,
)
