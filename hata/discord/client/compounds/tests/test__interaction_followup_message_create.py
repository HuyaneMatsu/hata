import vampytest
from scarletio.web_common import FormData

from ....channel import Channel
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....interaction import InteractionEvent, InteractionType
from ....interaction.responding.constants import (
    RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING
)
from ....poll import Poll, PollAnswer
from ....message import Message, MessageFlag, MessageType

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__interaction_followup_message_create__stuffed():
    """
    Tests whether ``Client.interaction_followup_message_create`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403170024
    channel_id = 202403170024
    message_id = 202403170026
    attachment_id = 202403170028
    interaction_event_id = 202403170029
    interaction_event_token = 'yuyuko'
    
    mock_api_message_create_called = False
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
    interaction_event._response_flags = RESPONSE_FLAG_DEFERRED
    interaction_event._add_response_waiter()
    
    allowed_mentions = ['everyone']
    attachments = ('mister.txt', b'hey')
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    poll = Poll(answers = [PollAnswer(text = 'sister')], duration = 3600)
    silent = True
    tts = True
    show_for_invoking_user_only = True
    
    expected_message_data = FormData()
    expected_message_data.add_json(
        'payload_json',
        {
            'tts': True,
            'content': content,
            'embeds': [embed.to_data() for embed in embeds],
            'poll': poll.to_data(),
            'components': [create_row(components).to_data()],
            'allowed_mentions' : {'parse': ['everyone']},
            'flags': MessageFlag().update_by_keys(silent = True, invoking_user_only = True),
            'attachments': [{'id': '0'}],
        },
    )
    expected_message_data.add_field(
        f'files[{0}]', b'hey', file_name = 'mister.txt', content_type = 'application/octet-stream'
    )
    
    output_message_data = {
        'author': client.to_data(include_internals = True),
        'id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': None,
        'attachments': [{
            'id': str(attachment_id),
            'url': 'https://orindance.party/',
            'proxy_url': 'https://orindance.party/',
        }],
        'components': [create_row(components).to_data()],
        'content': content,
        'embeds': [embed.to_data() for embed in embeds],
        'poll': poll.to_data(),
        'flags': int(MessageFlag().update_by_keys(silent = True, invoking_user_only = True)),
        'tts': tts,
        'type': MessageType.default.value,
    }
    
    
    async def mock_interaction_followup_message_create(
        input_application_id, input_interaction_event_id, input_interaction_event_token, input_message_data
    ):
        nonlocal mock_api_message_create_called
        nonlocal client_id
        nonlocal expected_message_data
        nonlocal output_message_data
        nonlocal interaction_event_id
        nonlocal interaction_event_token
        nonlocal interaction_event
        mock_api_message_create_called = True
        vampytest.assert_eq(client_id, input_application_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(interaction_event_id, input_interaction_event_id)
        vampytest.assert_eq(interaction_event_token, input_interaction_event_token)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_DEFERRED | RESPONSE_FLAG_RESPONDING)
        return output_message_data
    
    api.interaction_followup_message_create = mock_interaction_followup_message_create
        
    try:
        output = await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            poll = poll,
            silent = silent,
            tts = tts,
            show_for_invoking_user_only = show_for_invoking_user_only,
        )
        vampytest.assert_true(mock_api_message_create_called)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDED)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, channel.messages)
        vampytest.assert_is(output.author, client)
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_eq(output.channel_id, channel_id)
        vampytest.assert_is_not(output.attachments, None)
        vampytest.assert_eq(output.attachments[0].id, attachment_id)
        vampytest.assert_is_not(output.components, None)
        vampytest.assert_eq(output.components[0], create_row(components))
        vampytest.assert_eq(output.content, content)
        vampytest.assert_eq(output.embeds, tuple(embeds))
        vampytest.assert_eq(output.poll, poll)
        vampytest.assert_eq(output.flags, MessageFlag().update_by_keys(silent = True, invoking_user_only = True))
        vampytest.assert_eq(output.tts, tts)
        vampytest.assert_is(output.type, MessageType.default)
        
        vampytest.assert_is(interaction_event.message, output)
    finally:
        client._delete()
        client = None


async def test__Client__interaction_followup_message_create__empty():
    """
    Tests whether ``Client.interaction_followup_message_create`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403170030
    channel_id = 202403170031
    interaction_event_id = 202403170032
    interaction_event_token = 'yuyuko'
    
    mock_api_message_create_called = False
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
    interaction_event._response_flags = RESPONSE_FLAG_DEFERRED
    interaction_event._add_response_waiter()
    
    async def mock_interaction_followup_message_create(
        input_application_id, input_interaction_event_id, input_interaction_event_token, input_message_data
    ):
        nonlocal mock_api_message_create_called
        mock_api_message_create_called = True
        return {}
    
    api.interaction_followup_message_create = mock_interaction_followup_message_create
        
    try:
        output = await client.interaction_followup_message_create(
            interaction_event,
        )
        vampytest.assert_false(mock_api_message_create_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
