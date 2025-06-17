from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_unix_time

from ..fields import put_expires_at


def _iter_options():
    until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'expires_at': None}
    yield until, False, {'expires_at': datetime_to_unix_time(until)}
    yield until, True, {'expires_at': datetime_to_unix_time(until)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_expires_at(input_value, defaults):
    """
    Tests whether ``put_expires_at`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Datetime`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_expires_at(input_value, {}, defaults)
