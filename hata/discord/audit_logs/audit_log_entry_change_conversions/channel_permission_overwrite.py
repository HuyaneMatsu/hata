__all__ = ()

from ...channel import PermissionOverwriteTargetType
from ...channel.permission_overwrite.fields import (
    validate_allow, validate_deny, validate_target_id, validate_target_type
)
from ...permission import Permission
from ...permission.constants import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_id, put_converter_id


# ---- allow ----

ALLOW_CONVERSION = AuditLogEntryChangeConversion(
    PERMISSION_ALLOW_KEY,
    'allow',
    FLAG_IS_MODIFICATION,
    validator = validate_allow,
)


# ---- deny ----

DENY_CONVERSION = AuditLogEntryChangeConversion(
    PERMISSION_DENY_KEY,
    'deny',
    FLAG_IS_MODIFICATION,
    validator = validate_deny,
)


# ----

@ALLOW_CONVERSION.set_get_converter
@DENY_CONVERSION.set_get_converter
def permission_get_converter(value):
    if value is None:
        value = Permission()
    else:
        value = Permission(value)
    return value


@ALLOW_CONVERSION.set_put_converter
@DENY_CONVERSION.set_put_converter
def permission_put_converter(value):
    return format(value, 'd')


# ---- target_id ----

TARGET_ID_CONVERSION = AuditLogEntryChangeConversion(
    'id',
    'target_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_target_id,
)


# ---- target_type ----

TARGET_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'type',
    'target_type',
    FLAG_IS_MODIFICATION,
    validator = validate_target_type,
)


@TARGET_TYPE_CONVERSION.set_get_converter
def target_type_get_converter(value):
    if (value is not None) and (PermissionOverwriteTargetType.VALUE_TYPE is int):
        value = int(value)
    
    return PermissionOverwriteTargetType.get(value)


@TARGET_TYPE_CONVERSION.set_put_converter
def target_type_put_converter(value):
    return str(value.value)


# ---- Construct ----

CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    ALLOW_CONVERSION,
    DENY_CONVERSION,
    TARGET_ID_CONVERSION,
    TARGET_TYPE_CONVERSION,
)
