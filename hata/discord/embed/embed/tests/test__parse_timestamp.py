from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_timestamp


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'timestamp': None}, None
    yield {'timestamp': datetime_to_timestamp(timestamp)}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_timestamp(input_data):
    """
    Tests whether ``parse_timestamp`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_timestamp(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
