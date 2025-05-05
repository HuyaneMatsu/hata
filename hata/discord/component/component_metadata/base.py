__all__ = ('ComponentMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder

from .constants import SEPARATOR_SPACING_SIZE_DEFAULT
from .preinstanced import ButtonStyle, TextInputStyle


class ComponentMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for component metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new component metadata from the given fields.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new component metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to build the metadata from.
        
        Returns
        -------
        self : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a keyword parameter's type is incorrect.
        ValueError
            - If a keyword parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the component metadata's representation."""
        return f'<{type(self).__name__}>'
    
    
    def __hash__(self):
        """Returns the component metadata's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two component metadatas are equal."""
        if type(self) is not type(other):
            return False
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self equals to other. Other must be the same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new component metadata from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Component data.
        
        Returns
        -------
        self : `instance<cls>`
            Returns the created component.
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the component metadata's json serializable representation.
        
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
        return {}
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the component metadata by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : ``None | Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy(self):
        """
        Copies the component metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the component metadata with the given fields.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        return self.copy()
    
    
    def copy_with_keyword_parameters(self, keyword_parameters):
        """
        Copies the component metadata with the given keyword parameters.
        
        The used up fields are popped from the keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters defining which fields should be changed.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return self.copy_with()
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the component metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        return
        yield
    
    
    # Field placeholders
    
    button_style = PlaceHolder(
        ButtonStyle.none,
        """
        The component's style. Applicable for button components.
        
        Returns
        -------
        button_style : ``ButtonStyle``
        """
    )
    
    
    channel_types = PlaceHolder(
        None,
        """
        The allowed channel types by the select.
        
        Returns
        -------
        channel_types : ``None | tuple<ChannelType>``
        """
    )
    
    
    color = PlaceHolder(
        None,
        """
        The color of the component. At the case of container components it means the strip on the left.
        Passing `0` means black.
        
        color : ``None | Color``
        """
    )
    
    
    components = PlaceHolder(
        None,
        """
        Sub-components.
        
        Returns
        -------
        components : ``None | tuple<Component>``
        """
    )
    
    
    content = PlaceHolder(
        None,
        """
        The content shown on the component.
        
        Returns
        -------
        content : `None | str`
        """
    )
    
    
    custom_id = PlaceHolder(
        None,
        """
        Custom identifier to detect which component was clicked (or used) by the user.
        
        > Mutually exclusive with the `sku_id` and `url` fields if the component is a buttons.
        
        Returns
        -------
        custom_id : `None | str`
        """
    )
    
    
    default_values = PlaceHolder(
        None,
        """
        Entities suggested by default in an entity select.
        
        Returns
        -------
        default_values : ``None | tuple<EntitySelectDefaultValue>``
        """
    )
    
    
    description = PlaceHolder(
        None,
        """
        Description of the component's media.
        
        Returns
        -------
        description : `None | str`
        """
    )
    
    
    divider = PlaceHolder(
        True,
        """
        Whether the separator should contain a divider.
        
        Returns
        -------
        divider : `bool`
        """
    )
    
    
    emoji = PlaceHolder(
        None,
        """
        Emoji of the component if applicable.
        
        Returns
        -------
        emoji : ``None | Emoji``
        """
    )
    
    
    enabled = PlaceHolder(
        True,
        """
        Whether the component is enabled.
        
        Returns
        -------
        enabled : `bool`
        """
    )
    
    
    items = PlaceHolder(
        None,
        """
        The media items shown on the component.
        
        Returns
        -------
        items : ``None | tuple<MediaItem>``
        """
    )
    
    
    label = PlaceHolder(
        None,
        """
        Label of the component.
        
        Returns
        -------
        label : `None | str`
        """
    )
    
    
    max_length = PlaceHolder(
        0,
        """
        The maximal length of the inputted text.
        
        Returns
        -------
        max_length : `int`
        """
    )
    
    
    max_values = PlaceHolder(
        1,
        """
        The maximal amount of options to select.
        
        Returns
        -------
        max_values : `int`
        """
    )
    
    
    media = PlaceHolder(
        None,
        """
        The media of the component.
        
        Returns
        -------
        media : ``None | MediaInfo``
        """
    )
    
    
    min_length = PlaceHolder(
        0,
        """
        The minimal length of the inputted text.
        
        Returns
        -------
        min_length : `int`
        """
    )
    
    
    min_values = PlaceHolder(
        1,
        """
        The minimal amount of options to select.
        
        Returns
        -------
        min_values : `int`
        """
    )
    
    
    options = PlaceHolder(
        None,
        """
        Options of the component.
        
        Returns
        -------
        options : ``None | tuple<StringSelectOption>``
        """
    )
    
    
    placeholder = PlaceHolder(
        None,
        """
        Place holder text of the select.
        
        Returns
        -------
        placeholder : `None | str`
        """
    )
    
    
    required = PlaceHolder(
        False,
        """
        Whether the field is required to be fulfilled.
        
        Returns
        -------
        required : `bool`
        """
    )
    
    
    sku_id = PlaceHolder(
        0,
        """
        Purchasable stock keeping unit identifier.
        
        > Mutually exclusive with the `custom_id` and `url` fields if the component is a buttons.
        
        Returns
        -------
        sku_id : `int`
        """
    )
    
    
    spacing_size = PlaceHolder(
        SEPARATOR_SPACING_SIZE_DEFAULT,
        """
        The separator's spacing's size.
        
        Returns
        -------
        spacing_size : ``SeparatorSpacingSize``
        """
    )
    
    
    spoiler = PlaceHolder(
        False,
        """
        Whether the media or the content of the component is spoilered.
        
        Returns
        -------
        spoiler : `bool`
        """
    )
    
    
    text_input_style = PlaceHolder(
        TextInputStyle.none,
        """
        The text input's style.
        
        Returns
        -------
        text_input_style : ``TextInputStyle``
        """
    )
    
    
    thumbnail = PlaceHolder(
        None,
        """
        The thumbnail or other accessory (button) of a section component.
        
        Returns
        -------
        thumbnail : ``Component``
        """
    )
    
    
    url = PlaceHolder(
        None,
        """
        Url to redirect to.
         
        > Mutually exclusive with the `custom_id` and `sku_id` fields if the component is a buttons.
        
        Returns
        -------
        url : `None | str`
        """
    )
    
    
    value = PlaceHolder(
        None,
        """
        The input component's default value.
        
        Returns
        -------
        value : `None | str`
        """
    )
