import vampytest

from ..preinstanced import SKUProductFamily


@vampytest.call_from(SKUProductFamily.INSTANCES.values())
def test__SKUProductFamily__instances(instance):
    """
    Tests whether ``SKUProductFamily`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUProductFamily``
        The instance to test.
    """
    vampytest.assert_instance(instance, SKUProductFamily)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SKUProductFamily.VALUE_TYPE)
