from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....localization import Locale
from ....utils import datetime_to_timestamp

from ...sku_enhancement import SKUEnhancement

from ..flags import SKUFlag
from ..preinstanced import SKUAccessType, SKUFeature, SKUProductFamily, SKUType
from ..sku import SKU

from .test__SKU__constructor import _assert_fields_set


def test__SKU__from_data():
    """
    Tests whether ``SKU.from_data`` works as intended.
    
    Case: Default.
    """
    sku_id = 202310010012
    access_type = SKUAccessType.full
    application_id = 202310010013
    dependent_sku_id = 202506290005
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
    
    data = {
        'access_type': access_type.value,
        'application_id': str(application_id),
        'dependent_sku_id': str(dependent_sku_id),
        'powerup_metadata': enhancement.to_data(),
        'features': [feature.value for feature in features],
        'flags': int(flags),
        'id': str(sku_id),
        'name': {
            'default': name,
            'localizations': {key.value: value for key, value in name_localizations.items()},
        },
        'premium': premium,
        'product_line': product_family.value,
        'release_date': datetime_to_timestamp(release_at),
        'slug': slug,
        'type': sku_type.value,
    }
    
    sku = SKU.from_data(data)
    _assert_fields_set(sku)
    
    vampytest.assert_eq(sku.id, sku_id)
    vampytest.assert_is(sku.access_type, access_type)
    vampytest.assert_eq(sku.application_id, application_id)
    vampytest.assert_eq(sku.dependent_sku_id, dependent_sku_id)
    vampytest.assert_eq(sku.enhancement, enhancement)
    vampytest.assert_eq(sku.features, tuple(features))
    vampytest.assert_eq(sku.flags, flags)
    vampytest.assert_eq(sku.name, name)
    vampytest.assert_eq(sku.name_localizations, name_localizations)
    vampytest.assert_eq(sku.premium, premium)
    vampytest.assert_is(sku.product_family, product_family)
    vampytest.assert_eq(sku.release_at, release_at)
    vampytest.assert_eq(sku.slug, slug)
    vampytest.assert_is(sku.type, sku_type)


def test__SKU__from_data__caching():
    """
    Tests whether ``SKU.from_data`` works as intended.
    
    Case: check caching.
    """
    sku_id = 202310030006
    
    data = {
        'id': str(sku_id),
    }
    
    sku = SKU.from_data(data)
    
    test_sku = SKU.from_data(data)
    
    vampytest.assert_is(sku, test_sku)


def test__SKU__set_attributes():
    """
    Tests whether ``SKU._set_attributes`` works as intended.
    """
    sku_id = 202310030007
    access_type = SKUAccessType.full
    application_id = 202310030008
    dependent_sku_id = 202506290006
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
    
    data = {
        'access_type': access_type.value,
        'application_id': str(application_id),
        'dependent_sku_id': str(dependent_sku_id),
        'powerup_metadata': enhancement.to_data(),
        'features': [feature.value for feature in features],
        'flags': int(flags),
        'name': {
            'default': name,
            'localizations': {key.value: value for key, value in name_localizations.items()},
        },
        'premium': premium,
        'product_line': product_family.value,
        'release_date': datetime_to_timestamp(release_at),
        'slug': slug,
        'type': sku_type.value,
    }
    
    sku = SKU._create_empty(sku_id)
    sku._set_attributes(data)
    
    vampytest.assert_is(sku.access_type, access_type)
    vampytest.assert_eq(sku.application_id, application_id)
    vampytest.assert_eq(sku.dependent_sku_id, dependent_sku_id)
    vampytest.assert_eq(sku.enhancement, enhancement)
    vampytest.assert_eq(sku.features, tuple(features))
    vampytest.assert_eq(sku.flags, flags)
    vampytest.assert_eq(sku.name, name)
    vampytest.assert_eq(sku.name_localizations, name_localizations)
    vampytest.assert_eq(sku.premium, premium)
    vampytest.assert_is(sku.product_family, product_family)
    vampytest.assert_eq(sku.release_at, release_at)
    vampytest.assert_eq(sku.slug, slug)
    vampytest.assert_is(sku.type, sku_type)



def test__SKU__to_data():
    """
    Tests whether ``SKU.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    sku_id = 202310010014
    access_type = SKUAccessType.full
    application_id = 202310010015
    dependent_sku_id = 202506290007
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
    
    expected_output = {
        'access_type': access_type.value,
        'application_id': str(application_id),
        'dependent_sku_id': str(dependent_sku_id),
        'powerup_metadata': enhancement.to_data(defaults = True),
        'features': [feature.value for feature in features],
        'flags': int(flags),
        'id': str(sku_id),
        'name': {
            'default': name,
            'localizations': {key.value: value for key, value in name_localizations.items()},
        },
        'premium': premium,
        'product_line': product_family.value,
        'release_date': datetime_to_timestamp(release_at),
        'slug': slug,
        'type': sku_type.value,
    }
    
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
    
    vampytest.assert_eq(
        sku.to_data(defaults = True, include_internals = True),
        expected_output,
    )
