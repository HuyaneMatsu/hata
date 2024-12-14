import vampytest

from ....application import Entitlement

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__entitlement_get__stuffed():
    """
    Tests whether ``Client.entitlement_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202412050060
    guild_id = 202412050061
    entitlement_id = 202412050062
    sku_id = 202412050064
    application_id = 202412050065
    user_id = 202412050066
    
    mock_api_entitlement_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    entitlement = Entitlement.precreate(
        entitlement_id, application_id = application_id, guild_id = guild_id
    )
    
    output_entitlement_data = {
        'instance_id': str(entitlement_id),
        'sku_id': str(sku_id),
        'application_id': application_id,
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    async def mock_api_entitlement_get(input_application_id, input_entitlement_id):
        nonlocal mock_api_entitlement_get_called
        nonlocal application_id
        nonlocal entitlement_id
        nonlocal output_entitlement_data
        mock_api_entitlement_get_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(entitlement_id, input_entitlement_id)
        return output_entitlement_data
    
    api.entitlement_get = mock_api_entitlement_get
        
    try:
        output = await client.entitlement_get(
            entitlement,
            force_update = True,
        )
        vampytest.assert_true(mock_api_entitlement_get_called)
        
        vampytest.assert_instance(output, Entitlement)
        vampytest.assert_eq(output.id, entitlement_id)
        vampytest.assert_eq(output.guild_id, guild_id)
        vampytest.assert_eq(output.sku_id, sku_id)
        vampytest.assert_eq(output.application_id, application_id)
        vampytest.assert_eq(output.user_id, user_id)
    finally:
        client._delete()
        client = None
