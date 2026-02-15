from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event import ScheduledEvent, ScheduledEventUserCounts
from ....utils import datetime_to_id

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__scheduled_event_user_counts_get():
    """
    Tests whether ``Client.scheduled_event_user_counts_get`` works as intended.
    """
    client_id = 202602110000
    scheduled_event_id = 202602110001
    guild_id = 202602110002
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    date_time_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    date_time_1 = DateTime(2016, 5, 24, tzinfo = TimeZone.utc)
    
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = 200,
        occasion_counts = {
            date_time_0 : 4,
            date_time_1 : 3,
        },
    )
    
    response_data = scheduled_event_user_counts.to_data()
    
    scheduled_event_user_counts_get_called = False
    
    async def mock_scheduled_event_user_counts_get(input_guild_id, input_scheduled_event_id, input_query):
        nonlocal guild_id
        nonlocal response_data
        nonlocal scheduled_event_id
        nonlocal date_time_0
        nonlocal date_time_1
        nonlocal scheduled_event_user_counts_get_called
        
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(
            {
                'guild_scheduled_event_exception_ids': [datetime_to_id(date_time_0), datetime_to_id(date_time_1)]
            },
            input_query,
        )
        scheduled_event_user_counts_get_called = True
        
        return response_data
    
    api.scheduled_event_user_counts_get = mock_scheduled_event_user_counts_get
    
    try:
        output = await client.scheduled_event_user_counts_get(
            scheduled_event, timestamps = [date_time_0, date_time_1],
        )
        
        vampytest.assert_true(scheduled_event_user_counts_get_called)
        vampytest.assert_eq(output, scheduled_event_user_counts)
    
    finally:
        client._delete()
        client = None
