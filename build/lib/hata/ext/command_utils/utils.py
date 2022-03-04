__all__ = ('Timeouter', 'multievent', )

from scarletio import LOOP_TIME

from ...discord.core import KOKORO

class multievent:
    """
    Helper class to hold more waitfor event handlers together allowing to add `target` - `waiter` pairs at the same to
    more.
    
    Attributes
    ----------
    events : `tuple` of `Any`
        A `tuple` of the contained event handlers.
    """
    __slots__ = ('events',)
    
    def __init__(self, *events):
        """
        Creates a ``multievent`` with the given event handlers
        
        Parameters
        ----------
        *events : `Any`
            The event handlers to hold together.
        """
        self.events = events
    
    
    def append(self, target, waiter):
        """
        Adds the given `target` - `waiter` pair to the contained event handlers.
        
        Parameters
        ----------
        target : ``DiscordEntity``
        waiter : `async callable`
        """
        for event in self.events:
            event.append(target, waiter)
    
    
    def remove(self, target, waiter):
        """
        Removes the given `target` - `waiter` pair to the contained event handlers.
        
        Parameters
        ----------
        target : ``DiscordEntity``
        waiter : `async callable`
        """
        for event in self.events:
            event.remove(target, waiter)


class Timeouter:
    """
    Executes timing out feature on ``Pagination`` and on other familiar types.
    
    Attributes
    ----------
    handle : `None`, ``TimerHandle``
        Handle to wake_up the timeouter with it's `._step` function.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    owner : `Any`
        The object what uses the timeouter.
        Set to `None`, when the respective timeout is over or if the timeout is cancelled.
    timeout : `float`
        The time with what the timeout will be expired when it's current waiting cycle is over.
    """
    __slots__ = ('handle', 'owner', 'timeout')
    
    def __init__(self, owner, timeout):
        """
        Creates a new ``Timeouter`` with the given `owner` and `timeout`.
        
        Parameters
        ----------
        owner : `Any`
            The object what uses the timeouter.
        timeout : `float`
            The time with what the timeout will be expired when it's current waiting cycle is over.
        """
        self.owner = owner
        self.timeout = 0.0
        self.handle = KOKORO.call_later(timeout, type(self)._step, self)
    
    
    def _step(self):
        """
        Executes a timeouter cycle.
        
        Increases the timeout if ``.timeout`` was updated. If not and applicable, calls it's ``.owner``'s
        `.canceller` with `TimeoutError` and unlinks ``.owner`` and `owner.canceller`,
        """
        timeout = self.timeout
        if timeout > 0.0:
            self.handle = KOKORO.call_later(timeout, type(self)._step, self)
            self.timeout = 0.0
            return
        
        self.handle = None
        owner = self.owner
        if owner is None:
            return
        
        self.owner = None
        
        owner.cancel(TimeoutError())
    
    
    def cancel(self):
        """
        Cancels the timeouter.
        
        Should be called by the timeouter's owner when it is cancelled with an other exception.
        """
        handle = self.handle
        if handle is None:
            return
        
        self.handle = None
        handle.cancel()
        self.owner = None
    
    
    def set_timeout(self, value):
        """
        Sets the timeouter of the timeouter to the given value.
        """
        handle = self.handle
        if handle is None:
            # Cannot change timeout of expired timeouter
            return
        
        if value <= 0.0:
            self.timeout = 0.0
            handle._run()
            handle.cancel()
            return
        
        now = LOOP_TIME()
        next_step = self.handle.when
        
        planed_end = now + value
        if planed_end < next_step:
            handle.cancel()
            self.handle = KOKORO.call_at(planed_end, type(self)._step, self)
            return
        
        self.timeout = planed_end - next_step
    
    
    def get_expiration_delay(self):
        """
        Returns after how much time the timeouter will expire.
        
        If the timeouter already expired, returns `0.0˙.
        
        Returns
        -------
        time_left : `float`
        """
        handle = self.handle
        if handle is None:
            return 0.0
        
        return handle.when - LOOP_TIME() + self.timeout
