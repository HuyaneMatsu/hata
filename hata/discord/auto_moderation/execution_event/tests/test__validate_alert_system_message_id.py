import vampytest

from ....message import Message

from ..fields import validate_alert_system_message_id


def test__validate_alert_system_message_id__0():
    """
    Tests whether `validate_alert_system_message_id` works as intended.
    
    Case: passing.
    """
    alert_system_message_id = 202211160010
    
    for input_value, expected_output in (
        (None, 0),
        (alert_system_message_id, alert_system_message_id),
        (Message.precreate(alert_system_message_id), alert_system_message_id),
        (str(alert_system_message_id), alert_system_message_id)
    ):
        output = validate_alert_system_message_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_alert_system_message_id__1():
    """
    Tests whether `validate_alert_system_message_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_alert_system_message_id(input_value)


def test__validate_alert_system_message_id__2():
    """
    Tests whether `validate_alert_system_message_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_alert_system_message_id(input_value)
