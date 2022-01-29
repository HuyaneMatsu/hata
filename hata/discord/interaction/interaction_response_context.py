__all__ = ('InteractionResponseContext',)

from scarletio import Task, to_coroutine

from ..core import KOKORO


RESPONSE_FLAG_DEFERRING = 1 << 0
RESPONSE_FLAG_DEFERRED = 1 << 1
RESPONSE_FLAG_RESPONDING = 1 << 2
RESPONSE_FLAG_RESPONDED = 1 << 3
RESPONSE_FLAG_EPHEMERAL = 1 << 4

RESPONSE_FLAG_NONE = 0
RESPONSE_FLAG_ACKNOWLEDGING = RESPONSE_FLAG_DEFERRING | RESPONSE_FLAG_RESPONDING
RESPONSE_FLAG_ACKNOWLEDGED = RESPONSE_FLAG_DEFERRED | RESPONSE_FLAG_RESPONDED
RESPONSE_FLAG_DEFERRING_OR_DEFERRED = RESPONSE_FLAG_DEFERRING | RESPONSE_FLAG_DEFERRED
RESPONSE_FLAG_RESPONDING_OR_RESPONDED = RESPONSE_FLAG_RESPONDING | RESPONSE_FLAG_RESPONDED
RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED = RESPONSE_FLAG_ACKNOWLEDGING | RESPONSE_FLAG_ACKNOWLEDGED


class InteractionResponseContext:
    """
    Interaction response context manager for managing the interaction event's response flag.
    
    Attributes
    ----------
    interaction_event : ``InteractionEvent``
        The respective interaction event event.
    is_deferring : `bool`
        Whether the request just deferring the interaction event.
    is_ephemeral : `bool`
        Whether the request is ephemeral.
    """
    __slots__ = ('interaction_event', 'is_deferring', 'is_ephemeral',)
    
    def __new__(cls, interaction_event, is_deferring, is_ephemeral):
        """
        Creates a new ``InteractionResponseContext`` with the given parameters.
        
        Parameters
        ----------
        is_deferring : `bool`
            Whether the request just deferring the interaction event.
        is_ephemeral : `bool`
            Whether the request is ephemeral.
        """
        self = object.__new__(cls)
        self.interaction_event = interaction_event
        self.is_deferring = is_deferring
        self.is_ephemeral = is_ephemeral
        return self
    
    
    @to_coroutine
    def ensure(self, coroutine):
        """
        Ensures the coroutine within the interaction response context
        
        This method is an awaitable generator.
        
        Parameters
        ----------
        coroutine : ``CoroutineType``
        """
        self.interaction_event._async_task = Task(self._async(coroutine), KOKORO)
        yield # skip a ready cycle
    
    
    async def _async(self, coroutine):
        """
        Ensures the coroutine within the interaction response context. Wrapped into a task by ``.ensure``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        coroutine : ``CoroutineType``
        """
        try:
            
            async with self:
                await coroutine
        
        finally:
            self.interaction_event._async_task = None
    
    
    async def __aenter__(self):
        """
        Enters the context manager as deferring or responding if applicable.
        
        This method is a coroutine.
        """
        interaction_event = self.interaction_event
        await interaction_event._wait_for_async_task_completion()
        
        response_flag = interaction_event._response_flag
        
        if self.is_deferring:
            if not (response_flag & RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED):
                response_flag |= RESPONSE_FLAG_DEFERRING
        else:
            if (
                (not response_flag & RESPONSE_FLAG_RESPONDING_OR_RESPONDED) and
                (not response_flag & RESPONSE_FLAG_DEFERRING_OR_DEFERRED)
            ):
                response_flag |= RESPONSE_FLAG_RESPONDING
        
        interaction_event._response_flag = response_flag
        
        return self
    
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager, marking the interaction event as deferred or responded if no exception occurred.
        
        This method is a coroutine.
        """
        interaction_event = self.interaction_event
        response_flag = interaction_event._response_flag
        if exc_type is None:
            if self.is_ephemeral:
                if not response_flag & RESPONSE_FLAG_ACKNOWLEDGED:
                    response_flag ^= RESPONSE_FLAG_EPHEMERAL
            
            if self.is_deferring:
                if response_flag & RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
                    response_flag |= RESPONSE_FLAG_DEFERRED
            else:
                if response_flag & RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
                    response_flag |= RESPONSE_FLAG_RESPONDED
        
        else:
            if self.is_deferring:
                if response_flag & RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
            else:
                if response_flag & RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
        
        interaction_event._response_flag = response_flag
        return False
