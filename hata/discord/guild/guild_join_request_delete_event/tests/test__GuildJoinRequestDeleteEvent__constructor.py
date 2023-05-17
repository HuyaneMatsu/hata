import vampytest

from ..guild_join_request_delete_event import GuildJoinRequestDeleteEvent


def _assert_fields_set(event):
    """
    Checks whether every attribute is set of the given guild join request delete event.
    
    Parameters
    ----------
    event : ``GuildJoinRequestDeleteEvent``
        The event to check.
    """
    vampytest.assert_instance(event, GuildJoinRequestDeleteEvent)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.user_id, int)


def test__GuildJoinRequestDeleteEvent__new__0():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = GuildJoinRequestDeleteEvent()
    _assert_fields_set(event)


def test__GuildJoinRequestDeleteEvent__new__1():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202305160013
    user_id = 202305160014
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.user_id, user_id)
