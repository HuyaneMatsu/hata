__all__ = ('RPCClient', )

import sys
from sys import platform as PLATFORM
from os import  getpid as get_process_identifier
from threading import current_thread

from ...backend.utils import to_json, from_json
from ...backend.event_loop import EventThread
from ...backend.futures import Task, Future, future_or_timeout, sleep
from ...discord.core import KOKORO
from ...discord.preconverters import preconvert_snowflake
from ...discord.client.request_helpers import get_user_id, get_guild_id
from ...discord.activity import ActivityRich
from ...discord.user import ZEROUSER

from .certified_device import CertifiedDevice
from .constants import OPERATION_CLOSE, PAYLOAD_KEY_COMMAND, PAYLOAD_KEY_NONCE, OPERATION_FRAME, IPC_VERSION, \
    OPERATION_VALUE_TO_NAME, DEFAULT_OPERATION_NAME, OPERATION_HANDSHAKE, REQUEST_TIMEOUT, CLOSE_PAYLOAD_KEY_CODE, \
    PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET, CLOSE_PAYLOAD_KEY_MESSAGE, PAYLOAD_KEY_PARAMETERS, PAYLOAD_KEY_EVENT, \
    PAYLOAD_COMMAND_ACTIVITY_JOIN_ACCEPT, PAYLOAD_COMMAND_ACTIVITY_SET, PAYLOAD_COMMAND_ACTIVITY_JOIN_REJECT, \
    PAYLOAD_COMMAND_UNSUBSCRIBE, PAYLOAD_COMMAND_SUBSCRIBE, RECONNECT_INTERVAL, RECONNECT_RATE_LIMITED_INTERVAL, \
    CLOSE_CODES_RECONNECT, CLOSE_CODE_RATE_LIMITED, CLOSE_CODES_FATAL
from .command_handling import COMMAND_HANDLERS
from .utils import get_ipc_path, check_for_error

PROCESS_IDENTIFIER = get_process_identifier()

class RPCClient:
    """
    Attributes
    ----------
    _auto_nonce : `int`
        Auto nonce generation index for the next request.
    _connection_waiter : `None` or ``Future``
        Waiter for client connection.
    _protocol : `None` or ``BaseProtocol``
        The connected protocol if any.
    _response_waiters : `dict` of (`str`, ``Future``) items
        Waiters for each request response.
    application_id : `int`
        The respective application's identifier.
    running : `bool`
        Whether the client is connected and running.
    user : ``ClientUserBase``
        The logged in user to the local Discord client.
        
        Set after connection. Defaults to `ZEROUSER`.
    """
    __slots__ = ('_auto_nonce', '_connection_waiter', '_protocol', '_response_waiters', 'application_id', 'running',
        'user')
    
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
            - If any parameter's type is incorrect.
        ValueError
            - If any parameter's value is incorrect.
        """
        application_id = preconvert_snowflake(application_id, 'application_id')
        
        self = object.__new__(cls)
        self.application_id = application_id
        self.running = False
        self._protocol = None
        self._response_waiters = {}
        self._auto_nonce = 0
        self._connection_waiter = None
        self.user = ZEROUSER
        return self
    
    
    def start(self):
        """
        Starts the ipc clients's connecting to Discord. If the client is already running, raises `RuntimeError`.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `bool`, ``Task`` or ``FutureAsyncWrapper``
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
        
        task = Task(self.connect(), KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(thread, EventThread):
            # `.async_wrap` wakes up KOKORO
            return task.async_wrap(thread)
        
        KOKORO.wake_up()
        return task.sync_wrap().wait()
    
    
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
        
        Task(self._connect(ipc_path), KOKORO)
        
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
                        sys.stderr.write(f'Received unexpected operation in handshake, got {operation_name}, '
                            f'({operation}).')
        
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
            protocol = await KOKORO.open_unix_connection(ipc_path)
            self._protocol = protocol
    else:
        async def _open_pipe(self, ipc_path):
            raise NotImplemented(f'Opening interprocess connection is not supported on {PLATFORM}.')
    
    
    
    
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
        self._auto_nonce = nonce = self._auto_nonce+1
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
        
        future_or_timeout(waiter, REQUEST_TIMEOUT)
        try:
            await self._send_data(OPERATION_FRAME, payload)
            return await waiter
        finally:
            try:
                del self._response_waiters[nonce]
            except KeyError:
                pass
    
    
    def stop(self, data):
        """
        Closes the rpc client.
        
        Parameters
        ----------
        data : `None` or `bytes`
            Received close data.
        """
        self.running = False
    
    
    async def subscribe(self, event, guild):
        """
        Subscribes to an event.
        
        Parameters
        ----------
        event : `str`
            The event's name to unsubscribe from.
        guild : ``Guild`` or `int`
            The guild where to subscribe for the event.
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild``, nor `int` instance.
        
        Raises
        ------
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
        """
        guild_id = get_guild_id(guild)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_SUBSCRIBE,
            PAYLOAD_KEY_PARAMETERS: {
                'guild_id': guild_id,
            },
            PAYLOAD_KEY_EVENT: event,
        }
        
        return await self._send_request(data)
    
    
    async def unsubscribe(self, event, guild):
        """
        Unsubscribes from an event.
        
        Parameters
        ----------
        event : `str`
            The event's name to unsubscribe from.
        guild : ``Guild`` or `int`
            The guild where to subscribe for the event.
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild``, nor `int` instance.
        
        Raises
        ------
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
        """
        guild_id = get_guild_id(guild)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_UNSUBSCRIBE,
            PAYLOAD_KEY_PARAMETERS: {
                'guild_id': guild_id,
            },
            PAYLOAD_KEY_EVENT: event,
        }
        
        return await self._send_request(data)
        
    
    async def set_certified_devices(self, *devices):
        """
        Sends information about the current state of hardware certified devices that are connected to Discord.
        
        This method is a coroutine.
        
        Attributes
        ----------
        *devices : ``CertifiedDevice``
            Certified devices.
        
        Raises
        ------
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
        """
        if __debug__:
            for device in devices:
                if not isinstance(device, CertifiedDevice):
                    raise AssertionError(f'Devices can be `{CertifiedDevice.__name__}` instances, got '
                        f'{device.__class__.__name__}.')
        
        device_datas = [device.to_data() for device in devices]
        
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET,
            PAYLOAD_KEY_PARAMETERS: {
                'devices': device_datas,
            },
        }
        
        return await self._send_request(data)
    
    
    async def activity_set(self, activity):
        """
        Sets activity to the client.
        
        This method is a coroutine.
        
        Parameters
        ----------
        activity : ``ActivityRich``
            The activity to set.
        
        Returns
        -------
        activity : ``ActivityRich``
            The set activity.
        
        Raises
        ------
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
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
        
        return await self._send_request(data)
    
    
    async def activity_join_accept(self, user):
        """
        Accepts activity join invite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase`` or `int` instance
            The user, who's achievement will be updated.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int` instance.
            - If `achievement` was not given neither as ``Achievement``, neither as `int` instance.
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
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
        user : ``ClientUserBase`` or `int` instance
            The user, who's achievement will be updated.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int` instance.
            - If `achievement` was not given neither as ``Achievement``, neither as `int` instance.
        ConnectionError
            RPC client not connected.
        TimeoutError
            No response received within timeout interval.
        DiscordRPCError
            Any exception dropped by back the discord client.
        """
        user_id = get_user_id(user)
        
        data = {
            PAYLOAD_KEY_COMMAND: PAYLOAD_COMMAND_ACTIVITY_JOIN_REJECT,
            PAYLOAD_KEY_PARAMETERS: {
                'user_id': user_id,
            },
        }
        
        return await self._send_request(data)
