__all__ = ('RPCClient', )

import sys
from math import floor
from os import getpid as get_process_identifier
from sys import platform as PLATFORM

from scarletio import (
    Future, RichAttributeErrorBaseType, Task, from_json, run_coroutine, sleep, to_json
)

from ...discord.activity import Activity
from ...discord.channel import Channel
from ...discord.client.request_helpers import get_channel_id, get_guild_id, get_user_id
from ...discord.core import KOKORO
from ...discord.guild import create_partial_guild_from_data
from ...discord.message.utils import process_message_chunk
from ...discord.preconverters import preconvert_snowflake
from ...discord.user import ZEROUSER

from .authenticate import AuthenticateResponse
from .certified_device import CertifiedDevice
from .command_handling import COMMAND_HANDLERS
from .constants import (
    CLOSE_CODES_FATAL, CLOSE_CODES_RECONNECT, CLOSE_CODE_RATE_LIMITED, CLOSE_PAYLOAD_KEY_CODE,
    CLOSE_PAYLOAD_KEY_MESSAGE, DEFAULT_OPERATION_NAME, DISPATCH_EVENT_ACTIVITY_JOIN,
    DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST, DISPATCH_EVENT_ACTIVITY_SPECTATE, DISPATCH_EVENT_CHANNEL_CREATE,
    DISPATCH_EVENT_CHANNEL_VOICE_SELECT, DISPATCH_EVENT_GUILD_CREATE, DISPATCH_EVENT_GUILD_STATUS_UPDATE,
    DISPATCH_EVENT_MESSAGE_CREATE, DISPATCH_EVENT_MESSAGE_DELETE, DISPATCH_EVENT_MESSAGE_EDIT,
    DISPATCH_EVENT_NOTIFICATION_CREATE, DISPATCH_EVENT_SPEAKING_START, DISPATCH_EVENT_SPEAKING_STOP,
    DISPATCH_EVENT_USER_VOICE_CREATE, DISPATCH_EVENT_USER_VOICE_DELETE, DISPATCH_EVENT_USER_VOICE_UPDATE,
    DISPATCH_EVENT_VOICE_CONNECTION_STATUS, DISPATCH_EVENT_VOICE_SETTINGS_UPDATE, IPC_VERSION, OPERATION_CLOSE,
    OPERATION_FRAME, OPERATION_HANDSHAKE, OPERATION_VALUE_TO_NAME, PAYLOAD_COMMAND_ACTIVITY_JOIN_ACCEPT,
    PAYLOAD_COMMAND_ACTIVITY_JOIN_REJECT, PAYLOAD_COMMAND_ACTIVITY_SET, PAYLOAD_COMMAND_AUTHENTICATE,
    PAYLOAD_COMMAND_AUTHORIZE, PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET, PAYLOAD_COMMAND_CHANNEL_GET,
    PAYLOAD_COMMAND_CHANNEL_TEXT_SELECT, PAYLOAD_COMMAND_CHANNEL_VOICE_GET, PAYLOAD_COMMAND_CHANNEL_VOICE_SELECT,
    PAYLOAD_COMMAND_GUILD_CHANNEL_GET_ALL, PAYLOAD_COMMAND_GUILD_GET, PAYLOAD_COMMAND_GUILD_GET_ALL,
    PAYLOAD_COMMAND_SUBSCRIBE, PAYLOAD_COMMAND_UNSUBSCRIBE, PAYLOAD_COMMAND_USER_VOICE_SETTINGS_SET,
    PAYLOAD_COMMAND_VOICE_SETTINGS_GET, PAYLOAD_COMMAND_VOICE_SETTINGS_SET, PAYLOAD_KEY_COMMAND, PAYLOAD_KEY_EVENT,
    PAYLOAD_KEY_NONCE, PAYLOAD_KEY_PARAMETERS, RECONNECT_INTERVAL, RECONNECT_RATE_LIMITED_INTERVAL, REQUEST_TIMEOUT
)
from .event_handler_manager import RPCEventHandlerManager
from .rich_voice_state import RichVoiceState
from .user_voice_settings import AudioBalance, UserVoiceSettings
from .utils import check_for_error, get_ipc_path
from .voice_settings import VoiceSettings, VoiceSettingsInput, VoiceSettingsMode, VoiceSettingsOutput


PROCESS_IDENTIFIER = get_process_identifier()

channel_key_transformer = lambda channel_id: {'channel_id': str(channel_id)}
guild_key_transformer = lambda guild_id: {'guild_id': str(guild_id)}

SUBSCRIPTION_KEY_TO_PARAMETERS_DATA = {
    DISPATCH_EVENT_GUILD_STATUS_UPDATE: guild_key_transformer,
    DISPATCH_EVENT_GUILD_CREATE: None,
    DISPATCH_EVENT_CHANNEL_CREATE: None,
    DISPATCH_EVENT_CHANNEL_VOICE_SELECT: None,
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE: None,
    DISPATCH_EVENT_USER_VOICE_CREATE: channel_key_transformer,
    DISPATCH_EVENT_USER_VOICE_UPDATE: channel_key_transformer,
    DISPATCH_EVENT_USER_VOICE_DELETE: channel_key_transformer,
    DISPATCH_EVENT_VOICE_CONNECTION_STATUS: None,
    DISPATCH_EVENT_MESSAGE_CREATE: channel_key_transformer,
    DISPATCH_EVENT_MESSAGE_EDIT: channel_key_transformer,
    DISPATCH_EVENT_MESSAGE_DELETE: channel_key_transformer,
    DISPATCH_EVENT_SPEAKING_START: channel_key_transformer,
    DISPATCH_EVENT_SPEAKING_STOP: channel_key_transformer,
    DISPATCH_EVENT_NOTIFICATION_CREATE: None,
    DISPATCH_EVENT_ACTIVITY_JOIN: None,
    DISPATCH_EVENT_ACTIVITY_SPECTATE: None,
    DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST: None,
}

del channel_key_transformer
del guild_key_transformer


class RPCClient(RichAttributeErrorBaseType):
    """
    RPC client connecting to a local Discord client with IPC.
    
    Attributes
    ----------
    _auto_nonce : `int`
        Auto nonce generation index for the next request.
    _connection_waiter : `None`, ``Future``
        Waiter for client connection.
    _protocol : `None`, ``BaseProtocol``
        The connected protocol if any.
    _response_waiters : `dict` of (`str`, ``Future``) items
        Waiters for each request response.
    _subscriptions : `dict` of (`str`, (`None`, `set`)) items
        The events to which the client is already subscribed to.
    application_id : `int`
        The respective application's identifier.
    events : ``RPCEventHandlerManager``
        Contains the event handlers of the rpc client. New event handlers can be added through it as well.
    running : `bool`
        Whether the client is connected and running.
    user : ``ClientUserBase``
        The logged in user to the local Discord client.
        
        Set after connection. Defaults to `ZEROUSER`.
    """
    __slots__ = (
        '_auto_nonce', '_connection_waiter', '_protocol', '_response_waiters', '_subscriptions', 'application_id',
        'events', 'running', 'user'
    )
    
    def __new__(cls, application_id):
        """
        Creates a new IPC client instance communicating with local Discord client.
        
        Parameters
        ----------
        application_id : `int`
            The application's identifier to connect to the client to as.
        
        Raises
        ------
        TypeError
            If any parameter's type is incorrect.
        ValueError
            If any parameter's value is incorrect.
        """
        application_id = preconvert_snowflake(application_id, 'application_id')
        
        self = object.__new__(cls)
        self.application_id = application_id
        self.running = False
        self._protocol = None
        self._response_waiters = {}
        self._auto_nonce = 0
        self._connection_waiter = None
        self._subscriptions = {}
        self.user = ZEROUSER
        self.events = RPCEventHandlerManager()
        
        return self
    
    
    def start(self):
        """
        Starts the ipc client's connecting to Discord. If the client is already running, raises `RuntimeError`.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `bool`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if connecting was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                `FutureAsyncWrapper`. The task will return `True`, if connecting was successful.
            - If the method was called from any other thread, then waits for the connector task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            - Discord inter process communication path could not be detected.
            - If the client is already running.
        """
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        return run_coroutine(self.connect(), KOKORO)
    
    
    async def connect(self):
        """
        Connects to Discord RPC.
        
        This method is a coroutine.
        
        Raises
        ------
        RuntimeError
            - Discord inter process communication path could not be detected.
            - The client is already running.
        """
        ipc_path = get_ipc_path(0)
        if (ipc_path is None):
            raise RuntimeError('Discord inter process communication path could not be detected.')
        
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        Task(KOKORO, self._connect(ipc_path))
        
        connection_waiter = self._connection_waiter
        if (connection_waiter is not None):
            connection_waiter.set_result_if_pending(False)
        
        connection_waiter = Future(KOKORO)
        self._connection_waiter = connection_waiter
        return await connection_waiter
    
    
    async def _connect(self, ipc_path):
        """
        Connects to Discord RPC and reconnects if needed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        ipc_path : `str`
            Inter process communication path to connect to.
        
        Raises
        ------
        NotImplemented
            Opening pipe is not supported on your platform.
        """
        self.running = True
        
        try:
            while True:
                try:
                    await self._open_pipe(ipc_path)
                except ConnectionError:
                    self._cleanup_connection()
                    if not self.running:
                        return
                    
                    await sleep(RECONNECT_INTERVAL, KOKORO)
                    continue
                
                await self._send_handshake()
                
                while True:
                    try:
                        operation, data = await self._receive_data()
                    except ConnectionError:
                        self._cleanup_connection()
                        if not self.running:
                            return
                        
                        await sleep(RECONNECT_INTERVAL, KOKORO)
                        break
                    
                    if operation == OPERATION_CLOSE:
                        self._cleanup_connection()
                        
                        data = from_json(data)
                        close_code = data[CLOSE_PAYLOAD_KEY_CODE]
                        
                        if close_code in CLOSE_CODES_RECONNECT:
                            if not self.running:
                                return
                            
                            if close_code == CLOSE_CODE_RATE_LIMITED:
                                reconnect_after = RECONNECT_RATE_LIMITED_INTERVAL
                            else:
                                reconnect_after = RECONNECT_INTERVAL
                            
                            await sleep(reconnect_after, KOKORO)
                        
                        else:
                            if close_code in CLOSE_CODES_FATAL:
                                exception_type = 'Fatal'
                            else:
                                exception_type = 'Unexpected'
                            
                            close_message = data[CLOSE_PAYLOAD_KEY_MESSAGE]
                            
                            sys.stderr.write(
                                f'{exception_type} RPC error occurred: [{close_code}] {close_message}\n'
                            )
                            
                            self.running = False
                            return
                        
                        break
                    
                    elif operation == OPERATION_FRAME:
                        if data is None:
                            continue
                        
                        data = from_json(data)
                        print(data)
                        check_for_error(data)
                        
                        command_name = data[PAYLOAD_KEY_COMMAND]
                        try:
                            command_handler = COMMAND_HANDLERS[command_name]
                        except KeyError:
                            sys.stderr.write(
                                f'No command handler for: {command_name}\n'
                                f'Payload: {data!r}\n'
                            )
                        else:
                            command_handler(self, data)
                    
                    else:
                        operation_name = OPERATION_VALUE_TO_NAME.get(operation, DEFAULT_OPERATION_NAME)
                        sys.stderr.write(
                            f'Received unexpected operation in handshake, got {operation_name}, ({operation}).'
                        )
        
        except:
            self.running = False
            self._cleanup_connection()
            raise
        
        finally:
            # Try to set result to False.
            self._set_connection_waiter_result(False)
    
    
    async def _send_data(self, operation, payload):
        protocol = self._protocol
        if (protocol is None):
            raise ConnectionError('RPC client nt connected.')
        
        data = to_json(payload).encode()
        data_length = len(data)
        
        header = operation.to_bytes(4, 'little') + data_length.to_bytes(4, 'little')
        protocol.write(header)
        protocol.write(data)
        await protocol.drain()
    
    
    async def _receive_data(self):
        protocol = self._protocol
        
        data = await protocol.read_exactly(8)
        operation = int.from_bytes(data[0:4], 'little')
        data_length = int.from_bytes(data[4:8], 'little')
        
        if data_length == 0:
            data = None
        else:
            data = await protocol.read_exactly(data_length)
        
        return operation, data
    
    if PLATFORM in ('linux', 'darwin'):
        async def _open_pipe(self, ipc_path):
            protocol = await KOKORO.open_unix_connection_to(ipc_path)
            self._protocol = protocol
    else:
        async def _open_pipe(self, ipc_path):
            raise NotImplementedError(f'Opening inter-process connection is not supported on {PLATFORM}.')
    
    
    async def _send_handshake(self):
        """
        Sends handshake payload.
        
        This method is a coroutine.
        """
        data = {
            'v': IPC_VERSION,
            'client_id': str(self.application_id),
        }
        
        await self._send_data(OPERATION_HANDSHAKE, data)
    
    
    def _set_connection_waiter_result(self, result):
        """
        Sets connection waiter result if applicable.
        
        Parameters
        ----------
        result : `bool`
            Whether connecting was successful.
        """
        connection_waiter = self._connection_waiter
        if (connection_waiter is not None):
            self._connection_waiter = None
            connection_waiter.set_result_if_pending(result)
    
    
    def _get_nonce(self):
        """
        Generates auto nonce for the next request.
        
        Returns
        -------
        nonce : `str`
        """
        self._auto_nonce = nonce = self._auto_nonce + 1
        return nonce.__format__('0>16x')
    
    
    def _cleanup_connection(self):
        """
        Cleans up the RPC client's connection.
        """
        protocol = self._protocol
        if (protocol is not None):
            self._protocol = None
            protocol.close()
    
    
    async def _send_request(self, payload):
        """
        This method is a coroutine.
        """
        nonce = self._get_nonce()
        payload[PAYLOAD_KEY_NONCE] = nonce
        
        waiter = Future(KOKORO)
        self._response_waiters[nonce] = waiter
        waiter.apply_timeout(REQUEST_TIMEOUT)
        
        try:
            await self._send_data(OPERATION_FRAME, payload)
            return await waiter
        finally:
            try:
                del self._response_waiters[nonce]
            except KeyError:
                pass
    
    
    def _is_subscribed_to(self, event, key):
        """
        Returns whether the client is already subscribed to the given event.
        
        Parameters
        ----------
        event : `str`
            The event's name.
        key : `Any`
            The key used to detect whether the client is subscribed.
        
        Returns
        -------
        is_subscribed_to : `bool`
            Whether the client is subscribed to the event.
        """
        try:
            keys = self._subscriptions[event]
        except KeyError:
            is_subscribed_to = False
        else:
            if key is None:
                is_subscribed_to = True
            else:
                is_subscribed_to = key in keys
        
        return is_subscribed_to
    
    
    def _subscribe_to(self, event, key):
        """
        Subscribed to the given event.
        
        Parameters
        ----------
        event : `str`
            The event's name.
        key : `Any`
            The key used to detect whether the client is subscribed.
        """
        try:
            keys = self._subscriptions[event]
        except KeyError:
            if key is None:
                keys = None
            else:
                keys = set()
            
            self._subscriptions[event] = keys
        
        else:
            if (key is not None):
                if keys is None:
                    keys = {}
                    self._subscriptions[event] = keys
                
                keys.add(key)
    
    
    def _unsubscribe_from(self, event, key):
        """
        Unsubscribed from the given event.
        
        Parameters
        ----------
        event : `str`
            The event's name.
        key : `Any`
            The key used to detect whether the client is subscribed.
        """
        try:
            keys = self._subscriptions[event]
        except KeyError:
            pass
        else:
            if key is None:
                if keys is None:
                    del self._subscriptions[event]
            
            else:
                if (keys is not None):
                    try:
                        del keys[key]
                    except ValueError:
                        pass
                    else:
                        if not keys:
                            del self._subscriptions[event]
    
    
    def stop(self, data):
        """
        Closes the rpc client.
        
        Parameters
        ----------
        data : `None`, `bytes`
            Received close data.
        """
        self.running = False
    
    
    async def authorize(self, scopes, rpc_token, name):
        """
        Authorizes a new client with your application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scopes : `list` of `str`
            Oauth2 to authorize the user with.
        rpc_token : `str`
            One time user rpc token.
        name : `str`
            User name to create a guest account with, if the user is not registered to Discord.
        
        Returns
        -------
        code : `str`
            OAuth2 authorization code.
        
        Raises
        ------
        TypeError
            If `Scopes` is neither `str` nor `list` of `str`-s.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        AssertionError
            - If `rpc_token` is not `str`.
            - If `name` is not `str`.
            - If `scopes` is empty.
            - If `scopes` contains empty string.
        """
        if isinstance(scopes, str):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` was given as an empty string.'
                    )
        
        elif isinstance(scopes, list):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` cannot be empty.'
                    )
                
                for index, scope in enumerate(scopes):
                    if not isinstance(scope, str):
                        raise AssertionError(
                            f'`scopes[{index!r}]` is not `str`, got {scope.__class__.__name__}; {scope!r} '
                            f'scopes={scopes!r}.'
                        )
                    
                    if not scope:
                        raise AssertionError(
                            f'`scopes{index!r}` is an empty string; got scopes={scopes!r}.'
                        )
            
            scopes = ' '.join(scopes)
        
        else:
            raise TypeError(
                f'`scopes` can be `str`, `list` of `str`, got {scopes.__class__.__name__}; {scopes!r}.'
            )
        
        
        if __debug__:
            if not isinstance(rpc_token, str):
                raise AssertionError(
                    f'`rpc_token` can be `str`, got {rpc_token.__class__.__name__}; {rpc_token!r}.'
                )
            
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
        
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_AUTHORIZE,
            PAYLOAD_KEY_PARAMETERS: {
                'scopes': scopes,
                'client_id': str(self.application_id),
                'rpc_token': rpc_token,
                'username': name,
            },
        }
        
        data = await self._send_request(data)
        
        return data['code']
    
    
    async def authenticate(self, access_token):
        """
        Gets all the guild of the user.
        
        This method is a coroutine.
        
        Returns
        -------
        response : ``AuthenticateResponse``
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        AssertionError
            If `access_token` is not `str`.
        """
        if __debug__:
            if not isinstance(access_token, str):
                raise AssertionError(
                    f'`access_token` can be `str`, got {access_token.__class__.__name__}; {access_token!r}.'
                )
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_AUTHENTICATE,
            PAYLOAD_KEY_PARAMETERS: {
                'access_token': access_token,
            },
        }
        
        data = await self._send_request(data)
        return AuthenticateResponse.from_data(data)
    
    
    async def guild_get_all(self):
        """
        Gets all the guild of the user.
        
        This method is a coroutine.
        
        Returns
        -------
        guilds : `list` of ``Guild``
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_GUILD_GET_ALL,
            PAYLOAD_KEY_PARAMETERS: {},
        }
        
        data = await self._send_request(data)
        
        guilds = []
        for guild_data in data['guilds']:
            guild = create_partial_guild_from_data(guild_data)
            guilds.append(guild)
        
        return guilds
    
    
    async def guild_get(self, guild):
        """
        Gets the guild.
        
        > The user must be in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or it's identifier.
        
        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If `guild` is neither `int`, nor ``Guild``.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        guild_id = get_guild_id(guild)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_GUILD_GET,
            PAYLOAD_KEY_PARAMETERS: {
                'channel_id': str(guild_id),
                'timeout': REQUEST_TIMEOUT,
            },
        }
        
        data = await self._send_request(data)
        return create_partial_guild_from_data(data)
    
    
    async def channel_get(self, channel):
        """
        Gets the channel.
        
        > The user must be in the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel or it's identifier.
        
        Returns
        -------
        channel : ``Channel``
            The response channel.
        messages : `None`, `list` of ``Message``
            Messages sent to the channel if applicable.
        rich_voice_states : `None`, `dict` of (`int`, ``RichVoiceState``) items
            Voice states of the users inside of the channel if applicable.
        
        Raises
        ------
        TypeError
            If `channel` is neither `int`, nor ``Channel``.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel)
        channel_id = str(channel_id)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CHANNEL_GET,
            PAYLOAD_KEY_PARAMETERS: {
                'channel_id': channel_id,
            },
        }
        
        data = await self._send_request(data)
        channel = Channel.from_data(data, None, 0)
        
        message_datas = data.get('messages', None)
        if (message_datas is not None) and message_datas:
            messages = process_message_chunk(data, channel)
        else:
            messages = None
        
        rich_voice_state_datas = data.get('voice_states', None)
        if (rich_voice_state_datas is not None) and rich_voice_state_datas:
            rich_voice_states = {}
            
            for rich_voice_state_data in rich_voice_state_datas:
                rich_voice_state = RichVoiceState.from_data(rich_voice_state_data)
                rich_voice_states[rich_voice_state.user.id] = rich_voice_state
        else:
            rich_voice_states = None
        
        return channel, messages, rich_voice_states
    
    
    async def guild_channel_get_all(self, guild):
        """
        Gets the guild's channels.
        
        > The user must be in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or it's identifier.
        
        Returns
        -------
        channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `guild` is neither `int`, nor ``Guild``.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        guild_id = get_guild_id(guild)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_GUILD_CHANNEL_GET_ALL,
            PAYLOAD_KEY_PARAMETERS: {
                'guild_id': str(guild_id),
            },
        }
        
        data = await self._send_request(data)
    
        channels = []
        for channel_data in data['channels']:
            channel = Channel.from_data(channel_data, None, guild_id)
            channels.append(channel)
        
        return channels
    
    
    async def user_voice_settings_set(self, *, audio_balance = None, mute = None, volume = None):
        """
        Changes the user's voice settings.
        
        This method is a coroutine.
        
        Parameters
        ----------
        audio_balance : `None`, ``AudioBalance`` = `None`, Optional (Keyword only)
            Audio balance.
        mute : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the user is muted.
        volume : `None`, `float` = `None`, Optional (Keyword only)
            The user's volume.
            
            Can be in range [0.0:2.0].
        
        Returns
        -------
        user_voice_settings : ``UserVoiceSettings``
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        AssertionError
            - If `audio_balance` is neither `None` nor ``AudioBalance``.
            - If `mute` is neither `None` nor `int`.
            - If `volume` is neither `None` nor `float`.
            - If `volume` is out of range [0.0:2.0].
        """
        parameters = {
            'user_id': str(self.user.id),
        }
        
        if (audio_balance is not None):
            if not isinstance(audio_balance, AudioBalance):
                raise AssertionError(
                    f'`audio_balance` can be `None`, `{AudioBalance.__name__}`, got '
                    f'{audio_balance.__class__.__name__}; {audio_balance!r}.'
                )
            
            audio_balance_data = audio_balance.to_data()
            if audio_balance_data:
                parameters['pan'] = audio_balance_data
        
        if (mute is not None):
            if not isinstance(mute, bool):
                raise AssertionError(
                    f'`mute` can be `None`, `bool`, got {mute.__class__.__name__}, {mute!r}.'
                )
            
            parameters['mute'] = mute
        
        if (volume is not None):
            if not isinstance(mute, float):
                raise AssertionError(
                    f'`volume` can be `None`, `float`, got {volume.__class__.__name__}; {volume!r}.'
                )
            
            if (volume < 0.0) or (volume > 2.0):
                raise AssertionError(
                    f'`volume` can be in range [0.0:2.0], got {volume!r}.'
                )
            
            parameters['volume'] = floor(volume * 100.0)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_USER_VOICE_SETTINGS_SET,
            PAYLOAD_KEY_PARAMETERS: parameters,
        }
        
        data = await self._send_request(data)
        return UserVoiceSettings.from_data(data)
    
    
    async def channel_voice_select(self, channel, *, force=False):
        """
        Selects the given voice channel joining it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : `None`, ``Channel``, `int`
            The channel to select or `None` to leave.
        force : `bool` = `False`, Optional (Keyword only)
            Forces the user to join the voice channel.
            
            Defaults to `False`.
        
        Returns
        -------
        channel : ``Channel``, `None`
        
        Raises
        ------
        TypeError
            If `channel` is neither `None`, ``Channel``, `int`.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        AssertionError
            If `force` is not `bool`.
        """
        if channel is None:
            channel_id = None
        else:
            channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
            channel_id = str(channel_id)
        
        if __debug__:
            if not isinstance(force, bool):
                raise AssertionError(
                    f'`force` can be `bool`, got {force.__class__.__name__}; {force!r}.'
                )
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CHANNEL_VOICE_SELECT,
            PAYLOAD_KEY_PARAMETERS: {
                'channel_id': channel_id,
                'timeout': REQUEST_TIMEOUT,
                'force': force,
            },
        }
        
        data = await self._send_request(data)
        if (data is None):
            channel = None
        else:
            channel = Channel.from_data(data, None, 0)
        
        return channel
    
    
    async def channel_voice_get(self):
        """
        Gets the voice channel to what the user is joined to.
        
        This method is a coroutine.
        
        Returns
        -------
        voice_settings : ``VoiceSettings``
            The new voice settings of the user.
        
        Returns
        -------
        channel : ``Channel``, `None`
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CHANNEL_VOICE_GET,
        }
        
        data = await self._send_request(data)
        if (data is None):
            channel = None
        else:
            channel = Channel.from_data(data, None, 0)
        
        return channel
    
    
    async def channel_text_select(self, channel):
        """
        Selects the given text channel by the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : `None`, ``Channel``, `int`
            The channel to select or `None` to leave.
        
        Returns
        -------
        channel : ``Channel``, `None`
        
        Raises
        ------
        TypeError
            If `channel` is neither `None`, ``Channel`` nor `int`.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        if (channel is None):
            channel_id = None
        else:
            channel_id = get_channel_id(channel, Channel.is_in_group_textual)
            channel_id = str(channel_id)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CHANNEL_TEXT_SELECT,
            PAYLOAD_KEY_PARAMETERS: {
                'channel_id': channel_id,
                'timeout': REQUEST_TIMEOUT,
            },
        }
        
        data = await self._send_request(data)
        if (data is None):
            channel = None
        else:
            channel = Channel.from_data(data, None, 0)
        
        return channel
    
    
    async def voice_settings_get(self):
        """
        gets the user's voice settings.
        
        This method is a coroutine.
        
        Returns
        -------
        voice_settings : ``VoiceSettings``
            The voice settings of the user.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_VOICE_SETTINGS_GET,
        }
        
        data = await self._send_request(data)
        return VoiceSettings.from_data(data)
    
    
    async def voice_settings_set(
        self,
        *,
        input_ = None,
        output = None,
        mode = None,
        automatic_gain_control = None,
        echo_cancellation = None,
        noise_suppression = None,
        quality_of_service = None,
        silence_warning = None,
        deaf = None,
        mute = None,
    ):
        """
        Modifies the user's voice settings and returns it's actual one.
        
        Only the passed parameters are modified.
        
        This method is a coroutine.
        
        Parameters
        ----------
        input_ : `None`, ``VoiceSettingsInput`` = `None`, Optional (Keyword only)
            Input settings.
        output : `None`, ``VoiceSettingsOutput`` = `None`, Optional (Keyword only)
            Output settings.
        mode : `None`, ``VoiceSettingsMode`` = `None`, Optional (Keyword only)
            Voice mode settings.
        automatic_gain_control : `None`, `bool` = `None`, Optional (Keyword only)
            Whether automatic gain control should be enabled.
        echo_cancellation : `None`, `bool` = `None`, Optional (Keyword only)
            Whether echo cancellation should be enabled.
        noise_suppression : `None`, `bool` = `None`, Optional (Keyword only)
            Whether noise suppression should be enabled.
        quality_of_service : `None`, `bool` = `None`, Optional (Keyword only)
            Whether voice quality of service should be enabled.
            
            > QoS, quality of service is a method to prioritize network traffic going through a router to provide
            > acceptable service to most users.
        silence_warning : `None`, `bool` = `None`, Optional (Keyword only)
            Whether silence warning notice should be enabled.
        deaf : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the user should be deaf.
        mute : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the user should be muted.
        
        Returns
        -------
        voice_settings : ``VoiceSettings``
            The new voice settings of the user.
        
        Raises
        ------
        AssertionError
            - If `input_` is not ``VoiceSettingsInput``.
            - If `output` is not ``VoiceSettingsOutput``.
            - If `mode` is not ``VoiceSettingsMode``.
            - If `automatic_gain_control` is not `bool`.
            - If `echo_cancellation` is not `bool`.
            - If `noise_suppression` is not `bool`.
            - If `quality_of_service` is not `bool`.
            - If `silence_warning` is not `bool`.
            - If `deaf` is not `bool`.
            - If `mute` is not `bool`.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        if __debug__:
            if (input_ is not None) and (not isinstance(input_, VoiceSettingsInput)):
                raise AssertionError(
                    f'`input_` can be `{VoiceSettingsInput.__name__}`, got'
                    f'{input_.__class__.__name__}; {input_!r}.'
                )
            
            if (output is not None) and (not isinstance(output, VoiceSettingsOutput)):
                raise AssertionError(
                    f'`output` can be `{VoiceSettingsOutput.__name__}`, got'
                    f'{output.__class__.__name__}; {output!r}.'
                )
            
            if (mode is not None) and (not isinstance(mode, VoiceSettingsMode)):
                raise AssertionError(
                    f'`mode` can be `{VoiceSettingsMode.__name__}`, got'
                    f'{mode.__class__.__name__}; {mode!r}.'
                )
            
            if (automatic_gain_control is not None) and (not isinstance(automatic_gain_control, bool)):
                raise AssertionError(
                    f'`automatic_gain_control` can be `bool`, got '
                    f'{automatic_gain_control.__class__.__name__}; {automatic_gain_control!r}.'
                )
            
            if (echo_cancellation is not None) and (not isinstance(echo_cancellation, bool)):
                raise AssertionError(
                    f'`echo_cancellation` can be `bool`, got '
                    f'{echo_cancellation.__class__.__name__}; {echo_cancellation!r}.'
                )
            
            if (noise_suppression is not None) and (not isinstance(noise_suppression, bool)):
                raise AssertionError(
                    f'`noise_suppression` can be `bool`, got '
                    f'{noise_suppression.__class__.__name__}; {noise_suppression!r}.'
                )
            
            if (quality_of_service is not None) and (not isinstance(quality_of_service, bool)):
                raise AssertionError(
                    f'`quality_of_service` can be `bool`, got '
                    f'{quality_of_service.__class__.__name__}; {quality_of_service!r}.'
                )
            
            if (silence_warning is not None) and (not isinstance(silence_warning, bool)):
                raise AssertionError(
                    f'`silence_warning` can be `bool`, got '
                    f'{silence_warning.__class__.__name__}; {silence_warning!r}.'
                )
            
            if (deaf is not None) and (not isinstance(deaf, bool)):
                raise AssertionError(
                    f'`deaf` can be `bool`, got {deaf.__class__.__name__}; {deaf!r}.'
                )
            
            if (mute is not None) and (not isinstance(mute, bool)):
                raise AssertionError(
                    f'`mute` can be `bool`, got {mute.__class__.__name__}; {mute!r}.'
                )
        
        
        parameters = {}
        
        if (input_ is not None):
            input_data = input_.to_data()
            if input_data:
                parameters['input'] = input_data
        
        if (output is not None):
            output_data = output.to_data()
            if output_data:
                parameters['output'] = output_data
        
        if (mode is not None):
            mode_data = mode.to_data()
            if mode_data:
                parameters['mode'] = mode_data
        
        if (automatic_gain_control is not None):
            parameters['automatic_gain_control'] = automatic_gain_control
        
        if (echo_cancellation is not None):
            parameters['echo_cancellation'] = echo_cancellation
        
        if (noise_suppression is not None):
            parameters['noise_suppression'] = noise_suppression
        
        if (quality_of_service is not None):
            parameters['qos'] = quality_of_service
        
        if (silence_warning is not None):
            parameters['silence_warning'] = silence_warning
        
        if (deaf is not None):
            parameters['deaf'] = deaf
        
        if (mute is not None):
            parameters['mute'] = mute
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_VOICE_SETTINGS_SET,
            PAYLOAD_KEY_PARAMETERS: parameters,
        }
        
        data = await self._send_request(data)
        return VoiceSettings.from_data(data)
    
    
    async def _subscribe(self, event, key):
        """
        Subscribes to the given event.
        
        Parameters
        ---------
        event : `str`
            The event to subscribe to.
        key : `Any`
            The key used to detect whether the client is subscribed.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        if self._is_subscribed_to(event, key):
            return
        
        transformer = SUBSCRIPTION_KEY_TO_PARAMETERS_DATA.get(PAYLOAD_COMMAND_UNSUBSCRIBE, None)
        if transformer is None:
            parameters_data = {}
        else:
            parameters_data = transformer(key)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_SUBSCRIBE,
            PAYLOAD_KEY_PARAMETERS: parameters_data,
            PAYLOAD_KEY_EVENT: event,
        }
        
        await self._send_request(data)
        self._subscribe_to(event, key)
    
    
    async def _unsubscribe(self, event, key):
        """
        Subscribes to the given event.
        
        Parameters
        ---------
        event : `str`
            The event to unsubscribe to.
        key : `Any`
            The key used to detect whether the client is subscribed.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        if not self._is_subscribed_to(event, key):
            return
        
        transformer = SUBSCRIPTION_KEY_TO_PARAMETERS_DATA.get(PAYLOAD_COMMAND_UNSUBSCRIBE, None)
        if transformer is None:
            parameters_data = {}
        else:
            parameters_data = transformer(key)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_UNSUBSCRIBE,
            PAYLOAD_KEY_PARAMETERS: parameters_data,
            PAYLOAD_KEY_EVENT: event,
        }
        
        await self._send_request(data)
        self._unsubscribe_from(event, key)
    
    
    async def subscribe_guild_status_update(self, guild):
        """
        Subscribes to `guild_status_update` events of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to subscribe for the event to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        guild_id = get_guild_id(guild)
        
        await self._subscribe(
            DISPATCH_EVENT_GUILD_STATUS_UPDATE,
            guild_id,
        )
    
    
    async def unsubscribe_guild_status_update(self, guild):
        """
        Unsubscribes from `guild_status_update` events of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to unsubscribe for the event to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        guild_id = get_guild_id(guild)
        
        await self._unsubscribe(
            DISPATCH_EVENT_GUILD_STATUS_UPDATE,
            guild_id,
        )
    
    
    async def subscribe_guild_create(self):
        """
        Subscribes to `guild_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_GUILD_CREATE,
            None,
        )
    
    
    async def unsubscribe_guild_create(self):
        """
        Unsubscribes from `guild_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_GUILD_CREATE,
            None,
        )
    
    
    async def subscribe_channel_create(self):
        """
        Subscribes to `channel_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_CHANNEL_CREATE,
            None,
        )
    
    
    async def unsubscribe_channel_create(self):
        """
        Unsubscribes from `channel_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_CHANNEL_CREATE,
            None,
        )
    
    
    async def subscribe_channel_voice_select(self):
        """
        Subscribes to `channel_voice_select` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_CHANNEL_VOICE_SELECT,
            None,
        )
    
    
    async def unsubscribe_channel_voice_select(self):
        """
        Unsubscribes from `channel_voice_select` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_CHANNEL_VOICE_SELECT,
            None,
        )
    
    
    async def subscribe_voice_settings_update(self):
        """
        Subscribes to `voice_settings_update` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_VOICE_SETTINGS_UPDATE,
            None,
        )
    
    
    async def unsubscribe_voice_settings_update(self):
        """
        Unsubscribes from `voice_settings_update` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_VOICE_SETTINGS_UPDATE,
            None,
        )
    
    
    async def subscribe_voice_state_create(self, channel):
        """
        Subscribes to `voice_state_create` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._subscribe(
            DISPATCH_EVENT_USER_VOICE_CREATE,
            channel_id,
        )
    
    
    async def unsubscribe_voice_state_create(self, channel):
        """
        Unsubscribes from `voice_state_create` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
            channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)

        await self._unsubscribe(
            DISPATCH_EVENT_USER_VOICE_CREATE,
            channel_id,
        )
    
    
    async def subscribe_voice_state_update(self, channel):
        """
        Subscribes to `voice_state_update` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._subscribe(
            DISPATCH_EVENT_USER_VOICE_UPDATE,
            channel_id,
        )
    
    
    async def unsubscribe_voice_state_update(self, channel):
        """
        Unsubscribes from `voice_state_update` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)

        await self._unsubscribe(
            DISPATCH_EVENT_USER_VOICE_UPDATE,
            channel_id,
        )
    
    
    async def subscribe_voice_state_delete(self, channel):
        """
        Subscribes to `voice_state_delete` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._subscribe(
            DISPATCH_EVENT_USER_VOICE_DELETE,
            channel_id,
        )
    
    
    async def unsubscribe_voice_state_delete(self, channel):
        """
        Unsubscribes from `voice_state_delete` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)

        await self._unsubscribe(
            DISPATCH_EVENT_USER_VOICE_DELETE,
            channel_id,
        )
    
    
    async def subscribe_voice_connection_status(self):
        """
        Subscribes to `voice_connection_status` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_VOICE_CONNECTION_STATUS,
            None,
        )
    
    
    async def unsubscribe_voice_connection_status(self):
        """
        Unsubscribes from `voice_connection_status` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_VOICE_CONNECTION_STATUS,
            None,
        )
    
    
    async def subscribe_message_create(self, channel):
        """
        Subscribes to `message_create` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        await self._subscribe(
            DISPATCH_EVENT_MESSAGE_CREATE,
            channel_id,
        )
    
    
    async def unsubscribe_message_create(self, channel):
        """
        Unsubscribes from `message_create` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)

        await self._unsubscribe(
            DISPATCH_EVENT_MESSAGE_CREATE,
            channel_id,
        )
    
    
    async def subscribe_message_edit(self, channel):
        """
        Subscribes to `message_edit` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        await self._subscribe(
            DISPATCH_EVENT_MESSAGE_EDIT,
            channel_id,
        )
    
    
    async def unsubscribe_message_edit(self, channel):
        """
        Unsubscribes from `message_edit` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)

        await self._unsubscribe(
            DISPATCH_EVENT_MESSAGE_EDIT,
            channel_id,
        )
    
    
    async def subscribe_message_delete(self, channel):
        """
        Subscribes to `message_delete` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        await self._subscribe(
            DISPATCH_EVENT_MESSAGE_DELETE,
            channel_id,
        )
    
    
    async def unsubscribe_message_delete(self, channel):
        """
        Unsubscribes from `message_delete` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)

        await self._unsubscribe(
            DISPATCH_EVENT_MESSAGE_DELETE,
            channel_id,
        )
    
    
    async def subscribe_speaking_start(self, channel):
        """
        Subscribes to `speaking_start` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._subscribe(
            DISPATCH_EVENT_SPEAKING_START,
            channel_id,
        )
    
    
    async def unsubscribe_speaking_start(self, channel):
        """
        Unsubscribes from `speaking_start` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)

        await self._unsubscribe(
            DISPATCH_EVENT_SPEAKING_START,
            channel_id,
        )
    
    
    async def subscribe_speaking_stop(self, channel):
        """
        Subscribes to `speaking_stop` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to subscribe to.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._subscribe(
            DISPATCH_EVENT_SPEAKING_STOP,
            channel_id,
        )
    
    
    async def unsubscribe_speaking_stop(self, channel):
        """
        Unsubscribes from `speaking_stop` events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to unsubscribe from.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_connectable)
        
        await self._unsubscribe(
            DISPATCH_EVENT_SPEAKING_STOP,
            channel_id,
        )
    
    
    async def subscribe_notification_create(self):
        """
        Subscribes to `notification_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_NOTIFICATION_CREATE,
            None,
        )
    
    
    async def unsubscribe_notification_create(self):
        """
        Unsubscribes from `notification_create` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_NOTIFICATION_CREATE,
            None,
        )
    
    
    async def subscribe_activity_join(self):
        """
        Subscribes to `activity_join` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_ACTIVITY_JOIN,
            None,
        )
    
    
    async def unsubscribe_activity_join(self):
        """
        Unsubscribes from `activity_join` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_ACTIVITY_JOIN,
            None,
        )
    
    
    async def subscribe_activity_spectate(self):
        """
        Subscribes to `activity_spectate` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_ACTIVITY_SPECTATE,
            None,
        )
    
    
    async def unsubscribe_activity_spectate(self):
        """
        Unsubscribes from `activity_spectate` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_ACTIVITY_SPECTATE,
            None,
        )
    
    
    async def subscribe_activity_join_request(self):
        """
        Subscribes to `activity_join_request` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._subscribe(
            DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST,
            None,
        )
    
    
    async def unsubscribe_activity_join_request(self):
        """
        Unsubscribes from `activity_join_request` events.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        await self._unsubscribe(
            DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST,
            None,
        )
    
    
    async def set_certified_devices(self, *devices):
        """
        Sends information about the current state of hardware certified devices that are connected to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *devices : ``CertifiedDevice``
            Certified devices.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        if __debug__:
            for device in devices:
                if not isinstance(device, CertifiedDevice):
                    raise AssertionError(
                        f'`devices` can be `{CertifiedDevice.__name__}`, got '
                        f'{device.__class__.__name__}; {device!r}.'
                    )
        
        device_datas = [device.to_data() for device in devices]
        
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET,
            PAYLOAD_KEY_PARAMETERS: {
                'devices': device_datas,
            },
        }
        
        await self._send_request(data)
    
    
    async def activity_set(self, activity):
        """
        Sets activity to the client.
        
        This method is a coroutine.
        
        Parameters
        ----------
        activity : ``Activity``
            The activity to set.
        
        Returns
        -------
        activity : ``Activity``
            The set activity.
        
        Raises
        ------
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        activity_data = activity.user_dict()
        activity_data['instance'] = True
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_ACTIVITY_SET,
            PAYLOAD_KEY_PARAMETERS: {
                'activity': activity_data,
                'pid': PROCESS_IDENTIFIER,
            },
        }
        
        data = await self._send_request(data)
        return Activity.from_data(data)
    
    
    async def activity_join_accept(self, user):
        """
        Accepts activity join invite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user, who's achievement will be updated.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        user_id = get_user_id(user)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_ACTIVITY_JOIN_ACCEPT,
            PAYLOAD_KEY_PARAMETERS: {
                'user_id': user_id,
            },
        }
        
        return await self._send_request(data)
    
    
    async def activity_join_reject(self, user):
        """
        Rejects activity join invite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user, who's achievement will be updated.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            RPC client is not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped back by the discord client.
        """
        user_id = get_user_id(user)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_ACTIVITY_JOIN_REJECT,
            PAYLOAD_KEY_PARAMETERS: {
                'user_id': user_id,
            },
        }
        
        return await self._send_request(data)
