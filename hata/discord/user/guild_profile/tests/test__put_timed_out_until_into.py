from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_timed_out_until_into


def _iter_options():
    until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'communication_disabled_until': None}
    yield until, False, {'communication_disabled_until': datetime_to_timestamp(until)}
    yield until, True, {'communication_disabled_until': datetime_to_timestamp(until)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_timed_out_until_into(input_value, defaults):
    """
    Tests whether ``put_timed_out_until_into`` works as intended.
    
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
    return put_timed_out_until_into(input_value, {}, defaults)
