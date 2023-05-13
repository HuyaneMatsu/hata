__all__ = ('Component',)

from scarletio import RichAttributeErrorBaseType, copy_docs, export

from ..component_metadata import ComponentMetadataBase
from ..component_metadata.fields import (
    validate_button_style, validate_channel_types, validate_enabled, validate_label, validate_max_length,
    validate_max_values, validate_min_length, validate_min_values, validate_options, validate_placeholder,
    validate_required, validate_text_input_style, validate_url, validate_value
)
from ..shared_fields import validate_components, validate_custom_id, validate_emoji

from .fields import parse_type, put_type_into, validate_type
from .preinstanced import ComponentType


@export
class Component(RichAttributeErrorBaseType):
    """
    Represents a message component.
    
    Attributes
    ----------
    type : ``ComponentType``
        The component's type.
    metadata : ``ComponentMetadataBase``
        The component's metadata.
    """
    __slots__ = ('metadata', 'type',)
    
    def __new__(cls, component_type, **keyword_parameters):
        """
        Creates a component with the given parameters.
        
        Parameters
        ----------
        component_type : `int`, ``ComponentType``
            The component's type to create.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters defining the component's fields.
        
        Other parameters
        ----------------
        button_style : ``ButtonStyle``, Optional (Keyword only)
            The component's style. Applicable for button components.
        
        channel_types : `None`, `tuple` of (``ChannelType``, `int`), Optional (Keyword only)
            The allowed channel types by the select.
        
        components : `None`, `tuple` of ``Component``, Optional (Keyword only)
            Sub-components.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        emoji : `None` ``Emoji``, Optional (Keyword only)
            Emoji of the component if applicable.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        label : `None`, `str`, Optional (Keyword only)
            Label of the component.
        
        max_length : `int`, Optional (Keyword only)
            The maximal length of the inputted text.
        
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_length : `int`, Optional (Keyword only)
            The minimal length of the inputted text.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : `None`, `tuple` of ``StringSelectOption``, Optional (Keyword only)
            Options of the component.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder of the select.
        
        required : `bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
        text_input_style : ``TextInputStyle``, Optional (Keyword only)
            The text input's style.
        
        url : `None`, `str`, Optional (Keyword only)
            Url to redirect to.
        
        value : `None`, `str`, Optional (Keyword only)
            The input component's default value.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        component_type = validate_type(component_type)
        metadata = component_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        self = object.__new__(cls)
        self.type = component_type
        self.metadata = metadata
        return self
    
    
    def __iter__(self):
        """
        Iterates over the sub components.
        
        This method is an iterable generator.
        
        Yields
        ------
        component
        """
        components = self.components
        if (components is not None):
            yield from components
    
    
    def __eq__(self, other):
        """Returns whether the two components are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.metadata != other.metadata:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the component's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
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
        """Returns the component's hash value."""
        hash_value = 0
        
        # metadata
        hash_value ^= hash(self.metadata)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a component from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Component data.
        
        Returns
        -------
        self : `instance<cls>`
            Returns the created component.
        """
        component_type = parse_type(data)
        metadata = component_type.metadata_type.from_data(data)
        
        self = object.__new__(cls)
        self.metadata = metadata
        self.type = component_type
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Returns the component's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        # metadata
        data = self.metadata.to_data(defaults = defaults)
        
        # type
        put_type_into(self.type, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the component.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        metadata = self.metadata.copy()
        
        new = object.__new__(type(self))
        new.metadata = metadata
        new.type = self.type
        return new
    
    
    def copy_with(self, *, component_type = ..., **keyword_parameters):
        """
        Copies the component with changing it's field.
        
        Parameters
        ----------
        component_type : `int`, ``ComponentType``, Optional (Keyword only)
            The component's type.
        
        **keyword_parameters : Keyword parameters
            Keyword parameters defining which fields should be changed.
        
        Other parameters
        ----------------
        button_style : ``ButtonStyle``, Optional (Keyword only)
            The component's style. Applicable for button components.
        
        channel_types : `None`, `tuple` of (``ChannelType``, `int`), Optional (Keyword only)
            The allowed channel types by the select.
        
        components : `None`, `tuple` of ``Component``, Optional (Keyword only)
            Sub-components.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        emoji : `None` ``Emoji``, Optional (Keyword only)
            Emoji of the component if applicable.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        label : `None`, `str`, Optional (Keyword only)
            Label of the component.
        
        max_length : `int`, Optional (Keyword only)
            The maximal length of the inputted text.
        
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_length : `int`, Optional (Keyword only)
            The minimal length of the inputted text.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : `None`, `tuple` of ``StringSelectOption``, Optional (Keyword only)
            Options of the component.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder of the select.
        
        required : `bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
        text_input_style : ``TextInputStyle``, Optional (Keyword only)
            The text input's style.
        
        url : `None`, `str`, Optional (Keyword only)
            Url to redirect to.
        
        value : `None`, `str`, Optional (Keyword only)
            The input component's default value.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
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
            metadata = component_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        # Construct
        new = object.__new__(type(self))
        new.metadata = metadata
        new.type = component_type
        return new
    
    
    # Field proxies
    
    @property
    @copy_docs(ComponentMetadataBase.button_style)
    def button_style(self):
        return self.metadata.button_style
    
    @button_style.setter
    def button_style(self, button_style):
        self.metadata.button_style = validate_button_style(button_style)
    
    
    @property
    @copy_docs(ComponentMetadataBase.channel_types)
    def channel_types(self):
        return self.metadata.channel_types
    
    @channel_types.setter
    def channel_types(self, channel_types):
        self.metadata.channel_types = validate_channel_types(channel_types)
    
    
    @property
    @copy_docs(ComponentMetadataBase.components)
    def components(self):
        return self.metadata.components
    
    @components.setter
    def components(self, components):
        self.metadata.components = validate_components(components)
    
    
    @property
    @copy_docs(ComponentMetadataBase.custom_id)
    def custom_id(self):
        return self.metadata.custom_id
    
    @custom_id.setter
    def custom_id(self, custom_id):
        self.metadata.custom_id = validate_custom_id(custom_id)
    
    
    @property
    @copy_docs(ComponentMetadataBase.emoji)
    def emoji(self):
        return self.metadata.emoji
    
    @emoji.setter
    def emoji(self, emoji):
        self.metadata.emoji = validate_emoji(emoji)
    
    
    @property
    @copy_docs(ComponentMetadataBase.enabled)
    def enabled(self):
        return self.metadata.enabled
    
    @enabled.setter
    def enabled(self, enabled):
        self.metadata.enabled = validate_enabled(enabled)
    
    
    @property
    @copy_docs(ComponentMetadataBase.label)
    def label(self):
        return self.metadata.label
    
    @label.setter
    def label(self, label):
        self.metadata.label = validate_label(label)
    
    
    @property
    @copy_docs(ComponentMetadataBase.max_length)
    def max_length(self):
        return self.metadata.max_length
    
    @max_length.setter
    def max_length(self, max_length):
        self.metadata.max_length = validate_max_length(max_length)
    
    
    @property
    @copy_docs(ComponentMetadataBase.max_values)
    def max_values(self):
        return self.metadata.max_values
    
    @max_values.setter
    def max_values(self, max_values):
        self.metadata.max_values = validate_max_values(max_values)
    
    
    @property
    @copy_docs(ComponentMetadataBase.min_length)
    def min_length(self):
        return self.metadata.min_length
    
    @min_length.setter
    def min_length(self, min_length):
        self.metadata.min_length = validate_min_length(min_length)
    
    
    @property
    @copy_docs(ComponentMetadataBase.min_values)
    def min_values(self):
        return self.metadata.min_values
    
    @min_values.setter
    def min_values(self, min_values):
        self.metadata.min_values = validate_min_values(min_values)
    
    
    @property
    @copy_docs(ComponentMetadataBase.options)
    def options(self):
        return self.metadata.options
    
    @options.setter
    def options(self, options):
        self.metadata.options = validate_options(options)
    
    
    @property
    @copy_docs(ComponentMetadataBase.placeholder)
    def placeholder(self):
        return self.metadata.placeholder
    
    @placeholder.setter
    def placeholder(self, placeholder):
        self.metadata.placeholder = validate_placeholder(placeholder)
    
    
    @property
    @copy_docs(ComponentMetadataBase.required)
    def required(self):
        return self.metadata.required
    
    @required.setter
    def required(self, required):
        self.metadata.required = validate_required(required)
    
    
    @property
    @copy_docs(ComponentMetadataBase.text_input_style)
    def text_input_style(self):
        return self.metadata.text_input_style
    
    @text_input_style.setter
    def text_input_style(self, text_input_style):
        self.metadata.text_input_style = validate_text_input_style(text_input_style)
    
    @property
    @copy_docs(ComponentMetadataBase.url)
    def url(self):
        return self.metadata.url
    
    @url.setter
    def url(self, url):
        self.metadata.url = validate_url(url)
    
    
    @property
    @copy_docs(ComponentMetadataBase.value)
    def value(self):
        return self.metadata.value
    
    @value.setter
    def value(self, value):
        self.metadata.value = validate_value(value)
    
    # Field proxy utilities
    
    @property
    def style(self):
        """
        Returns the component's style.
        
        Returns
        -------
        style : `None`, ``ButtonStyle``, ``TextInputStyle``
        """
        component_type = self.type
        if component_type is ComponentType.button:
            return self.button_style
        
        if component_type is ComponentType.text_input:
            return self.text_input_style
    
    @style.setter
    def style(self, style):
        component_type = self.type
        if component_type is ComponentType.button:
            self.metadata.button_style = validate_button_style(style)
            return
        
        if component_type is ComponentType.text_input:
            self.metadata.text_input_style = validate_text_input_style(style)
            return
        
        raise TypeError(
            f'`Cannot` set `style` of {component_type!r}; got {style!r}.'
        )
    
    
    def iter_components(self):
        """
        Iterates over the direct sub-components of the component.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``Component``
        """
        components = self.components
        if (components is not None):
            yield from components
    
    
    def iter_options(self):
        """
        Iterates over the options of the component.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``StringSelectOption``
        """
        options = self.options
        if (options is not None):
            yield from options
