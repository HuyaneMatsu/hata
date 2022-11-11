from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_timed_out_until_into


def test__put_timed_out_until_into():
    """
    Tests whether ``put_timed_out_until_into`` works as intended.
    """
    timed_out_until = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'communication_disabled_until': None}),
        (timed_out_until, False, {'communication_disabled_until': datetime_to_timestamp(timed_out_until)}),
    ):
        output = put_timed_out_until_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
