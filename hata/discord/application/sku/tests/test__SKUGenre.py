import vampytest

from ..preinstanced import SKUGenre


def test__SKUGenre__name():
    """
    Tests whether ``SKUGenre`` instance names are all strings.
    """
    for instance in SKUGenre.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__SKUGenre__value():
    """
    Tests whether ``SKUGenre`` instance values are all the expected value type.
    """
    for instance in SKUGenre.INSTANCES.values():
        vampytest.assert_instance(instance.value, SKUGenre.VALUE_TYPE)
