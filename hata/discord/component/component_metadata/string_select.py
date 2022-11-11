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
    
    placeholder : `None`, `str`
        Placeholder text of the select.
    
    options : `None`, `tuple` of ``ComponentSelectOption``
        Options of the select.
    """
    __slots__ = ('options', )
    
    @copy_docs(ComponentMetadataSelectBase.__new__)
    def __new__(cls, keyword_parameters):
        # options
        try:
            options = keyword_parameters.pop('options')
        except KeyError:
            options = None
        else:
            options = validate_options(options)
        
        # Construct
        self = ComponentMetadataSelectBase.__new__(cls, keyword_parameters)
        self.options = options
        
        return self
    
    
    @copy_docs(ComponentMetadataSelectBase._add_type_specific_repr_fields_into)
    def _add_type_specific_repr_fields_into(self, repr_parts):
        # options
        repr_parts.append(', options=')
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
    
    
    @copy_docs(ComponentMetadataSelectBase.copy_with)
    def copy_with(self, keyword_parameters):
        # options
        try:
            options = keyword_parameters.pop('options')
        except KeyError:
            options = self.options
            if (options is not None):
                options = tuple(option.copy() for option in options)
        else:
            options = validate_options(options)
        
        # Construct
        
        new = ComponentMetadataSelectBase.copy_with(self, keyword_parameters)
        new.options = options
        return new
