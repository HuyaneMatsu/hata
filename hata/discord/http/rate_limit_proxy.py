__all__ = ('RateLimitProxy', )

from threading import current_thread

from ...backend.export import include
from ...backend.utils import WeakReferer
from ...backend.futures import Future
from ...backend.event_loop import LOOP_TIME

from .rate_limit import RateLimitGroup, LIMITER_GLOBAL, LIMITER_UNLIMITED, LIMITER_CHANNEL, LIMITER_WEBHOOK, \
    LIMITER_INTERACTION, LIMITER_GUILD, RateLimitHandler, UNLIMITED_SIZE_VALUE

ChannelBase = include('ChannelBase')
ChannelGuildBase = include('ChannelGuildBase')
Message = include('Message')
Role = include('Role')
Webhook = include('Webhook')
WebhookRepr = include('WebhookRepr')
Guild = include('Guild')
InteractionEvent = include('InteractionEvent')


class RateLimitProxy:
    """
    A proxy towards a rate limit.
    
    Attributes
    ----------
    _handler : None` or (`WeakReferer` to ``RateLimitHandler``)
        Reference to the actual rate limit handler of the `client` with the specified `group` and `limiter`.
    _key : ``RateLimitHandler``
        RateLimit handler used to lookup the active one.
    client : ``Client``
        Who's rate limits will be looked up.
    group : ``RateLimitGroup``
        The proxy's rate limit group to pull additional information.
    """
    __slots__ = ('_handler', '_key', 'client', 'group',)
    def __new__(cls, client, group, limiter=None, keep_alive=False):
        """
        Creates a new rate limit proxy.
        
        Parameters
        ----------
        client : ``Client``
            Who's rate limits will be looked up.
        group : ``RateLimitGroup``
            The proxy's rate limit group to pull additional information.
        limiter : ``DiscordEntity`` instance, Optional
            What's rate limits will be looked up.
            
            The accepted types depend on the group's limiter:
            +-----------------------+-----------------------------------------------------------------------+
            | Respective limiter    |   Accepted values                                                     |
            +=======================+=======================================================================+
            | LIMITER_CHANNEL       | ``ChannelBase``, ``Message``                                          |
            +-----------------------+-----------------------------------------------------------------------+
            | LIMITER_GUILD         | ``Guild``, ``ChannelGuildBase``, ``Message``, ``Role``, ``Webhook``,  |
            |                       | ``WebhookRepr``                                                       |
            +-----------------------+-----------------------------------------------------------------------+
            | LIMITER_WEBHOOK       | ``Webhook``, ``WebhookRepr``                                          |
            +-----------------------+-----------------------------------------------------------------------+
            | LIMITER_INTERACTION   | ``InteractionEvent``                                                  |
            +-----------------------+-----------------------------------------------------------------------+
            | LIMITER_GLOBAL        | `Any`                                                                 |
            +-----------------------+-----------------------------------------------------------------------+
            | LIMITER_UNLIMITED     | `Any`                                                                 |
            +-----------------------+-----------------------------------------------------------------------+
            
            Note that at the case of `LIMITER_GUILD` partial objects will yield `.guild` as `None` so `ValueError`
            will still be raised.
        keep_alive : `bool`, Optional
            Whether the rate limit proxy should keep alive the respective rate limit handler. Defaults to `False`.
        
        Raises
        ------
        RuntimeError
            If the given `group`'s limiter is not any of the predefined ones. Note that limiters are compared by memory
            address and not by value.
        TypeError
            If `group` was not given as ``RateLimitGroup`` instance.
        ValueError
            If the given `limiter` cannot be casted to `limiter_id` with the specified `group` .
        """
        if (type(group) is not RateLimitGroup):
            raise TypeError(f'`group` should be type `{RateLimitGroup.__name__}`, got {group}.__class__.__name__.')
        
        while True:
            group_limiter = group.limiter
            if group_limiter is LIMITER_GLOBAL:
                limiter_id = 0
                break
            
            elif group_limiter is LIMITER_UNLIMITED:
                limiter_id = 0
                break
            
            elif group_limiter is LIMITER_CHANNEL:
                if (limiter is not None):
                    if isinstance(limiter, ChannelBase):
                        limiter_id = limiter.id
                        break
                    
                    if isinstance(limiter, Message):
                        limiter_id = limiter.channel_id
                        break
            
            elif group_limiter is LIMITER_GUILD:
                if (limiter is not None):
                    if isinstance(limiter, Guild):
                        limiter_id = limiter.id
                        break
                    
                    if isinstance(limiter, (ChannelGuildBase, Message, Role, Webhook, WebhookRepr)):
                        
                        guild = limiter.guild
                        if (guild is not None):
                            limiter_id = limiter.id
                            break
            
            elif group_limiter is LIMITER_WEBHOOK:
                if (limiter is not None):
                    if isinstance(limiter, (Webhook, WebhookRepr)):
                        limiter_id = limiter.id
                        break
            
            elif group_limiter is LIMITER_INTERACTION:
                if (limiter is not None):
                    if isinstance(limiter, InteractionEvent):
                        limiter_id = limiter.id
                        break
            else:
                raise RuntimeError(f'`{group!r}.limiter` is not any of the defined limit groups.')
            
            raise ValueError(f'Cannot cast rate limit group\'s: `{group!r}` rate limit_id of: `{limiter!r}`.')
        
        key = RateLimitHandler(group, limiter_id)
        
        if keep_alive:
            key = client.http.handlers.set(key)
            handler = WeakReferer(key)
        else:
            handler = None
        
        self = object.__new__(cls)
        self.client = client
        self.group = group
        self._handler = handler
        self._key = key
        return self
    
    def is_limited_by_channel(self):
        """
        Returns whether the represented rate limit group is limited by channel id.
        
        Returns
        -------
        is_limited_by_channel : `bool`
        """
        return (self.group.limiter is LIMITER_CHANNEL)
    
    def is_limited_by_guild(self):
        """
        Returns whether the represented rate limit group is limited by guild id.
        
        Returns
        -------
        is_limited_by_guild : `bool`
        """
        return (self.group.limiter is LIMITER_GUILD)
    
    def is_limited_by_webhook(self):
        """
        Returns whether the represented rate limit group is limited by webhook id.
        
        Returns
        -------
        is_limited_by_webhook : `bool`
        """
        return (self.group.limiter is LIMITER_WEBHOOK)
    
    def is_limited_by_interaction(self):
        """
        Returns whether the represented rate limit group is limited by interaction id.
        
        Returns
        -------
        is_limited_by_interaction : `bool`
        """
        return (self.group.limiter is LIMITER_INTERACTION)
    
    def is_limited_globally(self):
        """
        Returns whether the represented rate limit group is limited globally,
        
        Returns
        -------
        is_limited_globally : `bool`
        """
        return (self.group.limiter is LIMITER_GLOBAL)
    
    def is_unlimited(self):
        """
        Returns whether the represented rate limit group is unlimited,
        
        Returns
        -------
        is_unlimited : `bool`
        """
        return (self.group.limiter is LIMITER_UNLIMITED)
    
    def is_alive(self):
        """
        Returns whether the respective client has the represented rate limit handler is alive.
        
        Returns
        -------
        is_alive : `bool`
        """
        return (self.handler is not None)
    
    def has_info(self):
        """
        Returns whether the represented rate limit handler now stores any rate limit information.
        
        Returns
        -------
        has_info : `bool`
        """
        handler = self.handler
        if handler is None:
            return False
        
        return (handler.queue is not None)
    
    @property
    def keep_alive(self):
        """
        Get-set property for accessing whether the rate limit proxy should keep alive the respective rate limit
        handler.
        
        Accepts and returns `bool`.
        """
        handler = self._handler
        if handler is None:
            return False
        
        return (handler() is self._key)
    
    @keep_alive.setter
    def keep_alive(self, value):
        if value:
            while True:
                handler = self._handler
                if handler is None:
                    break
                
                handler = handler()
                if handler is None:
                    break
                
                if (self._key is not handler):
                    self._key = handler
                
                return
            
            key = self._key
            handler = self.client.http.handlers.set(key)
            if (handler is not key):
                self._key = handler
            self._handler = WeakReferer(handler)
            return
        else:
            handler = self._handler
            if handler is None:
                return
            
            handler = handler()
            if handler is None:
                return
            
            if self._key is handler:
                self._key = handler.copy()
            return
    
    @property
    def limiter_id(self):
        """
        Returns the the represented rate limit handler's `.limiter_id`.
        
        Returns
        -------
        limiter_id : `int`
        """
        return self._key.limiter_id
    
    def has_size_set(self):
        """
        Returns whether the represented rate limit group size is already set.
        
        Not only not used rate limit groups, but still optimistic or unlimited rate limit groups fall under this
        category as well.
        
        Returns
        -------
        has_size_set : `bool`
        """
        return (self.group.size > 0)
    
    @property
    def size(self):
        """
        Returns the represented rate limit group's size.
        
        Returns
        -------
        size : `int`
        """
        return self.group.size
    
    @property
    def handler(self):
        """
        Returns the client's represented active handler if applicable.
        
        Returns
        -------
        handler : `None` or ``RateLimitHandler``
        """
        handler = self._handler
        if (handler is not None):
            handler = handler()
            if (handler is not None):
                return handler
        
        handler = self.client.http.handlers.get(self._key)
        if (handler is not None):
            self._handler = WeakReferer(handler)
        
        return handler
    
    @property
    def used_count(self):
        """
        Returns how much requests are used up or already done right now.
        
        Returns
        -------
        count : `int`
        """
        handler = self.handler
        if handler is None:
            return 0
        
        return (handler.active + handler.count_drops())
    
    @property
    def free_count(self):
        """
        Returns how much requests can be done towards the represented rate limit.
        
        If the rate limit proxy represents an unlimited endpoint, then `0` is returned.
        
        Returns
        -------
        free_count : `int`
        """
        size = self.group.size
        if size < 1:
            if size == 0:
                size = 1
            elif size == UNLIMITED_SIZE_VALUE:
                return 0
            else:
                size = -size
        
        handler = self.handler
        if handler is None:
            return size
        
        return (size - handler.active - handler.count_drops())
    
    @property
    def waiting_count(self):
        """
        Returns how much requests are waiting in queue by the represented rate limit.
        
        Returns
        -------
        count : `int`
        """
        handler = self.handler
        if handler is None:
            return 0
        
        queue = handler.queue
        if queue is None:
            return 0
        
        return len(queue)
    
    def __hash__(self):
        """Hashes the rate limit proxy."""
        return self.group.group_id^self._key.limiter_id
    
    class _wait_till_limits_expire_callback:
        """
        `WeakReferer` callback used at ``.wait_till_limits_expire`` for waking it up.
        """
        __slots__ = ('future')
        def __init__(self, future):
            self.future = future
        
        def __call__(self, reference):
            future = self.future
            future.set_result_if_pending(None)
            loop = future._loop
            if current_thread() is not loop:
                loop.wake_up()
    
    async def wait_till_limits_expire(self):
        """
        Waits till the represented rate limits expire.
        
        This method is a coroutine.
        
        Raises
        ------
        RuntimeError
            If the method is called meanwhile `keep_alive` is `True`.
        
        Notes
        -----
        The waiting is implemented with weakreference callback, so the coroutine returns when the source callback is
        garbage collected. This also means waiting on the exact same limit multiple times causes misbehaviour.
        """
        handler = self._handler
        
        while True:
            if (handler is not None):
                handler = handler()
                if (handler is not None):
                    break
            
            handler = self.client.http.handlers.get(self._key)
            if handler is None:
                return
            
            break
        
        if handler is self._key:
            raise RuntimeError('Cannot use `.wait_till_limits_expire` meanwhile `keep_alive` is `True`.')
        
        future = Future(current_thread())
        self._handler = WeakReferer(handler, self._wait_till_limits_expire_callback(future))
        await future
    
    @property
    def next_reset_at(self):
        """
        Returns when the next rate limit reset will happen of the represented rate limit handler.
        
        If there is no active rate limit handler represented or if the handler has has 0 used up limits, then returns
        `0.0`. if there is any, then returns it in `LOOP_TIME` time.
        
        Returns
        -------
        next_reset_at : `float`
        """
        handler = self.handler
        if handler is None:
            return 0.0
        
        drops = handler.drops
        if (drops is None) or (not drops):
            return 0.0
        
        return drops[0].drop
    
    @property
    def next_reset_after(self):
        """
        Familiar to ``.next_reset_at`` but it instead returns how time is left till next reset instead.
        
        Returns
        -------
        next_reset_after : `float`
        """
        handler = self.handler
        if handler is None:
            return 0.0
        
        drops = handler.drops
        if (drops is None) or (not drops):
            return 0.0
        
        return drops[0].drop-LOOP_TIME()
