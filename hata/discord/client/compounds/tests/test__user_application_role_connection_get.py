import vampytest
from scarletio import IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION

from ....application import ApplicationRoleConnection

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__user_application_role_connection_get__stuffed():
    """
    Tests whether ``Client.user_application_role_connection_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202607050000
    application_id = 202607050001
    platform_name = 'Only Fumos'
    platform_user_name = 'Remilia'
    metadata_values = {'hey': 'mister'}

    access_token = 'hey mister'
    
    api_user_application_role_connection_get__patched_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    
    
    headers = IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION] = f'Bearer {access_token}'
    
    output_entitlement_data = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    ).to_data()
    
    async def api_user_application_role_connection_get__patched(self, input_application_id, input_headers):
        nonlocal api_user_application_role_connection_get__patched_called
        nonlocal application_id
        nonlocal headers
        nonlocal output_entitlement_data
        api_user_application_role_connection_get__patched_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(headers, input_headers)
        return output_entitlement_data
    
    user_application_role_connection_get__original = TestDiscordApiClient.user_application_role_connection_get
        
    try:
        TestDiscordApiClient.user_application_role_connection_get = api_user_application_role_connection_get__patched
    
        output = await client.user_application_role_connection_get(
            access_token,
        )
        vampytest.assert_true(api_user_application_role_connection_get__patched_called)
        
        vampytest.assert_instance(output, ApplicationRoleConnection)
        vampytest.assert_eq(output.platform_name, platform_name)
        vampytest.assert_eq(output.platform_user_name, platform_user_name)
        vampytest.assert_eq(output.metadata_values, metadata_values)
        
    finally:
        TestDiscordApiClient.user_application_role_connection_get = user_application_role_connection_get__original
        
        client._delete()
        client = None
