import vampytest

from ..preinstanced import ConnectionVisibility


def test__ConnectionVisibility__name():
    """
    Tests whether ``ConnectionVisibility`` instance names are all strings.
    """
    for instance in ConnectionVisibility.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ConnectionVisibility__value():
    """
    Tests whether ``ConnectionVisibility`` instance values are all the expected value type.
    """
    for instance in ConnectionVisibility.INSTANCES.values():
        vampytest.assert_instance(instance.value, ConnectionVisibility.VALUE_TYPE)
