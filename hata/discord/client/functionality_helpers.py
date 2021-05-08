__all__ = ()

from math import inf

from ...env import CACHE_PRESENCE

from ...backend.utils import basemethod
from ...backend.event_loop import LOOP_TIME
from ...backend.futures import Future, sleep

from ..core import KOKORO, CLIENTS
from ..rate_limit import RateLimitProxy
from ..gateway import DiscordGateway

USER_CHUNK_TIMEOUT = 2.5

class SingleUserChunker:
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

class MassUserChunker:
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


class DiscoveryCategoryRequestCacher:
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
    def __init__(self, func, timeout, cached=...):
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
            if (result is ...):
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
        if (cached is not ...):
            result.append(' cached=')
            result.append(repr(cached))
        
        result.append(')')
        
        return ''.join(result)
    
    __call__ = execute


class TimedCacheUnit:
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


class DiscoveryTermRequestCacher:
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
            for client_ in CLIENTS.values():
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
        repr_parts = [
            self.__class__.__name__,
            '(func=',
            repr(self.func),
            ', timeout=',
            repr(self.timeout),
        ]
        
        rate_limit_group, rate_limit_limiter = self._rate_limit_proxy_args
        
        repr_parts.append(', rate_limit_group=')
        repr_parts.append(repr(rate_limit_group))
        
        if (rate_limit_limiter is not None):
            repr_parts.append(', rate_limit_limiter=')
            repr_parts.append(repr(rate_limit_limiter))
        
        repr_parts.append(')')
        
        return ''.join(repr_parts)
    
    __call__ = execute



class MultiClientMessageDeleteSequenceSharder:
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
    

class WaitForHandler:
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


def _check_is_client_duped(client, client_id):
    """
    Checks whether the client is duplicated.
    
    Raises
    ------
    RuntimeError
        Creating the same client multiple times is not allowed.
    """
    try:
        other_client = CLIENTS[client_id]
    except KeyError:
        return
    
    if other_client is not client:
        raise RuntimeError(f'Creating the same client multiple times is not allowed; {client!r} already exists:, '
            f'{other_client!r}.')



def _message_delete_multiple_private_task_message_id_iterator(groups):
    """
    `message_id` iterator used by ``Client._message_delete_multiple_private_task``.
    
    This function is a generator.
    
    Parameters
    ----------
    groups : `tuple` (`deque` of (`bool`, `int`), `deque` of `int`, `deque` of `int`)
        `deque`-s, which contain message identifiers depending in which rate limit group they are bound to.
    
    Yields
    ------
    message_id : `int`
    """
    message_group_new, message_group_old, message_group_old_own = groups
    for item in message_group_new:
        yield item[1]
    
    yield from message_group_old
    yield from message_group_old_own



async def _request_members_loop(gateway, guilds):
    """
    Called by ``Client._request_members2`` parallelly with other ``request_members_loop``-s for each shard.
    
    The function requests all the members of given guilds without putting too much pressure on the respective
    gateway's rate limits.
    
    This function is a coroutine.
    
    Parameters
    ----------
    gateway : ``DiscordGateway``
        The gateway to use for requests.
    guilds : `list` of ``Guild``
        The guilds, what's members should be requested.
    """
    sub_data = {
        'guild_id': 0,
        'query': '',
        'limit': 0,
        'presences': CACHE_PRESENCE,
        'nonce' : '0000000000000000',
    }
    
    data = {
        'op': DiscordGateway.REQUEST_MEMBERS,
        'd': sub_data
    }
    
    for guild in guilds:
        sub_data['guild_id'] = guild.id
        await gateway.send_as_json(data)
        await sleep(0.6, KOKORO)

