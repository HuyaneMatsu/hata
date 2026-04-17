__all__ = ()

from ...invite import InviteFlag
from ...invite.invite.fields import (
    validate_channel_id, validate_code, validate_flags, validate_inviter_id, validate_max_age, validate_max_uses,
    validate_temporary, validate_uses
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('channel_id',),
    'channel_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_channel_id,
)


# ---- code ----

CODE_CONVERSION = AuditLogEntryChangeConversion(
    ('code',),
    'code',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_code,
)


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    ('flags',),
    'flags',
    value_validator = validate_flags,
)


@FLAGS_CONVERSION.set_value_deserializer
def flags_value_deserializer(value):
    if value is None:
        value = InviteFlag()
    else:
        value = InviteFlag(value)
    
    return value


@FLAGS_CONVERSION.set_value_serializer
def flags_value_serializer(value):
    return int(value)


# ---- inviter_id ----

INVITER_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('inviter_id',),
    'inviter_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_inviter_id,
)


# ---- max_age ----

MAX_AGE_CONVERSION = AuditLogEntryChangeConversion(
    ('max_age',),
    'max_age',
    value_validator = validate_max_age,
)


# ---- max_uses ----

MAX_USES_CONVERSION = AuditLogEntryChangeConversion(
    ('max_uses',),
    'max_uses',
    value_validator = validate_max_uses,
)


# ---- uses ----

USES_CONVERSION = AuditLogEntryChangeConversion(
    ('uses',),
    'uses',
    value_validator = validate_uses,
)

# ----

@MAX_AGE_CONVERSION.set_value_deserializer
@MAX_USES_CONVERSION.set_value_deserializer
@USES_CONVERSION.set_value_deserializer
def max_value_deserializer(value):
    if value is None:
        value = 0
    return value


# ---- temporary ----

TEMPORARY_CONVERSION = AuditLogEntryChangeConversion(
    ('temporary',),
    'temporary',
    value_validator = validate_temporary,
)


@TEMPORARY_CONVERSION.set_value_deserializer
def temporary_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- Construct ----

INVITE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    CHANNEL_ID_CONVERSION,
    CODE_CONVERSION,
    FLAGS_CONVERSION,
    INVITER_ID_CONVERSION,
    MAX_AGE_CONVERSION,
    MAX_USES_CONVERSION,
    TEMPORARY_CONVERSION,
    USES_CONVERSION,
)
