import vampytest

from .. import SKUType


def test__SKUType__name():
    """
    Tests whether ``SKUType`` instance names are all strings.
    """
    for instance in SKUType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SKUType__value():
    """
    Tests whether ``SKUType`` instance values are all the expected value type.
    """
    for instance in SKUType.INSTANCES.values():
        vampytest.assert_instance(instance.value, SKUType.VALUE_TYPE)
