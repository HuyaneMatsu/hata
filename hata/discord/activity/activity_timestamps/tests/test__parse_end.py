from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..fields import parse_end


def test__parse_end():
    """
    Tests whether ``parse_end`` works as intended.
    """
    date = DateTime(2016, 1, 14)
    
    for input_data, expected_output in (
        ({}, None),
        ({'end': None}, None),
        ({'end': datetime_to_millisecond_unix_time(date)}, date)
    ):
        output = parse_end(input_data)
        vampytest.assert_eq(output, expected_output)
