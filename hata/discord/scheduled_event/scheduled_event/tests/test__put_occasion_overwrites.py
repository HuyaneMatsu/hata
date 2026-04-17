from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import put_occasion_overwrites


def _iter_options():
    occasion_overwrite_0 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_1 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 15, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506210031
    
    yield (
        None,
        False,
        scheduled_event_id,
        {},
    )
    
    yield (
        None,
        True,
        scheduled_event_id,
        {
            'guild_scheduled_event_exceptions': [],
        },
    )
    
    yield (
        (occasion_overwrite_0, occasion_overwrite_1),
        False,
        scheduled_event_id,
        {
            'guild_scheduled_event_exceptions': [
                {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_0.to_data(defaults = False, include_internals = True),
                }, {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_1.to_data(defaults = False, include_internals = True),
                },
            ],
        },
    )
    
    yield (
        (occasion_overwrite_0, occasion_overwrite_1),
        True,
        scheduled_event_id,
        {
            'guild_scheduled_event_exceptions': [
                {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_0.to_data(defaults = True, include_internals = True),
                }, {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_1.to_data(defaults = True, include_internals = True),
                },
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_occasion_overwrites(input_value, defaults, scheduled_event_id):
    """
    Tests whether ``put_occasion_overwrites`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<ScheduledEventOccasionOverwrite>``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    scheduled_event_id : `int`
        The parent scheduled event's identifier. 
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_occasion_overwrites(input_value, {}, defaults, scheduled_event_id = scheduled_event_id)
