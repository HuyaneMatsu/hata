__all__ = ()

from scarletio import ScarletLock, RichAttributeErrorBaseType, copy_docs

from ...discord.core import KOKORO


class RateLimitContextBase(RichAttributeErrorBaseType):
    """
    Rate limit context used to handle static rate limits when communicating with top.gg.
    
    Attributes
    ----------
    acquired : `bool`
        Whether the lock is acquired.
    """
    __slots__ = ('acquired', )
    
    def __new__(cls):
        """
        Creates a new rate limit context instance.
        """
        self = object.__new__(cls)
        self.acquired = False
        return self
    
    
    async def __aenter__(self):
        """
        Enters the rate limit context, blocking till acquiring it.
        
        This method is a coroutine.
        """
        self.acquired = True
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the rate limit context.
        
        This method is a coroutine.
        """
        self.release()
        return False
        
    
    def __del__(self):
        """Releases the rate limit context if not yet released."""
        self.release()
    
    
    def release(self):
        """Releases the rate limit context."""
        self.acquired = False


class RateLimitContext(RateLimitContextBase):
    """
    Rate limit context used to handle static rate limits when communicating with top.gg.
    
    Attributes
    ----------
    acquired : `bool`
        Whether the lock is acquired.
    rate_limit_group : ``RateLimitGroup``
        The parent rate limit group.
    """
    __slots__ = ('rate_limit_group',)
    
    def __new__(cls, rate_limit_group):
        """
        Creates a new rate limit context instance.
        
        Parameters
        ----------
        rate_limit_group : ``RateLimitGroup``
            The parent rate limit group.
        """
        self = object.__new__(cls)
        self.rate_limit_group = rate_limit_group
        self.acquired = False
        return self
    
    
    @copy_docs(RateLimitContextBase.__aenter__)
    async def __aenter__(self):
        await self.rate_limit_group.lock.acquire()
        self.acquired = True
        return self
    
    
    @copy_docs(RateLimitContextBase.release)
    def release(self):
        if self.acquired:
            rate_limit_group = self.rate_limit_group
            KOKORO.call_later(rate_limit_group.reset_after, rate_limit_group.lock.release)
            self.acquired = False


class StackedRateLimitContext(RateLimitContextBase):
    """
    Rate limit context used to handle multiple static rate limits when communicating with top.gg.
    
    Attributes
    ----------
    acquired : `bool`
        Whether the lock is acquired.
    rate_limit_groups : `tuple` of ``RateLimitGroup``
        The parent rate limit groups.
    """
    __slots__ = ('rate_limit_groups',)
    
    def __new__(cls, rate_limit_groups):
        """
        Creates a new rate limit context instance.
        
        Parameters
        ----------
        rate_limit_groups : `tuple` of ``RateLimitGroup``
            The parent rate limit groups.
        """
        self = object.__new__(cls)
        self.rate_limit_groups = rate_limit_groups
        self.acquired = False
        return self
    
    
    @copy_docs(RateLimitContextBase.__aenter__)
    async def __aenter__(self):
        # Use linear acquiring.
        for rate_limit_group in self.rate_limit_groups:
            try:
                await rate_limit_group.lock.acquire()
            except:
                # If already acquired, release on cancellation
                for rate_limit_group_to_cancel in self.rate_limit_groups:
                    if rate_limit_group is rate_limit_group_to_cancel:
                        break
                    
                    rate_limit_group_to_cancel.lock.release()
                    continue
                
                raise
        
        self.acquired = True
        return self
    
    
    @copy_docs(RateLimitContextBase.release)
    def release(self):
        if self.acquired:
            for rate_limit_group in self.rate_limit_groups:
                KOKORO.call_later(rate_limit_group.reset_after, rate_limit_group.lock.release)
            
            self.acquired = False


class RateLimitHandlerBase(RichAttributeErrorBaseType):
    """
    Rate limit handler which can be entered.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new rate limit handler instance.
        """
        return object.__new__(cls)
    
    def ctx(self):
        """
        Enters the rate limit handler, allowing it to be used as an asynchronous context manager.
        
        Returns
        -------
        rate_limit_context : ``RateLimitContextBase``
        """
        return RateLimitContextBase()


class RateLimitHandler(RateLimitHandlerBase):
    """
    Rate limit handler which can be entered.
    
    Attributes
    ----------
    rate_limit_group : ``RateLimitGroup``
        The wrapped rate limit group.
    """
    __slots__ = ('rate_limit_group',)
    
    def __new__(cls, rate_limit_group):
        """
        Creates a new rate limit handler instance with the given rate limit group.
        
        Parameters
        ----------
        rate_limit_group : ``RateLimitGroup``
            The parent rate limit group.
        """
        self = object.__new__(cls)
        self.rate_limit_group = rate_limit_group
        return self
    
    
    @copy_docs(RateLimitHandlerBase.ctx)
    def ctx(self):
        return RateLimitContext(self.rate_limit_group)


class StackedRateLimitHandler(RateLimitHandlerBase):
    """
    Rate limit handler which can be entered.
    
    Attributes
    ----------
    rate_limit_groups : `tuple` of ``RateLimitGroup``
        The wrapped rate limit group.
    """
    __slots__ = ('rate_limit_groups',)
    
    def __new__(cls, *rate_limit_groups):
        """
        Creates a new rate limit handler instance with the given rate limit group.
        
        Parameters
        ----------
        *rate_limit_groups : ``RateLimitGroup``
            The parent rate limit groups.
        """
        self = object.__new__(cls)
        self.rate_limit_groups = rate_limit_groups
        return self
    
    
    @copy_docs(RateLimitHandlerBase.ctx)
    def ctx(self):
        return StackedRateLimitContext(self.rate_limit_groups)


class RateLimitGroup(RichAttributeErrorBaseType):
    """
    Static rate limit handler group implementation.
    
    Attributes
    ----------
    lock : ``ScarletLock``
        Lock used to block requests.
    reset_after : `int`
        Duration to release a rate limit after.
    """
    __slots__ = ('lock', 'reset_after', )
    
    def __new__(cls, size, reset_after):
        """
        Creates a new rate limit handler instance.
        
        Parameters
        ----------
        size : `int`
            Rate limit size.
        reset_after : `float`
            The time to reset rate limit after.
        """
        self = object.__new__(cls)
        self.reset_after = reset_after
        self.lock = ScarletLock(KOKORO, size)
        return self
