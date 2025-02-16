import vampytest

from ...message_role_subscription import MessageRoleSubscription

from ..fields import put_role_subscription


def test__put_role_subscription():
    """
    Tests whether ``put_role_subscription`` is working as intended.
    """
    message_role_subscription = MessageRoleSubscription(tier_name = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (message_role_subscription, False, {'role_subscription_data': message_role_subscription.to_data()}),
        (
            message_role_subscription,
            True,
            {'role_subscription_data': message_role_subscription.to_data(defaults = True)},
        ),
    ):
        data = put_role_subscription(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
