__all__ = ('ComponentMetadataRow', )

from scarletio import copy_docs

from ..shared_fields import parse_components, put_components_into, validate_components

from .base import ComponentMetadataBase


class ComponentMetadataRow(ComponentMetadataBase):
    """
    Row component metadata.
    
    Attributes
    ----------
    components : `None`, `tuple` of ``Component``
        The contained components.
    """
    __slots__ = ('components',)
    
    @copy_docs(ComponentMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # components
        try:
            components = keyword_parameters.pop('components')
        except KeyError:
            components = None
        else:
            components = validate_components(components)
        
        self = object.__new__(cls)
        self.components = components
        return self
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # sub-component fields : components
        
        # components
        repr_parts.append(' components=')
        components = self.components
        if (components is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(components)
            
            while True:
                component = components[index]
                index += 1
                
                repr_parts.append(repr(component))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components) << 12
            for component in components:
                hash_value ^= hash(component)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.components = parse_components(data)
        
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data =  {}
        
        put_components_into(self.components, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        
        new.components = components
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with)
    def copy_with(self, keyword_parameters):
        # components
        try:
            components = keyword_parameters.pop('components')
        except KeyError:
            components = self.components
            if (components is not None):
                components = tuple(component.copy() for component in self.components)
        else:
            components = validate_components(components)
        
        # Construct
        
        new = object.__new__(type(self))
        new.components = components
        return new
