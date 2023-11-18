import vampytest

from ....application_command.application_command_permission.fields import validate_permission_overwrites

from ...audit_log_entry_change_conversion.change_deserializers import (
    change_deserializer_application_command_permission_overwrite
)
from ...audit_log_entry_change_conversion.change_serializers import (
    change_serializer_application_command_permission_overwrite
)
from ...audit_log_entry_change_conversion.key_pre_checks import key_pre_check_id
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...audit_log_entry_change_conversion.value_mergers import value_merger_sorted_array

from ..application_command import APPLICATION_COMMAND_CONVERSIONS, PERMISSION_OVERWRITE_CONVERSION


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `APPLICATION_COMMAND_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(APPLICATION_COMMAND_CONVERSIONS)
    vampytest.assert_eq(
        {*APPLICATION_COMMAND_CONVERSIONS.iter_field_keys()},
        {'\\d+'},
    )


# ---- permission_overwrite ----

def test__PERMISSION_OVERWRITE_CONVERSION__generic():
    """
    Tests whether ``PERMISSION_OVERWRITE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PERMISSION_OVERWRITE_CONVERSION)
    vampytest.assert_is(PERMISSION_OVERWRITE_CONVERSION.value_validator, validate_permission_overwrites)
    
    vampytest.assert_is(PERMISSION_OVERWRITE_CONVERSION.change_deserialization_key_pre_check, key_pre_check_id)
    vampytest.assert_is(PERMISSION_OVERWRITE_CONVERSION.value_merger, value_merger_sorted_array)
    vampytest.assert_is(
        PERMISSION_OVERWRITE_CONVERSION.change_deserializer,
        change_deserializer_application_command_permission_overwrite,
    )
    vampytest.assert_is(
        PERMISSION_OVERWRITE_CONVERSION.change_serializer,
        change_serializer_application_command_permission_overwrite,
    )

