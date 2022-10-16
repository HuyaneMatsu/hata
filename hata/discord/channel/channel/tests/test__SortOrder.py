import vampytest

from ..preinstanced import SortOrder


def test__SortOrder__name():
    """
    Tests whether ``SortOrder`` instance names are all strings.
    """
    for instance in SortOrder.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SortOrder__value():
    """
    Tests whether ``SortOrder`` instance values are all the expected value type.
    """
    for instance in SortOrder.INSTANCES.values():
        vampytest.assert_instance(instance.value, SortOrder.VALUE_TYPE)
