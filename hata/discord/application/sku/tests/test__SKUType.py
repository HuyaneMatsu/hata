import vampytest

from ..preinstanced import SKUType


@vampytest.call_from(SKUType.INSTANCES.values())
def test__SKUType__instances(instance):
    """
    Tests whether ``SKUType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUType``
        The instance to test.
    """
    vampytest.assert_instance(instance, SKUType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SKUType.VALUE_TYPE)
    vampytest.assert_instance(instance.giftable, bool)
    vampytest.assert_instance(instance.package, bool)
