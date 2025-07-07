from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp, datetime_to_id

from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from .test__ScheduledEventOccasionOverwrite__constructor import _assert_fields_set


def test__ScheduledEventOccasionOverwrite__from_data():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.from_data`` works as intended.
    
    Case: all fields given.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    data = {
        'is_canceled': cancelled,
        'scheduled_end_time': datetime_to_timestamp(end),
        'scheduled_start_time': datetime_to_timestamp(start),
        'event_exception_id': datetime_to_id(timestamp),
    }
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite.from_data(data)
    _assert_fields_set(scheduled_event_occasion_overwrite)
    
    vampytest.assert_eq(scheduled_event_occasion_overwrite.cancelled, cancelled)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.end, end)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.start, start)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.timestamp, timestamp)


def test__ScheduledEventOccasionOverwrite__to_data():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.to_data`` works as intended.
    
    Case: Include defaults.
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
    
    expected_output = {
        'is_canceled': cancelled,
        'scheduled_end_time': datetime_to_timestamp(end),
        'scheduled_start_time': datetime_to_timestamp(start),
        'event_exception_id': datetime_to_id(timestamp),
    }
    
    vampytest.assert_eq(
        scheduled_event_occasion_overwrite.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ScheduledEventOccasionOverwrite__update_attributes():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.update_attributes`` works as intended.
    
    Case: Include defaults.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    data = {
        'is_canceled': cancelled,
        'scheduled_end_time': datetime_to_timestamp(end),
        'scheduled_start_time': datetime_to_timestamp(start),
        'event_exception_id': datetime_to_id(timestamp),
    }
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = timestamp,
    )
    
    scheduled_event_occasion_overwrite._update_attributes(data)
    
    vampytest.assert_eq(scheduled_event_occasion_overwrite.cancelled, cancelled)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.end, end)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.start, start)


def test__ScheduledEventOccasionOverwrite__difference_update_attributes():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.update_attributes`` works as intended.
    
    Case: Include defaults.
    """
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    old_cancelled = True
    old_end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    old_start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    
    new_cancelled = False
    new_end = DateTime(2016, 5, 15, 20, 0, 0, tzinfo = TimeZone.utc)
    new_start = DateTime(2016, 5, 15, 10, 0, 0, tzinfo = TimeZone.utc)
    
    data = {
        'is_canceled': new_cancelled,
        'scheduled_end_time': datetime_to_timestamp(new_end),
        'scheduled_start_time': datetime_to_timestamp(new_start),
        'event_exception_id': datetime_to_id(timestamp),
    }
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = old_cancelled,
        end = old_end,
        start = old_start,
        timestamp = timestamp,
    )
    
    output = scheduled_event_occasion_overwrite._difference_update_attributes(data)
    
    vampytest.assert_eq(
        output,
        {
            'end': old_end,
            'start': old_start,
            'cancelled': old_cancelled,
        },
    )
    
    vampytest.assert_eq(scheduled_event_occasion_overwrite.cancelled, new_cancelled)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.end, new_end)
    vampytest.assert_eq(scheduled_event_occasion_overwrite.start, new_start)
