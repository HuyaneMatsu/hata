__all__ = ('InteractionComponent',)

from reprlib import repr as short_repr

from scarletio import RichAttributeErrorBaseType, export

from ...component import ComponentType

from .fields import (
    parse_custom_id, parse_components, parse_type, parse_value, put_custom_id_into,
    put_components_into, put_type_into, put_value_into, validate_custom_id, validate_components, validate_type,
    validate_value
)


@export
class InteractionComponent(RichAttributeErrorBaseType):
    """
    Integration component representing a parameter or a sub-command-group.
    
    Attributes
    ----------
    components : `None`, `tuple` of ``InteractionComponent``
        Nested components.
    
    custom_id : `None`, `str`
        The `.custom_id` of the represented component.
    
    type : ``ComponentType``
        The represented component's type.
    
    value : `None`, `str`
        The component's value defined by the user.
        
        > Mutually exclusive with the `components` field.
    """
    __slots__ = ('components', 'custom_id', 'type', 'value')
    
    
    def __new__(cls, *, component_type = ..., components = ..., custom_id = ..., value = ...):
        """
        Creates a new interaction component from the given keyword parameters.
        
        Parameters
        ----------
        custom_id : `None`, `str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Nested components.
        
        component_type : ``ComponentType``, Optional (Keyword only)
            The represented component's type.
        
        value : `None`, `str`, Optional (Keyword only)
            The component's value defined by the user.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        ValueError
            - If a field's value is incorrect.
        """
        # component_type
        if component_type is ...:
            component_type = ComponentType.none
        else:
            component_type = validate_type(component_type)
        
        # components
        if components is ...:
            components = None
        else:
            components = validate_components(components)
        
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # value
        if value is ...:
            value = None
        else:
            value = validate_value(value)
        
        # Construct
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.components = components
        self.type = component_type
        self.value = value
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an interaction component with it's default values set.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.components = None
        self.custom_id = None
        self.type = ComponentType.none
        self.value = None
        return self
    
    
    def copy(self):
        """
        Copies the interaction component.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        components = self.components
        if (components is not None):
            components = (*(component.copy() for component in components),)
        new.components = components
        new.custom_id = self.custom_id
        new.type = self.type
        new.value = self.value
        return new
    
    
    def copy_with(self, component_type = ..., components = ..., custom_id = ..., value = ...):
        """
        Copies the interaction component with replacing the defined fields.
        
        Parameters
        ----------
        custom_id : `None`, `str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Nested components.
        
        component_type : ``ComponentType``, Optional (Keyword only)
            The represented component's type.
        
        value : `None`, `str`, Optional (Keyword only)
            The component's value defined by the user.
        
        Returns
        -------
        new : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        # component_type
        if component_type is ...:
            component_type = self.type
        else:
            component_type = validate_type(component_type)
        
        # components
        if components is ...:
            components = self.components
            if (components is not None):
                components = (*(component.copy() for component in components),)
        else:
            components = validate_components(components)
        
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # value
        if value is ...:
            value = self.value
        else:
            value = validate_value(value)
        
        # Construct
        self = object.__new__(type(self))
        self.custom_id = custom_id
        self.components = components
        self.type = component_type
        self.value = value
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction component from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`)
            Interaction component data.
        """
        self = object.__new__(cls)
        self.components = parse_components(data)
        self.custom_id = parse_custom_id(data)
        self.type = parse_type(data)
        self.value = parse_value(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the interaction component into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_components_into(self.components, data, defaults)
        put_custom_id_into(self.custom_id, data, defaults)
        put_type_into(self.type, data, defaults)
        put_value_into(self.value, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the interaction component's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : type
        
        # type
        component_type = self.type
        if component_type is not ComponentType.none:
            repr_parts.append(' type = ')
            repr_parts.append(component_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(component_type.value))
            
            field_added = True
        
        else:
            field_added = False
        
        # System fields : custom_id
        
        # custom_id
        
        custom_id = self.custom_id
        if custom_id is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' custom_id = ')
            repr_parts.append(short_repr(custom_id))
        
        # Extra descriptive fields : components | value
        # components
        components = self.components
        if (components is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' components = [')
            
            index = 0
            limit = len(components)
            
            while True:
                option = components[index]
                index += 1
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # value
        value = self.value
        if (value is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' value = ')
            repr_parts.append(repr(value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the interaction component's hash value."""
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= (len(components) << 8)
            
            for component in components:
                hash_value ^= hash(component)
        
        # type
        hash_value ^= self.type.value
        
        # value
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two interaction component's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # components
        if self.components != other.components:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # value
        if self.value != other.value:
            return False
        
        return True
    
    
    def iter_components(self):
        """
        Iterates over the sub-components of the interaction component.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``InteractionComponent``
        """
        components = self.components
        if (components is not None):
            yield from components


    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction option.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id : `str`
            The `custom_id` of a represented component.
        value : `str`
            The `value` passed by the user.
        """
        custom_id = self.custom_id
        if (custom_id is not None):
            yield custom_id, self.value
        
        for component in self.iter_components():
            yield from component.iter_custom_ids_and_values()
