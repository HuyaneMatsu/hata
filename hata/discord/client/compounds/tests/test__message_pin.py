import vampytest

from ....message import Message

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_pin__stuffed():
    """
    Tests whether ``Client.message_pin`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202511080000
    channel_id = 202511080001
    message_id = 202511080002
    
    mock_api_message_pin_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
    )
    reason = 'hey mister'
    
    async def mock_api_message_pin(input_channel_id, input_message_id, input_reason):
        nonlocal mock_api_message_pin_called
        nonlocal channel_id
        nonlocal message_id
        nonlocal reason
        
        mock_api_message_pin_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(message_id, input_message_id)
        vampytest.assert_eq(input_reason, reason)
        
        return None
    
    api.message_pin = mock_api_message_pin
        
    try:
        output = await client.message_pin(
            message,
            reason = reason,
        )
        vampytest.assert_true(mock_api_message_pin_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
