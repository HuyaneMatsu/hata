__all__ = ()

from time import perf_counter

from scarletio import Task, copy_docs, from_json, repeat_timeout, sleep, to_json
from scarletio.web_common import ConnectionClosed, InvalidHandshake, URL, WebSocketProtocolError

from ..core import KOKORO

from .constants import (
    GATEWAY_ACTION_CONNECT, GATEWAY_ACTION_KEEP_GOING, GATEWAY_ACTION_RESUME, GATEWAY_CONNECT_TIMEOUT,
    GATEWAY_OPERATION_VOICE_CLIENT_CONNECT, GATEWAY_OPERATION_VOICE_CLIENT_DISCONNECT, GATEWAY_OPERATION_VOICE_FLAGS,
    GATEWAY_OPERATION_VOICE_HEARTBEAT, GATEWAY_OPERATION_VOICE_HEARTBEAT_ACKNOWLEDGE, GATEWAY_OPERATION_VOICE_HELLO,
    GATEWAY_OPERATION_VOICE_IDENTIFY, GATEWAY_OPERATION_VOICE_PLATFORM, GATEWAY_OPERATION_VOICE_READY,
    GATEWAY_OPERATION_VOICE_RESUME, GATEWAY_OPERATION_VOICE_RESUMED, GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL,
    GATEWAY_OPERATION_VOICE_SESSION_DESCRIPTION, GATEWAY_OPERATION_VOICE_SPEAKING,
    GATEWAY_OPERATION_VOICE_USERS_CONNECT, GATEWAY_OPERATION_VOICE_VIDEO_SESSION_DESCRIPTION,
    GATEWAY_OPERATION_VOICE_VIDEO_SINK, LATENCY_DEFAULT, POLL_TIMEOUT
)
from .heartbeat import Kokoro
from .rate_limit import GatewayRateLimiter
from .voice_base import DiscordGatewayVoiceBase


async def _handle_operation_dummy(gateway, data):
    """
    Dummy operation handler.
    
    Parameters
    ----------
    gateway : ``DiscordGatewayVoice``
        The gateway receiving the operation.
    data : `None | dict<str, object>`
        The received data.
    
    Returns
    -------
    gateway_action : `int`
    """
    return GATEWAY_ACTION_KEEP_GOING


class DiscordGatewayVoice(DiscordGatewayVoiceBase):
    """
    The gateway used by ``VoiceClient``-s to communicate with Discord with secure web socket.
    
    Attributes
    ----------
    _operation_handlers : `dict<int, (instance, dict<str, object>) -> int>`
        Handler for each expected operation.
    
    _should_run : `bool`
        Whether the gateway should be running.
    
    kokoro : `None | Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    
    sequence : `int`
        Last sequence number received.
    
    voice_client : ``VoiceClient``
        The owner voice client of the gateway.
    
    web_socket : `None`, ``WebSocketClient``
        The web socket of the gateway.
    """
    __slots__ = (
        '_operation_handlers', '_should_run', 'kokoro', 'rate_limit_handler', 'sequence', 'voice_client', 'web_socket'
    )
    
    def __new__(cls, voice_client):
        """
        Creates a voice gateway with it's default attributes.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The owner voice_client of the gateway.
        """
        operation_handlers = {
            # GATEWAY_OPERATION_VOICE_IDENTIFY: send only
            # GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL: send only
            GATEWAY_OPERATION_VOICE_READY: cls._handle_operation_ready,
            # GATEWAY_OPERATION_VOICE_HEARTBEAT: send only
            GATEWAY_OPERATION_VOICE_SESSION_DESCRIPTION: cls._handle_operation_session_description,
            GATEWAY_OPERATION_VOICE_SPEAKING: cls._handle_operation_speaking,
            GATEWAY_OPERATION_VOICE_HEARTBEAT_ACKNOWLEDGE: cls._handle_operation_heartbeat_acknowledge,
            # GATEWAY_OPERATION_VOICE_RESUME: send only 
            GATEWAY_OPERATION_VOICE_HELLO: cls._handle_operation_hello,
            GATEWAY_OPERATION_VOICE_RESUMED: cls._handle_operation_resumed,
            GATEWAY_OPERATION_VOICE_USERS_CONNECT: cls._handle_operation_users_connect,
            GATEWAY_OPERATION_VOICE_CLIENT_CONNECT: cls._handle_operation_client_connect,
            GATEWAY_OPERATION_VOICE_CLIENT_DISCONNECT: cls._handle_operation_client_disconnect,
            GATEWAY_OPERATION_VOICE_VIDEO_SESSION_DESCRIPTION: _handle_operation_dummy,
            GATEWAY_OPERATION_VOICE_VIDEO_SINK: _handle_operation_dummy,
            GATEWAY_OPERATION_VOICE_FLAGS: _handle_operation_dummy,
            GATEWAY_OPERATION_VOICE_PLATFORM: _handle_operation_dummy,
        }
        
        self = object.__new__(cls)
        self._operation_handlers = operation_handlers
        self._should_run = False
        self.kokoro = None
        self.rate_limit_handler = GatewayRateLimiter()
        self.sequence = -1
        self.voice_client = voice_client
        self.web_socket = None
        return self
    
    
    def _create_kokoro(self):
        """
        Creates the gateway's ``.kokoro``.
        """
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = Kokoro(self)
        else:
            kokoro.stop()
    
    
    @copy_docs(DiscordGatewayVoiceBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(' voice_client = ')
        repr_parts.append(repr(self.voice_client))

    
    @property
    @copy_docs(DiscordGatewayVoiceBase.latency)
    def latency(self):
        kokoro = self.kokoro
        if kokoro is None:
            latency = LATENCY_DEFAULT
        else:
            latency = kokoro.latency
        return latency
    
    
    @copy_docs(DiscordGatewayVoiceBase.send_as_json)
    async def send_as_json(self, data):
        web_socket = self.web_socket
        if web_socket is None:
            return
        
        if not (await self.rate_limit_handler):
            return
        
        try:
            await web_socket.send(to_json(data))
        except ConnectionClosed:
            pass
    
    
    @copy_docs(DiscordGatewayVoiceBase.beat)
    async def beat(self):
        data = {
            'op': GATEWAY_OPERATION_VOICE_HEARTBEAT,
            'd': {
                't': int(perf_counter() * 1000),
                'seq_ack': self.sequence,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _voice_client_connect(self):
        """
        Sends a voice client connect packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.voice_client
        data = {
            'op': GATEWAY_OPERATION_VOICE_CLIENT_CONNECT,
            'd': {
                'audio_ssrc': voice_client._audio_source,
                'video_ssrc': voice_client._video_source,
                'rtx_ssrc': 0,
            }
        }
        
        await self.send_as_json(data)
    
    
    @copy_docs(DiscordGatewayVoiceBase.set_speaking)
    async def set_speaking(self, speaking):
        data = {
            'op': GATEWAY_OPERATION_VOICE_SPEAKING,
            'd': {
                'speaking': speaking,
                'delay': 0,
            },
        }
        
        await self.send_as_json(data)
    
    
    def _get_session_id(self):
        """
        Gets the session identifier of the connections.
        
        Returns
        -------
        session_id : `str`
        """
        voice_state = self.voice_client.voice_state
        if voice_state is None:
            session_id = ''
        else:
            session_id = voice_state.session_id
        
        return session_id
    
    
    async def _identify(self):
        """
        Sends an identify packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.voice_client
        
        data = {
            'op': GATEWAY_OPERATION_VOICE_IDENTIFY,
            'd': {
                'seq_ack': self.sequence,
                'server_id': str(voice_client.guild_id),
                'session_id': self._get_session_id(),
                'token': voice_client._token,
                'user_id': str(voice_client.client.id),
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _resume(self):
        """
        Sends a resume packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.voice_client
        
        data = {
            'op': GATEWAY_OPERATION_VOICE_RESUME,
            'd': {
                'seq_ack': self.sequence,
                'server_id': str(voice_client.guild_id),
                'session_id': self._get_session_id(),
                'token': voice_client._token,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _select_protocol(self, ip, port):
        """
        Sends a select protocol packet to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        ip : `str`
            The received ip of the voice voice_client to use.
        port : `int`
            The received port of the voice voice_client to use.
        """
        data = {
            'op': GATEWAY_OPERATION_VOICE_SELECT_PROTOCOL,
            'd': {
                'protocol': 'udp',
                'data': {
                    'address': ip,
                    'port': port,
                    'mode': self.voice_client.get_encryption_mode(),
                },
            },
        }
        
        await self.send_as_json(data)
    
    
    def _cancel_self_and_get_web_socket(self):
        """
        Cancels the gateway except its web socket. Returns the web socket if still running instead.
        
        Returns
        -------
        web_socket : `None | WebSocketClient`
        """
        kokoro = self.kokoro
        if (kokoro is not None):
            kokoro.stop()
        
        web_socket = self.web_socket
        if web_socket is None:
            return None
        
        self.web_socket = None
        
        if web_socket.closed:
            return None
        
        return web_socket
    
    
    @copy_docs(DiscordGatewayVoiceBase.terminate)
    async def terminate(self):
        web_socket = self._cancel_self_and_get_web_socket()
        if (web_socket is not None):
            await web_socket.close(4000)
    
    
    @copy_docs(DiscordGatewayVoiceBase.close)
    async def close(self):
        web_socket = self._cancel_self_and_get_web_socket()
        if (web_socket is not None):
            await web_socket.close(1000)
    
    
    @copy_docs(DiscordGatewayVoiceBase.abort)
    def abort(self):
        web_socket = self._cancel_self_and_get_web_socket()
        if (web_socket is not None):
            web_socket.close_transport(True)
        
        self._should_run = False
    
    
    async def _connect(self, resume):
        """
        Connects the gateway to Discord. If the connecting was successful, will start it's `.kokoro` as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        resume : `bool`
            Whether the gateway should try to resume the existing connection.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionError
        OSError
        ValueError
        ConnectionClosed
        InvalidHandshake
        WebSocketProtocolError
        """
        self._create_kokoro()
        
        web_socket = self.web_socket
        if (web_socket is not None) and (not web_socket.closed):
            self.web_socket = None
            await web_socket.close(4000)
        
        gateway_url = URL(f'wss://{self.voice_client._endpoint}/?v=8', True)
        self.web_socket = await self.voice_client.client.http.connect_web_socket(gateway_url)
        self.kokoro.start()
        
        if not resume:
            await self._identify()
            return GATEWAY_ACTION_KEEP_GOING
        
        await self._resume()
        
        try:
            await self.web_socket.ensure_open()
        except ConnectionClosed:
            # web_socket got closed so let's just do a regular connect.
            self._clear_session()
            self.kokoro.stop()
            self.web_socket = None
            return GATEWAY_ACTION_CONNECT
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_users_connect(self, message):
        # Dont know what to do with the payload currently.
        # It looks like:
        # message = {'op': 11, 'd': {'user_ids': ['22221231231231231231']}}
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_client_connect(self, message):
        """
        Handles a voice client connect gateway operation.
        Note that not we are connecting, but someone else.
        
        This function is a coroutine.
        
        Parameters
        ----------
        data : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        user_id = int(data['user_id'])
        voice_client = self.voice_client
        
        try:
            audio_source = data['audio_ssrc']
        except KeyError:
            pass
        else:
            voice_client._update_audio_source(user_id, audio_source)
        
        try:
            video_source = data['video_ssrc']
        except KeyError:
            pass
        else:
            voice_client._update_video_source(user_id, video_source)
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_session_description(self, message):
        """
        Handles a voice session description operation.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        voice_client = self.voice_client
        voice_client.set_encryption_mode(data['mode'], bytes(data['secret_key']))
        
        await self.set_speaking(voice_client.speaking)
        
        voice_client.set_connected()
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_speaking(self, message):
        """
        Handles a speaking operation.
        Note that not we are speaking, but someone else.
        
        This function is a coroutine.
        
        Parameters
        ----------
        data : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        user_id = int(data['user_id'])
        audio_source = data['ssrc']
        self.voice_client._update_audio_source(user_id, audio_source)
        return GATEWAY_ACTION_KEEP_GOING

    
    async def _handle_operation_client_disconnect(self, message):
        """
        Handles a client disconnect operation.
        Note that not we are disconnecting, but someone else.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        voice_client = self.voice_client
        
        user_id = int(data['user_id'])
        voice_client._remove_audio_source(user_id)
        voice_client._remove_video_source(user_id)
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_ready(self, message):
        """
        Handles a ready operation and selects protocol with `._select_protocol`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        data = message.get('d', None)
        if data is None:
            return GATEWAY_ACTION_KEEP_GOING
        
        kokoro = self.kokoro
        if (kokoro is None) or (kokoro.runner is None):
            return GATEWAY_ACTION_CONNECT
        
        # ignore setting heartbeat interval
        # kokoro.interval = data['heartbeat_interval'] / 1000.0
        
        voice_client = self.voice_client
        audio_source = data['ssrc']
        voice_client._audio_source = audio_source
        voice_client._endpoint_ip = data['ip']
        voice_client._endpoint_port = data['port']
        voice_client.prefer_encryption_mode_from_options(data['modes'])
        
        # data structure
        # byte  0 -  2 : `version` -> we send 1
        # byte  2 -  4 : `length` -> 70 (this excluded type and length)
        # byte  4 -  8 : `audio_source` value as unsigned integer
        # byte  8 - 72 : `ip` null terminated string, receive only but still have to send for some weird reason?
        # byte 72 - 74 : `port` as integer, receive only, but still have to send for some weird reason?
        packet = b''.join([b'\x00\x01\x00\x46', audio_source.to_bytes(4, 'big'), b'\x00' * 66])
        
        voice_client.send_packet(packet)
        
        protocol = voice_client._protocol
        # Make sure, that the voice voice client's reader do not wanna read our data away from us.
        protocol.cancel_current_reader()
        
        received = await protocol.read(74)
        
        ip_end = received.index(0, 8)
        if ip_end == -1:
            ip_end = 72
        elif ip_end > 72:
            ip_end = 72
        
        ip = received[8 : ip_end].decode('ascii')
        voice_client._ip = ip
        
        # port is last 2 bytes
        port = int.from_bytes(received[72 : 74], 'big')
        voice_client._port = port
        
        await self._select_protocol(ip, port)
        await self._voice_client_connect()
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_hello(self, message):
        """
        Handles a hello operation.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received data.
        
        Returns
        -------
        gateway_action : `int`
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = Kokoro(self)
            self.kokoro = kokoro
        
        # ignore setting heartbeat interval
        # kokoro.interval = data['heartbeat_interval'] / 1000.0
        
        # beat now calls `.start` since it has to check the current state
        await kokoro.beat_now()
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_heartbeat_acknowledge(self, message):
        """
        Handles a heart beat acknowledge operation.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = Kokoro(self)
            self.kokoro = kokoro
            # `.answered` is not calling `.start` 
            kokoro.start()
            
        kokoro.answered()
        
        return GATEWAY_ACTION_KEEP_GOING
    
    
    async def _handle_operation_resumed(self, message):
        """
        Handles a resumed operation. Called after the gateway was resumed successfully. We do nothing.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `dict<str, object>`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        return GATEWAY_ACTION_KEEP_GOING

    
    async def _handle_received_operation(self, message):
        """
        Processes the message sent by Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `str`
            The received message.
        
        Returns
        -------
        gateway_action : `int`
        """
        message = from_json(message)
        
        sequence = message.get('seq', None)
        if (sequence is not None):
            self.sequence = sequence
        
        operation = message['op']
        
        try:
            operation_handler = self._operation_handlers[operation]
        except KeyError:
            client = self.voice_client.client
            Task(
                KOKORO,
                client.events.error(
                    client,
                    f'{type(self).__name__}._handle_received_operation',
                    f'Unknown operation: {operation!r}\nMessage: {message!r}'
                ),
            )
            return GATEWAY_ACTION_KEEP_GOING
        
        return (await operation_handler(self, message))
    
    
    async def _poll_and_handle_received_operation(self):
        """
        Waits to receive a message from Discord, then calls ``._handle_received_operation``.
        
        This method is a coroutine.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionClosed
            If the web_socket connection closed.
        """
        web_socket = self.web_socket
        if web_socket is None:
            return GATEWAY_ACTION_CONNECT
        
        message = await web_socket.receive()
        return await self._handle_received_operation(message)
    
    
    async def _keep_polling_and_handling(self):
        """
        Keeps polling and handling till decided otherwise.
        
        This function is a coroutine.
        
        Returns
        -------
        gateway_action : `int`
        
        Raises
        ------
        ConnectionClosed
            If the web_socket connection closed.
        """
        try:
            with repeat_timeout(POLL_TIMEOUT) as loop:
                for _ in loop:
                    action = await self._poll_and_handle_received_operation()
                    if action != GATEWAY_ACTION_KEEP_GOING:
                        return action
        
        except TimeoutError:
            # timeout, no internet probably.
            pass
        
        return GATEWAY_ACTION_CONNECT
    
    
    @copy_docs(DiscordGatewayVoiceBase.run)
    async def run(self, waiter = None):
        self._should_run = True
        voice_client = self.voice_client
        action = GATEWAY_ACTION_CONNECT
        
        try:
            while True:
                voice_client.clear_connected()
                if (not self._should_run) or (not voice_client.running):
                    return False
                
                try:
                    task = Task(KOKORO, self._connect(action == GATEWAY_ACTION_RESUME))
                    task.apply_timeout(GATEWAY_CONNECT_TIMEOUT)
                    action = await task
                    
                    if action != GATEWAY_ACTION_KEEP_GOING:
                        continue
                    
                    if (waiter is not None):
                        waiter.set_result_if_pending(True)
                        waiter = None
                    
                    action = await self._keep_polling_and_handling()
                
                except GeneratorExit:
                    self.abort()
                    return False
                
                except TimeoutError:          
                    pass
                
                except (ConnectionError, InvalidHandshake, OSError, ValueError, WebSocketProtocolError) as exception:
                    from scarletio import write_exception_async
                    await write_exception_async(exception)
                    
                    # We are not connected anymore, clear connection waiter.
                    voice_client.clear_connected()
                    await sleep(1.0, KOKORO)
                
                else:
                    continue
        
        except:
            raise
        
        finally:
            if (waiter is not None):
                waiter.set_result_if_pending(False)
                waiter = None
            
            # we are not running anymore.
            self._should_run = False
        
        return False
    
    
    def _clear_session(self):
        """
        Clears current session data, disabling the option of resuming the connection.
        """
        self.sequence = -1
