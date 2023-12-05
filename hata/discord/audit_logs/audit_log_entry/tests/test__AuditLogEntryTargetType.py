from types import FunctionType, MethodType

import vampytest

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversionGroup
from ...audit_log_entry_detail_conversion import AuditLogEntryDetailConversionGroup

from ..preinstanced import AuditLogEntryTargetType


@vampytest.call_from(AuditLogEntryTargetType.INSTANCES.values())
def test__AuditLogEntryTargetType__instances(instance):
    """
    Tests whether ``AuditLogEntryTargetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AuditLogEntryTargetType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AuditLogEntryTargetType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AuditLogEntryTargetType.VALUE_TYPE)
    vampytest.assert_instance(instance.change_conversions, AuditLogEntryChangeConversionGroup, nullable = True)
    vampytest.assert_instance(instance.detail_conversions, AuditLogEntryDetailConversionGroup, nullable = True)
    vampytest.assert_instance(instance.target_converter, FunctionType, MethodType, nullable = True)


