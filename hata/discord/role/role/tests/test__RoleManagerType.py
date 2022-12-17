import vampytest

from ...role_manager_metadata import RoleManagerMetadataBase

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


def test__RoleManagerType__metadata_type():
    """
    Tests whether ``RoleManagerType.metadata_type``-s are set correctly.
    """
    for instance in RoleManagerType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, RoleManagerMetadataBase)
