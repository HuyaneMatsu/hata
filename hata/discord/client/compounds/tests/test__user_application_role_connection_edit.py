import vampytest
from scarletio import IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION

from ....application import ApplicationRoleConnection

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__user_application_role_connection_edit__stuffed():
    """
    Tests whether ``Client.user_application_role_connection_edit`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202607050002
    application_id = 202607050003
    platform_name = 'Only Fumos'
    platform_user_name = 'Remilia'
    metadata_values = {'hey': 'mister'}

    access_token = 'hey mister'
    
    api_user_application_role_connection_edit__patched_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    
    
    headers = IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION] = f'Bearer {access_token}'
    
    data = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    ).to_data(defaults = True)
    
    output_entitlement_data = ApplicationRoleConnection(
        platform_name = platform_name,
        platform_user_name = platform_user_name,
        metadata_values = metadata_values,
    ).to_data()
    
    
    async def api_user_application_role_connection_edit__patched(self, input_application_id, input_data, input_headers):
        nonlocal api_user_application_role_connection_edit__patched_called
        nonlocal application_id
        nonlocal data
        nonlocal headers
        nonlocal output_entitlement_data
        api_user_application_role_connection_edit__patched_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(data, input_data)
        vampytest.assert_eq(headers, input_headers)
        return output_entitlement_data
    
    user_application_role_connection_edit__original = TestDiscordApiClient.user_application_role_connection_edit
        
    try:
        TestDiscordApiClient.user_application_role_connection_edit = api_user_application_role_connection_edit__patched
    
        output = await client.user_application_role_connection_edit(
            access_token,
            platform_name = platform_name,
            platform_user_name = platform_user_name,
            metadata_values = metadata_values,
        )
        vampytest.assert_true(api_user_application_role_connection_edit__patched_called)
        
        vampytest.assert_instance(output, ApplicationRoleConnection)
        vampytest.assert_eq(output.platform_name, platform_name)
        vampytest.assert_eq(output.platform_user_name, platform_user_name)
        vampytest.assert_eq(output.metadata_values, metadata_values)
        
    finally:
        TestDiscordApiClient.user_application_role_connection_edit = user_application_role_connection_edit__original
        
        client._delete()
        client = None
