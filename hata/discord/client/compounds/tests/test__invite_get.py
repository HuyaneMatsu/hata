import vampytest

from ....invite import Invite
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_get():
    """
    Tests whether ``Client.invite_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604110000
    invite_code = 'satori'
    guild_id = 202604110002
    
    mock_api_invite_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    guild.clients.append(client)
    
    invite = Invite.precreate(
        invite_code, guild = guild, uses = 13
    )
    new_uses = 17
    
    response_data = {
        **invite.to_data(include_internals = True),
        'uses': new_uses,
    }
    
    async def mock_api_invite_get(input_invite_code, input_query_string_parameters):
        nonlocal mock_api_invite_get_called
        nonlocal invite_code
        nonlocal response_data
        
        mock_api_invite_get_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(input_query_string_parameters, {'with_counts': True, 'with_permissions': True})
        
        return response_data
    
    
    api.invite_get = mock_api_invite_get
        
    try:
        output = await client.invite_get(invite)
        vampytest.assert_true(mock_api_invite_get_called)
        
        vampytest.assert_is(output, invite)
        vampytest.assert_eq(invite.uses, new_uses)
    finally:
        client._delete()
        client = None
