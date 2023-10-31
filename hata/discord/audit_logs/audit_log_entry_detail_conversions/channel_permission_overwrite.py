__all__ = ()

from ...channel import PermissionOverwriteTargetType
from ...channel.permission_overwrite.fields import validate_target_id, validate_target_type
from ...role.role.fields import validate_name

from ..audit_log_entry_detail_conversion import AuditLogEntryDetailConversion, AuditLogEntryDetailConversionGroup
from ..conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name


# ---- role_name ----

ROLE_NAME_CONVERSION = AuditLogEntryDetailConversion(
    'role_name',
    'role_name',
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- target_id ----

TARGET_ID_CONVERSION = AuditLogEntryDetailConversion(
    'id',
    'target_id',
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_target_id,
)


# ---- target_type ----

TARGET_TYPE_CONVERSION = AuditLogEntryDetailConversion(
    'type',
    'target_type',
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

CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS = AuditLogEntryDetailConversionGroup(
    ROLE_NAME_CONVERSION,
    TARGET_ID_CONVERSION,
    TARGET_TYPE_CONVERSION,
)
