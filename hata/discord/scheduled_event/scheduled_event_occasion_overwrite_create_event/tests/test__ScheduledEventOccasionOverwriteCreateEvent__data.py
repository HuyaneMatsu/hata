from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event_occasion_overwrite_create_event import ScheduledEventOccasionOverwriteCreateEvent

from .test__ScheduledEventOccasionOverwriteCreateEvent__constructor import _assert_fields_set


def test__ScheduledEventOccasionOverwriteCreateEvent__from_data():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202506220012
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220013
    
    data = {
        'guild_id': str(guild_id),
        **occasion_overwrite.to_data(defaults = True, include_internals = True),
        'event_id': str(scheduled_event_id),
    }
    
    event = ScheduledEventOccasionOverwriteCreateEvent.from_data(data)
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.occasion_overwrite, occasion_overwrite)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)


def test__ScheduledEventOccasionOverwriteCreateEvent__to_data():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202506220014
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220015
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        **occasion_overwrite.to_data(defaults = True, include_internals = True),
        'event_id': str(scheduled_event_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
