import vampytest

from ....user import User

from ..guild_user_chunk_event import GuildUserChunkEvent


def test__GuildUserChunkEvent__repr():
    """
    Tests whether ``GuildUserChunkEvent.__repr__`` works as intended.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010012
    nonce = 'koishi'
    users = [User.precreate(202307010013), User.precreate(202307010014)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    
    vampytest.assert_instance(repr(guild_user_chunk_event), str)


def test__GuildUserChunkEvent__eq():
    """
    Tests whether ``GuildUserChunkEvent.__repr__`` works as intended.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010015
    nonce = 'koishi'
    users = [User.precreate(202307010016), User.precreate(202307010017)]
    
    keyword_parameters = {
        'chunk_count': chunk_count,
        'chunk_index': chunk_index,
        'guild_id': guild_id,
        'nonce': nonce,
        'users': users,
    }
    
    guild_user_chunk_event_original = GuildUserChunkEvent(**keyword_parameters)
    
    vampytest.assert_eq(guild_user_chunk_event_original, guild_user_chunk_event_original)
    
    for field_name, field_value in (
        ('chunk_count', 0),
        ('chunk_index', 0),
        ('guild_id', 0),
        ('nonce', None),
        ('users', None),
    ):
        guild_user_chunk_event_altered = GuildUserChunkEvent(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild_user_chunk_event_original, guild_user_chunk_event_altered)


def test__GuildUserChunkEvent__hash():
    """
    Tests whether ``GuildUserChunkEvent.__hash__`` works as intended.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010018
    nonce = 'koishi'
    users = [User.precreate(202307010019), User.precreate(202307010020)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    
    vampytest.assert_instance(hash(guild_user_chunk_event), int)


def test__GuildUserChunkEvent__unpack():
    """
    Tests whether ``GuildUserChunkEvent`` unpacking works as intended.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010021
    nonce = 'koishi'
    users = [User.precreate(202307010022), User.precreate(202307010023)]
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    
    vampytest.assert_eq(len([*guild_user_chunk_event]), len(guild_user_chunk_event))
