from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import put_occasion_overwrite


def _iter_options():
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    yield (
        occasion_overwrite,
        False,
        occasion_overwrite.to_data(defaults = False, include_internals = True),
    )
    
    yield (
        occasion_overwrite,
        True,
        occasion_overwrite.to_data(defaults = True, include_internals = True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_occasion_overwrite(input_value, defaults):
    """
    Tests whether ``put_occasion_overwrite`` works as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventOccasionOverwrite``
        Occasion overwrite to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_occasion_overwrite(input_value, {}, defaults)
