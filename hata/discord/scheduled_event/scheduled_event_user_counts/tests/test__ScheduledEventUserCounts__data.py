from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..scheduled_event_user_counts import ScheduledEventUserCounts

from .test__ScheduledEventUserCounts__constructor import _assert_fields_set


def test__ScheduledEventUserCounts__from_data():
    """
    Tests whether ``ScheduledEventUserCounts.from_data`` works as intended.
    """
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    data = {
        'guild_scheduled_event_count': count,
        'guild_scheduled_event_exception_counts': {
            str(datetime_to_id(key)): value for key, value in occasion_counts.items()
        },
    }
    
    
    scheduled_event_user_counts = ScheduledEventUserCounts.from_data(data)
    _assert_fields_set(scheduled_event_user_counts)
    
    vampytest.assert_eq(scheduled_event_user_counts.count, count)
    vampytest.assert_eq(scheduled_event_user_counts.occasion_counts, occasion_counts)


def test__ScheduledEventUserCounts__to_data():
    """
    Tests whether ``ScheduledEventUserCounts.to_data`` works as intended.
    """
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    expected_output = {
        'guild_scheduled_event_count': count,
        'guild_scheduled_event_exception_counts': {
            str(datetime_to_id(key)): value for key, value in occasion_counts.items()
        },
    }
    
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    
    vampytest.assert_eq(
        scheduled_event_user_counts.to_data(defaults = True),
        expected_output,
    )
