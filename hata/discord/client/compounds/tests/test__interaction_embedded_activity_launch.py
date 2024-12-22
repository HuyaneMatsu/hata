import vampytest

from ....channel import Channel
from ....interaction import InteractionEvent, InteractionResponseType, InteractionType
from ....interaction.responding.constants import RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__interaction_embedded_activity_launch__empty():
    """
    Tests whether ``Client.interaction_embedded_activity_launch`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202412220000
    channel_id = 202412220001
    interaction_event_id = 202412220003
    interaction_event_token = 'yuyuko'
    
    mock_api_interaction_response_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = client_id)
    channel = Channel.precreate(channel_id)
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
        token = interaction_event_token,
        channel = channel,
    )
    interaction_event._add_response_waiter()
    
    expected_interaction_data = {
        'type': InteractionResponseType.embedded_activity_launch.value,
    }
    
    async def mock_api_interaction_response_message_create(
        input_interaction_event_id, input_interaction_event_token, input_interaction_data, query_string_parameters
    ):
        nonlocal mock_api_interaction_response_message_create_called
        nonlocal interaction_event_id
        nonlocal expected_interaction_data
        nonlocal interaction_event_token
        nonlocal interaction_event
        mock_api_interaction_response_message_create_called = True
        vampytest.assert_eq(interaction_event_id, input_interaction_event_id)
        vampytest.assert_eq(expected_interaction_data, input_interaction_data)
        vampytest.assert_eq(interaction_event_token, input_interaction_event_token)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDING)
        return {'resource': None}
    
    api.interaction_response_message_create = mock_api_interaction_response_message_create
        
    try:
        output = await client.interaction_embedded_activity_launch(
            interaction_event,
        )
        vampytest.assert_true(mock_api_interaction_response_message_create_called)
        
        vampytest.assert_is(output, None)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDED)
    
    finally:
        client._delete()
        client = None
