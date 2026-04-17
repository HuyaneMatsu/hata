import vampytest

from ....invite import Invite

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_delete__stuffed():
    """
    Tests whether ``Client.invite_delete`` works as intended.
    
    Case: stuffed invite.
    
    This function is a coroutine.
    """
    client_id = 202604110007
    invite_code = 'satori'
    reason = 'howling moon'
    
    mock_api_invite_delete_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    invite = Invite.precreate(invite_code)
    
    response_data = invite.to_data(include_internals = True)
    
    
    async def mock_api_invite_delete(input_invite_code, input_reason):
        nonlocal mock_api_invite_delete_called
        nonlocal reason
        nonlocal invite_code
        nonlocal response_data
        
        mock_api_invite_delete_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(reason, input_reason)
        
        return response_data
    
    
    api.invite_delete = mock_api_invite_delete
        
    try:
        output = await client.invite_delete(
            invite,
            reason = reason,
        )
        vampytest.assert_true(mock_api_invite_delete_called)
        
        vampytest.assert_instance(output, Invite)
        vampytest.assert_is(output, invite)
    finally:
        client._delete()
        client = None
