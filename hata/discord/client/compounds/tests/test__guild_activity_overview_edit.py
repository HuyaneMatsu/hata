import vampytest

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_activity_overview_edit():
    """
    Tests whether ``Client.guild_activity_overview_edit`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202504270006
    guild_id = 202504270007
    guild_name = 'pudding'
    reason = 'looks good'
    
    mock_api_guild_activity_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    output_guild_activity_overview_data = {
        'id': str(guild_id),
        'name': guild_name,
    }
    
    async def mock_api_guild_activity_edit(input_guild_id, input_data, input_reason):
        nonlocal mock_api_guild_activity_edit_called
        nonlocal guild_id
        nonlocal reason
        nonlocal guild_name
        nonlocal output_guild_activity_overview_data
        mock_api_guild_activity_edit_called = True
        vampytest.assert_eq(input_guild_id, guild_id)
        vampytest.assert_eq(input_data, {'name': guild_name})
        vampytest.assert_eq(input_reason, reason)
        return output_guild_activity_overview_data
    
    api.guild_activity_overview_edit = mock_api_guild_activity_edit
        
    try:
        output = await client.guild_activity_overview_edit(guild_id, name = guild_name, reason = reason)
        
        vampytest.assert_true(mock_api_guild_activity_edit_called)
        
        vampytest.assert_instance(output, type(None))
        
    finally:
        client._delete()
        client = None
