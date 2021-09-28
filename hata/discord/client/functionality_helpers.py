__all__ = ()

from math import inf
from datetime import datetime

from ...backend.utils import basemethod
from ...backend.event_loop import LOOP_TIME
from ...backend.futures import Future, Task, WaitTillFirst

from ..core import KOKORO, CLIENTS, CHANNELS
from ..http import RateLimitProxy
from ..utils import time_now, DISCORD_EPOCH
from ..exceptions import DiscordException
from ..channel import ChannelThread
from ..user import create_partial_user_from_id, thread_user_create
from ..permission.permission import PERMISSION_MASK_VIEW_CHANNEL

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
        users : `list` of ``ClientUserBase`` objects
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
    timer : `Handle` or `None`
        The time-outer of the chunker, what will cancel if the timeout occurs.
    waiter : ``Future``
        The waiter future what will yield, when we receive the response, or when the timeout occurs.
    """
    __slots__ = ('last', 'timer', 'waiter',)
    
    def __init__(self, left):
        """
        Parameters
        ----------
        left : `int`
            How much guild's chunks are left to be received.
        """
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
        Rate limit proxy parameters used when looking up the rate limits of clients.
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
            raise TypeError(f'The parameter can be given as `str` instance, got {arg_type.__class__}.')
        
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
        if not permissions&PERMISSION_MASK_VIEW_CHANNEL:
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
            Other received parameters by the event.
        """
        for future, check in self.waiters.items():
            try:
                result = check(*args)
            except BaseException as err:
                future.set_exception_if_pending(err)
            else:
                if isinstance(result, bool):
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
    `message_id` iterator used by ``_message_delete_multiple_private_task``.
    
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


async def _message_delete_multiple_private_task(client, channel_id, groups, reason):
    """
    Internal task used by ``Client.message_delete_multiple``.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    channel_id : `int`
        The channel's identifier, where the messages are.
    groups : `tuple` (`deque` of (`bool`, `int`), `deque` of `int`, `deque` of `int`)
        `deque`-s, which contain message identifiers depending in which rate limit group they are bound to.
    reason : `None` or `str`
        Additional reason which would show up in the guild's audit logs.
    
    Raises
    ------
    ConnectionError
        No internet connection.
    DiscordException
        If any exception was received from the Discord API.
    """
    for message in _message_delete_multiple_private_task_message_id_iterator(groups):
        await client.http.message_delete(channel_id, message.id, reason)


async def _message_delete_multiple_task(client, channel_id, groups, reason):
    """
    Internal task used by ``Client.message_delete_multiple``.
    
    This method is a coroutine.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier, where the messages are.
    groups : `tuple` (`deque` of (`bool`, `int`), `deque` of `int`, `deque` of `int`)
        `deque`-s, which contain message identifiers depending in which rate limit group they are bound to.
    reason : `None` or `str`
        Additional reason which shows up in the respective guild's audit logs.
    
    Raises
    ------
    ConnectionError
        No internet connection.
    DiscordException
        If any exception was received from the Discord API.
    """
    message_group_new, message_group_old, message_group_old_own = groups
    
    tasks = []
    
    delete_mass_task = None
    delete_new_task = None
    delete_old_task = None
    
    while True:
        if delete_mass_task is None:
            message_limit = len(message_group_new)
            
            # 0 is all good, but if it is more, lets check them
            if message_limit:
                message_ids = []
                message_count = 0
                limit = int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks - 10s
                
                while message_group_new:
                    own, message_id = message_group_new.popleft()
                    if message_id > limit:
                        message_ids.append(message_id)
                        message_count += 1
                        if message_count == 100:
                            break
                        continue
                    
                    if (message_id+20971520000) < limit:
                        continue
                    
                    # If the message is really older than the limit, with ignoring the 10 second, then we move it.
                    if own:
                        group = message_group_old_own
                    else:
                        group = message_group_old
                    
                    group.appendleft(message_id)
                    continue
                
                if message_count:
                    if message_count == 1:
                        if (delete_new_task is None):
                            message_id = message_ids[0]
                            delete_new_task = Task(client.http.message_delete(channel_id, message_id, reason), KOKORO)
                            tasks.append(delete_new_task)
                    else:
                        delete_mass_task = Task(
                            client.http.message_delete_multiple(channel_id, {'messages': message_ids}, reason),
                                KOKORO)
                        
                        tasks.append(delete_mass_task)
        
        if delete_old_task is None:
            if message_group_old:
                message_id = message_group_old.popleft()
                delete_old_task = Task(client.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                tasks.append(delete_old_task)
        
        if delete_new_task is None:
            if message_group_new:
                group = message_group_new
            elif message_group_old_own:
                group = message_group_old_own
            else:
                group = None
            
            if (group is not None):
                message_id = message_group_old_own.popleft()
                delete_new_task = Task(client.http.message_delete(channel_id, message_id, reason), KOKORO)
                tasks.append(delete_new_task)
        
        if not tasks:
            # It can happen, that there are no more tasks left,  at that case we check if there is more message
            # left. Only at `message_group_new` can be anymore message, because there is a time interval of 10
            # seconds, what we do not move between categories.
            if not message_group_new:
                break
            
            # We really have at least 1 message at that interval.
            own, message_id = message_group_new.popleft()
            # We will delete that message with old endpoint if not own, to make
            # Sure it will not block the other endpoint for 2 minutes with any chance.
            if own:
                delete_new_task = Task(client.http.message_delete(channel_id, message_id, reason), KOKORO)
            else:
                delete_old_task = Task(client.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
            
            tasks.append(delete_old_task)
        
        done, pending = await WaitTillFirst(tasks, KOKORO)
        
        for task in done:
            tasks.remove(task)
            try:
                result = task.result()
            except (DiscordException, ConnectionError):
                for task in tasks:
                    task.cancel()
                raise
            
            if task is delete_mass_task:
                delete_mass_task = None
                continue
            
            if task is delete_new_task:
                delete_new_task = None
                continue
            
            if task is delete_old_task:
                delete_old_task = None
                continue
             
            # Should not happen
            continue




async def request_channel_thread_channels(client, guild, channel_id, request_function):
    """
    Gets thread channels trough the discord API with the given http client and function.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : `Guild``
        The source guild of the channel.
    channel_id : `int`
        The respective guild text channel's identifier.
    request_function : ``CoroutineFunctionType``
        The function to request the threads with.
    
    Returns
    -------
    thread_channels : `list` of ``ChannelThread``
    
    Raises
    ------
    ConnectionError
        No internet connection.
    DiscordException
        If any exception was received from the Discord API.
    """
    thread_channels = []
    
    data = None
    
    while True:
        data = await request_function(client.http, channel_id, data)
        thread_channel_datas = data['threads']
        
        for thread_channel_data in thread_channel_datas:
            thread_channel = ChannelThread(thread_channel_data, client, guild.id)
            thread_channels.append(thread_channel)
        
        thread_user_datas = data['members']
        for thread_user_data in thread_user_datas:
            thread_chanel_id = int(thread_user_data['id'])
            try:
                thread_channel = CHANNELS[thread_chanel_id]
            except KeyError:
                continue
    
            user_id = int(thread_user_data['user_id'])
            user = create_partial_user_from_id(user_id)
            
            thread_user_create(thread_channel, user, thread_user_data)
        
        if not data.get('has_more', True):
            break
        
        if thread_channels:
            before = thread_channels[-1].created_at
        else:
            before = datetime.utcnow()
        
        data = {'before': before}
    
    return thread_channels


class ForceUpdateCache:
    """
    Cache for static `force_update` endpoints.
    
    Attributes
    ----------
    synced : `bool`
        Whether the cache was synced already.
    value : `Any`
        The cached value.
    """
    __slots__ = ('synced', 'value')
    
    def __new__(cls):
        """
        Creates a new ``ForceUpdateCache`` instance.
        """
        self = object.__new__(cls)
        self.synced = False
        self.value = None
        return self
    
    def __repr__(self):
        """Returns the cache's representation."""
        repr_parts = ['<', self.__class__.__name__]
        if self.synced:
            repr_parts.append(' value=')
            repr_parts.append(repr(self.value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def set(self, value):
        """
        Sets value to the cache and marks it as synced.
        
        Parameters
        ----------
        value : `Any`
            The cached value.
        """
        self.value = value
        self.synced = True


def channel_move_sort_key(channel_key):
    """
    Channel move sort key sued at `Client.channel_move`.
    
    Parameters
    ----------
    channel_key : `tuple` of (`int`, `int`, `int`, (`None` or `list` of `...`))
    
        Channel sort keys have the following structure:
        - channel order group
        - position
        - channel identifier
        - sub channel key
    
    Returns
    -------
    order_group : `int`
    """
    return channel_key[0]


def role_move_key(role, position):
    """
    Used at ``Client.role_move`` and ``Client.role_reorder`` to create a json serializible change key from the given
    `role` and `position`.
    
    Parameters
    ----------
    role : ``Role``
        Respective role.
    position : `int`
        The role's new position.
    
    Returns
    -------
    change_key : `dict` of (`str`, `int`)
    """
    return {
        'id': role.id,
        'position': position,
    }


def role_reorder_valid_roles_sort_key(item):
    """
    Kes used inside of ``Client.role_reorder`` to sort out roles based on their position.
    
    Parameters
    ----------
    item : `tuple` of (``Role``, `int`)
        
        The item contains the following elements:
        - role
        - position
    """
    return item[1]


def application_command_autocomplete_choice_parser(choices):
    """
    Tries to build application command autocomplete choices from the given `choices`.
    
    Parameters
    ----------
    choices : `None` or `iterable` of (`str`, `int`, `float`)
        Application command autocomplete choices to parse.
    
    Returns
    -------
    choices_processed : `list` of `dict` of (`str`, `str`)
        Json serializable application command autocomplete choices.
    
    Raises
    ------
    TypeError
        - If `choices` is neither `None`, `tuple`, `list`, `set` ,`dict` nor other `iterable`.
        - If a choice is neither `str`, `int`, `float` nor a `name` - `value` pair.
    """
    choices_processed = []
    
    if choices is None:
        pass
    
    elif isinstance(choices, (list, tuple)):
        for choice in choices:
            choices_processed.append(application_command_autocomplete_choice_validator(choice))
    
    elif isinstance(choices, set):
        for choice in choices:
            choices_processed.append(application_command_autocomplete_choice_validator(choice))
        
        choices_processed.sort(key=application_command_autocomplete_choice_sort_key)
    
    elif isinstance(choices, dict):
        for choice_item in choices.items():
            choices_processed.append(application_command_autocomplete_choice_validator_tuple_item(choice_item))
        
        choices_processed.sort(key=application_command_autocomplete_choice_sort_key)
    
    elif hasattr(type(choices), '__iter__'):
        for choice in choices:
            choices_processed.append(application_command_autocomplete_choice_validator(choice))
        
        # Should we sort it?
    
    else:
        raise TypeError(f'`{choices}` can be either `None` or `list`, `tuple`, `set`, `dict` including any other '
            f'iterables, got {choices.__class__.__name__}; {choices!r}.')
    
    del choices_processed[20:]
    
    return choices_processed


def application_command_autocomplete_choice_validator(choice):
    """
    Validates an application autocomplete choice given as a tuple item of 2 elements.
    
    Parameters
    ----------
    choice : `str`, `int`, `float`, `tuple` (`str`, (`str`, `int`, `float`))
        The choice or a `name` - `value` pair.
    
    Returns
    -------
    choice : `dict` of (`str`, `str`)
        Json serializable application command autocomplete choice.
    
    Raises
    ------
    TypeError
        If `choice`'s type is incorrect.
    """
    if isinstance(choice, tuple):
        choice_tuple_length = len(choice)
        if choice_tuple_length == 2:
            return application_command_autocomplete_choice_validator_tuple_item(choice)
        
        raise TypeError(f'Tuple autocomplete choice can have length `2`, got {choice_tuple_length}; {choice!r}.')
    
    if isinstance(choice, str):
        pass
    elif isinstance(choice, (int, float)):
        choice = str(choice)
    else:
        raise TypeError(f'An autocomplete choice can be either a `name` - `value` pair or a `str`, `int` or a `float` '
            f'instance, got {choice.__class__.__name__}; {choice!r}.')
    
    return application_command_autocomplete_choice_builder(choice, choice)


def application_command_autocomplete_choice_validator_tuple_item(item):
    """
    Validates an application autocomplete choice given as a tuple item of 2 elements.
    
    Parameters
    ----------
    item : `tuple` (`str`, (`str`, `int`, `float`))
        A `name` - `value` pair.
    
    Returns
    -------
    choice : `dict` of (`str`, `str`)
        Json serializable application command autocomplete choice.
    
    Raises
    ------
    TypeError
        - If `item[0]` is not `str` instance.
        - If `item[1]` is neither `str`, `int` nor `float` instance.
    """
    name, value = item
    if not isinstance(name, str):
        raise TypeError(f'Tuple item autocomplete choice name should be `str` instance, got '
            f'{name.__class__.__name__}; {name!r}.')
    
    if isinstance(value, str):
        pass
    elif isinstance(value, (int, float)):
        value = str(value)
    else:
        raise TypeError(f'Tuple item autocomplete choice value should be either `str`, `int` or `float` instance, got '
            f'{value.__class__.__name__}, {value!r}.')
    
    return application_command_autocomplete_choice_builder(name, value)


def application_command_autocomplete_choice_builder(name, value):
    """
    Builds an application autocomplete choice from the given `name` - `value` pair.
    
    Parameters
    ----------
    name : `str`
        Choice name.
    value : `str`, `int` or `float`
        Choice value.
    
    Returns
    -------
    choice : `dict` of (`str`, `str`)
        Json serializable application command autocomplete choice.
    """
    return {
        'name': name,
        'value': value,
    }


def application_command_autocomplete_choice_sort_key(choice):
    """
    Choice sort key used to sort unsorted application command autocomplete keys.
    
    Parameters
    ----------
    choice : `dict` of (`str`, `str`)
        Json serializable application command autocomplete choice.
    
    Returns
    -------
    choice_sort_key : `str`
        The choice's name.
    """
    return choice['name']
