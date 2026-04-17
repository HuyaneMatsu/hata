__all__ = ()

from ...channel import PermissionOverwriteTargetType
from ...channel.permission_overwrite.fields import (
    validate_allow, validate_deny, validate_target_id, validate_target_type
)
from ...permission import Permission
from ...permission.constants import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_id, value_serializer_id


# ---- allow ----

ALLOW_CONVERSION = AuditLogEntryChangeConversion(
    (PERMISSION_ALLOW_KEY,),
    'allow',
    value_validator = validate_allow,
)


# ---- deny ----

DENY_CONVERSION = AuditLogEntryChangeConversion(
    (PERMISSION_DENY_KEY,),
    'deny',
    value_validator = validate_deny,
)


# ----

@ALLOW_CONVERSION.set_value_deserializer
@DENY_CONVERSION.set_value_deserializer
def permission_value_deserializer(value):
    if value is None:
        value = Permission()
    else:
        value = Permission(value)
    return value


@ALLOW_CONVERSION.set_value_serializer
@DENY_CONVERSION.set_value_serializer
def permission_value_serializer(value):
    return format(value, 'd')


# ---- target_id ----

TARGET_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('id',),
    'target_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_target_id,
)


# ---- target_type ----

TARGET_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('type',),
    'target_type',
    value_validator = validate_target_type,
)


@TARGET_TYPE_CONVERSION.set_value_deserializer
def target_type_value_deserializer(value):
    if (value is not None) and (PermissionOverwriteTargetType.VALUE_TYPE is int):
        value = int(value)
    
    return PermissionOverwriteTargetType(value)


@TARGET_TYPE_CONVERSION.set_value_serializer
def target_type_value_serializer(value):
    return str(value.value)


# ---- Construct ----

CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    ALLOW_CONVERSION,
    DENY_CONVERSION,
    TARGET_ID_CONVERSION,
    TARGET_TYPE_CONVERSION,
)
