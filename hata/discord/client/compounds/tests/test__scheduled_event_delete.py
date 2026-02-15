import vampytest

from ....scheduled_event import ScheduledEvent

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__scheduled_event_delete__stuffed():
    """
    Tests whether ``Client.scheduled_event_delete`` works as intended.
    
    Case: stuffed scheduled_event.
    
    This function is a coroutine.
    """
    client_id = 202602070006
    guild_id = 202602070007
    scheduled_event_id = 202602070008
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    reason = 'howling moon'
    
    mock_api_scheduled_event_delete_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    
    async def mock_api_scheduled_event_delete(input_guild_id, input_scheduled_event_id, input_reason):
        nonlocal mock_api_scheduled_event_delete_called
        nonlocal guild_id
        nonlocal scheduled_event_id
        nonlocal reason
        mock_api_scheduled_event_delete_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(reason, input_reason)
    
    api.scheduled_event_delete = mock_api_scheduled_event_delete
        
    try:
        output = await client.scheduled_event_delete(
            scheduled_event,
            reason = reason,
        )
        vampytest.assert_true(mock_api_scheduled_event_delete_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
