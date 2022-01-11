__all__ = ('ComponentRow',)

from scarletio import copy_docs, export, include

from .component_base import ComponentBase
from .debug import _debug_component_components
from .preinstanced import ComponentType


create_component = include('create_component')


@export
class ComponentRow(ComponentBase):
    """
    Action row component.
    
    Attributes
    ----------
    components : `None`, `tuple` of ``ComponentBase``s
        Stored components.
    
    Class Attributes
    ----------------
    custom_id : `NoneType` = `None`
        `custom_id` is not applicable for component rows.
    type : ``ComponentType`` = `ComponentType.row`
        The component's type.
    """
    type = ComponentType.row
    
    __slots__ = ('components',)
    
    def __new__(cls, *components):
        """
        Creates a new action component from the given components.
        
        Parameters
        ----------
        *components : ``ComponentBase``s
            Sub components.
        
        Raises
        ------
        AssertionError
            - If `components` contains a non ``ComponentBase``.
        """
        if __debug__:
            _debug_component_components(components)
        
        # components
        if not components:
            components = None
        
        self = object.__new__(cls)
        self.components = components
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        # components
        component_datas = data.get('components', None)
        if (component_datas is None) or (not component_datas):
            components = None
        else:
            components = [create_component(component_data) for component_data in component_datas]
        self.components = components
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # type
        data = {
            'type' : self.type.value
        }
        
        # components
        components = self.components
        if (components is None):
            component_datas = []
        else:
            component_datas = [component.to_data() for component in components]
        data['components'] = component_datas
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        # sub-component fields : components
        
        # components
        repr_parts.append(', components=')
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
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        
        new.components = components
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        components : `iterable` of ``ComponentBase``s, Optional (Keyword only)
            Sub components.
        
        Returns
        -------
        new : ``ComponentRow``
        """
        # components
        try:
            components = kwargs.pop('components')
        except KeyError:
            components = self.components
        else:
            components = tuple(components)
            
            if __debug__:
                _debug_component_components(components)
            
            if not components:
                components = None
        
        new = object.__new__(type(self))
        new.components = components
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        # components
        if self.components != other.components:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        # type
        hash_value = self.type.value
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components) << 12
            for component in components:
                hash_value ^= hash(component)
        
        return hash_value
    
    
    @copy_docs(ComponentBase._iter_components)
    def _iter_components(self):
        yield self
        
        components = self.components
        if (components is not None):
            for component in components:
                yield from component._iter_components()
    
    
    @copy_docs(ComponentBase._replace_direct_sub_components)
    def _replace_direct_sub_components(self, relation):
        components = self.components
        if (components is not None):
            self.components = tuple(relation.get(component, component) for component in components)
    
    
    @copy_docs(ComponentBase._iter_direct_sub_components)
    def _iter_direct_sub_components(self):
        components = self.components
        if (components is not None):
            yield from components
