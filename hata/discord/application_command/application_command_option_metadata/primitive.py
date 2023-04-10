__all__ = ('ApplicationCommandOptionMetadataPrimitive',)

from scarletio import copy_docs

from .fields import (
    parse_autocomplete, parse_choices, put_autocomplete_into, put_choices_into, validate_autocomplete,
    validate_choices_postprocessed
)
from .parameter import ApplicationCommandOptionMetadataParameter


class ApplicationCommandOptionMetadataPrimitive(ApplicationCommandOptionMetadataParameter):
    """
    Base type for primitive parameter application command option metadatas.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for the user to pick from.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    TYPE = object
    
    __slots__ = ('autocomplete', 'choices')
    
    
    def __new__(cls, *, autocomplete = ..., choices = ..., required = ...):
        """
        Creates a new primitive application command option metadata with the given parameters.
        
        Parameters
        ----------
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            Choices for the user to pick from.
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # autocomplete
        if autocomplete is ...:
            autocomplete = False
        else:
            autocomplete = validate_autocomplete(autocomplete)
        
        # choices
        if choices is ...:
            choices = None
        else:
            choices = validate_choices_postprocessed(choices, cls.TYPE)
        
        # Construct
        new = ApplicationCommandOptionMetadataParameter.__new__(
            cls,
            required = required,
        )
        new.autocomplete = autocomplete
        new.choices = choices
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataParameter.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            autocomplete = keyword_parameters.pop('autocomplete', ...),
            choices = keyword_parameters.pop('choices', ...),
            required = keyword_parameters.pop('required', ...),
        )
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataParameter.from_data)
    def from_data(cls, data):
        self = super(ApplicationCommandOptionMetadataPrimitive, cls).from_data(data)
        self.autocomplete = parse_autocomplete(data)
        self.choices = parse_choices(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.to_data)
    def to_data(self, *, defaults = False):
        data = ApplicationCommandOptionMetadataParameter.to_data(self, defaults = defaults)
        put_autocomplete_into(self.autocomplete, data, defaults)
        put_choices_into(self.choices, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        ApplicationCommandOptionMetadataParameter._add_type_specific_repr_fields(self, repr_parts)
        
        repr_parts.append(', autocomplete = ')
        repr_parts.append(repr(self.autocomplete))
        
        repr_parts.append(', choices = ')
        repr_parts.append(repr(self.choices))
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ApplicationCommandOptionMetadataParameter._is_equal_same_type(self, other):
            return False
        
        if self.autocomplete != other.autocomplete:
            return False
        
        if self.choices != other.choices:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.__hash__)
    def __hash__(self):
        hash_value = ApplicationCommandOptionMetadataParameter.__hash__(self)
        
        # autocomplete
        hash_value ^= self.autocomplete << 1
        
        # choices
        choices = self.choices
        if (choices is not None):
            hash_value ^= len(choices) << 1
            
            for choice in choices:
                hash_value ^= hash(choice)
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.copy)
    def copy(self):
        new = ApplicationCommandOptionMetadataParameter.copy(self)
        new.autocomplete = self.autocomplete
        
        # choices
        choices = self.choices
        if (choices is not None):
            choices = (*(choice.copy() for choice in choices),)
        new.choices = choices
        
        return new
    
    
    def copy_with(self, *, autocomplete = ..., choices = ..., required = ...):
        """
        Copies the primitive application command option metadata with the given fields.
        
        Parameters
        ----------
        autocomplete : `bool`, Optional (Keyword only)
            Whether the option supports auto completion.
        
        choices : `None`, `iterable` of ``ApplicationCommandOptionChoice``, Optional (Keyword only)
            Choices for the user to pick from.
        
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
        # autocomplete
        if autocomplete is ...:
            autocomplete = self.autocomplete
        else:
            autocomplete = validate_autocomplete(autocomplete)
        
        # choices
        if choices is ...:
            choices = self.choices
            if (choices is not None):
                choices = (*(choice.copy() for choice in choices),)
        else:
            choices = validate_choices_postprocessed(choices, type(self).TYPE)
        
        # Construct
        new = ApplicationCommandOptionMetadataParameter.copy_with(
            self,
            required = required,
        )
        new.autocomplete = autocomplete
        new.choices = choices
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            autocomplete = keyword_parameters.pop('autocomplete', ...),
            choices = keyword_parameters.pop('choices', ...),
            required = keyword_parameters.pop('required', ...),
        )
