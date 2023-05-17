import vampytest

from ....user import ClientUserBase

from ...guild import Guild

from ..guild_join_request_delete_event import GuildJoinRequestDeleteEvent

from .test__GuildJoinRequestDeleteEvent__constructor import _assert_fields_set


def test__GuildJoinRequestDeleteEvent__copy():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.copy`` works as intended.
    """
    guild_id = 202305160027
    user_id = 202305160028
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__GuildJoinRequestDeleteEvent__copy_with__0():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202305160029
    user_id = 202305160030
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__GuildJoinRequestDeleteEvent__copy_with__1():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202305160031
    old_user_id = 202305160032
    
    new_guild_id = 202305160033
    new_user_id = 202305160034
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = old_guild_id,
        user_id = old_user_id,
    )
    copy = event.copy_with(
        guild_id = new_guild_id,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.user_id, new_user_id)


def test__GuildJoinRequestDeleteEvent__guild():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.guild`` works as intended.
    
    Case: no fields given.
    """
    guild_id_0 = 202305160035
    guild_id_1 = 202305160036
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, None),
        (guild_id_1, Guild.precreate(guild_id_1)),
    ):
        event = GuildJoinRequestDeleteEvent(
            guild_id = input_value,
        )
        
        vampytest.assert_is(event.guild, expected_output)


def test__GuildJoinRequestDeleteEvent__user():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.user`` works as intended.
    
    Case: no fields given.
    """
    user_id = 202305160037
    
    event = GuildJoinRequestDeleteEvent(
        user_id = user_id,
    )
    
    output = event.user
    vampytest.assert_instance(output, ClientUserBase)
    vampytest.assert_eq(output.id, user_id)
