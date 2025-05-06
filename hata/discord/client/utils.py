__all__ = (
    'Typer', 'run_console_till_interruption', 'start_clients', 'stop_clients', 'wait_for_interruption'
)

import sys
from threading import current_thread
from time import sleep as blocking_sleep

from scarletio import CancelledError, Task, TaskGroup, get_last_module_frame, sleep
from scarletio.tools.asynchronous_interactive_console import (
    create_banner, create_exit_message, run_asynchronous_interactive_console
)

from ... import __package__ as PACKAGE_NAME
from ..core import CLIENTS, KOKORO
from ..permission import Permission
from ..permission.constants import PERMISSION_KEY

PACKAGE = __import__(PACKAGE_NAME)


def start_clients():
    """
    Starts up all the not running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS.values():
        if client.running:
            continue
        
        Task(KOKORO, client.connect())
    
    if (current_thread() is not KOKORO):
        KOKORO.wake_up()


def stop_clients():
    """
    Stops all the running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS.values():
        if client.running:
            Task(KOKORO, client.disconnect())
    
    if (current_thread() is not KOKORO):
        KOKORO.wake_up()


def wait_for_interruption():
    """
    Waits for keyboard interruption. If occurred, shuts down all the clients and closes the event loop. This operation
    is unreleasable.
    
    > Shutting down the clients might take a few seconds depending on the added shutdown event handlers.
    
    Raises
    ------
    RuntimeError
        If used inside of the event loop of clients.
    KeyboardInterrupt
        The received keyboard interrupt.
    """
    if current_thread() is KOKORO:
        raise RuntimeError(f'`wait_for_interruption` cannot be used inside of {KOKORO!r}.')
    
    try:
        while True:
            # sleep 1 day
            blocking_sleep(86400.0)
    except KeyboardInterrupt as err:
        exception = err
    else:
        # should not happen
        exception = None
    
    _exit_callback()
    
    KOKORO.stop()
    
    # reraise exception
    if (exception is not None):
        raise exception


def _exit_callback():
    """
    Callback used by ``wait_for_interruption`` and ``run_console_till_interruption``
    to stop the running clients.
    """
    sys.stdout.write('\ninterrupted ...\n')
    
    TaskGroup(
        KOKORO,
        (Task(KOKORO, client.disconnect()) for client in CLIENTS.values())
    ).wait_all().sync_wrap().wait()


IGNORED_CONSOLE_VARIABLES = {'__name__', '__package__', '__loader__', '__spec__'}

def run_console_till_interruption():
    """
    Runs interactive console.
    
    On system exit shuts down all the clients and closes the event loop.
    
    > Shutting down the clients might take a few seconds depending on the added shutdown event handlers.
    
    Raises
    ------
    RuntimeError
        If used inside of the event loop of clients.
    """
    if current_thread() is KOKORO:
        raise RuntimeError(f'`run_console_till_interruption` cannot be used inside of {KOKORO!r}.')
    
    frame = get_last_module_frame()
    
    interactive_console_locals = {}
    for variable_name, variable_value in frame.f_globals.items():
        if (variable_name not in IGNORED_CONSOLE_VARIABLES):
            interactive_console_locals[variable_name] = variable_value
    
    run_asynchronous_interactive_console(
        interactive_console_locals,
        banner = create_banner(PACKAGE),
        exit_message = create_exit_message(PACKAGE),
        callback = _exit_callback,
        stop_on_interruption = True,
    )


class UserGuildPermission:
    """
    Represents a user's permissions inside of a guild. Returned by ``Client.user_guild_get_all``.
    
    Attributes
    ----------
    owner : `bool`
        Whether the user is the owner of the guild.
    permission : ``Permission``
        The user's permissions at the guild.
    """
    __slots__ = ('owner', 'permission', )
    
    def __init__(self, data):
        """
        Creates a ``GuildPermission`` object form user guild data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild permission data.
        """
        self.owner = data['owner']
        self.permission = Permission(data[PERMISSION_KEY])
    
    
    def __repr__(self):
        """Returns the user guild permission's representation."""
        return f'<{self.__class__.__name__}  owner = {self.owner}, permissions = {self.permission:d}>'
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    
    def __iter__(self):
        """Unpacks the user guild permission."""
        yield self.owner
        yield self.permission


class Typer:
    """
    A typer what will keep sending typing events to the given channel with the client. Can be used as a context
    manager.
    
    After entered as a context manager sends a typing event each `8` seconds to the given channel.
    
    Attributes
    ----------
    client : ``Client``
        The client what will send the typing events.
    channel_id : `int`
        The channel's id where typing will be triggered.
    timeout : `float`
        The leftover timeout till the typer will send typing events. Is reduced every time, when the typer sent a typing
        event. If goes under `0.0` the typer stops sending more events.
    waiter : ``Future``, `None`
        The sleeping future what will wake_up ``.run``.
    """
    __slots__ = ('channel_id', 'client', 'timeout', 'waiter',)
    
    def __init__(self, client, channel_id, timeout = 300.0):
        """
        Parameters
        ----------
        client : ``Client``
            The client what will send the typing events.
        channel_id : `int`
            The channel's id where typing will be triggered.
        timeout : `float` = `300.0`, Optional
            The maximal amount of time till the client will keep sending typing events. Defaults to `300.0`.
        """
        self.client = client
        self.channel_id = channel_id
        self.waiter = None
        self.timeout = timeout
    
    
    def __enter__(self):
        """Enters the typer's context block by ensuring it's ``.run`` method."""
        Task(KOKORO, self.run())
        return self
    
    
    async def run(self):
        """
        The coroutine what keeps sending the typing requests.
        
        This method is a coroutine.
        """
        # js client's typing is 8s
        while self.timeout > 0.0:
            self.timeout -= 8.0
            self.waiter = waiter = sleep(8.0, KOKORO)
            await self.client.api.typing(self.channel_id)
            await waiter
        
        self.waiter = None
    
    
    def __await__(self):
        """Keeps typing till timeout occurs."""
        while True:
            timeout = self.timeout
            if timeout <= 0.0:
                break
            
            self.timeout = new_timeout = timeout - 8.0
            if new_timeout < 0.0:
                sleep_duration = 8.0 + new_timeout
            else:
                sleep_duration = 8.0
            
            self.waiter = waiter = sleep(sleep_duration, KOKORO)
            yield from self.client.api.typing(self.channel_id).__await__()
            
            try:
                yield from waiter
            except CancelledError:
                # Reraise if cancelled from outside
                if (self.waiter is not None):
                    raise
    
    
    def cancel(self):
        """
        If the context manager is still active, cancels it.
        """
        self.timeout = 0.0
        waiter = self.waiter
        if (waiter is not None):
            self.waiter = None
            waiter.cancel()
    
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Exits the typer's context block by cancelling it."""
        self.cancel()
        return False
