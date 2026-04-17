import vampytest

from ....core import MESSAGES
from ....message import Message
from ....poll import Poll, PollAnswer, PollResult
from ....user import ClientUserBase, User

from ...client import Client

from .helpers import TestDiscordApiClient


def _iter_options():
    
    # known message + no poll
    client_id = 202404220100
    message_id = 202404220101
    channel_id = 202404220102
    answer_id = 202404220103
    
    answer = PollAnswer.precreate(answer_id = answer_id)
    poll = None
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [],
            None,
        )
    )
    
    # known message + poll + no answer for id
    client_id = 202404220104
    message_id = 202404220105
    channel_id = 202404220106
    answer_id = 202404220107
    
    answer = PollAnswer.precreate(answer_id = answer_id)
    poll = Poll()
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [],
            Poll(),
        )
    )
    
    # known message + poll + answer for id + known users
    client_id = 202404220108
    message_id = 202404220109
    channel_id = 2024042201010
    answer_id = 2024042201011
    user_id_0 = 2024042201012
    user_id_1 = 2024042201013
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    answer = PollAnswer.precreate(answer_id = answer_id)
    poll = Poll(
        answers = [
            answer,
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 2,
                users = [user_0, user_1],
            ),
        ]
    )
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [user_0, user_1],
            Poll(
                answers = [
                    answer,
                ],
                results = [
                    PollResult(
                        answer_id = answer_id,
                        count = 2,
                        users = [user_0, user_1],
                    ),
                ],
            ),
        )
    )

    # no message + answer id
    client_id = 2024042201014
    message_id = 202404220115
    channel_id = 2024042201016
    answer_id = 2024042201017
    user_id_0 = 2024042201018
    user_id_1 = 2024042201019
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    answer = PollAnswer.precreate(answer_id = answer_id)
    message = None
    
    yield (
        client_id,
        (channel_id, message_id),
        answer,
        {},
        [
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', 0), ('limit', 100),))
        ],
        [
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
        None,
        {'message': message},
        (
            [user_0, user_1],
            None,
        )
    )
    
    # known message + poll + answer for id + not known users
    client_id = 202404220120
    message_id = 202404220121
    channel_id = 2024042201022
    answer_id = 2024042201023
    user_id_0 = 2024042201024
    user_id_1 = 2024042201025
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    answer = PollAnswer.precreate(answer_id = answer_id)
    poll = Poll(
        answers = [
            answer,
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 2,
                users = [],
            ),
        ]
    )
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', 0), ('limit', 100),))
        ],
        [
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
        None,
        {'message': message},
        (
            [user_0, user_1],
            Poll(
                answers = [
                    answer,
                ],
                results = [
                    PollResult(
                        answer_id = answer_id,
                        count = 2,
                        users = [user_0, user_1],
                    ),
                ],
            ),
        )
    )


    # known message + poll + detect answer id + known users
    client_id = 202404220126
    message_id = 202404220127
    channel_id = 2024042201028
    answer_id = 2024042201029
    user_id_0 = 2024042201030
    user_id_1 = 2024042201031
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    answer = PollAnswer(text = 'hey')
    
    poll = Poll(
        answers = [
            PollAnswer.precreate(answer_id = answer_id, text = 'hey'),
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 2,
                users = [user_0, user_1],
            ),
        ]
    )
    
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [user_0, user_1],
            Poll(
                answers = [
                    PollAnswer.precreate(answer_id = answer_id, text = 'hey'),
                ],
                results = [
                    PollResult(
                        answer_id = answer_id,
                        count = 2,
                        users = [user_0, user_1],
                    ),
                ],
            ),
        )
    )


    # known message + no poll + detect answer id
    client_id = 202404220132
    message_id = 20240422033
    channel_id = 2024042201034
    
    answer = PollAnswer(text = 'hey')
    
    poll = None
    
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [],
            None,
        )
    )


    # known message + poll + cannot detect answer id
    client_id = 202404220135
    message_id = 20240422036
    channel_id = 2024042201037
    answer_id = 2024042201038
    
    answer = PollAnswer(text = 'hey')
    
    poll = Poll(
        answers = [
            PollAnswer.precreate(answer_id = answer_id, text = 'mister'),
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 2,
                users = [],
            ),
        ]
    )
    
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [],
        [],
        None,
        {'message': message},
        (
            [],
            Poll(
                answers = [
                    PollAnswer.precreate(answer_id = answer_id, text = 'mister'),
                ],
                results = [
                    PollResult(
                        answer_id = answer_id,
                        count = 2,
                        users = [],
                    ),
                ]
            ),
        )
    )


    # not known message + poll + answer for id + not known users
    client_id = 202404220139
    message_id = 202404220140
    channel_id = 2024042201041
    answer_id = 2024042201042
    user_id_0 = 2024042201043
    user_id_1 = 2024042201044
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    answer = PollAnswer(text = 'hey')
    poll = Poll(
        answers = [
            PollAnswer.precreate(answer_id = answer_id, text = 'hey'),
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 2,
                users = [],
            ),
        ]
    )
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    message_data = message.to_data(include_internals = True)
    message = None
    
    try:
        del MESSAGES[message_id]
    except KeyError:
        pass
    
    yield (
        client_id,
        (channel_id, message_id),
        answer,
        {},
        [
            ('message_get', channel_id, message_id),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', 0), ('limit', 100),)),
        ],
        [
            message_data,
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
        None,
        {'message': message},
        (
            [user_0, user_1],
            None,
        )
    )


    # known message + poll + answer for id + not known users + chunks
    client_id = 202404220145
    message_id = 202404220146
    channel_id = 2024042201047
    answer_id = 2024042201048
    user_id_0 = 2024042201049
    user_id_1 = 2024042201050
    user_id_2 = 2024042201051
    user_id_3 = 2024042201052
    
    chunk_size = 2
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_3 = User.precreate(user_id_3)
    answer = PollAnswer.precreate(answer_id = answer_id)
    poll = Poll(
        answers = [
            answer,
        ],
        results = [
            PollResult(
                answer_id = answer_id,
                count = 4,
                users = [],
            ),
        ]
    )
    message = Message.precreate(message_id, channel_id = channel_id, poll = poll)
    
    yield (
        client_id,
        message,
        answer,
        {},
        [
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', 0), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', user_id_1), ('limit', chunk_size),)),
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('after', user_id_3), ('limit', chunk_size),)),
        ],
        [
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
            [user_0, user_1, user_2, user_3],
            Poll(
                answers = [
                    answer,
                ],
                results = [
                    PollResult(
                        answer_id = answer_id,
                        count = 4,
                        users = [user_0, user_1, user_2, user_3],
                    ),
                ],
            ),
        )
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__poll_result_user_get_all(
    client_id, message, poll_answer, extra_request_parameters, expected_requests, request_returns, global_mocks, cache,
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
    poll_answer : `PollAnswer | int`
        Poll answer.
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
        mocked = Client.poll_result_user_get_all
        if (global_mocks is not None):
            mocked = vampytest.mock_globals(mocked, values = global_mocks)
        
        output = await mocked(client, message, poll_answer, **extra_request_parameters)
        vampytest.assert_not(expected_requests)
        vampytest.assert_instance(output, list)
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
        
        cached_message = cache.get('message', None)
        if cached_message is None:
            poll = None
        else:
            poll = cached_message.poll
        
        return output, poll
    
    finally:
        client._delete()
        client = None
