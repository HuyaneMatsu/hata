__all__ = ()

from collections import deque

from ...backend.futures import Future
from ...backend.event_loop import LOOP_TIME

from ..core import KOKORO

GATEWAY_RATE_LIMIT_LIMIT = 120
GATEWAY_RATE_LIMIT_RESET = 60.0


class GatewayRateLimiter:
    """
    Burst rate limit handler for gateways, what operates on the clients' loop only.
    
    Attributes
    ----------
    queue : `deque` of ``Future``
        The queue of the rate limit handler. It is filled up with futures, if the handler's limit is exhausted.
        These futures are removed and their result is set, when the limit is reset.
    remaining : `int`
        The amount of requests which can be done, before the limit is exhausted.
    resets_at : `float`
        When the rate limit of the respective gateway will be reset.
    wake_upper : `None`  or `TimerHandle`
        A handler what will reset the limiter's limit and ensure it's queue if needed.
    """
    __slots__ = ('queue', 'remaining', 'resets_at', 'wake_upper', )
    
    def __init__(self):
        """
        Creates a gateway rate limiter.
        """
        self.remaining = GATEWAY_RATE_LIMIT_LIMIT
        self.queue = deque()
        self.wake_upper = None
        self.resets_at = 0.0
    
    
    def __iter__(self):
        """
        Awaits the rate limit handler.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        cancelled : `bool`
            Whether the respective gateway was closed.
        """
        now = LOOP_TIME()
        if now >= self.resets_at:
            self.resets_at = now+GATEWAY_RATE_LIMIT_RESET
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            remaining = self.remaining
        
        if remaining:
            self.remaining = remaining-1
            return False
        
        if self.wake_upper is None:
            self.wake_upper = KOKORO.call_at(self.resets_at, type(self).wake_up, self)
        
        future = Future(KOKORO)
        self.queue.append(future)
        return (yield from future)
    
    __await__ = __iter__
    
    
    def wake_up(self):
        """
        Wake ups the waiting futures of the ``GatewayRateLimiter``.
        """
        queue = self.queue
        remaining = GATEWAY_RATE_LIMIT_LIMIT
        if queue:
            while True:
                if not queue:
                    wake_upper = None
                    break
                
                if not remaining:
                    self.resets_at = resets_at = LOOP_TIME() + GATEWAY_RATE_LIMIT_RESET
                    wake_upper = KOKORO.call_at(resets_at + GATEWAY_RATE_LIMIT_RESET, type(self).wake_up, self)
                    break
                
                queue.popleft().set_result_if_pending(False)
                remaining -= 1
        
        else:
            wake_upper = None
        
        self.wake_upper = wake_upper
        self.remaining = remaining
    
    
    def cancel(self):
        """
        Cancels the ``GatewayRateLimiter``'s queue and it's `.wake_upper` if set.
        """
        queue = self.queue
        while queue:
            queue.popleft().set_result_if_pending(True)
        
        wake_upper = self.wake_upper
        if (wake_upper is not None):
            self.wake_upper = None
            wake_upper.cancel()
    
    
    def __repr__(self):
        """Returns the gateway rate limiter's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        resets_at = self.resets_at
        if resets_at <= LOOP_TIME():
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            repr_parts.append(' resets_at=')
            repr_parts.append(repr(LOOP_TIME()))
            repr_parts.append(' (monotonic),')
            
            remaining = self.remaining
        
        repr_parts.append(' remaining=')
        repr_parts.append(repr(remaining))
        repr_parts.append('>')
        
        return ''.join(repr_parts)
