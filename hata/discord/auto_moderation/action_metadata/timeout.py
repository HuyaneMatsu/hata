__all__ = ('AutoModerationActionMetadataTimeout',)

from math import ceil

from scarletio import copy_docs

from ..constants import AUTO_MODERATION_ACTION_TIMEOUT_MAX

from .base import AutoModerationActionMetadataBase


class AutoModerationActionMetadataTimeout(AutoModerationActionMetadataBase):
    """
    Timeout action metadata of an auto moderation action.
    
    Attributes
    ----------
    duration : `int`
        The timeout's duration applied on trigger.
    """
    __slots__ = ('duration',)
    
    def __new__(cls, duration):
        """
        Creates a new timeout action metadata for ``AutoModerationAction``-s.
        
        Parameters
        ----------
        duration : `None`, `int`, `float`
        The timeout's duration applied on trigger.
        
        Raises
        ------
        TypeError
            - If `duration` type is incorrect.
        ValueError
            - If `duration` is out of the expected range.
        """
        if duration is None:
            duration = 0
        
        elif isinstance(duration, int):
            pass
        
        elif isinstance(duration, float):
            duration = ceil(duration)
        
        else:
            raise TypeError(
                f'`duration` can be `None`, `int`, `float`, got {duration.__class__.__name__}; {duration!r}.'
            )
        
        if duration > AUTO_MODERATION_ACTION_TIMEOUT_MAX:
            raise ValueError(
                f'`duration` can be max {AUTO_MODERATION_ACTION_TIMEOUT_MAX!r}, got {duration!r}.'
            )
        
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' duration=')
        repr_parts.append(repr(self.duration))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadataBase.from_data)
    def from_data(cls, data):
        duration = data.get('duration_seconds', None)
        if (duration is None):
            duration = 0
        
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.to_data)
    def to_data(self):
        data = {}
        
        data['duration_seconds'] = self.duration
        
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
