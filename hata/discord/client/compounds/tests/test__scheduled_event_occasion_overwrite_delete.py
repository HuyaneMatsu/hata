from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....scheduled_event import ScheduledEvent
from ....utils import id_to_datetime

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__scheduled_event_occasion_overwrite_delete__stuffed():
    """
    Tests whether ``Client.scheduled_event_occasion_overwrite_delete`` works as intended.
    
    Case: stuffed fields.
    
    This function is a coroutine.
    """
    client_id = 202506240033
    guild_id = 202506240034
    scheduled_event_id = 202506240035
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    reason = 'patchouli'
    
    mock_api_scheduled_event_occasion_overwrite_delete_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
    
    
    async def mock_api_scheduled_event_occasion_overwrite_delete(
        input_guild_id, input_scheduled_event_id, input_timestamp_as_id, input_reason,
    ):
        nonlocal mock_api_scheduled_event_occasion_overwrite_delete_called
        nonlocal guild_id
        nonlocal scheduled_event_id
        nonlocal timestamp
        nonlocal reason
        mock_api_scheduled_event_occasion_overwrite_delete_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(timestamp, id_to_datetime(input_timestamp_as_id))
        vampytest.assert_eq(reason, input_reason)
        return None
    
    api.scheduled_event_occasion_overwrite_delete = mock_api_scheduled_event_occasion_overwrite_delete
        
    try:
        output = await client.scheduled_event_occasion_overwrite_delete(
            scheduled_event,
            timestamp,
            reason = reason,
        )
        vampytest.assert_true(mock_api_scheduled_event_occasion_overwrite_delete_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
