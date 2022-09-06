__all__ = ('ActivityTimestamps',)

from datetime import datetime

from scarletio import copy_docs

from ...utils import DATETIME_FORMAT_CODE, datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime

from .base import ActivityFieldBase


def _assert__activity_timestamp__start(start):
    """
    Asserts the `start` parameter of ``ActivityTimestamps.__new__`` method.
    
    Parameters
    ----------
    start : `None`, `datetime`
       When the activity starts.
    
    Raises
    ------
    AssertionError
        - If `start` is not `None`, `datetime`.
    """
    if (start is not None) and (not isinstance(start, datetime)):
        raise AssertionError(
            f'`start` can be `None`, `datetime`, got {start.__class__.__name__}; {start!r}.'
        )
    
    return True


def _assert__activity_timestamp__end(end):
    """
    Asserts the `end` parameter of ``ActivityTimestamps.__new__`` method.
    
    Parameters
    ----------
    end : `None`, `datetime`
        When the activity ends.
    
    Raises
    ------
    AssertionError
        - If `end` is not `None`, `datetime`.
    """
    if (end is not None) and (not isinstance(end, datetime)):
        raise AssertionError(
            f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
        )
    
    return True


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
    
    def __new__(cls, *, start=None, end=None):
        """
        Creates a new activity timestamp with the given parameters.
        
        Parameters
        ----------
        end : `None`, `datetime` = `None`, Optional (Keyword only)
            When the activity ends. 
        start : `None`, `datetime` = `None`, Optional (Keyword only)
           When the activity starts.
        """
        assert _assert__activity_timestamp__start(start)
        assert _assert__activity_timestamp__end(end)
        
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    @classmethod
    @copy_docs(ActivityFieldBase.from_data)
    def from_data(cls, timestamps_data):
        start = timestamps_data.get('start', None)
        if (start is not None):
            start = millisecond_unix_time_to_datetime(start)
        
        end = timestamps_data.get('end', None)
        if (end is not None):
            end = millisecond_unix_time_to_datetime(end)
        
        self = object.__new__(cls)
        self.start = start
        self.end = end
        return self
    
    
    @copy_docs(ActivityFieldBase.to_data)
    def to_data(self):
        timestamps_data = {}
        
        start = self.start
        if (start is not None):
            timestamps_data['start'] = datetime_to_millisecond_unix_time(start)
        
        end = self.end
        if (end is not None):
            timestamps_data['end'] = datetime_to_millisecond_unix_time(end)
        
        return timestamps_data
    
    
    @copy_docs(ActivityFieldBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        start = self.start
        if (start is not None):
            repr_parts.append(' start=')
            repr_parts.append(start.__format__(DATETIME_FORMAT_CODE))
            field_added = True
        else:
            field_added = False
        
        end = self.end
        if (end is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' end=')
            repr_parts.append(start.__format__(DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityFieldBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.start != other.start:
            return False
        
        if self.end != other.end:
            return False
        
        return True
    
    
    @copy_docs(ActivityFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        start = self.start
        if (start is not None):
            hash_value ^= hash(start)
            hash_value ^= (1 << 0)
        
        end = self.end
        if (end is not None):
            hash_value ^= hash(end)
            hash_value ^= (1 << 4)
        
        return hash_value


    @copy_docs(ActivityFieldBase.__bool__)
    def __bool__(self):
        start = self.start
        if (start is not None):
            return True
        
        end = self.end
        if (end is not None):
            return True
        
        return False
