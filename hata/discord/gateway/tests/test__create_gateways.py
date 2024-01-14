import vampytest

from ...client import Client

from ..client_shard import DiscordGatewayClientShard
from ..client_sharder import _create_gateways


def test__create_gateways__nothing():
    """
    Tests whether ``_create_gateways`` works as intended.
    
    Case: Nothing given.
    """
    client = Client(
        'token_202301140000',
        client_id = 202301140001,
    )
    
    shard_count = 4
    
    try:
        output = _create_gateways(client, shard_count, None)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), shard_count)
        
        for index, gateway in enumerate(output):
            vampytest.assert_instance(gateway, DiscordGatewayClientShard)
            vampytest.assert_eq(gateway.shard_id, index)
        
    finally:
        client._delete()
        client = None


def test__create_gateways__increase():
    """
    Tests whether ``_create_gateways`` works as intended.
    
    Case: Increase gateway count.
    """
    client = Client(
        'token_202301140002',
        client_id = 202301140003,
    )
    
    shard_count = 4
    
    try:
        gateways = (
            DiscordGatewayClientShard(client, 0),
            DiscordGatewayClientShard(client, 1),
        )
        output = _create_gateways(client, shard_count, gateways)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), shard_count)
        
        for index, gateway in enumerate(output):
            vampytest.assert_instance(gateway, DiscordGatewayClientShard)
            vampytest.assert_eq(gateway.shard_id, index)
        
        for gateway_0, gateway_1 in zip(gateways, output):
            vampytest.assert_is(gateway_0, gateway_1)
        
    finally:
        client._delete()
        client = None


def test__create_gateways__decrease():
    """
    Tests whether ``_create_gateways`` works as intended.
    
    Case: Decrease gateway count.
    """
    client = Client(
        'token_202301140004',
        client_id = 202301140005,
    )
    
    shard_count = 2
    
    try:
        gateways = (
            DiscordGatewayClientShard(client, 0),
            DiscordGatewayClientShard(client, 1),
            DiscordGatewayClientShard(client, 2),
            DiscordGatewayClientShard(client, 3),
        )
        output = _create_gateways(client, shard_count, gateways)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), shard_count)
        
        for index, gateway in enumerate(output):
            vampytest.assert_instance(gateway, DiscordGatewayClientShard)
            vampytest.assert_eq(gateway.shard_id, index)
        
        for gateway_0, gateway_1 in zip(gateways, output):
            vampytest.assert_is(gateway_0, gateway_1)
        
    finally:
        client._delete()
        client = None
