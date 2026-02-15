from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import GuildProfile, User
from ....utils import datetime_to_id

from ..scheduled_event_user_entry import ScheduledEventUserEntry

from .test__ScheduledEventUserEntry__constructor import _assert_fields_set


def test__ScheduledEventUserEntry__from_data():
    """
    Tests whether ``ScheduledEventUserEntry.from_data`` works as intended.
    """
    guild_id = 202602100030
    guild_profile = GuildProfile(nick = 'Moriya')
    
    scheduled_event_id = 202602100031
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100032,
        name = 'Suwako',
    )
    
    data = {
        'guild_scheduled_event_id': str(scheduled_event_id),
        'guild_scheduled_event_exception_id': str(datetime_to_id(timestamp)),
        'user': {
            **user.to_data(include_internals = True),
            'member': guild_profile.to_data(include_internals = True),
        },
    }
    
    
    scheduled_event_user_entry = ScheduledEventUserEntry.from_data(data, guild_id)
    _assert_fields_set(scheduled_event_user_entry)
    
    vampytest.assert_eq(scheduled_event_user_entry.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(scheduled_event_user_entry.timestamp, timestamp)
    vampytest.assert_is(scheduled_event_user_entry.user, user)
    vampytest.assert_eq(scheduled_event_user_entry.user.guild_profiles, {guild_id : guild_profile})


def test__ScheduledEventUserEntry__to_data():
    """
    Tests whether ``ScheduledEventUserEntry.to_data`` works as intended.
    """
    guild_id = 202602100033
    guild_profile = GuildProfile(nick = 'Moriya')
    
    scheduled_event_id = 202602100034
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100035,
        name = 'Suwako',
    )
    user.guild_profiles[guild_id] = guild_profile
    
    
    expected_output = {
        'guild_scheduled_event_id': str(scheduled_event_id),
        'guild_scheduled_event_exception_id': str(datetime_to_id(timestamp)),
        'user': {
            **user.to_data(defaults = True, include_internals = True),
            'member': guild_profile.to_data(defaults = True, include_internals = True),
        },
    }
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    
    vampytest.assert_eq(
        scheduled_event_user_entry.to_data(defaults = True, guild_id = guild_id),
        expected_output,
    )
