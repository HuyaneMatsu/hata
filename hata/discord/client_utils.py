# -*- coding: utf-8 -*-
__all__ = ('BanEntry', 'ClientWrapper', 'Typer', )

from math import inf
from collections import namedtuple

from ..backend.utils import basemethod, _spaceholder
from ..backend.event_loop import LOOP_TIME
from ..backend.futures import Future, sleep, Task

from .permission import Permission
from .role import PERMISSION_KEY
from .client_core import KOKORO, CLIENTS
from .rate_limit import RateLimitProxy

Client = NotImplemented

USER_CHUNK_TIMEOUT = 2.5



class SingleUserChunker(object):
    """
    A user chunk waiter, which yields after the first received chunk. Used at ``Client.request_members``.
    
    Attributes
    ----------
    timer : `Handle` or `None`
        The time-outer of the chunker, what will cancel if the timeout occurs.
    waiter : ``Future``
        The waiter future what will yield, when we receive the response, or when the timeout occurs.
    """
    __slots__ = ('timer', 'waiter',)
    
    def __init__(self, ):
        self.waiter = Future(KOKORO)
        self.timer = KOKORO.call_at(LOOP_TIME()+USER_CHUNK_TIMEOUT, type(self)._cancel, self)
    
    def __call__(self, event):
        """
        Called when a chunk is received with it's respective nonce.
        
        Parameters
        ----------
        event : ``GuildUserChunkEvent``
            The received guild user chunk's event.
        
        Returns
        -------
        is_last : `bool`
            ``SingleUserChunker`` returns always `True`, because it waits only for one event.
        """
        self.waiter.set_result_if_pending(event.users)
        timer = self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
        
        return True
    
    def _cancel(self):
        """
        The chunker's timer calls this method.
        
        Cancels ``.waiter`` and ``.timer``. After this method was called, the waiting coroutine will remove it's
        reference from the event handler.
        """
        self.waiter.cancel()
        
        timer = self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
    
    def cancel(self):
        """
        Cancels the chunker.
        
        This method should be called when when the chunker is canceller from outside. Before this method is called,
        it's references should be removed as well from the event handler.
        """
        self.waiter.set_result_if_pending([])
        
        timer = self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
    
    def __await__(self):
        """
        Awaits the chunker's waiter and returns that's result.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
            The received users. Can be an empty list.
        
        Raises
        ------
        CancelledError
            If timeout occurred.
        """
        return self.waiter.__await__()

class MassUserChunker(object):
    """
    A user chunk waiter, which yields after the chunks of certain amount of guilds are received. Used at
    ``Client._request_members`` and at ``Client._request_members``.
    
    Attributes
    ----------
    last : `float`
        The timestamp of the last received chunk.
    left : `int`
        The amount of guilds, which's chunks are not yet requested
    timer : `Handle` or `None`
        The time-outer of the chunker, what will cancel if the timeout occurs.
    waiter : ``Future``
        The waiter future what will yield, when we receive the response, or when the timeout occurs.
    """
    __slots__ = ('last', 'left', 'timer', 'waiter',)
    
    def __init__(self, left):
        """
        Parameters
        ----------
        left : `int`
            How much guild's chunks are left to be received.
        """
        self.left = left
        self.waiter = Future(KOKORO)
        self.last = now = LOOP_TIME()
        self.timer = KOKORO.call_at(now+USER_CHUNK_TIMEOUT, type(self)._cancel, self)
    
    def __call__(self, event):
        """
        Called when a chunk is received with it's respective nonce.
        
        Updates the chunker's last received chunk's time to push out the current timeout.
        
        Parameters
        ----------
        event : ``GuildUserChunkEvent``
            The received guild user chunk's event.
        
        Returns
        -------
        is_last : `bool`
            Whether the last chunk was received.
        """
        self.last = LOOP_TIME()
        if event.index+1 != event.count:
            return False
        
        self.left = left = self.left-1
        if left > 0:
            return False
        
        self.waiter.set_result_if_pending(None)
        timer = self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
        
        return True
    
    def _cancel(self):
        """
        The chunker's timer calls this method. If the chunker received any chunks since it's ``.timer`` was started,
        pushes out the timeout.
        
        Cancels ``.waiter`` and ``.timer``. After this method was called, the waiting coroutine will remove it's
        reference from the event handler.
        """
        now = LOOP_TIME()
        next_ = self.last + USER_CHUNK_TIMEOUT
        if next_ > now:
            self.timer = KOKORO.call_at(next_, type(self)._cancel, self)
        else:
            self.timer = None
            self.waiter.cancel()
    
    def cancel(self):
        """
        Cancels the chunker.
        
        This method should be called when when the chunker is canceller from outside. Before this method is called,
        it's references should be removed as well from the event handler.
        """
        self.left = 0
        self.waiter.set_result_if_pending(None)
        
        timer = self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
    
    def __await__(self):
        """
        Awaits the chunker's waiter.
        
        Raises
        ------
        CancelledError
            If timeout occurred.
        """
        return self.waiter.__await__()

class DiscoveryCategoryRequestCacher(object):
    """
    Cacher for storing ``Client``'s requests.
    
    Attributes
    ----------
    _active_request : `bool`
        Whether there is an active request.
    _last_update : `float`
        The last time when the cache was updated
    _waiter : ``Future`` or `None`
        Waiter to avoid concurrent calls.
    cached : `Any`
        Last result.
    func : `callable`
        Async callable, what's yields are cached.
    timeout : `float`
        The time interval between what the requests should be done.
    """
    __slots__ = ('_active_request', '_last_update', '_waiter', 'cached', 'func', 'timeout',)
    def __init__(self, func, timeout, cached=_spaceholder):
        """
        Creates a ``DiscoveryCategoryRequestCacher`` instance.
        
        Parameters
        ----------
        timeout : `float`
            The time after new request should be executed.
        func : `callable`
            Async callable, what's yields would be cached.
        cached : `Any`, Optional
            Whether there should be an available cache by default.
        """
        self.func = func
        self.timeout = timeout
        self.cached = cached
        self._waiter = None
        self._active_request = False
        self._last_update = -inf
    
    def __get__(self, client, type_):
        if client is None:
            return self
        
        return basemethod(self.__class__.execute, self, client)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    async def execute(self, client):
        """
        Executes the request and returns it's result or raises.
        
        This method is a coroutine.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        ConnectionError
            If there is no internet connection, or there is no available cached result.
        DiscordException
            If any exception was received from the Discord API.
        """
        if (LOOP_TIME() - self.timeout) < self._last_update:
            if self._active_request:
                waiter = self._waiter
                if waiter is None:
                    waiter = self._waiter = Future(KOKORO)
                
                result = await waiter
            else:
                result = self.cached
            
            return result
        
        self._active_request = True
        try:
            result = await self.func(client)
        except ConnectionError as err:
            result = self.cached
            if (result is _spaceholder):
                waiter = self._waiter
                if (waiter is not None):
                    self._waiter = None
                    waiter.set_exception(err)
                
                raise
        
        except BaseException as err:
            waiter = self._waiter
            if (waiter is not None):
                self._waiter = None
                waiter.set_exception(err)
            
            raise
        
        else:
            self._last_update = LOOP_TIME()
        
        finally:
            self._active_request = False
        
        waiter = self._waiter
        if (waiter is not None):
            self._waiter = None
            waiter.set_result(result)
        
        return result
    
    def __repr__(self):
        """Returns the cacher's representation."""
        result = [
            self.__class__.__name__,
            '(func=',
            repr(self.func),
            ', timeout=',
            repr(self.timeout),
                ]
        
        cached = self.cached
        if (cached is not _spaceholder):
            result.append(' cached=')
            result.append(repr(cached))
        
        result.append(')')
        
        return ''.join(result)
    
    __call__ = execute

class TimedCacheUnit(object):
    """
    Timed cache unit used at keyed request cachers.
    
    Attributes
    ----------
    result : `str`
        The cached response object.
    creation_time : `float`
        The LOOP_TIME time when the last response was received.
    last_usage_time : `float`
        The monotonic time when this unit was last time used.
    """
    __slots__ = ('creation_time', 'last_usage_time', 'result')
    def __repr__(self):
        """Returns the timed cache unit's representation."""
        return (f'<{self.__class__.__name__} creation_time={self.creation_time!r}, last_usage_time='
                f'{self.last_usage_time!r}, result={self.result!r}>')

class DiscoveryTermRequestCacher(object):
    """
    Cacher for storing ``Client'' requests. Also uses other clients, if the source client's rate limits are already
    exhausted.
    
    Attributes
    ----------
    _last_cleanup : `float`
        The last time when a cleanup was done.
    _minimal_cleanup_interval : `float`
        The minimal time what needs to pass between cleanups.
    _rate_limit_proxy_args : `tuple` (``RateLimitGroup``, (``DiscordEntity`` or `None`))
        Rate limit proxy arguments used when looking up the rate limits of clients.
    _waiters : `dict` of (`str`, `
        Waiters for requests already being done.
    cached : `dict`
        Already cached responses.
    func : `callable`
        Async callable, what's yields are cached.
    timeout : `float`
        The timeout after the new request should be done instead of using the already cached response.
    """
    __slots__ =('_last_cleanup', '_minimal_cleanup_interval', '_rate_limit_proxy_args', '_waiters', 'cached', 'func',
        'timeout')
    def __init__(self, func, timeout, rate_limit_group, rate_limit_limiter=None,):
        """
        Creates a new ``DiscoveryTermRequestCacher`` object with the given parameters.
        
        Parameters
        ----------
        func : `callable`
            Async callable, what's yields are cached.
        timeout : `float`
            The timeout after the new request should be done instead of using the already cached response.
        rate_limit_group : ``RateLimitGroup``
            Rate limit group of the respective request.
        rate_limit_limiter : ``DiscordEntity``, Optional
            Rate limit limiter fo the respective request.
        """
        self.func = func
        self.timeout = timeout
        self.cached = {}
        self._rate_limit_proxy_args = (rate_limit_group, rate_limit_limiter)
        self._waiters = {}
        minimal_cleanup_interval = timeout / 10.0
        if minimal_cleanup_interval < 1800.0:
            minimal_cleanup_interval = 1800.0
        
        self._minimal_cleanup_interval = minimal_cleanup_interval
        self._last_cleanup = -inf
    
    def __get__(self, client, type_):
        if client is None:
            return self
        
        return basemethod(self.__class__.execute, self, client)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    async def execute(self, client, arg):
        """
        Executes the request and returns it's result or raises.
        
        This method is a coroutine.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        ConnectionError
            If there is no internet connection, or there is no available cached result.
        TypeError
            The given `arg` was not passed as `str` instance.
        DiscordException
            If any exception was received from the Discord API.
        """
        # First check arg
        arg_type = arg.__class__
        if arg_type is str:
            pass
        elif issubclass(arg_type, str):
            arg = str(arg)
        else:
            raise TypeError(f'The argument can be given as `str` instance, got {arg_type.__class__}.')
        
        # First check cache
        try:
            unit = self.cached[arg]
        except KeyError:
            unit = None
        else:
            now = LOOP_TIME()
            if self.timeout + unit.creation_time > now:
                unit.last_usage_time = now
                return unit.result
        
        # Second check actual request
        try:
            waiter = self._waiters[arg]
        except KeyError:
            pass
        else:
            if waiter is None:
                self._waiters[arg] = waiter = Future(KOKORO)
            
            return await waiter
        
        # No actual request is being done, so mark that we are doing a request.
        self._waiters[arg] = None
        
        # Search client with free rate limits.
        free_count = RateLimitProxy(client, *self._rate_limit_proxy_args).free_count
        if not free_count:
            requester = client
            for client_ in CLIENTS:
                if client_ is client:
                    continue
                
                free_count = RateLimitProxy(client_, *self._rate_limit_proxy_args).free_count
                if free_count:
                    requester = client_
                    break
                
                continue
            
            # If there is no client with free count do not care about the reset times, because probably only 1 client
            # forces requests anyways, so that's rate limits will reset first as well.
            client = requester
        
        # Do the request
        try:
            result = await self.func(client, arg)
        except ConnectionError as err:
            if (unit is None):
                waiter = self._waiters.pop(arg)
                if (waiter is not None):
                    waiter.set_exception(err)
                
                raise
            
            unit.last_usage_time = LOOP_TIME()
            result = unit.result
        
        except BaseException as err:
            waiter = self._waiters.pop(arg, None)
            if (waiter is not None):
                waiter.set_exception(err)
            
            raise
        
        else:
            if unit is None:
                self.cached[arg] = unit = TimedCacheUnit()
            
            now = LOOP_TIME()
            unit.last_usage_time = now
            unit.creation_time = now
            unit.result = result
        
        finally:
            # Do cleanup if needed
            now = LOOP_TIME()
            if self._last_cleanup + self._minimal_cleanup_interval < now:
                self._last_cleanup = now
                
                cleanup_till = now - self.timeout
                collected = []
                
                cached = self.cached
                for cached_arg, cached_unit in cached.items():
                    if cached_unit.last_usage_time < cleanup_till:
                        collected.append(cached_arg)
                
                for cached_arg in collected:
                    del cached[cached_arg]
        
        waiter = self._waiters.pop(arg)
        if (waiter is not None):
            waiter.set_result(result)
        
        return result
    
    def __repr__(self):
        """Returns the cacher's representation."""
        result = [
            self.__class__.__name__,
            '(func=',
            repr(self.func),
            ', timeout=',
            repr(self.timeout),
                ]
        
        rate_limit_group, rate_limit_limiter = self._rate_limit_proxy_args
        
        result.append(', rate_limit_group=')
        result.append(repr(rate_limit_group))
        
        if (rate_limit_limiter is not None):
            result.append(', rate_limit_limiter=')
            result.append(repr(rate_limit_limiter))
        
        result.append(')')
        
        return ''.join(result)
    
    __call__ = execute


class UserGuildPermission(object):
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
        """
        self.owner = data['owner']
        self.permission = Permission(data[PERMISSION_KEY])
    
    def __repr__(self):
        """Returns the user guild permission's representation."""
        return f'<{self.__class__.__name__}  owner={self.owner}, permissions={int.__repr__(self.permission)}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """Unpacks the user guild permission."""
        yield self.owner
        yield self.permission


class MultiClientMessageDeleteSequenceSharder(object):
    """
    Helper class of multi client message sequence deleter.
    
    Attributes
    ----------
    client : ``Client``
        The respective client.
    can_read_message_history : `int`
        Whether the `client` can read message history at the respective channel.
    can_manage_messages : `int`
        Whether the respective client can manage messages at the respective channel.
    delete_mass_task : `None` or ``Task``
        Task of bulk deleting messages.
    delete_new_task : `None` or ``Task``
        Task of deleting new or own messages.
    delete_old_task : `None` or ``Task``
        task of deleting other's old messages.
    """
    __slots__ = ('can_manage_messages', 'can_read_message_history', 'client', 'delete_mass_task', 'delete_new_task',
        'delete_old_task', )
    def __new__(cls, client, channel):
        """
        Creates a new helper instance of a multi client message sequence deleter.
        
        Parameters
        ----------
        client : ``Client``
            A client who would execute the delete task.
        channel : ``ChannelTextBase``
            Channel, from where the client would delete messages.
        
        Returns
        -------
        self : `None` or ``MultiClientMessageDeleteSequenceSharder``
            If the respective client could not contribute to any task, returns `None`.
        """
        permissions = channel.cached_permissions_for(client)
        if not permissions.can_view_channel:
            return None
        
        self = object.__new__(cls)
        self.client = client
        self.can_read_message_history = permissions.can_read_message_history
        self.can_manage_messages = permissions.can_manage_messages
        
        self.delete_mass_task = None
        self.delete_new_task = None
        self.delete_old_task = None
        
        return self
    

class WaitForHandler(object):
    """
    O(n) event waiter. Added as an event handler by ``Client.wait_for``.
    
    Attributes
    ----------
    waiters : `dict` of (``Future``, `callable`) items
        A dictionary which contains the waiter futures and the respective checks.
    """
    __slots__ = ('waiters', )
    def __init__(self):
        """
        Creates a new ``WaitForHandler`` instance.
        """
        self.waiters = {}
    
    async def __call__(self, client, *args):
        """
        Runs the checks of the respective event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective events.
        args : `tuple` of `Any`
            Other received arguments by the event.
        """
        for future, check in self.waiters.items():
            try:
                result = check(*args)
            except BaseException as err:
                future.set_exception_if_pending(err)
            else:
                if type(result) is bool:
                    if result:
                        if len(args) == 1:
                            args = args[0]
                    else:
                        return
                else:
                    args = (*args, result)
                
                future.set_result_if_pending(args)

class Typer(object):
    """
    A typer what will keep sending typing events to the given channel with the client. Can be used as a context
    manager.
    
    After entered as a context manager sends a typing event each `8` seconds to the given channel.
    
    Attributes
    ----------
    client : ``Client``
        The client what will send the typing events.
    channel_id : `int` instance
        The channel's id where typing will be triggered.
    timeout : `float`
        The leftover timeout till the typer will send typing events. Is reduced every time, when the typer sent a typing
        event. If goes under `0.0` the typer stops sending more events.
    waiter : ``Future`` or `None`
        The sleeping future what will wake_up ``.run``.
    """
    __slots__ = ('channel_id', 'client', 'timeout', 'waiter',)
    def __init__(self, client, channel_id, timeout=300.):
        """
        Parameters
        ----------
        client : ``Client``
            The client what will send the typing events.
        channel_id : `int` instance
            The channel's id where typing will be triggered.
        timeout : `float`, Optional
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
        while self.timeout > 0.:
            self.timeout -= 8.0
            self.waiter = waiter = sleep(8., KOKORO)
            await self.client.http.typing(self.channel_id)
            await waiter
        
        self.waiter = None
    
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


class ClientWrapper(object):
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
        Creates a new ``ClientWrapper`` instance with the given clients. If no clients are given, then will wrap
        all the clients.
        
        Parameters
        ----------
        *clients : ``Client``
            The clients to wrap together.
        
        Raises
        ------
        TypeError
            A non ``Client`` instance was given.
        """
        if clients:
            for client in clients:
                if not isinstance(client, Client):
                    raise TypeError(f'{cls.__name__} expects only `{Client.__name__}` instances to be given, got '
                        f'{client.__class__.__name__}: {client!r}.')
        else:
            clients = tuple(CLIENTS)
        
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
        Adds the given `func` as event handler to the contained clients's with the given parameters.
        
        If `func` argument is not given, returns an ``._events_wrapper`` instance, what allows using this method
        as a decorator with passing additional keyword arguments at the same time.
        
        Parameters
        ----------
        func : `callable`
            The event handler to add to the respective clients.
        
        Returns
        -------
        func : `callable`
            The given `func`, or ``._events_wrapper`` instance if `func` was not given.
        
        Raises
        ------
        AttributeError
            Invalid event name.
        TypeError
            - If `func` is given as `None`.
            - If `func` was not given as callable.
            - If `func` is not as async and neither cannot be converted to an async one.
            - If `func` expects less or more non reserved positional arguments as `expected` is.
            - If `name` was not passed as `None` or type `str`.
        """

        if func is None:
            return self._events_wrapper(self, (name, overwrite))
        
        for client in self.clients:
            client.events(func, name=name, overwrite=overwrite)
        
        return func
    
    class _events_wrapper(object):
        """
        When the parent ``ClientWrapper``'s `.events` is called without giving the `func` parameter to it an instance
        of this class is created for allowing using it as a decorator with passing additional keyword arguments at the
        same time.
        
        Attributes
        ----------
        parent : ``ClientWrapper``
            The owner event descriptor.
        args: `tuple` of `Any`
            Additional keyword arguments (in order) passed when the wrapper was created.
        """
        __slots__ = ('parent', 'args',)
        def __init__(self, parent, args):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``EventDescriptor``
                The owner event descriptor.
            args: `tuple` of `Any`
                Additional keyword arguments (in order) passed when the wrapper was created.
            """
            self.parent = parent
            self.args = args
        
        def __call__(self, func):
            """
            Adds the given `func` as event handler to the parent's clients's with the stored up parameters.
            
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
                - If `func` expects less or more non reserved positional arguments as `expected` is.
                - If `name` was not passed as `None` or type `str`.
            """
            if func is None:
                raise TypeError('`func` is given as `None`.')
            
            return self.parent(func, *self.args)
    
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
            ``EventDescriptor`` has no attribute named as the given `attribute_name`.
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
            ``EventDescriptor`` has no attribute named as the given `attribute_name`.
        """
        for client in self.clients:
            client.events.__delattr__(attribute_name)


def maybe_snowflake(value):
    """
    Converts the given `value` to `snowflake` if applicable. If not returns `None`.
    
    Parameters
    ----------
    value : `str`, `int` or `Any`
        A value what might be snowflake.
    
    Returns
    -------
    value : `int` or `None`
    
    Raises
    ------
    AssertionError
        - If `value` was passed as `str` and cannot be converted to `int`.
        - If the `value` is negative or it's bit length is over 64.
    """
    if isinstance(value, int):
        pass
    elif isinstance(value, str):
        if value.isdigit():
            if __debug__:
                if not 6 < len(value) < 21:
                    raise AssertionError('An `id` was given as `str` instance, but it\'s value is out of 64uint '
                        f'range, got {value!r}.')
            
            value = int(value)
        else:
            return None
    else:
        return None
    
    if __debug__:
        if value < 0 or value > ((1<<64)-1):
            raise AssertionError('An `id` was given as `str` instance, but it\'s value is out of 64uint range, got '
                f'{value!r}.')
    
    return value

BanEntry = namedtuple('BanEntry', ('user', 'reason'))
BanEntry.__doc__ = ("""
    A `namedtuple` instance representing a ban entry.
    
    Attributes
    ----------
    user : `User`` or ``Client``
        The banned user.
    reason : `None` or `str`
        The ban reason if applicable.
    """)


def maybe_snowflake_pair(value):
    """
    Checks whether the given value is a `tuple` of 2 snowflakes. If it, returns it, if not returns `None`.
    
    Parameters
    ----------
    value : `tuple` of (`str`, `int`) or `Any`
        A value what might be snowflake.
    
    Returns
    -------
    value : `tuple` (`int`, `int`) or `None`
    
    Raises
    ------
    AssertionError
        - If `value` contains a `str` element, what cannot be converted to `int`.
        - If `value` contains a value, what is negative or it's bit length is over 64.
    """
    if isinstance(value, tuple):
        if len(value) == 2:
            value_1, value_2 = value
            value_1 = maybe_snowflake(value_1)
            if value_1 is None:
                value = None
            else:
                value_2 = maybe_snowflake(value_2)
                if value_2 is None:
                    value = None
                else:
                    value = (value_1, value_2)
        else:
            value = None
    else:
        value = None
    
    return value
