import vampytest
from scarletio.web_common import FormData

from ....invite import Invite

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_allowed_user_ids_edit():
    """
    Tests whether ``Client.invite_allowed_user_ids_edit`` works as intended.
    
    Case: bland invite; with allowed user ids.
    
    This function is a coroutine.
    """
    client_id = 202604110015
    user_id_0 = 202604110016
    user_id_1 = 202604110017
    invite_code = 'satori'
    
    mock_api_invite_allowed_user_ids_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    invite = Invite.precreate(invite_code)
    
    allowed_user_ids = [
        user_id_0,
        user_id_1,
    ]
    
    expected_data = FormData()
    expected_data.add_field(
        'target_users_file',
        '\n'.join([str(user_id) for user_id in allowed_user_ids]),
        content_type = 'text/csv',
        file_name = f'file.csv',
    )
    
    async def mock_api_invite_allowed_user_ids_edit(input_invite_code, input_data):
        nonlocal mock_api_invite_allowed_user_ids_edit_called
        nonlocal expected_data
        nonlocal invite_code
        mock_api_invite_allowed_user_ids_edit_called = True
        vampytest.assert_eq(invite_code, input_invite_code)
        vampytest.assert_eq(expected_data, input_data)
        return None
    
    api.invite_allowed_user_ids_edit = mock_api_invite_allowed_user_ids_edit
        
    try:
        output = await client.invite_allowed_user_ids_edit(
            invite,
            allowed_user_ids = allowed_user_ids,
        )
        vampytest.assert_true(mock_api_invite_allowed_user_ids_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
