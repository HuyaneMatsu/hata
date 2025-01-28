import vampytest

from ..preinstanced import SKUType


def _assert_fields_set(sku_type):
    """
    Asserts whether every field are set of the given sku type.
    
    Parameters
    ----------
    sku_type : ``SKUType``
        The instance to test.
    """
    vampytest.assert_instance(sku_type, SKUType)
    vampytest.assert_instance(sku_type.name, str)
    vampytest.assert_instance(sku_type.value, SKUType.VALUE_TYPE)
    vampytest.assert_instance(sku_type.giftable, bool)
    vampytest.assert_instance(sku_type.package, bool)


@vampytest.call_from(SKUType.INSTANCES.values())
def test__SKUType__instances(instance):
    """
    Tests whether ``SKUType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SKUType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__SKUType__new__min_fields():
    """
    Tests whether ``SKUType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 20
    
    try:
        output = SKUType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, SKUType.NAME_DEFAULT)
        vampytest.assert_eq(output.giftable, False)
        vampytest.assert_eq(output.package, False)
        vampytest.assert_is(SKUType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del SKUType.INSTANCES[value]
        except KeyError:
            pass
