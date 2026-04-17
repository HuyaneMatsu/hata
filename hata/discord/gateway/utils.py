__all__ = ()

from .client_base import DiscordGatewayClientBase
from .client_shard import DiscordGatewayClientShard
from .client_sharder import DiscordGatewayClientSharder


def create_gateway(client):
    """
    Creates a gateway for the given count with the given shard count.
    
    Parameters
    ----------
    client : ``Client``
        The client to create the gateway for.
    
    Returns
    -------
    gateway : ``DiscordGatewayClientBase``
    """
    shard_count = client.shard_count
    if shard_count <= 1:
        gateway = DiscordGatewayClientShard(client, 0)
    else:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
    
    return gateway


def reshard_gateway(client):
    """
    Reshards the gateway to a new shard count. Trying to keep the existing instances as possible.
    
    Parameters
    ----------
    client : ``Client``
        The client to reshard its gateway of.
    
    Returns
    -------
    gateway : ``DiscordGatewayClientBase``
    """
    gateway = client.gateway
    shard_count = client.shard_count
    
    # Using shard gateway?
    if isinstance(gateway, DiscordGatewayClientShard):
        if shard_count <= 1:
            return gateway
        
        return DiscordGatewayClientSharder(client, shard_count, None)
    
    # Using sharder gateway?
    if isinstance(gateway, DiscordGatewayClientSharder):
        if shard_count <= 1:
            return gateway.get_gateway(0)
        
        return DiscordGatewayClientSharder(client, shard_count, gateway.gateways)
    
    # Default or unknown gateway type? Should not happen.
    return create_gateway(client) 
