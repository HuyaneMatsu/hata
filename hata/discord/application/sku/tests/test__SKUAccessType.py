import vampytest

from ..preinstanced import SKUAccessType


@vampytest.call_from(SKUAccessType.INSTANCES.values())
def test__SKUAccessType__instances(instance):
    """
    Tests whether ``SKUAccessType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUAccessType``
        The instance to test.
    """
    vampytest.assert_instance(instance, SKUAccessType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SKUAccessType.VALUE_TYPE)
