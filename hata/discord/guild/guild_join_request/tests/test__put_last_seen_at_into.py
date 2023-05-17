from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_last_seen_at_into


def test__put_last_seen_at_into():
    """
    Tests whether ``put_last_seen_at_into`` works as intended.
    """
    last_seen_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'last_seen': None}),
        (last_seen_at, False, {'last_seen': datetime_to_timestamp(last_seen_at)}),
    ):
        output = put_last_seen_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
