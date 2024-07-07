from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ..fields import put_start_into


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'start': None}
    yield timestamp, False, {'start': datetime_to_millisecond_unix_time(timestamp)}
    yield timestamp, True, {'start': datetime_to_millisecond_unix_time(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_start_into(input_value, defaults):
    """
    Tests whether ``put_start_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_start_into(input_value, {}, defaults)
