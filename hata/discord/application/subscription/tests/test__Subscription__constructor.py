from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..subscription import Subscription
from ..preinstanced import SubscriptionStatus


def _assert_fields_set(subscription):
    """
    Asserts whether every attributes of the given subscription are set.
    
    Parameters
    ----------
    subscription : ``Subscription``
        The subscription check.
    """
    vampytest.assert_instance(subscription, Subscription)
    vampytest.assert_instance(subscription.cancelled_at, DateTime, nullable = True)
    vampytest.assert_instance(subscription.country_code, str, nullable = True)
    vampytest.assert_instance(subscription.current_period_end, DateTime, nullable = True)
    vampytest.assert_instance(subscription.current_period_start, DateTime, nullable = True)
    vampytest.assert_instance(subscription.entitlement_ids, tuple, nullable = True)
    vampytest.assert_instance(subscription.id, int)
    vampytest.assert_instance(subscription.renewal_sku_ids, tuple, nullable = True)
    vampytest.assert_instance(subscription.sku_ids, tuple, nullable = True)
    vampytest.assert_instance(subscription.status, SubscriptionStatus)
    vampytest.assert_instance(subscription.user_id, int)


def test__Subscription__new__no_fields():
    """
    Tests whether ``Subscription.__new__`` works as intended.
    
    Case: No parameters given.
    """
    subscription = Subscription()
    _assert_fields_set(subscription)


def test__Subscription__new__all_fields():
    """
    Tests whether ``Subscription.__new__`` works as intended.
    
    Case: All parameters given.
    """
    entitlement_ids = [202409220020, 202409220021]
    renewal_sku_ids = [202412210010, 202412210011]
    sku_ids = [202409220022, 202409220023]
    user_id = 202409220024
    
    subscription = Subscription(
        entitlement_ids = entitlement_ids,
        renewal_sku_ids = renewal_sku_ids,
        sku_ids = sku_ids,
        user_id = user_id,
    )
    _assert_fields_set(subscription)
    
    vampytest.assert_eq(subscription.entitlement_ids, tuple(entitlement_ids))
    vampytest.assert_eq(subscription.renewal_sku_ids, tuple(renewal_sku_ids))
    vampytest.assert_eq(subscription.sku_ids, tuple(sku_ids))
    vampytest.assert_eq(subscription.user_id, user_id)


def test__Subscription__create_empty():
    """
    Tests whether ``Subscription._create_empty`` works as intended.
    """
    subscription_id = 202409220025
    
    subscription = Subscription._create_empty(subscription_id)
    _assert_fields_set(subscription)
    vampytest.assert_eq(subscription.id, subscription_id)


def test__Subscription__precreate__no_fields():
    """
    Tests whether ``Subscription.precreate`` works as intended.
    
    Case: No parameters given.
    """
    subscription_id = 202409220026
    
    subscription = Subscription.precreate(subscription_id)
    _assert_fields_set(subscription)
    vampytest.assert_eq(subscription.id, subscription_id)


def test__Subscription__precreate__all_fields():
    """
    Tests whether ``Subscription.precreate`` works as intended.
    
    Case: All parameters given.
    """
    subscription_id = 202409220027
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220028, 202409220029]
    renewal_sku_ids = [202412210012, 202412210013]
    sku_ids = [202409220030, 202409220031]
    status = SubscriptionStatus.ending
    user_id = 202409220032
    
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


def test__Subscription__precreate__caching():
    """
    Tests whether ``Subscription.precreate`` works as intended.
    
    Case: Caching.
    """
    subscription_id = 202409220033
    
    subscription = Subscription.precreate(subscription_id)
    test_subscription = Subscription.precreate(subscription_id)
    
    vampytest.assert_is(subscription, test_subscription)
