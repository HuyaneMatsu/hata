__all__ = ()

from ...invite import InviteFlag
from ...invite.invite.fields import (
    validate_channel_id, validate_code, validate_flags, validate_inviter_id, validate_max_age, validate_max_uses,
    validate_temporary, validate_uses
)

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name


# ---- channel_id ----

CHANNEL_ID_CONVERSION = AuditLogEntryChangeConversion(
    'channel_id',
    'channel_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_channel_id,
)


# ---- code ----

CODE_CONVERSION = AuditLogEntryChangeConversion(
    'code',
    'code',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_code,
)


# ---- flags ----

FLAGS_CONVERSION = AuditLogEntryChangeConversion(
    'flags',
    'flags',
    FLAG_IS_MODIFICATION,
    validator = validate_flags,
)


@FLAGS_CONVERSION.set_get_converter
def flags_get_converter(value):
    if value is None:
        value = InviteFlag()
    else:
        value = InviteFlag(value)
    
    return value


@FLAGS_CONVERSION.set_put_converter
def flags_put_converter(value):
    return int(value)


# ---- inviter_id ----

INVITER_ID_CONVERSION = AuditLogEntryChangeConversion(
    'inviter_id',
    'inviter_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_inviter_id,
)


# ---- max_age ----

MAX_AGE_CONVERSION = AuditLogEntryChangeConversion(
    'max_age',
    'max_age',
    FLAG_IS_MODIFICATION,
    validator = validate_max_age,
)


# ---- max_uses ----

MAX_USES_CONVERSION = AuditLogEntryChangeConversion(
    'max_uses',
    'max_uses',
    FLAG_IS_MODIFICATION,
    validator = validate_max_uses,
)


# ---- uses ----

USES_CONVERSION = AuditLogEntryChangeConversion(
    'uses',
    'uses',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_uses,
)

# ----

@MAX_AGE_CONVERSION.set_get_converter
@MAX_USES_CONVERSION.set_get_converter
@USES_CONVERSION.set_get_converter
def max_get_converter(value):
    if value is None:
        value = 0
    return value


# ---- temporary ----

TEMPORARY_CONVERSION = AuditLogEntryChangeConversion(
    'temporary',
    'temporary',
    FLAG_IS_MODIFICATION,
    validator = validate_temporary,
)


@TEMPORARY_CONVERSION.set_get_converter
def temporary_get_converter(value):
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
