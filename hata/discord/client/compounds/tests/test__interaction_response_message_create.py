import vampytest

from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....interaction import InteractionEvent, InteractionResponseType, InteractionType
from ....interaction.responding.constants import (
    RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_DEFERRING, RESPONSE_FLAG_EPHEMERAL, RESPONSE_FLAG_RESPONDED,
    RESPONSE_FLAG_RESPONDING
)
from ....poll import Poll, PollAnswer
from ....message import MessageFlag

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__interaction_response_message_create__stuffed():
    """
    Tests whether ``Client.interaction_response_message_create`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403170000
    interaction_event_id = 202403170001
    interaction_event_token = 'yuyuko'
    
    mock_api_interaction_response_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = client_id)
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
        token = interaction_event_token,
    )
    
    allowed_mentions = ['everyone']
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    poll = Poll(answers = [PollAnswer(text = 'sister')], duration = 3600)
    silent = True
    tts = True
    show_for_invoking_user_only = True
    
    expected_message_data = {
        'data': {
            'tts': True,
            'content': content,
            'embeds': [embed.to_data() for embed in embeds],
            'poll': poll.to_data(),
            'components': [create_row(components).to_data()],
            'allowed_mentions' : {'parse': ['everyone']},
            'flags': MessageFlag().update_by_keys(silent = True, invoking_user_only = True),
        },
        'type': InteractionResponseType.message_and_source.value,
    }
    
    
    async def mock_api_interaction_response_message_create(
        input_interaction_event_id, input_interaction_event_token, input_message_data
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
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDING)
        return {}
    
    api.interaction_response_message_create = mock_api_interaction_response_message_create
        
    try:
        output = await client.interaction_response_message_create(
            interaction_event,
            allowed_mentions = allowed_mentions,
            components = components,
            content = content,
            embeds = embeds,
            poll = poll,
            silent = silent,
            tts = tts,
            show_for_invoking_user_only = show_for_invoking_user_only,
        )
        vampytest.assert_true(mock_api_interaction_response_message_create_called)
        
        vampytest.assert_is(output, None)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDED | RESPONSE_FLAG_EPHEMERAL)
    finally:
        client._delete()
        client = None


async def test__Client__interaction_response_message_create__empty():
    """
    Tests whether ``Client.interaction_response_message_create`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403170002
    interaction_event_id = 202403170003
    interaction_event_token = 'yuyuko'
    
    mock_api_interaction_response_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id, application_id = client_id)
    interaction_event = InteractionEvent.precreate(
        interaction_event_id,
        interaction_type = InteractionType.application_command,
        token = interaction_event_token,
    )
    
    expected_message_data = {
        'type': InteractionResponseType.source.value,
    }
    
    async def mock_api_interaction_response_message_create(
        input_interaction_event_id, input_interaction_event_token, input_message_data
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
        return {}
    
    api.interaction_response_message_create = mock_api_interaction_response_message_create
        
    try:
        output = await client.interaction_response_message_create(
            interaction_event,
        )
        vampytest.assert_true(mock_api_interaction_response_message_create_called)
        
        vampytest.assert_is(output, None)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_DEFERRED)
    finally:
        client._delete()
        client = None
