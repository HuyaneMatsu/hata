from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import put_timestamp


def _iter_options():
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    yield timestamp, False, {'event_exception_id': datetime_to_id(timestamp)}
    yield timestamp, True, {'event_exception_id': datetime_to_id(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_timestamp(input_value, defaults):
    """
    Tests whether ``put_timestamp`` works as intended.
    
    Parameters
    ----------
    input_value : `DateTime`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_timestamp(input_value, {}, defaults)
