from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..subscription import Subscription
from ..preinstanced import SubscriptionStatus


def test__Subscription__repr():
    """
    Tests whether ``Subscription.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    subscription_id = 202409220059
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220060, 202409220061]
    sku_ids = [202409220062, 202409220063]
    status = SubscriptionStatus.ending
    user_id = 202409220064
    
    subscription = Subscription.precreate(
        subscription_id,
        cancelled_at = cancelled_at,
        country_code = country_code,
        current_period_end = current_period_end,
        current_period_start = current_period_start,
        entitlement_ids = entitlement_ids,
        sku_ids = sku_ids,
        status = status,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(subscription), str)


def test__Subscription__hash():
    """
    Tests whether ``Subscription.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    subscription_id = 202409220065
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    country_code = 'AA'
    current_period_end = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    current_period_start = DateTime(2016, 5, 16, tzinfo = TimeZone.utc)
    entitlement_ids = [202409220066, 202409220067]
    sku_ids = [202409220068, 202409220069]
    status = SubscriptionStatus.ending
    user_id = 202409220070
    
    keyword_parameters = {
        'entitlement_ids': entitlement_ids,
        'sku_ids': sku_ids,
        'user_id': user_id,
    }
    
    # Full
    subscription = Subscription.precreate(
        subscription_id,
        cancelled_at = cancelled_at,
        country_code = country_code,
        current_period_end = current_period_end,
        current_period_start = current_period_start,
        status = status,
    )
    
    vampytest.assert_instance(hash(subscription), int)
    
    # Partial
    subscription = Subscription(**keyword_parameters,)
    
    vampytest.assert_instance(hash(subscription), int)


def _iter_options__eq__partial():
    entitlement_ids = [202409230000, 202409220001]
    sku_ids = [202409220002, 202409220003]
    user_id = 202409220004
    
    keyword_parameters = {
        'entitlement_ids': entitlement_ids,
        'sku_ids': sku_ids,
        'user_id': user_id,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'entitlement_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sku_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': 202409220005,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__partial()).returning_last())
def test__Subscription__eq__partial(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Subscription.__eq__`` works as intended.
    
    Case: partial
    
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
    subscription_0 = Subscription(**keyword_parameters_0)
    subscription_1 = Subscription(**keyword_parameters_1)
    
    output = subscription_0 == subscription_1
    vampytest.assert_instance(output, bool)
    return output


def test__Subscription__eq():
    """
    Tests whether ``Subscription.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    subscription_id_0 = 202409220071
    subscription_id_1 = 202409220006
    entitlement_ids_0 = [202409220072, 202409220073]
    entitlement_ids_1 = [202409220074, 202409220075]
    
    subscription_0 = Subscription.precreate(
        subscription_id_0,
        entitlement_ids = entitlement_ids_0,
    )
    
    subscription_1 = Subscription.precreate(
        subscription_id_1,
        entitlement_ids = entitlement_ids_1,
    )
    
    subscription_2 = Subscription(
        entitlement_ids = entitlement_ids_0
    )
    
    vampytest.assert_eq(subscription_0, subscription_0)
    vampytest.assert_ne(subscription_0, subscription_1)
    vampytest.assert_ne(subscription_1, subscription_2)
    vampytest.assert_eq(subscription_0, subscription_2)
    vampytest.assert_ne(subscription_0, object())
