import vampytest

from ....invite import Invite, InviteAllowedUserIdsStatus

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_allowed_user_ids_get_status():
    """
    Tests whether ``Client.invite_allowed_user_ids_get_status`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604110014
    invite_code = 'satori'
    
    mock_api_invite_allowed_user_ids_get_status_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    invite = Invite.precreate(invite_code)
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus(
        processed = 5,
        total = 10,
    )
    
    response_data = invite_allowed_user_ids_status.to_data()
    
    
    async def mock_api_invite_allowed_user_ids_get_status(input_invite_code):
        nonlocal mock_api_invite_allowed_user_ids_get_status_called
        nonlocal invite_code
        nonlocal response_data
        
        mock_api_invite_allowed_user_ids_get_status_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        
        return response_data
    
    
    api.invite_allowed_user_ids_get_status = mock_api_invite_allowed_user_ids_get_status
        
    try:
        output = await client.invite_allowed_user_ids_get_status(invite)
        vampytest.assert_true(mock_api_invite_allowed_user_ids_get_status_called)
        
        vampytest.assert_instance(output, InviteAllowedUserIdsStatus)
        vampytest.assert_eq(output, invite_allowed_user_ids_status)
    finally:
        client._delete()
        client = None
