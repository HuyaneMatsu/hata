import vampytest

from ....application import Subscription

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__subscription_get_all_sku_user():
    """
    Tests whether ``Client.subscription_get_all_sku_user`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202409240017
    sku_id = 202409240018
    user_id = 202409240019
    subscription_id_0 = 202409240020
    subscription_id_1 = 202409240021
    
    
    mock_api_subscription_get_chunk_sku_user_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    sku_ids_0 = [sku_id, 202409240022]
    sku_ids_1 = [sku_id, 202409240023]
    
    output_subscription_datas = [
        {
            'id': str(subscription_id_0),
            'user_id': str(user_id),
            'sku_ids': [str(sku_id) for sku_id in sku_ids_0],
        }, {
            'id': str(subscription_id_1),
            'user_id': str(user_id),
            'sku_ids': [str(sku_id) for sku_id in sku_ids_1],
        }
    ]
    
    async def mock_api_subscription_get_chunk_sku_user(input_sku_id, query_string_parameters):
        nonlocal mock_api_subscription_get_chunk_sku_user_called
        nonlocal sku_id
        nonlocal output_subscription_datas
        nonlocal user_id
        mock_api_subscription_get_chunk_sku_user_called = True
        vampytest.assert_eq(sku_id, input_sku_id)
        vampytest.assert_eq(
            query_string_parameters,
            {
                'limit': 100,
                'after': 0,
                'user_id': user_id,
            },
        )
        return output_subscription_datas
    
    api.subscription_get_chunk_sku_user = mock_api_subscription_get_chunk_sku_user
        
    try:
        output = await client.subscription_get_all_sku_user(sku_id, user_id)
        vampytest.assert_true(mock_api_subscription_get_chunk_sku_user_called)
        
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(len(output), 2)
        
        output_subscription_0 = output[0]
        vampytest.assert_instance(output_subscription_0, Subscription)
        vampytest.assert_eq(output_subscription_0.id, subscription_id_0)
        vampytest.assert_eq(output_subscription_0.user_id, user_id)
        vampytest.assert_eq(output_subscription_0.sku_ids, tuple(sku_ids_0))
        
        output_subscription_1 = output[1]
        vampytest.assert_instance(output_subscription_1, Subscription)
        vampytest.assert_eq(output_subscription_1.id, subscription_id_1)
        vampytest.assert_eq(output_subscription_1.user_id, user_id)
        vampytest.assert_eq(output_subscription_1.sku_ids, tuple(sku_ids_1))
    
    finally:
        client._delete()
        client = None
