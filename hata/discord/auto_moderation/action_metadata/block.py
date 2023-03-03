__all__ = ('AutoModerationActionMetadataBlock',)

from scarletio import copy_docs

from .base import AutoModerationActionMetadataBase
from .fields import parse_custom_message, put_custom_message_into, validate_custom_message


class AutoModerationActionMetadataBlock(AutoModerationActionMetadataBase):
    """
    Block action metadata of an auto moderation action.
    
    Attributes
    ----------
    custom_message : `int`
        A custom message that can be used as an explanation if a message is blocked.
    """
    __slots__ = ('custom_message',)
    
    def __new__(cls, custom_message = None):
        """
        Creates a new timeout action metadata for ``AutoModerationAction``-s.
        
        Parameters
        ----------
        custom_message : `None`, `str` = `None`, Optional
            A custom message that can be used as an explanation if a message is blocked.
        
        Raises
        ------
        TypeError
            - If `custom_message` type is incorrect.
        """
        custom_message = validate_custom_message(custom_message)
        
        self = object.__new__(cls)
        self.custom_message = custom_message
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        custom_message = self.custom_message
        if (custom_message is not None):
            repr_parts.append(' custom_message = ')
            repr_parts.append(repr(custom_message))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadataBase.from_data)
    def from_data(cls, data):
        custom_message = parse_custom_message(data)
        
        self = object.__new__(cls)
        self.custom_message = custom_message
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_custom_message_into(self.custom_message, data, defaults)
        return data
    
    
    @copy_docs(AutoModerationActionMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.custom_message != other.custom_message:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationActionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_message
        custom_message = self.custom_message
        if (custom_message is not None):
            hash_value ^= hash(custom_message)
        
        return hash_value
    
    
    @copy_docs(AutoModerationActionMetadataBase.copy)
    def copy(self):
        new = AutoModerationActionMetadataBase.copy(self)
        
        # custom_message
        new.custom_message = self.custom_message
        
        return new
    
    
    def copy_with(self, *, custom_message = ...):
        """
        Copies the action metadata and modifies it's attributes by the given values.
        
        Parameters
        ----------
        custom_message : `None`, `str`, Optional (Keyword only)
            A custom message that can be used as an explanation if a message is blocked.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if custom_message is ...:
            custom_message = self.custom_message
        else:
            custom_message = validate_custom_message(custom_message)
        
        new = AutoModerationActionMetadataBase.copy(self)
        new.custom_message = custom_message
        return new
