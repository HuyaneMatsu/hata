from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_end_into


def test__put_end_into():
    """
    Tests whether ``put_end_into`` works as intended.
    """
    end = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'scheduled_end_time': None}),
        (end, False, {'scheduled_end_time': datetime_to_timestamp(end)}),
    ):
        output = put_end_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
