import vampytest

from ....guild import Guild
from ....user import User

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_ban_add__stuffed():
    """
    Tests whether ``Client.guild_ban_add`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202405010079
    guild_id = 202405010080
    user_id = 202405010081
    
    mock_api_guild_ban_add_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    guild = Guild.precreate(guild_id)
    user = User.precreate(user_id)
    delete_message_duration = 56
    reason = 'hey mister'
    
    async def mock_api_guild_ban_add(input_guild_id, input_user_id, input_data, input_reason):
        nonlocal mock_api_guild_ban_add_called
        nonlocal guild_id
        nonlocal user_id
        nonlocal delete_message_duration
        nonlocal reason
        
        mock_api_guild_ban_add_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(user_id, input_user_id)
        vampytest.assert_eq(input_data, {'delete_message_seconds': delete_message_duration})
        vampytest.assert_eq(input_reason, reason)
        
        return None
    
    api.guild_ban_add = mock_api_guild_ban_add
        
    try:
        output = await client.guild_ban_add(
            guild,
            user,
            delete_message_duration = delete_message_duration,
            reason = reason,
        )
        vampytest.assert_true(mock_api_guild_ban_add_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
