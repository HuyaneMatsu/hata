__all__ = ('AutoModerationActionMetadata', 'SendAlertMessageActionMetadata', 'TimeoutActionMetadata')

from math import ceil

from scarletio import RichAttributeErrorBaseType, copy_docs

from ..channel import Channel, create_partial_channel_from_id

from .constants import AUTO_MODERATION_ACTION_TIMEOUT_MAX


class AutoModerationActionMetadata(RichAttributeErrorBaseType):
    """
    Base class for ``AutoModerationAction``'s action metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new action metadata instance.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the action metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new auto moderation action metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
           Auto moderation action metadata payload.
        
        Returns
        -------
        self : ``ScheduledEventEntityMetadata``
        """
        return object.__new__(cls)
    
    
    def to_data(self):
        """
        Converts the action metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two action metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the action metadata's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the action metadata.
        
        Returns
        -------
        new : ``AutoModerationActionMetadata``
        """
        return object.__new__(type(self))


class SendAlertMessageActionMetadata(AutoModerationActionMetadata):
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
    
    
    @copy_docs(AutoModerationActionMetadata.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channel_id=')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadata.from_data)
    def from_data(cls, data):
        channel_id = data.get('channel_id', None)
        if (channel_id is None):
            channel_id = 0
        
        else:
            channel_id = int(channel_id)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        return self
    
    
    @copy_docs(AutoModerationActionMetadata.to_data)
    def to_data(self):
        data = {}
        
        data['channel_id'] = self.channel_id
        
        return data
    
    
    @copy_docs(AutoModerationActionMetadata.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.channel_id != other.channel_id:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationActionMetadata.__hash__)
    def __hash__(self):
        return self.channel_id
    
    
    @copy_docs(AutoModerationActionMetadata.copy)
    def copy(self):
        new = AutoModerationActionMetadata.copy(self)
        
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
            return create_partial_channel_from_id(channel_id, -1, 0)


class TimeoutActionMetadata(AutoModerationActionMetadata):
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
    
    
    @copy_docs(AutoModerationActionMetadata.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' duration=')
        repr_parts.append(repr(self.duration))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationActionMetadata.from_data)
    def from_data(cls, data):
        duration = data.get('duration_seconds', None)
        if (duration is None):
            duration = 0
        
        self = object.__new__(cls)
        self.duration = duration
        return self
    
    
    @copy_docs(AutoModerationActionMetadata.to_data)
    def to_data(self):
        data = {}
        
        data['duration_seconds'] = self.duration
        
        return data
    
    
    @copy_docs(AutoModerationActionMetadata.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.duration != other.duration:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationActionMetadata.__hash__)
    def __hash__(self):
        return self.duration
    
    
    @copy_docs(AutoModerationActionMetadata.copy)
    def copy(self):
        new = AutoModerationActionMetadata.copy(self)
        
        # duration
        new.duration = self.duration
        
        return new
