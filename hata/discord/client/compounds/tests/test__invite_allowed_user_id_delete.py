import vampytest

from ....invite import Invite

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_allowed_user_id_delete():
    """
    Tests whether ``Client.invite_allowed_user_id_delete`` works as intended.
    
    Case: bland invite; with allowed user ids.
    
    This function is a coroutine.
    """
    client_id = 202610070020
    user_id_0 = 202610070021
    invite_code = 'satori'
    
    mock_api_invite_allowed_user_id_delete_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    invite = Invite.precreate(invite_code)
    

    async def mock_api_invite_allowed_user_id_delete(input_invite_code, input_allowed_user_id):
        nonlocal mock_api_invite_allowed_user_id_delete_called
        nonlocal user_id_0
        nonlocal invite_code
        mock_api_invite_allowed_user_id_delete_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(user_id_0, input_allowed_user_id)
        return None
    
    api.invite_allowed_user_id_delete = mock_api_invite_allowed_user_id_delete
    
    try:
        output = await client.invite_allowed_user_id_delete(
            invite,
            allowed_user_id = user_id_0,
        )
        vampytest.assert_true(mock_api_invite_allowed_user_id_delete_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
