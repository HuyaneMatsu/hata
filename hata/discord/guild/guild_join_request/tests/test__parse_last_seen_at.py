from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_last_seen_at


def test__parse_last_seen_at():
    """
    Tests whether ``parse_last_seen_at`` works as intended.
    """
    last_seen_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'last_seen': None}, None),
        ({'last_seen': datetime_to_timestamp(last_seen_at)}, last_seen_at),
    ):
        output = parse_last_seen_at(input_value)
        vampytest.assert_eq(output, expected_output)
