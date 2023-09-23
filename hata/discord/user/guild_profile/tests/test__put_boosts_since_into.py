from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_boosts_since_into


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield None, False, {}
    yield None, True, {'premium_since': None}
    yield until, False, {'premium_since': datetime_to_timestamp(until)}
    yield until, True, {'premium_since': datetime_to_timestamp(until)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_boosts_since_into(input_value, defaults):
    """
    Tests whether ``put_boosts_since_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_boosts_since_into(input_value, {}, defaults)
