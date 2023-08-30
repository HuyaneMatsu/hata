import vampytest

from ..fields import validate_send_start_notification


def test__validate_send_start_notification__0():
    """
    Tests whether `validate_send_start_notification` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_send_start_notification(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_send_start_notification__1():
    """
    Tests whether `validate_send_start_notification` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_send_start_notification(input_value)
