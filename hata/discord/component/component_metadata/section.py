__all__ = ('ComponentMetadataSection', )

from scarletio import copy_docs

from .base import ComponentMetadataBase
from .fields import (
    parse_components, parse_thumbnail, put_components, put_thumbnail, validate_components__section, validate_thumbnail
)


class ComponentMetadataSection(ComponentMetadataBase):
    """
    Section component metadata.
    
    Attributes
    ----------
    components : ``None | tuple<Component>``
        The contained components.
    
    thumbnail : ``None | Component``
        The thumbnail or other accessory (button).
    """
    __slots__ = ('components', 'thumbnail')
    
    
    def __new__(cls, *, components = ..., thumbnail = ...):
        """
        Creates a new section component metadata.
        
        Parameters
        ----------
        components : ``None | iterable<Component | (tuple | list)<Component>>``, Optional (Keyword only)
            The contained components.
        
        thumbnail : ``None | Component``, Optional (Keyword only)
            The thumbnail or other accessory (button).
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # components
        if components is ...:
            components = None
        else:
            components = validate_components__section(components)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = None
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # Construct
        self = object.__new__(cls)
        self.components = components
        self.thumbnail = thumbnail
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            components = keyword_parameters.pop('components', ...),
            thumbnail = keyword_parameters.pop('thumbnail', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # sub-component fields : components
        
        # components
        repr_parts.append(' components = ')
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
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            repr_parts.append(', thumbnail = ')
            repr_parts.append(repr(thumbnail))
        
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
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            hash_value ^= 1 << 14
            hash_value ^= hash(thumbnail)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # components
        if self.components != other.components:
            return False
        
        # thumbnail
        if self.thumbnail != other.thumbnail:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.components = parse_components(data)
        self.thumbnail = parse_thumbnail(data)
        
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_components(self.components, data, defaults, include_internals = include_internals)
        put_thumbnail(self.thumbnail, data, defaults, include_internals = include_internals)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.clean_copy(guild) for component in self.components)
        
        new.components = components
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            thumbnail = thumbnail.clean_copy(guild)
        
        new.thumbnail = thumbnail
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        
        new.components = components
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            thumbnail = thumbnail.copy()
        
        new.thumbnail = thumbnail
        
        return new
    
    
    def copy_with(self, *, components = ..., thumbnail = ...):
        """
        Copies the section component metadata with the given fields.
        
        Parameters
        ----------
        components : ``None | iterable<Component | (tuple | list)<Component>>``, Optional (Keyword only)
            The contained components.
        
        thumbnail : ``None | Component``, Optional (Keyword only)
            The thumbnail or other accessory (button).
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = tuple(component.copy() for component in self.components)
        else:
            components = validate_components__section(components)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = self.thumbnail
            if (thumbnail is not None):
                thumbnail = thumbnail.copy()
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # Construct
        
        new = object.__new__(type(self))
        new.components = components
        new.thumbnail = thumbnail
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            components = keyword_parameters.pop('components', ...),
            thumbnail = keyword_parameters.pop('thumbnail', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.iter_contents)
    def iter_contents(self):
        components = self.components
        if (components is not None):
            for component in components:
                yield from component.iter_contents()

