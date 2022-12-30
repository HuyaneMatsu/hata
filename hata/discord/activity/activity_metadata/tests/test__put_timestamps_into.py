from datetime import datetime as DateTime

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import put_timestamps_into


def test__put_timestamps_into():
    """
    Tests whether ``put_timestamps_into`` is working as intended.
    """
    timestamps = ActivityTimestamps(start = DateTime(2017, 5, 13))
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (timestamps, False, {'timestamps': timestamps.to_data()}),
        (timestamps, True, {'timestamps': timestamps.to_data(defaults = True)}),
    ):
        data = put_timestamps_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
