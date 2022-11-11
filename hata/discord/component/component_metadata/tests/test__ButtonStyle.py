import vampytest

from ..preinstanced import ButtonStyle


def test__ButtonStyle__name():
    """
    Tests whether ``ButtonStyle`` instance names are all strings.
    """
    for instance in ButtonStyle.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ButtonStyle__value():
    """
    Tests whether ``ButtonStyle`` instance values are all the expected value type.
    """
    for instance in ButtonStyle.INSTANCES.values():
        vampytest.assert_instance(instance.value, ButtonStyle.VALUE_TYPE)
