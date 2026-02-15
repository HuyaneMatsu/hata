import vampytest

from ....scheduled_event import ScheduledEvent, ScheduledEventUserEntry
from ....user import User

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__scheduled_event_user_get_all():
    """
    Tests whether ``Client.scheduled_event_user_get_all`` works as intended.
    """
    client_id = 202602080010
    user_id_0 = 202602080011
    user_id_1 = 202602080012
    user_id_2 = 202602080015
    user_id_3 = 202602080016
    guild_id = 202602080013
    scheduled_event_id = 202602080014
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_3 = User.precreate(user_id_3)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    
    response_datas = [
        [
            {
                'guild_scheduled_event_id': str(scheduled_event_id),
                'user': user_0.to_data(include_internals = True),
            },
            {
                'guild_scheduled_event_id': str(scheduled_event_id),
                'user': user_1.to_data(include_internals = True),
            },
        ], [
            {
                'guild_scheduled_event_id': str(scheduled_event_id),
                'user': user_2.to_data(include_internals = True),
            },
            {
                'guild_scheduled_event_id': str(scheduled_event_id),
                'user': user_3.to_data(include_internals = True),
            },
        ], [
        ],
    ]
    
    expected_queries = [
        {'after': 0, 'limit': 2, 'with_member': True},
        {'after': user_id_1, 'limit': 2, 'with_member': True},
        {'after': user_id_3, 'limit': 2, 'with_member': True},
    ]
    
    scheduled_event_user_get_chunk_count = 0
    
    async def mock_scheduled_event_user_get_chunk(input_guild_id, input_scheduled_event_id, input_query):
        nonlocal guild_id
        nonlocal response_datas
        nonlocal scheduled_event_id
        nonlocal scheduled_event_user_get_chunk_count
        nonlocal expected_queries
        
        vampytest.assert_true(scheduled_event_user_get_chunk_count < len(expected_queries))
        
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(expected_queries[scheduled_event_user_get_chunk_count], input_query)
        response_data = response_datas[scheduled_event_user_get_chunk_count]
        scheduled_event_user_get_chunk_count += 1
        return response_data
    
    
    api.scheduled_event_user_get_chunk = mock_scheduled_event_user_get_chunk
    
    mocked = vampytest.mock_globals(
        Client.scheduled_event_user_get_all,
        SCHEDULED_EVENT_USER_GET_CHUNK_LIMIT_MAX = 2,
    )
    
    try:
        output = await mocked(client, scheduled_event)
        
        vampytest.assert_eq(scheduled_event_user_get_chunk_count, len(expected_queries))
        vampytest.assert_eq(
            output,
            [
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_0),
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_1),
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_2),
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_3),
            ],
        )
    
    finally:
        client._delete()
        client = None
