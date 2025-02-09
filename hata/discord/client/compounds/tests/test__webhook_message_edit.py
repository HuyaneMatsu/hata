import vampytest
from scarletio.web_common import FormData

from ....channel import Channel
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....message import Message, MessageFlag
from ....webhook import Webhook

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__webhook_message_edit__stuffed():
    """
    Tests whether ``Client.webhook_message_edit`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403160060
    channel_id = 202403160061
    message_id = 202403160062
    webhook_id = 202403160063
    webhook_token = 'reisen'
    
    mock_api_webhook_message_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    message = Message.precreate(message_id, channel = channel, author = webhook)
    
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
    
    async def mock_api_webhook_message_edit(
        input_webhook_id, input_webhook_token, input_message_id, input_message_data, input_query
    ):
        nonlocal mock_api_webhook_message_edit_called
        nonlocal webhook_id
        nonlocal expected_message_data
        nonlocal message_id
        nonlocal webhook_token
        mock_api_webhook_message_edit_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(message_id, input_message_id)
        vampytest.assert_eq({'with_components': True}, input_query)
        return {}
    
    api.webhook_message_edit = mock_api_webhook_message_edit
        
    try:
        output = await client.webhook_message_edit(
            webhook,
            message,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            suppress_embeds = suppress_embeds,
        )
        vampytest.assert_true(mock_api_webhook_message_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_edit__empty():
    """
    Tests whether ``Client.webhook_message_edit`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403160064
    channel_id = 202403160065
    message_id = 202403160066
    webhook_id = 202403160067
    webhook_token = 'reisen'
    
    mock_api_webhook_message_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    message = Message.precreate(message_id, channel = channel, author = webhook)
    
    async def mock_api_webhook_message_edit(input_webhook_id, input_webhook_token, input_message_id, input_message_data):
        nonlocal mock_api_webhook_message_edit_called
        mock_api_webhook_message_edit_called = True
        return {}
    
    api.webhook_message_edit = mock_api_webhook_message_edit
        
    try:
        output = await client.webhook_message_edit(
            webhook,
            message,
        )
        vampytest.assert_false(mock_api_webhook_message_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
