__all__ = ('ActivityTimestamps',)

from scarletio import copy_docs

from ...utils import DATETIME_FORMAT_CODE

from ..activity_field_base import ActivityFieldBase

from .fields import parse_end, parse_start, put_end_into, put_start_into, validate_end, validate_start


class ActivityTimestamps(ActivityFieldBase):
    """
    Represents an activity's timestamp field.
    
    Attributes
    ----------
    end : `None`, `datetime`
        When the activity ends.
    start : `None`, `datetime`
       When the activity starts.
    """
    __slots__ = ('end', 'start',)
    
    def __new__(cls, *, end = ..., start = ...):
        """
        Creates a new activity timestamp with the given parameters.
        
        Parameters
        ----------
        end : `None`, `datetime`, Optional (Keyword only)
            When the activity ends. 
        start : `None`, `datetime`, Optional (Keyword only)
           When the activity starts.
       
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # end
        if end is ...:
            end = None
        else:
            end = validate_end(end)
        
        # start
        if start is ...:
            start = None
        else:
            start = validate_start(start)
        
        # Construct
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.start = parse_start(data)
        self.end = parse_end(data)
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_end_into(self.end, data, defaults)
        put_start_into(self.start, data, defaults)
        return data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        start = self.start
        if (start is not None):
            repr_parts.append(' start = ')
            repr_parts.append(format(start, DATETIME_FORMAT_CODE))
            field_added = True
        else:
            field_added = False
        
        end = self.end
        if (end is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' end = ')
            repr_parts.append(format(start, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.end != other.end:
            return False
        
        if self.start != other.start:
            return False
        
        return True
    
    
    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        end = self.end
        if (end is not None):
            hash_value ^= hash(end)
            hash_value ^= (1 << 0)
        
        start = self.start
        if (start is not None):
            hash_value ^= hash(start)
            hash_value ^= (1 << 4)
        
        return hash_value


    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        end = self.end
        if (end is not None):
            return True
        
        start = self.start
        if (start is not None):
            return True
        
        return False
    
    
    @copy_docs(ActivityFieldBase.copy)
    def copy(self):
        new  = object.__new__(type(self))
        new.end = self.end
        new.start = self.start
        return new
    
    
    def copy_with(self, *, end = ..., start = ...):
        """
        Copies the activity timestamp with the given fields.
        
        Parameters
        ----------
        end : `None`, `datetime`, Optional (Keyword only)
            When the activity ends. 
        start : `None`, `datetime`, Optional (Keyword only)
           When the activity starts.
        
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
        # end
        if end is ...:
            end = self.end
        else:
            end = validate_end(end)
        
        # start
        if start is ...:
            start = self.start
        else:
            start = validate_start(start)
        
        # Construct
        new = object.__new__(type(self))
        new.start = start
        new.end = end
        return new
