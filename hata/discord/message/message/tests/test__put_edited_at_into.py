from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_edited_at_into


def _iter_options():
    edited_at = DateTime(2016, 5, 14)
    
    yield None, False, {}
    yield None, True, {'edited_timestamp': None}
    yield edited_at, False, {'edited_timestamp': datetime_to_timestamp(edited_at)}
    yield edited_at, True, {'edited_timestamp': datetime_to_timestamp(edited_at)}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_edited_at_into(input_value, defaults):
    """
    Tests whether ``put_edited_at_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        The input value to serialize.
    defaults : `bool`
        Whether values with their default value should be included in the output data.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_edited_at_into(input_value, {}, defaults)
