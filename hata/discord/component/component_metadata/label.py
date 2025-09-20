__all__ = ('ComponentMetadataLabel', )

from scarletio import copy_docs

from .base import ComponentMetadataBase
from .fields import (
    parse_component__label, parse_description, parse_label, put_component__label, put_description, put_label,
    validate_component__label, validate_description, validate_label
)


class ComponentMetadataLabel(ComponentMetadataBase):
    """
    Label component metadata.
    
    Attributes
    ----------
    component : ``None | tuple<Component>``
        The contained component.
    
    description : `None | str`
        The description of the component.
    
    label : `None | str`
        The label of the component.
    """
    __slots__ = ('component', 'description', 'label')
    
    
    def __new__(cls, *, component = ..., description = ..., label = ...):
        """
        Creates a new label component metadata.
        
        Parameters
        ----------
        component : ``None | Component``, Optional (Keyword only)
            The contained component.
        
        description : `None | str`, Optional (Keyword only)
            The description of the component.
        
        label : `None | str`, Optional (Keyword only)
            The label of the component.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # component
        if component is ...:
            component = None
        else:
            component = validate_component__label(component)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # label
        if label is ...:
            label = None
        else:
            label = validate_label(label)
        
        # Construct
        self = object.__new__(cls)
        self.component = component
        self.description = description
        self.label = label
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            component = keyword_parameters.pop('component', ...),
            description = keyword_parameters.pop('description', ...),
            label = keyword_parameters.pop('label', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # component
        component = self.component
        if (component is not None):
            repr_parts.append(' component = ')
            repr_parts.append(repr(component))
            
            field_added = True
        else:
            field_added = False
        
        # description
        description = self.description
        if (description is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' description = ')
            repr_parts.append(repr(description))
        
        # label
        label = self.label
        if (label is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' label = ')
            repr_parts.append(repr(label))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # component
        component = self.component
        if (component is not None):
            hash_value ^= 1 << 0
            hash_value ^= hash(component)
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= 1 << 1
            hash_value ^= hash(description)
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= 1 << 2
            hash_value ^= hash(label)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # component
        if self.component != other.component:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # label
        if self.label != other.label:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.component = parse_component__label(data)
        self.description = parse_description(data)
        self.label = parse_label(data)
        
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_component__label(self.component, data, defaults, include_internals = include_internals)
        put_description(self.description, data, defaults)
        put_label(self.label, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # component
        component = self.component
        if (component is not None):
            component = component.clean_copy(guild)
        
        new.component = component
        
        # description
        new.description = self.description
        
        # label
        new.label = self.label
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # component
        component = self.component
        if (component is not None):
            component = component.copy()
        
        new.component = component
        
        # description
        new.description = self.description
        
        # label
        new.label = self.label
        
        return new
    
    
    def copy_with(self, *, component = ..., description = ..., label = ...):
        """
        Copies the label component metadata with the given fields.
        
        Parameters
        ----------
        component : ``None | Component``, Optional (Keyword only)
            The contained component.
        
        description : `None | str`, Optional (Keyword only)
            The description of the component.
        
        label : `None | str`, Optional (Keyword only)
            The label of the component.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # component
        if component is ...:
            component = self.component
            if (component is not None):
                component = component.copy()
        else:
            component = validate_component__label(component)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # label
        if label is ...:
            label = self.label
        else:
            label = validate_label(label)
        
        # Construct
        new = object.__new__(type(self))
        new.component = component
        new.description = description
        new.label = label
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            component = keyword_parameters.pop('component', ...),
            description = keyword_parameters.pop('description', ...),
            label = keyword_parameters.pop('label', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.iter_contents)
    def iter_contents(self):
        component = self.component
        if (component is not None):
            yield from component.iter_contents()

