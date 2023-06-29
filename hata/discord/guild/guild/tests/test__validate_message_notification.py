import vampytest

from ..fields import validate_message_notification
from ..preinstanced import MessageNotificationLevel


def test__validate_message_notification__0():
    """
    Tests whether `validate_message_notification` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (MessageNotificationLevel.none, MessageNotificationLevel.none),
        (MessageNotificationLevel.none.value, MessageNotificationLevel.none)
    ):
        output = validate_message_notification(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_message_notification__1():
    """
    Tests whether `validate_message_notification` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_message_notification(input_value)
