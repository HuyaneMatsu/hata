__all__ = ('FlagDeprecation', )

from datetime import datetime as DateTime, timezone as TimeZone
from warnings import warn

from scarletio import RichAttributeErrorBaseType


NOW = DateTime.now(tz = TimeZone.utc)
FORMAT_CODE = '%Y %B'


class FlagDeprecation(RichAttributeErrorBaseType):
    """
    Represents deprecation notice for a flag.
    
    Attributes
    ----------
    allowed : `bool`
        Whether the deprecation notice is allowed to trigger.
    
    removed_after : `str`
        When the field supposed to be removed.
    
    use_instead : `str`
        What should be used instead of this feature.
    """
    __slots__ = ('allowed', 'removed_after', 'use_instead')
    
    def __new__(cls, use_instead, removed_after, *, trigger_after = None):
        """
        Creates a new flag deprecation.
        
        Parameters
        ----------
        user_instance : `str`
            What should be used instead.
        
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
        self.removed_after = removed_after
        self.use_instead = use_instead
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two deprecations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # allowed
        if self.allowed != other.allowed:
            return False
        
        # removed_after
        if self.removed_after != other.removed_after:
            return False
        
        # use_instead
        if self.use_instead != other.use_instead:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the deprecation's hash value."""
        hash_value = 0
        
        # allowed
        hash_value ^= self.allowed
        
        # removed_after
        hash_value ^= hash(self.removed_after)
        
        # use_instead
        hash_value ^= hash(self.use_instead)
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the deprecation's representation"""
        repr_parts = ['<', type(self).__name__]
        
        # allowed
        repr_parts.append(', allowed = ')
        repr_parts.append(repr(self.allowed))
        
        # removed_after
        repr_parts.append(', removed_after = ')
        repr_parts.append(repr(self.removed_after))
        
        # use_instead
        repr_parts.append(', use_instead = ')
        repr_parts.append(repr(self.use_instead))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def trigger(self, type_name, flag_name, stack_level):
        """
        Triggers the deprecation.
        
        Parameters
        ----------
        type_name : `str`
            The deprecated's name.
        
        flag_name : `str`
            The deprecated flags name.
        
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
                f'`{type_name}.{flag_name}` is deprecated and will be removed at {self.removed_after}. '
                f'Please use {self.use_instead} instead.'
            ),
            FutureWarning,
            stacklevel = stack_level,
        )
        return True
