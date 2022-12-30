from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..fields import put_start_into


def test__put_start_into():
    """
    Tests whether ``put_start_into`` works as intended.
    """
    date = DateTime(2016, 1, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'start': None}),
        (date, False, {'start': datetime_to_millisecond_unix_time(date)})
    ):
        output = put_start_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
