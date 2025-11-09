import vampytest

from ....message import Message

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__message_unpin__stuffed():
    """
    Tests whether ``Client.message_unpin`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202511080010
    channel_id = 202511080011
    message_id = 202511080012
    
    mock_api_message_unpin_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
    )
    reason = 'hey mister'
    
    async def mock_api_message_unpin(input_channel_id, input_message_id, input_reason):
        nonlocal mock_api_message_unpin_called
        nonlocal channel_id
        nonlocal message_id
        nonlocal reason
        
        mock_api_message_unpin_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(message_id, input_message_id)
        vampytest.assert_eq(input_reason, reason)
        
        return None
    
    api.message_unpin = mock_api_message_unpin
        
    try:
        output = await client.message_unpin(
            message,
            reason = reason,
        )
        vampytest.assert_true(mock_api_message_unpin_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
