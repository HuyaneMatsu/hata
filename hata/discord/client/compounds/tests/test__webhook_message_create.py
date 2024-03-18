import vampytest
from scarletio.web_common import FormData

from ....channel import Channel, ChannelType, ForumTag
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....message import Message, MessageFlag, MessageType
from ....webhook import Webhook, WebhookRepr

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__webhook_message_create__stuffed_message():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403160020
    channel_id = 202403160021
    message_id = 202403160022
    attachment_id = 202403160024
    webhook_id = 202403160031
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    
    allowed_mentions = ['everyone']
    attachments = ('mister.txt', b'hey')
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    silent = True
    tts = True
    
    expected_message_data = FormData()
    expected_message_data.add_json(
        'payload_json',
        {
            'tts': True,
            'content': content,
            'embeds': [embed.to_data() for embed in embeds],
            'components': [create_row(components).to_data()],
            'allowed_mentions' : {'parse': ['everyone']},
            'flags': MessageFlag().update_by_keys(silent = True),
            'attachments': [{'id': '0'}],
        },
    )
    expected_message_data.add_field(
        f'files[{0}]', b'hey', file_name = 'mister.txt', content_type = 'application/octet-stream'
    )
    
    output_message_data = {
        'id': str(message_id),
        'channel_id': str(channel_id),
        'author': webhook.to_data(include_internals = True),
        'guild_id': None,
        'attachments': [{
            'id': str(attachment_id),
            'url': 'https://orindance.party/',
            'proxy_url': 'https://orindance.party/',
        }],
        'components': [create_row(components).to_data()],
        'content': content,
        'embeds': [embed.to_data() for embed in embeds],
        'flags': int(MessageFlag().update_by_keys(silent = True)),
        'tts': tts,
        'type': MessageType.default.value,
        'webhook_id': str(webhook_id),
    }
    
    
    async def mock_api_webhook_message_create(input_webhook_id, input_webhook_token, input_message_data, input_query_parameters):
        nonlocal mock_api_webhook_message_create_called
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_webhook_message_create_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq({'wait': True}, input_query_parameters)
        return output_message_data
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            silent = silent,
            tts = tts,
            wait = True,
        )
        vampytest.assert_true(mock_api_webhook_message_create_called)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, channel.messages)
        vampytest.assert_eq(output.author, webhook)
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_eq(output.channel_id, channel_id)
        vampytest.assert_is_not(output.attachments, None)
        vampytest.assert_eq(output.attachments[0].id, attachment_id)
        vampytest.assert_is_not(output.components, None)
        vampytest.assert_eq(output.components[0], create_row(components))
        vampytest.assert_eq(output.content, content)
        vampytest.assert_eq(output.embeds, tuple(embeds))
        vampytest.assert_eq(output.flags, MessageFlag().update_by_keys(silent = True))
        vampytest.assert_eq(output.tts, tts)
        vampytest.assert_is(output.type, MessageType.default)
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_create__empty():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403160025
    channel_id = 202403160026
    webhook_id = 202403160031
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    
    async def mock_api_webhook_message_create(input_channel_id, input_message_data):
        nonlocal mock_api_webhook_message_create_called
        mock_api_webhook_message_create_called = True
        return {}
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
        )
        vampytest.assert_false(mock_api_webhook_message_create_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_create__stuffed_webhook():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: stuffed webhook.
    
    This function is a coroutine.
    """
    client_id = 202403160034
    channel_id = 202403160035
    message_id = 202403160037
    webhook_id = 202403160036
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    
    content = 'suika'
    name = 'flandre'
    avatar_url = 'https://orindance.party/'
    
    
    expected_message_data = {
        'content': content,
        'name': name,
        'avatar_url': avatar_url,
    }
    
    output_message_data = {
        'id': str(message_id),
        'channel_id': str(channel_id),
        'author': {
            'name': name,
            'id': webhook_id,
        },
        'guild_id': None,
        'content': content,
        'webhook_id': str(webhook_id),
    }
    
    
    async def mock_api_webhook_message_create(input_webhook_id, input_webhook_token, input_message_data, input_query_parameters):
        nonlocal mock_api_webhook_message_create_called
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_webhook_message_create_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq({'wait': True}, input_query_parameters)
        return output_message_data
    
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
            content = content,
            name = name,
            avatar_url = avatar_url,
            wait = True,
        )
        vampytest.assert_true(mock_api_webhook_message_create_called)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, channel.messages)
        
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_instance(output.author, WebhookRepr)
        vampytest.assert_eq(output.author.id, webhook_id)
        vampytest.assert_eq(output.author.name, name)
        vampytest.assert_eq(output.content, content)
        vampytest.assert_is(output.type, MessageType.default)
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_create__create_thread():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: create thread.
    
    This function is a coroutine.
    """
    client_id = 202403160040
    channel_id = 202403160041
    message_id = 202403160042
    tag_id = 202403160044
    thread_id = 202403160045
    webhook_id = 202403160043
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    tag = ForumTag.precreate(tag_id)
    
    content = 'suika'
    thread_name = 'inaba'
    applied_tags = [tag]
    
    
    expected_message_data = {
        'content': content,
        'thread_name': thread_name,
        'applied_tags': [str(tag.id) for tag in applied_tags],
    }
    
    output_message_data = {
        'id': str(message_id),
        'channel_id': str(channel_id),
        'thread': {
            'name': thread_name,
            'id': str(thread_id),
            'applied_tags': [str(tag.id) for tag in applied_tags],
            'parent_id': str(channel_id),
            'type': ChannelType.guild_thread_public.value,
        },
        'guild_id': None,
        'content': content,
        'webhook_id': str(webhook_id),
    }
    
    
    async def mock_api_webhook_message_create(input_webhook_id, input_webhook_token, input_message_data, input_query_parameters):
        nonlocal mock_api_webhook_message_create_called
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_webhook_message_create_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq({'wait': True}, input_query_parameters)
        return output_message_data
    
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
            content = content,
            thread_name = thread_name,
            applied_tags = applied_tags,
            wait = True,
        )
        vampytest.assert_true(mock_api_webhook_message_create_called)
        
        vampytest.assert_instance(output, Message)
        
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_is(output.author, webhook)
        vampytest.assert_eq(output.content, content)
        vampytest.assert_is(output.type, MessageType.default)
        
        thread = output.thread
        vampytest.assert_is_not(thread, None)
        vampytest.assert_true(channel.is_in_group_thread())
        vampytest.assert_eq(thread.name, thread_name)
        vampytest.assert_eq(thread.applied_tags, tuple(applied_tags))
        vampytest.assert_in(output, thread.messages)
        
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_create__create_into_thread():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: create into thread.
    
    This function is a coroutine.
    """
    client_id = 202403160046
    channel_id = 202403160047
    message_id = 202403160048
    thread_id = 202403160050
    webhook_id = 202403160051
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    thread = Channel.precreate(thread_id, channel_type = ChannelType.guild_thread_public)
    
    content = 'suika'
    
    
    expected_message_data = {
        'content': content,
    }
    
    output_message_data = {
        'id': str(message_id),
        'channel_id': str(thread_id),
        'guild_id': None,
        'content': content,
        'webhook_id': str(webhook_id),
    }
    
    
    async def mock_api_webhook_message_create(input_webhook_id, input_webhook_token, input_message_data, input_query_parameters):
        nonlocal mock_api_webhook_message_create_called
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data
        nonlocal output_message_data
        nonlocal thread_id
        mock_api_webhook_message_create_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq({'wait': True, 'thread_id': str(thread_id)}, input_query_parameters)
        return output_message_data
    
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
            content = content,
            thread = thread,
            wait = True,
        )
        vampytest.assert_true(mock_api_webhook_message_create_called)
        
        vampytest.assert_instance(output, Message)
        vampytest.assert_in(output, thread.messages)
        
        vampytest.assert_eq(output.id, message_id)
        vampytest.assert_is(output.author, webhook)
        vampytest.assert_eq(output.content, content)
        vampytest.assert_is(output.type, MessageType.default)
        
    finally:
        client._delete()
        client = None


async def test__Client__webhook_message_create__no_wait():
    """
    Tests whether ``Client.webhook_message_create`` works as intended.
    
    Case: no wait.
    
    This function is a coroutine.
    """
    client_id = 202403160052
    channel_id = 202403160053
    webhook_id = 202403160054
    webhook_token = 'reisen'
    
    mock_api_webhook_message_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    webhook = Webhook.precreate(webhook_id, token = webhook_token, channel = channel)
    
    content = 'inaba'
    
    expected_message_data = {
        'content': content,
    }
    
    output_message_data = None
    
    
    async def mock_api_webhook_message_create(input_webhook_id, input_webhook_token, input_message_data, input_query_parameters):
        nonlocal mock_api_webhook_message_create_called
        nonlocal webhook_id
        nonlocal webhook_token
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_webhook_message_create_called = True
        vampytest.assert_eq(webhook_id, input_webhook_id)
        vampytest.assert_eq(webhook_token, input_webhook_token)
        vampytest.assert_eq(expected_message_data, input_message_data)
        vampytest.assert_eq(None, input_query_parameters)
        return output_message_data
    
    api.webhook_message_create = mock_api_webhook_message_create
        
    try:
        output = await client.webhook_message_create(
            webhook,
            content = content,
        )
        vampytest.assert_true(mock_api_webhook_message_create_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
