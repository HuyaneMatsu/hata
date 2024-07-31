
import vampytest

from ....emoji import Emoji
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_get_all_guild():
    """
    Tests whether ``Client.emoji_get_all_guild`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407270012
    guild_id = 202407270013
    emoji_id_0 = 202407270014
    emoji_id_1 = 202407270017
    
    
    mock_api_emoji_get_all_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
    name_0 = 'OrinGang'
    role_ids_0 = [202407270015, 202407290016]
    name_1 = 'OrinDance'
    role_ids_1 = [202407270018, 202407270019]
    
    output_emoji_datas = [
        {
            'id': str(emoji_id_0),
            'animated': False,
            'name': name_0,
            'roles': [str(role_id) for role_id in role_ids_0],
        }, {
            'id': str(emoji_id_1),
            'animated': False,
            'name': name_1,
            'roles': [str(role_id) for role_id in role_ids_1],
        }
    ]
    
    async def mock_api_emoji_get_all_guild(input_guild_id):
        nonlocal mock_api_emoji_get_all_guild_called
        nonlocal guild_id
        nonlocal output_emoji_datas
        mock_api_emoji_get_all_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        return output_emoji_datas
    
    api.emoji_get_all_guild = mock_api_emoji_get_all_guild
        
    try:
        output = await client.emoji_get_all_guild(guild_id)
        vampytest.assert_true(mock_api_emoji_get_all_guild_called)
        
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(len(output), 2)
        
        output_emoji_0 = output[0]
        vampytest.assert_instance(output_emoji_0, Emoji)
        vampytest.assert_eq(output_emoji_0.id, emoji_id_0)
        vampytest.assert_is(output_emoji_0.guild_id, guild_id)
        vampytest.assert_eq(output_emoji_0.name, name_0)
        vampytest.assert_eq(output_emoji_0.role_ids, tuple(role_ids_0))
        
        output_emoji_1 = output[1]
        vampytest.assert_instance(output_emoji_1, Emoji)
        vampytest.assert_eq(output_emoji_1.id, emoji_id_1)
        vampytest.assert_is(output_emoji_1.guild_id, guild_id)
        vampytest.assert_eq(output_emoji_1.name, name_1)
        vampytest.assert_eq(output_emoji_1.role_ids, tuple(role_ids_1))
        
        vampytest.assert_eq(
            guild.emojis,
            {
                emoji_id_0: output_emoji_0,
                emoji_id_1: output_emoji_1,
            },
        )
    
    finally:
        client._delete()
        client = None
