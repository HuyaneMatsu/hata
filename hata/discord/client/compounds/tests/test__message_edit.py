import vampytest
from scarletio.web_common import FormData

from ....channel import Channel
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....message import Message, MessageFlag

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_edit__stuffed():
    """
    Tests whether ``Client.message_edit`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202303160011
    channel_id = 202303160012
    message_id = 202303160013
    
    mock_api_message_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
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
    
    async def mock_api_message_edit(input_channel_id, input_message_id, input_message_data):
        nonlocal mock_api_message_edit_called
        nonlocal channel_id
        nonlocal expected_message_data
        nonlocal message_id
        mock_api_message_edit_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(message_id, input_message_id)
        return {}
    
    api.message_edit = mock_api_message_edit
        
    try:
        output = await client.message_edit(
            message,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            suppress_embeds = suppress_embeds,
        )
        vampytest.assert_true(mock_api_message_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None


async def test__Client__message_edit__empty():
    """
    Tests whether ``Client.message_edit`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202303160014
    channel_id = 202303160015
    message_id = 202303160016
    
    mock_api_message_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    message = Message.precreate(message_id, channel = channel)
    
    async def mock_api_message_edit(input_channel_id, input_message_id, input_message_data):
        nonlocal mock_api_message_edit_called
        mock_api_message_edit_called = True
        return {}
    
    api.message_edit = mock_api_message_edit
        
    try:
        output = await client.message_edit(
            message,
        )
        vampytest.assert_false(mock_api_message_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
