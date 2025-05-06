__all__ = ('EventBase', )

from scarletio import RichAttributeErrorBaseType


class EventBase(RichAttributeErrorBaseType):
    """
    Base class for events.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new event instance.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new event instance from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Reaction event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_fields(cls):
        """
        Creates a event instance from the given fields.
        
        Returns
        -------
        new : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the event base into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        return {}
    
    
    def __repr__(self):
        """Returns the event's representation."""
        return f'<{type(self).__name__}>'
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 0
    
    
    def __iter__(self):
        """
        Unpacks the event.
        
        This method is an iterable generator.
        """
        return
        yield
    
    
    def __eq__(self, other):
        """Returns whether the two events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the event's hash."""
        return 0
