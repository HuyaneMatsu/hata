import vampytest

from ....message import Message
from ....poll import Poll, PollAnswer, PollResult
from ....user import User

from ...client import Client

from .helpers import TestDiscordApiClient


def _iter_options():
    
    # no poll
    client_id = 202404220200
    message_id = 202404220201
    channel_id = 202404220202
    
    poll = None
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        {},
        [
            ('message_get', channel_id, message_id),
        ],
        [
            message.to_data(include_internals = True),
        ],
        None,
        {'message': message},
        (
            message,
            None,
        )
    )
    
    # general
    client_id = 202404220239
    message_id = 202404220240
    channel_id = 2024042202041
    answer_id_0 = 2024042202042
    answer_id_1 = 2024042202043
    answer_id_2 = 2024042202044
    answer_id_3 = 2024042202045
    user_id_0 = 2024042202046
    user_id_1 = 2024042202047
    user_id_2 = 2024042202048
    user_id_3 = 2024042202049
    
    chunk_size = 2
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_3 = User.precreate(user_id_3)
    
    poll = Poll(
        answers = [
            PollAnswer.precreate(answer_id = answer_id_0, text = 'hey'),
            PollAnswer.precreate(answer_id = answer_id_1, text = 'mister'),
            PollAnswer.precreate(answer_id = answer_id_2, text = 'sister'),
            PollAnswer.precreate(answer_id = answer_id_3, text = 'aya'),
        ],
        results = [
            PollResult(
                answer_id = answer_id_0,
                count = 2,
                users = [],
            ),
            PollResult(
                answer_id = answer_id_1,
                count = 4,
                users = [],
            ),
            PollResult(
                answer_id = answer_id_2,
                count = 2,
                users = [user_1, user_2],
            ),
        ]
    )
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        {},
        [
            ('message_get', channel_id, message_id),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id_0, (('after', 0), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id_0, (('after', user_id_1), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id_1, (('after', 0), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id_1, (('after', user_id_1), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id_1, (('after', user_id_3), ('limit', chunk_size),)),
        ],
        [
            message.to_data(include_internals = True),
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            },
            {
                'users': []
            },
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            },
            {
                'users': [user_2.to_data(include_internals = True), user_3.to_data(include_internals = True),]
            },
            {
                'users': []
            },
        ],
        {'POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX': chunk_size},
        {'message': message},
        (
            message,Poll(
                answers = [
                    PollAnswer.precreate(answer_id = answer_id_0, text = 'hey'),
                    PollAnswer.precreate(answer_id = answer_id_1, text = 'mister'),
                    PollAnswer.precreate(answer_id = answer_id_2, text = 'sister'),
                    PollAnswer.precreate(answer_id = answer_id_3, text = 'aya'),
                ],
                results = [
                    PollResult(
                        answer_id = answer_id_0,
                        count = 2,
                        users = [user_0, user_1],
                    ),
                    PollResult(
                        answer_id = answer_id_1,
                        count = 4,
                        users = [user_0, user_1, user_2, user_3],
                    ),
                    PollResult(
                        answer_id = answer_id_2,
                        count = 2,
                        users = [user_1, user_2],
                    ),
                    PollResult(
                        answer_id = answer_id_3,
                        count = 0,
                        users = [],
                    ),
                ]
            )
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__poll_result_get_all(
    client_id, message, extra_request_parameters, expected_requests, request_returns, global_mocks, cache,
):
    """
    Tests whether ``Client.poll_result_user_get_all`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier.
    message : `Message | (int, int)`
        Message to request to.
    extra_request_parameters : `dict<str, object>`
        Extra parameters to execute the request with.
    expected_requests : `list<tuple<object>>`
        Expected requests.
    request_returns : `list<object>`
        Objects to return of requests.
    global_mocks : `dict<str, object>`
        Global variable mocks to apply.
    cache : `None | dict<str, object>`
        Extra objects to keep in the cache.
    
    Returns
    -------
    output : `list<ClientUserBase>`
    poll : `None | Poll`
    """
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    
    expected_requests = expected_requests.copy()
    request_returns = request_returns.copy()
    
    async def mock_poll_result_user_get_chunk(
        input_channel_id, input_message_id, input_answer_id, input_query_parameters
    ):
        nonlocal expected_requests
        nonlocal request_returns
        
        if (input_query_parameters is not None):
            input_query_parameters = tuple(sorted(input_query_parameters.items()))
        
        request_combined = (
            'poll_result_user_get_chunk', input_channel_id, input_message_id, input_answer_id, input_query_parameters
        )
        if expected_requests:
            expected_request = expected_requests[0]
        else:
            expected_request = None
        if request_combined != expected_request:
            raise RuntimeError(request_combined, '!=', expected_request)
        
        del expected_requests[0]
        return request_returns.pop(0)
    
    
    api.poll_result_user_get_chunk = mock_poll_result_user_get_chunk
    
    async def mock_message_get(
        input_channel_id, input_message_id
    ):
        nonlocal expected_requests
        nonlocal request_returns
        
        request_combined = (
            'message_get', input_channel_id, input_message_id
        )
        if expected_requests:
            expected_request = expected_requests[0]
        else:
            expected_request = None
        if request_combined != expected_request:
            raise RuntimeError(request_combined, '!=', expected_request)
        
        del expected_requests[0]
        return request_returns.pop(0)
    
    api.message_get = mock_message_get
    
    try:
        mocked = Client.poll_result_get_all
        if (global_mocks is not None):
            mocked = vampytest.mock_globals(mocked, values = global_mocks)
        
        output = await mocked(client, message, **extra_request_parameters)
        vampytest.assert_not(expected_requests)
        vampytest.assert_instance(output, Message)
        
        cached_message = cache.get('message', None)
        if cached_message is None:
            poll = None
        else:
            poll = cached_message.poll
        
        return output, poll
    
    finally:
        client._delete()
        client = None
