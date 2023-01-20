import vampytest

from ..fields import parse_role_subscription
from ..message_role_subscription import MessageRoleSubscription


def test__parse_role_subscription():
    """
    Tests whether ``parse_role_subscription`` works as intended.
    """
    message_role_subscription = MessageRoleSubscription(tier_name = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'role_subscription_data': None}, None),
        ({'role_subscription_data': message_role_subscription.to_data()}, message_role_subscription),
    ):
        output = parse_role_subscription(input_data)
        vampytest.assert_eq(output, expected_output)
