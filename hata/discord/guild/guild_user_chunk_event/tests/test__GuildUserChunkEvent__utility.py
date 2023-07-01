import vampytest

from ....guild import Guild

from ....user import User

from ..guild_user_chunk_event import GuildUserChunkEvent

from .test__GuildUserChunkEvent__constructor import _assert_fields_set


def test__GuildUserChunkEvent__copy():
    """
    Tests whether ``GuildUserChunkEvent.copy`` works as intended.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010024
    nonce = 'koishi'
    users = [User.precreate(202307010025), User.precreate(202307010026)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    
    copy = guild_user_chunk_event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_user_chunk_event, copy)

    vampytest.assert_eq(guild_user_chunk_event, copy)


def test__GuildUserChunkEvent__copy_with__no_fields():
    """
    Tests whether ``GuildUserChunkEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010027
    nonce = 'koishi'
    users = [User.precreate(202307010028), User.precreate(202307010029)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    copy = guild_user_chunk_event.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_user_chunk_event, copy)

    vampytest.assert_eq(guild_user_chunk_event, copy)


def test__GuildUserChunkEvent__copy_with__all_fields():
    """
    Tests whether ``GuildUserChunkEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_chunk_count = 2
    old_chunk_index = 1
    old_guild_id = 202307010030
    old_nonce = 'koishi'
    old_users = [User.precreate(202307010031), User.precreate(202307010032)]
    
    new_chunk_count = 4
    new_chunk_index = 3
    new_guild_id = 202307010033
    new_nonce = 'satori'
    new_users = [User.precreate(202307010034), User.precreate(202307010035)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = old_chunk_count,
        chunk_index = old_chunk_index,
        guild_id = old_guild_id,
        nonce = old_nonce,
        users = old_users,
    )
    copy = guild_user_chunk_event.copy_with(
        chunk_count = new_chunk_count,
        chunk_index = new_chunk_index,
        guild_id = new_guild_id,
        nonce = new_nonce,
        users = new_users,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_user_chunk_event, copy)
    
    vampytest.assert_eq(copy.chunk_count, new_chunk_count)
    vampytest.assert_eq(copy.chunk_index, new_chunk_index)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.nonce, new_nonce)
    vampytest.assert_eq(copy.users, new_users)


def test__GuildUserChunkEvent__guild__not_cached():
    """
    Tests whether ``GuildUserChunkEvent.guild`` works as intended.
    
    Case: Not cached.
    """
    guild_id = 202307010036
    
    guild_user_chunk_event = GuildUserChunkEvent(guild_id = guild_id)
    
    output = guild_user_chunk_event.guild
    vampytest.assert_is(output, None)


def test__GuildUserChunkEvent__guild__cached():
    """
    Tests whether ``GuildUserChunkEvent.guild`` works as intended.
    
    Case: Cached.
    """
    guild_id = 202307010037
    
    guild = Guild.precreate(guild_id)
    
    guild_user_chunk_event = GuildUserChunkEvent(guild_id = guild_id)
    
    vampytest.assert_is(guild_user_chunk_event.guild, guild)


def test__GuildUserChunkEvent__iter_users():
    """
    Tests whether ``GuildUserChunkEvent.iter_users`` works as intended.
    """
    user_0 = User.precreate(202307010039)
    user_1 = User.precreate(202307010040)
    
    for input_value, expected_output in (
        (None, []),
        ([user_0], [user_0]),
        ([user_0, user_1], [user_0, user_1]),
    ):
        guild_user_chunk_event = GuildUserChunkEvent(users = input_value)
        vampytest.assert_eq([*guild_user_chunk_event.iter_users()], expected_output)
