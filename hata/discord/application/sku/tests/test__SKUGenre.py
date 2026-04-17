import vampytest

from ..preinstanced import SKUGenre


@vampytest.call_from(SKUGenre.INSTANCES.values())
def test__SKUGenre__instances(instance):
    """
    Tests whether ``SKUGenre`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUGenre``
        The instance to test.
    """
    vampytest.assert_instance(instance, SKUGenre)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SKUGenre.VALUE_TYPE)
