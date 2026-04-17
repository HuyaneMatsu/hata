import vampytest

from ..fields import parse_safety_alerts_channel_id


def test__parse_safety_alerts_channel_id():
    """
    Tests whether ``parse_safety_alerts_channel_id`` works as intended.
    """
    safety_alerts_channel_id = 202301150016
    
    for input_data, expected_output in (
        ({}, 0),
        ({'safety_alerts_channel_id': None}, 0),
        ({'safety_alerts_channel_id': str(safety_alerts_channel_id)}, safety_alerts_channel_id),
    ):
        output = parse_safety_alerts_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
