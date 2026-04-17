from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import parse_occasion_counts


def _iter_options():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exception_counts': None,
        },
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exception_counts': {},
        },
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exception_counts': {
                str(datetime_to_id(date_time)): 5,
            },
        },
        {
            date_time : 5,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_occasion_counts(input_data):
    """
    Tests whether ``parse_occasion_counts`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<Datetime, int>`
    """
    output = parse_occasion_counts(input_data)
    vampytest.assert_instance(output, dict, nullable = True)
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, DateTime)
            vampytest.assert_instance(value, int)
    
    return output
