from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_current_period_start


def _iter_options():
    current_period_start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'current_period_start': None}
    yield current_period_start, False, {'current_period_start': datetime_to_timestamp(current_period_start)}
    yield current_period_start, True, {'current_period_start': datetime_to_timestamp(current_period_start)}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_current_period_start(input_value, defaults):
    """
    Tests whether ``put_current_period_start`` works as intended.
    
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
    return put_current_period_start(input_value, {}, defaults)
