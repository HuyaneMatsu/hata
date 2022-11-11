import vampytest

from ..preinstanced import RoleManagerType


def test__RoleManagerType__name():
    """
    Tests whether ``RoleManagerType`` instance names are all strings.
    """
    for instance in RoleManagerType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__RoleManagerType__value():
    """
    Tests whether ``RoleManagerType`` instance values are all the expected value type.
    """
    for instance in RoleManagerType.INSTANCES.values():
        vampytest.assert_instance(instance.value, RoleManagerType.VALUE_TYPE)
