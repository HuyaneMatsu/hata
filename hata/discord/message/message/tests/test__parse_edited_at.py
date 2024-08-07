from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_edited_at


def _iter_options():
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'edited_timestamp': None}, None
    yield {'edited_timestamp': datetime_to_timestamp(edited_at)}, edited_at


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_edited_at(input_data):
    """
    Tests whether ``parse_edited_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return parse_edited_at(input_data)
