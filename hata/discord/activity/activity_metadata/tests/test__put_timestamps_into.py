from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import put_timestamps_into


def _iter_options():
    timestamps = ActivityTimestamps(start = DateTime(2017, 5, 13, tzinfo = TimeZone.utc))
    
    yield None, False, {}
    yield None, True, {'timestamps': None}
    yield timestamps, False, {'timestamps': timestamps.to_data()}
    yield timestamps, True, {'timestamps': timestamps.to_data(defaults = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_timestamps_into(input_value, defaults):
    """
    Tests whether ``put_timestamps_into`` is working as intended.
    Parameters
    ----------
    input_value : `None | ActivityTimestamps`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_timestamps_into(input_value, {}, defaults)
