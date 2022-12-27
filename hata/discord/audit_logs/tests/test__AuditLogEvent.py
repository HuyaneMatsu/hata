import vampytest

from ..preinstanced import AuditLogEvent, AuditLogTargetType


def test__AuditLogEvent__name():
    """
    Tests whether ``AuditLogEvent` instance names are all strings.
    """
    for instance in AuditLogEvent.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AuditLogEvent__value():
    """
    Tests whether ``AuditLogEvent` instance values are all the expected value type.
    """
    for instance in AuditLogEvent.INSTANCES.values():
        vampytest.assert_instance(instance.value, AuditLogEvent.VALUE_TYPE)



def test__AuditLogEvent__target_type():
    """
    Tests whether ``AuditLogEvent` instance `.target_type`-s are all ``AuditLogTargetType` instances
    """
    for instance in AuditLogEvent.INSTANCES.values():
        vampytest.assert_instance(instance.target_type, AuditLogTargetType,)
