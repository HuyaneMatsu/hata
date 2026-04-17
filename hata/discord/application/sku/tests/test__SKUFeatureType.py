import vampytest

from ..preinstanced import SKUFeature


@vampytest.call_from(SKUFeature.INSTANCES.values())
def test__SKUFeature__instances(instance):
    """
    Tests whether ``SKUFeature`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUFeature``
        The instance to test.
    """
    vampytest.assert_instance(instance, SKUFeature)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SKUFeature.VALUE_TYPE)
