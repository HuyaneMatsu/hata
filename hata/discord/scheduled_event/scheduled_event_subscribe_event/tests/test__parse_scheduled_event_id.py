import vampytest

from ..fields import parse_scheduled_event_id


def test__parse_scheduled_event_id():
    """
    Tests whether ``parse_scheduled_event_id`` works as intended.
    """
    scheduled_event_id = 202303110064
    
    for input_data, expected_output in (
        ({}, 0),
        ({'guild_scheduled_event_id': None}, 0),
        ({'guild_scheduled_event_id': str(scheduled_event_id)}, scheduled_event_id),
    ):
        output = parse_scheduled_event_id(input_data)
        vampytest.assert_eq(output, expected_output)
