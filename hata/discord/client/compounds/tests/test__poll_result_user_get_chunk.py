import vampytest

from ....core import MESSAGES
from ....message import Message
from ....poll import Poll, PollAnswer, PollResult
from ....user import ClientUserBase, User

from ...client import Client

from .helpers import TestDiscordApiClient


def _iter_options():
    
    # known message + no poll
    client_id = 202404220000
    message_id = 202404220001
    channel_id = 202404220002
    answer_id = 202404220003
    
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
        {'message': message},
        (
            [],
            None,
        )
    )
    
    # known message + poll + no answer for id
    client_id = 202404220004
    message_id = 202404220005
    channel_id = 202404220006
    answer_id = 202404220007
    
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
        {'message': message},
        (
            [],
            Poll(),
        )
    )
    
    # known message + poll + answer for id + known users
    client_id = 202404220008
    message_id = 202404220009
    channel_id = 2024042200010
    answer_id = 2024042200011
    user_id_0 = 2024042200012
    user_id_1 = 2024042200013
    
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
    client_id = 2024042200014
    message_id = 202404220015
    channel_id = 2024042200016
    answer_id = 2024042200017
    user_id_0 = 2024042200018
    user_id_1 = 2024042200019
    
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
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('limit', 100),))
        ],
        [
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
        {'message': message},
        (
            [user_0, user_1],
            None,
        )
    )
    
    # known message + poll + answer for id + not known users
    client_id = 202404220020
    message_id = 202404220021
    channel_id = 2024042200022
    answer_id = 2024042200023
    user_id_0 = 2024042200024
    user_id_1 = 2024042200025
    
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
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('limit', 100),))
        ],
        [
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
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
    client_id = 202404220026
    message_id = 202404220027
    channel_id = 2024042200028
    answer_id = 2024042200029
    user_id_0 = 2024042200030
    user_id_1 = 2024042200031
    
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
    client_id = 202404220032
    message_id = 20240422033
    channel_id = 2024042200034
    
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
        {'message': message},
        (
            [],
            None,
        )
    )


    # known message + poll + cannot detect answer id
    client_id = 202404220035
    message_id = 20240422036
    channel_id = 2024042200037
    answer_id = 2024042200038
    
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
    client_id = 202404220039
    message_id = 202404220040
    channel_id = 2024042200041
    answer_id = 2024042200042
    user_id_0 = 2024042200043
    user_id_1 = 2024042200044
    
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
            ('poll_result_user_get_chunk', channel_id, message_id, answer_id, (('limit', 100),))
        ],
        [
            message_data,
            {
                'users': [user_0.to_data(include_internals = True), user_1.to_data(include_internals = True),]
            }
        ],
        {'message': message},
        (
            [user_0, user_1],
            None,
        )
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__poll_result_user_get_chunk(
    client_id, message, poll_answer, extra_request_parameters, expected_requests, request_returns, cache,
):
    """
    Tests whether ``Client.poll_result_user_get_chunk`` works as intended.
    
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
        output = await client.poll_result_user_get_chunk(message, poll_answer, **extra_request_parameters)
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
