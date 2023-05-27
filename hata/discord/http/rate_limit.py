__all__ = ()

from collections import deque
from datetime import datetime, timezone

from scarletio import Future, LOOP_TIME, ScarletLock
from scarletio.web_common.headers import DATE

from ..core import KOKORO
from ..utils import parse_date_header_to_datetime

from .headers import RATE_LIMIT_LIMIT, RATE_LIMIT_REMAINING, RATE_LIMIT_RESET, RATE_LIMIT_RESET_AFTER


GLOBALLY_LIMITED = 0x4000000000000000
RATE_LIMIT_DROP_ROUND = 0.20
MAXIMAL_UNLIMITED_PARARELLITY = -50
UNLIMITED_SIZE_VALUE = -10000
NO_SPECIFIC_RATE_LIMITER = 0

LIMITER_CHANNEL = 'channel_id'
LIMITER_GUILD = 'guild_id'
LIMITER_WEBHOOK = 'webhook_id'
LIMITER_INTERACTION = 'interaction_id'
LIMITER_GLOBAL = 'global'
LIMITER_UNLIMITED = 'unlimited'


class RateLimitGroup:
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
    
    _auto_next_id = 105 << 8
    _unlimited = None
    
    @classmethod
    def generate_next_id(cls):
        """
        Generates the next auto id of a rate limit group and returns it.
        
        Returns
        -------
        group_id : `int`
        """
        group_id = cls._auto_next_id
        cls._auto_next_id = group_id + (7 << 8)
        return group_id
    
    
    def __new__(cls, limiter = LIMITER_GLOBAL, optimistic = False):
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
        
        optimistic : `bool` = `False`, Optional
            Whether the rate limit group is optimistic.
        """
        self = object.__new__(cls)
        self.limiter = limiter
        self.size = ( -1 if optimistic else 0)
        self.group_id = cls.generate_next_id()
        return self
    
    
    @classmethod
    def unlimited(cls):
        """
        Creates a not limited rate limit group.
        
        Uses ``._unlimited`` to cache this instance, because it is enough to have only 1 unlimited one.
        
        Returns
        -------
        self : ``RateLimitGroup``
        """
        self = cls._unlimited
        if (self is not None):
            return self
        
        self = object.__new__(cls)
        self.size = UNLIMITED_SIZE_VALUE
        self.group_id = 0
        self.limiter = LIMITER_UNLIMITED
        
        cls._unlimited = self
        return self
    
    
    def __hash__(self):
        """Hash of a rate limit group equals to it's group_id."""
        return self.group_id
    
    
    def __repr__(self):
        """Returns the representation of the rate limit group."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' size=',
            repr(self.size),
            ', ',
        ]
        
        limiter = self.limiter
        if limiter is LIMITER_GLOBAL:
            repr_parts.append('limited globally')
        elif limiter is LIMITER_UNLIMITED:
            repr_parts.append('unlimited')
        else:
            repr_parts.append('limited by ')
            repr_parts.append(limiter)
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class RateLimitUnit:
    """
    Represents a chained rate limit unit storing how much request is already done till the next reset, what is
    also stored by it.
    
    Attributes
    ----------
    allocates : `int`
        The amount of done requests till next rate limit reset.
    drop : `float`
        The time of the next rate limit reset in `LOOP_TIME` time.
    next : `None`, ``RateLimitUnit``
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
        new_drop_max = drop + RATE_LIMIT_DROP_ROUND
        if new_drop_max < actual_drop:
            new = object.__new__(type(self))
            new.drop = self.drop
            new.allocates = self.allocates
            new.next = self.next
            self.drop = drop
            self.allocates = allocates
            self.next = new
            return
        
        new_drop_min = drop - RATE_LIMIT_DROP_ROUND
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
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' drop = ',
            repr(self.drop),
            ', allocates = ',
            repr(self.allocates),
        ]
        
        next_ = self.next
        if (next_ is not None):
            repr_parts.append(', next = [')
            while True:
                repr_parts.append('(')
                repr_parts.append(repr(next_.drop))
                repr_parts.append(', ')
                repr_parts.append(repr(next_.allocates))
                repr_parts.append(')')
                next_ = next_.next
                if (next_ is None):
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


def get_rate_limit_delay_from_headers(headers):
    """
    Returns rate limit delay based on the given headers.
    
    Parameters
    ----------
    headers : ``IgnoreCaseMultiValueDictionary``
        Request headers.
    
    Returns
    -------
    delay : `float`
    """
    delay_reset_after = float(headers[RATE_LIMIT_RESET_AFTER])
    
    try:
        rate_limit_reset_at = datetime.fromtimestamp(float(headers[RATE_LIMIT_RESET]), timezone.utc)
    except ValueError:
        # I dont know what they drank, but it happened:
        # ValueError: year 584556072 is out of range
        return delay_reset_after
    
    request_done_at = parse_date_header_to_datetime(headers[DATE])
    
    return min(
        delay_reset_after,
        (rate_limit_reset_at - request_done_at).total_seconds(),
    )


class RateLimitHandler:
    """
    Handles a request's rate limit.
    
    Attributes
    ----------
    active : `int`
        The amount of active requests with the same `limiter_id` and with the same `parent`.
    drops : `None`, ``RateLimitUnit``
        The already used up rate limits.
    limiter_id : `int`
        The `id` of the Discord Entity based on what the handler is limiter.
    parent : ``RateLimitGroup``
        The rate limit group of the rate limit handler.
    queue : `None` or (`deque` of ``Future``)
        Queue of ``Future`` objects of waiting requests.
    wake_upper : `None`, ``TimerHandle``
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
        `.drops`, ``.wake_upper`` one, but because this rate limit handler might be used just to look up an already
        existing one with the same ``.limiter_id`` and ``.parent``, so creating an another `deque` and then collecting
        it would be just waste of resources.
        
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
        Copies the rate limit handler. Only the ``.parent`` and the ``.limiter_id`` attributes are copied, because
        those are enough to describe it and will not cause misbehaviour.
        
        Returns
        -------
        new : ``RateLimitHandler``
        """
        new = object.__new__(type(self))
        new.parent = self.parent
        new.limiter_id = self.limiter_id
        new.drops = None
        new.active = 0
        new.queue = None
        new.wake_upper = None
        return new
    
    
    def __repr__(self):
        """Returns the representation of the rate limit handler."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        limiter = self.parent.limiter
        if limiter is LIMITER_UNLIMITED:
            repr_parts.append(' unlimited')
        else:
            repr_parts.append(' size: ')
            size = self.parent.size
            if size == -1:
                repr_parts.append('unset')
            else:
                repr_parts.append(repr(size))
            
            repr_parts.append(', active: ')
            repr_parts.append(repr(self.active))
            
            repr_parts.append(', cooldown drops: ')
            repr_parts.append(repr(self.drops))
            
            repr_parts.append(', queue length: ')
            queue = self.queue
            if queue is None:
                length = '0'
            else:
                length = repr(len(self.queue))
            repr_parts.append(length)
            
            if limiter is LIMITER_GLOBAL:
                repr_parts.append(', limited globally')
            else:
                repr_parts.append(', limited by ')
                repr_parts.append(limiter)
                repr_parts.append(': ')
                repr_parts.append(repr(self.limiter_id))
            
            repr_parts.append(', group id: ')
            repr_parts.append(repr(self.parent.group_id))
            
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        """Returns whether the two rate limit handler has the same ``.limiter_id`` and ``.parent``."""
        if self.limiter_id != other.limiter_id:
            return False
        
        if self.parent.group_id != other.parent.group_id:
            return False
        
        return True
    
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different ``.limiter_id``, ``.parent``."""
        if self.limiter_id != other.limiter_id:
            return True
        
        if self.parent.group_id != other.parent.group_id:
            return True
        
        return False
    
    
    def __hash__(self):
        """Hashes the rate limit handler."""
        return self.parent.group_id + self.limiter_id
    
    
    def is_unlimited(self):
        """
        Returns whether the rate limit handler is unlimited.
        
        Returns
        -------
        is_unlimited : `bool`
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
        left = size - active
        
        if left <= 0:
            future = Future(KOKORO)
            queue.append(future)
            await future
            
            self.active += 1
            return
        
        left -= self.count_drops()
        if left > 0:
            self.active = active + 1
            return
        
        future = Future(KOKORO)
        queue.append(future)
        await future
        
        self.active += 1
    
    
    def exit(self, headers):
        """
        Called by the rate limit handler's context manager (``RateLimitHandlerCTX``) when a respective request is done.
        
        Calculates the rate limits based on the given ``headers``. Handles first request, optimistic rate limit
        handling and changed rate limit sizes as well.
        
        Parameters
        ----------
        headers : `None`, ``IgnoreCaseMultiValueDictionary`` of (`str`, `str`) items
            Response headers
        """
        current_size = self.parent.size
        if current_size == UNLIMITED_SIZE_VALUE:
            return
        
        self.active -= 1
        
        optimistic = False
        while True:
            if (headers is not None):
                size = headers.get(RATE_LIMIT_LIMIT, None)
                if size is None:
                    if current_size < 0:
                        optimistic = True
                        # A not so special case when the endpoint is not rate limited yet.
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
                if current_size == -1 or current_size == 0:
                    current_size = 1
                    # We might have cooldowns from before as well
                    allocates = size - int(headers[RATE_LIMIT_REMAINING])
                
                can_free = size - current_size
                queue = self.queue
                queue_length = len(queue)
                
                if can_free > queue_length:
                    can_free = queue_length
                
                while can_free > 0:
                    future = queue.popleft()
                    future.set_result(None)
                    can_free -= 1
                    continue
        
        if optimistic:
            delay = 1.0
        else:
            delay = get_rate_limit_delay_from_headers(headers)
        
        drop = LOOP_TIME() + delay
        
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
        Called by ``.wake_upper`` when the handler's rate limits are dropped.
        
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
        queue_length = len(queue)
        if queue_length == 0:
            return
        
        # if exception occurs, nothing is added to self.drops, but active is decreased by one, so lets check active
        # count as well.
        # Also the first requests might set self.parent.size as well, to higher than 1 >.>
        size = self.parent.size
        if size < 0:
            size = -size
        
        can_free = size - self.active - self.count_drops()
        
        if can_free > queue_length:
            can_free = queue_length
        
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


class RateLimitHandlerCTX:
    """
    Context manager of a ``RateLimitHandler``.
    
    When the ``RateLimitHandlerCTX`` is exited by it's ``.exit`` or by it's ``.__exit__`` for the first time, then
    calls it's parent's ``.exit`` indicate that the request is done.
    
    Attributes
    ----------
    parent : ``RateLimitHandler``, ``StaticRateLimitHandler``
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
        Checks the context manager whether it was already exited and exits its parent with the given `headers`
        as well.
        
        Parameters
        ----------
        headers : `None`, `IgnoreCaseMultiValueDictionary`
            Response headers.
        """
        assert not self.exited, '`RateLimitHandlerCTX.exit`, `StaticRateLimitHandler.exit` was already called.'
        self.exited = True
        self.parent.exit(headers)
    
    
    def __enter__(self):
        """Enters the context manager returning itself."""
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exists the context manager and if the context manager was not exited yet, exists it's parent as well."""
        if not self.exited:
            self.exited = True
            self.parent.exit(None)
        
        return False


class StaticRateLimitGroup:
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
        limiter : `str` = `LIMITER_GLOBAL`, Optional
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
        repr_parts = [
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
            repr_parts.append('limited globally')
        elif limiter is LIMITER_UNLIMITED:
            repr_parts.append('unlimited')
        else:
            repr_parts.append('limited by ')
            repr_parts.append(limiter)
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class StaticRateLimitHandler:
    """
    Static rate limit handler to defend the wrapper from stupidity.
    
    Attributes
    ----------
    limiter_id : `int`
        The `id` of the Discord Entity based on what the handler is limiter.
    parent : ``RateLimitGroup``
        The rate limit group of the rate limit handler.
    lock : `None`, ``ScarletLock``
        Lock used to await entries and then lock them till they expire.
    
    Notes
    -----
    Static rate limit handlers are weakreferable.
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
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        limiter = self.parent.limiter
        if limiter is LIMITER_UNLIMITED:
            repr_parts.append(' unlimited')
        else:
            parent = self.parent
            repr_parts.append(' size: ')
            repr_parts.append(repr(parent.size))
            repr_parts.append(' timeout: ')
            repr_parts.append(repr(parent.timeout))
            
            repr_parts.append(', queue length: ')
            lock = self.lock
            if lock is None:
                length = '0'
            else:
                length = repr(lock.get_waiting())
            repr_parts.append(length)
            
            if limiter is LIMITER_GLOBAL:
                repr_parts.append(', limited globally')
            else:
                repr_parts.append(', limited by ')
                repr_parts.append(limiter)
                repr_parts.append(': ')
                repr_parts.append(repr(self.limiter_id))
            
            repr_parts.append(', group id: ')
            repr_parts.append(repr(self.parent.group_id))
            
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether the rate limit handler is active."""
        lock = self.lock
        if lock is None:
            return False
        
        if lock.get_acquired():
            return True
        
        return False
    
    
    def __eq__(self, other):
        """Returns whether the two rate limit handler has the same ``.limiter_id`` and ``.parent``."""
        if self.limiter_id != other.limiter_id:
            return False
        
        if self.parent.group_id != other.parent.group_id:
            return False
        
        return True
    
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different ``.limiter_id``, ``.parent``."""
        if self.limiter_id != other.limiter_id:
            return True
        
        if self.parent.group_id != other.parent.group_id:
            return True
        
        return False
    
    
    def __hash__(self):
        """Hashes the rate limit handler."""
        return self.parent.group_id + self.limiter_id
    
    
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
        headers : `None`, ``IgnoreCaseMultiValueDictionary`` of (`str`, `str`) items
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


class StackedStaticRateLimitHandler:
    """
    Stacked static rate limit handler to defend the wrapper from stacked stupidity.
    
    Attributes
    ----------
    stack : `tuple` of ``StaticRateLimitHandler``
        A stack of static rate limit handlers.
    
    Notes
    -----
    Stacked static rate limit handlers are weakreferable.
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
        """Returns whether the two rate limit handler has the same ``.limiter_id`` and ``.parent``."""
        if isinstance(other, StackedStaticRateLimitHandler):
            other = other.stack[0]
        
        if self.stack[0] == other:
            return True
        
        return False
    
    
    def __ne__(self, other):
        """Returns whether the two rate limit handler has different ``.limiter_id``, ``.parent``."""
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
        headers : `None`, ``IgnoreCaseMultiValueDictionary`` of (`str`, `str`) items
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
