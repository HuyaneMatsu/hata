__all__ = ('InteractionFieldBase',)

class InteractionFieldBase:
    """
    Base class for values assigned to ``InteractionEvent.interaction`` field.
    """
    __slots__ = ()
    
    def __new__(cls, data, interaction_event):
        """
        Creates a new interaction field from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The received interaction field data.
        interaction_event : ``InteractionEvent``
            The parent interaction event.
        """
        return None
    
    
    def __repr__(self):
        """Returns the interaction field's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the interaction field hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two interaction field are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return False
