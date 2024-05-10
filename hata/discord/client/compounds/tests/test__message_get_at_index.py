import vampytest

from ....channel import Channel
from ....message import Message
from ....utils import now_as_id

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_get_at_index():
    """
    Tests whether ``Client.message_get_at_index`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202405030000
    channel_id = 202405030001
    message_id_base = 202405031000
    index = 101
    channel = Channel.precreate(channel_id)
    
    messages = [Message.precreate(message_id_base + value, channel_id = channel_id) for value in reversed(range(0, 102))]
    
    
    mock_api_message_get_chunk_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    async def mock_api_message_get_chunk(input_channel_id, data):
        nonlocal mock_api_message_get_chunk_called
        nonlocal channel_id
        nonlocal message_id_base
        nonlocal index
        mock_api_message_get_chunk_called = True
        
        vampytest.assert_eq(input_channel_id, channel_id)
        
        before = int(data['before'])
        limit = data['limit']
        
        current_id = now_as_id()
        if (before > current_id - (1 << 26)) and (before < current_id + (1 << 26)):
            vampytest.assert_eq(limit, 100)
            area = slice(0, 0 + limit)
        else:
            vampytest.assert_eq(limit, 3)
            area = slice(100 - 1, 100  - 1 + limit)
        
        return [message.to_data(include_internals = True) for message in messages[area]]
    
    api.message_get_chunk = mock_api_message_get_chunk
        
    try:
        output = await client.message_get_at_index(channel, index)
        
        vampytest.assert_true(mock_api_message_get_chunk_called)
        vampytest.assert_is(output, messages[index])
    finally:
        client._delete()
        client = None
