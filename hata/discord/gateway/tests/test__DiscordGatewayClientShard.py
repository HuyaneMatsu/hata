from re import compile as re_compile
from sys import platform as PLATFORM
from zlib import Z_SYNC_FLUSH, compressobj as create_zlib_compressor, decompressobj as create_zlib_decompressor

import vampytest
from scarletio import Future, from_json, skip_ready_cycle, to_json
from scarletio.web_common import ConnectionClosed
from scarletio.web_socket import WebSocketClient

from ....env import CACHE_PRESENCE, LIBRARY_NAME

from ...activity import Activity
from ...client import Client
from ...core import KOKORO
from ...guild.guild.constants import LARGE_GUILD_LIMIT
from ...user import Status

from ..client_shard import DiscordGatewayClientShard
from ..constants import (
    GATEWAY_ACTION_CONNECT, GATEWAY_ACTION_KEEP_GOING, GATEWAY_ACTION_RESUME, GATEWAY_OPERATION_CLIENT_HEARTBEAT,
    GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE, GATEWAY_OPERATION_CLIENT_HELLO, GATEWAY_OPERATION_CLIENT_IDENTIFY,
    GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION, GATEWAY_OPERATION_CLIENT_RECONNECT, GATEWAY_OPERATION_CLIENT_RESUME,
    GATEWAY_OPERATION_CLIENT_VOICE_STATE, LATENCY_DEFAULT, INTERVAL_DEFAULT
)
from ..heartbeat import Kokoro
from ..rate_limit import GatewayRateLimiter

from .helpers_http_client import TestHTTPClient
from .helpers_websocket_client import TestWebSocketClient


ZlibDecompressorType = type(create_zlib_decompressor())

GATEWAY_URL_REGEX = re_compile('(.*?)\\?encoding=json&v=\\d+&compress=zlib-stream')


def _assert_fields_set(gateway):
    """
    Tests whether the gateway has ever of its attributes set.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayClientShard``
        The gateway to check.
    """
    vampytest.assert_instance(gateway, DiscordGatewayClientShard)
    vampytest.assert_instance(gateway._buffer, list)
    vampytest.assert_instance(gateway._decompressor, ZlibDecompressorType, nullable = True)
    vampytest.assert_instance(gateway._operation_handlers, dict)
    vampytest.assert_instance(gateway._should_run, bool)
    vampytest.assert_instance(gateway.client, Client)
    vampytest.assert_instance(gateway.kokoro, Kokoro, nullable = True)
    vampytest.assert_instance(gateway.rate_limit_handler, GatewayRateLimiter)
    vampytest.assert_instance(gateway.resume_gateway_url, str, nullable = True)
    vampytest.assert_instance(gateway.sequence, int)
    vampytest.assert_instance(gateway.session_id, str, nullable = True)
    vampytest.assert_instance(gateway.shard_id, int)
    vampytest.assert_instance(gateway.websocket, WebSocketClient, nullable = True)


def test__DiscordGatewayClientShard__new():
    """
    Tests whether ``DiscordGatewayClientShard.__new__`` works as intended.
    """
    client = Client(
        'token_202401060002',
        client_id = 202401060003,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        _assert_fields_set(gateway)
        
        vampytest.assert_is(gateway.client, client)
        vampytest.assert_eq(gateway.shard_id, shard_id)
        
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__repr():
    """
    Tests whether ``DiscordGatewayClientShard.__repr__`` works as intended.
    """
    client = Client(
        'token_202401060004',
        client_id = 202401060005,
        name = 'satori',
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        output = repr(gateway)
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in('client', output)
        vampytest.assert_in(client.name, output)
        
        vampytest.assert_in('shard_id', output)
        vampytest.assert_in(repr(shard_id), output)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__latency__no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.latency`` works as intended.
    
    Case: without kokoro.
    """
    client = Client(
        'token_202401060006',
        client_id = 202401060007,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        output = gateway.latency
        
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, LATENCY_DEFAULT)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__latency__with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.latency`` works as intended.
    
    Case: with kokoro.
    """
    client = Client(
        'token_202401060008',
        client_id = 202401060009,
    )
    
    shard_id = 2
    latency = 16.2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.latency = latency
        output = gateway.latency
        
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, latency)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__create_kokoro__starting():
    """
    Tests whether ``DiscordGatewayClientShard._create_kokoro`` works as intended.
    
    Case: Just starting.
    """
    client = Client(
        'token_202401070000',
        client_id = 202401070001,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        
        vampytest.assert_instance(gateway.kokoro, Kokoro)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__create_kokoro__running():
    """
    Tests whether ``DiscordGatewayClientShard._create_kokoro`` works as intended.
    
    Case: Already running -> should reset.
    """
    client = Client(
        'token_202401070002',
        client_id = 202401070003,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        
        gateway.kokoro.start()
        
        gateway._create_kokoro()
        
        vampytest.assert_instance(gateway.kokoro, Kokoro)
        vampytest.assert_is(gateway.kokoro.runner, None)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__send_json__no_websocket():
    """
    Tests whether ``DiscordGatewayClientShard._send_json`` works as intended.
    
    Case: No web socket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070004',
        client_id = 202401070005,
    )
    
    shard_id = 2
    
    data = {'hey': 'mister'}
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        await gateway._send_json(to_json(data))
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__send_json__sending():
    """
    Tests whether ``DiscordGatewayClientShard._send_json`` works as intended.
    
    Case: sending.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070005',
        client_id = 202401070006,
    )
    
    shard_id = 2
    
    data = {'hey': 'mister'}
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        await gateway._send_json(to_json(data))
        
        vampytest.assert_eq(
            websocket.out_operations,
            [
                ('send', to_json(data)),
            ],
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__resume():
    """
    Tests whether ``DiscordGatewayClientShard._resume`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070007',
        client_id = 202401070008,
    )
    
    shard_id = 2
    sequence = 69
    session_id = 'orin'
    
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway.sequence = sequence
        gateway.session_id = session_id
        
        await gateway._resume()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_CLIENT_RESUME,
                'd': {
                    'seq': sequence,
                    'session_id': session_id,
                    'token': client.token,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__identify__no_activity_no_shard():
    """
    Tests whether ``DiscordGatewayClientShard._identify`` works as intended.
    
    Case: No activity & no shard.
    
    This function is a coroutine.
    """
    shard_id = 0
    shard_count = 0
    status = Status.idle
    
    client = Client(
        'token_202401070009',
        client_id = 202401070010,
        shard_count = shard_count,
        status = status,
    )
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        await gateway._identify()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_CLIENT_IDENTIFY,
                'd': {
                    'token': client.token,
                    'properties': {
                        'os': PLATFORM,
                        'browser': LIBRARY_NAME,
                        'device': LIBRARY_NAME,
                    },
                    'compress': True,
                    'large_threshold': LARGE_GUILD_LIMIT,
                    'guild_subscriptions': CACHE_PRESENCE,
                    'intents': client.intents,
                    'v': 3,
                    'presence': {
                        'status': status.value,
                        'game': None,
                        'since': 0.0,
                        'afk': False,
                    },
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__identify__with_activity_with_shard():
    """
    Tests whether ``DiscordGatewayClientShard._identify`` works as intended.
    
    Case: with activity & with shard.
    
    This function is a coroutine.
    """
    shard_id = 1
    shard_count = 2
    status = Status.idle
    activity = Activity('carting')
    
    client = Client(
        'token_202401070011',
        client_id = 202401070012,
        shard_count = shard_count,
        status = status,
        activity = activity,
    )
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        await gateway._identify()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_CLIENT_IDENTIFY,
                'd': {
                    'token': client.token,
                    'properties': {
                        'os': PLATFORM,
                        'browser': LIBRARY_NAME,
                        'device': LIBRARY_NAME,
                    },
                    'compress': True,
                    'large_threshold': LARGE_GUILD_LIMIT,
                    'guild_subscriptions': CACHE_PRESENCE,
                    'intents': client.intents,
                    'v': 3,
                    'presence': {
                        'status': status.value,
                        'game': activity.to_data(),
                        'since': 0.0,
                        'afk': False,
                    },
                    'shard': [shard_id, shard_count],
                },
            }
        )
    finally:
        client._delete()
        client = None


def test__DiscordGatewayClientShard__clear_session():
    """
    Tests whether ``DiscordGatewayClientShard._clear_session`` works as intended.
    """
    client = Client(
        'token_202401070013',
        client_id = 202401070014,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.session_id = 'ayaya'
        gateway.sequence = 56
        gateway.resume_gateway_url = 'https://orindance.party/'
        
        gateway._clear_session()
        
        vampytest.assert_is(gateway.session_id, None)
        vampytest.assert_eq(gateway.sequence, -1)
        vampytest.assert_is(gateway.resume_gateway_url, None)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__terminate__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.terminate`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070015',
        client_id = 202401070016,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        await gateway.terminate()
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__terminate__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.terminate`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070017',
        client_id = 202401070018,
    )
    
    shard_id = 2
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        await gateway.terminate()
        
        vampytest.assert_is(gateway.kokoro.runner, None)
        
        vampytest.assert_eq(
            websocket.out_operations,
            [
                ('close', 4000),
            ],
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__close__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.close`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070019',
        client_id = 202401070020,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        await gateway.close()
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__close__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.close`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070021',
        client_id = 202401070022,
    )
    
    shard_id = 2
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        await gateway.close()
        
        vampytest.assert_is(gateway.kokoro.runner, None)
        
        vampytest.assert_eq(
            websocket.out_operations,
            [
                ('close', 1000),
            ],
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__abort__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.abort`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401110024',
        client_id = 202401110025,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        gateway.abort()
        
        vampytest.assert_eq(gateway._should_run, False)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__abort__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard.abort`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401110026',
        client_id = 202401110027,
    )
    
    shard_id = 2
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        gateway.abort()
        
        vampytest.assert_eq(gateway._should_run, False)
        vampytest.assert_is(gateway.kokoro.runner, None)
        vampytest.assert_eq(
            websocket.out_operations,
            [
                ('close_transport', True),
            ],
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__send_as_json__no_websocket():
    """
    Tests whether ``DiscordGatewayClientShard.send_as_json`` works as intended.
    
    Case: No websocket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070023',
        client_id = 202401070024,
    )
    
    shard_id = 2
    
    data = {'hey': 'mister'}
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        await gateway.send_as_json(data)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__send_as_json__sending():
    """
    Tests whether ``DiscordGatewayClientShard.send_as_json`` works as intended.
    
    Case: sending.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070025',
        client_id = 202401070026,
    )
    
    shard_id = 2
    
    data = {'hey': 'mister'}
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        await gateway.send_as_json(data)
        
        vampytest.assert_eq(
            websocket.out_operations,
            [
                ('send', to_json(data)),
            ],
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__beat():
    """
    Tests whether ``DiscordGatewayClientShard.beat`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070027',
        client_id = 202401070028,
    )
    
    shard_id = 2
    sequence = 69
    
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        await gateway.beat()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__change_voice_state():
    """
    Tests whether ``DiscordGatewayClientShard.change_voice_state`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401070029',
        client_id = 202401070030,
    )
    
    shard_id = 2
    
    channel_id = 202401070031
    guild_id = 202401070032
    
    self_deaf = True
    self_mute = True
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        await gateway.change_voice_state(guild_id, channel_id, self_mute = self_mute, self_deaf = self_deaf)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_CLIENT_VOICE_STATE,
                'd': {
                    'guild_id': str(guild_id),
                    'channel_id': str(channel_id),
                    'self_deaf': self_deaf,
                    'self_mute': self_mute,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_dispatch__unknown_dispatch_event():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_dispatch`` works as intended.
    
    Case: unknown dispatch event.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080000',
        client_id = 202401080001,
    )
    
    shard_id = 2
    
    message = {
        'd': {'hey': 'mister'},
        't': 'KOISHI',
    }
    
    mock_parsers = {}
    
    unknown_dispatch_event_event_handler_called = False
    
    def mock_call_unknown_dispatch_event_event_handler(client, event, data):
        nonlocal unknown_dispatch_event_event_handler_called  
        unknown_dispatch_event_event_handler_called = True
    
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_dispatch,
            PARSERS = mock_parsers,
            call_unknown_dispatch_event_event_handler = mock_call_unknown_dispatch_event_event_handler,
        )
        
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_true(unknown_dispatch_event_event_handler_called)
        
    finally:
        client._delete()
        client = None



async def test__DiscordGatewayClientShard__handle_operation_dispatch__no_data():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_dispatch`` works as intended.
    
    Case: No data received.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080002',
        client_id = 202401080003,
    )
    
    shard_id = 2
    
    event_data = None
    event_name = 'KOISHI'
    
    message = {
        'd': event_data,
        't': event_name,
    }
    
    event_parser_called = False
    
    def mock_event_parser(parser_client, parser_data):
        nonlocal event_parser_called
        event_parser_called = True
    
    mock_parsers = {event_name : mock_event_parser}
    
    unknown_dispatch_event_event_handler_called = False
    
    def mock_call_unknown_dispatch_event_event_handler(client, event, data):
        nonlocal unknown_dispatch_event_event_handler_called  
        unknown_dispatch_event_event_handler_called = True
    
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_dispatch,
            PARSERS = mock_parsers,
            call_unknown_dispatch_event_event_handler = mock_call_unknown_dispatch_event_event_handler,
        )
        
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_false(event_parser_called)
        vampytest.assert_false(unknown_dispatch_event_event_handler_called)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_dispatch__event_parser_call():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_dispatch`` works as intended.
    
    Case: event parser called.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080004',
        client_id = 202401080005,
    )
    
    shard_id = 2
    
    event_data = {'hey': 'mister'}
    event_name = 'KOISHI'
    
    message = {
        'd': event_data,
        't': event_name,
    }
    
    event_parser_called = False
    
    def mock_event_parser(parser_client, parser_data):
        nonlocal event_data
        nonlocal event_parser_called
        nonlocal client
        vampytest.assert_eq(event_data, parser_data)
        vampytest.assert_is(client, parser_client)
        event_parser_called = True
    
    mock_parsers = {event_name : mock_event_parser}
    
    unknown_dispatch_event_event_handler_called = False
    
    def mock_call_unknown_dispatch_event_event_handler(client, event, data):
        nonlocal unknown_dispatch_event_event_handler_called  
        unknown_dispatch_event_event_handler_called = True
    
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_dispatch,
            PARSERS = mock_parsers,
            call_unknown_dispatch_event_event_handler = mock_call_unknown_dispatch_event_event_handler,
        )
        
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_true(event_parser_called)
        vampytest.assert_false(unknown_dispatch_event_event_handler_called)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_dispatch__event_parser_exception():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_dispatch`` works as intended.
    
    Case: event parser raises exception.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080006',
        client_id = 202401080007,
    )
    
    shard_id = 2
    
    event_data = {'hey': 'mister'}
    event_name = 'KOISHI'
    
    message = {
        'd': event_data,
        't': event_name,
    }
    
    exception = ValueError('hi')
    
    def mock_event_parser(parser_client, parser_data):
        nonlocal exception
        raise exception
    
    mock_parsers = {event_name : mock_event_parser}
    
    error_event_handler_called = False
    
    async def mock_error_event_handler(error_client, error_location, error_exception):
        nonlocal client
        nonlocal event_name
        nonlocal exception
        nonlocal error_event_handler_called
        
        vampytest.assert_is(client, error_client)
        vampytest.assert_is(error_location, event_name)
        vampytest.assert_is(error_exception, exception)
        error_event_handler_called = True
    
    try:
        client.events.error = mock_error_event_handler
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_dispatch,
            PARSERS = mock_parsers,
        )
        
        output = await mocked(gateway, message)
        await skip_ready_cycle()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_true(error_event_handler_called)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_dispatch__ready_event():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_dispatch`` works as intended.
    
    Case: ready event.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080008',
        client_id = 202401080009,
    )
    
    shard_id = 2
    
    session_id = 'ayaya'
    resume_gateway_url = 'https://orindance.party/'
    
    event_data = {
        'session_id': session_id,
        'resume_gateway_url': resume_gateway_url,
    }
    event_name = 'READY'
    
    message = {
        'd': event_data,
        't': event_name,
    }
    
    def mock_event_parser(parser_client, parser_data):
        return ...
    
    mock_parsers = {event_name : mock_event_parser}
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_dispatch,
            PARSERS = mock_parsers,
        )
        
        output = await mocked(gateway, message)
        await skip_ready_cycle()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(gateway.session_id, session_id)
        vampytest.assert_eq(gateway.resume_gateway_url, resume_gateway_url)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_hello__with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_hello`` works as intended.
    
    Case: with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080010',
        client_id = 202401080011,
    )
    
    shard_id = 2
    heartbeat_interval = 36.0
    sequence = 12
    
    message = {
        'd': {
            'heartbeat_interval': int(heartbeat_interval * 1000.0),
        },
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        output = await gateway._handle_operation_hello(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(gateway.kokoro.interval, heartbeat_interval)
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {   
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            },
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_hello__with_kokoro_no_data():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_hello`` works as intended.
    
    Case: with kokoro but without data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080010',
        client_id = 202401080011,
    )
    
    shard_id = 2
    sequence = 12
    
    message = {
        'd': None,
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        output = await gateway._handle_operation_hello(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(gateway.kokoro.interval, INTERVAL_DEFAULT)
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {   
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            },
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_hello__no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_hello`` works as intended.
    
    Case: without kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401280000',
        client_id = 202401280001,
    )
    
    shard_id = 2
    heartbeat_interval = 36.0
    sequence = 12
    
    message = {
        'd': {
            'heartbeat_interval': heartbeat_interval * 1000.0,
        },
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        output = await gateway._handle_operation_hello(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        
        vampytest.assert_eq(gateway.kokoro.interval, heartbeat_interval)
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {   
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            },
        )
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_heartbeat_acknowledge__with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_heartbeat_acknowledge`` works as intended.
    
    Case: with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080012',
        client_id = 202401080013,
    )
    
    shard_id = 2
    
    message = {
        'd': None,
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        
        output = await gateway._handle_operation_heartbeat_acknowledge(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_ne(gateway.latency, LATENCY_DEFAULT)
        vampytest.assert_eq(len(websocket.out_operations), 0)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_heartbeat_acknowledge__no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_heartbeat_acknowledge`` works as intended.
    
    Case: without kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401280002',
        client_id = 202401280003,
    )
    
    shard_id = 2
    
    message = {
        'd': None,
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        
        output = await gateway._handle_operation_heartbeat_acknowledge(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_ne(gateway.latency, LATENCY_DEFAULT)
        vampytest.assert_true(gateway.latency < 0.001)
        vampytest.assert_eq(len(websocket.out_operations), 0)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_heartbeat__with_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_heartbeat`` works as intended.
    
    Case: with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080014',
        client_id = 202401080015,
    )
    
    shard_id = 2
    sequence = 12
    
    message = {
        'd': {},
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        output = await gateway._handle_operation_heartbeat(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            },
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_heartbeat__no_kokoro():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_heartbeat`` works as intended.
    
    Case: without kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401280004',
        client_id = 202401280005,
    )
    
    shard_id = 2
    sequence = 12
    
    message = {
        'd': {},
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        output = await gateway._handle_operation_heartbeat(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(len(websocket.out_operations), 0)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_reconnect__default():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_reconnect`` works as intended.
    
    Case: default.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080016',
        client_id = 202401080017,
    )
    
    shard_id = 2
    
    message = {
        'd': {},
    }
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway.websocket = websocket
        
        output = await gateway._handle_operation_reconnect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_RESUME)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, close_code = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'close')
        vampytest.assert_eq(close_code, 4000)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_invalidate_session__true():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_invalidate_session`` works as intended.
    
    Case: invalidate session with true.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080018',
        client_id = 202401080019,
    )
    
    shard_id = 2
    
    message = {
        'd': True,
    }
    
    sleep_called = False
    
    def mock_sleep(duration, loop = None):
        nonlocal sleep_called
        sleep_called = True
        
        future = Future(KOKORO)
        future.set_result(None)
        return future
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway.websocket = websocket
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_invalidate_session,
            sleep = mock_sleep,
        )
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_RESUME)
        
        await skip_ready_cycle()
        
        # Sleeping is optional
        # vampytest.assert_true(sleep_called)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, close_code = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'close')
        vampytest.assert_eq(close_code, 1000)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_operation_invalidate_session__false():
    """
    Tests whether ``DiscordGatewayClientShard._handle_operation_invalidate_session`` works as intended.
    
    Case: invalidate session with false.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080020',
        client_id = 202401080021,
    )
    
    shard_id = 2
    operation = GATEWAY_OPERATION_CLIENT_INVALIDATE_SESSION
    session_id = 'orin'
    
    message = {
        'd': False,
    }
    
    sleep_called = False
    
    def mock_sleep(duration, loop = None):
        nonlocal sleep_called
        sleep_called = True
        
        future = Future(KOKORO)
        future.set_result(None)
        return future
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway.websocket = websocket
        gateway.session_id = session_id
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_invalidate_session,
            sleep = mock_sleep,
        )
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        await skip_ready_cycle()
        
        vampytest.assert_false(sleep_called)
        vampytest.assert_is(gateway.session_id, None)
        
        vampytest.assert_eq(len(websocket.out_operations), 0)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_received_operation__unknown_operation():
    """
    Tests whether ``DiscordGatewayClientShard._handle_received_operation`` works as intended.
    
    Case: invalidate session with false.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401080022',
        client_id = 202401080023,
    )
    
    shard_id = 2
    operation = 999
    
    message = {
        'op': operation,
        'd': None,
    }
    
    error_event_handler_called = False
    
    async def mock_error_event_handler(error_client, error_location, error_exception):
        nonlocal client
        nonlocal error_event_handler_called
        
        vampytest.assert_is(client, error_client)
        vampytest.assert_instance(error_location, str)
        vampytest.assert_instance(error_exception, str)
        error_event_handler_called = True
    
    
    try:
        client.events.error = mock_error_event_handler
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway.websocket = websocket
        
        output = await gateway._handle_received_operation(to_json(message))
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(error_event_handler_called)
        vampytest.assert_eq(len(websocket.out_operations), 0)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__handle_received_operation__known_operation():
    """
    Tests whether ``DiscordGatewayClientShard._handle_received_operation`` works as intended.
    
    Case: Handling a heartbeat acknowledge operation.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130000',
        client_id = 202401130001,
    )
    
    shard_id = 2
    operation = 999
    sequence = 123
    
    message = {
        's': sequence,
        'op': operation,
        'd': {},
    }
    
    gateway = None
    mock_operation_handler_called = False
    
    async def mock_operation_handler(parameter_gateway, parameter_message):
        nonlocal gateway
        nonlocal message
        nonlocal mock_operation_handler_called
        
        vampytest.assert_is(gateway, parameter_gateway)
        vampytest.assert_eq(message, parameter_message)
        mock_operation_handler_called = True
        
        return GATEWAY_ACTION_RESUME
    
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._operation_handlers[operation] = mock_operation_handler
        gateway.websocket = websocket
        
        output = await gateway._handle_received_operation(to_json(message))
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_RESUME)
        
        vampytest.assert_true(mock_operation_handler_called)
        vampytest.assert_eq(gateway.sequence, sequence)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__poll_and_handle_received_operation__no_websocket():
    """
    Tests whether ``DiscordGatewayClientShard._poll_and_handle_received_operation`` works as intended.
    
    Case: no websocket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130002',
        client_id = 202401130003,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__poll_and_handle_received_operation__connection_closed_expected():
    """
    Tests whether ``DiscordGatewayClientShard._poll_and_handle_received_operation`` works as intended.
    
    Case: Polling fails with an expected code.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130004',
        client_id = 202401130005,
    )
    
    shard_id = 2
    
    try:
        websocket = await TestWebSocketClient(
            KOKORO,
            '',
            in_operations = [
                ('receive', True, ConnectionClosed(4000, None)),
            ],
        )
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__poll_and_handle_received_operation__connection_closed_un_expected():
    """
    Tests whether ``DiscordGatewayClientShard._poll_and_handle_received_operation`` works as intended.
    
    Case: Polling fails with an un-expected code.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130006',
        client_id = 202401130007,
    )
    
    shard_id = 2
    exception = ConnectionClosed(1000, None)
    
    try:
        websocket = await TestWebSocketClient(
            KOKORO,
            '',
            in_operations = [
                ('receive', True, exception),
            ],
        )
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        
        with vampytest.assert_raises(exception):
            await gateway._poll_and_handle_received_operation()

    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__poll_and_handle_received_operation__zlib_decode_error():
    """
    Tests whether ``DiscordGatewayClientShard._poll_and_handle_received_operation`` works as intended.
    
    Case: Zlib decode error.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130008',
        client_id = 202401130009,
    )
    
    shard_id = 2
    
    try:
        websocket = await TestWebSocketClient(
            KOKORO,
            '',
            in_operations = [
                ('receive', False, b'hey mister' + b'\x00\x00\xff\xff'),
            ],
        )
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        gateway._decompressor = create_zlib_decompressor()
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
    finally:
        client._delete()
        client = None



async def test__DiscordGatewayClientShard__poll_and_handle_received_operation__heartbeat_acknowledge():
    """
    Tests whether ``DiscordGatewayClientShard._poll_and_handle_received_operation`` works as intended.
    
    Case: Handling a heartbeat acknowledge operation.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401130010',
        client_id = 202401130011,
    )
    
    shard_id = 2
    operation = GATEWAY_OPERATION_CLIENT_HEARTBEAT_ACKNOWLEDGE
    
    message = {
        'op': operation,
        'd': {},
    }
    
    compressor = create_zlib_compressor()
    data = compressor.compress(to_json(message).encode()) + compressor.flush(Z_SYNC_FLUSH)
    
    try:
        websocket = await TestWebSocketClient(
            KOKORO,
            '',
            in_operations = [
                ('receive', False, data),
            ],
        )
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway._create_kokoro()
        gateway.websocket = websocket
        gateway._decompressor = create_zlib_decompressor()
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_ne(gateway.latency, LATENCY_DEFAULT)
        vampytest.assert_eq(len(websocket.out_operations), 0)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__connect__unexpected_closes_with_resume():
    """
    Tests whether ``DiscordGatewayClientShard._connect`` works as intended.
    
    Case: Unexpectedly closed with resume.
    
    This function is a coroutine.
    """
    heartbeat_interval = 40.0
    
    message_0 = {
        'op': GATEWAY_OPERATION_CLIENT_HELLO,
        'd': {
            'heartbeat_interval': int(heartbeat_interval * 1000.0),
        },
    }
    
    compressor = create_zlib_compressor()
    data_0 = compressor.compress(to_json(message_0).encode()) + compressor.flush(Z_SYNC_FLUSH)
    
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, data_0),
            ('ensure_open', True, ConnectionClosed(1000, None)),
        ],
    )

    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401130012',
        client_id = 202401130013,
        http = http,
    )
    
    shard_id = 2
    sequence = 69
    session_id = 'okuu'
    resume_gateway_url = 'koishi'
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.sequence = sequence
        gateway.session_id = session_id
        gateway.resume_gateway_url = resume_gateway_url
        
        output = await gateway._connect(True)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        match = GATEWAY_URL_REGEX.fullmatch(websocket.url)
        vampytest.assert_is_not(match, None)
        vampytest.assert_eq(match.group(1), resume_gateway_url)
        
        vampytest.assert_eq(len(websocket.out_operations), 2)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {   
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': sequence,
            },
        )
        operation, data = websocket.out_operations[1]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {
                'op': GATEWAY_OPERATION_CLIENT_RESUME,
                'd': {
                    'seq': sequence,
                    'session_id': session_id,
                    'token': client.token,
                },
            }
        )
        
        vampytest.assert_is(gateway.session_id, None)
        vampytest.assert_eq(gateway.sequence, -1)
        vampytest.assert_is(gateway.resume_gateway_url, None)
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is(gateway.kokoro.runner, None)
        vampytest.assert_is(gateway.websocket, None)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__connect__success_default():
    """
    Tests whether ``DiscordGatewayClientShard._connect`` works as intended.
    
    Case: Success default.
    
    This function is a coroutine.
    """
    heartbeat_interval = 40.0
    
    message_0 = {
        'op': GATEWAY_OPERATION_CLIENT_HELLO,
        'd': {
            'heartbeat_interval': int(heartbeat_interval * 1000.0),
        },
    }
    
    compressor = create_zlib_compressor()
    data_0 = compressor.compress(to_json(message_0).encode()) + compressor.flush(Z_SYNC_FLUSH)
    
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, data_0),
        ],
    )

    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401130014',
        client_id = 202401130015,
        http = http,
    )
    
    shard_id = 2
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        output = await gateway._connect(False)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        match = GATEWAY_URL_REGEX.fullmatch(websocket.url)
        vampytest.assert_is_not(match, None)
        vampytest.assert_eq(match.group(1), 'orin')
        
        vampytest.assert_eq(len(websocket.out_operations), 2)
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(
            from_json(data),
            {   
                'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                'd': -1,
            },
        )
        
        operation, data = websocket.out_operations[1]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {
                'op': GATEWAY_OPERATION_CLIENT_IDENTIFY,
                'd': {
                    'token': client.token,
                    'properties': {
                        'os': PLATFORM,
                        'browser': LIBRARY_NAME,
                        'device': LIBRARY_NAME,
                    },
                    'compress': True,
                    'large_threshold': LARGE_GUILD_LIMIT,
                    'guild_subscriptions': CACHE_PRESENCE,
                    'intents': client.intents,
                    'v': 3,
                    'presence': {
                        'status': client._status.value,
                        'game': None,
                        'since': 0.0,
                        'afk': False,
                    },
                },
            }
        )
        
        vampytest.assert_is(gateway.session_id, None)
        vampytest.assert_eq(gateway.sequence, -1)
        vampytest.assert_is(gateway.resume_gateway_url, None)
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        vampytest.assert_is_not(gateway.websocket, None)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__keep_polling_and_handling():
    """
    Tests whether ``DiscordGatewayClientShard._keep_polling_and_handling`` works as intended.
    
    This function is a coroutine.
    """
    message_0 = {
        'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
        'd': {},
    }
    
    compressor = create_zlib_compressor()
    data_0 = compressor.compress(to_json(message_0).encode()) + compressor.flush(Z_SYNC_FLUSH)
    data_1 = compressor.compress(to_json(message_0).encode()) + compressor.flush(Z_SYNC_FLUSH)
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, data_0),
            ('receive', False, data_1),
            ('receive', True, TimeoutError), # propagate timeout to stop
        ],
    )
    
    client = Client(
        'token_202401130016',
        client_id = 202401130017,
    )
    
    shard_id = 2
    sequence = 69
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        gateway.websocket = websocket
        gateway.sequence = sequence
        gateway._create_kokoro()
        gateway.kokoro.start()
        gateway._decompressor = create_zlib_decompressor()
        
        output = await gateway._keep_polling_and_handling()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        vampytest.assert_eq(len(websocket.out_operations), 2)
        
        for index in range(2):
            operation, sent_data = websocket.out_operations[0]
            vampytest.assert_eq(operation, 'send')
            vampytest.assert_eq(
                from_json(sent_data),
                {
                    'op': GATEWAY_OPERATION_CLIENT_HEARTBEAT,
                    'd': sequence,
                }
            )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayClientShard__run__default():
    """
    Tests whether ``DiscordGatewayClientShard.run`` works as intended.
    
    Case: Only testing a simple case. Feeling tired of writing so much.
    """
    heartbeat_interval = 40.0
    
    message_0 = {
        'op': GATEWAY_OPERATION_CLIENT_HELLO,
        'd': {
            'heartbeat_interval': int(heartbeat_interval * 1000.0),
        },
    }
    
    compressor = create_zlib_compressor()
    data_0 = compressor.compress(to_json(message_0).encode()) + compressor.flush(Z_SYNC_FLUSH)
    
    exception = RuntimeError('hiss')
    
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, data_0),
            ('receive', True, exception),
        ],
    )
    
    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401130018',
        client_id = 202401130019,
        http = http,
    )
    # yep, we are running.
    client.running = True
    
    shard_id = 2
    
    waiter = Future(KOKORO)
    
    try:
        gateway = DiscordGatewayClientShard(client, shard_id)
        
        with vampytest.assert_raises(exception):
            await gateway.run(waiter)
        
        output = waiter.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        client.running = False
        client._delete()
        client = None
