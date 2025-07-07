from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_paused_until


def _iter_options():
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'pause_ends_at': None,
        },
    )
    
    yield (
        paused_until,
        False,
        {
            'pause_ends_at': datetime_to_timestamp(paused_until),
        },
    )
    
    yield (
        paused_until,
        True,
        {
            'pause_ends_at': datetime_to_timestamp(paused_until),
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_paused_until(input_value, defaults):
    """
    Tests whether ``put_paused_until`` works as intended.
    
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
    return put_paused_until(input_value, {}, defaults)
