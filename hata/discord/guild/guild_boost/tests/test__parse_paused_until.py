from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_paused_until


def _iter_options():
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'pause_ends_at': None,
        },
        None,
    )
    
    yield (
        {
            'pause_ends_at': datetime_to_timestamp(paused_until),
        },
        paused_until,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_paused_until(input_data):
    """
    Tests whether ``parse_paused_until`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_paused_until(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
