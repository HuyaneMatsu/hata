__all__ = ('EventBase', )

class EventBase:
    """
    Base class for events.
    """
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        return None
    
    
    def __repr__(self):
        """Returns the event's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 0
    
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is an iterable generator.
        """
        return
        yield # This is intentional. Python stuff... Do not ask, just accept.
    
    
    def __eq__(self, other):
        """Returns whether the two events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the event's hash."""
        return 0
