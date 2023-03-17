from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_start


def test__parse_start():
    """
    Tests whether ``parse_start`` works as intended.
    """
    start = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'scheduled_start_time': None}, None),
        ({'scheduled_start_time': datetime_to_timestamp(start)}, start),
    ):
        output = parse_start(input_value)
        vampytest.assert_eq(output, expected_output)
