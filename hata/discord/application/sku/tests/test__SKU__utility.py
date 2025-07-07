from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....localization import Locale

from ...sku_enhancement import SKUEnhancement

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUProductFamily, SKUType
from ..sku import SKU

from .test__SKU__constructor import _assert_fields_set


def test__SKU__copy():
    """
    Tests whether ``SKU.copy`` works as intended.
    """
    access_type = SKUAccessType.full
    dependent_sku_id = 202506290012
    enhancement = SKUEnhancement(
        boost_cost = 3,
    )
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    name_localizations = {
        Locale.dutch: 'bloody',
        Locale.greek: 'moon',
    }
    premium = True
    product_family = SKUProductFamily.boost
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_type = SKUType.consumable
    
    sku = SKU(
        access_type = access_type,
        dependent_sku_id = dependent_sku_id,
        enhancement = enhancement,
        features = features,
        flags = flags,
        name = name,
        name_localizations = name_localizations,
        premium = premium,
        product_family = product_family,
        release_at = release_at,
        sku_type = sku_type,
    )
    
    copy = sku.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, sku)
    vampytest.assert_not_is(copy, sku)


def test__SKU__copy_with__no_fields():
    """
    Tests whether ``SKU.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    access_type = SKUAccessType.full
    dependent_sku_id = 202506290013
    enhancement = SKUEnhancement(
        boost_cost = 3,
    )
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    name_localizations = {
        Locale.dutch: 'bloody',
        Locale.greek: 'moon',
    }
    premium = True
    product_family = SKUProductFamily.boost
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_type = SKUType.consumable
    
    sku = SKU(
        access_type = access_type,
        dependent_sku_id = dependent_sku_id,
        enhancement = enhancement,
        features = features,
        flags = flags,
        name = name,
        name_localizations = name_localizations,
        premium = premium,
        product_family = product_family,
        release_at = release_at,
        sku_type = sku_type,
    )
    
    copy = sku.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, sku)
    vampytest.assert_not_is(copy, sku)


def test__SKU__copy_with__all_fields():
    """
    Tests whether ``SKU.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_access_type = SKUAccessType.full
    old_dependent_sku_id = 202506290014
    old_enhancement = SKUEnhancement(
        boost_cost = 3,
    )
    old_features = [SKUFeature.single_player, SKUFeature.pvp]
    old_flags = SKUFlag(11)
    old_name = 'Red'
    old_name_localizations = {
        Locale.dutch: 'bloody',
        Locale.greek: 'moon',
    }
    old_premium = True
    old_product_family = SKUProductFamily.boost
    old_release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_sku_type = SKUType.consumable
    
    new_access_type = SKUAccessType.early_access
    new_dependent_sku_id = 202506290015
    new_enhancement = SKUEnhancement(
        boost_cost = 3,
    )
    new_features = [SKUFeature.cross_platform, SKUFeature.rich_presence]
    new_flags = SKUFlag(12)
    new_name = 'Burning'
    new_name_localizations = {
        Locale.dutch: 'chinese',
        Locale.greek: 'tea',
    }
    new_premium = False
    new_product_family = SKUProductFamily.premium
    new_release_at = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)
    new_sku_type = SKUType.durable
    
    sku = SKU(
        access_type = old_access_type,
        dependent_sku_id = old_dependent_sku_id,
        enhancement = old_enhancement,
        features = old_features,
        flags = old_flags,
        name = old_name,
        name_localizations = old_name_localizations,
        premium = old_premium,
        product_family = old_product_family,
        release_at = old_release_at,
        sku_type = old_sku_type,
    )
    
    copy = sku.copy_with(
        access_type = new_access_type,
        dependent_sku_id = new_dependent_sku_id,
        enhancement = new_enhancement,
        features = new_features,
        flags = new_flags,
        name = new_name,
        name_localizations = new_name_localizations,
        premium = new_premium,
        product_family = new_product_family,
        release_at = new_release_at,
        sku_type = new_sku_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, sku)

    vampytest.assert_is(copy.access_type, new_access_type)
    vampytest.assert_eq(copy.dependent_sku_id, new_dependent_sku_id)
    vampytest.assert_eq(copy.enhancement, new_enhancement)
    vampytest.assert_eq(copy.features, tuple(new_features))
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.name_localizations, new_name_localizations)
    vampytest.assert_eq(copy.premium, new_premium)
    vampytest.assert_is(copy.product_family, new_product_family)
    vampytest.assert_eq(copy.release_at, new_release_at)
    vampytest.assert_is(copy.type, new_sku_type)



def test__SKU__partial__true():
    """
    Tests whether ``SKU.partial`` works as intended.
    
    Case: true.
    """
    sku = SKU()
    
    output = sku.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__SKU__partial__false():
    """
    Tests whether ``SKU.partial`` works as intended.
    
    Case: false.
    """
    sku_id = 202310010022
    
    sku = SKU.precreate(sku_id)
    
    output = sku.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def _iter_options__iter_features():
    feature_0 = SKUFeature.single_player
    feature_1 = SKUFeature.pvp
    
    yield 202506290020, None, set()
    yield 202506290021, [feature_0], {feature_0}
    yield 202506290022, [feature_0, feature_1], {feature_0, feature_1}


@vampytest._(vampytest.call_from(_iter_options__iter_features()).returning_last())
def test__Guild__iter_features(sku_id, features):
    """
    Tests whether ``Guild.iter_features`` works as intended.
    
    Parameters
    ----------
    sku_id : `int`
        Stick keeping unit identifier.
    
    features : ``None | list<SKUFeature>``
        Stock keeping unit features.
    
    Returns
    -------
    output : ``set<SKUFeature>>`
    """
    sku = SKU.precreate(sku_id, features = features)
    
    output = {*sku.iter_features()}
    
    for element in output:
        vampytest.assert_instance(element, SKUFeature)
    
    return output


def _iter_options__has_feature():
    feature = SKUFeature.single_player

    yield 202506290023, None, feature, False
    yield 202506290024, [SKUFeature.pvp], feature, False
    yield 202506290025, [feature], feature, True
    yield 202506290026, [SKUFeature.pvp, feature], feature, True


@vampytest._(vampytest.call_from(_iter_options__has_feature()).returning_last())
def test__Guild__has_feature(sku_id, features, feature):
    """
    Tests whether ``Guild.has_feature`` works as intended.
    
    Parameters
    ----------
    sku_id : `int`
        Stick keeping unit identifier.
    
    features : ``None | list<SKUFeature>``
        Stock keeping unit features.
    
    feature : ``SKUFeature``
        The feature to check for.
    
    Returns
    -------
    output : `bool`
    """
    sku = SKU.precreate(sku_id, features = features)
    output = sku.has_feature(feature)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__dependent_sku():
    dependent_sku_id_0 = 202506290015
    dependent_sku_id_1 = 202506290016
    dependent_sku_0 = SKU.precreate(dependent_sku_id_0)
    
    yield 202506290017, 0, None
    yield 202506290018, dependent_sku_id_0, dependent_sku_0
    yield 202506290019, dependent_sku_id_1, None


@vampytest._(vampytest.call_from(_iter_options__dependent_sku()).returning_last())
def test__SKU__dependent_sku(sku_id, input_value):
    """
    Tests whether ``SKU.dependent_sku`` works as intended.
    
    Parameters
    ----------
    sku_id : `int`
        SKU identifier to create the instance with.
    
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : ``None | SKU``
    """
    sku = SKU.precreate(sku_id, dependent_sku_id = input_value)
    output = sku.dependent_sku
    vampytest.assert_instance(output, SKU, nullable = True)
    return output

