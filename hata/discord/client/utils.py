__all__ = (
    'ClientWrapper', 'BanEntry', 'Typer', 'run_console_till_interruption', 'start_clients', 'stop_clients',
    'wait_for_interruption'
)

import sys
from threading import current_thread
from time import sleep as blocking_sleep

from scarletio import CancelledError, Task, WaitTillAll, get_last_module_frame, include, sleep
from scarletio.tools.asynchronous_interactive_console import (
    create_banner, create_exit_message, run_asynchronous_interactive_console
)

from ... import __package__ as PACKAGE_NAME
from ..core import CLIENTS, KOKORO
from ..permission import Permission
from ..permission.utils import PERMISSION_KEY

PACKAGE = __import__(PACKAGE_NAME)


Client = include('Client')

def start_clients():
    """
    Starts up all the not running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS.values():
        if client.running:
            continue
        
        Task(client.connect(), KOKORO)
    
    if (current_thread() is not KOKORO):
        KOKORO.wake_up()


def stop_clients():
    """
    Stops all the running clients.
    
    Can be called from any thread.
    """
    for client in CLIENTS.values():
        if client.running:
            Task(client.disconnect(), KOKORO)
    
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
    
    sys.stdout.write('\ninterrupted ...\n')
    
    WaitTillAll([Task(client.disconnect(), KOKORO) for client in CLIENTS.values()], KOKORO).sync_wrap().wait()
    KOKORO.stop()
    
    # reraise exception
    if (exception is not None):
        raise exception


def _console_exit_callback():
    """
    Callback used by ``run_console_till_interruption`` to stop the running clients.
    """
    WaitTillAll([Task(client.disconnect(), KOKORO) for client in CLIENTS.values()], KOKORO).sync_wrap().wait()


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
        callback = _console_exit_callback,
        stop_on_interruption = True,
    )


class BanEntry:
    """
    A ban entry.
    
    Attributes
    ----------
    user : ``ClientUserBase``
        The banned user.
    reason : `None`, `str`
        The ban reason if applicable.
    """
    __slots__ = ('user', 'reason')
    
    def __init__(self, user, reason):
        """
        Creates a new ban entry instance.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The banned user.
        reason : `None`, `str`
            The ban reason if applicable.
        """
        self.user = user
        self.reason = reason
    
    
    def __repr__(self):
        """Returns the ban entry's representation."""
        return f'<{self.__class__.__name__} user={self.user!r}, reason={self.reason!r}>'
    
    
    def __len__(self):
        """Helper for unpacking."""
        return 2
    
    
    def __iter__(self):
        """Unpacks the ban entry."""
        yield self.user
        yield self.reason


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
        data : `dict` of (`str`, `Any`)
            Guild permission data.
        """
        self.owner = data['owner']
        self.permission = Permission(data[PERMISSION_KEY])
    
    
    def __repr__(self):
        """Returns the user guild permission's representation."""
        return f'<{self.__class__.__name__}  owner = {self.owner}, permissions = {int.__repr__(self.permission)}>'
    
    
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
        Task(self.run(), KOKORO)
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
            await self.client.http.typing(self.channel_id)
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
            yield from self.client.http.typing(self.channel_id).__await__()
            
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
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the typer's context block by cancelling it."""
        self.cancel()
        return False


class ClientWrapper:
    """
    Wraps together more clients enabling to add the same event handlers or commands to them. Tho for that feature, you
    need first import it's respective extension.
    
    Attributes
    ----------
    clients : ``Clients``
        The clients to wrap together.
    """
    __slots__ = ('clients',)
    
    def __new__(cls, *clients):
        """
        Creates a new ``ClientWrapper`` with the given clients. If no clients are given, then will wrap
        all the clients.
        
        Parameters
        ----------
        *clients : ``Client``
            The clients to wrap together.
        
        Raises
        ------
        TypeError
            A non ``Client`` was given.
        """
        if clients:
            for client in clients:
                if not isinstance(client, Client):
                    raise TypeError(
                        f'{cls.__name__} expects only `{Client.__name__}`, got '
                        f'{client.__class__.__name__}; {client!r}.'
                    )
        else:
            clients = tuple(CLIENTS.values())
        
        self = object.__new__(cls)
        object.__setattr__(self, 'clients', clients)
        return self
    
    
    def __repr__(self):
        """Returns the client wrapper's representation."""
        result = [self.__class__.__name__, '(']
        
        clients = self.clients
        limit = len(clients)
        if limit:
            index = 0
            while True:
                client = clients[index]
                result.append(client.full_name)
                
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(')')
        
        return ''.join(result)
    
    
    def events(self, func=None, name=None, overwrite=False):
        """
        Adds the given `func` as event handler to the contained clients' with the given parameters.
        
        If `func` parameter is not given, returns an ``._events_wrapper``, what allows using this method
        as a decorator with passing additional keyword parameters at the same time.
        
        Parameters
        ----------
        func : `None`, `callable` = `None`, Optional
            The event handler to add to the respective clients.
            
            If not given, will return a decorator.
        
        name : `None`, `str` = `None`, Optional
            The name to which event the handler should be registered to.
            
            If not given, it will be extracted from the handler's name.
        
        overwrite : `bool` = `False`, Optional
            Whether the current event handler(s) should be replaced by the added one.
        
        
        Returns
        -------
        func : `callable`
            The given `func`. ``._events_wrapper`` if `func` was not given.
        
        Raises
        ------
        AttributeError
            Invalid event name.
        TypeError
            - If `func` is given as `None`.
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional parameters as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """

        if func is None:
            return self._events_wrapper(self, (name, overwrite))
        
        for client in self.clients:
            client.events(func, name=name, overwrite=overwrite)
        
        return func
    
    
    class _events_wrapper:
        """
        When the parent ``ClientWrapper``'s `.events` is called without giving the `func` parameter to it an instance
        of this class is created for allowing using it as a decorator with passing additional keyword parameters at the
        same time.
        
        Attributes
        ----------
        parent : ``ClientWrapper``
            The owner event descriptor.
        parameters: `tuple` of `Any`
            Additional keyword parameters (in order) passed when the wrapper was created.
        """
        __slots__ = ('parent', 'parameters',)
        
        def __init__(self, parent, parameters):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``EventHandlerManager``
                The owner event descriptor.
            parameters: `tuple` of `Any`
                Additional keyword parameters (in order) passed when the wrapper was created.
            """
            self.parent = parent
            self.parameters = parameters
        
        
        def __call__(self, func):
            """
            Adds the given `func` as event handler to the parent's clients' with the stored up parameters.
            
            Parameters
            ----------
            func : `callable`
                The event handler to add to the respective clients.
            
            Returns
            -------
            func : `callable`
                The added callable.
            
            Raises
            ------
            AttributeError
                Invalid event name.
            TypeError
                - If `func` is given as `None`.
                - If `func` was not given as callable.
                - If `func` is not as async and neither cannot be converted to an async one.
                - If `func` expects less or more non reserved positional parameters as `expected` is.
                - If `name` was not passed as `None` or type `str`.
            """
            if func is None:
                raise TypeError('`func` is given as `None`.')
            
            return self.parent.events(func, *self.parameters)
    
    
    def __setattr__(self, attribute_name, attribute_value):
        """
        Sets the given event handler for the respective clients under the specified event name. Updates the respective
        event's parser(s) if needed.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the event.
        attribute_value : `callable`
            The event handler.
        
        Raises
        ------
        AttributeError
            ``EventHandlerManager`` has no attribute named as the given `attribute_name`.
        """
        for client in self.clients:
            client.events.__setattr__(attribute_name, attribute_value)
    
    
    def __delattr__(self, attribute_name):
        """
        Removes the event handler with the given name from the respective client's events.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the event.
        
        Raises
        ------
        AttributeError
            ``EventHandlerManager`` has no attribute named as the given `attribute_name`.
        """
        for client in self.clients:
            client.events.__delattr__(attribute_name)
