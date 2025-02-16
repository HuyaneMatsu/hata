from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_edited_at


def _iter_options():
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'message': {'edited_timestamp': None}}
    yield edited_at, False, {'message': {'edited_timestamp': datetime_to_timestamp(edited_at)}}
    yield edited_at, True, {'message': {'edited_timestamp': datetime_to_timestamp(edited_at)}}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_edited_at(input_value, defaults):
    """
    Tests whether ``put_edited_at`` works as intended.
    
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
    return put_edited_at(input_value, {}, defaults)
