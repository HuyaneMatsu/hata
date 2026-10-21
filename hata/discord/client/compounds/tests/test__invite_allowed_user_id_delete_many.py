import vampytest

from ....invite import Invite

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_allowed_user_id_delete_many():
    """
    Tests whether ``Client.invite_allowed_user_id_delete_many`` works as intended.
    
    Case: bland invite; with allowed user ids.
    
    This function is a coroutine.
    """
    client_id = 202610070040
    user_id_0 = 202610070041
    user_id_1 = 202610070042
    invite_code = 'satori'
    
    mock_api_invite_allowed_user_id_delete_many_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    invite = Invite.precreate(invite_code)
    
    expected_data = {
        'user_ids': [
            user_id_0,
            user_id_1,
        ],
    }

    async def mock_api_invite_allowed_user_id_delete_many(input_invite_code, input_data):
        nonlocal mock_api_invite_allowed_user_id_delete_many_called
        nonlocal expected_data
        nonlocal invite_code
        mock_api_invite_allowed_user_id_delete_many_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(expected_data, input_data)
        return None
    
    api.invite_allowed_user_id_delete_many = mock_api_invite_allowed_user_id_delete_many
    
    try:
        output = await client.invite_allowed_user_id_delete_many(
            invite,
            allowed_user_ids = [user_id_0, user_id_1],
        )
        vampytest.assert_true(mock_api_invite_allowed_user_id_delete_many_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
