import vampytest

from ..fields import validate_role_subscription
from ..message_role_subscription import MessageRoleSubscription


def test__validate_role_subscription__0():
    """
    Tests whether `validate_role_subscription` works as intended.
    
    Case: passing.
    """
    message_role_subscription = MessageRoleSubscription(tier_name = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (message_role_subscription, message_role_subscription),
    ):
        output = validate_role_subscription(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_role_subscription__1():
    """
    Tests whether `validate_role_subscription` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_role_subscription(input_value)
