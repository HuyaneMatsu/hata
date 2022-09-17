__all__ = ('AutoModerationActionMetadataSendAlertMessage',)

from scarletio import copy_docs

from ...channel import Channel, ChannelType, create_partial_channel_from_id

from .base import AutoModerationActionMetadataBase


class AutoModerationActionMetadataSendAlertMessage(AutoModerationActionMetadataBase):
    """
    Send alert message action metadata for an auto moderation action.
    
    Attributes
    ----------
    channel_id : `int`
        The channel's identifier where the alert messages are sent.
    """
    __slots__ = ('channel_id',)
    
    def __new__(cls, channel):
        """
        Creates a new send alert message action metadata.
        
        Parameters
        ----------
        channel : `None`, ``Channel``, `int`
            The channel where the alert message should be sent.
               
        Raises
        ------
        TypeError
            - If `channel`'s type is incorrect.
        """
        if channel is None:
            channel_id = 0
        
        elif isinstance(channel, Channel):
            channel_id = channel.id
        
        elif isinstance(channel, int):
            channel_id = channel
        
        else:
            raise TypeError(
                f'`channel` parameter can be `{Channel.__name__}`, `int`, '
                f'got {channel.__class__.__name__}; {channel!r}.'
            )
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channel_id=')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadataBase.from_data)
    def from_data(cls, data):
        channel_id = data.get('channel_id', None)
        if (channel_id is None):
            channel_id = 0
        
        else:
            channel_id = int(channel_id)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    
    @copy_docs(AutoModerationActionMetadataBase.to_data)
    def to_data(self):
        data = {}
        
        data['channel_id'] = self.channel_id
        
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
        
        # channel_id
        new.channel_id = self.channel_id
        
        return new
    
    @property
    def channel(self):
        """
        Returns the channels where the alert messages are sent.
        """
        channel_id = self.channel_id
        if channel_id:
            return create_partial_channel_from_id(channel_id, ChannelType.unknown, 0)
