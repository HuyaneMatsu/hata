from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_timestamp


def test__parse_timestamp():
    """
    Tests whether ``parse_timestamp`` works as intended.
    """
    timestamp = DateTime(2016, 9, 9)
    
    for input_data, expected_output in (
        ({}, None),
        ({'timestamp': None}, None),
        ({'timestamp': datetime_to_timestamp(timestamp)}, timestamp),
    ):
        output = parse_timestamp(input_data)
        vampytest.assert_eq(output, expected_output)
