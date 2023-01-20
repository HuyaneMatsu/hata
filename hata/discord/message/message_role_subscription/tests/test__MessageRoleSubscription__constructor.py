import vampytest

from ..message_role_subscription import MessageRoleSubscription


def _check_is_all_attribute_set(message_role_subscription):
    """
    Tests whether all attributes are set of the given message activity.
    
    Parameters
    ----------
    message_role_subscription : ``MessageRoleSubscription``
        The message activity to check.
    """
    vampytest.assert_instance(message_role_subscription, MessageRoleSubscription)
    vampytest.assert_instance(message_role_subscription.renewal, bool)
    vampytest.assert_instance(message_role_subscription.subscription_listing_id, int)
    vampytest.assert_instance(message_role_subscription.tier_name, str)
    vampytest.assert_instance(message_role_subscription.total_months, int)


def test__MessageRoleSubscription__new__0():
    """
    Tests whether ``MessageRoleSubscription.__new__`` works as intended.
    
    Case: No fields given.
    """
    message_role_subscription = MessageRoleSubscription()
    _check_is_all_attribute_set(message_role_subscription)


def test__MessageRoleSubscription__new__1():
    """
    Tests whether ``MessageRoleSubscription.__new__`` works as intended.
    
    Case: All fields given.
    """
    renewal = True
    subscription_listing_id = 202301200000
    tier_name = 'Nue'
    total_months = 3

    message_role_subscription = MessageRoleSubscription(
        renewal = renewal,
        subscription_listing_id = subscription_listing_id,
        tier_name = tier_name,
        total_months = total_months,
    )
    _check_is_all_attribute_set(message_role_subscription)
    
    vampytest.assert_eq(message_role_subscription.renewal, renewal)
    vampytest.assert_eq(message_role_subscription.subscription_listing_id, subscription_listing_id)
    vampytest.assert_eq(message_role_subscription.tier_name, tier_name)
    vampytest.assert_eq(message_role_subscription.total_months, total_months)
