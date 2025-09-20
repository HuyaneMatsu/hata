__all__ = ('InteractionComponent',)

from scarletio import RichAttributeErrorBaseType, copy_docs, export, include

from ..component import ComponentType
from ..interaction_component_metadata import InteractionComponentMetadataBase
from ..interaction_component_metadata.fields import (
    validate_component__label, validate_components, validate_custom_id, validate_thumbnail, validate_value,
    validate_values
)

from .fields import parse_type, put_type, validate_type


Component = include('Component')


@export
class InteractionComponent(RichAttributeErrorBaseType):
    """
    Integration component representing a parameter or a sub-command-group.
    
    Attributes
    ----------
    type : ``ComponentType``
        The represented component's type.
    
    metadata : ``InteractionComponentMetadataBase``
        The interaction component's metadata.
    """
    __slots__ = ('metadata', 'type')
    
    
    def __new__(cls, component_type, **keyword_parameters):
        """
        Creates a new interaction component from the given keyword parameters.
        
        Parameters
        ----------
        component_type : ``None | int | ComponentType``
            The component's type to create.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters defining the component's fields.
        
        Other Parameters
        ----------------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            The sub-component nested inside (the label component).
        
        components : ``None | tuple<InteractionComponent>``, Optional (Keyword only)
            Sub-components.
        
        custom_id : `None | str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        thumbnail : ``None | InteractionComponent``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
        value : `None | str`, Optional (Keyword only)
            The component's value defined by the user.
        
        values : `None | str`, Optional (Keyword only)
            The component's values selected by the user.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a field's value is incorrect.
        """
        component_type = validate_type(component_type)
        metadata = component_type.interaction_metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        self = object.__new__(cls)
        self.type = component_type
        self.metadata = metadata
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
        self.type = ComponentType.none
        self.metadata = InteractionComponentMetadataBase()
        return self
    
    
    def copy(self):
        """
        Copies the interaction component.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        new.metadata = self.metadata.copy()
        new.type = self.type
        return new
    
    
    def copy_with(self, *, component_type = ..., **keyword_parameters):
        """
        Copies the interaction component with replacing the defined fields.
        
        Parameters
        ----------
        component_type : ``None | int | ComponentType``, Optional (Keyword only)
            The component's type to create.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters defining the component's fields.
        
        Other Parameters
        ----------------
        component : ``None | InteractionComponent``, Optional (Keyword only)
            The sub-component nested inside (the label component).
        
        components : ``None | tuple<InteractionComponent>``, Optional (Keyword only)
            Sub-components.
        
        custom_id : `None | str`, Optional (Keyword only)
            The `.custom_id` of the represented component.
        
        thumbnail : ``None | InteractionComponent``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
        value : `None | str`, Optional (Keyword only)
            The component's value defined by the user.
        
        values : `None | str`, Optional (Keyword only)
            The component's values selected by the user.
        
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
        
        # metadata
        if component_type is self.type:
            metadata = self.metadata.copy_with_keyword_parameters(keyword_parameters)
        else:
            metadata = component_type.interaction_metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        # Construct
        new = object.__new__(type(self))
        new.metadata = metadata
        new.type = component_type
        return new
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction component from the data received from Discord.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Interaction component data.
        """
        component_type = parse_type(data)
        metadata = component_type.interaction_metadata_type.from_data(data)
        
        self = object.__new__(cls)
        self.metadata = metadata
        self.type = component_type
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
        data : `dict<str, object>`
        """
        # metadata
        data = self.metadata.to_data(defaults = defaults)
        
        # type
        put_type(self.type, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' type = ')
        
        component_type = self.type
        repr_parts.append(component_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(component_type.value))
        
        repr_parts.append(', metadata = ')
        repr_parts.append(repr(self.metadata))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # metadata
        hash_value ^= hash(self.metadata)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.metadata != other.metadata:
            return False
        
        return True
    
    
    def __mod__(self, other):
        """Returns self % other."""
        if type(other) is not Component:
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        return self.metadata._match_to_component(other)
    
    
    __rmod__ = __mod__
    
    
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
        Iterates over all the `custom_id`-s and values of the interaction component.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id_is_multi_value_values : `(str, ComponentType, None | str | tuple<str>)`
        """
        return (yield from self.metadata.iter_custom_ids_and_values())
    
    
    # component
    @property
    @copy_docs(InteractionComponentMetadataBase.component)
    def component(self):
        return self.metadata.component
    
    @component.setter
    def component(self, component):
        self.metadata.component = validate_component__label(component)
    
    
    # components
    @property
    @copy_docs(InteractionComponentMetadataBase.components)
    def components(self):
        return self.metadata.components
    
    @components.setter
    def components(self, components):
        self.metadata.components = validate_components(components)
    
    
    # custom_id
    @property
    @copy_docs(InteractionComponentMetadataBase.custom_id)
    def custom_id(self):
        return self.metadata.custom_id
    
    @custom_id.setter
    def custom_id(self, custom_id):
        self.metadata.custom_id = validate_custom_id(custom_id)
    
    
    # thumbnail
    @property
    @copy_docs(InteractionComponentMetadataBase.thumbnail)
    def thumbnail(self):
        return self.metadata.thumbnail
    
    @thumbnail.setter
    def thumbnail(self, thumbnail):
        self.metadata.thumbnail = validate_thumbnail(thumbnail)

    
    # value
    @property
    @copy_docs(InteractionComponentMetadataBase.value)
    def value(self):
        return self.metadata.value
    
    @value.setter
    def value(self, value):
        self.metadata.value = validate_value(value)
    
    
    # values
    @property
    @copy_docs(InteractionComponentMetadataBase.values)
    def values(self):
        return self.metadata.values
    
    @values.setter
    def values(self, values):
        self.metadata.values = validate_values(values)
