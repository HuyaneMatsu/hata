import vampytest

from ..fields import parse_send_start_notification


def test__parse_send_start_notification():
    """
    Tests whether ``parse_send_start_notification`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'send_start_notification': False}, False),
        ({'send_start_notification': True}, True),
    ):
        output = parse_send_start_notification(input_data)
        vampytest.assert_eq(output, expected_output)
