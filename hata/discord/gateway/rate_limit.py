__all__ = ()

from collections import deque

from scarletio import Future, LOOP_TIME, RichAttributeErrorBaseType

from ..core import KOKORO

from .constants import GATEWAY_RATE_LIMIT_LIMIT, GATEWAY_RATE_LIMIT_RESET


class GatewayRateLimiter(RichAttributeErrorBaseType):
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
    wake_up_handle : `None`  or ``TimerHandle``
        A handler what will reset the limiter's limit and ensure it's queue if needed.
    """
    __slots__ = ('queue', 'remaining', 'resets_at', 'wake_up_handle')
    
    def __new__(cls):
        """
        Creates a gateway rate limiter.
        """
        self = object.__new__(cls)
        self.remaining = GATEWAY_RATE_LIMIT_LIMIT
        self.queue = deque()
        self.wake_up_handle = None
        self.resets_at = 0.0
        return self
    
    
    def __repr__(self):
        """Returns the gateway rate limiter's representation."""
        repr_parts = ['<', type(self).__name__,]
        
        resets_at = self.resets_at
        if resets_at <= LOOP_TIME():
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            repr_parts.append(' resets_at = ')
            repr_parts.append(format(resets_at, '.2f'))
            repr_parts.append(' (monotonic),')
            
            remaining = self.remaining
        
        repr_parts.append(', remaining = ')
        repr_parts.append(repr(remaining))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __iter__(self):
        """
        Awaits the rate limit handler.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        success : `bool`
            Whether the action can be executed.
            Returns `False` if the gateway was closed and no action should be executed.
        """
        now = LOOP_TIME()
        if now >= self.resets_at:
            self.resets_at = now + GATEWAY_RATE_LIMIT_RESET
            remaining = GATEWAY_RATE_LIMIT_LIMIT
        else:
            remaining = self.remaining
        
        if remaining:
            self.remaining = remaining - 1
            return True
        
        if self.wake_up_handle is None:
            self.wake_up_handle = KOKORO.call_at(self.resets_at, type(self).wake_up, self)
        
        future = Future(KOKORO)
        self.queue.append(future)
        return (yield from future)
    
    
    __await__ = __iter__
    
    
    def wake_up(self):
        """
        Wake ups the waiting futures of the gateway rate limiter.
        """
        queue = self.queue
        remaining = GATEWAY_RATE_LIMIT_LIMIT
        if not queue:
            wake_up_handle = None
        
        else:
            while True:
                if not queue:
                    wake_up_handle = None
                    break
                
                if not remaining:
                    self.resets_at = resets_at = LOOP_TIME() + GATEWAY_RATE_LIMIT_RESET
                    wake_up_handle = KOKORO.call_at(resets_at + GATEWAY_RATE_LIMIT_RESET, type(self).wake_up, self)
                    break
                
                # if the future is already done (expectedly cancelled) `.set_result_if_pending` returns `0`.
                # At that case we do not want to decrease `remaining`.
                if queue.popleft().set_result_if_pending(True):
                    remaining -= 1
        
        self.wake_up_handle = wake_up_handle
        self.remaining = remaining
    
    
    def cancel(self):
        """
        Cancels the gateway rate limiter's queue and it's `.wake_up_handle` if set.
        """
        queue = self.queue
        while queue:
            queue.popleft().set_result_if_pending(False)
        
        wake_up_handle = self.wake_up_handle
        if (wake_up_handle is not None):
            self.wake_up_handle = None
            wake_up_handle.cancel()
