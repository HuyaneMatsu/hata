import vampytest

from ....role import Role
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__role_get():
    """
    Tests whether ``Client.role_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202411020000
    role_id = 202411020001
    guild_id = 202411020002
    
    mock_api_role_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    guild.clients.append(client)
    
    role = Role.precreate(
        role_id, guild_id = guild_id, name = 'pudding'
    )
    new_name = 'sister'
    
    response_data = {
        **role.to_data(include_internals = True),
        'name': new_name,
    }
    
    async def mock_api_role_get(input_guild_id, input_role_id):
        nonlocal mock_api_role_get_called
        nonlocal role_id
        nonlocal guild_id
        nonlocal response_data
        
        mock_api_role_get_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(role_id, input_role_id)
        
        return response_data
    
    
    api.role_get = mock_api_role_get
        
    try:
        output = await client.role_get(role, force_update = True)
        vampytest.assert_true(mock_api_role_get_called)
        
        vampytest.assert_is(output, role)
        vampytest.assert_eq(role.name, new_name)
    finally:
        client._delete()
        client = None
