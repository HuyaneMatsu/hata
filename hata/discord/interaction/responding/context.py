__all__ = ('InteractionResponseContext',)

from scarletio import Task, to_coroutine

from ...core import KOKORO

from .constants import (
    RESPONSE_FLAG_ACKNOWLEDGED, RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED, RESPONSE_FLAG_DEFERRED,
    RESPONSE_FLAG_DEFERRING, RESPONSE_FLAG_EPHEMERAL, RESPONSE_FLAG_RESPONDED, RESPONSE_FLAG_RESPONDING,
    RESPONSE_FLAG_RESPONDING_OR_RESPONDED
)


class InteractionResponseContext:
    """
    Interaction response context manager for managing the interaction event's response flag.
    
    Attributes
    ----------
    interaction_event : ``InteractionEvent``
        The respective interaction event event.
    
    deferring : `bool`
        Whether the request just deferring the interaction event.
    
    ephemeral : `bool`
        Whether the request is ephemeral.
    """
    __slots__ = ('interaction_event', 'deferring', 'ephemeral',)
    
    def __new__(cls, interaction_event, deferring, ephemeral):
        """
        Creates a new ``InteractionResponseContext`` with the given parameters.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The interaction event to which wew are responding to.
        
        deferring : `bool`
            Whether the request just deferring the interaction event.
        
        ephemeral : `bool`
            Whether the request is ephemeral.
        """
        self = object.__new__(cls)
        self.interaction_event = interaction_event
        self.deferring = deferring
        self.ephemeral = ephemeral
        return self
    
    
    def __repr__(self):
        """Returns the interaction response context's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self.deferring:
            repr_parts.append(' deferring')
        
        if self.ephemeral:
            repr_parts.append(' (ephemeral)')
        
        repr_parts.append(' interaction_event=')
        repr_parts.append(repr(self.interaction_event))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the interaction response context's hash value."""
        hash_value = 0
        
        # deferring
        hash_value ^= self.deferring << 2
        
        # ephemeral
        hash_value ^= self.ephemeral << 6
        
        # interaction_event
        hash_value ^= hash(self.interaction_event)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two interaction response contexts are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # deferring
        if self.deferring != other.deferring:
            return False
        
        # ephemeral
        if self.ephemeral != other.ephemeral:
            return False
        
        # interaction_event
        if self.interaction_event != other.interaction_event:
            return False
        
        return True
    
    
    @to_coroutine
    def ensure(self, coroutine):
        """
        Ensures the coroutine within the interaction response context
        
        This method is an awaitable generator.
        
        Parameters
        ----------
        coroutine : ``CoroutineType``
        """
        self.interaction_event._async_task = Task(KOKORO, self._async(coroutine))
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
        
        if self.deferring:
            if not (response_flag & RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED):
                response_flag |= RESPONSE_FLAG_DEFERRING
        else:
            if (not response_flag & RESPONSE_FLAG_RESPONDING_OR_RESPONDED):
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
            if self.ephemeral:
                if not response_flag & RESPONSE_FLAG_ACKNOWLEDGED:
                    response_flag ^= RESPONSE_FLAG_EPHEMERAL
            
            if self.deferring:
                if response_flag & RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
                    response_flag |= RESPONSE_FLAG_DEFERRED
            else:
                if response_flag & RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
                    response_flag |= RESPONSE_FLAG_RESPONDED
                    
                    if response_flag & RESPONSE_FLAG_DEFERRED:
                        response_flag ^= RESPONSE_FLAG_DEFERRED
        
        else:
            if self.deferring:
                if response_flag & RESPONSE_FLAG_DEFERRING:
                    response_flag ^= RESPONSE_FLAG_DEFERRING
            else:
                if response_flag & RESPONSE_FLAG_RESPONDING:
                    response_flag ^= RESPONSE_FLAG_RESPONDING
        
        interaction_event._response_flag = response_flag
        return False
