import vampytest

from ..preinstanced import HypesquadHouse


@vampytest.call_from(HypesquadHouse.INSTANCES.values())
def test__HypesquadHouse__instances(instance):
    """
    Tests whether ``HypesquadHouse`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``HypesquadHouse``
        The instance to test.
    """
    vampytest.assert_instance(instance, HypesquadHouse)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, HypesquadHouse.VALUE_TYPE)
