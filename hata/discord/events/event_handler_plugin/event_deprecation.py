__all__ = ('EventDeprecation',)

from datetime import datetime as DateTime, timezone as TimeZone
from warnings import warn

from scarletio import RichAttributeErrorBaseType


NOW = DateTime.now(tz = TimeZone.utc)
FORMAT_CODE = '%Y %B'


class EventDeprecation(RichAttributeErrorBaseType):
    """
    Represents deprecation notice for an event.
    
    Attributes
    ----------
    allowed : `bool`
        Whether the deprecation notice is allowed to trigger.
    
    use_instead : `str`
        The event's name to use instead.
    
    removed_after : `str`
        When the field supposed to be removed.
    """
    __slots__ = ('allowed', 'use_instead', 'removed_after')

    def __new__(cls, use_instead, removed_after, *, trigger_after = None):
        """
        Creates a new event deprecation.
        
        Parameters
        ----------
        use_instead : `str`
            The event's name to use instead.
        
        removed_after : `DateTime`
            When the feature will be removed.
        
        trigger_after : `None | DateTime` = `None`, Optional (Keyword only)
            After when the deprecation should trigger.
        """
        # create allowed from trigger_after
        if trigger_after is None:
            allowed = True
        else:
            allowed = NOW > trigger_after
        
        # process removed_after
        removed_after = format(removed_after, FORMAT_CODE)
        
        # Construct
        self = object.__new__(cls)
        self.allowed = allowed
        self.use_instead = use_instead
        self.removed_after = removed_after
        return self

    
    def __eq__(self, other):
        """Returns whether the two deprecations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # allowed
        if self.allowed != other.allowed:
            return False
        
        # use_instead
        if self.use_instead != other.use_instead:
            return False
        
        # removed_after
        if self.removed_after != other.removed_after:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the deprecation's hash value."""
        hash_value = 0
        
        # allowed
        hash_value ^= self.allowed
        
        # use_instead
        hash_value ^= hash(self.use_instead)
        
        # removed_after
        hash_value ^= hash(self.removed_after)
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the deprecation's representation"""
        repr_parts = ['<', type(self).__name__]
        
        # allowed
        repr_parts.append(', allowed = ')
        repr_parts.append(repr(self.allowed))
        
        # use_instead
        repr_parts.append(', use_instead = ')
        repr_parts.append(repr(self.use_instead))
        
        # removed_after
        repr_parts.append(', removed_after = ')
        repr_parts.append(repr(self.removed_after))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def trigger(self, event_name, stack_level):
        """
        Triggers the deprecation.
        
        Parameters
        ----------
        event_name : `str`
            The event's name that is deprecated.
        
        stack_level : `int`
            The stack level to warn at.
        
        Returns
        -------
        warned : `bool`
        """
        if not self.allowed:
            return False
        
        warn(
            (
                f'`{event_name}` event is deprecated and will be removed at {self.removed_after}. '
                f'Please use {self.use_instead} instead.'
            ),
            FutureWarning,
            stacklevel = stack_level,
        )
        return True
