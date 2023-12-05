import vampytest

from ..preinstanced import AuditLogEntryType, AuditLogEntryTargetType


@vampytest.call_from(AuditLogEntryType.INSTANCES.values())
def test__AuditLogEntryType__instances(instance):
    """
    Tests whether ``AuditLogEntryType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AuditLogEntryType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AuditLogEntryType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AuditLogEntryType.VALUE_TYPE)
    vampytest.assert_instance(instance.target_type, AuditLogEntryTargetType)
