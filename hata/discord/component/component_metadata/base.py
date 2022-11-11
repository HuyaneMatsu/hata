__all__ = ('ComponentMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder

from .preinstanced import ButtonStyle, TextInputStyle


class ComponentMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for component metadata.
    """
    __slots__ = ()
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new component metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to build the metadata from.
        
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
        return f'<{self.__class__.__name__}>'
    
    
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
        data : `dict` of (`str`, `Any`) items
            Component data.
        
        Returns
        -------
        self : `instance<cls>`
            Returns the created component.
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Returns the component metadata's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def copy(self):
        """
        Copies the component metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self, keyword_parameters):
        """
        Copies the component metadata with changing it's field.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters defining which fields should be changed.
        
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
        return object.__new__(type(self))
    
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
        channel_types : `None`, `tuple` of ``ChannelType``
        """
    )
    
    
    components = PlaceHolder(
        None,
        """
        Sub-components.
        
        Returns
        -------
        components : `None`, `tuple` of ``Component``
        """
    )
    
    
    custom_id = PlaceHolder(
        None,
        """
        Custom identifier to detect which component was clicked (or used) by the user.
        
        > Mutually exclusive with the `url` field if the component is a buttons.
        
        Returns
        -------
        custom_id : `None`, `str`
        """
    )
    
    
    emoji = PlaceHolder(
        None,
        """
        Emoji of the component if applicable.
        
        Returns
        -------
        emoji : `None` ``Emoji``
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
    
    
    label = PlaceHolder(
        None,
        """
        Label of the component.
        
        Returns
        -------
        label : `None`, `str`
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
        options : `None`, `tuple` of ``StringSelectOption``
        """
    )
    
    
    placeholder = PlaceHolder(
        None,
        """
        Placeholder text of the select.
        
        Returns
        -------
        placeholder : `None`, `str`
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
    
    
    text_input_style = PlaceHolder(
        TextInputStyle.none,
        """
        The text input's style.
        
        Returns
        -------
        text_input_style : ``TextInputStyle``
        """
    )
    
    
    url = PlaceHolder(
        None,
        """
        Url to redirect to.
         
        > Mutually exclusive with the `custom_id` field if the component is a buttons.
        
        Returns
        -------
        url : `None`, `str`
        """
    )
    
    
    value = PlaceHolder(
        None,
        """
        The input component's default value.
        
        Returns
        -------
        value : `None`, `str`
        """
    )
