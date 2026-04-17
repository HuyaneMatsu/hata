import vampytest

from ....channel import Channel
from ....interaction import InteractionEvent, InteractionResponseType, InteractionType
from ....interaction.responding.constants import (
    RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_DEFERRING, RESPONSE_FLAG_EPHEMERAL
)
from ....message import Message, MessageFlag, MessageType

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__interaction_application_command_acknowledge__empty():
    """
    Tests whether ``Client.interaction_application_command_acknowledge`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202409210008
    channel_id = 202409210009
    message_id = 202409210010
    interaction_event_id = 202409210011
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
    show_for_invoking_user_only = True
    
    expected_message_data = {
        'type': InteractionResponseType.source.value,
        'data': {
            'flags': MessageFlag().update_by_keys(invoking_user_only = True),
        },
    }
    
    output_message_data = {
        'author': client.to_data(include_internals = True),
        'id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': None,
        'flags': int(MessageFlag().update_by_keys(loading = True, invoking_user_only = True)),
        'type': MessageType.default.value,
    }
    
    async def mock_api_interaction_response_message_create(
        input_interaction_event_id, input_interaction_event_token, input_message_data, query_string_parameters
    ):
        nonlocal mock_api_interaction_response_message_create_called
        nonlocal interaction_event_id
        nonlocal expected_message_data
        nonlocal interaction_event_token
        nonlocal interaction_event
        mock_api_interaction_response_message_create_called = True
        vampytest.assert_eq(interaction_event_id, input_interaction_event_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(interaction_event_token, input_interaction_event_token)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_DEFERRING)
        return {'resource': {'message': output_message_data}}
    
    api.interaction_response_message_create = mock_api_interaction_response_message_create
        
    try:
        output = await client.interaction_application_command_acknowledge(
            interaction_event,
            show_for_invoking_user_only = show_for_invoking_user_only,
        )
        vampytest.assert_true(mock_api_interaction_response_message_create_called)
        
        vampytest.assert_is_not(output, None)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_DEFERRED | RESPONSE_FLAG_EPHEMERAL)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, channel.messages)
        vampytest.assert_is(output.author, client)
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_eq(output.channel_id, channel_id)
        vampytest.assert_eq(output.flags, MessageFlag().update_by_keys(loading = True, invoking_user_only = True))
        vampytest.assert_is(output.type, MessageType.default)
        
        vampytest.assert_is(interaction_event.message, output)
    finally:
        client._delete()
        client = None
