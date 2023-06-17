__all__ = ()

import sys
from datetime import datetime as DateTime
from shutil import copy2 as copy_file
from os import mkdir as create_directory
from os.path import abspath as absolute_path, dirname as get_parent_directory_path, exists, join as join_paths

from scarletio import Future, LOOP_TIME, Task, TaskGroup, WeakReferer

from ....discord import (
    CLIENTS, DATETIME_FORMAT_CODE, KOKORO, stop_clients, run_console_till_interruption, wait_for_interruption
)
from ...core import register


PROFILING_LIBRARY = None


def _log(message):
    """
    Logs the given message.
    
    Parameters
    ----------
    message : `str`
        The message to log.
    """
    sys.stdout.write(f'{DateTime.utcnow():{DATETIME_FORMAT_CODE}} {message}\n')


class ConnectionEventHandler:
    """
    handler of launch and shutdown event handlers.
    
    Attributes
    ----------
    _client_reference : ``WeakReferer`` to ``Client``
        Reference to the respective client.
    _do_log : `bool`
        Whether actions should be logged.
    _launch_handler : `int`
        Whether the event handler is a launch handler.
    _waiter : ``Future``
        The respective future.
    """
    __slots__ = ('_client_reference', '_do_log', '_launch_handler', '_waiter')
    
    def __new__(cls, client, waiter, launch_handler, do_log):
        """
        Creates a new launch and shutdown event handler.
        
        Parameters
        ----------
        waiter : ``Future``
            The respective future.
        launch_handler : `int`
            Whether the event handler is a launch handler.
        do_log : `bool`
            Whether actions should be logged.
        """
        self = object.__new__(cls)
        self._client_reference = WeakReferer(client)
        self._do_log = do_log
        self._launch_handler = launch_handler
        self._waiter = waiter
        return self
    
    
    def __repr__(self):
        """Returns the event handler's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self.is_cancelled():
            repr_parts.append(' cancelled')
        
        repr_parts.append('shutdown' if self._launch_handler else 'launch')
        repr_parts.append(' event handler')
        
        client = self.get_client()
        if (client is not None):
            repr_parts.append(' of client: ')
            repr_parts.append(repr(client))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @property
    def __event_name__(self):
        """
        Returns of which event the event handler is responsible for.
        
        Returns
        -------
        event_name : `str`
        """
        if self._launch_handler:
            event_name = 'launch'
        else:
            event_name = 'shutdown'
        
        return event_name
    
    
    def get_client(self):
        """
        Returns the client to which one is the event handler bound.
        
        Returns
        -------
        client : `None`, ``Client``
        """
        client_reference = self._client_reference
        if (client_reference is not None):
            return client_reference()
    
    
    def cancel(self):
        """
        Cancels the event handler.
        """
        waiter = self._waiter
        if (waiter is None):
            return
        
        self._waiter = None
        
        client = self.get_client()
        if (client is not None):
            client.events.remove(self)
        
        self._client_reference = None
    
    
    def is_cancelled(self):
        """
        Returns whether the event handler is already cancelled.
        """
        return (self._waiter is None)
    
    
    async def __call__(self, client):
        """
        Calls the event handler.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        """
        waiter = self._waiter
        if (waiter is None):
            return
            
        waiter.set_result_if_pending(self._launch_handler)
        
        client = self.get_client()
        
        self.cancel()
        
        if (client is not None) and self._do_log:
            _log_client_connection(client, self._launch_handler)


def _log_clients_start_begin(clients):
    """
    Logs when how much clients are being started.
    
    Parameters
    ----------
    clients : `list` of ``Client``
        All the clients to start.
    """
    total_count = len(CLIENTS)
    client_count = len(clients)
    
    if total_count != client_count:
        message = f'Starting {total_count - client_count} / {total_count} clients ({client_count} already running)'
    else:
        message = f'Starting {total_count} bots'
    _log(message)


def _log_clients_start_finish(clients, duration):
    """
    Logs when how much clients started
    
    Parameters
    ----------
    clients : `list` of ``Client``
        All the clients to start.
    duration : `float`
        How long logging in took.
    """
    client_count = len(clients)
    connected_count = sum(client.running for client in clients)
    
    if client_count == connected_count:
        message = f'All clients connected. Took {duration:.02f} seconds.'
    else:
        message = f'{connected_count} / {client_count} clients connected. Took {duration:.02f} seconds.'
    _log(message)


def _log_client_authorization(client, authorized):
    """
    Logs client authorization.
    
    Parameters
    ----------
    client : ``Client``
        The client who's connection was started.
    authorized : `bool`
        Whether the client authorized.
    """
    if authorized:
        message = f'Client authorized: {client.full_name} {client.id}'
    else:
        message = f'Client authorization failed: {client.id}'
    _log(message)


def _log_client_connection(client, launched):
    """
    Logs client connection.
    
    Parameters
    ----------
    client : ``Client``
        The client who's connection was started.
    launched : `int`
        Whether the client launched.
    """
    message = f'Client {"connected" if launched else "connection failed"}: {client.full_name} {client.id}'
    _log(message)


async def _client_start(client, connection_waiter, do_log):
    """
    Starts the given client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to log in.
    connection_waiter : ``Future``
        Future to set result when the connection finished.
    do_log : `bool`
        Whether actions should be logged.
    """
    try:
        try:
            authorized = await client.connect()
        except GeneratorExit:
            raise
    
        if do_log:
            _log_client_authorization(client, authorized)
    except:
        connection_waiter.set_result_if_pending(0)
        raise
    
    else:
        if not authorized:
            connection_waiter.set_result_if_pending(0)


async def _connect_clients(do_log):
    """
    Connects the clients logging their status.
    
    This function is a coroutine.
    
    Parameters
    ----------
    do_log : `bool`
        Whether actions should be logged.
    """
    if do_log:
        start_time = LOOP_TIME()
    
    clients = [client for client in CLIENTS.values() if not client.running]
    
    if do_log:
        _log_clients_start_begin(clients)
    
    connection_waiters = [Future(KOKORO) for client in clients]
    
    event_handlers = []
    
    for client, connection_waiter in zip(clients, connection_waiters):
        Task(KOKORO, _client_start(client, connection_waiter, do_log))
        
        for is_launch_handler in range(2):
            event_handler = ConnectionEventHandler(client, connection_waiter, is_launch_handler, do_log)
            client.events(event_handler)
            event_handlers.append(event_handler)
    
    # clear up reference.
    event_handler = None
    
    try:
        await TaskGroup(KOKORO, connection_waiters).wait_all()
    except:
        stop_clients()
        raise
    
    else:
        connected_count = sum(waiter.get_result() for waiter in connection_waiters)
    
    finally:
        for event_handler in event_handlers:
            event_handler.cancel()
        
        # clear up references.
        connection_waiters = None
        event_handler = None
        event_handlers = None
    
    
    if do_log:
        _log_clients_start_finish(clients, LOOP_TIME() - start_time)
    
    return connected_count


def _check_profiling_available():
    """
    Checks whether profiling library is available.
    
    Returns
    -------
    available : `bool`
    """
    global PROFILING_LIBRARY
    try:
        import yappi
    except ModuleNotFoundError:
        return False
    
    PROFILING_LIBRARY = yappi
    yappi.set_clock_type('cpu')
    return True


def _begin_profiling():
    """
    Begins profiling if available.
    
    Should be called after ``_check_profiling_available``.
    """
    if PROFILING_LIBRARY is None:
        return
    
    PROFILING_LIBRARY.start(builtins = True)


def _stop_profiling():
    """
    Stops profiling if available.
    
    Should be called after ``_begin_profiling``.
    """
    if PROFILING_LIBRARY is None:
        return
    
    directory_path = absolute_path('.profiles')
    
    if not exists(directory_path):
        # If the current directory was deleted dont write logs.
        if not exists(get_parent_directory_path(directory_path)):
            return
        
        create_directory(directory_path)
    
    PROFILING_LIBRARY.stop()
    stats = PROFILING_LIBRARY.get_func_stats()
    stats = PROFILING_LIBRARY.convert2pstats(stats)
    
    file_path_latest = join_paths(directory_path, 'latest.prof')
    file_path_history = join_paths(directory_path, f'{DateTime.utcnow():%Y_%m_%d_%H_%M_%S}.prof')
    
    try:
        stats.dump_stats(file_path_latest)
        copy_file(file_path_latest, file_path_history)
    except FileNotFoundError:
        # No need to panic.
        pass


@register
def run(
    *,
    console: bool = False,
    log: bool = True,
    profile: bool = False,
):
    """
    Starts the created Discord bots.
    
    On keyboard interrupt shuts the bots down. It might take a few seconds.
    
    When `--console` is defined it will start an interactive console after the clients started up.
    When `--log` is defined (default) logging in status will be logged into `sys.stdout`.
    When `--profile`` is defined a `.prof` file will be created on exit under the `.prof` directory.
    To open the latest profile file use `snakeviz .profiles/latest.prof` (example).
    """
    if profile and (not _check_profiling_available()):
        sys.stdout.write(f'Profiling library not available. Please install `yappi`.\n')
        return
    
    try:
        _begin_profiling()
        
        connected_count = KOKORO.run(_connect_clients(log))
        
        if console:
            run_console_till_interruption()
        elif connected_count:
            wait_for_interruption()
    except KeyboardInterrupt as err:
        raise SystemExit from err
    
    finally:
        _stop_profiling()
