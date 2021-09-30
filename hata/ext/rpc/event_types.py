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
    
    def __new__(cls, guild_id, guild_name):
        """
        Creates a new guild create event from the given parameters
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier.
        guild_name : `str`
            The created guilds name.
        """
        self = object.__new__(cls)
        self.id = guild_id
        self.name = guild_name
        return self
    
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
    
    def __new__(cls, channel_id, channel_name, channel_type):
        """
        Creates a new channel create event from the given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's identifier.
        channel_name : `str`
            The created channel name.
        channel_type : `int`
            The channel's type.
        """
        self = object.__new__(cls)
        self.id = channel_id
        self.name = channel_name
        self.type = channel_type
        return self
    
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
    
    def __new__(cls, channel_id, guild_id):
        """
        Creates a new channel voice select event from teh given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The respective channel's identifier.
        guild_id : `int`
            The respective guild's identifier.
        """
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.guild_id = guild_id
        return self
    
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
