import vampytest

from ..discovery_category import DiscoveryCategory


@vampytest.call_from(DiscoveryCategory.INSTANCES.values())
def test__DiscoveryCategory__instances(instance):
    """
    Tests whether ``DiscoveryCategory`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``DiscoveryCategory``
        The instance to test.
    """
    vampytest.assert_instance(instance, DiscoveryCategory)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, DiscoveryCategory.VALUE_TYPE)
    vampytest.assert_instance(instance.primary, bool)
    vampytest.assert_instance(instance.name_localizations, dict, nullable = True)
