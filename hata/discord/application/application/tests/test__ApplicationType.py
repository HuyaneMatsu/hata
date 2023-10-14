import vampytest

from ..preinstanced import ApplicationType


def test__ApplicationType__name():
    """
    Tests whether ``ApplicationType`` instance names are all strings.
    """
    for instance in ApplicationType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationType__value():
    """
    Tests whether ``ApplicationType`` instance values are all the expected value type.
    """
    for instance in ApplicationType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationType.VALUE_TYPE)
