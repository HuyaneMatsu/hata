import vampytest

from ..preinstanced import ReactionType


def test__ReactionType__name():
    """
    Tests whether ``ReactionType`` instance names are all strings.
    """
    for instance in ReactionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ReactionType__value():
    """
    Tests whether ``ReactionType`` instance values are all the expected value type.
    """
    for instance in ReactionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ReactionType.VALUE_TYPE)
