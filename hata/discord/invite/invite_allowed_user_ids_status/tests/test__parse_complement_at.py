from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_completed_at


def _iter_options():
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'completed_at': None,
        },
        None,
    )
    
    yield (
        {
            'completed_at': datetime_to_timestamp(completed_at),
        },
        completed_at,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_completed_at(input_data):
    """
    Tests whether ``parse_completed_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_completed_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
