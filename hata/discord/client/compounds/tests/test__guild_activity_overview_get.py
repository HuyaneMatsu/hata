import vampytest

from ....guild import GuildActivityOverview

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_activity_overview_get():
    """
    Tests whether ``Client.guild_activity_overview_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202504270004
    guild_id = 202504270005
    guild_name = 'pudding'
    
    mock_api_guild_activity_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    output_guild_activity_overview_data = {
        'id': str(guild_id),
        'name': guild_name,
    }
    
    async def mock_api_guild_activity_get(input_guild_id):
        nonlocal mock_api_guild_activity_get_called
        nonlocal guild_id
        nonlocal output_guild_activity_overview_data
        mock_api_guild_activity_get_called = True
        vampytest.assert_eq(input_guild_id, guild_id)
        return output_guild_activity_overview_data
    
    api.guild_activity_overview_get = mock_api_guild_activity_get
        
    try:
        output = await client.guild_activity_overview_get(guild_id)
        
        vampytest.assert_true(mock_api_guild_activity_get_called)
        
        vampytest.assert_instance(output, GuildActivityOverview)
        vampytest.assert_eq(output.id, guild_id)
        vampytest.assert_eq(output.name, guild_name)
        
    finally:
        client._delete()
        client = None
