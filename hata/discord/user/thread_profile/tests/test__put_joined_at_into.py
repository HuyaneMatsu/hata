from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_joined_at_into


def test__put_joined_at_into():
    """
    Tests whether ``put_joined_at_into`` works as intended.
    """
    joined_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'joined_at': None}),
        (joined_at, False, {'joined_at': datetime_to_timestamp(joined_at)}),
    ):
        output = put_joined_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
