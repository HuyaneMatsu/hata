__all__ = ('InteractionForm',)

import reprlib

from ...backend.utils import copy_docs

from .components import ComponentBase, ComponentRow, create_component

class InteractionForm(ComponentBase):
    """
    Form component.
    
    Attributes
    ----------
    components : `None` or `tuple` of ``ComponentBase`` instances
        Stored components.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.none`
        The component's type.
    """
    __slots__ = ('custom_id', 'components')
    
    def __new__(cls, *components, custom_id=None):
        """
        Creates an form interaction instance.
        
        Parameters
        ----------
        *components : ``ComponentBase`` instances
            Sub components.
        
        Raises
        ------
        AssertionError
            - If `components` contains a non ``ComponentBase`` instance.
            - If `custom_id` was not given neither as `None` or `str` instance.
            - If `custom_id`'s length is over `100`.
        """
        if __debug__:
            _debug_component_components(components)
            _debug_component_custom_id(custom_id)
        
        # components
        if components:
            tuple(
                component if isinstance(component, ComponentRow) else ComponentRow(component)
                for component in components
            )
        else:
            components = None
        
        # custom_id
        if (custom_id is None) and (not custom_id):
            custom_id = create_auto_custom_id()
        
        self = object.__new__(cls)
        self.components = components
        self.custom_id = custom_id
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
        
        # custom_id
        self.custom_id = data.get('custom_id', None)
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {}
        
        # components
        components = self.components
        if (components is None):
            component_datas = []
        else:
            component_datas = [component.to_data() for component in components]
        data['components'] = component_datas
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            data['custom_id'] = custom_id
        
        return data
    

    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # System fields : custom_id
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
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
        
        # custom_id
        new.custom_id = self.custom_id
        
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
        components : `iterable` of ``ComponentBase`` instances, Optional (Keyword only)
            Sub components.
        
        custom_id : `None` or `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
        
        Returns
        -------
        new : ``InteractionForm``
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
            
            if components:
                tuple(
                    component if isinstance(component, ComponentRow) else ComponentRow(component)
                    for component in components
                )
            else:
                components = None
        
        # custom_id
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
            
            if (custom_id is None) or (not custom_id):
                custom_id = create_auto_custom_id()
        
        
        new = object.__new__(type(self))
        new.components = components
        new.custom_id = custom_id
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        # components
        if self.components != other.components:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        # type
        hash_value = self.type.value
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components)<<12
            for component in components:
                hash_value ^= hash(component)
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
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
