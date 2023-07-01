import vampytest

from ....guild import Guild

from ....user import User, GuildProfile

from ..guild_user_chunk_event import GuildUserChunkEvent

from .test__GuildUserChunkEvent__constructor import _assert_fields_set


def test__GuildUserChunkEvent__from_data__all_fields():
    """
    Tests whether ``GuildUserChunkEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010003
    nonce = 'koishi'
    users = [User.precreate(202307010004), User.precreate(202307010005)]
    
    data = {
        'chunk_count': chunk_count,
        'chunk_index': chunk_index,
        'guild_id': str(guild_id),
        'nonce': nonce,
        'members': [
            {**GuildProfile().to_data(include_internals = True), 'user': user.to_data(include_internals = True)}
            for user in users
        ],
    }
    
    guild_user_chunk_event = GuildUserChunkEvent.from_data(data)
    _assert_fields_set(guild_user_chunk_event)
    
    vampytest.assert_eq(guild_user_chunk_event.chunk_count, chunk_count)
    vampytest.assert_eq(guild_user_chunk_event.chunk_index, chunk_index)
    vampytest.assert_eq(guild_user_chunk_event.guild_id, guild_id)
    vampytest.assert_eq(guild_user_chunk_event.nonce, nonce)
    vampytest.assert_eq(guild_user_chunk_event.users, users)



def test__GuildUserChunkEvent__from_data__caching_new():
    """
    Tests whether ``GuildUserChunkEvent.from_data`` works as intended.
    
    Case: caching new.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010006
    nonce = 'koishi'
    users = [User.precreate(202307010007), User.precreate(202307010008)]
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'chunk_count': chunk_count,
        'chunk_index': chunk_index,
        'guild_id': str(guild_id),
        'nonce': nonce,
        'members': [
            {**GuildProfile().to_data(include_internals = True), 'user': user.to_data(include_internals = True)}
            for user in users
        ],
    }
    
    GuildUserChunkEvent.from_data(data)
    
    vampytest.assert_eq(guild.users, {user.id: user for user in users})


def test__GuildUserChunkEvent__to_data__defaults_and_internals():
    """
    Tests whether ``GuildUserChunkEvent.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    chunk_count = 2
    chunk_index = 1
    guild_id = 202307010009
    nonce = 'koishi'
    users = [User.precreate(202307010010), User.precreate(202307010011)]
    
    for user in users:
        user.guild_profiles[guild_id] = GuildProfile()
    
    guild_user_chunk_event = GuildUserChunkEvent(
        chunk_count = chunk_count,
        chunk_index = chunk_index,
        guild_id = guild_id,
        nonce = nonce,
        users = users,
    )
    
    expected_output = {
        'chunk_count': chunk_count,
        'chunk_index': chunk_index,
        'guild_id': str(guild_id),
        'nonce': nonce,
        'members': [
            {
                **GuildProfile().to_data(defaults = True, include_internals = True),
                'user': user.to_data(defaults = True, include_internals = True),
            }
            for user in users
        ],
    }
    
    vampytest.assert_eq(
        guild_user_chunk_event.to_data(defaults = True),
        expected_output,
    )
