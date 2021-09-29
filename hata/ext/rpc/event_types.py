__all__ = ('ChannelCreateEvent', 'ChannelVoiceSelectEvent', 'GuildCreateEvent', )

from ...discord.bases import EventBase

class GuildCreateEvent(EventBase):
    """
    Represents a processed guild create rpc dispatch event.
    
    Attributes
    ----------
    id : `int`
        The guild's identifier.
    name : `str`
        The created guilds name.
    """
    __slots__ = ('id', 'name')
    
    def __repr__(self):
        """Returns the representation of the guild create event."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """
        Unpacks the guild create event.
        
        This method is a generator.
        """
        yield self.id
        yield self.name


class ChannelCreateEvent(EventBase):
    """
    Represents a processed channel create rpc dispatch event.
    
    Attributes
    ----------
    id : `int`
        The channel's identifier.
    name : `str`
        The created channel name.
    type : `int`
        The channel's type.
    """
    __slots__ = ('id', 'name', 'type')
    
    def __repr__(self):
        """Returns the representation of the channel create event."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}, type={self.type}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """
        Unpacks the channel create event.
        
        This method is a generator.
        """
        yield self.id
        yield self.name
        yield self.type


class ChannelVoiceSelectEvent(EventBase):
    """
    Represents a voice select event.
    
    Attributes
    ----------
    channel_id : `int`
        The respective chanel's identifier, or `0` if the users left the channel.
    guild_id : `int`
        The respective guild's identifier, or `0` for private channels.
    """
    __slots__ = ('channel_id', 'guild_id')
    
    def __repr__(self):
        """Returns the representation of the channel voice select event."""
        return f'<{self.__class__.__name__} guild_id={self.guild_id}, channel_id={self.channel_id}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """
        Unpacks the channel voice select event.
        
        This method is a generator.
        """
        yield self.guild_id
        yield self.channel_id
