from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import put_occasion_counts


def _iter_options():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        False,
        {
            'guild_scheduled_event_exception_counts': {},
        },
    )
    
    yield (
        None,
        True,
        {
            'guild_scheduled_event_exception_counts': {},
        },
    )
    
    yield (
        {
            date_time : 5,
        },
        False,
        {
            'guild_scheduled_event_exception_counts': {
                str(datetime_to_id(date_time)): 5,
            },
        },
    )
    
    yield (
        {
            date_time : 5,
        },
        True,
        {
            'guild_scheduled_event_exception_counts': {
                str(datetime_to_id(date_time)): 5,
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_occasion_counts(input_value, defaults):
    """
    Tests whether ``put_occasion_counts`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<Datetime, int>`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_occasion_counts(input_value, {}, defaults)
