__all__ = ('ComponentMetadataStringSelect', )

from scarletio import copy_docs

from .fields import parse_options, put_options_into, validate_options
from .select_base import ComponentMetadataSelectBase


class ComponentMetadataStringSelect(ComponentMetadataSelectBase):
    """
    String select component metadata.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which component was used by the user.
    
    enabled : `bool`
        Whether the component is enabled.
    
    max_values : `int
        The maximal amount of options to select.
    
    min_values : `int`
        The minimal amount of options to select.
    
    options : `None`, `tuple` of ``StringSelectOption``
        Options of the select.
    
    placeholder : `None`, `str`
        Placeholder text of the select.
    """
    __slots__ = ('options', )
    
    
    def __new__(
        cls,
        *,
        custom_id = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        options = ...,
        placeholder = ...,
    ):
        """
        Creates a new string select component metadata with the given parameters.
        
        Parameters
        ----------
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : `None`, `iterable` of ``StringSelectOption``, Optional (Keyword only)
            Options of the select.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder text of the select.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # Construct
        self = ComponentMetadataSelectBase.__new__(
            cls,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        self.options = options
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            options = keyword_parameters.pop('options', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
    
    
    @copy_docs(ComponentMetadataSelectBase._add_type_specific_repr_fields_into)
    def _add_type_specific_repr_fields_into(self, repr_parts):
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
    
    
    @copy_docs(ComponentMetadataSelectBase.__hash__)
    def __hash__(self):
        hash_value = ComponentMetadataSelectBase.__hash__(self)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 12
            for option in options:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataSelectBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ComponentMetadataSelectBase._is_equal_same_type(self, other):
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_data)
    def from_data(cls, data):
        self = super(ComponentMetadataStringSelect, cls).from_data(data)
        self.options = parse_options(data)
        return self
    
    
    @copy_docs(ComponentMetadataSelectBase.to_data)
    def to_data(self, *, defaults = False):
        data =  ComponentMetadataSelectBase.to_data(self)
        
        put_options_into(self.options, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataSelectBase.copy)
    def copy(self):
        new = ComponentMetadataSelectBase.copy(self)
        
        # options
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        new.options = options
        
        return new
    
    
    def copy_with(
        self,
        *,
        custom_id = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        options = ...,
        placeholder = ...,
    ):
        """
        Copies the channel select component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : `None`, `iterable` of ``StringSelectOption``, Optional (Keyword only)
            Options of the select.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder text of the select.
        
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
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = tuple(option.copy() for option in options)
        else:
            options = validate_options(options)
        
        # Construct
        new = ComponentMetadataSelectBase.copy_with(
            self,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        new.options = options
        return new
    
    
    @copy_docs(ComponentMetadataSelectBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            options = keyword_parameters.pop('options', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
