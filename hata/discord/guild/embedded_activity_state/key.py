__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_application_id, parse_channel_id, parse_guild_id, put_application_id_into, put_channel_id_into,
    put_guild_id_into, validate_application_id, validate_channel_id, validate_guild_id
)


class EmbeddedActivityStateKey(RichAttributeErrorBaseType):
    """
    Used as a key of an embedded activity.
    
    Attributes
    ----------
    application_id : `int`
        The embedded activity's application's identifier.
    channel_id : `int`
        The embedded activity's channel's identifier.
    guild_id : `int`
        The embedded activity's guild's identifier.
    """
    __slots__ = ('application_id', 'channel_id', 'guild_id')
    
    def __new__(cls, guild_id, channel_id, application_id):
        """
        Creates a new embedded activity state.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``
            The embedded activity's guild or its identifier.
        channel_id : `int`, ``Channel``
            The embedded activity's channel or its identifier.
        application_id : `int`, ``Application``
            The embedded activity's application or its identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        application_id = validate_application_id(application_id)
        channel_id = validate_channel_id(channel_id)
        guild_id = validate_guild_id(guild_id)
        
        # Construct
        self = object.__new__(cls)
        self.application_id = application_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id):
        """
        Creates a new embedded activity key from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received data.
        guild_id : `int`
            The guild's identifier where the activity is.
            If given as `0`, will try to pull it from the given data instead.
        
        Returns
        -------
        self : `instance<cls>`
        """
        if not guild_id:
            guild_id = parse_guild_id(data)
        
        channel_id = parse_channel_id(data)
        application_id = parse_application_id(data)
        
        # Construct
        self = object.__new__(cls)
        self.application_id = application_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the embedded activity state key into it's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_application_id_into(self.application_id, data, defaults)
        put_channel_id_into(self.channel_id, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the embedded activity key's representation."""
        repr_parts = [self.__class__.__name__, '(']
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # channel_id
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        # application_id
        repr_parts.append(', application_id = ')
        repr_parts.append(repr(self.application_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the embedded activity key's hash value."""
        hash_value = 0
        
        # application_id
        hash_value ^= self.application_id
        
        # channel_id
        hash_value ^= self.channel_id
        
        # guild_id
        hash_value ^= self.guild_id
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity keys are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking."""
        return 3
    
    
    def __iter__(self):
        """Unpacks the embedded activity key in order of `guild_id`, `channel_id`, `application_id`."""
        yield self.guild_id
        yield self.channel_id
        yield self.application_id
    
    
    def copy(self):
        """
        Copies the embedded activity key.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.application_id = self.application_id
        new.channel_id = self.channel_id
        new.guild_id = self.guild_id
        return new
    
    
    def copy_with(self, *, application_id = ..., channel_id = ..., guild_id = ...):
        """
        Copies the embedded activity key with the given fields.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The embedded activity's guild or its identifier.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The embedded activity's channel or its identifier.
        application_id : `int`, ``Application``, Optional (Keyword only)
            The embedded activity's application or its identifier.
        
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
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
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
        
        new = object.__new__(type(self))
        new.application_id = application_id
        new.channel_id = channel_id
        new.guild_id = guild_id
        return new
