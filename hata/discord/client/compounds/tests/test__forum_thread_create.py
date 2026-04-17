import vampytest
from scarletio.web_common import FormData

from ....channel import Channel, ChannelFlag, ChannelType, ForumTag
from ....component import Component, ComponentType, create_row
from ....embed import Embed
from ....message import Message, MessageFlag, MessageType
from ....sticker import Sticker, create_partial_sticker_data

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__forum_thread_create__stuffed():
    """
    Tests whether ``Client.forum_thread_create`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202403160070
    channel_id = 202403160071
    message_id = 202403160072
    sticker_id = 202403160073
    attachment_id = 202403160074
    tag_id = 202403160075
    thread_id = 202403160076
    
    mock_api_thread_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_forum)
    sticker = Sticker.precreate(sticker_id, name = 'miau')
    tag = ForumTag.precreate(tag_id)
    
    allowed_mentions = ['everyone']
    attachments = ('mister.txt', b'hey')
    components = Component(ComponentType.button, label = 'koishi', custom_id = 'satori')
    content = 'suika'
    embeds = [Embed('orin')]
    nonce = 'okuu'
    stickers = [sticker]
    silent = True
    tts = True
    
    name = 'inaba'
    applied_tags = [tag]
    auto_archive_after = 86400
    flags = ChannelFlag(45)
    invitable = False
    open_ = False
    slowmode = 3600
    
    expected_message_data = FormData()
    expected_message_data.add_json(
        'payload_json',
        {
            'rate_limit_per_user': slowmode,
            'locked': not open_,
            'invitable': invitable,
            'flags': int(flags),
            'auto_archive_duration': auto_archive_after // 60,
            'applied_tags': [str(tag.id) for tag in applied_tags],
            'name': name,
            'message': {
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
        },
    )
    expected_message_data.add_field(
        f'files[{0}]', b'hey', file_name = 'mister.txt', content_type = 'application/octet-stream'
    )
    
    output_message_data = {
        'name': name,
        'id': str(thread_id),
        'applied_tags': [str(tag.id) for tag in applied_tags],
        'parent_id': str(channel_id),
        'type': ChannelType.guild_thread_public.value,
        'thread_metadata': {
            'auto_archive_duration': auto_archive_after // 60,
            'invitable': invitable,
            'locked': not open_,
        },
        'flags': int(flags),
        'rate_limit_per_user': slowmode,
        'message': {
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
        },
    }
    
    
    async def mock_api_thread_create(input_channel_id, input_message_data):
        nonlocal mock_api_thread_create_called
        nonlocal channel_id
        nonlocal expected_message_data
        nonlocal output_message_data
        mock_api_thread_create_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_message_data, input_message_data)
        return output_message_data
    
    api.thread_create = mock_api_thread_create
        
    try:
        output = await client.forum_thread_create(
            channel,
            allowed_mentions = allowed_mentions,
            attachments = attachments,
            components = components,
            content = content,
            embeds = embeds,
            nonce = nonce,
            stickers = stickers,
            silent = silent,
            tts = tts,
            name = name,
            applied_tags = applied_tags,
            auto_archive_after = auto_archive_after,
            flags = flags,
            invitable = invitable,
            open_ = open_,
            slowmode = slowmode,
        )
        vampytest.assert_true(mock_api_thread_create_called)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        
        output_0, output_1 = output
        
        vampytest.assert_instance(output_0, Channel)
        vampytest.assert_eq(output_0.id, thread_id)
        vampytest.assert_eq(output_0.name, name)
        vampytest.assert_eq(output_0.parent_id, channel_id)
        vampytest.assert_is(output_0.type, ChannelType.guild_thread_public)
        vampytest.assert_eq(output_0.auto_archive_after, auto_archive_after)
        vampytest.assert_eq(output_0.flags, flags)
        # public threads actually dont have this field
        # vampytest.assert_eq(output_0.invitable, invitable)
        vampytest.assert_eq(output_0.open, open_)
        vampytest.assert_eq(output_0.slowmode, slowmode)
        
        vampytest.assert_instance(output_1, Message)
        vampytest.assert_in(output_1, output_0.messages)
        vampytest.assert_is(output_1.author, client)
        vampytest.assert_eq(output_1.id, message_id)
        vampytest.assert_eq(output_1.channel_id, channel_id)
        vampytest.assert_is_not(output_1.attachments, None)
        vampytest.assert_eq(output_1.attachments[0].id, attachment_id)
        vampytest.assert_is_not(output_1.components, None)
        vampytest.assert_eq(output_1.components[0], create_row(components))
        vampytest.assert_eq(output_1.content, content)
        vampytest.assert_eq(output_1.embeds, tuple(embeds))
        vampytest.assert_eq(output_1.nonce, nonce)
        vampytest.assert_eq(output_1.stickers, tuple(stickers))
        vampytest.assert_eq(output_1.flags, MessageFlag().update_by_keys(silent = True))
        vampytest.assert_eq(output_1.tts, tts)
        vampytest.assert_is(output_1.type, MessageType.default)
    finally:
        client._delete()
        client = None


async def test__Client__forum_thread_create__empty():
    """
    Tests whether ``Client.forum_thread_create`` works as intended.
    
    Case: empty.
    
    This function is a coroutine.
    """
    client_id = 202403160077
    channel_id = 202403160078
    
    mock_api_thread_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_forum)
    
    async def mock_api_thread_create(input_channel_id, input_message_data):
        nonlocal mock_api_thread_create_called
        mock_api_thread_create_called = True
        return {}
    
    api.thread_create = mock_api_thread_create
        
    try:
        output = await client.forum_thread_create(
            channel,
        )
        vampytest.assert_false(mock_api_thread_create_called)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        
        output_0, output_1 = output
        vampytest.assert_is(output_0, None)
        vampytest.assert_is(output_1, None)
    finally:
        client._delete()
        client = None
