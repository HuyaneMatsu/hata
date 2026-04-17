import vampytest

from ..discovery_category import DiscoveryCategory


def _assert_fields_set(discovery_category):
    """
    Asserts whether every field are set of the given discovery category.
    
    Parameters
    ----------
    discovery_category : ``DiscoveryCategory``
        The instance to test.
    """
    vampytest.assert_instance(discovery_category, DiscoveryCategory)
    vampytest.assert_instance(discovery_category.name, str)
    vampytest.assert_instance(discovery_category.value, DiscoveryCategory.VALUE_TYPE)
    vampytest.assert_instance(discovery_category.name_localizations, dict, nullable = True)
    vampytest.assert_instance(discovery_category.primary, bool)


@vampytest.call_from(DiscoveryCategory.INSTANCES.values())
def test__DiscoveryCategory__instances(instance):
    """
    Tests whether ``DiscoveryCategory`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``DiscoveryCategory``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__DiscoveryCategory__new__min_fields():
    """
    Tests whether ``DiscoveryCategory.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 100
    
    try:
        output = DiscoveryCategory(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, DiscoveryCategory.NAME_DEFAULT)
        vampytest.assert_is(output.name_localizations, None)
        vampytest.assert_eq(output.primary, True)
        vampytest.assert_is(DiscoveryCategory.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del DiscoveryCategory.INSTANCES[value]
        except KeyError:
            pass
