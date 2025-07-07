from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....localization import Locale

from ...sku_enhancement import SKUEnhancement

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUProductFamily, SKUType
from ..sku import SKU


def test__SKU__repr():
    """
    Tests whether ``SKU.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    sku_id = 202310010016
    access_type = SKUAccessType.full
    application_id = 202310010017
    dependent_sku_id = 202506290008
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
    slug = 'https://orindance.party/'
    sku_type = SKUType.consumable
    
    
    sku = SKU.precreate(
        sku_id,
        access_type = access_type,
        application_id = application_id,
        dependent_sku_id = dependent_sku_id,
        enhancement = enhancement,
        features = features,
        flags = flags,
        name = name,
        name_localizations = name_localizations,
        premium = premium,
        product_family = product_family,
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
    dependent_sku_id = 202506290009
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
    slug = 'https://orindance.party/'
    sku_type = SKUType.consumable
    
    
    keyword_parameters = {
        'access_type': access_type,
        'dependent_sku_id': dependent_sku_id,
        'enhancement': enhancement,
        'features': features,
        'flags': flags,
        'name': name,
        'name_localizations': name_localizations,
        'premium': premium,
        'product_family': product_family,
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


def _iter_options__eq():
    access_type = SKUAccessType.full
    dependent_sku_id = 202506290010
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
    
    keyword_parameters = {
        'access_type': access_type,
        'dependent_sku_id': dependent_sku_id,
        'enhancement': enhancement,
        'features': features,
        'flags': flags,
        'name': name,
        'name_localizations': name_localizations,
        'premium': premium,
        'product_family': product_family,
        'release_at': release_at,
        'sku_type': sku_type,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'access_type' : SKUAccessType.early_access,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'dependent_sku_id' : 202506290011,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'enhancement' : None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'features' : None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags' : SKUFlag(12),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name' : 'Burning',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name_localizations' : None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'premium' : False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'product_family' : SKUProductFamily.application,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'release_at' : None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sku_type' : SKUType.durable,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__SKU__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``SKU.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    sku_0 = SKU(**keyword_parameters_0)
    sku_1 = SKU(**keyword_parameters_1)
    
    output = sku_0 == sku_1
    vampytest.assert_instance(output, bool)
    return output


def test__SKU__eq__non_partial():
    """
    Tests whether ``SKU.__eq__`` works as intended.
    
    Case: non partial
    """
    name = 'pudding'
    
    sku_id = 202310010020
    application_id = 202310010021
    slug = 'https://orindance.party/'
    
    sku_0 = SKU.precreate(sku_id, application_id = application_id, slug = slug, name = name)
    sku_1 = SKU(name = name)
    vampytest.assert_eq(sku_0, sku_0)
    vampytest.assert_eq(sku_0, sku_1)
    vampytest.assert_ne(sku_0, object())
