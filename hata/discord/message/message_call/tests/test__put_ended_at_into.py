from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_ended_at_into


def test__put_ended_at_into():
    """
    Tests whether ``put_ended_at_into`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'ended_timestamp': None}),
        (ended_at, False, {'ended_timestamp': datetime_to_timestamp(ended_at)}),
    ):
        output = put_ended_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
