__all__ = ('ComponentMetadataCheckbox', )

from scarletio import copy_docs

from ..shared_fields import parse_default, put_default, validate_default
from ..shared_helpers import create_auto_custom_id

from .base import ComponentMetadataBase
from .fields import parse_custom_id, put_custom_id, validate_custom_id


class ComponentMetadataCheckbox(ComponentMetadataBase):
    """
    Checkbox component metadata.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was used by the user.
    
    default : `bool`
        Whether the checkbox is checked by default.
    """
    __slots__ = ('custom_id', 'default')
    
    
    def __new__(
        cls,
        *,
        custom_id = ...,
        default = ...,
    ):
        """
        Creates a new checkbox component metadata with the given parameters.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        default : `None | bool`, Optional (Keyword only)
            Whether the checkbox is checked by default.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # default
        if default is ...:
            default = False
        else:
            default = validate_default(default)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.default = default
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
            default = keyword_parameters.pop('default', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # custom_id
        repr_parts.append(' custom_id = ')
        repr_parts.append(repr(self.custom_id))
        
        # Optional descriptive fields: default
        
        # default
        default = self.default
        if default:
            repr_parts.append(', default = ')
            repr_parts.append(repr(default))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # default
        hash_value ^= (self.default << 28)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # default
        if self.default != other.default:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        self.default = parse_default(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_custom_id(self.custom_id, data, defaults)
        put_default(self.default, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # default
        new.default = self.default
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # default
        new.default = self.default
        
        return new
    
    
    def copy_with(
        self,
        *,
        custom_id = ...,
        default = ...,
    ):
        """
        Copies the checkbox component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        default : `None | bool`, Optional (Keyword only)
            Whether the checkbox is checked by default.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # default
        if default is ...:
            default = self.default
        else:
            default = validate_default(default)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.default = default
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
            default = keyword_parameters.pop('default', ...),
        )
