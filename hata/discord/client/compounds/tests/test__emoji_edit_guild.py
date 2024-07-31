import vampytest

from ....emoji import Emoji

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__emoji_edit_guild__stuffed():
    """
    Tests whether ``Client.emoji_edit_guild`` works as intended.
    
    Case: stuffed fields.
    
    This function is a coroutine.
    """
    client_id = 202407270005
    guild_id = 202407270006
    emoji_id = 202407270007
    
    
    mock_api_emoji_edit_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    emoji = Emoji.precreate(emoji_id, guild_id = guild_id)
    
    name = 'OrinGang'
    role_ids = [202407270008, 202407270009]
    reason = 'miau'
    
    expected_emoji_data = {
        'name': name,
        'roles': [str(role_id) for role_id in role_ids],
    }
    
    output_emoji_data = {
        'id': str(emoji_id),
        'animated': False,
        'name': name,
        'roles': [str(role_id) for role_id in role_ids],
    }
    
    
    async def mock_api_emoji_edit_guild(input_guild_id, input_emoji_id, input_emoji_data, input_reason):
        nonlocal mock_api_emoji_edit_guild_called
        nonlocal guild_id
        nonlocal emoji_id
        nonlocal expected_emoji_data
        nonlocal output_emoji_data
        nonlocal reason
        mock_api_emoji_edit_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(emoji_id, input_emoji_id)
        vampytest.assert_eq(expected_emoji_data, input_emoji_data)
        vampytest.assert_eq(reason, input_reason)
        return output_emoji_data
    
    api.emoji_edit_guild = mock_api_emoji_edit_guild
        
    try:
        output = await client.emoji_edit_guild(
            emoji,
            name = name,
            role_ids = role_ids,
            reason = reason,
        )
        vampytest.assert_true(mock_api_emoji_edit_guild_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
