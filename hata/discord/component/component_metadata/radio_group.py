__all__ = ('ComponentMetadataRadioGroup', )

from scarletio import copy_docs

from ..shared_helpers import create_auto_custom_id

from .base import ComponentMetadataBase
from .fields import (
    parse_custom_id, parse_options__radio_group, parse_required, put_custom_id, put_options__radio_group, put_required,
    validate_custom_id, validate_options__radio_group, validate_required
)


class ComponentMetadataRadioGroup(ComponentMetadataBase):
    """
    Radio group component metadata.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was used by the user.
    
    options : ``None | tuple<RadioGroupOption>``
        Options of the radio group.
    
    required : `bool`
        Whether the field is required to be fulfilled.
    """
    __slots__ = ('custom_id', 'options', 'required', )
    
    
    def __new__(
        cls,
        *,
        custom_id = ...,
        options = ...,
        required = ...,
    ):
        """
        Creates a new radio group component metadata with the given parameters.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        options : `None`, `iterable` of ``RadioGroupOption``, Optional (Keyword only)
            Options of the radio group.
        
        required : `None | bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
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
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options__radio_group(options)
        
        # required
        if required is ...:
            required = False
        else:
            required = validate_required(required)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.options = options
        self.required = required
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
            options = keyword_parameters.pop('options', ...),
            required = keyword_parameters.pop('required', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # custom_id
        repr_parts.append(' custom_id = ')
        repr_parts.append(repr(self.custom_id))
        
        # options
        repr_parts.append(', options = ')
        options = self.options
        if (options is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # Optional descriptive fields: required
        
        # required
        required = self.required
        if required:
            repr_parts.append(', required = ')
            repr_parts.append(repr(required))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 12
            for option in options:
                hash_value ^= hash(option)
        
        # required
        if self.required:
            hash_value ^= (1 << 28)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        # required
        if self.required != other.required:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        self.options = parse_options__radio_group(data)
        self.required = parse_required(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_custom_id(self.custom_id, data, defaults)
        put_options__radio_group(self.options, data, defaults)
        put_required(self.required, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # options
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        new.options = options
        
        # required
        new.required = self.required
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # options
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        new.options = options
        
        # required
        new.required = self.required
        
        return new
    
    
    def copy_with(
        self,
        *,
        custom_id = ...,
        options = ...,
        required = ...,
    ):
        """
        Copies the radio group component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        options : `None`, `iterable` of ``RadioGroupOption``, Optional (Keyword only)
            Options of the radio group.
        
        required : `None | bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
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
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = tuple(option.copy() for option in options)
        else:
            options = validate_options__radio_group(options)
        
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.options = options
        new.required = required
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
            options = keyword_parameters.pop('options', ...),
            required = keyword_parameters.pop('required', ...),
        )
