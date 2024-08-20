import vampytest

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__application_role_connection_metadata_delete_all():
    """
    Tests whether ``Client.application_role_connection_metadata_delete_all`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202408120007
    application_id = 202408120008
    
    mock_api_application_role_connection_metadata_delete_all_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    
    
    async def mock_api_application_role_connection_metadata_delete_all(input_application_id):
        nonlocal mock_api_application_role_connection_metadata_delete_all_called
        nonlocal application_id
        mock_api_application_role_connection_metadata_delete_all_called = True
        vampytest.assert_eq(application_id, input_application_id)
        return None
    
    
    api.application_role_connection_metadata_delete_all = mock_api_application_role_connection_metadata_delete_all
        
    try:
        output = await client.application_role_connection_metadata_delete_all()
        vampytest.assert_true(mock_api_application_role_connection_metadata_delete_all_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
