import vampytest

from ..fields import parse_alert_system_message_id


def test__parse_alert_system_message_id():
    """
    Tests whether ``parse_alert_system_message_id`` works as intended.
    """
    alert_system_message_id = 202211160000
    
    for input_data, expected_output in (
        ({}, 0),
        ({'alert_system_message_id': None}, 0),
        ({'alert_system_message_id': str(alert_system_message_id)}, alert_system_message_id),
    ):
        output = parse_alert_system_message_id(input_data)
        vampytest.assert_eq(output, expected_output)
