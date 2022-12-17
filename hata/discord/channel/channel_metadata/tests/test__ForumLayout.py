import vampytest

from ..preinstanced import ForumLayout


def test__ForumLayout__name():
    """
    Tests whether ``ForumLayout`` instance names are all strings.
    """
    for instance in ForumLayout.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ForumLayout__value():
    """
    Tests whether ``ForumLayout`` instance values are all the expected value type.
    """
    for instance in ForumLayout.INSTANCES.values():
        vampytest.assert_instance(instance.value, ForumLayout.VALUE_TYPE)
