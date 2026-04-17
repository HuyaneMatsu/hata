from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_application_requested


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'partner_application_timestamp': None}
    yield timestamp, False, {'partner_application_timestamp': datetime_to_timestamp(timestamp)}
    yield timestamp, True, {'partner_application_timestamp': datetime_to_timestamp(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_requested(input_value, defaults):
    """
    Tests whether ``put_application_requested`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_requested(input_value, {}, defaults)
