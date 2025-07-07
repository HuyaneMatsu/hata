__all__ = ('ScheduledEventOccasionOverwrite',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DISCORD_EPOCH_START

from .fields import (
    parse_cancelled, parse_end, parse_start, parse_timestamp, put_cancelled, put_end, put_start, put_timestamp,
    validate_cancelled, validate_end, validate_start, validate_timestamp
)


class ScheduledEventOccasionOverwrite(RichAttributeErrorBaseType):
    """
    Represents a scheduled event occasion overwrite.
    
    Attributes
    ----------
    cancelled : `bool`
        Whether the occasion is cancelled.
    
    end : `None | DateTime`
        New end of the occasion.
    
    start : `None | DateTime`
        New start of the occasion.
    
    timestamp : `DateTime`
        The affected occasion.
    """
    __slots__ = ('cancelled', 'end', 'start', 'timestamp', )
    
    
    def __new__(cls, *, cancelled = ..., end = ..., start = ..., timestamp = ...):
        """
        Creates a new scheduled event occasion overwrite.
        
        Parameters
        ----------
        cancelled : `None | bool``, Optional (Keyword only)
            Whether the occasion is cancelled.
        
        end : `None | DateTime``, Optional (Keyword only)
            New end of the occasion.
        
        start : `None | DateTime``, Optional (Keyword only)
            New start of the occasion.
        
        timestamp : `DateTime`, Optional (Keyword only)
            The affected occasion.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # cancelled
        if cancelled is ...:
            cancelled = False
        else:
            cancelled = validate_cancelled(cancelled)
        
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
        
        # timestamp
        if timestamp is ...:
            timestamp = DISCORD_EPOCH_START
        else:
            timestamp = validate_timestamp(timestamp)
        
        # Construct
        self = object.__new__(cls)
        self.cancelled = cancelled
        self.end = end
        self.start = start
        self.timestamp = timestamp
        return self
    
    
    @classmethod
    def create_empty(cls):
        """
        Creates an empty occasion overwrite.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.cancelled = False
        self.end = None
        self.start = None
        self.timestamp = DISCORD_EPOCH_START
        return self
    
    
    @classmethod
    def from_fields(cls, timestamp, cancelled, start, end):
        """
        Creates a scheduled event occasion overwrite from the given already parsed fields.
        
        Parameters
        ----------
        timestamp : `DateTime`
            The affected occasion.
        
        cancelled : `bool`
            Whether the occasion is cancelled.
        
        start : `None | DateTime`
            New start of the occasion.
        
        end : `None | DateTime`
            New end of the occasion.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.timestamp = timestamp
        self.cancelled = cancelled
        self.start = start
        self.end = end
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event occasion overwrite from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Scheduled event cancellation event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.cancelled = parse_cancelled(data)
        self.end = parse_end(data)
        self.start = parse_start(data)
        self.timestamp = parse_timestamp(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serializes the scheduled event occasion overwrite.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields of their default value should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_cancelled(self.cancelled, data, defaults)
        put_end(self.end, data, defaults)
        put_start(self.start, data, defaults)
        
        if include_internals:
            put_timestamp(self.timestamp, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # timestamp
        repr_parts.append(' timestamp = ')
        repr_parts.append(repr(self.timestamp))
        
        # cancelled
        cancelled = self.cancelled
        if cancelled:
            repr_parts.append(', cancelled = ')
            repr_parts.append(repr(cancelled))
        
        # start
        start = self.start
        if (start is not None):
            repr_parts.append(', start = ')
            repr_parts.append(repr(start))
        
        # end
        end = self.end
        if (end is not None):
            repr_parts.append(', end = ')
            repr_parts.append(repr(end))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # cancelled
        if self.cancelled != other.cancelled:
            return False
        
        # end
        if self.end != other.end:
            return False
        
        # start
        if self.start != other.start:
            return False
        
        # timestamp
        if self.timestamp != other.timestamp:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns self > other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.timestamp > other.timestamp
    
    
    def __lt__(self, other):
        """Returns self < other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.timestamp < other.timestamp
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # cancelled
        hash_value ^= self.cancelled
        
        # end
        end = self.end
        if (end is not None):
            hash_value ^= hash(end)
        
        # start
        start = self.start
        if (start is not None):
            hash_value ^= hash(start)
        
        # timestamp
        hash_value ^= hash(self.timestamp)
        
        return hash_value
    

    def copy(self):
        """
        Copies the scheduled event occasion overwrite.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.cancelled = self.cancelled
        new.end = self.end
        new.start = self.start
        new.timestamp = self.timestamp
        return new
    
    
    def copy_with(self, *, cancelled = ..., end = ..., start = ..., timestamp = ...):
        """
        Copies the scheduled event occasion overwrite with the given fields.
        
        Parameters
        ----------
        cancelled : `None | bool``, Optional (Keyword only)
            Whether the occasion is cancelled.
        
        end : `None | DateTime``, Optional (Keyword only)
            New end of the occasion.
        
        start : `None | DateTime``, Optional (Keyword only)
            New start of the occasion.
        
        timestamp : `DateTime`, Optional (Keyword only)
            The affected occasion.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # cancelled
        if cancelled is ...:
            cancelled = self.cancelled
        else:
            cancelled = validate_cancelled(cancelled)
        
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
        
        # timestamp
        if timestamp is ...:
            timestamp = self.timestamp
        else:
            timestamp = validate_timestamp(timestamp)
        
        # Construct
        new = object.__new__(type(self))
        new.cancelled = cancelled
        new.end = end
        new.start = start
        new.timestamp = timestamp
        return new
    
    
    def _update_attributes(self, data):
        """
        Updates the attributes of the scheduled event occasion overwrite.
        
        Parameters
        ----------
        data : `dict<str, object>`
            State data given.
        """
        self.cancelled = parse_cancelled(data)
        self.end = parse_end(data)
        self.start = parse_start(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the attributes of the scheduled event and returns the changed ones within an `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Cancellation data.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            The updated attributes.
            
            The returned might have the following items:
            
            +-----------+-------------------+
            | Key       | Value             |
            +===========+===================+
            | cancelled | `bool`            |
            +-----------+-------------------+
            | end       | `None | DateTime` |
            +-----------+-------------------+
            | start     | `None | DateTime` |
            +-----------+-------------------+
        """
        old_attributes = {}
        
        # cancelled
        cancelled = parse_cancelled(data)
        if self.cancelled != cancelled:
            old_attributes['cancelled'] = self.cancelled
            self.cancelled = cancelled
        
        # end
        end = parse_end(data)
        if self.end != end:
            old_attributes['end'] = self.end
            self.end = end
        
        # start
        start = parse_start(data)
        if self.start != start:
            old_attributes['start'] = self.start
            self.start = start
        
        return old_attributes
