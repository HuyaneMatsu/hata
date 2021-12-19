__all__ = ('ChannelCreateEvent', 'ChannelVoiceSelectEvent', 'GuildCreateEvent', )

from scarletio import copy_docs

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
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.id
        yield self.name
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.id^hash(self.name)


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
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}, type={self.type}>'
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.id
        yield self.name
        yield self.type
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        if self.type != other.type:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.id^hash(self.name)^self.type


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
        Creates a new channel voice select event from the given parameters.
        
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
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} guild_id={self.guild_id}, channel_id={self.channel_id}>'
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.channel_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.channel_id != other.channel_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.guild_id^self.channel_id
