from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_archived_at


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'thread_metadata': None}, None
    yield {'thread_metadata': {}}, None
    yield {'thread_metadata': {'archive_timestamp': None}}, None
    yield {'thread_metadata': {'archive_timestamp': datetime_to_timestamp(timestamp)}}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_archived_at(input_data):
    """
    Tests whether ``parse_archived_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_archived_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
