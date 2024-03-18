import vampytest
from scarletio.web_common import FormData

from ....channel import Channel
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....interaction import InteractionEvent, InteractionType
from ....interaction.responding.constants import RESPONSE_FLAG_RESPONDED
from ....message import Message, MessageFlag, MessageType

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__interaction_followup_message_edit__stuffed():
    """
    Tests whether ``Client.interaction_followup_message_edit`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403170033
    channel_id = 202403170034
    message_id = 202403170035
    attachment_id = 202403170036
    interaction_event_id = 202403170038
    interaction_event_token = 'yuyuko'
    
    mock_api_message_edit_called = False
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
    interaction_event._response_flags = RESPONSE_FLAG_RESPONDED
    interaction_event._add_response_waiter()
    message = Message.precreate(message_id, channel = channel)
    
    allowed_mentions = ['everyone']
    attachments = ('mister.txt', b'hey')
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    suppress_embeds = True
    
    expected_message_data = FormData()
    expected_message_data.add_json(
        'payload_json',
        {
            'content': content,
            'embeds': [embed.to_data() for embed in embeds],
            'components': [create_row(components).to_data()],
            'allowed_mentions' : {'parse': ['everyone']},
            'flags': MessageFlag().update_by_keys(embeds_suppressed = True),
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
        'flags': int(MessageFlag().update_by_keys(embeds_suppressed = True)),
        'type': MessageType.default.value,
    }
    
    
    async def mock_interaction_followup_message_edit(
        input_application_id,
        input_interaction_event_id,
        input_interaction_event_token,
        input_message_id,
        input_message_data,
    ):
        nonlocal mock_api_message_edit_called
        nonlocal client_id
        nonlocal expected_message_data
        nonlocal output_message_data
        nonlocal interaction_event_id
        nonlocal interaction_event_token
        nonlocal interaction_event
        nonlocal message_id
        mock_api_message_edit_called = True
        vampytest.assert_eq(client_id, input_application_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(interaction_event_id, input_interaction_event_id)
        vampytest.assert_eq(interaction_event_token, input_interaction_event_token)
        vampytest.assert_eq(message_id, input_message_id)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDED)
        return output_message_data
    
    api.interaction_followup_message_edit = mock_interaction_followup_message_edit
        
    try:
        output = await client.interaction_followup_message_edit(
            interaction_event,
            message,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            suppress_embeds = suppress_embeds,
        )
        vampytest.assert_true(mock_api_message_edit_called)
        vampytest.assert_eq(interaction_event._response_flags, RESPONSE_FLAG_RESPONDED)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None


async def test__Client__interaction_followup_message_edit__empty():
    """
    Tests whether ``Client.interaction_followup_message_edit`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403170039
    message_id = 202403170040
    channel_id = 202403170041
    interaction_event_id = 202403170042
    interaction_event_token = 'yuyuko'
    
    mock_api_message_edit_called = False
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
    interaction_event._response_flags = RESPONSE_FLAG_RESPONDED
    message = Message.precreate(message_id)
    
    async def mock_interaction_followup_message_edit(
        input_application_id,
        input_interaction_event_id,
        input_interaction_event_token,
        input_message_id,
        input_message_data,
    ):
        nonlocal mock_api_message_edit_called
        mock_api_message_edit_called = True
        return {}
    
    api.interaction_followup_message_edit = mock_interaction_followup_message_edit
        
    try:
        output = await client.interaction_followup_message_edit(
            interaction_event,
            message,
        )
        vampytest.assert_false(mock_api_message_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
