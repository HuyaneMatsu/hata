import vampytest

from ..preinstanced import TextInputStyle


def test__TextInputStyle__name():
    """
    Tests whether ``TextInputStyle`` instance names are all strings.
    """
    for instance in TextInputStyle.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__TextInputStyle__value():
    """
    Tests whether ``TextInputStyle`` instance values are all the expected value type.
    """
    for instance in TextInputStyle.INSTANCES.values():
        vampytest.assert_instance(instance.value, TextInputStyle.VALUE_TYPE)
