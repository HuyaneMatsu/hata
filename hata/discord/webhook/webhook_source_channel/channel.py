__all__ = ('WebhookSourceChannel',)

from scarletio import include

from ...bases import DiscordEntity

from .fields import validate_id, validate_name, parse_id, parse_name, put_id_into, put_name_into


ChannelMetadataGuildBase = include('ChannelMetadataGuildBase')
ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')


class WebhookSourceChannel(DiscordEntity):
    """
    Entity representing a server type ``Webhook``'s channel.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the channel.
    name : `str`
        The name of the channel.
    """
    __slots__ = ('name',)
    
    def __new__(cls, *, channel_id = ..., name = ...):
        """
        Creates a new webhook source channel from the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier.
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_id(channel_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Constructor
        self = object.__new__(cls)
        self.id = channel_id
        self.name = name
        return self
        
        
    @classmethod
    def from_data(cls, data):
        """
        Creates a new webhook source channel from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Webhook source channel data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        return self
    
    
    @classmethod
    def from_channel(cls, channel):
        """
        Creates a new webhook source channel from the given channel.
        
        Parameters
        ----------
        channel : ``Channel``
            The respective channel instance.
        
        Returns
        -------
        self : ``WebhookSourceChannel``
        """
        self = object.__new__(cls)
        self.id = channel.id
        self.name = channel.name
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the webhook source channel to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the webhook source channel's representation."""
        return f'<{self.__class__.__name__} id = {self.id!r}, name = {self.name!r}>'
        
    
    def __hash__(self):
        """Returns the webhook channel source's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two webhook source channels are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two webhook source channels are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self equals to other. `other` must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other webhook source channel to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    @property
    def channel(self):
        """
        Returns the channel of the webhook source channel.
        
        If the channel is not cached, creates a new one.
        
        Returns
        -------
        channel : ``Channel``
        """
        channel = create_partial_channel_from_id(self.id, ChannelType.guild_announcements, 0)
        
        if channel.partial:
            metadata = channel.metadata
            if isinstance(metadata, ChannelMetadataGuildBase):
                metadata.name = self.name
        
        return channel
    
    
    def copy(self):
        """
        Copies the webhook source channel.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        return new
    
    
    def copy_with(self, *, channel_id = ..., name = ...):
        """
        Copies a new webhook source channel from the given fields.
        
        Parameters
        ----------
        channel_id : `int`, Optional (Keyword only)
            The channel's identifier.
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = self.id
        else:
            channel_id = validate_id(channel_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Constructor
        new = object.__new__(type(self))
        new.id = channel_id
        new.name = name
        return new
