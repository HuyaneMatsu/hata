from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_joined_at


def test__parse_joined_at():
    """
    Tests whether ``parse_joined_at`` works as intended.
    """
    joined_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'joined_at': None}, None),
        ({'joined_at': datetime_to_timestamp(joined_at)}, joined_at),
    ):
        output = parse_joined_at(input_value)
        vampytest.assert_eq(output, expected_output)
