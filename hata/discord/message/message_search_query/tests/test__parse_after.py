from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import parse_after


def _iter_options():
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'min_id': None,
        },
        None,
    )
    
    yield (
        {
            'min_id': 0,
        },
        None,
    )
    
    yield (
        {
            'min_id': datetime_to_id(after),
        },
        after,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_after(input_data):
    """
    Tests whether ``parse_after`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the after from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_after(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
