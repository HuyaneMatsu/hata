import vampytest

from ....role import Role

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__role_delete__stuffed():
    """
    Tests whether ``Client.role_delete`` works as intended.
    
    Case: stuffed role.
    
    This function is a coroutine.
    """
    client_id = 202506190006
    guild_id = 202506190007
    role_id = 202506190008
    reason = 'howling moon'
    
    mock_api_role_delete_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    
    async def mock_api_role_delete(input_guild_id, input_role_id, input_reason):
        nonlocal mock_api_role_delete_called
        nonlocal guild_id
        nonlocal reason
        nonlocal role_id
        mock_api_role_delete_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(role_id, input_role_id)
        vampytest.assert_eq(reason, input_reason)
        return None
    
    api.role_delete = mock_api_role_delete
        
    try:
        output = await client.role_delete(
            role,
            reason = reason,
        )
        vampytest.assert_true(mock_api_role_delete_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
