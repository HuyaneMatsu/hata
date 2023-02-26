import vampytest

from ..preinstanced import ApplicationCommandTargetType


def test__ApplicationCommandTargetType__name():
    """
    Tests whether ``ApplicationCommandTargetType`` instance names are all strings.
    """
    for instance in ApplicationCommandTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationCommandTargetType__value():
    """
    Tests whether ``ApplicationCommandTargetType`` instance values are all the expected value type.
    """
    for instance in ApplicationCommandTargetType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationCommandTargetType.VALUE_TYPE)
