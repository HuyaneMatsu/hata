from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_created_at_into


def test__put_created_at_into():
    """
    Tests whether ``put_created_at_into`` works as intended.
    """
    created_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'created_at': None}),
        (created_at, False, {'created_at': datetime_to_timestamp(created_at)}),
    ):
        output = put_created_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
