import vampytest

from ..discovery_category import DiscoveryCategory


def test__DiscoveryCategory__name():
    """
    Tests whether ``DiscoveryCategory`` instance names are all strings.
    """
    for instance in DiscoveryCategory.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__DiscoveryCategory__value():
    """
    Tests whether ``DiscoveryCategory`` instance values are all the expected value type.
    """
    for instance in DiscoveryCategory.INSTANCES.values():
        vampytest.assert_instance(instance.value, DiscoveryCategory.VALUE_TYPE)


def test__DiscoveryCategory__primary():
    """
    Tests whether ``DiscoveryCategory.primary`` is set as boolean.
    """
    for instance in DiscoveryCategory.INSTANCES.values():
        vampytest.assert_instance(instance.primary, bool)


def test__DiscoveryCategory__name_localizations():
    """
    Tests whether ``DiscoveryCategory.primary`` is set as boolean.
    """
    for instance in DiscoveryCategory.INSTANCES.values():
        vampytest.assert_instance(instance.name_localizations, dict, nullable = True)
