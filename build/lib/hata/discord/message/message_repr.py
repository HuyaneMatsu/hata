__all__ = ('MessageRepr', )

from ...backend.export import include

from ..bases import DiscordEntity
from ..core import GUILDS, CHANNELS

Message = include('Message')

class MessageRepr(DiscordEntity):
    """
    Represents an uncached message.
    
    The class is used, when `HATA_ALLOW_DEAD_EVENTS` env variable is set as `True`.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the represented message.
    channel_id : `int`
        The respective message's channel's identifier.
    guild_id : `int`
        The respective message's guild's identifier.
        
        Defaults to `0`.
    """
    __slots__ = ('channel_id', 'guild_id',)
    
    def __init__(self, message_id, channel_id, guild_id):
        """
        Creates a new message representation with the given parameters.
        
        Parameters
        ----------
        message_id : `int`
            The unique identifier number of the represented message.
        channel_id : `int`
            The respective message's channel's identifier.
        guild_id : `int`
            The respective message's guild's identifier.
        """
        self.id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
    
    
    @property
    def channel(self):
        """
        Returns the represented message's channel.
        
        Returns
        -------
        channel : `None` or ``ChannelBase``
        """
        return CHANNELS.get(self.channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the represented message's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def __repr__(self):
        """Returns the message representation's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' id=',
            repr(self.id),
            ', channel_id=',
            repr(self.channel_id),
        ]
        
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(', guild_id=')
            repr_parts.append(repr(guild_id))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
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
