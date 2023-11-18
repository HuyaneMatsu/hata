__all__ = ()

from ...emoji.emoji.fields import validate_available, validate_name, validate_role_ids

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_ids, value_deserializer_name, value_serializer_ids, value_serializer_name
)


# ---- available ----

AVAILABLE_CONVERSION = AuditLogEntryChangeConversion(
    ('available',),
    'available',
    value_validator = validate_available,
)


@AVAILABLE_CONVERSION.set_value_deserializer
def available_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- role_ids ----

ROLE_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('roles',),
    'role_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_role_ids,
)


# ---- Construct ----

EMOJI_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    AVAILABLE_CONVERSION,
    NAME_CONVERSION,
    ROLE_IDS_CONVERSION,
)
