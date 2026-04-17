from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....guild import Guild

from ...scheduled_event import ScheduledEvent
from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event_occasion_overwrite_create_event import ScheduledEventOccasionOverwriteCreateEvent

from .test__ScheduledEventOccasionOverwriteCreateEvent__constructor import _assert_fields_set


def test__ScheduledEventOccasionOverwriteCreateEvent__copy():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.copy`` works as intended.
    """
    guild_id = 202506220025
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220026
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)


def test__ScheduledEventOccasionOverwriteCreateEvent__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202506220027
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220028
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)


def test__ScheduledEventOccasionOverwriteCreateEvent__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202506220029
    old_occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    old_scheduled_event_id = 202506220030
    
    new_guild_id = 202506220031
    new_occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 16, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    new_scheduled_event_id = 202506220032
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = old_guild_id,
        occasion_overwrite = old_occasion_overwrite,
        scheduled_event_id = old_scheduled_event_id,
    )
    copy = event.copy_with(
        guild_id = new_guild_id,
        occasion_overwrite = new_occasion_overwrite,
        scheduled_event_id = new_scheduled_event_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.occasion_overwrite, new_occasion_overwrite)
    vampytest.assert_eq(copy.scheduled_event_id, new_scheduled_event_id)


def _iter_options__guild():
    guild_id_0 = 202506220033
    guild_id_1 = 202506220034
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)
    

@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__ScheduledEventOccasionOverwriteCreateEvent__guild(guild_id):
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create event with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
    )
    
    output = event.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__scheduled_event():
    scheduled_event_id_0 = 202506220035
    scheduled_event_id_1 = 202506220036
    
    yield 0, None
    yield scheduled_event_id_0, None
    yield scheduled_event_id_1, ScheduledEvent.precreate(scheduled_event_id_1)
    

@vampytest._(vampytest.call_from(_iter_options__scheduled_event()).returning_last())
def test__ScheduledEventOccasionOverwriteCreateEvent__scheduled_event(scheduled_event_id):
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.scheduled_event`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier to create event with.
    
    Returns
    -------
    scheduled_event : ``None | ScheduledEvent``
    """
    event = ScheduledEventOccasionOverwriteCreateEvent(
        scheduled_event_id = scheduled_event_id,
    )
    
    output = event.scheduled_event
    vampytest.assert_instance(output, ScheduledEvent, nullable = True)
    return output
