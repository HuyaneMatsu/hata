__all__ = ('ApplicationCommandOptionMetadataNumeric',)

from scarletio import copy_docs

from .fields import (
    parse_max_value, parse_min_value, put_max_value_into, put_min_value_into, validate_max_value_postprocessed,
    validate_min_value_postprocessed
)
from .primitive import ApplicationCommandOptionMetadataPrimitive


class ApplicationCommandOptionMetadataNumeric(ApplicationCommandOptionMetadataPrimitive):
    """
    Base type for numeric parameter application command option metadatas.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for the user to pick from.
    
    max_value : `None`, `float`, `int`
        The maximal value permitted for this option.
    
    min_value : `None`, `float`, ``int`
        The minimum value permitted for this option.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    __slots__ = ('max_value', 'min_value')
    
    
    def __new__(cls, *, autocomplete = ..., choices = ..., max_value = ..., min_value = ..., required = ...):
        """
        Creates a new numeric application command option metadata with the given parameters.
        
        Parameters
        ----------
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            Choices for the user to pick from.
        
        max_value : `None`, `float`, `int`, Optional (Keyword only)
            The maximal value permitted for this option.
        
        min_value : `None`, `float`, ``int`, Optional (Keyword only)
            The minimum value permitted for this option.
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # max_value
        if max_value is ...:
            max_value = None
        else:
            max_value = validate_max_value_postprocessed(max_value, cls.TYPE)
        
        # min_value
        if min_value is ...:
            min_value = None
        else:
            min_value = validate_min_value_postprocessed(min_value, cls.TYPE)
        
        # Construct
        new = ApplicationCommandOptionMetadataPrimitive.__new__(
            cls,
            autocomplete = autocomplete,
            choices = choices,
            required = required,
        )
        new.max_value = max_value
        new.min_value = min_value
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            autocomplete = keyword_parameters.pop('autocomplete', ...),
            choices = keyword_parameters.pop('choices', ...),
            max_value = keyword_parameters.pop('max_value', ...),
            min_value = keyword_parameters.pop('min_value', ...),
            required = keyword_parameters.pop('required', ...),
        )
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.from_data)
    def from_data(cls, data):
        self = super(ApplicationCommandOptionMetadataNumeric, cls).from_data(data)
        self.max_value = parse_max_value(data)
        self.min_value = parse_min_value(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.to_data)
    def to_data(self, *, defaults = False):
        data = ApplicationCommandOptionMetadataPrimitive.to_data(self, defaults = defaults)
        put_max_value_into(self.max_value, data, defaults)
        put_min_value_into(self.min_value, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        ApplicationCommandOptionMetadataPrimitive._add_type_specific_repr_fields(self, repr_parts)
        
        repr_parts.append(', max_value = ')
        repr_parts.append(repr(self.max_value))
        
        repr_parts.append(', min_value = ')
        repr_parts.append(repr(self.min_value))
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ApplicationCommandOptionMetadataPrimitive._is_equal_same_type(self, other):
            return False
        
        if self.max_value != other.max_value:
            return False
        
        if self.min_value != other.min_value:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.__hash__)
    def __hash__(self):
        hash_value = ApplicationCommandOptionMetadataPrimitive.__hash__(self)
        
        # max_value
        hash_value ^= hash(self.max_value) << 6
        
        # min_value
        hash_value ^= hash(self.min_value) << 10
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.copy)
    def copy(self):
        new = ApplicationCommandOptionMetadataPrimitive.copy(self)
        new.max_value = self.max_value
        
        # min_value
        new.min_value = self.min_value
        
        return new
    
    
    def copy_with(self, *, autocomplete = ..., choices = ..., max_value = ..., min_value = ..., required = ...):
        """
        Copies the numeric application command option metadata with the given fields.
        
        Parameters
        ----------
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            Choices for the user to pick from.
        
        max_value : `None`, `float`, `int`, Optional (Keyword only)
            The maximal value permitted for this option.
        
        min_value : `None`, `float`, ``int`, Optional (Keyword only)
            The minimum value permitted for this option.
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # max_value
        if max_value is ...:
            max_value = self.max_value
        else:
            max_value = validate_max_value_postprocessed(max_value, type(self).TYPE)
        
        # min_value
        if min_value is ...:
            min_value = self.min_value
        else:
            min_value = validate_min_value_postprocessed(min_value, type(self).TYPE)
        
        # Construct
        new = ApplicationCommandOptionMetadataPrimitive.copy_with(
            self,
            autocomplete = autocomplete,
            choices = choices,
            required = required,
        )
        new.max_value = max_value
        new.min_value = min_value
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataPrimitive.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            autocomplete = keyword_parameters.pop('autocomplete', ...),
            choices = keyword_parameters.pop('choices', ...),
            max_value = keyword_parameters.pop('max_value', ...),
            min_value = keyword_parameters.pop('min_value', ...),
            required = keyword_parameters.pop('required', ...),
        )
