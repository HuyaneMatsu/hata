import vampytest

from ...client import Client
from ...core import KOKORO

from ..client_shard import DiscordGatewayClientShard
from ..client_sharder import _close_and_abort_gateway

from .helpers_websocket_client import TestWebSocketClient


async def test__close_and_abort_gateway__decrease():
    """
    Tests whether ``_close_and_abort_gateway`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140006',
        client_id = 202301140007,
    )
    
    try:
        gateway = DiscordGatewayClientShard(client, 0)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway._should_run = True
        gateway.websocket = await TestWebSocketClient(KOKORO, None)
        
        await _close_and_abort_gateway(gateway)
        
        vampytest.assert_is(gateway.kokoro.runner, None)
        vampytest.assert_eq(gateway._should_run, False)
        vampytest.assert_is(gateway.websocket, None)
    
    finally:
        client._delete()
        client = None
