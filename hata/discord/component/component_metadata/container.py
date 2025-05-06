__all__ = ('ComponentMetadataContainer', )

from scarletio import copy_docs

from .base import ComponentMetadataBase
from .fields import (
    parse_color, parse_components, parse_spoiler, put_color, put_components, put_spoiler, validate_color,
    validate_components__container, validate_spoiler
)


class ComponentMetadataContainer(ComponentMetadataBase):
    """
    Container component metadata.
    
    Attributes
    ----------
    color : ``None | Color``
        The color of the strip on the left.
    
    components : ``None | tuple<Component>``
        The contained components.
    
    spoiler : `bool`
        Whether the content of the component is spoilered.
    """
    __slots__ = ('color', 'components', 'spoiler')
    
    
    def __new__(cls, *, color = ..., components = ..., spoiler = ...):
        """
        Creates a new container component metadata.
        
        Parameters
        ----------
        color : ``None | int | Color``, Optional (Keywords only)
            The color of the strip on the left.
        
        components : ``None | iterable<Component | (tuple | list)<Component>>``, Optional (Keyword only)
            The contained components.
        
        spoiler : `bool`, Optional (Keyword only)
            Whether the content of the component is spoilered.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # color
        if color is ...:
            color = None
        else:
            color = validate_color(color)
        
        # components
        if components is ...:
            components = None
        else:
            components = validate_components__container(components)
        
        # spoiler
        if spoiler is ...:
            spoiler = False
        else:
            spoiler = validate_spoiler(spoiler)
        
        # Construct
        self = object.__new__(cls)
        self.color = color
        self.components = components
        self.spoiler = spoiler
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            color = keyword_parameters.pop('color', ...),
            components = keyword_parameters.pop('components', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
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
        
        # color
        color = self.color
        if (color is not None):
            repr_parts.append(', color = ')
            repr_parts.append(repr(color))
        
        # spoiler
        spoiler = self.spoiler
        if spoiler:
            repr_parts.append(', spoiler = ')
            repr_parts.append(repr(spoiler))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # color
        color = self.color
        if (color is not None):
            hash_value ^= 1 << 10
            hash_value ^= color
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components) << 12
            for component in components:
                hash_value ^= hash(component)
        
        # spoiler
        hash_value ^= self.spoiler << 19
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # color
        if self.color != other.color:
            return False
        
        # components
        if self.components != other.components:
            return False
        
        # spoiler
        if self.spoiler != other.spoiler:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.color = parse_color(data)
        self.components = parse_components(data)
        self.spoiler = parse_spoiler(data)
        
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_color(self.color, data, defaults)
        put_components(self.components, data, defaults, include_internals = include_internals)
        put_spoiler(self.spoiler, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # color
        new.color = self.color
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.clean_copy(guild) for component in self.components)
        
        new.components = components
        
        # spoiler
        new.spoiler = self.spoiler
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # color
        new.color = self.color
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        
        new.components = components
        
        # spoiler
        new.spoiler = self.spoiler
        
        return new
    
    
    def copy_with(self, *, color = ..., components = ..., spoiler = ...):
        """
        Copies the container component metadata with the given fields.
        
        Parameters
        ----------
        color : ``None | int | Color``, Optional (Keywords only)
            The color of the strip on the left.
        
        components : ``None | iterable<Component | (tuple | list)<Component>>``, Optional (Keyword only)
            The contained components.
        
        spoiler : `bool`, Optional (Keyword only)
            Whether the content of the component is spoilered.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # color
        if color is ...:
            color = self.color
        else:
            color = validate_color(color)
        
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = tuple(component.copy() for component in self.components)
        else:
            components = validate_components__container(components)
        
        # spoiler
        if spoiler is ...:
            spoiler = self.spoiler
        else:
            spoiler = validate_spoiler(spoiler)
        
        # Construct
        new = object.__new__(type(self))
        new.color = color
        new.components = components
        new.spoiler = spoiler
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            color = keyword_parameters.pop('color', ...),
            components = keyword_parameters.pop('components', ...),
            spoiler = keyword_parameters.pop('spoiler', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.iter_contents)
    def iter_contents(self):
        components = self.components
        if (components is not None):
            for component in components:
                yield from component.iter_contents()
