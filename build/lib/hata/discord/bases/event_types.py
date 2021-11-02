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
        
        This method is a generator.
        """
        return
        yield # This is intentional. Python stuff... Do not ask, just accept.
