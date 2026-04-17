__all__ = ()

from itertools import islice

from scarletio import Task, TaskGroup, copy_docs, sleep, to_json

from ..core import KOKORO

from .client_base import DiscordGatewayClientBase
from .client_shard import DiscordGatewayClientShard
from .heartbeat import LATENCY_DEFAULT


def _create_gateways(client, shard_count, gateways):
    """
    Creates the amount of gateways requested.
    
    Parameters
    ----------
    client : ``Client``
        The client to create the gateways for.
    shard_count : `int`
        The amount of gateways to return.
        Should be greater than `1` and must be greater than `0`.
    gateways : `None | tuple<DiscordGatewayClientShard>`
        Already existing gateways to use.
    
    Returns
    -------
    gateways : `tuple<DiscordGatewayClientShard>`
    """
    # Process input
    if gateways is None:
        gateways = []
    else:
        gateways = [*gateways]
    
    gateway_count = len(gateways)
    
    # Adjust gateway count
    if shard_count == gateway_count:
        # nothing to do, should not happen
        pass
    
    elif shard_count > gateway_count:
        # Add new gateways
        gateways.extend(DiscordGatewayClientShard(client, shard_id) for shard_id in range(gateway_count, shard_count))
    
    else:
        # Remove extra gateways
        for _ in range(shard_count, gateway_count):
            gateways.pop().abort()
    
    # return
    return tuple(gateways)


async def _close_and_abort_gateway(gateway):
    """
    Closes and aborts the gateway.
    
    This function is a coroutine.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayClientShard``
        The gateway to stop.
    """
    try:
        await gateway.close()
    finally:
        gateway.abort()


async def _connect_gateway_batch(task_group, gateways):
    """
    Connects a batch of gateways.
    
    Parameters
    ----------
    task_group : ``TaskGroup``
        Task group to use for waiters and the runner tasks.
    gateways : `iterable<DiscordGatewayClientShard>`
        The gateways to run.
    
    Returns
    -------
    success : `bool`
    """
    batch_size = 0
    
    # Add gateways
    for gateway in gateways:
        future = task_group.create_future()
        task_group.create_task(gateway.run(future))
        
        batch_size += 1
    
    # Wait for connection waiters. These always have result of `True` on success. While `False` on failure.
    # If a `.runner` ends it also results in `False`. Like this we do not need to differentiate between them..
    while batch_size:
        done_future = await task_group.wait_first_and_pop()
        
        result = done_future.get_result()
        if not result:
            return False
        
        batch_size -= 1
        continue
    
    return True


async def _connect_gateways(task_group, gateways, max_concurrency):
    """
    Connects the given gateways adding each runner's into `task_group`.
    Connects them in batches of `max_concurrency`. If there is more, we wait for rate limits and continue.
    
    This function is a coroutine.
    
    Parameters
    ----------
    task_group : ``TaskGroup``
        Task group to use for waiters and the runner tasks.
    gateways : `list<DiscordGatewayClientShard>`
        The gateways to run.
    max_concurrency : `int`
        The maximal amount of shards that can be launched at the same time.
    
    Returns
    -------
    success : `bool`
    """
    chunk_start = 0
    limit = len(gateways)
    # At every step we add up to `max_concurrency` gateways to launch up. When a gateway is launched up
    while True:
        chunk_end = min(chunk_start + max_concurrency, limit)
        
        result = await _connect_gateway_batch(task_group, islice(gateways, chunk_start, chunk_end))
        if not result:
            return False
            
        chunk_start = chunk_end
        if chunk_start >= limit:
            break
        
        # Each gateway does an `IDENTIFY` on connection. You can send `max_concurrency` amount of identifies every
        # second. That means here we sleep `5` seconds. We could rush this 5 seconds, but no need.
        await sleep(5.0, KOKORO)
        continue
    
    return True


class DiscordGatewayClientSharder(DiscordGatewayClientBase):
    """
    Gateway of a client controlling multiple shards.
    
    Attributes
    ----------
    client : ``Client``
        The owner client of the gateway.
    gateways : `tuple<DiscordGatewayClientShard>`
        The controlled gateways.
    """
    __slots__ = ('client', 'gateways')
    
    def __new__(cls, client, shard_count, gateways):
        """
        Creates a sharder gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``Client``
            The owner client of the gateway.
        shard_count : `int`
            The amount of shards to create the gateway with.
        gateways : `None | tuple<DiscordGatewayClientShard>`
            Existing gateways to use.
        """
        gateways = _create_gateways(client, shard_count, gateways)
        
        self = object.__new__(cls)
        self.client = client
        self.gateways = gateways
        return self
    
    
    @copy_docs(DiscordGatewayClientBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(' client = ')
        repr_parts.append(repr(self.client.full_name))
        
        repr_parts.append(', shard_count = ')
        repr_parts.append(repr(len(self.gateways)))
    
    
    @copy_docs(DiscordGatewayClientBase.run)
    async def run(self):
        task_group = TaskGroup(KOKORO)
        
        try:
            result = await _connect_gateways(task_group, self.gateways, self.client._gateway_max_concurrency)
            
            if result:
                # If all shards successfully connected we wait till the first is cancelled.
                # Then we cancel the rest as well.
                finished_task = await task_group.wait_first()
                await self.close()
                finished_task.get_result()
            
            else:
                # If not all shards connected, we stop all of our shards
                await self.close()
        
        except:
            self.abort()
            raise
        
        finally:
            task_group.cancel_all()
        
        return False
    
    
    @property
    @copy_docs(DiscordGatewayClientBase.latency)
    def latency(self):
        total = 0.0
        count = 0
        for gateway in self.gateways:
            kokoro = gateway.kokoro
            if kokoro is None:
                continue
            
            total += kokoro.latency
            count += 1
        
        if count:
            return total / count
        
        return LATENCY_DEFAULT
    
    
    @copy_docs(DiscordGatewayClientBase.terminate)
    async def terminate(self):
        await TaskGroup(KOKORO, (Task(KOKORO, gateway.terminate()) for gateway in self.gateways)).wait_all()
    
    
    @copy_docs(DiscordGatewayClientBase.close)
    async def close(self):
        await TaskGroup(
            KOKORO,
            (Task(KOKORO, _close_and_abort_gateway(gateway)) for gateway in self.gateways),
        ).wait_all()
    
    
    @copy_docs(DiscordGatewayClientBase.abort)
    def abort(self):
        for gateway in self.gateways:
            gateway.abort()
    
    
    @copy_docs(DiscordGatewayClientBase.send_as_json)
    async def send_as_json(self, data):
        data = to_json(data)
        
        task_group = TaskGroup(KOKORO, (Task(KOKORO, gateway._send_json(data)) for gateway in self.gateways))
        failed_task = await task_group.wait_exception()
        if (failed_task is not None):
            task_group.cancel_all()
            failed_task.get_result()
    
    
    @copy_docs(DiscordGatewayClientBase.change_voice_state)
    async def change_voice_state(self, guild_id, channel_id, *, self_deaf = False, self_mute = False):
        gateway = self.get_gateway(guild_id)
        await gateway.change_voice_state(guild_id, channel_id, self_mute = self_mute, self_deaf = self_deaf)
    
    
    @copy_docs(DiscordGatewayClientBase.get_gateway)
    def get_gateway(self, guild_id):
        gateways = self.gateways
        if guild_id:
            gateway = gateways[(guild_id >> 22) % len(gateways)]
        else:
            gateway = gateways[0]
        
        return gateway
