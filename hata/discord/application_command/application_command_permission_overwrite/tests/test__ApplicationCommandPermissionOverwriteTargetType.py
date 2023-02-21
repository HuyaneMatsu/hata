import vampytest

from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def test__ApplicationCommandPermissionOverwriteTargetType__name():
    """
    Tests whether ``ApplicationCommandPermissionOverwriteTargetType`` instance names are all strings.
    """
    for instance in ApplicationCommandPermissionOverwriteTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationCommandPermissionOverwriteTargetType__value():
    """
    Tests whether ``ApplicationCommandPermissionOverwriteTargetType`` instance values are all the expected value type.
    """
    for instance in ApplicationCommandPermissionOverwriteTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationCommandPermissionOverwriteTargetType.VALUE_TYPE)
