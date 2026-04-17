from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....message import Message, MessagePin
from ....utils import DISCORD_EPOCH_START, datetime_to_timestamp

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__channel_pin_get_all__stuffed():
    """
    Tests whether ``Client.channel_pin_get_chunk`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202511080030
    channel_id = 202511080031
    
    mock_api_channel_pin_get_chunk_called = 0
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
                202511080032,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        ),
        MessagePin(
            message = Message.precreate(
                202511080033,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 16, tzinfo = TimeZone.utc),
        ),
    ]
    
    chunk_1 = [
        MessagePin(
            message = Message.precreate(
                202511080034,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 17, tzinfo = TimeZone.utc),
        ),
        MessagePin(
            message = Message.precreate(
                202511080035,
                channel_id = channel_id,
            ),
            pinned_at = DateTime(2016, 5, 18, tzinfo = TimeZone.utc),
        ),
    ]
    
    async def mock_api_channel_pin_get_chunk(input_channel_id, input_data):
        nonlocal mock_api_channel_pin_get_chunk_called
        nonlocal channel_id
        nonlocal limit
        nonlocal chunk_0
        nonlocal chunk_1
        
        vampytest.assert_eq(channel_id, input_channel_id)
        
        if mock_api_channel_pin_get_chunk_called > 1:
            raise RuntimeError
        
        if mock_api_channel_pin_get_chunk_called == 0:
            expected_input_data = {
                'after': datetime_to_timestamp(DISCORD_EPOCH_START),
            }
        
        else:
            expected_input_data = {
                'after': datetime_to_timestamp(chunk_0[-1].pinned_at),
            }
            
        vampytest.assert_eq(
            input_data,
            expected_input_data,
        )
        
        if mock_api_channel_pin_get_chunk_called == 0:
            output_data = {
                'items': [message_pin.to_data() for message_pin in chunk_0],
                'has_more': True,
            }
        else:
            output_data = {
                'items': [message_pin.to_data() for message_pin in chunk_1],
                'has_more': False,
            }
        
        mock_api_channel_pin_get_chunk_called += 1
        
        return output_data
    
    api.channel_pin_get_chunk = mock_api_channel_pin_get_chunk
        
    try:
        output = await client.channel_pin_get_all(
            channel,
        )
        vampytest.assert_instance(output, list)
        for element in output:
            vampytest.assert_instance(element, MessagePin)
        
        vampytest.assert_eq(mock_api_channel_pin_get_chunk_called, 2)
        
        vampytest.assert_eq(output, [*chunk_0, *chunk_1])
    finally:
        client._delete()
        client = None
