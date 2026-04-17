__all__ = ('ScheduledEventUserEntry',)

from scarletio import RichAttributeErrorBaseType

from ...user import ZEROUSER

from .fields import (
    parse_scheduled_event_id, parse_timestamp, parse_user, put_scheduled_event_id, put_timestamp, put_user,
    validate_scheduled_event_id, validate_timestamp, validate_user
)


class ScheduledEventUserEntry(RichAttributeErrorBaseType):
    """
    Represents a scheduled event user entry.
    
    Attributes
    ----------
    scheduled_event_id : `int`
        The owner scheduled event's identifier.
    
    timestamp : `None | DateTime`
        The timestamp of the specific affected event if any.
    
    user : ``ClientUserBase``
        The user.
    """
    __slots__ = ('scheduled_event_id', 'timestamp', 'user')
    
    
    def __new__(cls, *, scheduled_event_id = ..., timestamp = ..., user = ...):
        """
        Creates a new scheduled event user entry.
        
        Parameters
        ----------
        scheduled_event_id : `None | int``, Optional (Keyword only)
            The owner scheduled event's identifier.
        
        timestamp : `None | DateTime`, Optional (Keyword only)
            The timestamp of the specific affected event if any.
        
        user : ``None | ClientUserBase``, Optional (Keyword only)
            The user.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = False
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # timestamp
        if timestamp is ...:
            timestamp = None
        else:
            timestamp = validate_timestamp(timestamp)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.scheduled_event_id = scheduled_event_id
        self.timestamp = timestamp
        self.user = user
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
        self.scheduled_event_id = 0
        self.timestamp = None
        self.user = ZEROUSER
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new scheduled event user entry from the given data.
        
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
        self.scheduled_event_id = parse_scheduled_event_id(data)
        self.timestamp = parse_timestamp(data)
        self.user = parse_user(data, guild_id)
        return self
    
    
    def to_data(self, *, defaults = False, guild_id = 0):
        """
        Serializes the scheduled event user entry.
        
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
        put_scheduled_event_id(self.scheduled_event_id, data, defaults)
        put_timestamp(self.timestamp, data, defaults)
        put_user(self.user, data, defaults, guild_id = guild_id)
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # scheduled_event_id
        repr_parts.append(' scheduled_event_id = ')
        repr_parts.append(repr(self.scheduled_event_id))
        
        # timestamp
        timestamp = self.timestamp
        if (timestamp is not None):
            repr_parts.append(', timestamp = ')
            repr_parts.append(repr(timestamp))
        
        # user
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # scheduled_event_id
        if self.scheduled_event_id != other.scheduled_event_id:
            return False
        
        # timestamp
        if self.timestamp != other.timestamp:
            return False
        
        # user
        if self.user != other.user:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # scheduled_event_id
        hash_value ^= self.scheduled_event_id
        
        # timestamp
        timestamp = self.timestamp
        if (timestamp is not None):
            hash_value ^= hash(timestamp)
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    

    def copy(self):
        """
        Copies the scheduled event user entry.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.scheduled_event_id = self.scheduled_event_id
        new.timestamp = self.timestamp
        new.user = self.user
        return new
    
    
    def copy_with(self, *, scheduled_event_id = ..., timestamp = ..., user = ...):
        """
        Copies the scheduled event user entry with the given fields.
        
        Parameters
        ----------
        scheduled_event_id : `None | int``, Optional (Keyword only)
            The owner scheduled event's identifier.
        
        timestamp : `None | DateTime`, Optional (Keyword only)
            The timestamp of the specific affected event if any.
        
        user : ``None | ClientUserBase``, Optional (Keyword only)
            The user.
        
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
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = self.scheduled_event_id
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # timestamp
        if timestamp is ...:
            timestamp = self.timestamp
        else:
            timestamp = validate_timestamp(timestamp)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.scheduled_event_id = scheduled_event_id
        new.timestamp = timestamp
        new.user = user
        return new
