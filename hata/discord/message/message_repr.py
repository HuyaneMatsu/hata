__all__ = ('MessageRepr', )

from ...backend.export import include

from ..bases import DiscordEntity

Message = include('Message')

class MessageRepr(DiscordEntity):
    """
    Represents an uncached message.
    
    The class is used, when `HATA_ALLOW_DEAD_EVENTS` env variable is set as `True`.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the represented message.
    channel : ``ChannelBase``
        The respective message's channel.
    """
    __slots__ = ('channel',)
    def __init__(self, message_id, channel):
        """
        Creates a new message representation with the given parameters.
        
        Parameters
        ----------
        message_id : `int`
            The unique identifier number of the represented message.
        channel : ``ChannelBase`` instance
            The respective message's channel.
        """
        self.id = message_id
        self.channel = channel
    
    @property
    def guild(self):
        """
        Returns the represented message's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return self.channel.guild
    
    def __repr__(self):
        """Returns the message representation's representation."""
        return f'<{self.__class__.__name__} id={self.id}, channel={self.channel!r}>'
    
    def __gt__(self, other):
        """Returns whether this message's id is greater than the other's."""
        other_type = other.__class__
        if other_type is type(self) or isinstance(other_type, Message):
            return (self.id > other.id)
        
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether this message's id is greater than the other's, or whether the two messages are equal."""
        other_type = other.__class__
        if other_type is type(self):
            return (self.id >= other.id)
        
        if isinstance(other_type, Message):
            return (self.id > other.id)
    
        return NotImplemented
    
    def __eq__(self, other):
        """Returns whether the two message representations are equal."""
        if type(self) is type(other):
            return (self.id == other.id)
        
        return NotImplemented
    
    def __ne__(self, other):
        """Returns whether the two message representations are not equal."""
        if type(self) is type(other):
            return (self.id != other.id)
        
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether this message's id is less than the other's, or whether the two messages are equal."""
        other_type = other.__class__
        if other_type is type(self):
            return (self.id <= other.id)
        
        if isinstance(other_type, Message):
            return (self.id < other.id)
    
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether this message's id is less than the other's."""
        other_type = other.__class__
        if other_type is type(self) or isinstance(other_type, Message):
            return (self.id < other.id)
        
        return NotImplemented
