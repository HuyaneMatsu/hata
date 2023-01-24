from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_requested_to_speak_at_into


def test__put_requested_to_speak_at_into():
    """
    Tests whether ``put_requested_to_speak_at_into`` works as intended.
    """
    requested_to_speak_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'request_to_speak_timestamp': None}),
        (requested_to_speak_at, False, {'request_to_speak_timestamp': datetime_to_timestamp(requested_to_speak_at)}),
    ):
        output = put_requested_to_speak_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
