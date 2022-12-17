__all__ = ('ScheduledEventEntityMetadataBase',)

from scarletio import RichAttributeErrorBaseType


class ScheduledEventEntityMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``ScheduledEvent``'s entity metadata.
    """
    __slots__ = ()
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new entity metadata instance.
        """
        raise NotImplementedError
        
    def __repr__(self):
        """Returns the entity metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event entity metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity metadata structure.
        
        Returns
        -------
        self : `instance<cls>`
        """
        raise NotImplementedError
    
    
    def to_data(self):
        """
        Converts the entity metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two entity metadatas equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the entity metadata's hash value."""
        return 0
