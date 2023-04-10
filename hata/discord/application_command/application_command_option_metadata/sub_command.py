__all__ = ('ApplicationCommandOptionMetadataSubCommand',)

from scarletio import copy_docs

from .fields import parse_default, put_default_into, validate_default
from .nested import ApplicationCommandOptionMetadataNested


class ApplicationCommandOptionMetadataSubCommand(ApplicationCommandOptionMetadataNested):
    """
    Sub-command parameter application command option metadata.
    
    Attributes
    ----------
    default : `bool`
        Whether the option is the default one.
    
    options : `None`, `tuple` of ``ApplicationCommandOption``
        Contains the option's parameter or its sub-commands (or groups).
    """
    __slots__ = ('default',)
    
    
    def __new__(cls, *, default = ..., options = ...):
        """
        Creates a new sub-command application command option metadata with the given parameters.
        
        Parameters
        ----------
        default : `bool`, Optional (Keyword only)
            Whether the option is the default one.
        
        options : `None`, `iterable` of ``ApplicationCommandOption``, Optional (Keyword only)
            Contains the option's parameter or its sub-commands (or groups).
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # default
        if default is ...:
            default = False
        else:
            default = validate_default(default)
        
        # Construct
        new = ApplicationCommandOptionMetadataNested.__new__(
            cls, 
            options = options,
        )
        new.default = default
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataNested.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            default = keyword_parameters.pop('default', ...),
            options = keyword_parameters.pop('options', ...),
        )
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataNested.from_data)
    def from_data(cls, data):
        self = super(ApplicationCommandOptionMetadataSubCommand, cls).from_data(data)
        self.default = parse_default(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested.to_data)
    def to_data(self, *, defaults = False):
        data = ApplicationCommandOptionMetadataNested.to_data(self, defaults = defaults)
        put_default_into(self.default, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        ApplicationCommandOptionMetadataNested._add_type_specific_repr_fields(self, repr_parts)
        
        repr_parts.append(', default = ')
        repr_parts.append(repr(self.default))
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ApplicationCommandOptionMetadataNested._is_equal_same_type(self, other):
            return False
        
        if self.default != other.default:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested.__hash__)
    def __hash__(self):
        hash_value = ApplicationCommandOptionMetadataNested.__hash__(self)
        
        # default
        hash_value ^= self.default << 13
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested.copy)
    def copy(self):
        new = ApplicationCommandOptionMetadataNested.copy(self)
        new.default = self.default
        return new
    
    
    def copy_with(self, *, default = ..., options = ...):
        """
        Copies the sub-command application command option metadata with the given fields.
        
        Parameters
        ----------
        default : `bool`, Optional (Keyword only)
            Whether the option is the default one.
        
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
        # default
        if default is ...:
            default = self.default
        else:
            default = validate_default(default)
        
        # Construct
        new = ApplicationCommandOptionMetadataNested.copy_with(
            self,
            options = options,
        )
        new.default = default
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            default = keyword_parameters.pop('default', ...),
            options = keyword_parameters.pop('options', ...),
        )
