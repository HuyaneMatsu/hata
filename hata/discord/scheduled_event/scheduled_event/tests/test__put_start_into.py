from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_start_into


def test__put_start_into():
    """
    Tests whether ``put_start_into`` works as intended.
    """
    start = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'scheduled_start_time': None}),
        (start, False, {'scheduled_start_time': datetime_to_timestamp(start)}),
    ):
        output = put_start_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
