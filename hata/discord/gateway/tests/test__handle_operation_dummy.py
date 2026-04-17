import vampytest

from ...client import Client
from ...voice import VoiceClient

from ..constants import GATEWAY_ACTION_KEEP_GOING
from ..voice import _handle_operation_dummy, DiscordGatewayVoice


async def test__handle_operation_dummy():
    """
    Tests whether ``_handle_operation_dummy`` works as intended.
    
    Case: No kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210024',
        client_id = 202401210025,
    )
    
    data = None
    
    try:
        voice_client = VoiceClient(client, 202401210026, 202401210027)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await _handle_operation_dummy(gateway, data)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
    finally:
        client._delete()
        client = None
