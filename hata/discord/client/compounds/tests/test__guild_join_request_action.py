import vampytest

from ....guild import GuildJoinRequestStatus

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__guild_join_request_action():
    client_id = 202610200000
    guild_id = 202610200001
    guild_join_request_id = 202610200002
    action = GuildJoinRequestStatus.rejected
    rejection_reason = 'satori'
    
    mock_api_guild_join_request_action_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    async def mock_api_guild_join_request_action(input_guild_id, input_guild_join_request_id, query):
        nonlocal mock_api_guild_join_request_action_called
        nonlocal guild_id
        nonlocal guild_join_request_id
        nonlocal action
        nonlocal rejection_reason
        mock_api_guild_join_request_action_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(guild_join_request_id, input_guild_join_request_id)
        vampytest.assert_eq(
            query,
            {
                'action': action.value,
                'rejection_reason': rejection_reason,
            }
        )
        return None
    
    api.guild_join_request_action = mock_api_guild_join_request_action
    
    try:
        output = await client.guild_join_request_action(
            guild_id,
            guild_join_request_id,
            action,
            rejection_reason = rejection_reason,
        )
        vampytest.assert_true(mock_api_guild_join_request_action_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
