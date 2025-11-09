from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START, datetime_to_timestamp

from ..fields import parse_pinned_at


def _iter_options():
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        DISCORD_EPOCH_START,
    )
    
    yield (
        {
            'pinned_at': datetime_to_timestamp(DISCORD_EPOCH_START),
        },
        DISCORD_EPOCH_START,
    )
    
    yield (
        {
            'pinned_at': datetime_to_timestamp(pinned_at),
        },
        pinned_at,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_pinned_at(input_data):
    """
    Tests whether ``parse_pinned_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `DateTime`
    """
    output = parse_pinned_at(input_data)
    vampytest.assert_instance(output, DateTime)
    return output
