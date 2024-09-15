__all__ = ('EmbeddedActivityLocation', )

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_channel_id, parse_guild_id, parse_type, put_channel_id_into, put_guild_id_into, put_type_into,
    validate_channel_id, validate_guild_id, validate_type
)
from .preinstanced import EmbeddedActivityLocationType


class EmbeddedActivityLocation(RichAttributeErrorBaseType):
    """
    Represents an embedded activity's location
    
    Attributes
    ----------
    channel_id : `int`
        The location's channel's identifier.
    
    guild_id : `int`
        The location's guild's identifier.
    
    type : ``EmbeddedActivityLocationType``
        The location's type
    """
    __slots__ = ('channel_id', 'guild_id', 'type', )
    
    def __new__(cls, *, channel_id = ..., guild_id = ..., location_type = ...):
        """
        Creates a new embedded activity location.
        
        Parameters
        ----------
        channel_id : `int | Channel`, Optional (Keyword only)
            The location's channel's identifier.
    
        guild_id : `int | Guild`, Optional (Keyword only)
            The location's guild's identifier.
    
        location_type : `EmbeddedActivityLocationType | str`, Optional (Keyword only)
            The location's type
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # location_type
        if location_type is ...:
            location_type = EmbeddedActivityLocationType.none
        else:
            location_type = validate_type(location_type)
        
        # Construct
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.type = location_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new embedded activity location from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Construct
        self = object.__new__(cls)
        self.channel_id = parse_channel_id(data)
        self.guild_id = parse_guild_id(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the embedded activity location.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_type_into(self.type, data, defaults)
        put_channel_id_into(self.channel_id, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the embedded activity location's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # channel_id
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        # type
        location_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(location_type.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the embedded activity location's hash value."""
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # guild_id
        hash_value ^= self.guild_id
        
        # type
        hash_value ^= hash(self.type)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity locations are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the embedded activity location.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.channel_id = self.channel_id
        new.guild_id = self.guild_id
        new.type = self.type
        return new
    
    
    def copy_with(self, *, channel_id = ..., guild_id = ..., location_type = ...):
        """
        Copies the embedded activity location with the given fields.
        
        Parameters
        ----------
        channel_id : `int | Channel`, Optional (Keyword only)
            The location's channel's identifier.
    
        guild_id : `int | Guild`, Optional (Keyword only)
            The location's guild's identifier.
    
        location_type : `EmbeddedActivityLocationType | str`, Optional (Keyword only)
            The location's type
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # location_type
        if location_type is ...:
            location_type = self.type
        else:
            location_type = validate_type(location_type)
        
        # Construct
        new = object.__new__(type(self))
        new.channel_id = channel_id
        new.guild_id = guild_id
        new.type = location_type
        return new
