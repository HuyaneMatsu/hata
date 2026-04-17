import vampytest

from ....invite import Invite
from ....guild import Guild

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_get_all_guild():
    """
    Tests whether ``Client.invite_get_all_guild`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604110003
    invite_code_0 = 'satori'
    invite_code_1 = 'eye'
    guild_id = 202604110004
    
    mock_api_invite_get_all_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    guild.clients.append(client)
    
    invite_0 = Invite.precreate(
        invite_code_0, guild = guild, uses = 13
    )
    invite_1 = Invite.precreate(
        invite_code_1, guild = guild, uses = 14
    )
    response_data = [
        invite_0.to_data(include_internals = True),
        invite_1.to_data(include_internals = True),
    ]
    
    async def mock_api_invite_get_all_guild(input_guild_id):
        nonlocal mock_api_invite_get_all_guild_called
        nonlocal guild_id
        nonlocal response_data
        
        mock_api_invite_get_all_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        
        return response_data
    
    
    api.invite_get_all_guild = mock_api_invite_get_all_guild
        
    try:
        output = await client.invite_get_all_guild(guild)
        vampytest.assert_true(mock_api_invite_get_all_guild_called)
        
        vampytest.assert_eq(output, [invite_0, invite_1])
    finally:
        client._delete()
        client = None
