from types import FunctionType, MethodType

import vampytest

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversionGroup
from ...audit_log_entry_detail_conversion import AuditLogEntryDetailConversionGroup

from ..preinstanced import AuditLogEntryType, AuditLogEntryTargetType


def test__AuditLogEntryType():
    """
    Tests whether ``AuditLogEntryType` instance are set up correctly.
    """
    for instance in AuditLogEntryType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)
        vampytest.assert_instance(instance.value, AuditLogEntryType.VALUE_TYPE)
        vampytest.assert_instance(instance.target_type, AuditLogEntryTargetType)


def test__AuditLogEntryTargetType():
    """
    Tests whether ``AuditLogEntryTargetType` instance are set up correctly.
    """
    for instance in AuditLogEntryTargetType.INSTANCES.values():
        vampytest.assert_instance(instance, AuditLogEntryTargetType)
        vampytest.assert_instance(instance.name, str)
        vampytest.assert_instance(instance.value, AuditLogEntryTargetType.VALUE_TYPE)
        vampytest.assert_instance(instance.change_conversions, AuditLogEntryChangeConversionGroup, nullable = True)
        vampytest.assert_instance(instance.detail_conversions, AuditLogEntryDetailConversionGroup, nullable = True)
        vampytest.assert_instance(instance.target_converter, FunctionType, MethodType, nullable = True)
