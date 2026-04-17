from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event import ScheduledEvent, ScheduledEventUserEntry
from ....user import User
from ....utils import datetime_to_id

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__scheduled_event_occasion_user_get_chunk():
    """
    Tests whether ``Client.scheduled_event_occasion_user_get_chunk`` works as intended.
    """
    client_id = 202602110000
    user_id_0 = 202602110001
    user_id_1 = 202602110002
    guild_id = 202602110003
    scheduled_event_id = 202602110004
    timestamp = DateTime(2016, 5, 28, tzinfo = TimeZone.utc)
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    limit = 50
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    
    response_data = [
        {
            'guild_scheduled_event_id': str(scheduled_event_id),
            'user': user_0.to_data(include_internals = True),
        },
        {
            'guild_scheduled_event_id': str(scheduled_event_id),
            'user': user_1.to_data(include_internals = True),
        },
    ]
    
    scheduled_event_occasion_user_get_chunk_called = False
    
    async def mock_scheduled_event_occasion_user_get_chunk(
        input_guild_id, input_scheduled_event_id, input_timestamp_as_id, input_query
    ):
        nonlocal guild_id
        nonlocal response_data
        nonlocal scheduled_event_id
        nonlocal timestamp
        nonlocal after
        nonlocal limit
        nonlocal scheduled_event_occasion_user_get_chunk_called
        
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(datetime_to_id(timestamp), input_timestamp_as_id)
        vampytest.assert_eq({'after': datetime_to_id(after), 'limit': limit, 'with_member': True}, input_query)
        scheduled_event_occasion_user_get_chunk_called = True
        
        return response_data
    
    api.scheduled_event_occasion_user_get_chunk = mock_scheduled_event_occasion_user_get_chunk
    
    try:
        output = await client.scheduled_event_occasion_user_get_chunk(
            scheduled_event, timestamp, after = after, limit = limit)
        
        vampytest.assert_true(scheduled_event_occasion_user_get_chunk_called)
        vampytest.assert_eq(
            output,
            [
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_0),
                ScheduledEventUserEntry(scheduled_event_id = scheduled_event_id, user = user_1),
            ],
        )
    
    finally:
        client._delete()
        client = None
