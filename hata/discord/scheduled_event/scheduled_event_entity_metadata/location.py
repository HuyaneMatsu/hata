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
    
    
    def __new__(cls, *, location = ...):
        """
        Creates a new entity metadata instance.
        
        Parameters
        ----------
        location : `None`, `str`, Optional (Keyword only)
            The place where the event will take place.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # location
        if location is ...:
            location = None
        else:
            location = validate_location(location)
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            location = keyword_parameters.pop('location', ...),
        )
    
    
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
    
    
    def copy_with(self, *, location = ...):
        """
        Copies the scheduled event entity metadata with the given fields.
        
        Parameters
        ----------
        location : `None`, `str`, Optional (Keyword only)
            The place where the event will take place.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # location
        if location is ...:
            location = self.location
        else:
            location = validate_location(location)
        
        new = object.__new__(type(self))
        new.location = location
        return new

    
    @copy_docs(ScheduledEventEntityMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            location = keyword_parameters.pop('location', ...),
        )
