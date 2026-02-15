import vampytest

from ....guild import Guild
from ....scheduled_event import ScheduledEvent

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__scheduled_event_get_all_guild__stuffed():
    """
    Tests whether ``Client.scheduled_event_get_all_guild`` works as intended.
    
    Case: stuffed scheduled_event.
    
    This function is a coroutine.
    """
    client_id = 202602070020
    guild_id = 202602070021
    scheduled_event_id_0 = 202602070022
    scheduled_event_id_1 = 202602070023
    
    guild = Guild.precreate(
        guild_id,
    )
    
    scheduled_event_0 = ScheduledEvent.precreate(
        scheduled_event_id_0,
        guild_id = guild_id,
    )
    
    scheduled_event_1 = ScheduledEvent.precreate(
        scheduled_event_id_1,
        guild_id = guild_id,
    )
    
    mock_api_scheduled_event_get_all_guild_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    
    output_scheduled_event_data = [
        scheduled_event_0.to_data(include_internals = True),
        scheduled_event_1.to_data(include_internals = True),
    ]
    
    
    async def mock_api_scheduled_event_get_all_guild(input_guild_id, input_query):
        nonlocal mock_api_scheduled_event_get_all_guild_called
        nonlocal guild_id
        nonlocal output_scheduled_event_data
        mock_api_scheduled_event_get_all_guild_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq({'with_user_count': True}, input_query)
        return output_scheduled_event_data
    
    api.scheduled_event_get_all_guild = mock_api_scheduled_event_get_all_guild
        
    try:
        # location & stage  & voice are mutually exclusive
        output = await client.scheduled_event_get_all_guild(
            guild,
        )
        vampytest.assert_true(mock_api_scheduled_event_get_all_guild_called)
        
        vampytest.assert_eq(output, [scheduled_event_0, scheduled_event_1])
    finally:
        client._delete()
        client = None
