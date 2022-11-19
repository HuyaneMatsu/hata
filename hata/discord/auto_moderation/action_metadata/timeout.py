__all__ = ('AutoModerationActionMetadataTimeout',)

from scarletio import copy_docs

from .base import AutoModerationActionMetadataBase
from .fields import parse_duration, put_duration_into, validate_duration


class AutoModerationActionMetadataTimeout(AutoModerationActionMetadataBase):
    """
    Timeout action metadata of an auto moderation action.
    
    Attributes
    ----------
    duration : `int`
        The timeout's duration applied on trigger.
    """
    __slots__ = ('duration',)
    
    def __new__(cls, duration = None):
        """
        Creates a new timeout action metadata for ``AutoModerationAction``-s.
        
        Parameters
        ----------
        duration : `None`, `int`, `float` = `None`, Optional
            The timeout's duration applied on trigger.
        
        Raises
        ------
        TypeError
            - If `duration` type is incorrect.
        """
        duration = validate_duration(duration)
        
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' duration = ')
        repr_parts.append(repr(self.duration))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadataBase.from_data)
    def from_data(cls, data):
        duration = parse_duration(data)
        
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_duration_into(self.duration, data, defaults)
        return data
    
    
    @copy_docs(AutoModerationActionMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.duration != other.duration:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationActionMetadataBase.__hash__)
    def __hash__(self):
        return self.duration
    
    
    @copy_docs(AutoModerationActionMetadataBase.copy)
    def copy(self):
        new = AutoModerationActionMetadataBase.copy(self)
        
        # duration
        new.duration = self.duration
        
        return new
    
    
    def copy_with(self, *, duration = ...):
        """
        Copies the action metadata and modifies it's attributes by the given values.
        
        Parameters
        ----------
        duration : `None`, `int`, `float`, Optional (Keyword only)
            The timeout's duration applied on trigger.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if duration is ...:
            duration = self.duration
        else:
            duration = validate_duration(duration)
        
        new = AutoModerationActionMetadataBase.copy(self)
        new.duration = duration
        return new
