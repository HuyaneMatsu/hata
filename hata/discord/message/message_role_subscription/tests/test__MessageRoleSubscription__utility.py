import vampytest

from ..message_role_subscription import MessageRoleSubscription

from .test__MessageRoleSubscription__constructor import _check_is_all_attribute_set


def test__MessageRoleSubscription__copy():
    """
    Tests whether ``MessageRoleSubscription.copy`` works as intended.
    """
    renewal = True
    subscription_listing_id = 202301200007
    tier_name = 'Nue'
    total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months
    )
    copy = message_role_subscription.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_role_subscription, copy)
    
    vampytest.assert_eq(message_role_subscription, copy)


def test__MessageRoleSubscription__copy_with__0():
    """
    Tests whether ``MessageRoleSubscription.copy_with`` works as intended.
    
    Case: no fields given.
    """
    renewal = True
    subscription_listing_id = 202301200008
    tier_name = 'Nue'
    total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months,
    )
    copy = message_role_subscription.copy_with()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_role_subscription, copy)
    
    vampytest.assert_eq(message_role_subscription, copy)


def test__MessageRoleSubscription__copy_with__1():
    """
    Tests whether ``MessageRoleSubscription.copy_with`` works as intended.
    
    Case: all no fields given.
    """
    old_renewal = True
    old_tier_name = 'Nue'
    old_subscription_listing_id = 202301200009
    old_total_months = 3
    new_renewal = False
    new_tier_name = 'Remilia'
    new_subscription_listing_id = 202301200010
    new_total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = old_renewal,
        subscription_listing_id = old_subscription_listing_id,
        tier_name = old_tier_name,
        total_months = old_total_months,
    )
    copy = message_role_subscription.copy_with(
        renewal = new_renewal,
        subscription_listing_id = new_subscription_listing_id,
        tier_name = new_tier_name,
        total_months = new_total_months
    )
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(message_role_subscription, copy)
    
    vampytest.assert_eq(copy.renewal, new_renewal)
    vampytest.assert_eq(copy.subscription_listing_id, new_subscription_listing_id)
    vampytest.assert_eq(copy.tier_name, new_tier_name)
    vampytest.assert_eq(copy.total_months, new_total_months)
