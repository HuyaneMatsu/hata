__all__ = ('ApplicationCommandOptionMetadataNested',)

from scarletio import copy_docs

from .base import ApplicationCommandOptionMetadataBase
from .fields import parse_options, put_options_into, validate_options


class ApplicationCommandOptionMetadataNested(ApplicationCommandOptionMetadataBase):
    """
    Base type for nested application command option metadatas.
    
    Attributes
    ----------
    options : `None`, `tuple` of ``ApplicationCommandOption``
        Contains the option's parameter or its sub-commands (or groups).
    """
    __slots__ = ('options',)
    
    
    def __new__(cls, *, options = ...):
        """
        Creates a new nested application command option metadata with the given parameters.
        
        Parameters
        ----------
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            Contains the option's parameter or its sub-commands (or groups).
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # Construct
        new = object.__new__(cls)
        new.options = options
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            options = keyword_parameters.pop('options', ...),
        )
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.options = parse_options(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_options_into(self.options, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        repr_parts.append(' options = ')
        repr_parts.append(repr(self.options))
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.options != other.options:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 10
            
            for option in options:
                hash_value ^= hash(options)
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        return new
    
    
    def copy_with(self, *, options = ...):
        """
        Copies the nested application command option metadata with the given fields.
        
        Parameters
        ----------
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            Contains the option's parameter or its sub-commands (or groups).
        
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
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # Construct
        new = object.__new__(type(self))
        new.options = options
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            options = keyword_parameters.pop('options', ...),
        )
