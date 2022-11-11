from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_timed_out_until


def test__parse_timed_out_until():
    """
    Tests whether ``parse_timed_out_until`` works as intended.
    """
    timed_out_until = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'communication_disabled_until': None}, None),
        ({'communication_disabled_until': datetime_to_timestamp(timed_out_until)}, timed_out_until),
    ):
        output = parse_timed_out_until(input_value)
        vampytest.assert_eq(output, expected_output)
