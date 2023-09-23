from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_timed_out_until


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield {}, None
    yield {'communication_disabled_until': None}, None
    yield {'communication_disabled_until': datetime_to_timestamp(until)}, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_timed_out_until(input_data):
    """
    Tests whether ``parse_timed_out_until`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `DateTime`
    """
    return parse_timed_out_until(input_data)
