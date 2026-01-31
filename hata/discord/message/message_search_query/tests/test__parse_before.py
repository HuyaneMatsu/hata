from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START, datetime_to_id

from ..fields import parse_before


def _iter_options():
    before = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'max_id': None,
        },
        None,
    )
    
    yield (
        {
            'max_id': 0,
        },
        DISCORD_EPOCH_START,
    )
    
    yield (
        {
            'max_id': datetime_to_id(before),
        },
        before,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_before(input_data):
    """
    Tests whether ``parse_before`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the before from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_before(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
