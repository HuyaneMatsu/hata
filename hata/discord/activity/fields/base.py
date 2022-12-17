__all__ = ('ActivityFieldBase',)

from scarletio import RichAttributeErrorBaseType


class ActivityFieldBase(RichAttributeErrorBaseType):
    """
    Base class for activity fields.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new activity field.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new activity field from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Activity field data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self):
        """
        Serializes the activity field.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __repr__(self):
        """Returns the activity field's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __eq__(self, other):
        """Returns whether the two activity fields are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the activity field's hash value."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the activity field has any non-default attribute set."""
        return False
