from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event_occasion_overwrite_create_event import ScheduledEventOccasionOverwriteCreateEvent


def _assert_fields_set(event):
    """
    Checks whether every attribute is set of the given scheduled event occasion overwrite create event.
    
    Parameters
    ----------
    event : ``ScheduledEventOccasionOverwriteCreateEvent``
        The event to check.
    """
    vampytest.assert_instance(event, ScheduledEventOccasionOverwriteCreateEvent)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.occasion_overwrite, ScheduledEventOccasionOverwrite)
    vampytest.assert_instance(event.scheduled_event_id, int)


def test__ScheduledEventOccasionOverwriteCreateEvent__new__no_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = ScheduledEventOccasionOverwriteCreateEvent()
    _assert_fields_set(event)


def test__ScheduledEventOccasionOverwriteCreateEvent__new__all_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202506220010
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220011
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.occasion_overwrite, occasion_overwrite)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)


def test__ScheduledEventOccasionOverwriteCreateEvent__from_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.from_fields`` works as intended.
    """
    guild_id = 202506250000
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506250001
    
    event = ScheduledEventOccasionOverwriteCreateEvent.from_fields(
        guild_id,
        scheduled_event_id,
        occasion_overwrite,
    )
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.occasion_overwrite, occasion_overwrite)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)
