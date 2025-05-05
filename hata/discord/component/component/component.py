__all__ = ('Component',)

from scarletio import RichAttributeErrorBaseType, copy_docs, export

from ..component_metadata import ComponentMetadataBase
from ..component_metadata.fields import (
    validate_button_style, validate_channel_types, validate_color, validate_content, validate_default_values,
    validate_description, validate_divider, validate_enabled, validate_items, validate_label, validate_max_length,
    validate_max_values, validate_media, validate_min_length, validate_min_values, validate_options,
    validate_placeholder, validate_required, validate_sku_id, validate_spacing_size, validate_spoiler,
    validate_text_input_style, validate_thumbnail, validate_url, validate_value
)
from ..shared_fields import validate_components, validate_custom_id, validate_emoji

from .fields import parse_type, put_type, validate_type
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
        
        Other Parameters
        ----------------
        button_style : ``int | ButtonStyle``, Optional (Keyword only)
            The component's style. Applicable for button components.
        
        channel_types : ``None | iterable<int> | iterable<ChannelType>``, Optional (Keyword only)
            The allowed channel types by the select.
        
        color : ``None | int | Color``, Optional (Keywords only)
            The color of the component.
        
        components : ``None | tuple<Component>``, Optional (Keyword only)
            Sub-components.
        
        content : `None | str`, Optional (Keyword only)
            The content shown on the component.
        
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        default_values : ``None | iterable<Channel> | iterable<Role> | iterable<ClientUserBase> | iterable<EntitySelectDefaultValue> | iterable<(str | EntitySelectDefaultValueTyp, int | str)>>`` \
                , Optional (Keyword only)
            Entities presented in the select by default.
        
        emoji : ``None | Emoji``, Optional (Keyword only)
            Emoji of the component if applicable.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        description : `None | str`, Optional (Keyword only)
            Description of the component's media.
        
        divider : `bool`, Optional (Keyword only)
            Whether the separator should contain a divider.
        
        items : ``None | iterable<str> | iterable<MediaItem>``, Optional (Keyword only)
            The media items shown on the component.
        
        label : `None | str`, Optional (Keyword only)
            Label of the component.
        
        max_length : `int`, Optional (Keyword only)
            The maximal length of the inputted text.
        
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select.
        
        media : ``str | MediaInfo``, Optional (Keyword only)
            The media of the component.
            Supports only attachments using the `attachment://<file_name>` url format.
        
        min_length : `int`, Optional (Keyword only)
            The minimal length of the inputted text.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : ``None | iterable<StringSelectOption>``, Optional (Keyword only)
            Options of the component.
        
        placeholder : `None | str`, Optional (Keyword only)
            Placeholder of the select.
        
        required : `bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
        sku_id : ``int | SKU``, Optional (keyword only)
            Purchasable stock keeping unit identifier.
        
        spacing_size : ``int | SeparatorSpacingSize``, Optional (Keyword only)
            The separator's spacing's size.
        
        spoiler : `bool`, Optional (Keyword only)
            Whether the media or the content of the component is spoilered.
        
        text_input_style : ``int | TextInputStyle``, Optional (Keyword only)
            The text input's style.
        
        thumbnail : ``None | Component``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
        url : `None | str`, Optional (Keyword only)
            Url to redirect to.
        
        value : `None | str`, Optional (Keyword only)
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
    
    
    def __len__(self):
        """Returns len(self)"""
        length = 0
        
        for content in self.metadata.iter_contents():
            length += len(content)
        
        return length
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a component from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
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
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the component's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        # metadata
        data = self.metadata.to_data(defaults = defaults, include_internals = include_internals)
        
        # type
        put_type(self.type, data, defaults)
        
        return data
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the component by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : ``None | Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.metadata = self.metadata.clean_copy(guild)
        new.type = self.type
        return new
    
    
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
        
        Other Parameters
        ----------------
        button_style : ``int | ButtonStyle``, Optional (Keyword only)
            The component's style. Applicable for button components.
        
        channel_types : ``None | iterable<int> | iterable<ChannelType>``, Optional (Keyword only)
            The allowed channel types by the select.
        
        color : ``None | int | Color``, Optional (Keywords only)
            The color of the component.
        
        components : ``None | tuple<Component>``, Optional (Keyword only)
            Sub-components.
        
        content : `None | str`, Optional (Keyword only)
            The content shown on the component.
        
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was clicked (or used) by the user.
        
        default_values : ``None | iterable<Channel> | iterable<Role> | iterable<ClientUserBase> | iterable<EntitySelectDefaultValue> | iterable<(str | EntitySelectDefaultValueTyp, int | str)>>`` \
                , Optional (Keyword only)
            Entities presented in the select by default.
        
        description : `None | str`, Optional (Keyword only)
            Description of the component's media.
        
        divider : `bool`, Optional (Keyword only)
            Whether the separator should contain a divider.
        
        emoji : ``None | Emoji``, Optional (Keyword only)
            Emoji of the component if applicable.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        items : ``None | iterable<str> | iterable<MediaItem>``, Optional (Keyword only)
            The media items shown on the component.
        
        label : `None | str`, Optional (Keyword only)
            Label of the component.
        
        max_length : `int`, Optional (Keyword only)
            The maximal length of the inputted text.
        
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_length : `int`, Optional (Keyword only)
            The minimal length of the inputted text.
        
        media : ``str | MediaInfo``, Optional (Keyword only)
            The media of the component.
            Supports only attachments using the `attachment://<file_name>` url format.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        options : ``None | iterable<StringSelectOption>``, Optional (Keyword only)
            Options of the component.
        
        placeholder : `None | str`, Optional (Keyword only)
            Placeholder of the select.
        
        required : `bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
        sku_id : ``int | SKU``, Optional (keyword only)
            Purchasable stock keeping unit identifier.
        
        spacing_size : ``int | SeparatorSpacingSize``, Optional (Keyword only)
            The separator's spacing's size.
        
        spoiler : `bool`, Optional (Keyword only)
            Whether the media or the content of the component is spoilered.
        
        text_input_style : ``int | TextInputStyle``, Optional (Keyword only)
            The text input's style.
        
        thumbnail : ``None | Component``, Optional (Keyword only)
            The thumbnail or other accessory (button) of a section component.
        
        url : `None | str`, Optional (Keyword only)
            Url to redirect to.
        
        value : `None | str`, Optional (Keyword only)
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
    
    # button_style
    @property
    @copy_docs(ComponentMetadataBase.button_style)
    def button_style(self):
        return self.metadata.button_style
    
    @button_style.setter
    def button_style(self, button_style):
        self.metadata.button_style = validate_button_style(button_style)
    
    
    # channel_types
    @property
    @copy_docs(ComponentMetadataBase.channel_types)
    def channel_types(self):
        return self.metadata.channel_types
    
    @channel_types.setter
    def channel_types(self, channel_types):
        self.metadata.channel_types = validate_channel_types(channel_types)
    
    
    # components
    @property
    @copy_docs(ComponentMetadataBase.components)
    def components(self):
        return self.metadata.components
    
    @components.setter
    def components(self, components):
        self.metadata.components = validate_components(components)
    
    
    # color
    @property
    @copy_docs(ComponentMetadataBase.color)
    def color(self):
        return self.metadata.color
    
    @color.setter
    def color(self, color):
        self.metadata.color = validate_color(color)
    
    
    # content
    @property
    @copy_docs(ComponentMetadataBase.content)
    def content(self):
        return self.metadata.content
    
    @content.setter
    def content(self, content):
        self.metadata.content = validate_content(content)
    
    
    # custom_id
    @property
    @copy_docs(ComponentMetadataBase.custom_id)
    def custom_id(self):
        return self.metadata.custom_id
    
    @custom_id.setter
    def custom_id(self, custom_id):
        self.metadata.custom_id = validate_custom_id(custom_id)
    
    
    # default_values
    @property
    @copy_docs(ComponentMetadataBase.default_values)
    def default_values(self):
        return self.metadata.default_values
    
    @default_values.setter
    def default_values(self, default_values):
        self.metadata.default_values = validate_default_values(default_values)
    
    
    # description
    @property
    @copy_docs(ComponentMetadataBase.description)
    def description(self):
        return self.metadata.description
    
    @description.setter
    def description(self, description):
        self.metadata.description = validate_description(description)
    
    
    # divider
    @property
    @copy_docs(ComponentMetadataBase.divider)
    def divider(self):
        return self.metadata.divider
    
    @divider.setter
    def divider(self, divider):
        self.metadata.divider = validate_divider(divider)
    
    
    # emoji
    @property
    @copy_docs(ComponentMetadataBase.emoji)
    def emoji(self):
        return self.metadata.emoji
    
    @emoji.setter
    def emoji(self, emoji):
        self.metadata.emoji = validate_emoji(emoji)
    
    
    # enabled
    @property
    @copy_docs(ComponentMetadataBase.enabled)
    def enabled(self):
        return self.metadata.enabled
    
    @enabled.setter
    def enabled(self, enabled):
        self.metadata.enabled = validate_enabled(enabled)
    
    
    # label
    @property
    @copy_docs(ComponentMetadataBase.label)
    def label(self):
        return self.metadata.label
    
    @label.setter
    def label(self, label):
        self.metadata.label = validate_label(label)
    
    
    # items
    @property
    @copy_docs(ComponentMetadataBase.items)
    def items(self):
        return self.metadata.items
    
    @items.setter
    def items(self, items):
        self.metadata.items = validate_items(items)
    
    
    # max_length
    @property
    @copy_docs(ComponentMetadataBase.max_length)
    def max_length(self):
        return self.metadata.max_length
    
    @max_length.setter
    def max_length(self, max_length):
        self.metadata.max_length = validate_max_length(max_length)
    
    
    # max_values
    @property
    @copy_docs(ComponentMetadataBase.max_values)
    def max_values(self):
        return self.metadata.max_values
    
    @max_values.setter
    def max_values(self, max_values):
        self.metadata.max_values = validate_max_values(max_values)
    
    
    # media
    @property
    @copy_docs(ComponentMetadataBase.media)
    def media(self):
        return self.metadata.media
    
    @media.setter
    def media(self, media):
        self.metadata.media = validate_media(media)
    
    
    # min_length
    @property
    @copy_docs(ComponentMetadataBase.min_length)
    def min_length(self):
        return self.metadata.min_length
    
    @min_length.setter
    def min_length(self, min_length):
        self.metadata.min_length = validate_min_length(min_length)
    
    
    # min_values
    @property
    @copy_docs(ComponentMetadataBase.min_values)
    def min_values(self):
        return self.metadata.min_values
    
    @min_values.setter
    def min_values(self, min_values):
        self.metadata.min_values = validate_min_values(min_values)
    
    
    # options
    @property
    @copy_docs(ComponentMetadataBase.options)
    def options(self):
        return self.metadata.options
    
    @options.setter
    def options(self, options):
        self.metadata.options = validate_options(options)
    
    
    # placeholder
    @property
    @copy_docs(ComponentMetadataBase.placeholder)
    def placeholder(self):
        return self.metadata.placeholder
    
    @placeholder.setter
    def placeholder(self, placeholder):
        self.metadata.placeholder = validate_placeholder(placeholder)
    
    
    # required
    @property
    @copy_docs(ComponentMetadataBase.required)
    def required(self):
        return self.metadata.required
    
    @required.setter
    def required(self, required):
        self.metadata.required = validate_required(required)
    
    
    # sku_id
    @property
    @copy_docs(ComponentMetadataBase.sku_id)
    def sku_id(self):
        return self.metadata.sku_id
    
    @sku_id.setter
    def sku_id(self, sku_id):
        self.metadata.sku_id = validate_sku_id(sku_id)
    
    
    # spacing_size
    @property
    @copy_docs(ComponentMetadataBase.spacing_size)
    def spacing_size(self):
        return self.metadata.spacing_size
    
    @spacing_size.setter
    def spacing_size(self, spacing_size):
        self.metadata.spacing_size = validate_spacing_size(spacing_size)
    
    
    # spoiler
    @property
    @copy_docs(ComponentMetadataBase.spoiler)
    def spoiler(self):
        return self.metadata.spoiler
    
    @spoiler.setter
    def spoiler(self, spoiler):
        self.metadata.spoiler = validate_spoiler(spoiler)
    
    
    # text_input_style
    @property
    @copy_docs(ComponentMetadataBase.text_input_style)
    def text_input_style(self):
        return self.metadata.text_input_style
    
    @text_input_style.setter
    def text_input_style(self, text_input_style):
        self.metadata.text_input_style = validate_text_input_style(text_input_style)
    
    
    # thumbnail
    @property
    @copy_docs(ComponentMetadataBase.thumbnail)
    def thumbnail(self):
        return self.metadata.thumbnail
    
    @thumbnail.setter
    def thumbnail(self, thumbnail):
        self.metadata.thumbnail = validate_thumbnail(thumbnail)
    
    
    # url
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

    
    def iter_default_values(self):
        """
        Iterates over the default options of the component.
        
        This method is an iterable generator.
        
        Yields
        ------
        default_value : ``EntitySelectDefaultValue``
        """
        default_values = self.default_values
        if (default_values is not None):
            yield from default_values

    
    def iter_items(self):
        """
        Iterates over the media items of the component.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : ``MediaItem``
        """
        items = self.items
        if (items is not None):
            yield from items
    
    
    def iter_contents(self):
        """
        Iterates over the component's contents.
        
        This method is an iterable generator.
        
        Yields
        -------
        contents : `str`
        """
        yield from self.metadata.iter_contents()
    
    
    @property
    def contents(self):
        """
        Returns the component's contents.
        
        Returns
        -------
        contents : `list<str>`
        """
        return [*self.metadata.iter_contents()]
