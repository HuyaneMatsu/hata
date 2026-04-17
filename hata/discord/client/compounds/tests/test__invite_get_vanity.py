import vampytest

from ....invite import Invite
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_get_vanity():
    """
    Tests whether ``Client.invite_get_vanity`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604090000
    guild_id = 202604090001
    invite_code = 'satori'
    
    mock_api_invite_get_vanity_called = False
    mock_api_invite_get_called = False
    
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    guild.clients.append(client)
    
    invite = Invite.precreate(
        invite_code, guild = guild, uses = 69,
    )
    new_uses = 90
    
    response_data_0 = {
        'code': invite_code,
        'uses': new_uses,
    }
    
    response_data_1 = {
        **invite.to_data(include_internals = True),
    }
    try:
        del response_data_1['uses']
    except KeyError:
        pass
    
    
    async def mock_api_invite_get_vanity(input_guild_id):
        nonlocal mock_api_invite_get_vanity_called
        nonlocal invite_code
        nonlocal guild_id
        nonlocal response_data_0
        
        mock_api_invite_get_vanity_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        
        return response_data_0
    
    
    async def mock_api_invite_get(input_invite_code, query):
        nonlocal mock_api_invite_get_called
        nonlocal invite_code
        nonlocal guild_id
        nonlocal response_data_1
        
        mock_api_invite_get_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(query, {'with_counts': True})
        
        return response_data_1
    
    
    api.invite_get_vanity = mock_api_invite_get_vanity
    api.invite_get = mock_api_invite_get
        
    try:
        output = await client.invite_get_vanity(guild)
        vampytest.assert_true(mock_api_invite_get_vanity_called)
        vampytest.assert_true(mock_api_invite_get_called)
        
        vampytest.assert_is(output, invite)
        vampytest.assert_eq(invite.uses, new_uses)
    finally:
        client._delete()
        client = None
