# -*- coding: utf-8 -*-
__all__ = ('RATE_LIMIT_GROUPS', 'RateLimitProxy', )

from email._parseaddr import _parsedate_tz as parse_date_timezone
from datetime import datetime, timedelta, timezone
from collections import deque
from threading import current_thread

from ..backend.utils import modulize, WeakReferer, DOCS_ENABLED
from ..backend.futures import Future, ScarletLock
from ..backend.headers import DATE
from ..backend.event_loop import LOOP_TIME

from .client_core import KOKORO
from .utils.DISCORD_HEADERS import RATE_LIMIT_RESET, RATE_LIMIT_RESET_AFTER, RATE_LIMIT_REMAINING, RATE_LIMIT_LIMIT

ChannelBase      = NotImplemented
ChannelGuildBase = NotImplemented
Message          = NotImplemented
Role             = NotImplemented
Webhook          = NotImplemented
WebhookRepr      = NotImplemented
Guild            = NotImplemented
InteractionEvent = NotImplemented

#parsing time
#email.utils.parse_date_to_datetime
def parse_date_to_datetime(data):
    """
    Parsers header date to `datetime`.
    
    Parameters
    ----------
    data : ``imultidict``

    Returns
    -------
    date : `datetime`
    """
    *date_tuple, tz = parse_date_timezone(data)
    if tz is None:
        date = datetime(*date_tuple[:6])
    else:
        date = datetime(*date_tuple[:6], tzinfo=timezone(timedelta(seconds=tz)))
    return date

class global_lock_canceller:
    """
    Cancels the global lock on a discord http session by setting it as `None` causing all the new requests to not be
    globally locked.
    
    The already waiting requests are free'd up by the source `8Future``, what's callback this is.
    
    Attributes
    ----------
    session : ``DiscordHTTPClient``
        The globally locked http session.
    """
    __slots__ = ('session',)
    def __init__(self, session):
        """
        Creates a new global lock canceller.
        
        Parameters
        ----------
        session : ``DiscordHTTPClient``
            The globally locked http session.
        """
        self.session = session
    
    def __call__(self, future):
        """
        Cancels the global lock of the respective discord http session by setting it as `None`.
        
        Parameters
        ----------
        future : ``Future``
            The global locker of the session.
        """
        self.session.global_lock = None

def rate_limit_global(session, retry_after):
    """
    Applies global lock on the given session.
    
    If the session is already globally locked, return it's waiter future.
    
    Parameters
    ----------
    session : ``DiscordHTTPClient``
        The session to be globally locked.
    retry_after : `float`
        The time for what the session is locked for.
    
    Returns
    -------
    future : ``Future``
        Waiter future till the global lock is over.
    """
    future = session.global_lock
    if (future is None):
        future = Future(KOKORO)
        future.add_done_callback(global_lock_canceller(session))
        session.global_lock = future
        KOKORO.call_later(retry_after, Future.set_result_if_pending, future, None)
    
    return future

GLOBALLY_LIMITED = 0x4000000000000000
RATE_LIMIT_DROP_ROUND = 0.20
MAXIMAL_UNLIMITED_PARARELLITY = -50
UNLIMITED_SIZE_VALUE = -10000
NO_SPECIFIC_RATE_LIMITER = 0

LIMITER_CHANNEL     = 'channel_id'
LIMITER_GUILD       = 'guild_id'
LIMITER_WEBHOOK     = 'webhook_id'
LIMITER_INTERACTION = 'interaction_id'
LIMITER_GLOBAL      = 'global'
LIMITER_UNLIMITED   = 'unlimited'

class RateLimitGroup(object):
    """
    Represents a rate limit group of one endpoint or of more endpoints sharing the same one.
    
    Attributes
    ----------
    group_id : `int`
        The rate limit group's group id is like it's identifier number, what makes each rate limit group unique.
    limiter : `str`
        identifier name by what is the rate limit group limited.
        
        Possible values:
        +-----------------------+-----------------------+
        | Respective name       | Value                 |
        +=======================+=======================+
        | LIMITER_CHANNEL       | `'channel_id'`        |
        +-----------------------+-----------------------+
        | LIMITER_GUILD         | `'guild_id'`          |
        +-----------------------+-----------------------+
        | LIMITER_WEBHOOK       | `'webhook_id'`        |
        +-----------------------+-----------------------+
        | LIMITER_INTERACTION   | `'interaction_id'`    |
        +-----------------------+-----------------------+
        | LIMITER_GLOBAL        | `'global'`            |
        +-----------------------+-----------------------+
        | LIMITER_UNLIMITED     | `'unlimited'`         |
        +-----------------------+-----------------------+
    
    size : `int`
        The maximal amount of requests, which can be executed per limiter till the respective rate limit reset.
        
        Set as `0` by default, what indicates, that the size of the group is not known yet. At this case the
        rate limits are adjusted by the first request's response.
        
        Can be set as a negative number as well if the rate limits are optimistic, so the rate limit group is not
        limited yet, but this behaviour might change at the future. If a request is done through an optimistic
        rate limit group and no rate limit information is received then the rate limit size is decreased, increasing
        the possible active requests, up to `MAXIMAL_UNLIMITED_PARARELLITY`'s value what is -50 by default. However
        if rate limit information is received, then the size of the group is corrected to positive. Note that the size
        is decreased only by `1` each time, because Discord might not send rate limit information even tho, an endpoint
        is limited.
    """
    __slots__ = ('group_id', 'limiter', 'size', )
    
    __auto_next_id = 105<<8
    __unlimited = None
    
    @classmethod
    def generate_next_id(cls):
        """
        Generates the next auto id of a rate limit group and returns it.
        
        Returns
        -------
        group_id : `int`
        """
        group_id = cls.__auto_next_id
        cls.__auto_next_id = group_id+(7<<8)
        return group_id
    
    def __new__(cls, limiter=LIMITER_GLOBAL, optimistic=False):
        """
        Creates a new rate limit group.
        
        Parameters
        ----------
        limiter : `str`, Optional
            Identifier name by what is the rate limit group limited. Defaults to `LIMITER_GLOBAL`.
            
            Possible values:
            +-----------------------+-----------------------+
            | Respective name       | Value                 |
            +=======================+=======================+
            | LIMITER_CHANNEL       | `'channel_id'`        |
            +-----------------------+-----------------------+
            | LIMITER_GUILD         | `'guild_id'`          |
            +-----------------------+-----------------------+
            | LIMITER_WEBHOOK       | `'webhook_id'`        |
            +-----------------------+-----------------------+
            | LIMITER_INTERACTION   | `'interaction_id'`    |
            +-----------------------+-----------------------+
            | LIMITER_GLOBAL        | `'global'`            |
            +-----------------------+-----------------------+
            | LIMITER_UNLIMITED     | `'unlimited'`         |
            +-----------------------+-----------------------+
        
        optimistic : `bool`, Optional
            Whether the rate limit group is optimistic.
        """
        self = object.__new__(cls)
        self.limiter = limiter
        self.size = (-1 if optimistic else 0)
        self.group_id = cls.generate_next_id()
        return self
    
    @classmethod
    def unlimited(cls):
        """
        Creates a not limited rate limit group.
        
        Uses ``.__unlimited`` to cache this instance, because it is enough to have only 1 unlimited one.
        
        Returns
        -------
        self : ``RateLimitGroup``
        """
        self = cls.__unlimited
        if (self is not None):
            return self
        
        self = object.__new__(cls)
        self.size = UNLIMITED_SIZE_VALUE
        self.group_id = 0
        self.limiter = LIMITER_UNLIMITED
        
        cls.__unlimited = self
        return self
    
    def __hash__(self):
        """Hash of a rate limit group equals to it's group_id."""
        return self.group_id
    
    def __repr__(self):
        """Returns the representation of the rate limit group."""
        result = [
            '<',
            self.__class__.__name__,
            ' size=',
            repr(self.size),
            ', ',
                ]
        
        limiter = self.limiter
        if limiter is LIMITER_GLOBAL:
            result.append('limited globally')
        elif limiter is LIMITER_UNLIMITED:
            result.append('unlimited')
        else:
            result.append('limited by ')
            result.append(limiter)
        
        result.append('>')
        
        return ''.join(result)

class RateLimitUnit(object):
    """
    Represents a chained rate limit unit storing how much request is already done till the next reset, what is
    also stored by it.
    
    Attributes
    ----------
    allocates : `int`
        The amount of done requests till next rate limit reset.
    drop : `float`
        The time of the next rate limit reset in LOOP_TIME time.
    next : `None` or ``RateLimitUnit``
        The next rate limit unit on the chain. It can happen that requests are done between two reset and we would need
        to store multiple rate limit units and using a chain is still better than allocating a list every time.
    """
    __slots__ = ('allocates', 'drop', 'next')
    
    def __init__(self, drop, allocates):
        """
        Creates a new rate limit unit.
        
        Parameters
        ----------
        allocates : `int`
            The amount of done requests till next rate limit reset.
        drop : `float`
            The time of the next rate limit reset in LOOP_TIME time.
        """
        self.drop = drop
        self.allocates = allocates
        self.next = None
    
    def update_with(self, drop, allocates):
        """
        Updates the rate limit unit with the given `drop` and `allocates` information.
        
        If the given `drop` is within `RATE_LIMIT_DROP_ROUND` (so 0.20s by default), then the two drop and allocate will
        be merged, using the earlier `drop` value and summing the two `allocates`.
        
        Parameters
        ----------
        allocates : `int`
            The amount of done requests till next rate limit reset.
        drop : `float`
            The time of the next rate limit reset in LOOP_TIME time.
        """
        actual_drop = self.drop
        new_drop_max = drop+RATE_LIMIT_DROP_ROUND
        if new_drop_max < actual_drop:
            new = object.__new__(type(self))
            new.drop = self.drop
            new.allocates = self.allocates
            new.next = self.next
            self.drop = drop
            self.allocates = allocates
            self.next = new
            return
        
        new_drop_min = drop-RATE_LIMIT_DROP_ROUND
        if new_drop_min > actual_drop:
            last = self
            while True:
                actual = last.next
                if actual is None:
                    new = object.__new__(type(self))
                    new.drop = drop
                    new.allocates = allocates
                    new.next = None
                    last.next = new
                    break
                
                actual_drop = actual.drop
                if new_drop_max < actual_drop:
                    new = object.__new__(type(self))
                    new.drop = drop
                    new.allocates = allocates
                    new.next = actual
                    last.next = new
                    break
                
                if new_drop_min > actual_drop:
                    last = actual
                    continue
                
                if drop < actual_drop:
                    actual.drop = drop
                
                actual.allocates += allocates
                break
            
            return
            
        if drop < actual_drop:
            self.drop = drop
        
        self.allocates += allocates
        return
        
    def __repr__(self):
        """Returns the representation of the rate limit unit."""
        result = [
            '<',
            self.__class__.__name__,
            ' drop=',
            repr(self.drop),
            ', allocates=',
            repr(self.allocates),
                ]
        
        next_ = self.next
        if (next_ is not None):
            result.append(', next=[')
            while True:
                result.append('(')
                result.append(repr(next_.drop))
                result.append(', ')
                result.append(repr(next_.allocates))
                result.append(')')
                next_ = next_.next
                if (next_ is None):
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)

class RateLimitHandler(object):
    """
    Handles a request's rate limit.
    
    Attributes
    ----------
    active : `int`
        The amount of active requests with the same `limiter_id` and with the same `parent`.
    drops : `None` or `RateLimitUnit`
        The already used up rate limits.
    limiter_id : `int`
        The `id` of the Discord Entity based on what the handler is limiter.
    parent : ``RateLimitGroup``
        The rate limit group of the rate limit handler.
    queue : `None` or (`deque` of ``Future``)
        Queue of ``Future`` objects of waiting requests.
    wake_upper : `None` or `TimerHandle`
        Wake ups the rate limit handler, when it's rate limits are reset.
    
    Notes
    -----
    ``RateLimitHandler`` supports weakreferencing for garbage collecting purposing.
    """
    __slots__ = ('__weakref__', 'active', 'drops', 'limiter_id', 'parent', 'queue', 'wake_upper', )
    def __new__(cls, parent, limiter_id):
        """
        Creates a new rate limit handler.
        
        New rate limit handlers have `.queue` set to `None` not because it does not need `.queue` attribute, like the
        `.drops` or `.wake_upper` one, but because this rate limit handler might be used just to look up an already
        existing one with the same `.limiter_id` and `.parent`, so creating an another `deque` and then collecting it
        would be just waste of resources.
        
        Parameters
        ----------
        parent : ``RateLimitGroup``
            The rate limit group of the rate limit handler.
        limiter_id : `int`
            The `id` of the Discord Entity based on what the handler is limiter.
        """
        self = object.__new__(cls)
        self.parent = parent
        
        limiter = parent.limiter
        if limiter is LIMITER_UNLIMITED:
            limiter_id = 0
        elif limiter is LIMITER_GLOBAL:
            limiter_id = GLOBALLY_LIMITED
        
        self.limiter_id = limiter_id
        self.drops = None
        self.active = 0
        self.queue = None
        self.wake_upper = None
        
        return self
    
    def copy(self):
        """
        Copies the rate limit handler. Only the `.parent` and the `.limiter_id` attributes are copied, because those
        are enough to describe it and will not cause misbehaviour.
        
        Returns
        -------
        new : ``RateLimitHandler``
        """
        new = object.__new__(type(self))
        new.parent = self.parent
        new.limiter_id  = self.limiter_id
        new.drops = None
        new.active = 0
        new.queue = None
        new.wake_upper = None
        return new
    
    def __repr__(self):
        """Returns the representation of the rate limit handler."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        limiter = self.parent.limiter
        if limiter is LIMITER_UNLIMITED:
            result.append(' unlimited')
        else:
            result.append(' size: ')
            size = self.parent.size
            if size == -1:
                result.append('unset')
            else:
                result.append(repr(size))
            
            result.append(', active: ')
            result.append(repr(self.active))
            
            result.append(', cooldown drops: ')
            result.append(repr(self.drops))
            
            result.append(', queue length: ')
            queue = self.queue
            if queue is None:
                length = '0'
            else:
                length = repr(len(self.queue))
            result.append(length)
            
            if limiter is LIMITER_GLOBAL:
                result.append(', limited globally')
            else:
                result.append(', limited by ')
                result.append(limiter)
                result.append(': ')
                result.append(repr(self.limiter_id))
            
            result.append(', group id: ')
            result.append(repr(self.parent.group_id))
            
        result.append('>')
        return ''.join(result)
    
    def __bool__(self):
        """Returns whether the rate limit handler is active."""
        if self.active:
            return True
        
        if (self.drops is not None):
            return True
        
        queue = self.queue
        if (queue is not None) and queue:
            return True
        
        return False
    
    def __eq__(self, other):
        """Returns whether the two rate limit handler has the same `.limiter_id` and `.parent`."""
        if self.limiter_id != other.limiter_id:
            return False
        
        if self.parent.group_id != other.parent.group_id:
            return False
        
        return True
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different `.limiter_id` or `.parent`."""
        if self.limiter_id != other.limiter_id:
            return True
        
        if self.parent.group_id != other.parent.group_id:
            return True
        
        return False
    
    def __hash__(self):
        """Hashes the rate limit handler."""
        return self.parent.group_id+self.limiter_id
    
    def is_unlimited(self):
        """
        Returns whether the rate limit handler is unlimited.
        
        is_unlimited : `bool` = `False`
            Stacked rate limit handlers are always limited.
        """
        if self.parent.group_id:
            return False
        
        return True
    
    async def enter(self):
        """
        Waits till a respective request can be started.
        
        Should be called before the rate limit handler is used inside of it's context manager.
        
        This method is a coroutine.
        """
        size = self.parent.size
        if size < 1:
            if size == UNLIMITED_SIZE_VALUE:
                return
            
            if size == 0:
                size = 1
            else:
                size = -size
        
        queue = self.queue
        if queue is None:
            self.queue = queue = deque()
        
        active = self.active
        left = size-active
        
        if left <= 0:
            future = Future(KOKORO)
            queue.append(future)
            await future
            
            self.active += 1
            return
        
        left -= self.count_drops()
        if left > 0:
            self.active = active+1
            return
        
        future = Future(KOKORO)
        queue.append(future)
        await future
        
        self.active += 1
    
    def exit(self, headers):
        """
        Called by the rate limit handler's context manager (``RateLimitHandlerCTX``) when a respective request is done.
        
        Calculates the rate limits based on the given `headers`. Handles first request, optimistic rate limit handling
        and changed rate limit sizes as well.
        
        Parameters
        ----------
        headers : `None` or `imultidict` of (`str`, `str) items
            Response headers
        """
        current_size = self.parent.size
        if current_size == UNLIMITED_SIZE_VALUE:
            return
        
        self.active -= 1
        
        optimistic = False
        while True:
            if (headers is not None):
                size = headers.get(RATE_LIMIT_LIMIT,None)
                if size is None:
                    if current_size < 0:
                        optimistic = True
                        # A not so special case when the endpoint is not rate limit yet.
                        # If this happens, we increase the maximal size.
                        size = current_size
                        if size > MAXIMAL_UNLIMITED_PARARELLITY:
                            size -= 1
                        
                        break
                else:
                    size = int(size)
                    break
            
            wake_upper = self.wake_upper
            if (wake_upper is not None):
                wake_upper.cancel()
                self.wake_upper = None
            
            self.wake_up()
            return
        
        allocates = 1
        
        if size != current_size:
            self.parent.size = size
            
            if optimistic:
                current_size = -current_size
                size = -size
            
            if size > current_size:
                if current_size == -1:
                    current_size = 1
                    # We might have cooldowns from before as well
                    allocates = size-int(headers[RATE_LIMIT_REMAINING])
                
                can_free = size-current_size
                queue = self.queue
                queue_ln = len(queue)
                
                if can_free > queue_ln:
                    can_free = queue_ln
                
                while can_free > 0:
                    future = queue.popleft()
                    future.set_result(None)
                    can_free -=1
                    continue
        
        if optimistic:
            delay = 1.0
        else:
            delay1 = (
                datetime.fromtimestamp(
                    float(headers[RATE_LIMIT_RESET]), timezone.utc) - parse_date_to_datetime(headers[DATE])
                        ).total_seconds()
            delay2 = float(headers[RATE_LIMIT_RESET_AFTER])
            
            if delay1 < delay2:
                delay = delay1
            else:
                delay = delay2
        
        drop = LOOP_TIME()+delay
        
        drops = self.drops
        if (drops is None):
            self.drops = RateLimitUnit(drop, allocates)
        else:
            drops.update_with(drop, allocates)
        
        wake_upper = self.wake_upper
        if wake_upper is None:
            wake_upper = KOKORO.call_at(drop, type(self).wake_up, self)
            self.wake_upper = wake_upper
            return
        
        if wake_upper.when <= drop:
            return
        
        wake_upper.cancel()
        wake_upper = KOKORO.call_at(drop, type(self).wake_up, self)
        self.wake_upper = wake_upper
    
    def wake_up(self):
        """
        Called by `.wake_upper` when the handler's rate limits are dropped.
        
        Checks whether there are waiting requests to start and starts the maximal amount what the rate limits allow.
        If there are still rate limits left, then sets an another wake_upper.
        """
        drops = self.drops
        if (drops is None):
            wake_upper = None
        else:
            self.drops = drops = drops.next
            if (drops is not None):
                wake_upper = KOKORO.call_at(drops.drop, type(self).wake_up, self)
            else:
                wake_upper = None
        
        self.wake_upper = wake_upper
        
        queue = self.queue
        queue_ln = len(queue)
        if queue_ln == 0:
            return
        
        # if exception occurs, nothing is added to self.drops, but active is decreased by one, so lets check active
        # count as well.
        # Also the first requests might set self.parent.size as well, to higher than 1 >.>
        size = self.parent.size
        if size < 0:
            size = -size
        
        can_free = size-self.active-self.count_drops()
        
        if can_free > queue_ln:
            can_free = queue_ln
        
        while can_free > 0:
            future = queue.popleft()
            future.set_result(None)
            can_free -=1
            continue
    
    def ctx(self):
        """
        Context manager for rate limit handler.
        
        Returns
        -------
        ctx : ``RateLimitHandlerCTX``
        """
        return RateLimitHandlerCTX(self)
    
    def count_drops(self):
        """
        Counts how much request is already used up.
        
        Returns
        -------
        result : `int`
        """
        drops = self.drops
        result = 0
        while (drops is not None):
            result += drops.allocates
            drops = drops.next
            continue
        
        return result

class RateLimitHandlerCTX(object):
    """
    Context manager of a ``RateLimitHandler``.
    
    When the ``RateLimitHandlerCTX`` is exited by it's ``.exit`` or by it's ``.__exit__`` for the first time, then
    calls it's parent's ``.exit`` indicate that the request is done.
    
    Attributes
    ----------
    parent : ``RateLimitHandler`` or ``StaticRateLimitHandler``
        The owner rate limit handler.
    exited : `bool`
        Whether the context manager was exited already.
    """
    __slots__ = ('parent', 'exited', )
    def __init__(self, parent):
        """
        Creates a new rate limit handler context manager.
        
        Parameters
        ----------
        parent : ``RateLimitHandler``
            The owner rate limit handler.
        """
        self.parent = parent
        self.exited = False
    
    def exit(self, headers):
        """
        Checks the context manager whether it was already exited and exists's its parent with the given `headers`
        as well.
        
        Parameters
        ----------
        headers : `None` or `imultidict`
            Response headers.
        """
        assert not self.exited, '`RateLimitHandlerCTX.exit` or `StaticRateLimitHandler.exit` was already called.'
        self.exited = True
        self.parent.exit(headers)
    
    def __enter__(self):
        """Enters the context manager returning itself."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exists the context manager and if the context manager was not exited yet, exists it's parent as well."""
        if self.exited:
            return
        
        self.exited = True
        self.parent.exit(None)

class RateLimitProxy(object):
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
                        limiter_id = limiter.channel.id
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
        
    def _get_keep_alive(self):
        handler = self._handler
        if handler is None:
            return False
        
        return (handler() is self._key)
    
    def _set_keep_alive(self, value):
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
        
    keep_alive = property(_get_keep_alive, _set_keep_alive)
    del _get_keep_alive, _set_keep_alive
    
    if DOCS_ENABLED:
        keep_alive.__doc__ = (
        """
        Get-set property for accessing whether the rate limit proxy should keep alive the respective rate limit handler.
        
        Accepts and returns `bool`.
        """)
    
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
    
    class _wait_till_limits_expire_callback(object):
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

class StaticRateLimitGroup(object):
    """
    Represents a static rate limit group of one endpoint or of more endpoints sharing the same one.
    
    Attributes
    ----------
    group_id : `int`
        The rate limit group's group id is like it's identifier number, what makes each rate limit group unique.
    limiter : `str`
        Identifier name by what is the rate limit group limited.
        
        Possible values:
        +-------------------+-------------------+
        | Respective name   | Value             |
        +===================+===================+
        | LIMITER_CHANNEL   | `'channel_id'`    |
        +-------------------+-------------------+
        | LIMITER_GUILD     | `'guild_id'`      |
        +-------------------+-------------------+
        | LIMITER_WEBHOOK   | `'webhook_id'`    |
        +-------------------+-------------------+
        | LIMITER_GLOBAL    | `'global'`        |
        +-------------------+-------------------+
        | LIMITER_UNLIMITED | `'unlimited'`     |
        +-------------------+-------------------+
    
    size : `int`
        The maximal amount of requests, which can be executed parallelly.
    timeout : `float`
        The timeout till the rate limits reset.
    """
    __slots__ = ('group_id', 'limiter', 'size', 'timeout')
    def __new__(cls, size, timeout, limiter=LIMITER_GLOBAL):
        """
        Creates a new rate limit group.
        
        Parameters
        ----------
        size : `int`
            The maximal amount of requests, which can be executed parallelly.
        timeout : `float`
            The timeout till the rate limits reset.
        limiter : `str`, Optional
            Identifier name by what is the rate limit group limited. Defaults to `LIMITER_GLOBAL`.
            
            Possible values:
            +-------------------+-------------------+
            | Respective name   | Value             |
            +===================+===================+
            | LIMITER_CHANNEL   | `'channel_id'`    |
            +-------------------+-------------------+
            | LIMITER_GUILD     | `'guild_id'`      |
            +-------------------+-------------------+
            | LIMITER_WEBHOOK   | `'webhook_id'`    |
            +-------------------+-------------------+
            | LIMITER_GLOBAL    | `'global'`        |
            +-------------------+-------------------+
            | LIMITER_UNLIMITED | `'unlimited'`     |
            +-------------------+-------------------+
        """
        self = object.__new__(cls)
        self.limiter = limiter
        self.size = size
        self.timeout = timeout
        self.group_id = RateLimitGroup.generate_next_id()
        
        return self
    
    def __hash__(self):
        """Hash of a rate limit group equals to it's group_id."""
        return self.group_id
    
    def __repr__(self):
        """Returns the representation of the rate limit group."""
        result = [
            '<',
            self.__class__.__name__,
            ' size=',
            repr(self.size),
            ', timeout=',
            repr(self.timeout),
            ', ',
                ]
        
        limiter = self.limiter
        if limiter is LIMITER_GLOBAL:
            result.append('limited globally')
        elif limiter is LIMITER_UNLIMITED:
            result.append('unlimited')
        else:
            result.append('limited by ')
            result.append(limiter)
        
        result.append('>')
        
        return ''.join(result)


class StaticRateLimitHandler(object):
    """
    Static rate limit handler to defend the wrapper from stupidity.
    
    Attributes
    ----------
    limiter_id : `int`
        The `id` of the Discord Entity based on what the handler is limiter.
    parent : ``RateLimitGroup``
        The rate limit group of the rate limit handler.
    lock : `None` or ``ScarletLock``
        Lock used to await entries and then lock them till they expire.
    
    Notes
    -----
    Static rate limit handlers are weakreferencable.
    """
    __slots__ = ('__weakref__', 'limiter_id', 'parent', 'lock')
    def __new__(cls, parent, limiter_id):
        """
        Creates a new static rate limiter instance.
        
        Parameters
        ----------
        parent : ``StaticRateLimitGroup``
            The static rate limit group.
        limiter_id : `int`
            The `id` of the Discord Entity based on what the handler is limiter.
        """
        self = object.__new__(cls)
        self.parent = parent

        limiter = parent.limiter
        if limiter is LIMITER_UNLIMITED:
            limiter_id = 0
        elif limiter is LIMITER_GLOBAL:
            limiter_id = GLOBALLY_LIMITED
        
        self.limiter_id = limiter_id
        self.lock = None
        
        return self
    
    def __repr__(self):
        """Returns the rate limit handler's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        limiter = self.parent.limiter
        if limiter is LIMITER_UNLIMITED:
            result.append(' unlimited')
        else:
            parent = self.parent
            result.append(' size: ')
            result.append(repr(parent.size))
            result.append(' timeout: ')
            result.append(repr(parent.timeout))
            
            result.append(', queue length: ')
            lock = self.lock
            if lock is None:
                length = '0'
            else:
                length = repr(lock.get_waiting())
            result.append(length)
            
            if limiter is LIMITER_GLOBAL:
                result.append(', limited globally')
            else:
                result.append(', limited by ')
                result.append(limiter)
                result.append(': ')
                result.append(repr(self.limiter_id))
            
            result.append(', group id: ')
            result.append(repr(self.parent.group_id))
            
        result.append('>')
        return ''.join(result)
    
    def __bool__(self):
        """Returns whether the rate limit handler is active."""
        lock = self.lock
        if lock is None:
            return False
        
        if lock.get_acquired():
            return True
        
        return False
    
    def __eq__(self, other):
        """Returns whether the two rate limit handler has the same `.limiter_id` and `.parent`."""
        if self.limiter_id != other.limiter_id:
            return False
        
        if self.parent.group_id != other.parent.group_id:
            return False
        
        return True
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different `.limiter_id` or `.parent`."""
        if self.limiter_id != other.limiter_id:
            return True
        
        if self.parent.group_id != other.parent.group_id:
            return True
        
        return False
    
    def __hash__(self):
        """Hashes the rate limit handler."""
        return self.parent.group_id+self.limiter_id
    
    def is_unlimited(self):
        """
        Returns whether the rate limit handler is unlimited.
        
        is_unlimited : `bool` = `False`
            Static rate limit handlers are always limited.
        """
        return False
    
    async def enter(self):
        """
        Waits till a respective request can be started.
        
        Should be called before the rate limit handler is used inside of it's context manager.
        
        This method is a coroutine.
        """
        lock = self.lock
        if lock is None:
            self.lock = lock = ScarletLock(KOKORO, self.parent.size)
        
        await lock.acquire()
    
    def exit(self, headers):
        """
        Called by the rate limit handler's context manager (``RateLimitHandlerCTX``) when a respective request is done.
        
        Static rate limit handler always ensures it's timeout.
        
        Parameters
        ----------
        headers : `None` or `imultidict` of (`str`, `str`) items
            Response headers
        """
        handle = KOKORO.call_later(self.parent.timeout, self.lock.release)
        if handle is None: # If the loop is stopped, force release it.
            self.lock.release()
    
    def ctx(self):
        """
        Context manager for rate limit handler.
        
        Returns
        -------
        ctx : ``RateLimitHandlerCTX``
        """
        return RateLimitHandlerCTX(self)

class StackedStaticRateLimitHandler(object):
    """
    Stacked static rate limit handler to defend the wrapper from stacked stupidity.
    
    Attributes
    ----------
    stack : `tuple` of ``StaticRateLimitHandler``
        A stack of static rate limit handlers.
    
    Notes
    -----
    Stacked static rate limit handlers are weakreferencable.
    """
    __slots__ = ('__weakref__', 'stack',)
    def __new__(cls, parents, limiter_id):
        """
        Creates a new stacked static rate limiter instance.
        
        Parameters
        ----------
        parents : `tuple` of ``StaticRateLimitGroup``
            A stack of static rate limit groups.
        limiter_id : `int`
            The `id` of the Discord Entity based on what the handler is limiter.
        """
        self = object.__new__(cls)
        self.stack = tuple(StaticRateLimitHandler(parent, limiter_id) for parent in parents)
        return self
    
    def __repr__(self):
        """Returns the rate limit handler's representation."""
        return f'<{self.__class__.__name__} stack={self.stack!r}>'
    
    def __bool__(self):
        """Returns whether the rate limit handler is active."""
        for handler in self.stack:
            if handler:
                return True
        
        return False
    
    def __eq__(self, other):
        """Returns whether the two rate limit handler has the same `.limiter_id` and `.parent`."""
        if isinstance(other, StackedStaticRateLimitHandler):
            other = other.stack[0]
        
        if self.stack[0] == other:
            return True
        
        return False
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different `.limiter_id` or `.parent`."""
        if isinstance(other, StackedStaticRateLimitHandler):
            other = other.stack[0]
        
        if self.stack[0] != other:
            return True
        
        return False
    
    def __hash__(self):
        """Hashes the rate limit handler."""
        return hash(self.stack[0])
    
    def is_unlimited(self):
        """
        Returns whether the rate limit handler is unlimited.
        
        is_unlimited : `bool` = `False`
            Static rate limit handlers are always limited.
        """
        return False
    
    async def enter(self):
        """
        Waits till a respective request can be started.
        
        Should be called before the rate limit handler is used inside of it's context manager.
        
        This method is a coroutine.
        """
        stack = self.stack
        for handler in stack:
            try:
                await handler.enter()
            except:
                for entered in stack[:stack.index(handler)]:
                    entered.exit(None)
                
                raise
    
    def exit(self, headers):
        """
        Called by the rate limit handler's context manager (``RateLimitHandlerCTX``) when a respective request is done.
        
        Static rate limit handler always ensures it's timeout.
        
        Parameters
        ----------
        headers : `None` or `imultidict` of (`str`, `str`) items
            Response headers
        """
        for handler in self.stack:
            handler.exit(headers)
    
    def ctx(self):
        """
        Context manager for rate limit handler.
        
        Returns
        -------
        ctx : ``RateLimitHandlerCTX``
        """
        return RateLimitHandlerCTX(self)

@modulize
class RATE_LIMIT_GROUPS:
    """
    Defines the rate limit groups by hata. Hata uses burst half automatic rate limit handler.
    
    Burst rate limit handler means, if (for example) 30 requests can be done to an endpoint before it resets, it will
    let 30 requests to pass trough, and with 31th will wait till the limits expires.
    
    Half automatic, since it automatically detects rate limit sizes with it's first request, but it do not detects
    which endpoints are limited together and by which id, since they are set by their rate limit group.
    
    It is optimistic, since Discord do not limits every endpoint, but endpoints which will be potentially changed
    are marked as optimistic. They have a limiter set, but their limit can be subject of change. The implementation
    lets trough 1 more request with each cycle, starting from `1`, till it reaches a set `n` limit. If any of the
    requests return rate limit information, then changes the endpoints limitations to it. The increased pararellity
    starting by `1` is to ensure, that the endpoint is mapped by first request. The increasing pararellity represents
    the decreasing chance of getting any rate limit information back.
    
    Limit Guides
    ------------
    The following shortenings are used inside of group descriptions:
    - `N/A` : Not applicable
    - `UN` : Unknown
    - `OPT` : Optimistic
    
    Limiter types:
    - `UNLIMITED`
    - `GLOBAL`
    - `channel_id`
    - `guild_id`
    - `webhook_id`
    
    Required auth types:
    - `N/A` (No auth required.)
    - `UN` (Unknown, not bot.)
    - `application`
    - `bearer`
    - `bot`
    - `user`
    
    Content Delivery Network Endpoint
    ---------------------------------
    - Endpoint : `https://cdn.discordapp.com/`
    - Method : `GET`
    - Required auth : `N/A`
    - Limiter : `UNLIMITED`
    - Limit : `N/A`
    - Resets after : `N/A`
    
    Shared Groups
    -------------
    - GROUP_REACTION_MODIFY
        - Used by : `reaction_clear`, `reaction_delete_emoji`, `reaction_delete_own`, `reaction_add`, `reaction_delete`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - GROUP_PIN_MODIFY
        - Used by : `message_unpin`, `message_pin`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `4.0`
    
    - GROUP_USER_MODIFY
        - Used by : `user_edit`, `user_move`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - GROUP_USER_ROLE_MODIFY
        - Used by : `user_role_delete`, `user_role_add`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - GROUP_WEBHOOK_EXECUTE
        - Used by : `webhook_message_create`, `webhook_message_delete`, `webhook_message_edit`
        - Limiter : `webhook_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - GROUP_INTERACTION_EXECUTE
        - Used by: `interaction_followup_message_create`, `interaction_response_message_delete`,
            `interaction_response_message_edit`, `interaction_followup_message_delete`,
            `interaction_followup_message_edit`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    Group Details
    -----------
    - oauth2_token
        - Endpoint : `oauth2/token`
        - Method : `POST`
        - Required auth : `application`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - application_get
        - Endpoint : `/applications/{application_id}`
        - Method : `GET`
        - Required auth : `UN`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - achievement_get_all
        - Endpoint : `/applications/{application_id}/achievements`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - achievement_create
        - Endpoint : `/applications/{application_id}/achievements`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - achievement_delete
        - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - achievement_get
        - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - achievement_edit
        - Endpoint : `/applications/{application_id}/achievements/{achievement_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - application_command_global_get_all
        - Endpoint : `/applications/{application_id}/commands`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_global_get
        - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_global_delete
        - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_global_create
        - Endpoint : `/applications/{application_id}/commands`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_global_edit
        - Endpoint : `/applications/{application_id}/commands/{application_command_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_guild_get_all
        - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_guild_get
        - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_guild_delete
        - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_guild_create
        - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_command_guild_edit
        - Endpoint : `/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - application_get_all_detectable
        - Endpoint : `/applications/detectable`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - client_logout
        - Endpoint : `/auth/logout`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `N/A`
        - Resets after : `N/A`
        - Notes : Untested.
    
    - channel_delete
        - Endpoint : `/channels/{channel_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`

    - channel_group_leave
        - Endpoint : `/channels/{channel_id}`
        - Method : `DELETE`
        - Required auth : `user`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
        - Notes : Untested.
    
    - channel_edit
        - Endpoint : `/channels/{channel_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `15`
        - Notes : Has sub-limits.
    
    - channel_group_edit
        - Endpoint : `/channels/{channel_id}`
        - Method : `PATCH`
        - Required auth : `user`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - channel_follow
        - Endpoint : `/channels/{channel_id}/followers`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - invite_get_all_channel
        - Endpoint : `/channels/{channel_id}/invites`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - invite_create
        - Endpoint : `/channels/{channel_id}/invites`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `15.0`
    
    - message_get_chunk
        - Endpoint : `/channels/{channel_id}/messages`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `5.0`
    
    - message_create
        - Endpoint : `/channels/{channel_id}/messages`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `4.0`
    
    - message_delete_multiple
        - Endpoint : `/channels/{channel_id}/messages/bulk-delete`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `3.0`
    
    - message_delete
        - Endpoint : `/channels/{channel_id}/messages/{message_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `3`
        - Resets after : `1.0`
        - Notes : Applicable for messages posted by the bot or which are younger than 2 weeks. Has sub-limits.
    
    - message_delete_b2wo
        - Endpoint : `/channels/{channel_id}/messages/{message_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `30`
        - Resets after : `120.0`
        - Notes : Applicable for messages which are not posted by the bot and are older than 2 weeks. Has sub-limits.
    
    - message_get
        - Endpoint : `/channels/{channel_id}/messages/{message_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `5.0`
    
    - message_edit
        - Endpoint : `/channels/{channel_id}/messages/{message_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `4.0`
    
    - message_ack
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/ack`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - message_crosspost
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/crosspost`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `10`
        - Resets after : `3600.0`
    
    - reaction_clear
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - reaction_delete_emoji
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - reaction_user_get_chunk
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - reaction_delete_own
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - reaction_add
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - reaction_delete
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `1`
        - Resets after : `0.25`
    
    - message_suppress_embeds
        - Endpoint : `/channels/{channel_id}/messages/{message_id}/suppress-embeds`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `3`
        - Resets after : `1`
    
    - permission_overwrite_delete
        - Endpoint : `/channels/{channel_id}/permissions/{overwrite_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - permission_overwrite_create
        - Endpoint : `/channels/{channel_id}/permissions/{overwrite_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - channel_pin_get_all
        - Endpoint : `/channels/{channel_id}/pins`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `5`
    
    - channel_pin_ack
        - Endpoint : `/channels/{channel_id}/pins/ack`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - message_unpin
        - Endpoint : `/channels/{channel_id}/pins/{message_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `4`
    
    - message_pin
        - Endpoint : `/channels/{channel_id}/pins/{message_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `4`
    
    - channel_group_user_get_all
        - Endpoint : `/channels/{channel_id}/recipients/`
        - Method : `GET`
        - Required auth : `user`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - channel_group_user_delete
        - Endpoint : `/channels/{channel_id}/recipients/{user_id}`
        - Method : `DELETE`
        - Required auth : `user`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - channel_group_user_add
        - Endpoint : `/channels/{channel_id}/recipients/{user_id}`
        - Method : `PUT`
        - Required auth : `user`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
        
    - thread_create
        - Endpoint : `/channels/{channel_id}/threads`
        - Method : `POST`
        - Required auth : `UN`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - thread_user_get_all
        - Endpoint : `/channels/{channel_id}/threads/participants`
        - Method : `GET`
        - Required auth : `UN`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - thread_user_delete
        - Endpoint : `/channels/{channel_id}/threads/participants/{user_id}`
        - Method : `DELETE`
        - Required auth : `UN`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - thread_user_add
        - Endpoint : `/channels/{channel_id}/threads/participants/{user_id}`
        - Method : `POST`
        - Required auth : `UN`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - typing
        - Endpoint : `/channels/{channel_id}/typing`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `5`
        - Resets after : `5.0`
    
    - webhook_get_all_channel
        - Endpoint : `/channels/{channel_id}/webhooks`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - webhook_create
        - Endpoint : `/channels/{channel_id}/webhooks`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `channel_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - discovery_category_get_all
        - Endpoint : `/discovery/categories`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `10`
        - Resets after : `120.0`
    
    - discovery_validate_term
        - Endpoint : `/discovery/valid-term`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `10`
        - Resets after : `10.0`
    
    - client_gateway_hooman
        - Endpoint : `/gateway`
        - Method : `GET`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `UN`
        - Resets after : `UN`
        - Notes : Untested.
    
    - client_gateway_bot
        - Endpoint : `/gateway/bot`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `2`
        - Resets after : `5`
    
    - guild_create
        - Endpoint : `/guilds`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - guild_delete
        - Endpoint : `/guilds/{guild_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - guild_get
        - Endpoint : `/guilds/{guild_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_edit
        - Endpoint : `/guilds/{guild_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_ack
        - Endpoint : `/guilds/{guild_id}/ack`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `UN`
        - Resets after : `UN`
        - Notes : Untested.
    
    - audit_log_get_chunk
        - Endpoint : `/guilds/{guild_id}/audit-logs`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_ban_get_all
        - Endpoint : `/guilds/{guild_id}/bans`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_ban_delete
        - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_ban_get
        - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_ban_add
        - Endpoint : `/guilds/{guild_id}/bans/{user_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_channel_get_all
        - Endpoint : `/guilds/{guild_id}/channels`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - channel_move
        - Endpoint : `/guilds/{guild_id}/channels`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - channel_create
        - Endpoint : `/guilds/{guild_id}/channels`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_discovery_delete_subcategory
        - Endpoint : `/guilds/{guild_id}/discovery-categories/{category_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_discovery_add_subcategory
        - Endpoint : `/guilds/{guild_id}/discovery-categories/{category_id}`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_discovery_get
        - Endpoint : `/guilds/{guild_id}/discovery-metadata`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_discovery_edit
        - Endpoint : `/guilds/{guild_id}/discovery-metadata`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_embed_get
        - Endpoint : `/guilds/{guild_id}/embed`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Deprecated. Works on v6, v7.
    
    - guild_embed_edit
        - Endpoint : `/guilds/{guild_id}/embed`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Deprecated. Works on v6, v7.
    
    - guild.embed_url
        - Endpoint : `/guilds/{guild_id}/embed.png`
        - Method : `GET`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
        - Notes : Deprecated. Works on v6, v7.
    
    - guild_emoji_get_all
        - Endpoint : `/guilds/{guild_id}/emojis`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - emoji_create
        - Endpoint : `/guilds/{guild_id}/emojis`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `50`
        - Resets after : `3600.0`
    
    - emoji_delete
        - Endpoint : `/guilds/{guild_id}/emojis`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `2.0`
    
    - emoji_get
        - Endpoint : `/guilds/{guild_id}/emojis/{emoji_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - emoji_edit
        - Endpoint : `/guilds/{guild_id}/emojis/{emoji_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `2.0`
    
    - integration_get_all
        - Endpoint : `/guilds/{guild_id}/integrations`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - integration_create
        - Endpoint : `/guilds/{guild_id}/integrations`
        - Method : `POST`
        - Required auth : `UN`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - integration_delete
        - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}`
        - Method : `DELETE`
        - Required auth : `UN`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - integration_edit
        - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}`
        - Method : `PATCH`
        - Required auth : `UN`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - integration_edit
        - Endpoint : `/guilds/{guild_id}/integrations/{integration_id}/sync`
        - Method : `POST`
        - Required auth : `UN`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - invite_get_all_guild
        - Endpoint : `/guilds/{guild_id}/invites`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - verification_screen_get
        - Endpoint : `/guilds/{guild_id}/member-verification`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - verification_screen_edit
        - Endpoint : `/guilds/{guild_id}/member-verification`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_user_get_chunk
        - Endpoint : `/guilds/{guild_id}/members`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - client_edit_nick
        - Endpoint : `/guilds/{guild_id}/members/@me/nick`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `1.0`
    
    - guild_user_delete
        - Endpoint : `/guilds/{guild_id}/members/{user_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `5`
        - Resets after : `1.0`
    
    - guild_user_get
        - Endpoint : `/guilds/{guild_id}/members/{user_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `5`
        - Resets after : `1.0`
    
    - user_edit, user_move
        - Endpoint : `/guilds/{guild_id}/members/{user_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - guild_user_add
        - Endpoint : `/guilds/{guild_id}/members/{user_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - guild_user_search
        - Endpoint : `/guilds/{guild_id}/members/search`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - user_role_delete
        - Endpoint : `/guilds/{guild_id}/members/{user_id}/roles/{role_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - user_role_add
        - Endpoint : `/guilds/{guild_id}/members/{user_id}/roles/{role_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `10`
        - Resets after : `10.0`
    
    - guild_preview_get
        - Endpoint : `/guilds/{guild_id}/preview`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - guild_prune_estimate
        - Endpoint : `/guilds/{guild_id}/prune`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_prune
        - Endpoint : `/guilds/{guild_id}/prune`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_voice_region_get_all
        - Endpoint : `/guilds/{guild_id}/regions`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_role_get_all
        - Endpoint : `/guilds/{guild_id}/roles`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - role_move
        - Endpoint : `/guilds/{guild_id}/roles`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - role_create
        - Endpoint : `/guilds/{guild_id}/roles`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `250`
        - Resets after : `172800.0`
    
    - role_delete
        - Endpoint : `/guilds/{guild_id}/roles/{role_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - role_edit
        - Endpoint : `/guilds/{guild_id}/roles/{role_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `1000`
        - Resets after : `86400.0`
    
    - vanity_invite_get
        - Endpoint : `/guilds/{guild_id}/vanity-url`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - vanity_invite_get
        - Endpoint : `/guilds/{guild_id}/vanity-url`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - welcome_screen_get
        - Endpoint : `/guilds/{guild_id}/welcome-screen`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - welcome_screen_edit
        - Endpoint : `/guilds/{guild_id}/welcome-screen`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `100`
        - Resets after : `86400`
    
    - webhook_get_all_guild
        - Endpoint : `/guilds/{guild_id}/webhooks`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `guild_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_widget_get
        - Endpoint : `/guilds/{guild_id}/widget.json`
        - Method : `GET`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - guild.widget_url
        - Endpoint : `/guilds/{guild_id}/widget.png`
        - Method : `GET`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - hypesquad_house_leave
        - Endpoint : `/hypesquad/online`
        - Method : `DELETE`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `UN`
        - Resets after : `UN`
        - Notes : Untested.
    
    - hypesquad_house_change
        - Endpoint : `/hypesquad/online`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `UN`
        - Resets after : `UN`
        - Notes : Untested.
    
    - interaction_response_message_create
        - Endpoint : `/interactions/{interaction_id}/{interaction_token}/callback`
        - Method : `POST`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - invite_delete
        - Endpoint : `/invites/{invite_code}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - invite_get
        - Endpoint : `/invites/{invite_code}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `250`
        - Resets after : `6.0`
    
    - client_application_get
        - Endpoint : `/oauth2/applications/@me`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - bulk_ack
        - Endpoint : `/read-states/ack-bulk`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `UN`
        - Resets after : `UN`
        - Notes : Untested.
    
    - eula_get
        - Endpoint : `/store/eulas/{eula_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - user_info_get
        - Endpoint : `/users/@me`
        - Method : `GET`
        - Required auth : `bearer`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - client_user_get
        - Endpoint : `/users/@me`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - client_edit
        - Endpoint : `/users/@me`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `2`
        - Resets after : `3600.0`
    
    - user_achievement_get_all
        - Endpoint : `/users/@me/applications/{application_id}/achievements`
        - Method : `GET`
        - Required auth : `bearer`
        - Limiter : `GLOBAL`
        - Limit : `2`
        - Resets after : `5.0`
        - Notes : Untested.
    
    - user_achievement_update
        - Endpoint : `/users/{user_id}/applications/{application_id}/achievements/{achievement_id}`
        - Method : `PUT`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `5`
        - Resets after : `5.0`
    
    - channel_private_get_all
        - Endpoint : `/users/@me/channels`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - channel_private_create
        - Endpoint : `/users/@me/channels`
        - Method : `POST`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - client_connection_get_all
        - Endpoint : `/users/@me/connections`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - user_connection_get_all
        - Endpoint : `/users/@me/connections`
        - Method : `GET`
        - Required auth : `bearer`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - guild_get_all
        - Endpoint : `/users/@me/guilds`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `1.0`
    
    - user_guild_get_all
        - Endpoint : `/users/@me/guilds`
        - Method : `GET`
        - Required auth : `bearer`
        - Limiter : `GLOBAL`
        - Limit : `1`
        - Resets after : `1.0`
    
    - guild_leave
        - Endpoint : `/users/@me/guilds/{guild_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - relationship_friend_request
        - Endpoint : `/users/@me/relationships`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - relationship_delete
        - Endpoint : `/users/@me/relationships/{user_id}`
        - Method : `DELETE`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - relationship_create
        - Endpoint : `/users/@me/settings`
        - Method : `PUT`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - client_settings_get
        - Endpoint : `/users/@me/settings`
        - Method : `GET`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - client_settings_edit
        - Endpoint : `/users/@me/settings`
        - Method : `PATCH`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - user_get
        - Endpoint : `/users/{user_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `30`
        - Resets after : `30.0`
    
    - channel_group_create
        - Endpoint : `/users/{user_id}/channels`
        - Method : `POST`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - user_get_profile
        - Endpoint : `users/{user_id}/profile`
        - Method : `GET`
        - Required auth : `user`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
        - Notes : Untested.
    
    - voice_region_get_all
        - Endpoint : `/voice/regions`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `GLOBAL`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - interaction_followup_message_create
        - Endpoint : `webhooks/{application_id}/{interaction_token}`
        - Method : `POST`
        - Required auth : `N/A`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - interaction_response_message_delete
        - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/@original`
        - Method : `DELETE`
        - Required auth : `N/A`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - interaction_response_message_edit
        - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/@original`
        - Method : `PATCH`
        - Required auth : `N/A`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - interaction_followup_message_delete
        - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/{message_id}`
        - Method : `DELETE`
        - Required auth : `N/A`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - interaction_followup_message_edit
        - Endpoint : `webhooks/{application_id}/{interaction_token}/messages/{message_id}`
        - Method : `PATCH`
        - Required auth : `N/A`
        - Limiter : `interaction_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - webhook_delete
        - Endpoint : `/webhooks/{webhook_id}`
        - Method : `DELETE`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - webhook_get
        - Endpoint : `/webhooks/{webhook_id}`
        - Method : `GET`
        - Required auth : `bot`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - webhook_edit
        - Endpoint : `/webhooks/{webhook_id}`
        - Method : `PATCH`
        - Required auth : `bot`
        - Limiter : `webhook_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - webhook_delete_token
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
        - Method : `DELETE`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - webhook_get_token
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
        - Method : `GET`
        - Required auth : `N/A`
        - Limiter : `UNLIMITED`
        - Limit : `N/A`
        - Resets after : `N/A`
    
    - webhook_edit_token
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
        - Method : `PATCH`
        - Required auth : `N/A`
        - Limiter : `webhook_id`
        - Limit : `OPT`
        - Resets after : `OPT`
    
    - webhook_message_create
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}`
        - Method : `POST`
        - Required auth : `N/A`
        - Limiter : `webhook_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - webhook_message_delete
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}`
        - Method : `DELETE`
        - Required auth : `N/A`
        - Limiter : `webhook_id`
        - Limit : `5`
        - Resets after : `2.0`
    
    - webhook_message_edit
        - Endpoint : `/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}`
        - Method : `PATCH`
        - Required auth : `N/A`
        - Limiter : `webhook_id`
        - Limit : `5`
        - Resets after : `2.0`
    """
    GROUP_REACTION_MODIFY       = RateLimitGroup(LIMITER_CHANNEL)
    GROUP_PIN_MODIFY            = RateLimitGroup(LIMITER_CHANNEL)
    GROUP_USER_MODIFY           = RateLimitGroup(LIMITER_GUILD) # both has the same endpoint
    GROUP_USER_ROLE_MODIFY      = RateLimitGroup(LIMITER_GUILD)
    GROUP_WEBHOOK_EXECUTE       = RateLimitGroup(LIMITER_WEBHOOK)
    GROUP_INTERACTION_EXECUTE   = RateLimitGroup(LIMITER_INTERACTION)
    
    oauth2_token                = RateLimitGroup(optimistic=True)
    application_get             = RateLimitGroup(optimistic=True) # untested
    achievement_get_all         = RateLimitGroup()
    achievement_create          = RateLimitGroup()
    achievement_delete          = RateLimitGroup()
    achievement_get             = RateLimitGroup()
    achievement_edit            = RateLimitGroup()
    application_command_global_get_all = RateLimitGroup.unlimited()
    application_command_global_get = RateLimitGroup.unlimited()
    application_command_global_delete = RateLimitGroup.unlimited()
    application_command_global_create = RateLimitGroup.unlimited()
    application_command_global_edit = RateLimitGroup.unlimited()
    application_command_guild_get_all = RateLimitGroup.unlimited()
    application_command_guild_get = RateLimitGroup.unlimited()
    application_command_guild_delete = RateLimitGroup.unlimited()
    application_command_guild_create = RateLimitGroup.unlimited()
    application_command_guild_edit = RateLimitGroup.unlimited()
    application_get_all_detectable = RateLimitGroup(optimistic=True)
    client_logout               = RateLimitGroup() # untested
    channel_delete              = RateLimitGroup.unlimited()
    channel_group_leave         = RateLimitGroup.unlimited() # untested; same as channel_delete?
    channel_edit                = RateLimitGroup(LIMITER_CHANNEL)
    channel_group_edit          = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested; same as channel_edit?
    channel_follow              = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    invite_get_all_channel      = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    invite_create               = RateLimitGroup()
    message_get_chunk           = RateLimitGroup(LIMITER_CHANNEL)
    message_create              = RateLimitGroup(LIMITER_CHANNEL)
    message_delete_multiple     = RateLimitGroup(LIMITER_CHANNEL)
    message_delete              = RateLimitGroup(LIMITER_CHANNEL)
    message_delete_b2wo         = RateLimitGroup(LIMITER_CHANNEL)
    message_get                 = RateLimitGroup(LIMITER_CHANNEL)
    message_edit                = RateLimitGroup(LIMITER_CHANNEL)
    message_ack                 = RateLimitGroup(optimistic=True) # untested
    message_crosspost           = RateLimitGroup(LIMITER_CHANNEL)
    reaction_clear              = GROUP_REACTION_MODIFY
    reaction_delete_emoji       = GROUP_REACTION_MODIFY
    reaction_user_get_chunk     = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    reaction_delete_own         = GROUP_REACTION_MODIFY
    reaction_add                = GROUP_REACTION_MODIFY
    reaction_delete             = GROUP_REACTION_MODIFY
    message_suppress_embeds     = RateLimitGroup()
    permission_overwrite_delete = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    permission_overwrite_create = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    channel_pin_get_all         = RateLimitGroup()
    channel_pin_ack             = RateLimitGroup(optimistic=True) # untested
    message_unpin               = GROUP_PIN_MODIFY
    message_pin                 = GROUP_PIN_MODIFY
    channel_group_user_get_all  = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    channel_group_user_delete   = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    channel_group_user_add      = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    thread_create               = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    thread_user_get_all         = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    thread_user_delete          = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    thread_user_add             = RateLimitGroup(LIMITER_CHANNEL, optimistic=True) # untested
    typing                      = RateLimitGroup(LIMITER_CHANNEL)
    webhook_get_all_channel     = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    webhook_create              = RateLimitGroup(LIMITER_CHANNEL, optimistic=True)
    discovery_category_get_all  = RateLimitGroup()
    discovery_validate_term     = RateLimitGroup()
    client_gateway_hooman       = RateLimitGroup()
    client_gateway_bot          = RateLimitGroup()
    guild_create                = RateLimitGroup.unlimited()
    guild_delete                = RateLimitGroup.unlimited()
    guild_get                   = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_edit                  = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_ack                   = RateLimitGroup() # untested
    audit_log_get_chunk         = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_ban_get_all           = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_ban_delete            = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_ban_get               = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_ban_add               = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_channel_get_all       = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    channel_move                = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    channel_create              = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_discovery_delete_subcategory = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_discovery_add_subcategory = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_discovery_get         = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_discovery_edit        = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_embed_get             = RateLimitGroup(LIMITER_GUILD, optimistic=True) # deprecated
    guild_embed_edit            = RateLimitGroup(LIMITER_GUILD, optimistic=True) # deprecated
    guild_emoji_get_all         = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    emoji_create                = RateLimitGroup()
    emoji_delete                = RateLimitGroup()
    emoji_get                   = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    emoji_edit                  = RateLimitGroup()
    integration_get_all         = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    integration_create          = RateLimitGroup(optimistic=True) # untested
    integration_delete          = RateLimitGroup(optimistic=True) # untested
    integration_edit            = RateLimitGroup(optimistic=True) # untested
    integration_sync            = RateLimitGroup(optimistic=True) # untested
    invite_get_all_guild        = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    verification_screen_get     = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    verification_screen_edit    = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_user_get_chunk        = RateLimitGroup(LIMITER_GUILD)
    client_edit_nick            = RateLimitGroup()
    guild_user_delete           = RateLimitGroup(LIMITER_GUILD)
    guild_user_get              = RateLimitGroup(LIMITER_GUILD)
    user_edit                   = GROUP_USER_MODIFY
    user_move                   = GROUP_USER_MODIFY
    guild_user_add              = RateLimitGroup(LIMITER_GUILD)
    guild_user_search           = RateLimitGroup(LIMITER_GUILD)
    user_role_delete            = GROUP_USER_ROLE_MODIFY
    user_role_add               = GROUP_USER_ROLE_MODIFY
    guild_preview_get           = RateLimitGroup()
    guild_prune_estimate        = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_prune                 = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_voice_region_get_all  = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_role_get_all          = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    role_move                   = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    role_create                 = RateLimitGroup(LIMITER_GUILD)
    role_delete                 = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    role_edit                   = RateLimitGroup(LIMITER_GUILD)
    vanity_invite_get           = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    vanity_invite_edit          = RateLimitGroup(LIMITER_GUILD, optimistic=True) # untested
    welcome_screen_get          = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    welcome_screen_edit         = RateLimitGroup(LIMITER_GUILD)
    webhook_get_all_guild       = RateLimitGroup(LIMITER_GUILD, optimistic=True)
    guild_widget_get            = RateLimitGroup.unlimited()
    hypesquad_house_leave       = RateLimitGroup() # untested
    hypesquad_house_change      = RateLimitGroup() # untested
    interaction_response_message_create = RateLimitGroup.unlimited() # untested
    invite_delete               = RateLimitGroup.unlimited()
    invite_get                  = RateLimitGroup()
    client_application_get      = RateLimitGroup(optimistic=True)
    bulk_ack                    = RateLimitGroup(optimistic=True) # untested
    eula_get                    = RateLimitGroup(optimistic=True)
    user_info_get               = RateLimitGroup(optimistic=True)
    client_user_get             = RateLimitGroup(optimistic=True)
    client_edit                 = RateLimitGroup()
    user_achievement_get_all    = RateLimitGroup() # untested; has expected global rate limit
    user_achievement_update     = RateLimitGroup()
    channel_private_get_all     = RateLimitGroup(optimistic=True)
    channel_private_create      = RateLimitGroup.unlimited()
    client_connection_get_all   = RateLimitGroup(optimistic=True)
    user_connection_get_all     = RateLimitGroup(optimistic=True)
    guild_get_all               = RateLimitGroup()
    user_guild_get_all          = RateLimitGroup()
    guild_leave                 = RateLimitGroup.unlimited()
    relationship_friend_request = RateLimitGroup(optimistic=True) # untested
    relationship_delete         = RateLimitGroup(optimistic=True) # untested
    relationship_create         = RateLimitGroup(optimistic=True) # untested
    client_settings_get         = RateLimitGroup(optimistic=True) # untested
    client_settings_edit        = RateLimitGroup(optimistic=True) # untested
    user_get                    = RateLimitGroup()
    channel_group_create        = RateLimitGroup(optimistic=True) # untested
    user_get_profile            = RateLimitGroup(optimistic=True) # untested
    voice_region_get_all        = RateLimitGroup(optimistic=True)
    interaction_followup_message_create = GROUP_INTERACTION_EXECUTE
    interaction_response_message_delete = GROUP_INTERACTION_EXECUTE
    interaction_response_message_edit = GROUP_INTERACTION_EXECUTE
    interaction_followup_message_delete = GROUP_INTERACTION_EXECUTE
    interaction_followup_message_edit = GROUP_INTERACTION_EXECUTE
    webhook_delete              = RateLimitGroup.unlimited()
    webhook_get                 = RateLimitGroup.unlimited()
    webhook_edit                = RateLimitGroup(LIMITER_WEBHOOK, optimistic=True)
    webhook_delete_token        = RateLimitGroup.unlimited()
    webhook_get_token           = RateLimitGroup.unlimited()
    webhook_edit_token          = RateLimitGroup(LIMITER_WEBHOOK, optimistic=True)
    webhook_message_create      = GROUP_WEBHOOK_EXECUTE
    webhook_message_edit        = GROUP_WEBHOOK_EXECUTE
    webhook_message_delete      = GROUP_WEBHOOK_EXECUTE

    # Alternative static versions
    STATIC_MESSAGE_DELETE_SUB   = StaticRateLimitGroup(5, 5.0, LIMITER_CHANNEL)
    static_message_delete       = (STATIC_MESSAGE_DELETE_SUB, StaticRateLimitGroup(3, 1.0, LIMITER_CHANNEL))
    static_message_delete_b2wo  = (STATIC_MESSAGE_DELETE_SUB, StaticRateLimitGroup(30, 120.0, LIMITER_CHANNEL))

del modulize
del DOCS_ENABLED
