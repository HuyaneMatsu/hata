from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_user_counts import ScheduledEventUserCounts


def _assert_fields_set(scheduled_event_user_counts):
    """
    Asserts whether all fields are of the given instance.
    
    Parameters
    ----------
    scheduled_event_user_counts : ``ScheduledEventUserCounts``
        The instance to check.
    """
    vampytest.assert_instance(scheduled_event_user_counts, ScheduledEventUserCounts)
    vampytest.assert_instance(scheduled_event_user_counts.count, int)
    vampytest.assert_instance(scheduled_event_user_counts.occasion_counts, dict, nullable = True)


def test__ScheduledEventUserCounts__new__no_fields():
    """
    Tests whether ``ScheduledEventUserCounts.__new__`` works as intended.
    
    Case: no fields given.
    """
    scheduled_event_user_counts = ScheduledEventUserCounts()
    _assert_fields_set(scheduled_event_user_counts)


def test__ScheduledEventUserCounts__new__all_fields():
    """
    Tests whether ``ScheduledEventUserCounts.__new__`` works as intended.
    
    Case: all fields given.
    """
    count = 100
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    _assert_fields_set(scheduled_event_user_counts)
    
    vampytest.assert_eq(scheduled_event_user_counts.count, count)
    vampytest.assert_eq(scheduled_event_user_counts.occasion_counts, occasion_counts)
