import vampytest

from ....application import Entitlement

from ...client import Client

from .helpers import TestDiscordApiClient


def _iter_options():
    client_id = 202412050020
    exclude_deleted = True
    exclude_ended = True
    guild_id = 202412050021
    sku_id_0 = 202412050022
    sku_id_1 = 202412050023
    sku_ids = [sku_id_0, sku_id_1]
    user_id = 202412050024
    entitlement_id_0 = 202412050025
    entitlement_id_1 = 202412050026
    limit = 3
    after = 202412050027
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0, application_id = client_id, user_id = user_id, sku_id = sku_id_0
    )
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1, application_id = client_id, user_id = user_id, sku_id = sku_id_1
    )
    
    yield (
        client_id,
        {
            'after': after,
            'limit': limit,
            'exclude_deleted': exclude_deleted,
            'exclude_ended': exclude_ended,
            'guild_id': guild_id,
            'sku_ids': sku_ids,
            'user_id': user_id,
        },
        [
            (
                'entitlement_get_chunk',
                client_id,
                (
                    ('after', after),
                    ('exclude_deleted', exclude_deleted),
                    ('exclude_ended', exclude_ended),
                    ('guild_id', guild_id),
                    ('limit', limit),
                    ('sku_ids', ','.join(str(sku_id) for sku_id in sku_ids)),
                    ('user_id', user_id),
                ),
            ),
        ],
        [
            [
                entitlement_0.to_data(include_internals = True),
                entitlement_1.to_data(include_internals = True),
            ],
        ],
        [],
        [
            entitlement_0,
            entitlement_1,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__entitlement_get_chunk(
    client_id, extra_request_parameters, expected_requests, request_returns, global_mocks,
):
    """
    Tests whether ``Client.entitlement_get_chunk`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier.
    
    extra_request_parameters : `dict<str, object>`
        Extra parameters to execute the request with.
    
    expected_requests : `list<tuple<object>>`
        Expected requests.
    
    request_returns : `list<object>`
        Objects to return of requests.
    
    global_mocks : `dict<str, object>`
        Global variable mocks to apply.
    
    Returns
    -------
    output : `list<Entitlement>`
    """
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(
        token,
        api = api,
        client_id = client_id,
        application_id = client_id,
    )
    
    expected_requests = expected_requests.copy()
    request_returns = request_returns.copy()
    
    async def mock_entitlement_get_chunk(
        input_application_id, input_query_parameters
    ):
        nonlocal expected_requests
        nonlocal request_returns
        
        if (input_query_parameters is not None):
            input_query_parameters = tuple(sorted(input_query_parameters.items()))
        
        request_combined = (
            'entitlement_get_chunk', input_application_id, input_query_parameters
        )
        if expected_requests:
            expected_request = expected_requests[0]
        else:
            expected_request = None
        if request_combined != expected_request:
            raise RuntimeError(request_combined, '!=', expected_request)
        
        del expected_requests[0]
        return request_returns.pop(0)
    
    
    api.entitlement_get_chunk = mock_entitlement_get_chunk
    
    try:
        mocked = Client.entitlement_get_chunk
        if (global_mocks is not None):
            mocked = vampytest.mock_globals(mocked, values = global_mocks)
        
        output = await mocked(client, **extra_request_parameters)
        vampytest.assert_not(expected_requests)
        vampytest.assert_instance(output, list)
        for element in output:
            vampytest.assert_instance(element, Entitlement)
        
        return output
    
    finally:
        client._delete()
        client = None
