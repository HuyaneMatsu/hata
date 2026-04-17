from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..subscription import Subscription
from ..preinstanced import SubscriptionStatus

from .test__Subscription__constructor import _assert_fields_set


def test__Subscription__from_data():
    """
    Tests whether ``Subscription.from_data`` works as intended.
    
    Case: Default.
    """
    subscription_id = 202409220033
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220034, 202409220035]
    renewal_sku_ids = [202412210013, 202412210014]
    sku_ids = [202409220036, 202409220037]
    status = SubscriptionStatus.ending
    user_id = 202409220038
    
    data = {
        'id': str(subscription_id),
        'cancelled_at': datetime_to_timestamp(cancelled_at),
        'country': country_code,
        'current_period_end': datetime_to_timestamp(current_period_end),
        'current_period_start': datetime_to_timestamp(current_period_start),
        'entitlement_ids': [str(entitlement_id) for entitlement_id in entitlement_ids],
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'status': status.value,
        'user_id': str(user_id),
    }
    
    subscription = Subscription.from_data(data)
    _assert_fields_set(subscription)
    vampytest.assert_eq(subscription.id, subscription_id)
    
    vampytest.assert_eq(subscription.cancelled_at, cancelled_at)
    vampytest.assert_eq(subscription.country_code, country_code)
    vampytest.assert_eq(subscription.current_period_end, current_period_end)
    vampytest.assert_eq(subscription.current_period_start, current_period_start)
    vampytest.assert_eq(subscription.entitlement_ids, tuple(entitlement_ids))
    vampytest.assert_eq(subscription.renewal_sku_ids, tuple(renewal_sku_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(sku_ids))
    vampytest.assert_is(subscription.status, status)
    vampytest.assert_eq(subscription.user_id, user_id)


def test__Subscription__from_data__caching():
    """
    Tests whether ``Subscription.from_data`` works as intended.
    
    Case: Caching.
    """
    subscription_id = 202409220039
    
    data = {
        'id': str(subscription_id),
    }
    
    subscription = Subscription.from_data(data)
    test_subscription = Subscription.from_data(data)
    vampytest.assert_eq(subscription, test_subscription)


def test__Subscription__from_data_is_created():
    """
    Tests whether ``Subscription.from_data_is_created`` works as intended.
    
    Case: Default.
    """
    subscription_id = 202409220040
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220041, 202409220042]
    renewal_sku_ids = [202412210015, 202412210016]
    sku_ids = [202409220043, 202409220044]
    status = SubscriptionStatus.ending
    user_id = 202409220045
    
    data = {
        'id': str(subscription_id),
        'cancelled_at': datetime_to_timestamp(cancelled_at),
        'country': country_code,
        'current_period_end': datetime_to_timestamp(current_period_end),
        'current_period_start': datetime_to_timestamp(current_period_start),
        'entitlement_ids': [str(entitlement_id) for entitlement_id in entitlement_ids],
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'status': status.value,
        'user_id': str(user_id),
    }
    
    subscription, is_created = Subscription.from_data_is_created(data)
    _assert_fields_set(subscription)
    vampytest.assert_eq(subscription.id, subscription_id)
    
    vampytest.assert_instance(is_created, bool)
    vampytest.assert_eq(is_created, True)
    
    vampytest.assert_eq(subscription.cancelled_at, cancelled_at)
    vampytest.assert_eq(subscription.country_code, country_code)
    vampytest.assert_eq(subscription.current_period_end, current_period_end)
    vampytest.assert_eq(subscription.current_period_start, current_period_start)
    vampytest.assert_eq(subscription.entitlement_ids, tuple(entitlement_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(sku_ids))
    vampytest.assert_is(subscription.status, status)
    vampytest.assert_eq(subscription.user_id, user_id)


def test__Subscription__from_data_is_created__caching():
    """
    Tests whether ``Subscription.from_data_is_created`` works as intended.
    
    Case: Caching.
    """
    subscription_id = 202409220046
    
    data = {
        'id': str(subscription_id),
    }
    
    subscription, is_created_0 = Subscription.from_data_is_created(data)
    test_subscription, is_created_1 = Subscription.from_data_is_created(data)
    vampytest.assert_eq(subscription, test_subscription)

    vampytest.assert_instance(is_created_0, bool)
    vampytest.assert_eq(is_created_0, True)


    vampytest.assert_instance(is_created_1, bool)
    vampytest.assert_eq(is_created_1, False)


def test__Subscription__set_attributes():
    """
    Tests whether ``Subscription._set_attributes`` works as intended.
    """
    subscription_id = 202409220046
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220047, 202409220048]
    renewal_sku_ids = [202412210016, 202412210017]
    sku_ids = [202409220048, 202409220049]
    status = SubscriptionStatus.ending
    user_id = 202409220050
    
    data = {
        'cancelled_at': datetime_to_timestamp(cancelled_at),
        'country': country_code,
        'current_period_end': datetime_to_timestamp(current_period_end),
        'current_period_start': datetime_to_timestamp(current_period_start),
        'entitlement_ids': [str(entitlement_id) for entitlement_id in entitlement_ids],
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'status': status.value,
        'user_id': str(user_id),
    }
    
    subscription = Subscription._create_empty(subscription_id)
    subscription._set_attributes(data)
    
    vampytest.assert_eq(subscription.cancelled_at, cancelled_at)
    vampytest.assert_eq(subscription.country_code, country_code)
    vampytest.assert_eq(subscription.current_period_end, current_period_end)
    vampytest.assert_eq(subscription.current_period_start, current_period_start)
    vampytest.assert_eq(subscription.entitlement_ids, tuple(entitlement_ids))
    vampytest.assert_eq(subscription.renewal_sku_ids, tuple(renewal_sku_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(sku_ids))
    vampytest.assert_is(subscription.status, status)
    vampytest.assert_eq(subscription.user_id, user_id)


def test__Subscription__update_attributes():
    """
    Tests whether ``Subscription._update_attributes`` works as intended.
    """
    subscription_id = 202409220051
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AB'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    renewal_sku_ids = [202412210018, 202412210019]
    sku_ids = [202409220020, 202409220021]
    status = SubscriptionStatus.ending
    
    data = {
        'cancelled_at': datetime_to_timestamp(cancelled_at),
        'country': country_code,
        'current_period_end': datetime_to_timestamp(current_period_end),
        'current_period_start': datetime_to_timestamp(current_period_start),
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'status': status.value,
    }
    
    subscription = Subscription._create_empty(subscription_id)
    subscription._update_attributes(data)
    
    vampytest.assert_eq(subscription.cancelled_at, cancelled_at)
    vampytest.assert_eq(subscription.country_code, country_code)
    vampytest.assert_eq(subscription.current_period_end, current_period_end)
    vampytest.assert_eq(subscription.current_period_start, current_period_start)
    vampytest.assert_eq(subscription.renewal_sku_ids, tuple(renewal_sku_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(sku_ids))
    vampytest.assert_is(subscription.status, status)


def test__Subscription__difference_update_attributes():
    """
    Tests whether ``Subscription._difference_update_attributes`` works as intended.
    """
    subscription_id = 202409220052
    
    old_cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_country_code = 'AB'
    old_current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    old_current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    old_renewal_sku_ids = [202412210022, 202412210023]
    old_sku_ids = [202409220024, 202409220025]
    old_status = SubscriptionStatus.ending
    
    new_cancelled_at = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)
    new_country_code = 'AC'
    new_current_period_end = DateTime(2016, 6, 15, tzinfo = TimeZone.utc)
    new_current_period_start = DateTime(2016, 6, 16, tzinfo = TimeZone.utc)
    new_renewal_sku_ids = [202412210026, 202412210027]
    new_sku_ids = [202409220028, 202409220029]
    new_status = SubscriptionStatus.inactive
    
    data = {
        'cancelled_at': datetime_to_timestamp(new_cancelled_at),
        'country': new_country_code,
        'current_period_end': datetime_to_timestamp(new_current_period_end),
        'current_period_start': datetime_to_timestamp(new_current_period_start),
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in new_renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in new_sku_ids],
        'status': new_status.value,
    }
    
    subscription = Subscription.precreate(
        subscription_id,
        cancelled_at = old_cancelled_at,
        country_code = old_country_code,
        current_period_end = old_current_period_end,
        current_period_start = old_current_period_start,
        renewal_sku_ids = old_renewal_sku_ids,
        sku_ids = old_sku_ids,
        status = old_status,
    )
    
    old_attributes = subscription._difference_update_attributes(data)
    
    vampytest.assert_eq(subscription.cancelled_at, new_cancelled_at)
    vampytest.assert_eq(subscription.country_code, new_country_code)
    vampytest.assert_eq(subscription.current_period_end, new_current_period_end)
    vampytest.assert_eq(subscription.current_period_start, new_current_period_start)
    vampytest.assert_eq(subscription.renewal_sku_ids, tuple(new_renewal_sku_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(new_sku_ids))
    vampytest.assert_is(subscription.status, new_status)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'cancelled_at': old_cancelled_at,
            'country_code': old_country_code,
            'current_period_end': old_current_period_end,
            'current_period_start': old_current_period_start,
            'status': old_status,
            'renewal_sku_ids': tuple(old_renewal_sku_ids),
            'sku_ids': tuple(old_sku_ids),
        },
    )


def test__Subscription__to_data__full():
    """
    Tests whether ``Subscription.to_data`` works as intended.
    
    Case: include defaults.
    """
    subscription_id = 202409220053
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220054, 202409220055]
    renewal_sku_ids = [202412210030, 202412210031]
    sku_ids = [202409220056, 202409220057]
    status = SubscriptionStatus.ending
    user_id = 202409220058
    
    
    expected_output = {
        'id': str(subscription_id),
        'cancelled_at': datetime_to_timestamp(cancelled_at),
        'country': country_code,
        'current_period_end': datetime_to_timestamp(current_period_end),
        'current_period_start': datetime_to_timestamp(current_period_start),
        'entitlement_ids': [str(entitlement_id) for entitlement_id in entitlement_ids],
        'renewal_sku_ids': [str(renewal_sku_id) for renewal_sku_id in renewal_sku_ids],
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'status': status.value,
        'user_id': str(user_id),
    }
    
    subscription = Subscription.precreate(
        subscription_id,
        cancelled_at = cancelled_at,
        country_code = country_code,
        current_period_end = current_period_end,
        current_period_start = current_period_start,
        entitlement_ids = entitlement_ids,
        renewal_sku_ids = renewal_sku_ids,
        sku_ids = sku_ids,
        status = status,
        user_id = user_id,
    )
    
    vampytest.assert_eq(subscription.to_data(defaults = True), expected_output)
