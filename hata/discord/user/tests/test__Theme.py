import vampytest

from ..preinstanced import Theme


def test__Theme__name():
    """
    Tests whether ``Theme`` instance names are all strings.
    """
    for instance in Theme.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__Theme__value():
    """
    Tests whether ``Theme`` instance values are all the expected value type.
    """
    for instance in Theme.INSTANCES.values():
        vampytest.assert_instance(instance.value, Theme.VALUE_TYPE)
