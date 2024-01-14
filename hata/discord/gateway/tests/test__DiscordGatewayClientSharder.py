import vampytest
from scarletio import Task, skip_ready_cycle

from ...client import Client
from ...core import KOKORO

from ..client_sharder import DiscordGatewayClientSharder
from ..constants import LATENCY_DEFAULT
from ..heartbeat import Kokoro

from .helpers_gateway_shard import TestGatewayShard


def _assert_fields_set(gateway):
    """
    Asserts whether gateway sharder has all of its fields set.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayClientSharder``
        The gateway to check.
    """
    vampytest.assert_instance(gateway, DiscordGatewayClientSharder)
    vampytest.assert_instance(gateway.client, Client)
    vampytest.assert_instance(gateway.gateways, tuple)


def test__DiscordGatewayClientSharder__new__no_gateways():
    """
    Tests whether ``DiscordGatewayClientSharder.__new__`` works as intended.
    
    Case: No gateways.
    """
    client = Client(
        'token_202301140010',
        client_id = 202301140011,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        _assert_fields_set(gateway)
        
        vampytest.assert_eq(len(gateway.gateways), shard_count)
    
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientSharder__new__with_gateways():
    """
    Tests whether ``DiscordGatewayClientSharder.__new__`` works as intended.
    
    Case: With gateways.
    """
    client = Client(
        'token_202301140012',
        client_id = 202301140013,
    )
    
    shard_count = 4
    
    gateways = (TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard())
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, gateways)
        _assert_fields_set(gateway)
        
        vampytest.assert_eq(len(gateway.gateways), shard_count)
        vampytest.assert_eq(gateway.gateways, gateways)
    
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientSharder__repr():
    """
    Tests whether ``DiscordGatewayClientSharder.__repr__`` works as intended.
    """
    client = Client(
        'token_202301140014',
        client_id = 202301140015,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        
        output = repr(gateway)
        vampytest.assert_instance(output, str)
    
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientSharder__get_gateway():
    """
    Tests whether ``DiscordGatewayClientSharder.get_gateway`` works as intended.
    """
    client = Client(
        'token_202301140016',
        client_id = 202301140017,
    )
    
    shard_count = 4
    guild_id = 5 << 22
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        
        output = gateway.get_gateway(guild_id)
        vampytest.assert_is(gateway.gateways[1], output)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__change_voice_state():
    """
    Tests whether ``DiscordGatewayClientSharder.change_voice_state`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140018',
        client_id = 202301140019,
    )
    
    shard_count = 4
    channel_id = 69
    guild_id = 5 << 22
    self_deaf = True
    self_mute = True
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        await gateway.change_voice_state(guild_id, channel_id, self_deaf = self_deaf, self_mute = self_mute)
        
        vampytest.assert_eq(
            gateway.gateways[1].out_operations,
            [
                (
                    'change_voice_state',
                    (guild_id, channel_id, {'self_deaf': self_deaf, 'self_mute': self_mute})
                )
            ]
        )
        
        for gateway_shard in (gateway.gateways[0], gateway.gateways[2], gateway.gateways[3]):
            vampytest.assert_eq(gateway_shard.out_operations, [])
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__send_as_json():
    """
    Tests whether ``DiscordGatewayClientSharder.send_as_json`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140020',
        client_id = 202301140021,
    )
    
    shard_count = 4
    data = {'hey': 'mister'}
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        await gateway.send_as_json(data)
        
        for gateway_shard in gateway.gateways:
            vampytest.assert_eq(
                gateway_shard.out_operations,
                [
                    (
                        'send_as_json',
                        data,
                    )
                ]
            )
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__abort():
    """
    Tests whether ``DiscordGatewayClientSharder.abort`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140022',
        client_id = 202301140023,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        gateway.abort()
        
        for gateway_shard in gateway.gateways:
            vampytest.assert_eq(
                gateway_shard.out_operations,
                [
                    (
                        'abort',
                        None,
                    )
                ]
            )
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__close():
    """
    Tests whether ``DiscordGatewayClientSharder.close`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140024',
        client_id = 202301140025,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        await gateway.close()
        
        for gateway_shard in gateway.gateways:
            vampytest.assert_eq(
                gateway_shard.out_operations,
                [
                    (
                        'close',
                        None,
                    ), (
                        'abort',
                        None,
                    )
                ]
            )
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__terminate():
    """
    Tests whether ``DiscordGatewayClientSharder.terminate`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140026',
        client_id = 202301140027,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        await gateway.terminate()
        
        for gateway_shard in gateway.gateways:
            vampytest.assert_eq(
                gateway_shard.out_operations,
                [
                    (
                        'terminate',
                        None,
                    ),
                ]
            )
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__latency__default():
    """
    Tests whether ``DiscordGatewayClientSharder.terminate`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140028',
        client_id = 202301140029,
    )
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(
            TestGatewayShard(
                in_operations = [
                    ('kokoro', False, None)
                ]
            ) for _ in range(shard_count)
        ),)
        
        output = gateway.latency
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, LATENCY_DEFAULT)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__latency__non_default():
    """
    Tests whether ``DiscordGatewayClientSharder.terminate`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140028',
        client_id = 202301140029,
    )
    
    shard_count = 4
    latencies = [10.0, 20.0, 30.0, 20.0]
    kokoros = [Kokoro(TestGatewayShard()) for _ in range(shard_count)]
    for kokoro, latency in zip(kokoros, latencies):
        kokoro.latency = latency
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(
            TestGatewayShard(
                in_operations = [
                    ('kokoro', False, kokoro)
                ]
            ) for kokoro in kokoros
        ),)
        
        output = gateway.latency
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, sum(latencies) / len(latencies))
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientSharder__run__default():
    """
    Tests whether ``DiscordGatewayClientSharder.run`` works as intended.
    
    Case: Default case only.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202301140028',
        client_id = 202301140029,
    )
    client._gateway_max_concurrency = 4
    
    shard_count = 4
    
    try:
        gateway = DiscordGatewayClientSharder(client, shard_count, None)
        gateway.gateways = (*(TestGatewayShard() for _ in range(shard_count)),)
        
        task = Task(KOKORO, gateway.run())
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        for shard_gateway in gateway.gateways:
            vampytest.assert_is_not(shard_gateway.waiter, None)
        
        for shard_gateway in gateway.gateways:
            shard_gateway.set_waiter(False, True)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        for shard_gateway in gateway.gateways:
            vampytest.assert_true(shard_gateway.run_end_waiter.is_pending())
        
        gateway.gateways[1].run_end_waiter.set_result_if_pending(False)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        for shard_gateway in gateway.gateways:
            vampytest.assert_eq(shard_gateway.out_operations, [('close', None), ('abort', None)])
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        for shard_gateway in gateway.gateways:
            vampytest.assert_true(shard_gateway.run_end_waiter.is_done())
        
        vampytest.assert_true(task.is_done())
        output = task.get_result()
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
    finally:
        client._delete()
        client = None
