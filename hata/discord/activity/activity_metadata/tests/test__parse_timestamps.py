from datetime import datetime as DateTime

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import parse_timestamps


def test__parse_timestamps():
    """
    Tests whether ``parse_timestamps`` works as intended.
    """
    timestamps = ActivityTimestamps(start = DateTime(2016, 5, 14))
    
    for input_data, expected_output in (
        ({}, None),
        ({'timestamps': None}, None),
        ({'timestamps': timestamps.to_data()}, timestamps),
    ):
        output = parse_timestamps(input_data)
        vampytest.assert_eq(output, expected_output)
