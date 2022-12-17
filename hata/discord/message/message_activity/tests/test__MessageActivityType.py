import vampytest

from ..preinstanced import MessageActivityType


def test__MessageActivityType__name():
    """
    Tests whether ``MessageActivityType`` instance names are all strings.
    """
    for instance in MessageActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__MessageActivityType__value():
    """
    Tests whether ``MessageActivityType`` instance values are all the expected value type.
    """
    for instance in MessageActivityType.INSTANCES.values():
        vampytest.assert_instance(instance.value, MessageActivityType.VALUE_TYPE)
