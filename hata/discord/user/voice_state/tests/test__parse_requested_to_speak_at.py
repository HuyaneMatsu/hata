from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_requested_to_speak_at


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'request_to_speak_timestamp': None}, None
    yield {'request_to_speak_timestamp': datetime_to_timestamp(timestamp)}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_requested_to_speak_at(input_data):
    """
    Tests whether ``parse_requested_to_speak_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_requested_to_speak_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
