from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_created_at


def _iter_options():
    created_at = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'thread_metadata': {'create_timestamp': None}}
    yield created_at, False, {'thread_metadata': {'create_timestamp': datetime_to_timestamp(created_at)}}
    yield created_at, True, {'thread_metadata': {'create_timestamp': datetime_to_timestamp(created_at)}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_created_at(input_value, defaults):
    """
    Tests whether ``put_created_at`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        Value to serialize.
    defaults : `bool`
        Whether fields ast heir default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_created_at(input_value, {}, defaults)
