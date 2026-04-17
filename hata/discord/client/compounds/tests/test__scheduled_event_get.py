import vampytest

from ....scheduled_event import ScheduledEvent

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__scheduled_event_get__stuffed():
    """
    Tests whether ``Client.scheduled_event_get`` works as intended.
    
    Case: stuffed scheduled_event.
    
    This function is a coroutine.
    """
    client_id = 202602070010
    guild_id = 202602070011
    scheduled_event_id = 202602070012
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    name = 'komeiji'
    
    mock_api_scheduled_event_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    
    output_scheduled_event_data = {
        **scheduled_event.to_data(include_internals = True),
        'name': name,
    }
    
    
    async def mock_api_scheduled_event_get(input_guild_id, input_scheduled_event_id, input_query):
        nonlocal mock_api_scheduled_event_get_called
        nonlocal guild_id
        nonlocal scheduled_event_id
        nonlocal output_scheduled_event_data
        mock_api_scheduled_event_get_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq({'with_user_count': True}, input_query)
        return output_scheduled_event_data
    
    api.scheduled_event_get = mock_api_scheduled_event_get
        
    try:
        # location & stage  & voice are mutually exclusive
        output = await client.scheduled_event_get(
            scheduled_event,
            force_update = True,
        )
        vampytest.assert_true(mock_api_scheduled_event_get_called)
        
        vampytest.assert_is(output, scheduled_event)
        vampytest.assert_eq(scheduled_event.name, name)
    finally:
        client._delete()
        client = None
