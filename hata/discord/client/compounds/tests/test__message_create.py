import vampytest
from scarletio.web_common import FormData

from ....channel import Channel
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....message import Message, MessageFlag, MessageType
from ....sticker import Sticker, create_partial_sticker_data

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_create__stuffed():
    """
    Tests whether ``Client.message_create`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403160000
    channel_id = 202403160001
    message_id = 202403160002
    sticker_id = 202403160003
    attachment_id = 202403160004
    
    mock_api_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    sticker = Sticker.precreate(sticker_id, name = 'miau')
    
    allowed_mentions = ['everyone']
    attachments = ('mister.txt', b'hey')
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    enforce_nonce = True
    nonce = 'okuu'
    stickers = [sticker]
    silent = True
    tts = True
    
    expected_message_data = FormData()
    expected_message_data.add_json(
        'payload_json',
        {
            'enforce_nonce': enforce_nonce,
            'nonce': nonce,
            'tts': True,
            'content': content,
            'embeds': [embed.to_data() for embed in embeds],
            'components': [create_row(components).to_data()],
            'allowed_mentions' : {'parse': ['everyone']},
            'sticker_ids': [str(sticker.id) for sticker in stickers],
            'flags': MessageFlag().update_by_keys(silent = True),
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
        'nonce': nonce,
        'sticker_items': [
            create_partial_sticker_data(sticker) for sticker in stickers
        ],
        'flags': int(MessageFlag().update_by_keys(silent = True)),
        'tts': tts,
        'type': MessageType.default.value,
    }
    
    
    async def mock_api_message_create(input_channel_id, input_message_data):
        nonlocal mock_api_message_create_called
        nonlocal channel_id
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_message_create_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        return output_message_data
    
    api.message_create = mock_api_message_create
        
    try:
        output = await client.message_create(
            channel,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            enforce_nonce = enforce_nonce,
            nonce = nonce,
            stickers = stickers,
            silent = silent,
            tts = tts,
        )
        vampytest.assert_true(mock_api_message_create_called)
        
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
        vampytest.assert_eq(output.nonce, nonce)
        vampytest.assert_eq(output.stickers, tuple(stickers))
        vampytest.assert_eq(output.flags, MessageFlag().update_by_keys(silent = True))
        vampytest.assert_eq(output.tts, tts)
        vampytest.assert_is(output.type, MessageType.default)
    finally:
        client._delete()
        client = None


async def test__Client__message_create__empty():
    """
    Tests whether ``Client.message_create`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403160005
    channel_id = 202403160006
    
    mock_api_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    
    async def mock_api_message_create(input_channel_id, input_message_data):
        nonlocal mock_api_message_create_called
        mock_api_message_create_called = True
        return {}
    
    api.message_create = mock_api_message_create
        
    try:
        output = await client.message_create(
            channel,
        )
        vampytest.assert_false(mock_api_message_create_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None


async def test__Client__message_create__reply():
    """
    Tests whether ``Client.message_create`` works as intended.
    
    Case: reply.
    
    This function is a coroutine.
    """
    client_id = 202403160007
    channel_id = 202403160008
    reply_message_id = 202403160009
    message_id = 202403160010
    
    mock_api_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    reply_message = Message.precreate(reply_message_id, channel = channel)
    
    content = 'orin'
    
    expected_message_data = {
        'content': content,
        'message_reference': {
            'message_id': str(reply_message_id),
        },
    }
    
    output_message_data = {
        'id': str(message_id),
        'author': client.to_data(include_internals = True),
        'channel_id': str(channel_id),
        'guild_id': None,
        'content': content,
        'type': MessageType.inline_reply.value,
        'message_reference': reply_message.to_message_reference_data(),
    }
    
    
    async def mock_api_message_create(input_channel_id, input_message_data):
        nonlocal mock_api_message_create_called
        nonlocal channel_id
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_message_create_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        return output_message_data
    
    api.message_create = mock_api_message_create
        
    try:
        output = await client.message_create(
            reply_message,
            content = 'orin',
        )
        vampytest.assert_true(mock_api_message_create_called)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, channel.messages)
        vampytest.assert_is(output.author, client)
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_is(output.referenced_message, reply_message)
        vampytest.assert_eq(output.content, content)
        vampytest.assert_eq(output.type, MessageType.inline_reply)
        
    finally:
        client._delete()
        client = None
