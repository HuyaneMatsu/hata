from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_expires_at


def _iter_options():
    until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'expiry': None}, None
    yield {'expiry': datetime_to_timestamp(until)}, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_expires_at(input_data):
    """
    Tests whether ``parse_expires_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_expires_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
