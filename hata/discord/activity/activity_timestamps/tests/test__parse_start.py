from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..fields import parse_start


def test__parse_start():
    """
    Tests whether ``parse_start`` works as intended.
    """
    date = DateTime(2016, 1, 14)
    
    for input_data, expected_output in (
        ({}, None),
        ({'start': None}, None),
        ({'start': datetime_to_millisecond_unix_time(date)}, date)
    ):
        output = parse_start(input_data)
        vampytest.assert_eq(output, expected_output)
