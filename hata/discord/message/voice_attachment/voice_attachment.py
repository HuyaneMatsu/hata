__all__ = ('VoiceAttachment',)

from scarletio import RichAttributeErrorBaseType

from .constants import WAVEFORM_OGG_DEFAULT
from .fields import (
    put_description, put_duration, put_waveform, validate_description, validate_duration, validate_name,
    validate_waveform
)


class VoiceAttachment(RichAttributeErrorBaseType):
    """
    Voice attachment to be attachable to a message.
    
    Attributes
    ----------
    description : `None | str`
        Description for the attachment.
    
    duration : `float`
        The attachment's duration in seconds.
    
    io : `object`
        Data or stream to be sent.
    
    name : `str`
        The name of the attachment.
    
    waveform : `bytes`
        Represents a sampled waveform of the attached voice data.
    """
    __slots__ = ('description', 'duration', 'io', 'name', 'waveform')
    
    def __new__(cls, name, io, duration, *, description = ..., waveform = ...):
        """
        Creates a new voice attachment.
        
        Parameters
        ----------
        name : `str`
            The name of the attachment.
        
        io : `object`
            Data or stream to be sent.
        
        duration : `float`
            The attachment's duration in seconds.
        
        description : `None | str`, Optional (Keyword only)
            Description for the attachment.
        
        waveform : `None | bytes`, Optional (Keyword only)
            Represents a sampled waveform of the attached voice data.
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
            - If `waveform` is not given and could not interpret the default waveform.
        TypeError
            - If a parameter's type is incorrect.
        """
        # name
        name = validate_name(name)
        
        # duration
        duration = validate_duration(duration)
        
        # description
        if description is ...:
            description = None
        
        else:
            description = validate_description(description)
        
        # waveform
        if waveform is ...:
            waveform = None
        else:
            waveform = validate_waveform(waveform)
        
        # Post validate waveform.
        if waveform is None:
            if name.endswith('.ogg'):
                waveform = WAVEFORM_OGG_DEFAULT
            
            else:
                raise ValueError(
                    f'Could not interpret default `waveform` from `name` ({name!r}), please pass it manually.'
                )
        
        # Construct
        self = object.__new__(cls)
        self.description = description
        self.duration = duration
        self.io = io
        self.name = name
        self.waveform = waveform
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # duration
        repr_parts.append(', duration = ')
        repr_parts.append(repr(self.duration))
        
        # type(io)
        repr_parts.append(', type(io) = ')
        repr_parts.append(type(self.io).__name__)
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        # waveform
        repr_parts.append(', waveform = ')
        repr_parts.append(repr(self.waveform))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # duration
        hash_value ^= hash(self.duration)
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # io
        io = self.io
        try:
            io_hash = hash(io)
        except TypeError:
            io_hash = object.__hash__(io)
        
        hash_value ^= io_hash
        
        # name
        hash_value ^= hash(self.name)
        
        # waveform
        hash_value ^= hash(self.waveform)
        
        return hash_value
        
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # description
        if self.description != other.description:
            return False
        
        # duration
        if self.duration != other.duration:
            return False
        
        # io
        if self.io != other.io:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # waveform:
        if self.waveform != other.waveform:
            return False
        
        return True
    
    
    def copy(self):
        """
        Returns a copy of the voice attachment.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.description = self.description
        new.duration = self.duration
        new.io = self.io
        new.name = self.name
        new.waveform = self.waveform
        return new
    
    
    def copy_with(self, *, description = ..., duration = ..., io = ..., name = ..., waveform = ...):
        """
        Copies the voice attachment with the given fields.
        
        Parameters
        ----------
        description : `None | str`, Optional (Keyword only)
            Description for the attachment.
        
        duration : `float`, Optional (Keyword only)
            The attachment's duration in seconds.
        
        io : `object`, Optional (Keyword only)
            Data or stream to be sent.
        
        name : `str`, Optional (Keyword only)
            The name of the attachment.
        
        waveform : `None | bytes`, Optional (Keyword only)
            Represents a sampled waveform of the attached voice data.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
            - If `waveform` is not given and could not interpret the default waveform.
        TypeError
            - If a parameter's type is incorrect.
        """
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # duration
        if duration is ...:
            duration = self.duration
        else:
            duration = validate_duration(duration)
        
        # io
        if io is ...:
            io = self.io
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # waveform
        if waveform is ...:
            waveform = self.waveform
        else:
            waveform = validate_waveform(waveform)
        
        # Post validate waveform.
        if waveform is None:
            if name.endswith('.ogg'):
                waveform = WAVEFORM_OGG_DEFAULT
            
            else:
                raise ValueError(
                    f'Could not interpret default `waveform` from `name` ({name!r}), please pass it manually.'
                )
        
        # Construct
        new = object.__new__(type(self))
        new.description = description
        new.duration = duration
        new.io = io
        new.name = name
        new.waveform = waveform
        return new
    
    
    def to_data(self):
        """
        Converts the voice attachment to json serializable object.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {
            'id': '0',
        }
        
        put_duration(self.duration, data, False)
        put_description(self.description, data, False)
        put_waveform(self.waveform, data, False)
        return data
