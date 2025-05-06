from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_cancelled_at


def _iter_options():
    cancelled_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'cancelled_at': None}
    yield cancelled_at, False, {'cancelled_at': datetime_to_timestamp(cancelled_at)}
    yield cancelled_at, True, {'cancelled_at': datetime_to_timestamp(cancelled_at)}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_cancelled_at(input_value, defaults):
    """
    Tests whether ``put_cancelled_at`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        The input value to serialize.
    defaults : `bool`
        Whether values with their default value should be included in the output data.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_cancelled_at(input_value, {}, defaults)
