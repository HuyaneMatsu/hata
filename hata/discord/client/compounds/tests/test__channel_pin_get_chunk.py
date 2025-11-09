from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....message import Message, MessagePin
from ....utils import datetime_to_timestamp

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__channel_pin_get_chunk__stuffed():
    """
    Tests whether ``Client.channel_pin_get_chunk`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202511080020
    channel_id = 202511080021
    
    mock_api_channel_pin_get_chunk_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
    )
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    before = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    limit = 49
    
    chunk_0 = [
        MessagePin(
            message = Message.precreate(
                202511080022,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        ),
        MessagePin(
            message = Message.precreate(
                202511080023,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 16, tzinfo = TimeZone.utc),
        )
    ]
    
    async def mock_api_channel_pin_get_chunk(input_channel_id, input_data):
        nonlocal mock_api_channel_pin_get_chunk_called
        nonlocal channel_id
        nonlocal limit
        nonlocal chunk_0
        
        mock_api_channel_pin_get_chunk_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(
            input_data,
            {
                'after': datetime_to_timestamp(after),
                'before': datetime_to_timestamp(before),
                'limit': limit,
            },
        )
        
        return {
            'items': [message_pin.to_data() for message_pin in chunk_0],
            'has_more': True,
        }
    
    api.channel_pin_get_chunk = mock_api_channel_pin_get_chunk
        
    try:
        output = await client.channel_pin_get_chunk(
            channel,
            after = after,
            before = before,
            limit = limit,
        )
        vampytest.assert_instance(output, list)
        for element in output:
            vampytest.assert_instance(element, MessagePin)
        
        vampytest.assert_true(mock_api_channel_pin_get_chunk_called)
        
        vampytest.assert_eq(output, chunk_0)
    finally:
        client._delete()
        client = None
