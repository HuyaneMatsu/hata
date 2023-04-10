__all__ = ('ApplicationCommandOptionMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder

from .constants import APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT


class ApplicationCommandOptionMetadataBase(RichAttributeErrorBaseType):
    """
    Base type for application command metadatas.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new application command option metadata with the given parameters.
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new application command option metadata with the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters passed to ``ApplicationCommandOption.__new__``.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        return cls()
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new application command option metadata from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application command option data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application command option metadata to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def __repr__(self):
        """Returns the application command option metadata's representation."""
        repr_parts = ['<', self.__class__.__name__]
        self._add_type_specific_repr_fields(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _add_type_specific_repr_fields(self, repr_parts):
        """
        Adds the type specific fields into the given into the representation parts.
        
        Parameters
        ----------
        repr_parts : `list` of `str`
        """
    
    def __eq__(self, other):
        """Returns whether the two application command options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two application command options are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be the same type as `self`.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the application command option metadata."""
        return 0
    
    
    def copy(self):
        """
        Copies the application command option metadata.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the application command option metadata with the given fields.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        return self.copy()
    
    
    def copy_with_keyword_parameters(self, keyword_parameters):
        """
        Copies the application command option metadata with the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters passed to ``ApplicationCommandOption.copy_with``.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        return self.copy_with()
    
    
    autocomplete = PlaceHolder(
        False,
        """
        Whether the option supports auto completion.
        
        Applicable for string, integer and float options.
        
        Returns
        -------
        autocomplete : `bool`
        """
    )
    
    
    channel_types = PlaceHolder(
        None,
        """
        The accepted channel types by the option.
        
        Applicable for channel options.
        
        Returns
        -------
        channel_types : `None`, `tuple` of ``ChannelType``
        """
    )
    
    
    choices = PlaceHolder(
        None,
        """
        Choices for `str` and `int` types for the user to pick from.
        
        Applicable for string, integer and float options.
        
        Returns
        -------
        choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        """
    )
    
    
    default = PlaceHolder(
        False,
        """
        Whether the option is the default one.
        
        Applicable for sub-command options.
        
        Returns
        -------
        default : `bool`
        """
    )
    
    
    max_length = PlaceHolder(
        APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT,
        """
        The maximum input length allowed for this option.
        
        Applicable for string options.
        
        Returns
        -------
        max_length : `int`
        """
    )
    
    
    max_value = PlaceHolder(
        None,
        """
        The maximal value permitted for this option.
        
        Applicable for integer and float options.
        
        Returns
        -------
        max_value : `None`, `int`, `float`
        """
    )
    
    
    min_length = PlaceHolder(
        APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT,
        """
        The minimal input length allowed for this option.
        
        Applicable for string options.
        
        Returns
        -------
        min_length : `int`
        """
    )
    
    
    min_value = PlaceHolder(
        None,
        """
        The minimal value permitted for this option.
        
        Applicable for integer and float options.
        
        Returns
        -------
        min_value : `None`, `int`, `float`
        """
    )
    
    
    options = PlaceHolder(
        None,
        """
        Contains the option's parameter or its sub-commands (or groups).
        
        Applicable for sub-command and sub-command group options.
        
        Returns
        -------
        options : `None`, `tuple` of ``ApplicationCommandOption``
        """
    )
    
    
    required = PlaceHolder(
        False,
        """
        Whether the parameter is required.
        
        Applicable for all parameter option.
        
        Returns
        -------
        required : `bool`
        """
    )
