__all__ = ('InteractionComponent',)

import reprlib, warnings

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
        The components value defined by the user.
        
        > Mutually exclusive with the `components` field.
    """
    __slots__ = ('components', 'custom_id', 'type', 'value')
    
    
    def __new__(cls, **keyword_parameters):
        """
        Creates a new interaction component from the given keyword parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields and how should be set.
        
        Other Parameters
        ----------------
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Nested components.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        type_ : ``ComponentType``, Optional (Keyword only)
            The represented component's type.
        
        value : `None`, `str`, Optional (Keyword only)
            The components value defined by the user.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        self = cls._create_empty()
        self._populate_from_keyword_parameters(keyword_parameters)
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
        self.custom_id = None
        self.components = None
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
            components = tuple(component.copy() for component in components)
        new.components = components
        new.custom_id = self.custom_id
        new.type = self.type
        new.value = self.value
        return new
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the interaction component with replacing the defined fields.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields and how should be set.
        
        Other Parameters
        ----------------
        components : `None`, `tuple` of ``InteractionComponent``, Optional (Keyword only)
            Nested components.
        
        custom_id : `str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        type_ : ``ComponentType``, Optional (Keyword only)
            The represented component's type.
        
        value : `None`, `str`, Optional (Keyword only)
            The components value defined by the user.
        
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
        self = self.copy()
        self._populate_from_keyword_parameters(keyword_parameters)
        return self
    
    
    def _populate_from_keyword_parameters(self, keyword_parameters):
        """
        Sets the interaction component's attributes from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            A dictionary of keyword parameters defining which fields and how should be set.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused fields given.
        ValueError
            - If a field's value is incorrect.
        """
        if not keyword_parameters:
            return
        
        # components
        try:
            components = keyword_parameters.pop('components')
        except KeyError:
            pass
        else:
            self.components = validate_components(components)
        
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            pass
        else:
            self.custom_id = validate_custom_id(custom_id)
        
        # type
        try:
            type_ = keyword_parameters.pop('type_')
        except KeyError:
            pass
        else:
            self.type = validate_type(type_)
        
        # value
        try:
            value = keyword_parameters.pop('value')
        except KeyError:
            pass
        else:
            self.value = validate_value(value)
        
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction component from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
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
        data : `dict` of (`str`, `Any`) items
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
        type_ = self.type
        if type_ is not ComponentType.none:
            repr_parts.append(' type = ')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
            
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
            repr_parts.append(reprlib.repr(custom_id))
        
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
    
    
    @property
    def options(self):
        """
        `.options` is deprecated and will be removed in 2023 February. Please use `.components` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.options` is deprecated and will be removed in 2023 February. '
                f'Please use `.components` instead.'  
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.components
    
    
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
