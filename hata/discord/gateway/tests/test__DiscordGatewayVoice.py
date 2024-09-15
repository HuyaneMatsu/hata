from math import floor
from re import compile as re_compile

import vampytest
from scarletio import Future, from_json, skip_ready_cycle, to_json
from scarletio.web_common import ConnectionClosed
from scarletio.web_socket import WebSocketClient

from ...client import Client
from ...core import KOKORO
from ...guild import Guild
from ...user import VoiceState
from ...voice import VoiceClient
from ...voice.encryption_adapters import EncryptionAdapter__aead_xchacha20_poly1305_rtpsize, EncryptionAdapterBase

from ..constants import (
    GATEWAY_ACTION_CONNECT, GATEWAY_ACTION_KEEP_GOING, GATEWAY_ACTION_RESUME, GATEWAY_OPERATION_VOICE_CLIENT_CONNECT,
    GATEWAY_OPERATION_VOICE_HEARTBEAT, GATEWAY_OPERATION_VOICE_HELLO, GATEWAY_OPERATION_VOICE_IDENTIFY,
    GATEWAY_OPERATION_VOICE_RESUME, GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL, GATEWAY_OPERATION_VOICE_SPEAKING,
    LATENCY_DEFAULT
)
from ..heartbeat import Kokoro
from ..rate_limit import GatewayRateLimiter
from ..voice import DiscordGatewayVoice

from .helpers_http_client import TestHTTPClient
from .helpers_websocket_client import TestWebSocketClient


try:
    import nacl.secret
except ImportError:
    SecretBox = None
else:
    SecretBox = nacl.secret.SecretBox
    del nacl


GATEWAY_URL_REGEX = re_compile('wss://(.*?)/\\?v=\d+')


def _assert_fields_set(gateway):
    """
    Asserts whether the given gateway has all of its fields set.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayVoice``
        The gateway to check.
    """
    vampytest.assert_instance(gateway, DiscordGatewayVoice)
    vampytest.assert_instance(gateway._operation_handlers, dict)
    vampytest.assert_instance(gateway._should_run, bool)
    vampytest.assert_instance(gateway.kokoro, Kokoro, nullable = True)
    vampytest.assert_instance(gateway.rate_limit_handler, GatewayRateLimiter)
    vampytest.assert_instance(gateway.sequence, int)
    vampytest.assert_instance(gateway.voice_client, VoiceClient)
    vampytest.assert_instance(gateway.websocket, WebSocketClient, nullable = True)


def test__DiscordGatewayVoice():
    """
    Tests whether ``DiscordGatewayVoice`` works as intended.
    """
    client = Client(
        'token_202401180000',
        client_id = 202401180001,
    )
    
    try:
        voice_client = VoiceClient(client, 202401180002, 202401180003)
        gateway = DiscordGatewayVoice(voice_client)
        
        _assert_fields_set(gateway)
        vampytest.assert_is(gateway.voice_client, voice_client)
        
    finally:
        client.stop()


def test__DiscordGatewayVoice__create_kokoro__starting():
    """
    Tests whether ``DiscordGatewayVoice._create_kokoro`` works as intended.
    
    Case: Just starting.
    """
    client = Client(
        'token_202401180004',
        client_id = 202401180005,
    )
    
    try:
        voice_client = VoiceClient(client, 202401180006, 202401180007)
        gateway = DiscordGatewayVoice(voice_client)
        gateway._create_kokoro()
        
        vampytest.assert_instance(gateway.kokoro, Kokoro)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayVoice__create_kokoro__running():
    """
    Tests whether ``DiscordGatewayVoice._create_kokoro`` works as intended.
    
    Case: Already running -> should reset.
    """
    client = Client(
        'token_202401180008',
        client_id = 202401180009,
    )
    
    try:
        voice_client = VoiceClient(client, 202401180010, 202401180011)
        gateway = DiscordGatewayVoice(voice_client)
        gateway._create_kokoro()
        
        gateway.kokoro.start()
        
        gateway._create_kokoro()
        
        vampytest.assert_instance(gateway.kokoro, Kokoro)
        vampytest.assert_is(gateway.kokoro.runner, None)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayVoice__repr():
    """
    Tests whether ``DiscordGatewayVoice.__repr__`` works as intended.
    """
    client = Client(
        'token_202401180012',
        client_id = 202401180013,
        name = 'satori',
    )
    
    try:
        voice_client = VoiceClient(client, 202401180014, 202401180015)
        gateway = DiscordGatewayVoice(voice_client)
        
        output = repr(gateway)
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in('voice_client', output)
        vampytest.assert_in(repr(voice_client), output)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayVoice__latency__no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.latency`` works as intended.
    
    Case: without kokoro.
    """
    client = Client(
        'token_202401180016',
        client_id = 202401180017,
    )
    
    try:
        voice_client = VoiceClient(client, 202401180018, 202401180019)
        gateway = DiscordGatewayVoice(voice_client)
        
        output = gateway.latency
        
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, LATENCY_DEFAULT)
    finally:
        client._delete()
        client = None


def test__DiscordGatewayVoice__latency__with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.latency`` works as intended.
    
    Case: with kokoro.
    """
    client = Client(
        'token_202401180020',
        client_id = 202401180021,
    )
    
    latency = 2.1
    
    try:
        voice_client = VoiceClient(client, 202401180022, 202401180023)
        gateway = DiscordGatewayVoice(voice_client)
        gateway._create_kokoro()
        gateway.kokoro.latency = latency
        output = gateway.latency
        
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, latency)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__send_json__no_websocket():
    """
    Tests whether ``DiscordGatewayVoice._send_json`` works as intended.
    
    Case: No web socket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401180024',
        client_id = 202401180025,
    )
    
    data = {'hey': 'mister'}
    
    try:
        voice_client = VoiceClient(client, 202401180026, 202401180027)
        gateway = DiscordGatewayVoice(voice_client)
        
        await gateway.send_as_json(data)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__send_json__sending():
    """
    Tests whether ``DiscordGatewayVoice._send_json`` works as intended.
    
    Case: sending.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401180028',
        client_id = 202401180029,
    )
    
    data = {'hey': 'mister'}
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401180030, 202401180031)
        gateway = DiscordGatewayVoice(voice_client)
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


async def test__DiscordGatewayVoice__beat():
    """
    Tests whether ``DiscordGatewayVoice.beat`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401180032',
        client_id = 202401180033,
    )
    
    current_time = 69.1233
    sequence = 14666
    
    def mock_perf_counter():
        nonlocal current_time
        return current_time * 0.001
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401180034, 202401180035)
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        mocked = vampytest.mock_globals(
            type(gateway).beat,
            perf_counter = mock_perf_counter,
        )
        
        await mocked(gateway)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_HEARTBEAT,
                'd': {
                    't': floor(current_time),
                    'seq_ack': sequence,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__voice_client_connect():
    """
    Tests whether ``DiscordGatewayVoice._voice_client_connect`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190000',
        client_id = 202401190001,
    )
    
    audio_source = 12
    video_source = 13
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190002, 202401190003)
        voice_client._audio_source = audio_source
        voice_client._video_source = video_source
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        await gateway._voice_client_connect()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_CLIENT_CONNECT,
                'd': {
                    'audio_ssrc': audio_source,
                    'video_ssrc': video_source,
                    'rtx_ssrc': 0,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__set_speaking():
    """
    Tests whether ``DiscordGatewayVoice.set_speaking`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190004',
        client_id = 202401190005,
    )
    
    speaking = True
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190006, 202401190007)
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        await gateway.set_speaking(speaking)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_SPEAKING,
                'd': {
                    'speaking': speaking,
                    'delay': 0,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__identify():
    """
    Tests whether ``DiscordGatewayVoice._identify`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190008',
        client_id = 202401190009,
    )
    
    guild_id = 202401190012
    client_id = client.id
    session_id = 'orin'
    token = 'satori'
    sequence = 1122
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, guild_id, 202401190011)
        guild = Guild.precreate(guild_id, voice_states = [VoiceState(user_id = client.id, session_id = session_id)])
        voice_client._token = token
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        await gateway._identify()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_IDENTIFY,
                'd': {
                    'seq_ack': sequence,
                    'server_id': str(guild_id),
                    'session_id': session_id,
                    'token': token,
                    'user_id': str(client_id),
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__resume():
    """
    Tests whether ``DiscordGatewayVoice._resume`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190013',
        client_id = 202401190014,
    )
    
    guild_id = 202401190015
    session_id = 'orin'
    token = 'satori'
    sequence = 16655
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, guild_id, 202401190016)
        guild = Guild.precreate(guild_id, voice_states = [VoiceState(user_id = client.id, session_id = session_id)])
        voice_client._token = token
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway.sequence = sequence
        
        await gateway._resume()
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_RESUME,
                'd': {
                    'seq_ack': sequence,
                    'server_id': str(guild_id),
                    'session_id': session_id,
                    'token': token,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__select_protocol():
    """
    Tests whether ``DiscordGatewayVoice._select_protocol`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190017',
        client_id = 202401190018,
    )
    
    encryption_adapter_type = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize
    ip = 'hey'
    port = 'mister'
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190019, 202401190020)
        voice_client.prefer_encryption_mode_from_options([encryption_adapter_type.name])
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        await gateway._select_protocol(ip, port)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL,
                'd': {
                    'protocol': 'udp',
                    'data': {
                        'address': ip,
                        'port': port,
                        'mode': encryption_adapter_type.name,
                    },
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__terminate__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.terminate`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190021',
        client_id = 202401190022,
    )
    
    try:
        voice_client = VoiceClient(client, 202401190023, 202401190024)
        gateway = DiscordGatewayVoice(voice_client)
        
        await gateway.terminate()
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__terminate__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.terminate`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190025',
        client_id = 202401190026,
    )
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190027, 202401190028)
        gateway = DiscordGatewayVoice(voice_client)
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


async def test__DiscordGatewayVoice__close__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.close`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190029',
        client_id = 202401190030,
    )
    
    try:
        voice_client = VoiceClient(client, 202401190031, 202401190032)
        gateway = DiscordGatewayVoice(voice_client)
        
        await gateway.close()
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__close__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.close`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190033',
        client_id = 202401190034,
    )
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190035, 202401190036)
        gateway = DiscordGatewayVoice(voice_client)
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


async def test__DiscordGatewayVoice__abort__no_websocket_no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.abort`` works as intended.
    
    Case: no websocket & no kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190037',
        client_id = 202401190038,
    )
    
    try:
        voice_client = VoiceClient(client, 202401190039, 202401190040)
        gateway = DiscordGatewayVoice(voice_client)
        
        gateway.abort()
        
        vampytest.assert_eq(gateway._should_run, False)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__abort__with_websocket_with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice.abort`` works as intended.
    
    Case: with websocket & with kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401190041',
        client_id = 202401190042,
    )
    
    try:
        websocket = await TestWebSocketClient(KOKORO, '')
        voice_client = VoiceClient(client, 202401190043, 202401190044)
        gateway = DiscordGatewayVoice(voice_client)
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


async def test__DiscordGatewayVoice__connect__unexpected_closes_with_resume():
    """
    Tests whether ``DiscordGatewayVoice._connect`` works as intended.
    
    Case: Unexpectedly closed with resume.
    
    This function is a coroutine.
    """
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('ensure_open', True, ConnectionClosed(1000, None)),
        ],
    )

    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401190045',
        client_id = 202401190046,
        http = http,
    )
    
    session_id = 'okuu'
    endpoint = 'orin'
    token = 'satori'
    guild_id = 202401190047
    sequence = 1235
    
    try:
        voice_client = VoiceClient(client, guild_id, 202401190048)
        voice_client._endpoint = endpoint
        voice_client._token = token
        gateway = DiscordGatewayVoice(voice_client)
        gateway.sequence = sequence
        guild = Guild.precreate(guild_id, voice_states = [VoiceState(user_id = client.id, session_id = session_id)])
        
        output = await gateway._connect(True)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        match = GATEWAY_URL_REGEX.fullmatch(websocket.url)
        vampytest.assert_is_not(match, None)
        vampytest.assert_eq(match.group(1), endpoint)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, data = websocket.out_operations[0]
        
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {
                'op': GATEWAY_OPERATION_VOICE_RESUME,
                'd': {
                    'seq_ack': sequence,
                    'token': token,
                    'server_id': str(guild_id),
                    'session_id': session_id,
                },
            }
        )
        
        vampytest.assert_eq(gateway.sequence, -1)
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is(gateway.kokoro.runner, None)
        vampytest.assert_is(gateway.websocket, None)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__connect__success_default():
    """
    Tests whether ``DiscordGatewayVoice._connect`` works as intended.
    
    Case: Success default.
    
    This function is a coroutine.
    """
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
    )
    
    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401190049',
        client_id = 202401190050,
        http = http,
    )
    
    guild_id = 202401190051
    endpoint = 'orin'
    session_id = 'okuu'
    token = 'satori'
    
    try:
        voice_client = VoiceClient(client, guild_id, 202401190052)
        voice_client._endpoint = endpoint
        voice_client._token = token
        guild = Guild.precreate(guild_id, voice_states = [VoiceState(user_id = client.id, session_id = session_id)])
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._connect(False)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        match = GATEWAY_URL_REGEX.fullmatch(websocket.url)
        vampytest.assert_is_not(match, None)
        vampytest.assert_eq(match.group(1), 'orin')
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, data = websocket.out_operations[0]
        
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(data),
            {
                'op': GATEWAY_OPERATION_VOICE_IDENTIFY,
                'd': {
                    'seq_ack': -1,
                    'server_id': str(guild_id),
                    'user_id': str(client.id),
                    'session_id': session_id,
                    'token': token,
                },
            }
        )
        
        vampytest.assert_eq(gateway.sequence, -1)
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        vampytest.assert_is_not(gateway.websocket, None)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_users_connect__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_users_connect`` works as intended.
    
    This function is a coroutine.
    
    Case: no data.
    """
    client_id = 202408110005
    guild_id = 202408110006
    channel_id = 202408110007
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, guild_id, channel_id)
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_users_connect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_users_connect__with_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_users_connect`` works as intended.
    
    This function is a coroutine.
    
    Case: with data.
    """
    client_id = 202408110000
    guild_id = 202408110001
    channel_id = 202408110002
    user_id_0 = 202408110003
    user_id_1 = 202408110004
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    message = {
        'd': {
            'user_ids': [str(user_id_0), str(user_id_1)]
        },
    }
    
    try:
        voice_client = VoiceClient(client, guild_id, channel_id)
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_users_connect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_client_connect__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_client_connect`` works as intended.
    
    Case: no data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200000',
        client_id = 202401200001,
    )
    
    user_id = 202401200002
    source_id_0 = 566
    source_id_1 = 533
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401200003, 202401200004)
        
        voice_client._audio_sources[user_id] = source_id_0
        voice_client._video_sources[user_id] = source_id_1
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_client_connect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {user_id: source_id_0})
        vampytest.assert_eq(voice_client._video_sources, {user_id: source_id_1})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_client_connect__data_overwrite():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_client_connect`` works as intended.
    
    Case: With data, overwrite old.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200005',
        client_id = 202401200006,
    )
    
    user_id = 202401200007
    source_id_0 = 566
    source_id_1 = 533
    source_id_2 = 413
    source_id_3 = 369
    
    message = {
        'd': {
            'user_id': str(user_id),
            'audio_ssrc': source_id_2,
            'video_ssrc': source_id_3,
        },
    }
    
    try:
        voice_client = VoiceClient(client, 202401200008, 202401200009)
        
        voice_client._audio_sources[user_id] = source_id_0
        voice_client._video_sources[user_id] = source_id_1
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_client_connect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {user_id: source_id_2})
        vampytest.assert_eq(voice_client._video_sources, {user_id: source_id_3})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_session_description__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_session_description`` works as intended.
    
    Case: No data.
    
    This function is a coroutine.
    """

    client = Client(
        'token_202401200010',
        client_id = 202401200011,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401200013, 202401200014)
        
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        output = await gateway._handle_operation_session_description(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_instance(voice_client._encryption_adapter, EncryptionAdapterBase, accept_subtypes = False)
        vampytest.assert_eq(voice_client.is_connected(), False)
        
        vampytest.assert_eq(len(websocket.out_operations), 0)
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_session_description__with_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_session_description`` works as intended.
    
    Case: No data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200015',
        client_id = 202401200016,
    )
    
    encryption_adapter_type = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize
    secret_key = b'hey mister' + b'0' * 22
    
    message = {
        'd': {
            'mode': EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.name,
            'secret_key': [*secret_key]
        },
    }
    
    def mock_SecretBox(value):
        nonlocal secret_key
        vampytest.assert_eq(value, secret_key)
        return SecretBox(value)
    
    
    try:
        voice_client = VoiceClient(client, 202401200017, 202401200018)
        
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        mocked = vampytest.mock_globals(
            type(gateway)._handle_operation_session_description,
            SecretBox = mock_SecretBox,
        )
        
        output = await mocked(gateway, message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_instance(voice_client._encryption_adapter, encryption_adapter_type)
        vampytest.assert_eq(voice_client._encryption_adapter.key, secret_key)
        vampytest.assert_is(voice_client._encryption_adapter_type, encryption_adapter_type)
        
        vampytest.assert_eq(voice_client.is_connected(), True)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_SPEAKING,
                'd': {
                    'speaking': False,
                    'delay': 0,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_speaking__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_speaking`` works as intended.
    
    Case: no data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200019',
        client_id = 202401200020,
    )
    
    user_id = 202401200021
    source_id_0 = 566
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401200022, 202401200023)
        
        voice_client._audio_sources[user_id] = source_id_0
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_speaking(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {user_id: source_id_0})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_speaking__data_overwrite():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_speaking`` works as intended.
    
    Case: With data, overwrite old.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200024',
        client_id = 202401200025,
    )
    
    user_id = 202401200026
    source_id_0 = 566
    source_id_1 = 533
    
    message = {
        'd': {
            'user_id': str(user_id),
            'ssrc': source_id_1,
        },
    }
    
    try:
        voice_client = VoiceClient(client, 202401200027, 202401200028)
        
        voice_client._audio_sources[user_id] = source_id_0
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_speaking(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {user_id: source_id_1})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_client_disconnect__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_client_disconnect`` works as intended.
    
    Case: no data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200029',
        client_id = 20240120030,
    )
    
    user_id = 202401200021
    source_id_0 = 566
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401200031, 202401200032)
        
        voice_client._audio_sources[user_id] = source_id_0
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_client_disconnect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {user_id: source_id_0})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_client_disconnect__with_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_client_disconnect`` works as intended.
    
    Case: With data, remove old.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200033',
        client_id = 202401200034,
    )
    
    user_id = 202401200026
    source_id_0 = 566
    source_id_1 = 533
    
    message = {
        'd': {
            'user_id': str(user_id),
        },
    }
    
    try:
        voice_client = VoiceClient(client, 202401200035, 202401200036)
        
        voice_client._audio_sources[user_id] = source_id_0
        voice_client._video_sources[user_id] = source_id_1
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_client_disconnect(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_sources, {})
        vampytest.assert_eq(voice_client._video_sources, {})
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_ready__no_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_ready`` works as intended.
    
    Case: No data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200037',
        client_id = 202401200038,
    )
    
    message = {
        'data': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401200039, 202401200040)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_ready(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_ready__with_data():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_ready`` works as intended.
    
    Case: No data.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401200039',
        client_id = 202401200040,
    )
    
    audio_source = 123
    endpoint_port = 123
    endpoint_ip = 'orin'
    
    voice_client_ip = 'hey mister'
    voice_client_port = 432
    encryption_adapter_type = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize
    
    message = {
        'd': {
            'ssrc': audio_source,
            'port': endpoint_port,
            'ip': endpoint_ip,
            'modes': [encryption_adapter_type.name],
        },
    }
    
    class mock_transport:
        __slots__ = ('sent',)
        
        def __new__(cls):
            self = object.__new__(cls)
            self.sent = []
            return self
        
        
        def send_to(self, packet, address):
            self.sent.append((packet, address),)
    
    
    class mock_protocol:
        __slots__ = ('retrieve',)
        
        def __new__(cls, retrieve):
            retrieve.reverse()
            self = object.__new__(cls)
            self.retrieve = retrieve
            return self
        
        
        async def read(self, amount):
            value = self.retrieve.pop(0)
            vampytest.assert_eq(len(value), amount)
            return value
        
        
        def close(self):
            pass
        
        def cancel_current_reader(self):
            pass
    
    try:
        voice_client = VoiceClient(client, 202401200041, 202401200042)
        voice_client._transport = mock_transport()
        voice_client._protocol = mock_protocol([
            b''.join([
                b'\x00' * 8,
                voice_client_ip.encode(),
                b'\x00' * (64 - len(voice_client_ip)),
                voice_client_port.to_bytes(2, 'big'),
            ])
        ])
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        output = await gateway._handle_operation_ready(message)
        
        vampytest.assert_eq(
            voice_client._transport.sent,
            [
                (
                    b''.join([b'\x00\x01\x00\x46', audio_source.to_bytes(4, 'big'), b'\x00' * (64 + 2)]),
                    (endpoint_ip, endpoint_port),
                ),
            ],
        )
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(voice_client._audio_source, audio_source)
        vampytest.assert_eq(voice_client._endpoint_ip, endpoint_ip)
        vampytest.assert_eq(voice_client._endpoint_port, endpoint_port)
        vampytest.assert_eq(voice_client._ip, voice_client_ip)
        vampytest.assert_eq(voice_client._port, voice_client_port)
        vampytest.assert_is(voice_client._encryption_adapter_type, encryption_adapter_type)
        
        vampytest.assert_eq(len(websocket.out_operations), 2)
        
        operation, sent_data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL,
                'd': {
                    'protocol': 'udp',
                    'data': {
                        'address': voice_client_ip,
                        'port': voice_client_port,
                        'mode': encryption_adapter_type.name,
                    },
                },
            }
        )
    
        operation, sent_data = websocket.out_operations[1]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(
            from_json(sent_data),
            {
                'op': GATEWAY_OPERATION_VOICE_CLIENT_CONNECT,
                'd': {
                    'audio_ssrc': audio_source,
                    'video_ssrc': 0,
                    'rtx_ssrc': 0,
                },
            }
        )
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_ready__no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_ready`` works as intended.
    
    Case: No kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210000',
        client_id = 202401210001,
    )
    
    audio_source = 123
    endpoint_port = 123
    endpoint_ip = 'orin'
    
    message = {
        'd': {
            'ssrc': audio_source,
            'port': endpoint_port,
            'ip': endpoint_ip,
        }
    }
    
    try:
        voice_client = VoiceClient(client, 202401210002, 202401210003)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_ready(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_hello__no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_hello`` works as intended.
    
    Case: No kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210004',
        client_id = 202401210005,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401210006, 202401210007)
        
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        
        output = await gateway._handle_operation_hello(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(from_json(data)['op'], GATEWAY_OPERATION_VOICE_HEARTBEAT)
        
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_hello__with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_hello`` works as intended.
    
    Case: With kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210008',
        client_id = 202401210009,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401210010, 202401210011)
        
        websocket = await TestWebSocketClient(KOKORO, '')
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        # skip 1 cycle to wait for kokoro to come up.
        await skip_ready_cycle()
        
        output = await gateway._handle_operation_hello(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_eq(len(websocket.out_operations), 1)
        
        operation, data = websocket.out_operations[0]
        vampytest.assert_eq(operation, 'send')
        vampytest.assert_eq(from_json(data)['op'], GATEWAY_OPERATION_VOICE_HEARTBEAT)
        
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_heartbeat_acknowledge__no_kokoro():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_heartbeat_acknowledge`` works as intended.
    
    Case: No kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210012',
        client_id = 202401210013,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401210014, 202401210015)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_heartbeat_acknowledge(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_ne(gateway.latency, LATENCY_DEFAULT)
        
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_heartbeat_acknowledge__with_kokoro():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_heartbeat_acknowledge`` works as intended.
    
    Case: With kokoro.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210016',
        client_id = 202401210017,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401210018, 202401210019)
        
        gateway = DiscordGatewayVoice(voice_client)
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        # skip 1 cycle to wait for kokoro to come up.
        await skip_ready_cycle()
        
        output = await gateway._handle_operation_heartbeat_acknowledge(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        vampytest.assert_ne(gateway.latency, LATENCY_DEFAULT)
        
        vampytest.assert_is_not(gateway.kokoro, None)
        vampytest.assert_is_not(gateway.kokoro.runner, None)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_operation_resumed():
    """
    Tests whether ``DiscordGatewayVoice._handle_operation_resumed`` works as intended.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210020',
        client_id = 202401210021,
    )
    
    message = {
        'd': None,
    }
    
    try:
        voice_client = VoiceClient(client, 202401210022, 202401210023)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_operation_resumed(message)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_received_operation__known_operation():
    """
    Tests whether ``DiscordGatewayVoice._handle_received_operation`` works as intended.
    
    Case: Known operation.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210028',
        client_id = 202401210029,
    )
    
    operation = 999
    sequence = 123
    
    message = {
        'op': operation,
        'd': {
            'hey': 'mister',
        },
        'seq': sequence,
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
        voice_client = VoiceClient(client, 202401210030, 202401210032)
        
        gateway = DiscordGatewayVoice(voice_client)
        gateway._operation_handlers[operation] = mock_operation_handler
        
        output = await gateway._handle_received_operation(to_json(message))
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_RESUME)
        
        vampytest.assert_true(mock_operation_handler_called)
        vampytest.assert_eq(gateway.sequence, sequence)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__handle_received_operation__unknown_operation():
    """
    Tests whether ``DiscordGatewayVoice._handle_received_operation`` works as intended.
    
    Case: not known operation.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210032',
        client_id = 202401210033,
    )
    
    operation = 999
    data = {'hey': 'mister'}
    
    message = {
        'op': operation,
        'd': data,
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
        
        voice_client = VoiceClient(client, 202401210034, 202401210035)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._handle_received_operation(to_json(message))
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_KEEP_GOING)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(error_event_handler_called)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__poll_and_handle_received_operation__no_websocket():
    """
    Tests whether ``DiscordGatewayVoice._poll_and_handle_received_operation`` works as intended.
    
    Case: no websocket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210036',
        client_id = 202401210037,
    )
    
    try:
        voice_client = VoiceClient(client, 202401210038, 202401210039)
        
        gateway = DiscordGatewayVoice(voice_client)
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__poll_and_handle_received_operation__with_websocket():
    """
    Tests whether ``DiscordGatewayVoice._poll_and_handle_received_operation`` works as intended.
    
    Case: with websocket.
    
    This function is a coroutine.
    """
    client = Client(
        'token_202401210040',
        client_id = 202401210041,
    )
    
    operation = 999
    
    message = {
        'op': operation,
        'd': {
            'hey': 'mister',
        },
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
        voice_client = VoiceClient(client, 202401210042, 202401210043)
        
        websocket = await TestWebSocketClient(
            KOKORO,
            '',
            in_operations = [
                ('receive', False, to_json(message)),
            ]
        )
        gateway = DiscordGatewayVoice(voice_client)
        gateway._operation_handlers[operation] = mock_operation_handler
        gateway.websocket = websocket
        
        output = await gateway._poll_and_handle_received_operation()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_RESUME)
        
        vampytest.assert_true(mock_operation_handler_called)
        
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__keep_polling_and_handling():
    """
    Tests whether ``DiscordGatewayVoice._keep_polling_and_handling`` works as intended.
    
    This function is a coroutine.
    """
    message_0 = {
        'op': GATEWAY_OPERATION_VOICE_HELLO,
        'd': None,
    }
    
    data_0 = to_json(message_0)
    data_1 = to_json(message_0)
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
        'token_202401210044',
        client_id = 202401210045,
    )
    
    try:
        voice_client = VoiceClient(client, 202401210046, 202401210047)
        gateway = DiscordGatewayVoice(voice_client)
        gateway.websocket = websocket
        gateway._create_kokoro()
        gateway.kokoro.start()
        
        # Let kokoro to stand up
        await skip_ready_cycle()
        
        output = await gateway._keep_polling_and_handling()
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, GATEWAY_ACTION_CONNECT)
        
        vampytest.assert_eq(len(websocket.out_operations), 2)
        
        for index in range(2):
            operation, sent_data = websocket.out_operations[0]
            vampytest.assert_eq(operation, 'send')
            vampytest.assert_eq(from_json(sent_data)['op'], GATEWAY_OPERATION_VOICE_HEARTBEAT)
    
    finally:
        client._delete()
        client = None


async def test__DiscordGatewayVoice__run__default():
    """
    Tests whether ``DiscordGatewayVoice.run`` works as intended.
    
    Case: Only testing a simple case. Feeling tired of writing more tests for this type.
    """
    exception = RuntimeError('hiss')
    
    websocket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', True, exception)
        ],
    )
    
    http = TestHTTPClient(KOKORO, out_websocket = websocket)
    
    client = Client(
        'token_202401210048',
        client_id = 202401210049,
        http = http,
    )
    
    waiter = Future(KOKORO)
    
    try:
        voice_client = VoiceClient(client, 202401210050, 202401210051)
        voice_client.running = True
        gateway = DiscordGatewayVoice(voice_client)
        
        with vampytest.assert_raises(exception):
            await gateway.run(waiter)
        
        output = waiter.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        client._delete()
        client = None


def test__DiscordGatewayVoice__clear_session():
    """
    Tests whether ``DiscordGatewayVoice._clear_session`` works as intended.
    """
    client_id = 202409040070
    client = Client(
        'token_' + str(202409040070),
        client_id = 202409040070,
    )
    
    try:
        gateway = DiscordGatewayVoice(client)
        gateway.sequence = 56
        
        gateway._clear_session()
        
        vampytest.assert_eq(gateway.sequence, -1)
    finally:
        client._delete()
        client = None
