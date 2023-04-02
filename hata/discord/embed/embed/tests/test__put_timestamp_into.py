from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_timestamp_into


def test__put_timestamp_into():
    """
    Tests whether ``put_timestamp_into`` is working as intended.
    """
    timestamp = DateTime(2016, 9, 9)
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'timestamp': None}),
        (timestamp, False, {'timestamp': datetime_to_timestamp(timestamp)}),
    ):
        data = put_timestamp_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
