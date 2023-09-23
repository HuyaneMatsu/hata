from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_direct_messages_disabled_until_into


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield None, False, {}
    yield None, True, {'dms_disabled_until': None}
    yield until, False, {'dms_disabled_until': datetime_to_timestamp(until)}
    yield until, True, {'dms_disabled_until': datetime_to_timestamp(until)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_direct_messages_disabled_until_into(input_value, defaults):
    """
    Tests whether ``put_direct_messages_disabled_until_into`` works as intended.
    
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
    return put_direct_messages_disabled_until_into(input_value, {}, defaults)
