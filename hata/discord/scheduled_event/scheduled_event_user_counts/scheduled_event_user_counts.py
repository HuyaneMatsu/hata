__all__ = ('ScheduledEventUserCounts',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_count, parse_occasion_counts, put_count, put_occasion_counts, validate_count, validate_occasion_counts
)


class ScheduledEventUserCounts(RichAttributeErrorBaseType):
    """
    Represents a scheduled event user counts.
    
    Attributes
    ----------
    count : `int`
        The amount of users subscribed to the scheduled event.
    
    occasion_counts : `None | DateTime`
        The amount of users subscribed to a specific occasion.
    """
    __slots__ = ('count', 'occasion_counts')
    
    
    def __new__(cls, *, count = ..., occasion_counts = ...):
        """
        Creates a new scheduled event user counts.
        
        Parameters
        ----------
        count : `None | int``, Optional (Keyword only)
            The amount of users subscribed to the scheduled event.
        
        occasion_counts : `None | DateTime`, Optional (Keyword only)
            The amount of users subscribed to a specific occasion.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # count
        if count is ...:
            count = False
        else:
            count = validate_count(count)
        
        # occasion_counts
        if occasion_counts is ...:
            occasion_counts = None
        else:
            occasion_counts = validate_occasion_counts(occasion_counts)
        
        # Construct
        self = object.__new__(cls)
        self.count = count
        self.occasion_counts = occasion_counts
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
        self.count = 0
        self.occasion_counts = None
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new scheduled event user counts from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Input data.
        
        guild_id : `int` = `0`, Optional
            The local guild's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.count = parse_count(data)
        self.occasion_counts = parse_occasion_counts(data)
        return self
    
    
    def to_data(self, *, defaults = False, guild_id = 0):
        """
        Serializes the scheduled event user counts.
        
        Parameters
        ----------
        defaults : `int`
            Whether fields of their default value should be included as well.
        
        guild_id : `int` = `0`, Optional (Keyword only)
            The local guild's identifier.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_count(self.count, data, defaults)
        put_occasion_counts(self.occasion_counts, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # count
        repr_parts.append(' count = ')
        repr_parts.append(repr(self.count))
        
        # occasion_counts
        occasion_counts = self.occasion_counts
        if (occasion_counts is not None):
            repr_parts.append(', occasion_counts = ')
            repr_parts.append(repr(occasion_counts))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # count
        if self.count != other.count:
            return False
        
        # occasion_counts
        if self.occasion_counts != other.occasion_counts:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # count
        hash_value ^= self.count
        
        # occasion_counts
        occasion_counts = self.occasion_counts
        if (occasion_counts is not None):
            for key, value in occasion_counts.items():
                hash_value ^= hash(key) & value
        
        return hash_value
    

    def copy(self):
        """
        Copies the scheduled event user counts.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.count = self.count
        
        occasion_counts = self.occasion_counts
        if (occasion_counts is not None):
            occasion_counts = occasion_counts.copy()
        new.occasion_counts = occasion_counts
        
        return new
    
    
    def copy_with(self, *, count = ..., occasion_counts = ...):
        """
        Copies the scheduled event user counts with the given fields.
        
        Parameters
        ----------
        count : `None | int``, Optional (Keyword only)
            The amount of users subscribed to the scheduled event.
        
        occasion_counts : `None | DateTime`, Optional (Keyword only)
            The amount of users subscribed to a specific occasion.
        
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
        # count
        if count is ...:
            count = self.count
        else:
            count = validate_count(count)
        
        # occasion_counts
        if occasion_counts is ...:
            occasion_counts = self.occasion_counts
            if (occasion_counts is not None):
                occasion_counts = occasion_counts.copy()
        else:
            occasion_counts = validate_occasion_counts(occasion_counts)
        
        # Construct
        new = object.__new__(type(self))
        new.count = count
        new.occasion_counts = occasion_counts
        return new
