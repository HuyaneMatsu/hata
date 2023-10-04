from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_starts_at


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield {}, None
    yield {'starts_at': None}, None
    yield {'starts_at': datetime_to_timestamp(until)}, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_starts_at(input_data):
    """
    Tests whether ``parse_starts_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `DateTime`
    """
    return parse_starts_at(input_data)
