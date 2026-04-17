from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event import ScheduledEvent
from ....utils import datetime_to_timestamp, id_to_datetime

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__scheduled_event_occasion_overwrite_edit__stuffed():
    """
    Tests whether ``Client.scheduled_event_occasion_overwrite_edit`` works as intended.
    
    Case: stuffed fields.
    
    This function is a coroutine.
    """
    client_id = 202506280000
    guild_id = 202506280001
    scheduled_event_id = 202506280002
    cancelled = True
    end = DateTime(2016, 5, 14, 13, 30, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 13, 20, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    reason = 'patchouli'
    
    mock_api_scheduled_event_occasion_overwrite_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
    
    expected_cancellation_data = {
        'scheduled_start_time': datetime_to_timestamp(start),
        'scheduled_end_time': datetime_to_timestamp(end),
        'is_canceled': cancelled,
    }
    
    async def mock_api_scheduled_event_occasion_overwrite_edit(
        input_guild_id, input_scheduled_event_id, input_timestamp_as_id, input_cancellation_data, input_reason,
    ):
        nonlocal mock_api_scheduled_event_occasion_overwrite_edit_called
        nonlocal guild_id
        nonlocal scheduled_event_id
        nonlocal expected_cancellation_data
        nonlocal timestamp
        mock_api_scheduled_event_occasion_overwrite_edit_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(expected_cancellation_data, input_cancellation_data)
        vampytest.assert_eq(timestamp, id_to_datetime(input_timestamp_as_id))
        vampytest.assert_eq(reason, input_reason)
        return None
    
    api.scheduled_event_occasion_overwrite_edit = mock_api_scheduled_event_occasion_overwrite_edit
        
    try:
        output = await client.scheduled_event_occasion_overwrite_edit(
            scheduled_event,
            timestamp,
            cancelled = cancelled,
            end = end,
            start = start,
            reason = reason,
        )
        vampytest.assert_true(mock_api_scheduled_event_occasion_overwrite_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
