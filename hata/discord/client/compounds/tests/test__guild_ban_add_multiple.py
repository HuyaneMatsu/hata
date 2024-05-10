import vampytest

from ....guild import BanAddMultipleResult, Guild
from ....user import User

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_ban_add_multiple__stuffed():
    """
    Tests whether ``Client.guild_ban_add_multiple`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202405010082
    guild_id = 202405010083
    user_id_0 = 202405010084
    user_id_1 = 202405010085
    user_id_2 = 202405010086
    user_id_3 = 202405010087
    
    mock_api_guild_ban_add_multiple_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    guild = Guild.precreate(guild_id)
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_3 = User.precreate(user_id_3)
    delete_message_duration = 56
    reason = 'hey mister'
    expected_output = BanAddMultipleResult(
        banned_user_ids = [user_id_0, user_id_1],
        failed_user_ids = [user_id_2, user_id_3],
    )
    
    async def mock_api_guild_ban_add_multiple(input_guild_id, input_data, input_reason):
        nonlocal mock_api_guild_ban_add_multiple_called
        nonlocal guild_id
        nonlocal user_id_0
        nonlocal user_id_1
        nonlocal user_id_2
        nonlocal user_id_3
        nonlocal delete_message_duration
        nonlocal reason
        nonlocal expected_output
        
        mock_api_guild_ban_add_multiple_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(input_data['delete_message_seconds'], delete_message_duration)
        vampytest.assert_eq({*input_data['user_ids']}, {str(user_id_0), str(user_id_1), str(user_id_2), str(user_id_3)})
        vampytest.assert_eq(input_reason, reason)
        
        return expected_output.to_data()
    
    
    api.guild_ban_add_multiple = mock_api_guild_ban_add_multiple
        
    try:
        output = await client.guild_ban_add_multiple(
            guild,
            [user_0, user_1, user_2, user_3],
            delete_message_duration = delete_message_duration,
            reason = reason,
        )
        vampytest.assert_true(mock_api_guild_ban_add_multiple_called)
        
        vampytest.assert_instance(output, BanAddMultipleResult)
        vampytest.assert_eq(output, expected_output)
    finally:
        client._delete()
        client = None
