import vampytest

from ....application import Entitlement

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__entitlement_consume__stuffed():
    """
    Tests whether ``Client.entitlement_consume`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202404290000
    entitlement_id = 202404290001
    application_id = 202404290002
    
    entitlement = Entitlement.precreate(entitlement_id)
    
    mock_api_entitlement_consume_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    
    async def mock_api_entitlement_consume(input_application_id, input_entitlement_id):
        nonlocal mock_api_entitlement_consume_called
        nonlocal application_id
        nonlocal entitlement_id
        mock_api_entitlement_consume_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(entitlement_id, input_entitlement_id)
        return None
    
    api.entitlement_consume = mock_api_entitlement_consume
        
    try:
        output = await client.entitlement_consume(
            entitlement,
        )
        vampytest.assert_true(mock_api_entitlement_consume_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
