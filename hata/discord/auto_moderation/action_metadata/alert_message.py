__all__ = ('AutoModerationActionMetadataSendAlertMessage',)

from scarletio import copy_docs

from .base import AutoModerationActionMetadataBase
from .fields import parse_channel_id, put_channel_id_into, validate_channel_id


class AutoModerationActionMetadataSendAlertMessage(AutoModerationActionMetadataBase):
    """
    Send alert message action metadata for an auto moderation action.
    
    Attributes
    ----------
    channel_id : `int`
        The channel's identifier where the alert messages are sent.
    """
    __slots__ = ('channel_id',)
    
    def __new__(cls, channel_id = None):
        """
        Creates a new send alert message action metadata.
        
        Parameters
        ----------
        channel_id : `None`, ``Channel``, `int` = `None`, Optional
            The channel where the alert message should be sent.
               
        Raises
        ------
        TypeError
            - If `channel_id`'s type is incorrect.
        """
        channel_id = validate_channel_id(channel_id)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadataBase.from_data)
    def from_data(cls, data):
        channel_id = parse_channel_id(data)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        
        put_channel_id_into(self.channel_id, data, defaults)
        
        return data
    
    
    @copy_docs(AutoModerationActionMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.channel_id != other.channel_id:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationActionMetadataBase.__hash__)
    def __hash__(self):
        return self.channel_id
    
    
    @copy_docs(AutoModerationActionMetadataBase.copy)
    def copy(self):
        new = AutoModerationActionMetadataBase.copy(self)
        new.channel_id = self.channel_id
        return new
    
    
    def copy_with(self, *, channel_id = ...):
        """
        Copies the action metadata and modifies it's attributes by the given values.
        
        Parameters
        ----------
        channel_id : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel where the alert message should be sent.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        new = AutoModerationActionMetadataBase.copy(self)
        new.channel_id = channel_id
        return new
