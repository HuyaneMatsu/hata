import vampytest

from ..preinstanced import HypesquadHouse


def test__HypesquadHouse__name():
    """
    Tests whether ``HypesquadHouse`` instance names are all strings.
    """
    for instance in HypesquadHouse.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__HypesquadHouse__value():
    """
    Tests whether ``HypesquadHouse`` instance values are all the expected value type.
    """
    for instance in HypesquadHouse.INSTANCES.values():
        vampytest.assert_instance(instance.value, HypesquadHouse.VALUE_TYPE)
