__all__ = ()

from time import time as time_now

try:
    import nacl.secret
except ImportError:
    SecretBox = None
else:
    SecretBox = nacl.secret.SecretBox
    del nacl

from ...backend.exceptions import ConnectionClosed
from ...backend.utils import to_json, from_json

from ..exceptions import VOICE_CLIENT_DISCONNECT_CLOSE_CODE

from .heartbeat import Kokoro
from .rate_limit import GatewayRateLimiter


IDENTIFY = 0
SELECT_PROTOCOL = 1
READY = 2
HEARTBEAT = 3
SESSION_DESCRIPTION = 4
SPEAKING = 5
HEARTBEAT_ACK = 6
RESUME = 7
HELLO = 8
INVALIDATE_SESSION = 9
CLIENT_CONNECT = 12
CLIENT_DISCONNECT = 13
VIDEO_SESSION_DESCRIPTION = 14
VIDEO_SINK = 15

"""
IDENTIFY : `int` = `0`
    Send only, used at ``._identify``.
SELECT_PROTOCOL : `int` = `1`
    Send only, used at ``._select_protocol``.
READY : `int` = `2`
    Receive only, used at ``._initial_connection``.
HEARTBEAT : `int` = `3`
    Send only, used at ``._beat``.
SESSION_DESCRIPTION : `int` = `4`
    Receive only, used at ``._received_message``.
SPEAKING : `int` = `5`
    Send and receive, used at ``._set_speaking`` and at ``._received_message``.
HEARTBEAT_ACK : `int` = `6`
    Receive only, used at ``._received_message``.
RESUME : `int` = `7`
    Send only, used at ``._resume``.
HELLO : `int` = `8`
    Receive only, used at ``._received_message``.
INVALIDATE_SESSION : `int` = `9`
    Receive only, used at ``._received_message``.
CLIENT_CONNECT : `int` = `12`
    Receive only, used at ``._received_message``.
CLIENT_DISCONNECT : `int` = `13`
    Receive only, used at ``._received_message``.
VIDEO_SESSION_DESCRIPTION : `int` = `14`
    Receive only. Not used.
VIDEO_SINK : `int` = `15`
    Receive and send, not used.
"""

class DiscordGatewayVoice:
    """
    The gateway used by ``VoiceClient``-s to communicate with Discord with secure websocket.
    
    Attributes
    ----------
    client : ``VoiceClient``
        The owner voice client of the gateway.
    kokoro : `None` or `Kokoro`
        The heart of the gateway, sends beat-data at set intervals. If does not receives answer in time, restarts
        the gateway.
    rate_limit_handler : ``GatewayRateLimiter``
        The rate limit handler of the gateway.
    websocket : `None` or `WSClient`
        The websocket client of the gateway.
    """
    __slots__ = ('client', 'kokoro', 'rate_limit_handler', 'websocket')
    
    def __init__(self, voice_client):
        """
        Creates a voice gateway with it's default attributes.
        
        Parameters
        ----------
        client : ``VoiceClient``
            The owner client of the gateway.
        """
        self.websocket = None
        self.client = voice_client
        
        self.kokoro = None
        self.rate_limit_handler = GatewayRateLimiter()
    
    
    async def start(self):
        """
        Starts the gateway's ``.kokoro``.
        
        This method is a coroutine.
        """
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = await Kokoro(self)
        else:
            await kokoro.restart()
    
    # connecting, message receive and processing
    
    async def connect(self, resume=False):
        """
        Connects the gateway to Discord. If the connecting was successful, will start it's `.kokoro` as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        resume : `bool`
            Whether the gateway should try to resume the existing connection.
        
        Raises
        ------
        ConnectionError
        OSError
        ValueError
        ConnectionClosed
        InvalidHandshake
        WebSocketProtocolError
        """
        kokoro = self.kokoro
        if (kokoro is not None):
            kokoro.terminate()
            del kokoro
        
        websocket = self.websocket
        if (websocket is not None) and (not websocket.closed):
            await websocket.close(4000)
            self.websocket = None
        
        gateway = f'wss://{self.client._endpoint}/?v=4'
        self.websocket = await self.client.client.http.connect_ws(gateway)
        
        kokoro = self.kokoro
        if kokoro is None:
            self.kokoro = kokoro = await Kokoro(self)
        kokoro.start_beating()
        del kokoro
        
        if resume:
            await self._resume()
        else:
            await self._identify()
    
    
    async def _poll_event(self):
        """
        Waits to receive a message from Discord, then calls ``._received_message``.
        
        This method is a coroutine.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        ConnectionClosed
            If the websocket is already closed. Can happen when destroying ghost clients.
        """
        websocket = self.websocket
        if websocket is None:
            raise ConnectionClosed(VOICE_CLIENT_DISCONNECT_CLOSE_CODE, None)
        
        message = await websocket.receive()
        await self._received_message(message)
    
    
    async def _received_message(self, message):
        """
        Processes the message sent by Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : `bytes`
            The received message.
        
        Raises
        ------
        TimeoutError
            If the gateways's `.kokoro` is not beating, meanwhile it should.
        """
        message = from_json(message)
        
        operation = message['op']
        try:
            data = message['d']
        except KeyError:
            data = None
        
        if operation == CLIENT_CONNECT:
            user_id = int(data['user_id'])
            try:
                audio_source = data['audio_ssrc']
            except KeyError:
                pass
            else:
                self.client._update_audio_source(user_id, audio_source)
            
            try:
                video_source = data['video_ssrc']
            except KeyError:
                pass
            else:
                self.client._update_video_source(user_id, video_source)
            
            return
        
        if operation == SPEAKING:
            user_id = int(data['user_id'])
            audio_source = data['ssrc']
            self.client._update_audio_source(user_id, audio_source)
            return
        
        if operation == CLIENT_DISCONNECT:
            user_id = int(data['user_id'])
            self.client._remove_source(user_id)
            return
        
        kokoro = self.kokoro
        if kokoro is None:
            kokoro = await Kokoro(self)
        
        if operation == HELLO:
            # sowwy, but we need to ignore these or we will keep getting timeout
            # kokoro.interval=data['heartbeat_interval']/100.
            # send a heartbeat immediately
            await kokoro.beat_now()
            return
        
        if operation == HEARTBEAT_ACK:
            kokoro.answered()
            return
        
        if operation == SESSION_DESCRIPTION:
            # data['mode'] is same as our default every time?
            self.client._secret_box = SecretBox(bytes(data['secret_key']))
            if kokoro.beater is None: # Discord order bug ?
                kokoro.start_beating()
                await self._beat()
            
            await self._set_speaking(self.client.speaking)
            return
        
        if kokoro.beater is None:
            raise TimeoutError
        
        if operation == READY:
            # need to ignore interval
            # kokoro.interval = data['heartbeat_interval']/100.
            await self._initial_connection(data)
            return
        
        if operation == INVALIDATE_SESSION:
            await self._identify()
            return
        
        # Ignore VIDEO_SESSION_DESCRIPTION and VIDEO_SINK for now
    
    # general stuffs
    
    @property
    def latency(self):
        """
        The latency of the websocket in seconds. If no latency is recorded, will return `Kokoro.DEFAULT_LATENCY`.
        
        Returns
        -------
        latency : `float`
        """
        kokoro = self.kokoro
        if kokoro is None:
            return Kokoro.DEFAULT_LATENCY
        return kokoro.latency
    
    
    async def terminate(self):
        """
        Terminates the gateway's ``.kokoro`` and closes it's `.websocket`` with close code of `4000`.
        
        This method is a coroutine.
        """
        kokoro = self.kokoro
        if kokoro is not None:
            kokoro.terminate()
            
        websocket = self.websocket
        if websocket is None:
            return
        self.websocket = None
        await websocket.close(4000)
    
    
    async def close(self):
        """
        Cancels the gateway's ``.kokoro`` and closes it's ``.websocket`` with close code of `1000`.
        
        This method is a coroutine.
        """
        self.rate_limit_handler.cancel()
        
        kokoro = self.kokoro
        if (kokoro is not None):
            self.kokoro = None
            kokoro.cancel()
        
        websocket = self.websocket
        if websocket is None:
            return
        
        self.websocket = None
        await websocket.close(1000)
    
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's ``.websocket``. If there is no websocket, or the websocket
        is closed will not raise.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items or `list` of `Any`
        """
        websocket = self.websocket
        if websocket is None:
            return
        
        if await self.rate_limit_handler:
            return
        
        try:
            await websocket.send(to_json(data))
        except ConnectionClosed:
            pass
    
    
    def __repr__(self):
        """Returns the representation of the gateway."""
        return f'<{self.__class__.__name__} of {self.client}>'
    
    #special operations
    
    async def _identify(self):
        """
        Sends an `IDENTIFY` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        
        data = {
            'op': IDENTIFY,
            'd': {
                'server_id': str(voice_client.channel.guild.id),
                'user_id': str(voice_client.client.id),
                'session_id': voice_client._session_id,
                'token': voice_client._token,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _resume(self):
        """
        Sends a `RESUME` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        
        data = {
            'op': RESUME,
            'd': {
                'token': voice_client._token,
                'server_id': str(voice_client.channel.guild.id),
                'session_id': voice_client._session_id,
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _select_protocol(self, ip, port):
        """
        Sends a `SELECT_PROTOCOL` packet to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        ip : `str`
            The received ip of the voice client to use.
        port : `int`
            The received port of the voice client to use.
        """
        data = {
            'op': SELECT_PROTOCOL,
            'd': {
                'protocol': 'udp',
                'data': {
                    'address': ip,
                    'port': port,
                    'mode': 'xsalsa20_poly1305'
                },
            },
        }
        
        await self.send_as_json(data)
    
    
    async def _beat(self):
        """
        Sends a `HEARTBEAT` packet to Discord.
        
        This method is a coroutine.
        """
        data = {
            'op': HEARTBEAT,
            'd': int(time_now()*1000),
        }
        
        await self.send_as_json(data)
    
    
    async def _initial_connection(self, data):
        """
        Processes the data from `READY` operation and selects protocol with ``._select_protocol``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data from Discord.
        """
        voice_client = self.client
        voice_client._audio_source = data['ssrc']
        voice_client._audio_port = data['port']
        voice_client._endpoint_ip = data['ip']
        packet = bytearray(70)
        packet[0:4] = voice_client._audio_source.to_bytes(4, 'big')
        
        voice_client.send_packet(packet)
        
        protocol = voice_client._protocol
        # Make sure, that the voice client's reader do not wanna read our data away from us.
        protocol.cancel_current_reader()
        received = await protocol.read(70)
        
        # the ip is ascii starting at the 4th byte and ending at the first null
        voice_client._ip = ip = received[4:received.index(0, 4)].decode('ascii')
        voice_client._port = port = int.from_bytes(received[-2:], 'big')
        
        await self._select_protocol(ip, port)
        await self._client_connect()
   
    
    async def _client_connect(self):
        """
        Sends a `CLIENT_CONNECT` packet to Discord.
        
        This method is a coroutine.
        """
        voice_client = self.client
        data = {
            'op': CLIENT_CONNECT,
            'd': {
                'audio_ssrc': voice_client._audio_source,
                'video_ssrc': voice_client._video_source,
                'rtx_ssrc': 0,
            }
        }
        
        await self.send_as_json(data)
    
    
    async def _set_speaking(self, is_speaking):
        """
        Sends a `SPEAKING` packet with given `is_speaking` state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        is_speaking : `bool`
            Whether the voice client should show up as speaking and be able to send voice data or not.
        """
        data = {
            'op':SPEAKING,
            'd': {
                'speaking': is_speaking,
                'delay': 0,
            },
        }
        
        await self.send_as_json(data)
