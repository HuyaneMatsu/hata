from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from .test__ScheduledEventOccasionOverwrite__constructor import _assert_fields_set


def test__ScheduledEventOccasionOverwrite__copy():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.copy`` works as intended.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = cancelled,
        end = end,
        start = start,
        timestamp = timestamp,
    )
    copy = scheduled_event_occasion_overwrite.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(scheduled_event_occasion_overwrite, copy)

    vampytest.assert_eq(scheduled_event_occasion_overwrite, copy)


def test__ScheduledEventOccasionOverwrite__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.copy_with`` works as intended.
    
    Case: no fields given.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = cancelled,
        end = end,
        start = start,
        timestamp = timestamp,
    )
    copy = scheduled_event_occasion_overwrite.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(scheduled_event_occasion_overwrite, copy)

    vampytest.assert_eq(scheduled_event_occasion_overwrite, copy)


def test__ScheduledEventOccasionOverwrite__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_cancelled = True
    old_end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    old_start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    old_timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    new_cancelled = False
    new_end = DateTime(2016, 5, 14, 20, 10, 0, tzinfo = TimeZone.utc)
    new_start = DateTime(2016, 5, 14, 10, 20, 0, tzinfo = TimeZone.utc)
    new_timestamp = DateTime(2016, 5, 16, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = old_cancelled,
        end = old_end,
        start = old_start,
        timestamp = old_timestamp,
    )
    copy = scheduled_event_occasion_overwrite.copy_with(
        cancelled = new_cancelled,
        end = new_end,
        start = new_start,
        timestamp = new_timestamp,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(scheduled_event_occasion_overwrite, copy)

    vampytest.assert_eq(copy.cancelled, new_cancelled)
    vampytest.assert_eq(copy.end, new_end)
    vampytest.assert_eq(copy.start, new_start)
    vampytest.assert_eq(copy.timestamp, new_timestamp)
