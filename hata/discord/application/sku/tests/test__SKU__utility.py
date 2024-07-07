from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUType
from ..sku import SKU

from .test__SKU__constructor import _assert_fields_set


def test__SKU__copy():
    """
    Tests whether ``SKU.copy`` works as intended.
    """
    access_type = SKUAccessType.full
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_type = SKUType.consumable
    
    sku = SKU(
        access_type = access_type,
        features = features,
        flags = flags,
        name = name,
        premium = premium,
        release_at = release_at,
        sku_type = sku_type,
    )
    
    copy = sku.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, sku)
    vampytest.assert_not_is(copy, sku)


def test__SKU__copy_with__0():
    """
    Tests whether ``SKU.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    access_type = SKUAccessType.full
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_type = SKUType.consumable
    
    sku = SKU(
        access_type = access_type,
        features = features,
        flags = flags,
        name = name,
        premium = premium,
        release_at = release_at,
        sku_type = sku_type,
    )
    
    copy = sku.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, sku)
    vampytest.assert_not_is(copy, sku)


def test__SKU__copy_with__1():
    """
    Tests whether ``SKU.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_access_type = SKUAccessType.full
    old_features = [SKUFeature.single_player, SKUFeature.pvp]
    old_flags = SKUFlag(11)
    old_name = 'Red'
    old_premium = True
    old_release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_sku_type = SKUType.consumable
    
    new_access_type = SKUAccessType.early_access
    new_features = [SKUFeature.cross_platform, SKUFeature.rich_presence]
    new_flags = SKUFlag(12)
    new_name = 'Burning'
    new_premium = False
    new_release_at = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)
    new_sku_type = SKUType.durable
    
    sku = SKU(
        access_type = old_access_type,
        features = old_features,
        flags = old_flags,
        name = old_name,
        premium = old_premium,
        release_at = old_release_at,
        sku_type = old_sku_type,
    )
    
    copy = sku.copy_with(
        access_type = new_access_type,
        features = new_features,
        flags = new_flags,
        name = new_name,
        premium = new_premium,
        release_at = new_release_at,
        sku_type = new_sku_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, sku)

    vampytest.assert_is(copy.access_type, new_access_type)
    vampytest.assert_eq(copy.features, tuple(new_features))
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.premium, new_premium)
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
    
    yield SKU(features = None), set()
    yield SKU(features = [feature_0]), {feature_0}
    yield SKU(features = [feature_0, feature_1]), {feature_0, feature_1}


@vampytest._(vampytest.call_from(_iter_options__iter_features()).returning_last())
def test__Guild__iter_features(sku):
    """
    Tests whether ``Guild.iter_features`` works as intended.
    
    Parameters
    ----------
    sku : ``SKU``
        The stock keeping unit to iter the features of.
    
    Returns
    -------
    output : `set` of ``SKUFeature``
    """
    return {*sku.iter_features()}


def _iter_options__has_feature():
    feature = SKUFeature.single_player

    yield SKU(features = []), feature, False
    yield SKU(features = [SKUFeature.pvp]), feature, False
    yield SKU(features = [feature]), feature, True
    yield SKU(features = [SKUFeature.pvp, feature]), feature, True


@vampytest._(vampytest.call_from(_iter_options__has_feature()).returning_last())
def test__Guild__has_feature(sku, feature):
    """
    Tests whether ``Guild.has_feature`` works as intended.
    
    Parameters
    ----------
    sku : ``SKU``
        The stock keeping unit to check the feature of.
    feature : ``SKUFeature``
        The feature to check for.
    
    Returns
    -------
    output : `bool`
    """
    return sku.has_feature(feature)
