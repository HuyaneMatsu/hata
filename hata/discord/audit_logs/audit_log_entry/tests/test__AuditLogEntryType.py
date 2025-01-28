import vampytest

from ..preinstanced import AuditLogEntryType, AuditLogEntryTargetType


def _assert_fields_set(audit_log_entry_type):
    """
    Asserts whether every field are set of the given audit log entry type.
    
    Parameters
    ----------
    audit_log_entry_type : ``AuditLogEntryType``
        The instance to test.
    """
    vampytest.assert_instance(audit_log_entry_type, AuditLogEntryType)
    vampytest.assert_instance(audit_log_entry_type.name, str)
    vampytest.assert_instance(audit_log_entry_type.value, AuditLogEntryType.VALUE_TYPE)
    vampytest.assert_instance(audit_log_entry_type.target_type, AuditLogEntryTargetType)


@vampytest.call_from(AuditLogEntryType.INSTANCES.values())
def test__AuditLogEntryType__instances(instance):
    """
    Tests whether ``AuditLogEntryType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AuditLogEntryType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__AuditLogEntryType__new__min_fields():
    """
    Tests whether ``AuditLogEntryType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 20000
    
    try:
        output = AuditLogEntryType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AuditLogEntryType.NAME_DEFAULT)
        vampytest.assert_is(output.target_type, AuditLogEntryTargetType.none)
        vampytest.assert_is(AuditLogEntryType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AuditLogEntryType.INSTANCES[value]
        except KeyError:
            pass
