from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_user_counts import ScheduledEventUserCounts

from .test__ScheduledEventUserCounts__constructor import _assert_fields_set


def test__ScheduledEventUserCounts__copy():
    """
    Tests whether ``ScheduledEventUserCounts.copy`` works as intended.
    """
    count = 202602100050
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    
    copy = scheduled_event_user_counts.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_counts)


def test__ScheduledEventUserCounts__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventUserCounts.copy_with`` works as intended.
    
    Case: no fields given.
    """
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    
    copy = scheduled_event_user_counts.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_counts)


def test__ScheduledEventUserCounts__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventUserCounts.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_count = 120
    old_occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    new_count = 100
    new_occasion_counts = {
        DateTime(2016, 5, 18, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = old_count,
        occasion_counts = old_occasion_counts,
    )
    
    copy = scheduled_event_user_counts.copy_with(
        count = new_count,
        occasion_counts = new_occasion_counts,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event_user_counts)

    vampytest.assert_eq(copy.count, new_count)
    vampytest.assert_eq(copy.occasion_counts, new_occasion_counts)
