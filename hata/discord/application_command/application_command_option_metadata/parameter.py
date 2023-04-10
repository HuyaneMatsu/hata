__all__ = ('ApplicationCommandOptionMetadataParameter',)

from scarletio import copy_docs

from .base import ApplicationCommandOptionMetadataBase
from .fields import parse_required, put_required_into, validate_required


class ApplicationCommandOptionMetadataParameter(ApplicationCommandOptionMetadataBase):
    """
    Base type for parameter application command option metadatas.
    
    Attributes
    ----------
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    __slots__ = ('required',)
    
    
    def __new__(cls, *, required = ...):
        """
        Creates a new parameter application command option metadata with the given parameters.
        
        Parameters
        ----------
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # required
        if required is ...:
            required = False
        else:
            required = validate_required(required)
        
        # Construct
        new = object.__new__(cls)
        new.required = required
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            required = keyword_parameters.pop('required', ...),
        )
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.required = parse_required(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_required_into(self.required, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        repr_parts.append(' required = ')
        repr_parts.append(repr(self.required))
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.required != other.required:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # required
        hash_value ^= self.required << 1
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.required = self.required
        return new
    
    
    def copy_with(self, *, required = ...):
        """
        Copies the parameter application command option metadata with the given fields.
        
        Parameters
        ----------
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
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        # Construct
        new = object.__new__(type(self))
        new.required = required
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            required = keyword_parameters.pop('required', ...),
        )
