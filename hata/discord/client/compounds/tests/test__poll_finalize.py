import vampytest

from ....channel import Channel
from ....message import Message

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__poll_finalize__stuffed():
    """
    Tests whether ``Client.poll_finalize`` works as intended.
    
    Case: stuffed message.
    
    This function is a coroutine.
    """
    client_id = 202404210033
    channel_id = 202404210034
    message_id = 202404210035
    
    mock_api_poll_finalize_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id)
    message = Message.precreate(message_id, channel = channel)
    
    async def mock_api_poll_finalize(input_channel_id, input_message_id):
        nonlocal mock_api_poll_finalize_called
        nonlocal channel_id
        nonlocal message_id
        mock_api_poll_finalize_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(message_id, input_message_id)
        return {}
    
    api.poll_finalize = mock_api_poll_finalize
        
    try:
        output = await client.poll_finalize(
            message,
        )
        vampytest.assert_true(mock_api_poll_finalize_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
