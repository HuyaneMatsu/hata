from datetime import datetime as DateTime

import vampytest

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUType
from ..sku import SKU


def _assert_fields_set(sku):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    sku : ``SKU``
        The application entity to check.
    """
    vampytest.assert_instance(sku, SKU)
    vampytest.assert_instance(sku.access_type, SKUAccessType)
    vampytest.assert_instance(sku.application_id, int)
    vampytest.assert_instance(sku.features, tuple, nullable = True)
    vampytest.assert_instance(sku.flags, SKUFlag)
    vampytest.assert_instance(sku.id, int)
    vampytest.assert_instance(sku.name, str)
    vampytest.assert_instance(sku.premium, bool)
    vampytest.assert_instance(sku.release_at, DateTime, nullable = True)
    vampytest.assert_instance(sku.slug, str, nullable = True)
    vampytest.assert_instance(sku.type, SKUType)


def test__SKU__new__no_fields():
    """
    Tests whether ``SKU.__new__`` works as intended.
    
    Case: No parameters given.
    """
    sku = SKU()
    _assert_fields_set(sku)


def test__SKU__new__all_fields():
    """
    Tests whether ``SKU.__new__`` works as intended.
    
    Case: All parameters given.
    """
    access_type = SKUAccessType.full
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14)
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
    _assert_fields_set(sku)
    
    vampytest.assert_is(sku.access_type, access_type)
    vampytest.assert_eq(sku.features, tuple(features))
    vampytest.assert_eq(sku.flags, flags)
    vampytest.assert_eq(sku.name, name)
    vampytest.assert_eq(sku.premium, premium)
    vampytest.assert_eq(sku.release_at, release_at)
    vampytest.assert_is(sku.type, sku_type)


def test__SKU__create_empty():
    """
    Tests whether ``SKU._create_empty`` works as intended.
    """
    sku_id = 202310010008
    
    sku = SKU._create_empty(sku_id)
    _assert_fields_set(sku)
    vampytest.assert_eq(sku.id, sku_id)


def test__SKU__precreate__no_fields():
    """
    Tests whether ``SKU.precreate`` works as intended.
    
    Case: No parameters given.
    """
    sku_id = 202310010009
    
    sku = SKU.precreate(sku_id)
    _assert_fields_set(sku)
    vampytest.assert_eq(sku.id, sku_id)


def test__SKU__precreate__all_fields():
    """
    Tests whether ``SKU.precreate`` works as intended.
    
    Case: All parameters given.
    """
    sku_id = 202310010010
    access_type = SKUAccessType.full
    application_id = 202310010011
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14)
    slug = 'https://orindance.party/'
    sku_type = SKUType.consumable
    
    sku = SKU.precreate(
        sku_id,
        access_type = access_type,
        application_id = application_id,
        features = features,
        flags = flags,
        name = name,
        premium = premium,
        release_at = release_at,
        slug = slug,
        sku_type = sku_type,
    )
    _assert_fields_set(sku)
    vampytest.assert_eq(sku.id, sku_id)
    
    vampytest.assert_is(sku.access_type, access_type)
    vampytest.assert_eq(sku.application_id, application_id)
    vampytest.assert_eq(sku.features, tuple(features))
    vampytest.assert_eq(sku.flags, flags)
    vampytest.assert_eq(sku.name, name)
    vampytest.assert_eq(sku.premium, premium)
    vampytest.assert_eq(sku.release_at, release_at)
    vampytest.assert_eq(sku.slug, slug)
    vampytest.assert_is(sku.type, sku_type)


def test__SKU__precreate__caching():
    """
    Tests whether ``SKU.precreate`` works as intended.
    
    Case: Caching.
    """
    sku_id = 202310040003
    
    sku = SKU.precreate(sku_id)
    test_sku = SKU.precreate(sku_id)
    
    vampytest.assert_is(sku, test_sku)
