from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_end


def test__parse_end():
    """
    Tests whether ``parse_end`` works as intended.
    """
    end = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'scheduled_end_time': None}, None),
        ({'scheduled_end_time': datetime_to_timestamp(end)}, end),
    ):
        output = parse_end(input_value)
        vampytest.assert_eq(output, expected_output)
