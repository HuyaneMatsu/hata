__all__ = ('AutoModerationRuleTriggerMetadataBase', )

from scarletio import RichAttributeErrorBaseType


class AutoModerationRuleTriggerMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``AutoModerationRule``'s trigger metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new trigger metadata instance.
        """
        return object.__new__(cls)
        
    def __repr__(self):
        """Returns the trigger metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new auto moderation rule trigger metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Auto moderation rule trigger metadata payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self):
        """
        Converts the trigger metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two trigger metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the trigger metadata's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the trigger metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))

