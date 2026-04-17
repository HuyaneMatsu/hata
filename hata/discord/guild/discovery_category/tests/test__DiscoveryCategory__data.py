import vampytest

from ....localization import Locale

from ..discovery_category import DiscoveryCategory


def _assert_is_every_field_set(discovery_category):
    """
    Asserts whether fields are set of the given discovery category.
    
    Parameters
    ----------
    discovery_category : ``DiscoveryCategory``
        The discovery category to check.
    """
    vampytest.assert_instance(discovery_category, DiscoveryCategory)
    vampytest.assert_instance(discovery_category.primary, bool)
    vampytest.assert_instance(discovery_category.name, str)
    vampytest.assert_instance(discovery_category.name_localizations, dict, nullable = True)
    vampytest.assert_instance(discovery_category.value, int)


def test__DiscoveryCategory__from_data():
    """
    Tests whether ``DiscoveryCategory.from_data`` works as intended.
    """
    primary = True
    name = 'bloody'
    name_localizations = {
        Locale.dutch: 'bloody',
        Locale.greek: 'moon',
    }
    value = 106
    
    data = {
        'is_primary': primary,
        'name': name,
        'name_localizations': {locale.value: locale_name for locale, locale_name in name_localizations.items()},
        'id': value,
    }
    
    discovery_category = DiscoveryCategory.from_data(data)
    _assert_is_every_field_set(discovery_category)
    
    vampytest.assert_eq(discovery_category.primary, primary)
    vampytest.assert_eq(discovery_category.name, name)
    vampytest.assert_eq(discovery_category.name_localizations, name_localizations)
    vampytest.assert_eq(discovery_category.value, value)


def test__DiscoveryCategory__to_data():
    """
    Tests whether ``DiscoveryCategory.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    # We do not have a real constructor, so we use `.from_data`.
    primary = True
    name = 'bloody'
    name_localizations = {
        Locale.dutch: 'bloody',
        Locale.greek: 'moon',
    }
    value = 106
    
    data = {
        'is_primary': primary,
        'name': name,
        'name_localizations': {locale.value: locale_name for locale, locale_name in name_localizations.items()},
        'id': value,
    }
    
    discovery_category = DiscoveryCategory.from_data(data)
    
    vampytest.assert_eq(
        discovery_category.to_data(defaults = True, include_internals = True),
        data,
    )
