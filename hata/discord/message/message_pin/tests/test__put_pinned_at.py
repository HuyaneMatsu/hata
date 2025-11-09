from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START, datetime_to_timestamp

from ..fields import put_pinned_at


def _iter_options():
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        DISCORD_EPOCH_START,
        False,
        {
            'pinned_at': datetime_to_timestamp(DISCORD_EPOCH_START),
        },
    )
    
    yield (
        DISCORD_EPOCH_START,
        True,
        {
            'pinned_at': datetime_to_timestamp(DISCORD_EPOCH_START),
        },
    )
    
    yield (
        pinned_at,
        False,
        {
            'pinned_at': datetime_to_timestamp(pinned_at),
        },
    )
    
    yield (
        pinned_at,
        True,
        {
            'pinned_at': datetime_to_timestamp(pinned_at),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_pinned_at(input_value, defaults):
    """
    Tests whether ``put_pinned_at`` works as intended.
    
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
    return put_pinned_at(input_value, {}, defaults)
