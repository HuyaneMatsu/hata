from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event import ScheduledEvent
from ..utils import scheduled_event_occasion_overwrite_remove


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
        202506270012,
        [],
        occasion_overwrite_0.timestamp,
        (
            None,
            None,
        ),
    )
    
    yield (
        202506270013,
        [
            occasion_overwrite_1,
            occasion_overwrite_2,
        ],
        occasion_overwrite_0.timestamp,
        (
            None,
            (
                occasion_overwrite_1,
                occasion_overwrite_2,
            ),
        ),
    )
    
    yield (
        202506270014,
        [
            occasion_overwrite_2,
            occasion_overwrite_3,
        ],
        occasion_overwrite_4.timestamp,
        (
            None,
            (
                occasion_overwrite_2,
                occasion_overwrite_3,
            ),
        ),
    )
    
    yield (
        202506270015,
        [
            occasion_overwrite_0,
            occasion_overwrite_1,
            occasion_overwrite_3,
            occasion_overwrite_4,
        ],
        occasion_overwrite_2.timestamp,
        (
            None,
            (
                occasion_overwrite_0,
                occasion_overwrite_1,
                occasion_overwrite_3,
                occasion_overwrite_4,
            ),
        ),
    )
    
    yield (
        202506270016,
        [
            occasion_overwrite_0,
            occasion_overwrite_1,
        ],
        occasion_overwrite_0.timestamp,
        (
            occasion_overwrite_0,
            (
                occasion_overwrite_1,
            ),
        ),
    )
    
    yield (
        202506270017,
        [
            occasion_overwrite_0,
            occasion_overwrite_1,
        ],
        occasion_overwrite_1.timestamp,
        (
            occasion_overwrite_1,
            (
                occasion_overwrite_0,
            ),
        ),
    )
    
    yield (
        202506270018,
        [
            occasion_overwrite_0,
        ],
        occasion_overwrite_0.timestamp,
        (
            occasion_overwrite_0,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__scheduled_event_occasion_overwrite_remove(scheduled_event_id, occasion_overwrites, occasion_overwrite):
    """
    Tests whether ``scheduled_event_occasion_overwrite_remove`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        The scheduled event identifier to create instance with.
    
    occasion_overwrites : ``list<ScheduledEventOccasionOverwrite>``
        occasion_overwrites to create scheduled event with.
    
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        Cancellation to remove.
    
    Returns
    -------
    output : ``(None | ScheduledEventOccasionOverwrite, None | tuple<ScheduledEventOccasionOverwrite>)``
    """
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        occasion_overwrites = occasion_overwrites,
    )
    output = scheduled_event_occasion_overwrite_remove(scheduled_event, occasion_overwrite)
    vampytest.assert_instance(output, ScheduledEventOccasionOverwrite, nullable = True)
    
    occasion_overwrites = scheduled_event.occasion_overwrites
    vampytest.assert_instance(occasion_overwrites, tuple, nullable = True)
    if (occasion_overwrites is not None):
        for element in occasion_overwrites:
            vampytest.assert_instance(element, ScheduledEventOccasionOverwrite)
    
    return (output, occasion_overwrites)
