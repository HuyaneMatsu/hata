from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START, datetime_to_timestamp

from ..fields import put_created_at_into


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield DISCORD_EPOCH_START, False, {}
    yield DISCORD_EPOCH_START, True, {'message': {'timestamp': datetime_to_timestamp(DISCORD_EPOCH_START)}}
    yield created_at, False, {'message': {'timestamp': datetime_to_timestamp(created_at)}}
    yield created_at, True, {'message': {'timestamp': datetime_to_timestamp(created_at)}}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_created_at_into(input_value, defaults):
    """
    Tests whether ``put_created_at_into`` works as intended.
    
    Parameters
    ----------
    input_value : `DateTime`
        The input value to serialize.
    defaults : `bool`
        Whether values with their default value should be included in the output data.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_created_at_into(input_value, {}, defaults)
