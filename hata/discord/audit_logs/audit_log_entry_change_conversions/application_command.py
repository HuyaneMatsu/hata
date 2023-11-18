__all__ = ()

from ...application_command.application_command_permission.fields import validate_permission_overwrites

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import (
    change_deserializer_application_command_permission_overwrite
)
from ..audit_log_entry_change_conversion.change_serializers import (
    change_serializer_application_command_permission_overwrite
)
from ..audit_log_entry_change_conversion.key_pre_checks import key_pre_check_id
from ..audit_log_entry_change_conversion.value_mergers import value_merger_sorted_array


# ---- permission_overwrite ----

PERMISSION_OVERWRITE_CONVERSION = AuditLogEntryChangeConversion(
    ('\\d+',),
    'permission_overwrites',
    change_deserialization_key_pre_check = key_pre_check_id,
    change_deserializer = change_deserializer_application_command_permission_overwrite,
    change_serializer = change_serializer_application_command_permission_overwrite,
    value_merger = value_merger_sorted_array,
    value_validator = validate_permission_overwrites
)

# ---- Construct ----

APPLICATION_COMMAND_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    PERMISSION_OVERWRITE_CONVERSION,
)
