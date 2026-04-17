from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_clip_created_at


def _iter_options():
    clip_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield {}, None
    yield {'clip_created_at': None}, None
    yield {'clip_created_at': datetime_to_timestamp(clip_created_at)}, clip_created_at


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_clip_created_at(input_data):
    """
    Tests whether ``parse_clip_created_at`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_clip_created_at(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
