import vampytest

from ..fields import put_send_start_notification_into


def test__put_send_start_notification_into():
    """
    Tests whether ``put_send_start_notification_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'send_start_notification': False}),
        (True, False, {'send_start_notification': True}),
    ):
        data = put_send_start_notification_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
