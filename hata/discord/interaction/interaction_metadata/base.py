__all__ = ('InteractionMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...application_command import ApplicationCommandTargetType
from ...bases import PlaceHolder


class InteractionMetadataBase(RichAttributeErrorBaseType):
    """
    Base type for values assigned to ``InteractionEvent.message`` field.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new interaction metadata from the given parameters.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Construct
        self = object.__new__(cls)
        return self
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates the interaction metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to work with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls()
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an new interaction with it's attribute set as it's default values.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)    
    
    
    def copy(self):
        """
        Copies the interaction metadata.
        
        Returns
        -------
        new : `instance<cls>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the interaction metadata with the given fields.
        
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
        # Construct
        new = object.__new__(type(self))
        return new
    
    
    def copy_with_keyword_parameters(self, keyword_parameters):
        """
        Copies the interaction metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict<str, object>`
            Keyword parameters to work with.
        
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
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new interaction from the received data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            The received interaction field data.
        
        guild_id : `int` = `0`, Optional
            The respective guild's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False, guild_id = 0):
        """
        Converts the interaction into a json serailzable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        guild_id : `int` = `0`, Optional (Keyword only)
            The respective guild's identifier.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        return {}
    
    
    def __repr__(self):
        """Returns the interaction's representation."""
        repr_parts = []
        repr_parts.append('<')
        repr_parts.append(type(self).__name__)
        
        self._put_attribute_representations_into(repr_parts)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_attribute_representations_into(self, repr_parts):
        """
        Helper function to build representation of the interaction metadata.
        
        Parameters
        ----------
        repr_parts : `list` of `str`
            Integration metadata representation parts.
        
        Returns
        -------
        field_added : `bool`
            Whether any field was added.
        """
        return False
    
    
    def __hash__(self):
        """Returns the interaction's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two interactions are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other interaction. Must be the same type as `self`.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    application_command_id = PlaceHolder(
        0,
        """
        The represented application command's identifier number.
        
        Returns
        -------
        application_command_id : `int`
        """,
    )
    
    
    application_command_name = PlaceHolder(
        '',
        """
        The represented application command's name.
        
        Returns
        -------
        application_command_name : `str`
        """,
    )
    
    
    component = PlaceHolder(
        None,
        """
        The interacted component of a message component interaction.
        
        Returns
        -------
        components : ``None | InteractionComponent``
        """
    )
    
    
    components = PlaceHolder(
        None,
        """
        Submitted component values of a form submit interaction.
        
        Returns
        -------
        components : ``None | tuple<InteractionComponent>``
        """
    )
    
    
    custom_id = PlaceHolder(
        None,
        """
        Form interaction's custom identifier.
        
        Returns
        -------
        custom_id : `None | str`
        """,
    )
    
    
    options = PlaceHolder(
        None,
        """
        Application command option representations. Like sub-command or parameter.
            
        Returns
        -------
        options : `None`, `tuple` of ``InteractionOption``
        """,
    )
    
    
    target_id = PlaceHolder(
        0,
        """
        The interaction's target's identifier. Applicable for context commands.
        
        Returns
        -------
        target_id : `int`
        """,
    )
    
    
    target_type = PlaceHolder(
        ApplicationCommandTargetType.none,
        """
        The invoked application command's target type.
        
        Returns
        -------
        target_type : ``ApplicationCommandTargetType``
        """,
    )
    
    # Extra utility
    
    # Application command autocomplete
    
    def iter_options(self):
        """
        Iterates over the options of the interaction application command (autocomplete) interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``InteractionOption``
        """
        options = self.options
        if (options is not None):
            yield from options
    
    
    @property
    def focused_option(self):
        """
        Returns the focused option of the application command autocomplete interaction.
        
        Returns
        -------
        option : `None`, ``InteractionOption``
        """
        for option in self.iter_options():
            focused_option = option.focused_option
            if (focused_option is not None):
                return focused_option
    
    
    def get_non_focused_values(self):
        """
        Gets the non focused values of the interaction.
        
        Returns
        -------
        non_focused_options : `dict<str, None | str>`
        """
        return dict(self._iter_non_focused_values())
    
    
    def _iter_non_focused_values(self):
        """
        Iterates over the non focused values of the interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
            The option's name.
        
        value : `None | str`
            The option's value.
        """
        for option in self.iter_options():
            yield from option._iter_non_focused_values()
    
    
    def get_value_of(self, *option_names):
        """
        Gets the value for the option by the given name.
        
        Parameters
        ----------
        *option_names : `str`
            The option(s)'s name.
        
        Returns
        -------
        value : `None | str`
            The value, the user has been typed.
        """
        if not option_names:
            return
            
        option_name, *option_names = option_names
        
        for option in self.iter_options():
            if option.name == option_name:
                return option.get_value_of(*option_names)
    
    # Form submit
    
    def iter_components(self):
        """
        Iterates over the sub-components of a form-submit interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        component : ``InteractionComponent``
        """
        return
        yield
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the form submit interaction.
        
        This method is an iterable generator.
        
        Yields
        ------
        custom_id_is_multi_value_values : `(str, ComponentType, None | str | tuple<str>)`
        """
        return
        yield
