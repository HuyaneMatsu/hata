from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_created_at


def _iter_options():
    created_at = DateTime(2016, 5, 14)
    
    yield {}, None
    yield {'created_at': None}, None
    yield {'created_at': datetime_to_timestamp(created_at)}, created_at


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_created_at(input_data):
    """
    Tests whether ``parse_created_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `None`, `DateTime`
    """
    return parse_created_at(input_data)
