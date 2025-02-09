from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_clip_created_at_into


def _iter_options():
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'clip_created_at': None}
    yield clip_created_at, False, {'clip_created_at': datetime_to_timestamp(clip_created_at)}
    yield clip_created_at, True, {'clip_created_at': datetime_to_timestamp(clip_created_at)}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_clip_created_at_into(input_value, defaults):
    """
    Tests whether ``put_clip_created_at_into`` works as intended.
    
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
    return put_clip_created_at_into(input_value, {}, defaults)
