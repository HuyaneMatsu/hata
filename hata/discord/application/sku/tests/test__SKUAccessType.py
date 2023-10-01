import vampytest

from ..preinstanced import SKUAccessType


def test__SKUAccessType__name():
    """
    Tests whether ``SKUAccessType`` instance names are all strings.
    """
    for instance in SKUAccessType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SKUAccessType__value():
    """
    Tests whether ``SKUAccessType`` instance values are all the expected value type.
    """
    for instance in SKUAccessType.INSTANCES.values():
        vampytest.assert_instance(instance.value, SKUAccessType.VALUE_TYPE)
