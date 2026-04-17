from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_labelled_until


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {'label_until': None}
    yield None, True, {'label_until': None}
    yield timestamp, False, {'label_until': datetime_to_timestamp(timestamp)}
    yield timestamp, True, {'label_until': datetime_to_timestamp(timestamp)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_labelled_until(input_value, defaults):
    """
    Tests whether ``put_labelled_until`` works as intended.
    
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
    return put_labelled_until(input_value, {}, defaults)
