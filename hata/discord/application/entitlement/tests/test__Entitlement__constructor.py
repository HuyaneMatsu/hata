from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...sku import SKU

from ..entitlement import Entitlement
from ..fields import GiftCodeFlag
from ..preinstanced import EntitlementSourceType, EntitlementType


def _assert_fields_set(entitlement):
    """
    Asserts whether every attributes of the given entitlement are set.
    
    Parameters
    ----------
    entitlement : ``Entitlement``
        The entitlement check.
    """
    vampytest.assert_instance(entitlement, Entitlement)
    vampytest.assert_instance(entitlement._sku, SKU, nullable = True)
    vampytest.assert_instance(entitlement.application_id, int)
    vampytest.assert_instance(entitlement.consumed, bool)
    vampytest.assert_instance(entitlement.deleted, bool)
    vampytest.assert_instance(entitlement.ends_at, DateTime, nullable = True)
    vampytest.assert_instance(entitlement.gift_code_flags, GiftCodeFlag)
    vampytest.assert_instance(entitlement.guild_id, int)
    vampytest.assert_instance(entitlement.id, int)
    vampytest.assert_instance(entitlement.promotion_id, int)
    vampytest.assert_instance(entitlement.source_type, EntitlementSourceType)
    vampytest.assert_instance(entitlement.sku_id, int)
    vampytest.assert_instance(entitlement.starts_at, DateTime, nullable = True)
    vampytest.assert_instance(entitlement.subscription_id, int)
    vampytest.assert_instance(entitlement.type, EntitlementType)
    vampytest.assert_instance(entitlement.user_id, int)


def test__Entitlement__new__no_fields():
    """
    Tests whether ``Entitlement.__new__`` works as intended.
    
    Case: No parameters given.
    """
    entitlement = Entitlement()
    _assert_fields_set(entitlement)


def test__Entitlement__new__all_fields():
    """
    Tests whether ``Entitlement.__new__`` works as intended.
    
    Case: All parameters given.
    """
    guild_id = 202310040000
    sku_id = 202310040001
    user_id = 202310040002
    
    entitlement = Entitlement(
        guild_id = guild_id,
        sku_id = sku_id,
        user_id = user_id,
    )
    _assert_fields_set(entitlement)
    
    vampytest.assert_eq(entitlement.guild_id, guild_id)
    vampytest.assert_eq(entitlement.sku_id, sku_id)
    vampytest.assert_eq(entitlement.user_id, user_id)


def test__Entitlement__create_empty():
    """
    Tests whether ``Entitlement._create_empty`` works as intended.
    """
    entitlement_id = 202310040004
    
    entitlement = Entitlement._create_empty(entitlement_id)
    _assert_fields_set(entitlement)
    vampytest.assert_eq(entitlement.id, entitlement_id)


def test__Entitlement__precreate__no_fields():
    """
    Tests whether ``Entitlement.precreate`` works as intended.
    
    Case: No parameters given.
    """
    entitlement_id = 202310040005
    
    entitlement = Entitlement.precreate(entitlement_id)
    _assert_fields_set(entitlement)
    vampytest.assert_eq(entitlement.id, entitlement_id)


def test__Entitlement__precreate__all_fields():
    """
    Tests whether ``Entitlement.precreate`` works as intended.
    
    Case: All parameters given.
    """
    entitlement_id = 202310040006
    application_id = 202310040007
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    gift_code_flags = GiftCodeFlag(12)
    guild_id = 202310040008
    promotion_id = 202507020000
    source_type = EntitlementSourceType.user_gift
    sku_id = 202310040009
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040010
    user_id = 202310040011
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        name = 'yuuka',
    )
    
    entitlement = Entitlement.precreate(
        entitlement_id,
        application_id = application_id,
        consumed = consumed,
        deleted = deleted,
        ends_at = ends_at,
        entitlement_type = entitlement_type,
        gift_code_flags = gift_code_flags,
        guild_id = guild_id,
        promotion_id = promotion_id,
        source_type = source_type,
        sku = sku,
        sku_id = sku_id,
        starts_at = starts_at,
        subscription_id = subscription_id,
        user_id = user_id,
    )
    _assert_fields_set(entitlement)
    vampytest.assert_eq(entitlement.id, entitlement_id)
    
    vampytest.assert_is(entitlement._sku, sku)
    vampytest.assert_eq(entitlement.application_id, application_id)
    vampytest.assert_eq(entitlement.consumed, consumed)
    vampytest.assert_eq(entitlement.deleted, deleted)
    vampytest.assert_eq(entitlement.ends_at, ends_at)
    vampytest.assert_eq(entitlement.gift_code_flags, gift_code_flags)
    vampytest.assert_eq(entitlement.guild_id, guild_id)
    vampytest.assert_eq(entitlement.promotion_id, promotion_id)
    vampytest.assert_is(entitlement.source_type, source_type)
    vampytest.assert_eq(entitlement.sku_id, sku_id)
    vampytest.assert_eq(entitlement.starts_at, starts_at)
    vampytest.assert_eq(entitlement.subscription_id, subscription_id)
    vampytest.assert_is(entitlement.type, entitlement_type)
    vampytest.assert_eq(entitlement.user_id, user_id)


def test__Entitlement__precreate__caching():
    """
    Tests whether ``Entitlement.precreate`` works as intended.
    
    Case: Caching.
    """
    entitlement_id = 202310040012
    
    entitlement = Entitlement.precreate(entitlement_id)
    test_entitlement = Entitlement.precreate(entitlement_id)
    
    vampytest.assert_is(entitlement, test_entitlement)
