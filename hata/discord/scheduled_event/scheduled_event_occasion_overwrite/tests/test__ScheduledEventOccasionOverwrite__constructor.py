from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite


def _assert_fields_set(scheduled_event_occasion_overwrite):
    """
    Checks whether every attribute is set of the given scheduled event occasion overwrite.
    
    Parameters
    ----------
    scheduled_event_occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        The instance to check.
    """
    vampytest.assert_instance(scheduled_event_occasion_overwrite, ScheduledEventOccasionOverwrite)
    vampytest.assert_instance(scheduled_event_occasion_overwrite.cancelled, bool)
    vampytest.assert_instance(scheduled_event_occasion_overwrite.end, DateTime, nullable = True)
    vampytest.assert_instance(scheduled_event_occasion_overwrite.start, DateTime, nullable = True)
    vampytest.assert_instance(scheduled_event_occasion_overwrite.timestamp, DateTime)


def test__ScheduledEventOccasionOverwrite__new__no_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.__new__`` works as intended.
    
    Case: No fields given.
    """
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite()
    _assert_fields_set(scheduled_event_occasion_overwrite)


def test__ScheduledEventOccasionOverwrite__new__all_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.__new__`` works as intended.
    
    Case: Fields given.
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
    _assert_fields_set(scheduled_event_occasion_overwrite)
    
    vampytest.assert_eq(scheduled_event_occasion_overwrite.cancelled, cancelled)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.end, end)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.start, start)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.timestamp, timestamp)


def test__ScheduledEventOccasionOverwrite__from_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.from_fields`` works as intended.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite.from_fields(
        timestamp,
        cancelled,
        start,
        end,
    )
    _assert_fields_set(scheduled_event_occasion_overwrite)
    
    vampytest.assert_eq(scheduled_event_occasion_overwrite.cancelled, cancelled)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.end, end)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.start, start)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.timestamp, timestamp)


def test__ScheduledEventOccasionOverwrite__create_empty():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.create_empty`` works as intended.
    """
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite.create_empty()
    _assert_fields_set(scheduled_event_occasion_overwrite)

