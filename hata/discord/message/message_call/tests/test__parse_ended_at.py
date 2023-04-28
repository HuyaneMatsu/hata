from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_ended_at


def test__parse_ended_at():
    """
    Tests whether ``parse_ended_at`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'ended_timestamp': None}, None),
        ({'ended_timestamp': datetime_to_timestamp(ended_at)}, ended_at),
    ):
        output = parse_ended_at(input_value)
        vampytest.assert_eq(output, expected_output)
