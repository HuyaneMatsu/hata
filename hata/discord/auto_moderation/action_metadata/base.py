__all__ = ('AutoModerationActionMetadataBase',)

from scarletio import RichAttributeErrorBaseType


class AutoModerationActionMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``AutoModerationAction``'s action metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new action metadata instance.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the action metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new auto moderation action metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
           Auto moderation action metadata payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self):
        """
        Converts the action metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two action metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the action metadata's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the action metadata.
        
        Returns
        -------
        new : `instance<cls>`
        """
        return object.__new__(type(self))
