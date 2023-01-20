import vampytest

from ..message_role_subscription import MessageRoleSubscription


def test__MessageRoleSubscription__repr():
    """
    Tests whether ``MessageRoleSubscription.__repr__`` works as intended.
    """
    renewal = True
    subscription_listing_id = 202301200003
    tier_name = 'Nue'
    total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months,
    )
    
    vampytest.assert_instance(repr(message_role_subscription), str)


def test__MessageRoleSubscription__hash():
    """
    Tests whether ``MessageRoleSubscription.__hash__`` works as intended.
    """
    renewal = True
    subscription_listing_id = 202301200004
    tier_name = 'Nue'
    total_months = 3
    
    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months,
    )
    
    vampytest.assert_instance(hash(message_role_subscription), int)


def test__MessageRoleSubscription__eq():
    """
    Tests whether ``MessageRoleSubscription.__eq__`` works as intended.
    """
    renewal = True
    subscription_listing_id = 202301200005
    tier_name = 'Nue'
    total_months = 3
    
    keyword_parameters = {
        'renewal': renewal,
        'subscription_listing_id': subscription_listing_id,
        'tier_name': tier_name,
        'total_months': total_months,
    }
    
    message_role_subscription = MessageRoleSubscription(**keyword_parameters)
    
    vampytest.assert_eq(message_role_subscription, message_role_subscription)
    vampytest.assert_ne(message_role_subscription, object())
    
    for field_name, field_value in (
        ('renewal', False),
        ('subscription_listing_id', 202301200006),
        ('tier_name', 'Remilia'),
        ('total_months', 4),
    ):
        test_message_role_subscription = MessageRoleSubscription(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(message_role_subscription, test_message_role_subscription)
