__all__ = ('ApplicationCommandOptionMetadataSubCommand',)

from scarletio import copy_docs

from .fields import parse_default, put_default_into, validate_default
from .nested import ApplicationCommandOptionMetadataNested


class ApplicationCommandOptionMetadataSubCommand(ApplicationCommandOptionMetadataNested):
    """
    Sub-command parameter application command option metadata.
    
    Parameters
    ----------
    default : `bool`
        Whether the option is the default one.
    
    options : `None`, `tuple` of ``ApplicationCommandOption``
        Contains the option's parameter or its sub-commands (or groups).
    """
    __slots__ = ('default',)
    
    @copy_docs(ApplicationCommandOptionMetadataNested.__new__)
    def __new__(cls, keyword_parameters):
        # default
        try:
            default = keyword_parameters.pop('default')
        except KeyError:
            default = False
        else:
            default = validate_default(default)
        
        # Construct
        new = ApplicationCommandOptionMetadataNested.__new__(cls, keyword_parameters)
        new.default = default
        return new
    
    
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
    
    
    @copy_docs(ApplicationCommandOptionMetadataNested.copy_with)
    def copy_with(self, keyword_parameters):
        # default
        try:
            default = keyword_parameters.pop('default')
        except KeyError:
            default = self.default
        else:
            default = validate_default(default)
        
        # Construct
        new = ApplicationCommandOptionMetadataNested.copy_with(self, keyword_parameters)
        new.default = default
        return new
