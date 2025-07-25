from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...sku import SKU

from ..entitlement import Entitlement
from ..fields import GiftCodeFlag
from ..preinstanced import EntitlementOwnerType, EntitlementSourceType, EntitlementType

from .test__Entitlement__constructor import _assert_fields_set


def test__Entitlement__from_data():
    """
    Tests whether ``Entitlement.from_data`` works as intended.
    
    Case: Default.
    """
    entitlement_id = 202310040013
    application_id = 202310040014
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    gift_code_flags = GiftCodeFlag(12)
    guild_id = 202310040032
    promotion_id = 202507020001
    source_type = EntitlementSourceType.user_gift
    sku_id = 202310040033
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040015
    user_id = 202310040016
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        name = 'yuuka',
    )
    
    data = {
        'id': str(entitlement_id),
        'application_id': str(application_id),
        'consumed': consumed,
        'deleted': deleted,
        'ends_at': datetime_to_timestamp(ends_at),
        'type': entitlement_type.value,
        'gift_code_flags': int(gift_code_flags),
        'guild_id': str(guild_id),
        'promotion_id': str(promotion_id),
        'source_type': source_type.value,
        'sku': sku.to_data(include_internals = True),
        'sku_id': str(sku_id),
        'starts_at': datetime_to_timestamp(starts_at),
        'subscription_id': str(subscription_id),
        'user_id': str(user_id),
    }
    
    entitlement = Entitlement.from_data(data)
    _assert_fields_set(entitlement)
    vampytest.assert_eq(entitlement.id, entitlement_id)
    
    vampytest.assert_is(entitlement._sku, sku)
    vampytest.assert_eq(entitlement.application_id, application_id)
    vampytest.assert_eq(entitlement.consumed, consumed)
    vampytest.assert_eq(entitlement.deleted, deleted)
    vampytest.assert_eq(entitlement.ends_at, ends_at)
    vampytest.assert_eq(entitlement.guild_id, guild_id)
    vampytest.assert_eq(entitlement.gift_code_flags, gift_code_flags)
    vampytest.assert_eq(entitlement.promotion_id, promotion_id)
    vampytest.assert_is(entitlement.source_type, source_type)
    vampytest.assert_eq(entitlement.sku_id, sku_id)
    vampytest.assert_eq(entitlement.starts_at, starts_at)
    vampytest.assert_eq(entitlement.subscription_id, subscription_id)
    vampytest.assert_is(entitlement.type, entitlement_type)
    vampytest.assert_eq(entitlement.user_id, user_id)


def test__Entitlement__from_data__caching():
    """
    Tests whether ``Entitlement.from_data`` works as intended.
    
    Case: Caching.
    """
    entitlement_id = 202310040025
    
    data = {
        'id': str(entitlement_id),
    }
    
    entitlement = Entitlement.from_data(data)
    test_entitlement = Entitlement.from_data(data)
    vampytest.assert_eq(entitlement, test_entitlement)


def test__Entitlement__from_data_is_created():
    """
    Tests whether ``Entitlement.from_data_is_created`` works as intended.
    
    Case: Default.
    """
    entitlement_id = 202310070000
    application_id = 202310070001
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    gift_code_flags = GiftCodeFlag(12)
    guild_id = 202310070002
    promotion_id = 202507020002
    source_type = EntitlementSourceType.user_gift
    sku_id = 202310070003
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310070004
    user_id = 202310070005
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        name = 'yuuka',
    )
    
    data = {
        'id': str(entitlement_id),
        'application_id': str(application_id),
        'consumed': consumed,
        'deleted': deleted,
        'ends_at': datetime_to_timestamp(ends_at),
        'gift_code_flags': int(gift_code_flags),
        'type': entitlement_type.value,
        'promotion_id': str(promotion_id),
        'source_type': source_type.value,
        'guild_id': str(guild_id),
        'sku': sku.to_data(include_internals = True),
        'sku_id': str(sku_id),
        'starts_at': datetime_to_timestamp(starts_at),
        'subscription_id': str(subscription_id),
        'user_id': str(user_id),
    }
    
    entitlement, is_created = Entitlement.from_data_is_created(data)
    _assert_fields_set(entitlement)
    vampytest.assert_eq(entitlement.id, entitlement_id)
    
    vampytest.assert_instance(is_created, bool)
    vampytest.assert_eq(is_created, True)
    
    vampytest.assert_is(entitlement._sku, sku)
    vampytest.assert_eq(entitlement.application_id, application_id)
    vampytest.assert_eq(entitlement.consumed, consumed)
    vampytest.assert_eq(entitlement.deleted, deleted)
    vampytest.assert_eq(entitlement.ends_at, ends_at)
    vampytest.assert_is(entitlement.type, entitlement_type)
    vampytest.assert_eq(entitlement.guild_id, guild_id)
    vampytest.assert_eq(entitlement.gift_code_flags, gift_code_flags)
    vampytest.assert_eq(entitlement.promotion_id, promotion_id)
    vampytest.assert_is(entitlement.source_type, source_type)
    vampytest.assert_eq(entitlement.sku_id, sku_id)
    vampytest.assert_eq(entitlement.starts_at, starts_at)
    vampytest.assert_eq(entitlement.subscription_id, subscription_id)
    vampytest.assert_eq(entitlement.user_id, user_id)


def test__Entitlement__from_data_is_created__caching():
    """
    Tests whether ``Entitlement.from_data_is_created`` works as intended.
    
    Case: Caching.
    """
    entitlement_id = 202310070006
    
    data = {
        'id': str(entitlement_id),
    }
    
    entitlement, is_created_0 = Entitlement.from_data_is_created(data)
    test_entitlement, is_created_1 = Entitlement.from_data_is_created(data)
    vampytest.assert_eq(entitlement, test_entitlement)

    vampytest.assert_instance(is_created_0, bool)
    vampytest.assert_eq(is_created_0, True)


    vampytest.assert_instance(is_created_1, bool)
    vampytest.assert_eq(is_created_1, False)


def test__Entitlement__set_attributes():
    """
    Tests whether ``Entitlement._set_attributes`` works as intended.
    """
    entitlement_id = 202310040026
    application_id = 202310040027
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    gift_code_flags = GiftCodeFlag(12)
    guild_id = 202310040028
    promotion_id = 202507020003
    source_type = EntitlementSourceType.user_gift
    sku_id = 202310040029
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040030
    user_id = 202310040031
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        name = 'yuuka',
    )
    
    data = {
        'application_id': str(application_id),
        'consumed': consumed,
        'deleted': deleted,
        'ends_at': datetime_to_timestamp(ends_at),
        'gift_code_flags': int(gift_code_flags),
        'type': entitlement_type.value,
        'guild_id': str(guild_id),
        'promotion_id': str(promotion_id),
        'source_type': source_type.value,
        'sku': sku.to_data(include_internals = True),
        'sku_id': str(sku_id),
        'starts_at': datetime_to_timestamp(starts_at),
        'subscription_id': str(subscription_id),
        'user_id': str(user_id),
    }
    
    entitlement = Entitlement._create_empty(entitlement_id)
    entitlement._set_attributes(data)
    
    vampytest.assert_is(entitlement._sku, sku)
    vampytest.assert_eq(entitlement.application_id, application_id)
    vampytest.assert_eq(entitlement.consumed, consumed)
    vampytest.assert_eq(entitlement.deleted, deleted)
    vampytest.assert_eq(entitlement.ends_at, ends_at)
    vampytest.assert_is(entitlement.type, entitlement_type)
    vampytest.assert_eq(entitlement.gift_code_flags, gift_code_flags)
    vampytest.assert_eq(entitlement.guild_id, guild_id)
    vampytest.assert_eq(entitlement.promotion_id, promotion_id)
    vampytest.assert_is(entitlement.source_type, source_type)
    vampytest.assert_eq(entitlement.sku_id, sku_id)
    vampytest.assert_eq(entitlement.starts_at, starts_at)
    vampytest.assert_eq(entitlement.subscription_id, subscription_id)
    vampytest.assert_eq(entitlement.user_id, user_id)


def test__Entitlement__update_attributes():
    """
    Tests whether ``Entitlement._update_attributes`` works as intended.
    """
    entitlement_id = 202310040034
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    
    data = {
        'consumed': consumed,
        'deleted': deleted,
        'ends_at': datetime_to_timestamp(ends_at),
        'starts_at': datetime_to_timestamp(starts_at),
    }
    
    entitlement = Entitlement._create_empty(entitlement_id)
    entitlement._update_attributes(data)
    
    vampytest.assert_eq(entitlement.consumed, consumed)
    vampytest.assert_eq(entitlement.deleted, deleted)
    vampytest.assert_eq(entitlement.ends_at, ends_at)
    vampytest.assert_eq(entitlement.starts_at, starts_at)


def test__Entitlement__difference_update_attributes():
    """
    Tests whether ``Entitlement._difference_update_attributes`` works as intended.
    """
    entitlement_id = 202310040035
    
    old_consumed = True
    old_deleted = True
    old_ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    
    new_consumed = False
    new_deleted = False
    new_ends_at = DateTime(2016, 10, 14, tzinfo = TimeZone.utc)
    new_starts_at = DateTime(2015, 10, 14, tzinfo = TimeZone.utc)
    
    data = {
        'consumed': new_consumed,
        'deleted': new_deleted,
        'ends_at': datetime_to_timestamp(new_ends_at),
        'starts_at': datetime_to_timestamp(new_starts_at),
    }
    
    entitlement = Entitlement.precreate(
        entitlement_id,
        consumed = old_consumed,
        deleted = old_deleted,
        ends_at = old_ends_at,
        starts_at = old_starts_at,
    )
    
    old_attributes = entitlement._difference_update_attributes(data)
    
    vampytest.assert_eq(entitlement.consumed, new_consumed)
    vampytest.assert_eq(entitlement.deleted, new_deleted)
    vampytest.assert_eq(entitlement.ends_at, new_ends_at)
    vampytest.assert_eq(entitlement.starts_at, new_starts_at)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'consumed': old_consumed,
            'deleted': old_deleted,
            'ends_at': old_ends_at,
            'starts_at': old_starts_at,
        },
    )


def test__Entitlement__to_data__full():
    """
    Tests whether ``Entitlement.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    entitlement_id = 202310040017
    application_id = 202310040018
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    gift_code_flags = GiftCodeFlag(12)
    guild_id = 202310040019
    promotion_id = 202507020004
    source_type = EntitlementSourceType.user_gift
    sku_id = 202310040020
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040021
    user_id = 202310040022
    
    sku = SKU.precreate(
        sku_id,
        application_id = application_id,
        name = 'yuuka',
    )
    
    expected_output = {
        'id': str(entitlement_id),
        'application_id': str(application_id),
        'consumed': consumed,
        'deleted': deleted,
        'ends_at': datetime_to_timestamp(ends_at),
        'gift_code_flags': int(gift_code_flags),
        'type': entitlement_type.value,
        'guild_id': str(guild_id),
        'promotion_id': str(promotion_id),
        'source_type': source_type.value,
        'sku': sku.to_data(defaults = True, include_internals = True),
        'sku_id': str(sku_id),
        'starts_at': datetime_to_timestamp(starts_at),
        'subscription_id': str(subscription_id),
        'user_id': str(user_id),
    }
    
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
    
    vampytest.assert_eq(
        entitlement.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Entitlement__to_data__partial():
    """
    Tests whether ``Entitlement.to_data`` works as intended.
    
    Case: do not include internals.
    """
    guild_id = 202310040023
    sku_id = 202310040024
    
    
    expected_output = {
        'owner_type': EntitlementOwnerType.guild.value,
        'owner_id': str(guild_id),
        'sku_id': str(sku_id),
    }
    
    entitlement = Entitlement(
        guild_id = guild_id,
        sku_id = sku_id,
    )
    
    vampytest.assert_eq(entitlement.to_data(defaults = True, include_internals = False), expected_output)
