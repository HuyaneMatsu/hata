from types import FunctionType, MethodType

import vampytest

from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversionGroup
from ...audit_log_entry_detail_conversion import AuditLogEntryDetailConversionGroup

from ..preinstanced import AuditLogEntryTargetType


def _assert_fields_set(audit_log_entry_target_type):
    """
    Asserts whether every field are set of the given audit log entry target type.
    
    Parameters
    ----------
    audit_log_entry_target_type : ``AuditLogEntryTargetType``
        The instance to test.
    """
    vampytest.assert_instance(audit_log_entry_target_type, AuditLogEntryTargetType)
    vampytest.assert_instance(audit_log_entry_target_type.name, str)
    vampytest.assert_instance(audit_log_entry_target_type.value, AuditLogEntryTargetType.VALUE_TYPE)
    vampytest.assert_instance(
        audit_log_entry_target_type.change_conversions, AuditLogEntryChangeConversionGroup, nullable = True
    )
    vampytest.assert_instance(
        audit_log_entry_target_type.detail_conversions, AuditLogEntryDetailConversionGroup, nullable = True
    )
    vampytest.assert_instance(audit_log_entry_target_type.target_converter, FunctionType, MethodType, nullable = True)


@vampytest.call_from(AuditLogEntryTargetType.INSTANCES.values())
def test__AuditLogEntryTargetType__instances(instance):
    """
    Tests whether ``AuditLogEntryTargetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AuditLogEntryTargetType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__AuditLogEntryTargetType__new__min_fields():
    """
    Tests whether ``AuditLogEntryTargetType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = AuditLogEntryTargetType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AuditLogEntryTargetType.NAME_DEFAULT)
        vampytest.assert_is(output.change_conversions, None)
        vampytest.assert_is(output.detail_conversions, None)
        vampytest.assert_is(output.target_converter, None)
        vampytest.assert_is(AuditLogEntryTargetType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AuditLogEntryTargetType.INSTANCES[value]
        except KeyError:
            pass
