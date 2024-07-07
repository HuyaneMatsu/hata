from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import parse_timestamps


def _iter_options():
    timestamps = ActivityTimestamps(start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    yield {}, None
    yield {'timestamps': None}, None
    yield {'timestamps': timestamps.to_data()}, timestamps


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_timestamps(input_data):
    """
    Tests whether ``parse_timestamps`` works as intended.
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | ActivityTimestamps`
    """
    output = parse_timestamps(input_data)
    vampytest.assert_instance(output, ActivityTimestamps, nullable = True)
    return output
