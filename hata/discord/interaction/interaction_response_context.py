__all__ = ('InteractionResponseContext',)

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
    Interaction response context manager for managing the interaction's response flag.
    
    Attributes
    ----------
    interaction : ``InteractionEvent``
        The respective interaction event.
    is_deferring : `bool`
        Whether the request just deferring the interaction.
    is_ephemeral : `bool`
        Whether the request is ephemeral.
    """
    __slots__ = ('interaction', 'is_deferring', 'is_ephemeral',)
    
    def __new__(cls, interaction, is_deferring, is_ephemeral):
        """
        Creates a new ``InteractionResponseContext`` with the given parameters.
        
        Parameters
        ----------
        is_deferring : `bool`
            Whether the request just deferring the interaction.
        is_ephemeral : `bool`
            Whether the request is ephemeral.
        """
        self = object.__new__(cls)
        self.interaction = interaction
        self.is_deferring = is_deferring
        self.is_ephemeral = is_ephemeral
        return self
    
    def __enter__(self):
        """Enters the context manager as deferring or responding if applicable."""
        interaction = self.interaction
        response_flag = interaction._response_flag
        
        if self.is_deferring:
            if not (response_flag & RESPONSE_FLAG_ACKNOWLEDGING_OR_ACKNOWLEDGED):
                response_flag |= RESPONSE_FLAG_DEFERRING
        else:
            if (
                (not response_flag & RESPONSE_FLAG_RESPONDING_OR_RESPONDED) and
                (not response_flag & RESPONSE_FLAG_DEFERRING_OR_DEFERRED)
            ):
                response_flag |= RESPONSE_FLAG_RESPONDING
        
        interaction._response_flag = response_flag
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context manager, marking the interaction as deferred or responded if no exception occurred."""
        interaction = self.interaction
        response_flag = interaction._response_flag
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
        
        interaction._response_flag = response_flag
        return False
