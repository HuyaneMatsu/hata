from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_requested_to_speak_at


def test__parse_requested_to_speak_at():
    """
    Tests whether ``parse_requested_to_speak_at`` works as intended.
    """
    requested_to_speak_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'request_to_speak_timestamp': None}, None),
        ({'request_to_speak_timestamp': datetime_to_timestamp(requested_to_speak_at)}, requested_to_speak_at),
    ):
        output = parse_requested_to_speak_at(input_value)
        vampytest.assert_eq(output, expected_output)
