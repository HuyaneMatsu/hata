import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_get_guild__stuffed():
    """
    Tests whether ``Client.emoji_get_guild`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407290007
    guild_id = 202407290008
    emoji_id = 202407290009
    
    
    mock_api_emoji_get_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    name = 'OrinGang'
    role_ids = [202407290010, 202407290011]
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
        'roles': [str(role_id) for role_id in role_ids],
    }
    
    async def mock_api_emoji_get_guild(input_guild_id, input_emoji_id):
        nonlocal mock_api_emoji_get_guild_called
        nonlocal guild_id
        nonlocal emoji_id
        nonlocal output_emoji_data
        mock_api_emoji_get_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        return output_emoji_data
    
    api.emoji_get_guild = mock_api_emoji_get_guild
        
    try:
        output = await client.emoji_get_guild(
            emoji,
            force_update = True,
        )
        vampytest.assert_true(mock_api_emoji_get_guild_called)
        
        vampytest.assert_instance(output, Emoji)
        vampytest.assert_eq(output.id, emoji_id)
        vampytest.assert_is(output.guild_id, guild_id)
        vampytest.assert_eq(output.name, name)
        vampytest.assert_eq(output.role_ids, tuple(role_ids))
    finally:
        client._delete()
        client = None
