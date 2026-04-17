import vampytest

from ....application import Subscription

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__subscription_get_sku__stuffed():
    """
    Tests whether ``Client.subscription_get_sku`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202409240012
    sku_id = 202409240013
    subscription_id = 202409240014
    
    
    mock_api_subscription_get_sku_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    subscription = Subscription.precreate(subscription_id, sku_ids = [sku_id])
    
    sku_ids = [sku_id, 202409240016]
    
    output_subscription_data = {
        'id': str(subscription_id),
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
    }
    
    async def mock_api_subscription_get_sku(input_sku_id, input_subscription_id):
        nonlocal mock_api_subscription_get_sku_called
        nonlocal sku_id
        nonlocal subscription_id
        nonlocal output_subscription_data
        mock_api_subscription_get_sku_called = True
        vampytest.assert_eq(sku_id, input_sku_id)
        vampytest.assert_eq(subscription_id, input_subscription_id)
        return output_subscription_data
    
    api.subscription_get_sku = mock_api_subscription_get_sku
        
    try:
        output = await client.subscription_get_sku(
            subscription,
            force_update = True,
        )
        vampytest.assert_true(mock_api_subscription_get_sku_called)
        
        vampytest.assert_instance(output, Subscription)
        vampytest.assert_eq(output.id, subscription_id)
        vampytest.assert_eq(output.sku_ids, tuple(sku_ids))
    finally:
        client._delete()
        client = None
