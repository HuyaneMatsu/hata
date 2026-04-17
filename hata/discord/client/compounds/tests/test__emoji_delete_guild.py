import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_delete_guild():
    """
    Tests whether ``Client.emoji_delete_guild`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407290004
    guild_id = 202407290005
    emoji_id = 202407290006
    
    
    mock_api_emoji_delete_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    reason = 'miau'
    
    
    async def mock_api_emoji_delete_guild(input_guild_id, input_emoji_id, input_reason):
        nonlocal mock_api_emoji_delete_guild_called
        nonlocal guild_id
        nonlocal emoji_id
        nonlocal reason
        mock_api_emoji_delete_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        vampytest.assert_eq(reason, input_reason)
        return None
    
    api.emoji_delete_guild = mock_api_emoji_delete_guild
        
    try:
        output = await client.emoji_delete_guild(
            emoji,
            reason = reason,
        )
        vampytest.assert_true(mock_api_emoji_delete_guild_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
