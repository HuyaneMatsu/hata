from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_end_into


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'scheduled_end_time': None}
    yield timestamp, False, {'scheduled_end_time': datetime_to_timestamp(timestamp)}
    yield timestamp, True, {'scheduled_end_time': datetime_to_timestamp(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_end_into(input_value, defaults):
    """
    Tests whether ``put_end_into`` works as intended.
    
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
    return put_end_into(input_value, {}, defaults)
