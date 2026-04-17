import vampytest

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_edit_vanity__stuffed():
    """
    Tests whether ``Client.invite_edit_vanity`` works as intended.
    
    Case: stuffed invite.
    
    This function is a coroutine.
    """
    client_id = 202604090002
    guild_id = 202604090003
    invite_code = 'satori'
    reason = 'howling moon'
    
    mock_api_invite_edit_vanity_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    expected_invite_data = {
        'code': invite_code,
    }
    
    output_invite_data = None
    
    
    async def mock_api_invite_edit_vanity(input_guild_id, input_invite_data, input_reason):
        nonlocal mock_api_invite_edit_vanity_called
        nonlocal guild_id
        nonlocal expected_invite_data
        nonlocal output_invite_data
        nonlocal reason
        nonlocal invite_code
        mock_api_invite_edit_vanity_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(expected_invite_data, input_invite_data)
        vampytest.assert_eq(reason, input_reason)
        return output_invite_data
    
    api.invite_edit_vanity = mock_api_invite_edit_vanity
        
    try:
        output = await client.invite_edit_vanity(
            guild_id,
            invite_code,
            reason = reason,
        )
        vampytest.assert_true(mock_api_invite_edit_vanity_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
