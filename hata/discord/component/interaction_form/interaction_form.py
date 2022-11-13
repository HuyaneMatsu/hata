__all__ = ('InteractionForm',)

import reprlib

from scarletio import RichAttributeErrorBaseType

from ..shared_fields import (
    parse_components, parse_custom_id, put_components_into, put_custom_id_into, validate_custom_id
)
from ..shared_helpers import create_auto_custom_id

from .fields import parse_title, put_title_into, validate_components, validate_title


class InteractionForm(RichAttributeErrorBaseType):
    """
    Form component.
    
    Attributes
    ----------
    components : `None`, `tuple` of ``Component``
        Stored components.
    
    custom_id : `None`, `str`
        Custom identifier to match the form data when receiving it's interaction back.
    
    title : `None`, `str`
        The form's title.
    """
    __slots__ = ('components', 'custom_id', 'title')
    
    def __new__(cls, title, components, custom_id = None):
        """
        Creates a form interaction.
        
        Parameters
        ----------
        title : `None`, `str`
            The form's title.
        
        components : `None`, `iterable` of ``Component``
            Sub components.
        
        custom_id : `None`, `str` = `None`, Optional
             Custom identifier for the form.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        components = validate_components(components)
        custom_id = validate_custom_id(custom_id)
        title = validate_title(title)
        
        if (custom_id is None):
            custom_id = create_auto_custom_id()
        
        self = object.__new__(cls)
        self.components = components
        self.custom_id = custom_id
        self.title = title
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction form from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Interaction form data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.components = parse_components(data)
        self.custom_id = parse_custom_id(data)
        self.title = parse_title(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the interaction form to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        data = {}
        
        put_components_into(self.components, data, defaults)
        put_custom_id_into(self.custom_id, data, defaults)
        put_title_into(self.title, data, defaults)
        
        return data
    

    def __repr__(self):
        """Returns the interaction form's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # System fields : custom_id
        
        field_added = False
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' custom_id = ')
            repr_parts.append(reprlib.repr(custom_id))
        
        # Text fields : label & placeholder
        
        # title
        title = self.title
        if (title is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' title = ')
            repr_parts.append(reprlib.repr(title))
        
        # sub-component fields : components
        
        # components
        if field_added:
            repr_parts.append(',')
        else:
            field_added = True
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
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)


    def copy(self):
        """
        Copies the interaction form.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # components
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        new.components = components
        
        # custom_id
        new.custom_id = self.custom_id
        
        # title
        new.title = self.title
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields should be overwritten.
        
        Other Parameters
        ----------------
        components : `None`, `iterable` of ``Component``, Optional (Keyword only)
            Sub components.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
        
        title : `None`, `str`, Optional (Keyword only)
            The form's title.
        
        Returns
        -------
        new : ``InteractionForm``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # components
        try:
            components = kwargs.pop('components')
        except KeyError:
            components = self.components
            if (components is not None):
                components = tuple(component.copy() for component in self.components)
        else:
            components = validate_components(components)
        
        # custom_id
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # title
        try:
            title = kwargs.pop('title')
        except KeyError:
            title = self.title
        else:
            title = validate_title(title)
        
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        
        new = object.__new__(type(self))
        new.components = components
        new.custom_id = custom_id
        new.title = title
        return new
    
    
    def __eq__(self, other):
        """Returns whether the two interaction forms are equal."""
        if type(other) is not type(self):
            return NotImplemented
        
        # components
        if self.components != other.components:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the interaction form's hash value."""
        hash_value = 0
        
        # components
        components = self.components
        if (components is not None):
            hash_value ^= len(components) << 12
            for component in components:
                hash_value ^= hash(component)
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # title
        title = self.title
        if (title is not None):
            hash_value ^= hash(title)
        
        return hash_value
    
    
    def iter_components(self):
        """
        Iterates over the components of the form.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``Component``
        """
        components = self.components
        if (components is not None):
            yield from components
