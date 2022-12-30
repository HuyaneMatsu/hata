from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..fields import parse_created_at


def test__parse_created_at():
    """
    Tests whether ``parse_created_at`` works as intended.
    """
    date = DateTime(2016, 1, 14)
    
    for input_data, expected_output in (
        ({}, None),
        ({'created_at': None}, None),
        ({'created_at': datetime_to_millisecond_unix_time(date)}, date)
    ):
        output = parse_created_at(input_data)
        vampytest.assert_eq(output, expected_output)
