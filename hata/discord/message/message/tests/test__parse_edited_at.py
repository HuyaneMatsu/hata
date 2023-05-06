from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_edited_at


def test__parse_edited_at():
    """
    Tests whether ``parse_edited_at`` works as intended.
    """
    edited_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'edited_timestamp': None}, None),
        ({'edited_timestamp': datetime_to_timestamp(edited_at)}, edited_at),
    ):
        output = parse_edited_at(input_value)
        vampytest.assert_eq(output, expected_output)
