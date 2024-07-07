from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_starts_at_into


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'starts_at': None}
    yield timestamp, False, {'starts_at': datetime_to_timestamp(timestamp)}
    yield timestamp, True, {'starts_at': datetime_to_timestamp(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_starts_at_into(input_value, defaults):
    """
    Tests whether ``put_starts_at_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_starts_at_into(input_value, {}, defaults)
