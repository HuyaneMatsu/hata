from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_last_seen_at


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'last_seen': None}, None
    yield {'last_seen': datetime_to_timestamp(timestamp)}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_last_seen_at(input_data):
    """
    Tests whether ``parse_last_seen_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_last_seen_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
