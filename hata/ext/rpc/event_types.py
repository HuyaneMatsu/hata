__all__ = ('ChannelCreateEvent', 'ChannelVoiceSelectEvent', 'GuildCreateEvent', 'NotificationCreateEvent')

import reprlib

from scarletio import copy_docs

from ...discord.bases import EventBase
from ...discord.message import Message


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
    
    def __new__(cls, data):
        """
        Creates a new guild create event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild create event data.
        """
        self = object.__new__(cls)
        self.id = int(data['id'])
        self.name = data['name']
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
        return self.id ^ hash(self.name)


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
    
    def __new__(cls, data):
        """
        Creates a new channel create event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            channel create data.
        """
        self = object.__new__(cls)
        self.id = int(data['id'])
        self.name = data['name']
        self.type = data['type']
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
        return self.id ^ hash(self.name) ^ self.type


class ChannelVoiceSelectEvent(EventBase):
    """
    Represents a voice select event.
    
    Attributes
    ----------
    channel_id : `int`
        The respective channel's identifier, or `0` if the users left the channel.
    guild_id : `int`
        The respective guild's identifier, or `0` for private channels.
    """
    __slots__ = ('channel_id', 'guild_id')
    
    def __new__(cls, data):
        """
        Creates a new channel voice select event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild voice select event data.
        """
        channel_id = data.get('channel_id', None)
        if (channel_id is None):
            channel_id = 0
        else:
            channel_id = int(channel_id)
        
        guild_id = data.get('guild_id', None)
        if (guild_id is None):
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
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
        return self.guild_id ^ self.channel_id


class NotificationCreateEvent(EventBase):
    """
    Represents a notification create event.
    
    Attributes
    ----------
    body : `str`
        The body of the notification.
    channel_id : `int`
        The respective channel's identifier.
    icon_url : `None`, `str`
        Icon url for the notification.
    message : ``Message``
        The message, that generated this notification.
    title : `str`
        Title of the notification.
    """
    __slots__ = ('body', 'channel_id', 'icon_url', 'message', 'title')
    
    def __new__(cls, data):
        """
        Creates a new notification create event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Notification create data.
        """
        self = object.__new__(cls)
        self.body = data['body']
        self.channel_id = int(data['channel_id'])
        self.icon_url = data.get('icon_url', None)
        self.message = Message.from_data(data['message'])
        self.title = data['title']
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} channel_id={self.channel_id}, title={reprlib.repr(self.title)}>'
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 5
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.channel_id
        yield self.message
        yield self.title
        yield self.body
        yield self.icon_url
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.body != other.body:
            return False
        
        if self.channel_id != other.channel_id:
            return False
        
        if self.icon_url != other.icon_url:
            return False
        
        if self.message != other.message:
            return False
        
        if self.title != other.title:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        hash_value ^= hash(self.body)
        
        hash_value ^= self.channel_id
        
        icon_url = self.icon_url
        if (icon_url is not None):
            hash_value ^= hash(self.icon_url)
        
        hash_value ^= hash(self.message)
        
        hash_value = hash(self.title)
        
        return hash_value
