import vampytest

from ..guild_join_request_delete_event import GuildJoinRequestDeleteEvent

from .test__GuildJoinRequestDeleteEvent__constructor import _assert_fields_set


def test__GuildJoinRequestDeleteEvent__from_data():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202305160015
    user_id = 202305160016
    
    data = {
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    event = GuildJoinRequestDeleteEvent.from_data(data)
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.user_id, user_id)


def test__GuildJoinRequestDeleteEvent__to_data():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202305160017
    user_id = 202305160018
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
