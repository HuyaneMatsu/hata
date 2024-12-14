import vampytest

from ....application import Entitlement

from ...client import Client

from ..application import ENTITLEMENT_GET_CHUNK_LIMIT_MAX

from .helpers import TestDiscordApiClient


def _iter_options():
    client_id = 202412050000
    exclude_deleted = True
    exclude_ended = True
    guild_id = 202412050004
    sku_ids = [202412050001, 202412050002]
    user_id = 202412050003
    
    yield (
        client_id,
        {
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
                    ('after', 0),
                    ('exclude_deleted', exclude_deleted),
                    ('exclude_ended', exclude_ended),
                    ('guild_id', guild_id),
                    ('limit', ENTITLEMENT_GET_CHUNK_LIMIT_MAX),
                    ('sku_ids', ','.join(str(sku_id) for sku_id in sku_ids)),
                    ('user_id', user_id),
                ),
            ),
        ],
        [
            [],
        ],
        [],
        [],
    )
    
    # general
    client_id = 202412050005
    sku_id_0 = 202412050006
    sku_id_1 = 202412050007
    user_id_0 = 202412050007
    user_id_1 = 202412050008
    entitlement_id_0 = 202412050009
    entitlement_id_1 = 202412050010
    entitlement_id_2 = 202412050011
    entitlement_id_3 = 202412050012
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0, application_id = client_id, user_id = user_id_0, sku_id = sku_id_0
    )
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1, application_id = client_id, user_id = user_id_0, sku_id = sku_id_1
    )
    entitlement_2 = Entitlement.precreate(
        entitlement_id_2, application_id = client_id, user_id = user_id_1, sku_id = sku_id_0
    )
    entitlement_3 = Entitlement.precreate(
        entitlement_id_3, application_id = client_id, user_id = user_id_1, sku_id = sku_id_1
    )
    
    chunk_size = 2
    
    yield (
        client_id,
        {},
        [
            (
                'entitlement_get_chunk',
                client_id,
                (
                    ('after', 0),
                    ('limit', chunk_size),
                ),
            ),
            (
                'entitlement_get_chunk',
                client_id,
                (
                    ('after', entitlement_id_1),
                    ('limit', chunk_size),
                ),
            ),
            (
                'entitlement_get_chunk',
                client_id,
                (
                    ('after', entitlement_id_3),
                    ('limit', chunk_size),
                ),
            ),
        ],
        [
            [
                entitlement_0.to_data(include_internals = True),
                entitlement_1.to_data(include_internals = True),
            ],
            [
                entitlement_2.to_data(include_internals = True),
                entitlement_3.to_data(include_internals = True),
            ],
            [],
        ],
        {'ENTITLEMENT_GET_CHUNK_LIMIT_MAX': chunk_size},
        [
            entitlement_0,
            entitlement_1,
            entitlement_2,
            entitlement_3,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__entitlement_get_all(
    client_id, extra_request_parameters, expected_requests, request_returns, global_mocks,
):
    """
    Tests whether ``Client.entitlement_get_all`` works as intended.
    
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
        mocked = Client.entitlement_get_all
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
