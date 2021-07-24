__all__ = ()

import sys
from sys import platform as PLATFORM
from os.path import join as join_path
from os import listdir as list_directory, environ as ENVIRONMENTAL_VARIABLES, getpid as get_process_identifier
from tempfile import gettempdir as get_temporary_directory
from threading import current_thread

from ...backend.utils import set_docs, to_json, from_json
from ...backend.event_loop import EventThread
from ...backend.futures import Task, Future
from ...discord.core import KOKORO
from ...discord.preconverters import preconvert_snowflake

IPC_VERSION = 1

OPERATION_HANDSHAKE = 0
OPERATION_FRAME = 1
OPERATION_CLOSE = 2
OPERATION_PING = 3
OPERATION_PONG = 4

OPERATION_VALUE_TO_NAME = {
    OPERATION_HANDSHAKE: 'handshake',
    OPERATION_FRAME: 'frame',
    OPERATION_CLOSE: 'close',
    OPERATION_PING: 'ping',
    OPERATION_PONG: 'pong',
}

DEFAULT_OPERATION_NAME = 'unknown_operation',


PAYLOAD_COMMAND_DISPATCH = 'DISPATCH'
PAYLOAD_COMMAND_AUTHORIZE = 'AUTHORIZE'
PAYLOAD_COMMAND_AUTHENTICATE = 'AUTHENTICATE'
PAYLOAD_COMMAND_GUILD_GET = 'GET_GUILD'
PAYLOAD_COMMAND_GUILD_GET_ALL = 'GET_GUILDS'
PAYLOAD_COMMAND_CHANNEL_GET = 'GET_CHANNEL'
PAYLOAD_COMMAND_CHANNEL_GET_ALL = 'GET_CHANNELS'
PAYLOAD_COMMAND_SUBSCRIBE = 'SUBSCRIBE'
PAYLOAD_COMMAND_UNSUBSCRIBE = 'UNSUBSCRIBE'
PAYLOAD_COMMAND_USER_VOICE_SETTINGS_SET = 'SET_USER_VOICE_SETTINGS'
PAYLOAD_COMMAND_SELECT_CHANNEL_VOICE = 'SELECT_VOICE_CHANNEL'
PAYLOAD_COMMAND_CHANNEL_GET_JOINED = 'GET_SELECTED_VOICE_CHANNEL'
PAYLOAD_COMMAND_SELECT_CHANNEL_TEXT = 'SELECT_TEXT_CHANNEL'
PAYLOAD_COMMAND_VOICE_SETTINGS_GET = 'GET_VOICE_SETTINGS'
PAYLOAD_COMMAND_VOICE_SETTINGS_SET = 'SET_VOICE_SETTINGS'
PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET = 'SET_CERTIFIED_DEVICES'
PAYLOAD_COMMAND_ACTIVITY_SET = 'SET_ACTIVITY'
PAYLOAD_COMMAND_ACTIVITY_JOIN_ACCEPT = 'SEND_ACTIVITY_JOIN_INVITE'
PAYLOAD_COMMAND_ACTIVITY_JOIN_REJECT = 'CLOSE_ACTIVITY_REQUEST'

PAYLOAD_KEY_COMMAND = 'cmd'
PAYLOAD_KEY_NONCE = 'nonce'
PAYLOAD_KEY_EVENT = 'evt'
PAYLOAD_KEY_DATA = 'data'
PAYLOAD_KEY_PARAMETERS = 'args'

EVENT_ERROR = 'ERROR'


COMMAND_HANDLERS = {}
DISPATCH_EVENT_HANDLERS = {}

def handle_command_dispatch(self, data):
    dispatch_event_name = data[PAYLOAD_KEY_EVENT]
    try:
        dispatch_event_handler = DISPATCH_EVENT_HANDLERS[dispatch_event_name]
    except KeyError:
        sys.stderr.write(
            f'{self!r} cannot handle dispatch event {dispatch_event_name!r}.\n'
             f'Received data: {data!r}.'
        )
        return
    
    dispatch_event_handler(self, data)

COMMAND_HANDLERS[PAYLOAD_COMMAND_DISPATCH] = handle_command_dispatch
del handle_command_dispatch


if PLATFORM in ('linux', 'darwin'):
    TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('XDG_RUNTIME_DIR', None)
    if (TEMPORARY_DIRECTORY is None):
        TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TMPDIR', None)
        if (TEMPORARY_DIRECTORY is None):
            TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TMP', None)
            if (TEMPORARY_DIRECTORY is None):
                TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TEMP', None)
                if (TEMPORARY_DIRECTORY is None):
                    TEMPORARY_DIRECTORY = get_temporary_directory()
    
    def get_ipc_path(pipe):
        ipc = 'discord-ipc-'
        if (pipe is not None):
            ipc += pipe
        
        for path in (None, 'snap.discord', 'app/com.discordapp.Discord'):
            if path is None:
                full_path = TEMPORARY_DIRECTORY
            else:
                full_path = join_path(TEMPORARY_DIRECTORY)
            
            for node_name in list_directory(full_path):
                if node_name.startswith(ipc):
                    return join_path(full_path, node_name)
        
        return None

elif PLATFORM == 'win32':
    TEMPORARY_DIRECTORY = '\\\\?\\pipe'
    
    def get_ipc_path(pipe):
        ipc = 'discord-ipc-'
        if (pipe is not None):
            ipc += pipe
        
        for node_name in list_directory(TEMPORARY_DIRECTORY):
            if node_name.startswith(ipc):
                return join_path(TEMPORARY_DIRECTORY, node_name)
        
        return None

else:
    def get_ipc_path(pipe):
        return None


class DiscordRPCError(BaseException):
    """
    Discord RPC error code.
    
    Attributes
    ----------
    code : `int`
        Discord RPC error code.
    message : `str`
        Discord RPC error message.
    """
    def __init__(self, code, message):
        """
        Creates a new Discord RPC error instance with the given parameters.
        
        Parameters
        ----------
        code : `int`
            Discord RPC error code.
        message : `str`
            Discord RPC error message.
            
        """
        self.code = code
        self.message = message
        BaseException.__init__(self, code, message)
    
    def __repr__(self):
        """Returns the representation of the error code."""
        return f'{self.__class__.__name__}: [{self.code}] {self.message!r}'


def check_for_error(data):
    """
    Checks whether the given data contains an errors.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Data received from Discord.
    
    Raises
    ------
    DiscordRPCError
    """
    try:
        event = data[PAYLOAD_KEY_EVENT]
    except KeyError:
        pass
    else:
        if event == EVENT_ERROR:
            error_data = event[PAYLOAD_KEY_DATA]
            error_code = error_data['code']
            error_message = error_data['message']
            
            raise DiscordRPCError(error_code, error_message)


set_docs(get_ipc_path,
    """
    Gets Discord inter process communication path.
    
    Parameters
    ----------
    pipe : `None` or `str`
        # TODO
    
    Returns
    -------
    path : `None` or `str`
    """)


PROCESS_IDENTIFIER = get_process_identifier()

class IPCClient:
    """
    Attributes
    ----------
    application_id : `int`
        The respective application's identifier.
    protocol : `None` or ``BaseProtocol``
        The connected protocol if any.
    running : `bool`
        Whether the client is connected and running.
    """
    __slots__ = ('application_id', 'protocol', 'running')
    
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
        self.protocol = None
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
            If the client is already running.
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
        ipc_path = get_ipc_path(0)
        if (ipc_path is None):
            raise RuntimeError('Discord inter process communication path could not be detected.')
        
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        Task(self._connect(), KOKORO)
    
    async def _connect(self, ipc_path):
        """
        Raises
        ------
        NotImplemented
            Opening pipe is not supported on your platform.
        """
        while True:
            await self._open_pipe(ipc_path)
    
    async def _send_data(self, operation, data):
        protocol = self.protocol
        if (protocol is None):
            return
        
        data = to_json(data).encode()
        data_length = len(data)
        
        header = operation.to_bytes(4, 'little') + data_length.to_bytes(4, 'little')
        protocol.write(header)
        protocol.write(data)
        await protocol.drain()
    
    async def _receive_data(self):
        protocol = self.protocol
        if (protocol is None):
            return None
        
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
            protocol = KOKORO.open_unix_connection(ipc_path)
            self.protocol = protocol
    else:
        
        async def _open_pipe(self, ipc_path):
            raise NotImplemented
    
    async def _handshake(self):
        data = {
            'v': IPC_VERSION,
            'client_id': self.application_id,
        }
        
        await self._send_data(OPERATION_HANDSHAKE, data)
        
        operation, data = await self._receive_data()
        if operation == OPERATION_CLOSE:
            self.close()
        elif operation == OPERATION_FRAME:
            if data is None:
                raise RuntimeError(f'Received empty frame payload at handshake.')
            
            check_for_error(data)
            
            command = data.get(PAYLOAD_KEY_COMMAND, None)
            if (command is None) or (command != PAYLOAD_COMMAND_AUTHORIZE):
                raise RuntimeError(f'Received bad command after handshake, got: {command!r}')
            
        else:
            raise RuntimeError(f'Received unexpected operation in handshake, got '
                f'{OPERATION_VALUE_TO_NAME.get(operation, DEFAULT_OPERATION_NAME)}, ({operation}).')
