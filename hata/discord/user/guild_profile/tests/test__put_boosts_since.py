from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_boosts_since


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'premium_since': None}
    yield timestamp, False, {'premium_since': datetime_to_timestamp(timestamp)}
    yield timestamp, True, {'premium_since': datetime_to_timestamp(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_boosts_since(input_value, defaults):
    """
    Tests whether ``put_boosts_since`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_boosts_since(input_value, {}, defaults)
