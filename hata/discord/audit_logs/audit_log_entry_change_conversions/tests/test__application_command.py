import vampytest

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)

from ..application_command import APPLICATION_COMMAND_CONVERSIONS


def test__APPLICATION_COMMAND_CONVERSIONS():
    """
    Tests whether `APPLICATION_COMMAND_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(APPLICATION_COMMAND_CONVERSIONS)
    vampytest.assert_eq(
        {*APPLICATION_COMMAND_CONVERSIONS.get_converters.keys()},
        set(),
    )

