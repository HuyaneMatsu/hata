import vampytest

from ..preinstanced import ApplicationRoleConnectionMetadataType, ApplicationRoleConnectionValueType


def test__ApplicationRoleConnectionMetadataType__name():
    """
    Tests whether ``ApplicationRoleConnectionMetadataType`` instance names are all strings.
    """
    for instance in ApplicationRoleConnectionMetadataType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationRoleConnectionMetadataType__value():
    """
    Tests whether ``ApplicationRoleConnectionMetadataType`` instance values are all the expected value type.
    """
    for instance in ApplicationRoleConnectionMetadataType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationRoleConnectionMetadataType.VALUE_TYPE)


def test__ApplicationRoleConnectionMetadataType__value_type():
    """
    Tests whether ``ApplicationRoleConnectionMetadataType.value_type``-s are all set correctly.
    """
    for instance in ApplicationRoleConnectionMetadataType.INSTANCES.values():
        vampytest.assert_instance(instance.value_type, ApplicationRoleConnectionValueType)
