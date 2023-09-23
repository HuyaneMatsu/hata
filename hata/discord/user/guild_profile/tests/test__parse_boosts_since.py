from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_boosts_since


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield {}, None
    yield {'premium_since': None}, None
    yield {'premium_since': datetime_to_timestamp(until)}, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_boosts_since(input_data):
    """
    Tests whether ``parse_boosts_since`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `DateTime`
    """
    return parse_boosts_since(input_data)
