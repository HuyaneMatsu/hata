import vampytest

from ....user import ClientUserBase, User, ZEROUSER

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



def test__GuildJoinRequestDeleteEvent__copy_with__no_fields():
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



def test__GuildJoinRequestDeleteEvent__copy_with__all_fields():
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


def _iter_options__guild():
    guild_id_0 = 202305160035
    guild_id_1 = 202305160036
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__GuildJoinRequestDeleteEvent__guild(guild_id):
    """
    Tests whether ``GuildJoinRequestDeleteEvent.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create the event with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
    )
    
    output = event.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__user():
    user_id_0 = 202305160037
    
    yield 0, ZEROUSER
    yield user_id_0, User.precreate(user_id_0)


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test__GuildJoinRequestDeleteEvent__user(user_id):
    """
    Tests whether ``GuildJoinRequestDeleteEvent.user`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create the event with.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    event = GuildJoinRequestDeleteEvent(
        user_id = user_id,
    )
    
    output = event.user
    vampytest.assert_instance(output, ClientUserBase)
    return output
