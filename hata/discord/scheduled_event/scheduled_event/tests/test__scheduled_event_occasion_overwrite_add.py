from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event import ScheduledEvent
from ..utils import scheduled_event_occasion_overwrite_add


def _iter_options():
    occasion_overwrite_0 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 10, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_1 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 15, 13, 20, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_2 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 16, 13, 30, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_3 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 17, 13, 40, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_4 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 18, 13, 50, 0, tzinfo = TimeZone.utc),
    )
    
    yield (
        202506270007,
        [],
        occasion_overwrite_0,
        (
            None,
            (
                occasion_overwrite_0,
            ),
        ),
    )
    
    yield (
        202506270008,
        [
            occasion_overwrite_1,
            occasion_overwrite_2,
        ],
        occasion_overwrite_0,
        (
            None,
            (
                occasion_overwrite_0,
                occasion_overwrite_1,
                occasion_overwrite_2,
            ),
        ),
    )
    
    yield (
        202506270009,
        [
            occasion_overwrite_2,
            occasion_overwrite_3,
        ],
        occasion_overwrite_4,
        (
            None,
            (
                occasion_overwrite_2,
                occasion_overwrite_3,
                occasion_overwrite_4,
            ),
        ),
    )
    
    yield (
        202506270010,
        [
            occasion_overwrite_0,
            occasion_overwrite_1,
            occasion_overwrite_3,
            occasion_overwrite_4,
        ],
        occasion_overwrite_2,
        (
            None,
            (
                occasion_overwrite_0,
                occasion_overwrite_1,
                occasion_overwrite_2,
                occasion_overwrite_3,
                occasion_overwrite_4,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__scheduled_event_occasion_overwrite_add(scheduled_event_id, occasion_overwrites, occasion_overwrite):
    """
    Tests whether ``scheduled_event_occasion_overwrite_add`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        The scheduled event identifier to create instance with.
    
    occasion_overwrites : ``list<ScheduledEventOccasionOverwrite>``
        occasion_overwrites to create scheduled event with.
    
    occasion_overwrite : ˙`ScheduledEventOccasionOverwrite`˙
        Cancellation to add.
    
    Returns
    -------
    output_and_occasion_overwrites : ``(None, None | tuple<ScheduledEventOccasionOverwrite>)``
    """
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        occasion_overwrites = occasion_overwrites,
    )
    output = scheduled_event_occasion_overwrite_add(scheduled_event, occasion_overwrite)
    
    vampytest.assert_instance(output, type(None))
    vampytest.assert_is(output, None)
    
    occasion_overwrites = scheduled_event.occasion_overwrites
    vampytest.assert_instance(occasion_overwrites, tuple, nullable = True)
    if (occasion_overwrites is not None):
        for element in occasion_overwrites:
            vampytest.assert_instance(element, ScheduledEventOccasionOverwrite)
    
    return (output, occasion_overwrites)
