import vampytest

from ..message_role_subscription import MessageRoleSubscription

from .test__MessageRoleSubscription__constructor import _assert_fields_set


def test__MessageRoleSubscription__from_data():
    """
    Tests whether ``MessageRoleSubscription.from_data`` works as intended.
    """
    renewal = True
    subscription_listing_id = 202301200001
    tier_name = 'Nue'
    total_months = 3
    
    data = {
        'is_renewal': renewal,
        'role_subscription_listing_id': str(subscription_listing_id),
        'tier_name': tier_name,
        'total_months_subscribed': total_months,
    }
    
    message_role_subscription = MessageRoleSubscription.from_data(data)
    _assert_fields_set(message_role_subscription)

    vampytest.assert_eq(message_role_subscription.renewal, renewal)
    vampytest.assert_eq(message_role_subscription.subscription_listing_id, subscription_listing_id)
    vampytest.assert_eq(message_role_subscription.tier_name, tier_name)
    vampytest.assert_eq(message_role_subscription.total_months, total_months)


def test__MessageRoleSubscription__to_data():
    """
    Tests whether ``MessageRoleSubscription.to_data`` works as intended.
    
    Case: include defaults.
    """
    renewal = True
    subscription_listing_id = 202301200002
    tier_name = 'Nue'
    total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months,
    )
    
    expected_output = {
        'is_renewal': renewal,
        'role_subscription_listing_id': str(subscription_listing_id),
        'tier_name': tier_name,
        'total_months_subscribed': total_months,
    }
    
    vampytest.assert_eq(
        message_role_subscription.to_data(
            defaults = True,
        ),
        expected_output,
    )
