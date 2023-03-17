__all__ = ('ScheduledEventEntityMetadataLocation',)

from scarletio import copy_docs

from .base import ScheduledEventEntityMetadataBase
from .fields import parse_location, put_location_into, validate_location


class ScheduledEventEntityMetadataLocation(ScheduledEventEntityMetadataBase):
    """
    Location entity metadata of ``ScheduledEvent``-s.
    
    Attributes
    ----------
    location : `None`, `str`
        The place where the event will take place.
    """
    __slots__ = ('location', )
    
    @copy_docs(ScheduledEventEntityMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # location
        try:
            location = keyword_parameters.pop('location')
        except KeyError:
            location = None
        else:
            location = validate_location(location)
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.location = parse_location(data)
        return self
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_location_into(self.location, data, defaults)
        return data
    
    
    @classmethod
    def _create_empty(cls):
        self = object.__new__(cls)
        self.location = None
        return self
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        location = self.location
        if (location is not None):
            hash_value ^= hash(location)
        
        return hash_value
    
    
    @copy_docs(ScheduledEventEntityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.location != other.location:
            return False
        
        return True
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.location = self.location
        return new
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.copy)
    def copy_with(self, keyword_parameters):
        # location
        try:
            location = keyword_parameters.pop('location')
        except KeyError:
            location = self.location
        else:
            location = validate_location(location)
        
        new = object.__new__(type(self))
        new.location = location
        return new
