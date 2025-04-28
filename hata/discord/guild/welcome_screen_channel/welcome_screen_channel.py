__all__ = ('WelcomeScreenChannel',)

from scarletio import RichAttributeErrorBaseType

from ...channel import Channel, ChannelType, create_partial_channel_from_id

from .fields import (
    parse_channel_id, parse_description, parse_emoji, put_channel_id, put_description, put_emoji,
    validate_channel_id, validate_description, validate_emoji
)


class WelcomeScreenChannel(RichAttributeErrorBaseType):
    """
    Represents a featured channel by a welcome screen.
    
    Attributes
    ----------
    channel_id : `int`
        The represented channel's identifier.
    description : `None`, `str`
        The channel's short description.
    emoji : `None`, ``Emoji``
        An emoji displayed before the `description`.
    """
    __slots__ = ('channel_id', 'description', 'emoji', )
    
    def __new__(cls, *, channel_id = ..., description = ..., emoji = ...):
        """
        Creates a new welcome channel.
        
        Parameters
        -----------
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The represented channel or its identifier.
        description : `None`, `str`, Optional (Keyword only)
            The channel's short description.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            An emoji displayed before the `description`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # Construct
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.description = description
        self.emoji = emoji
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new welcome channel instance from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Welcome channel data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.channel_id = parse_channel_id(data)
        self.description = parse_description(data)
        self.emoji = parse_emoji(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the welcome channel to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `str`
        """
        data = {}
        put_channel_id(self.channel_id, data, defaults)
        put_description(self.description, data, defaults)
        put_emoji(self.emoji, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the welcome channel's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # channel_id
        repr_parts.append(' channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji = ')
            repr_parts.append(repr(emoji))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the welcome channel's hash."""
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two welcome channels are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the welcome channel.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.channel_id = self.channel_id
        new.description = self.description
        new.emoji = self.emoji
        return new
    
    
    def copy_with(self, *, channel_id = ..., description = ..., emoji = ...):
        """
        Creates a new welcome channel with the given fields.
        
        Parameters
        -----------
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The represented channel or its identifier.
        description : `None`, `str`, Optional (Keyword only)
            The channel's short description.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            An emoji displayed before the `description`.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # Construct
        new = object.__new__(type(self))
        new.channel_id = channel_id
        new.description = description
        new.emoji = emoji
        return new
    
    
    @property
    def channel(self):
        """
        Returns the welcome channel's respective channel.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.guild_text, 0)
