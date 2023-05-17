import vampytest

from ..guild_join_request_delete_event import GuildJoinRequestDeleteEvent


def test__GuildJoinRequestDeleteEvent__repr():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__repr__`` works as intended.
    """
    guild_id = 202305160019
    user_id = 202305160020
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__GuildJoinRequestDeleteEvent__hash():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__hash__`` works as intended.
    """
    guild_id = 202305160021
    user_id = 202305160022
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def test__GuildJoinRequestDeleteEvent__eq():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__repr__`` works as intended.
    """
    guild_id = 202305160023
    user_id = 202305160024
    
    keyword_parameters = {
        'guild_id': guild_id,
        'user_id': user_id,
    }
    
    event = GuildJoinRequestDeleteEvent(**keyword_parameters)
    
    vampytest.assert_eq(event, event)
    vampytest.assert_ne(event, object())
    
    for event_name, event_value in (
        ('guild_id', 0),
        ('user_id', 0),
    ):
        event_altered = GuildJoinRequestDeleteEvent(**{**keyword_parameters, event_name: event_value})
        vampytest.assert_ne(event, event_altered)


def test__GuildJoinRequestDeleteEvent__unpack():
    """
    Tests whether ``GuildJoinRequestDeleteEvent`` unpacking works as intended.
    """
    guild_id = 202305160025
    user_id = 202305160026
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
