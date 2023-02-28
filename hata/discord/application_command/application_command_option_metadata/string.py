__all__ = ('ApplicationCommandOptionMetadataString',)

from scarletio import copy_docs

from .constants import APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
from .fields import (
    parse_max_length, parse_min_length, put_max_length_into, put_min_length_into, validate_max_length,
    validate_min_length
)
from .primitive import ApplicationCommandOptionMetadataPrimitive


class ApplicationCommandOptionMetadataString(ApplicationCommandOptionMetadataPrimitive):
    """
    String parameter application command option metadata.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for the user to pick from.
    
    max_length : `int`
        The maximum input length allowed for this option.
    
    min_length : `int`
        The minimum input length allowed for this option.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    TYPE = str
    
    __slots__ = ('max_length', 'min_length')
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.__new__)
    def __new__(cls, keyword_parameters):
        # max_length
        try:
            max_length = keyword_parameters.pop('max_length')
        except KeyError:
            max_length = APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT
        else:
            max_length = validate_max_length(max_length)
        
        # min_length
        try:
            min_length = keyword_parameters.pop('min_length')
        except KeyError:
            min_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
        else:
            min_length = validate_min_length(min_length)
        
        # Construct
        new = ApplicationCommandOptionMetadataPrimitive.__new__(cls, keyword_parameters)
        new.max_length = max_length
        new.min_length = min_length
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.from_data)
    def from_data(cls, data):
        self = super(ApplicationCommandOptionMetadataString, cls).from_data(data)
        self.max_length = parse_max_length(data)
        self.min_length = parse_min_length(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.to_data)
    def to_data(self, *, defaults = False):
        data = ApplicationCommandOptionMetadataPrimitive.to_data(self, defaults = defaults)
        put_max_length_into(self.max_length, data, defaults)
        put_min_length_into(self.min_length, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        ApplicationCommandOptionMetadataPrimitive._add_type_specific_repr_fields(self, repr_parts)
        
        repr_parts.append(', max_length = ')
        repr_parts.append(repr(self.max_length))
        
        repr_parts.append(', min_length = ')
        repr_parts.append(repr(self.min_length))
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ApplicationCommandOptionMetadataPrimitive._is_equal_same_type(self, other):
            return False
        
        if self.max_length != other.max_length:
            return False
        
        if self.min_length != other.min_length:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.__hash__)
    def __hash__(self):
        hash_value = ApplicationCommandOptionMetadataPrimitive.__hash__(self)
        
        # max_length
        hash_value ^= self.max_length << 6
        
        # min_length
        hash_value ^= self.min_length  << 10
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.copy)
    def copy(self):
        new = ApplicationCommandOptionMetadataPrimitive.copy(self)
        new.max_length = self.max_length
        
        # min_length
        new.min_length = self.min_length
        
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.copy_with)
    def copy_with(self, keyword_parameters):
        # max_length
        try:
            max_length = keyword_parameters.pop('max_length')
        except KeyError:
            max_length = self.max_length
        else:
            max_length = validate_max_length(max_length)
        
        # min_length
        try:
            min_length = keyword_parameters.pop('min_length')
        except KeyError:
            min_length = self.min_length
        else:
            min_length = validate_min_length(min_length)
        
        # Construct
        new = ApplicationCommandOptionMetadataPrimitive.copy_with(self, keyword_parameters)
        new.max_length = max_length
        new.min_length = min_length
        return new
