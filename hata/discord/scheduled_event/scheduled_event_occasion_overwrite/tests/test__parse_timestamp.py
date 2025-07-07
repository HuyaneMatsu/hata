from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START, datetime_to_id

from ..fields import parse_timestamp


def _iter_options():
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    yield {}, DISCORD_EPOCH_START
    yield {'event_exception_id': None}, DISCORD_EPOCH_START
    yield {'event_exception_id': str(datetime_to_id(timestamp))}, timestamp


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_timestamp(input_data):
    """
    Tests whether ``parse_timestamp`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `DateTime`
    """
    output = parse_timestamp(input_data)
    vampytest.assert_instance(output, DateTime)
    return output
