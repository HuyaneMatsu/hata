import vampytest
from scarletio import IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__user_application_role_connection_delete__stuffed():
    """
    Tests whether ``Client.user_application_role_connection_delete`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202607050004
    application_id = 202607050005

    access_token = 'hey mister'
    
    api_user_application_role_connection_delete__patched_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    
    
    headers = IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION] = f'Bearer {access_token}'
    
    async def api_user_application_role_connection_delete__patched(self, input_application_id, input_headers):
        nonlocal api_user_application_role_connection_delete__patched_called
        nonlocal application_id
        nonlocal headers
        api_user_application_role_connection_delete__patched_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(headers, input_headers)
        return None
    
    user_application_role_connection_delete__original = TestDiscordApiClient.user_application_role_connection_delete
        
    try:
        TestDiscordApiClient.user_application_role_connection_delete = api_user_application_role_connection_delete__patched
    
        output = await client.user_application_role_connection_delete(
            access_token,
        )
        vampytest.assert_true(api_user_application_role_connection_delete__patched_called)
        
        vampytest.assert_is(output, None)
        
    finally:
        TestDiscordApiClient.user_application_role_connection_delete = user_application_role_connection_delete__original
        
        client._delete()
        client = None
