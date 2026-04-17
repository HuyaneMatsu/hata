from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_archived_at


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, False, {}
    yield None, True, {'thread_metadata': {'archive_timestamp': None}}
    yield timestamp, False, {'thread_metadata': {'archive_timestamp': datetime_to_timestamp(timestamp)}}
    yield timestamp, True, {'thread_metadata': {'archive_timestamp': datetime_to_timestamp(timestamp)}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_archived_at(input_value, defaults):
    """
    Tests whether ``put_archived_at`` works as intended.
    
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
    return put_archived_at(input_value, {}, defaults)
