__all__ = ('ScheduledEventEntityMetadataLocation',)

from scarletio import copy_docs

from .base import ScheduledEventEntityMetadataBase


class ScheduledEventEntityMetadataLocation(ScheduledEventEntityMetadataBase):
    """
    Location entity metadata of ``ScheduledEvent``-s.
    
    Attributes
    ----------
    location : `None`, `str`
        The place where the event will take place.
    """
    __slots__ = ('location', )
    
    def __new__(cls, location):
        """
        Creates a new location entity metadata for ``ScheduledEvent``-s.
        
        Parameters
        ----------
        location : `str`
            The location.
        
        Raises
        ------
        TypeError
            If `location`'s type is incorrect.
        ValueError
            If `location` is an empty string.
        """
        if not isinstance(location, str):
            raise TypeError(
                f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
            )
        
        if not location:
            raise ValueError(
                f'`location` cannot be empty string.'
            )
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadataBase.from_data)
    def from_data(cls, data):
        location = data.get('location', None)
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadataBase.to_data)
    def to_data(self):
        return {
            'location': self.location,
        }
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.location != other.location:
            return False
        
        return True
    
    @copy_docs(ScheduledEventEntityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        location = self.location
        if (location is not None):
            hash_value ^= hash(location)
        
        return hash_value
