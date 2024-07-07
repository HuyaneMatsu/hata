from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUType
from ..sku import SKU


def test__SKU__repr():
    """
    Tests whether ``SKU.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    sku_id = 202310010016
    access_type = SKUAccessType.full
    application_id = 202310010017
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
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
    
    vampytest.assert_instance(repr(sku), str)


def test__SKU__hash():
    """
    Tests whether ``SKU.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    sku_id = 202310010018
    access_type = SKUAccessType.full
    application_id = 202310010019
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    slug = 'https://orindance.party/'
    sku_type = SKUType.consumable
    
    
    keyword_parameters = {
        'access_type': access_type,
        'features': features,
        'flags': flags,
        'name': name,
        'premium': premium,
        'release_at': release_at,
        'sku_type': sku_type,
    }
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        slug = slug,
        **keyword_parameters
    )
    vampytest.assert_instance(hash(sku), int)


    sku = SKU(**keyword_parameters)
    vampytest.assert_instance(hash(sku), int)


def test__SKU__eq():
    """
    Tests whether ``SKU.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    sku_id = 202310010020
    access_type = SKUAccessType.full
    application_id = 202310010021
    features = [SKUFeature.single_player, SKUFeature.pvp]
    flags = SKUFlag(11)
    name = 'Red'
    premium = True
    release_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    slug = 'https://orindance.party/'
    sku_type = SKUType.consumable
    
    keyword_parameters = {
        'access_type': access_type,
        'features': features,
        'flags': flags,
        'name': name,
        'premium': premium,
        'release_at': release_at,
        'sku_type': sku_type,
    }
    
    sku = SKU.precreate(sku_id, application_id = application_id, slug = slug,**keyword_parameters)
    
    vampytest.assert_eq(sku, sku)
    vampytest.assert_ne(sku, object())
    
    test_sku = SKU(**keyword_parameters)
    vampytest.assert_eq(sku, test_sku)
    
    for field_name, field_value in (
        ('access_type', SKUAccessType.early_access),
        ('features', None),
        ('flags', SKUFlag(12)),
        ('name', 'Burning'),
        ('premium', False),
        ('release_at', None),
        ('sku_type', SKUType.durable),
    ):
        test_sku = SKU(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(sku, test_sku)
