import vampytest

from ..fields import put_send_start_notification


def test__put_send_start_notification():
    """
    Tests whether ``put_send_start_notification`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'send_start_notification': False}),
        (True, False, {'send_start_notification': True}),
    ):
        data = put_send_start_notification(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
