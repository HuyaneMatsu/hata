import vampytest

from ....invite import Invite

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_allowed_user_ids_get():
    """
    Tests whether ``Client.invite_allowed_user_ids_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604110010
    invite_code = 'satori'
    user_id_0 = 202604110011
    user_id_1 = 202604110012
    
    mock_api_invite_allowed_user_ids_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    invite = Invite.precreate(invite_code)
    
    response_data = f'user_id\r\n{user_id_0}\r\n{user_id_1}\r\n'
    
    
    async def mock_api_invite_allowed_user_ids_get(input_invite_code):
        nonlocal mock_api_invite_allowed_user_ids_get_called
        nonlocal invite_code
        nonlocal response_data
        
        mock_api_invite_allowed_user_ids_get_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        
        return response_data
    
    
    api.invite_allowed_user_ids_get = mock_api_invite_allowed_user_ids_get
        
    try:
        output = await client.invite_allowed_user_ids_get(invite)
        vampytest.assert_true(mock_api_invite_allowed_user_ids_get_called)
        
        vampytest.assert_eq(output, [user_id_0, user_id_1])
    finally:
        client._delete()
        client = None
