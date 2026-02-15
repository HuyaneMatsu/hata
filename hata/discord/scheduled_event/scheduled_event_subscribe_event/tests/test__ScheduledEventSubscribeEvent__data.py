from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..scheduled_event_subscribe_event import ScheduledEventSubscribeEvent

from .test__ScheduledEventSubscribeEvent__constructor import _assert_fields_set


def test__ScheduledEventSubscribeEvent__from_data():
    """
    Tests whether ``ScheduledEventSubscribeEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202303120003
    scheduled_event_id = 202303120004
    timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    user_id = 202303120005
    
    data = {
        'guild_id': str(guild_id),
        'guild_scheduled_event_id': str(scheduled_event_id),
        'guild_scheduled_event_exception_id': str(datetime_to_id(timestamp)),
        'user_id': str(user_id),
    }
    
    event = ScheduledEventSubscribeEvent.from_data(data)
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(event.timestamp, timestamp)
    vampytest.assert_eq(event.user_id, user_id)


def test__ScheduledEventSubscribeEvent__to_data():
    """
    Tests whether ``ScheduledEventSubscribeEvent.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202303120006
    scheduled_event_id = 202303120007
    timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    user_id = 202303120008
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user_id = user_id,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        'guild_scheduled_event_id': str(scheduled_event_id),
        'guild_scheduled_event_exception_id': str(datetime_to_id(timestamp)),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
