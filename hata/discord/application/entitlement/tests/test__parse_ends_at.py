from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_ends_at


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'ends_at': None}, None
    yield {'ends_at': datetime_to_timestamp(timestamp)}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_ends_at(input_data):
    """
    Tests whether ``parse_ends_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return parse_ends_at(input_data)
