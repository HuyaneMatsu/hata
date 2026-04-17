import vampytest

from ....user import User

from ..guild_user_chunk_event import GuildUserChunkEvent


def _assert_fields_set(guild_user_chunk_event):
    """
    Checks whether every attribute is set of the given guild user chunk event.
    
    Parameters
    ----------
    guild_user_chunk_event : ``GuildUserChunkEvent``
        The guild user chunk event to check.
    """
    vampytest.assert_instance(guild_user_chunk_event, GuildUserChunkEvent)
    vampytest.assert_instance(guild_user_chunk_event.chunk_count, int)
    vampytest.assert_instance(guild_user_chunk_event.chunk_index, int)
    vampytest.assert_instance(guild_user_chunk_event.guild_id, int)
    vampytest.assert_instance(guild_user_chunk_event.nonce, str, nullable = True)
    vampytest.assert_instance(guild_user_chunk_event.users, list)


def test__GuildUserChunkEvent__new__no_fields():
    """
    Tests whether ``GuildUserChunkEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_user_chunk_event = GuildUserChunkEvent()
    _assert_fields_set(guild_user_chunk_event)


def test__GuildUserChunkEvent__new__all_fields():
    """
    Tests whether ``GuildUserChunkEvent.__new__`` works as intended.
    
    Case: All fields given.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010000
    nonce = 'koishi'
    users = [User.precreate(202307010001), User.precreate(202307010002)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    _assert_fields_set(guild_user_chunk_event)
    
    vampytest.assert_eq(guild_user_chunk_event.chunk_count, chunk_count)
    vampytest.assert_eq(guild_user_chunk_event.chunk_index, chunk_index)
    vampytest.assert_eq(guild_user_chunk_event.guild_id, guild_id)
    vampytest.assert_eq(guild_user_chunk_event.nonce, nonce)
    vampytest.assert_eq(guild_user_chunk_event.users, users)
