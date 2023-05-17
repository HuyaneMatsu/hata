from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_created_at


def test__parse_created_at():
    """
    Tests whether ``parse_created_at`` works as intended.
    """
    created_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'created_at': None}, None),
        ({'created_at': datetime_to_timestamp(created_at)}, created_at),
    ):
        output = parse_created_at(input_value)
        vampytest.assert_eq(output, expected_output)
