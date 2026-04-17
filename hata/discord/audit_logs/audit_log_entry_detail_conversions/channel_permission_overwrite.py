__all__ = ()

from ...channel import PermissionOverwriteTargetType
from ...channel.permission_overwrite.fields import validate_target_id, validate_target_type
from ...role.role.fields import validate_name

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)


# ---- role_name ----

ROLE_NAME_CONVERSION = AuditLogEntryDetailConversion(
    'role_name',
    'role_name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- target_id ----

TARGET_ID_CONVERSION = AuditLogEntryDetailConversion(
    'id',
    'target_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_target_id,
)


# ---- target_type ----

TARGET_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'type',
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

CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    ROLE_NAME_CONVERSION,
    TARGET_ID_CONVERSION,
    TARGET_TYPE_CONVERSION,
)
