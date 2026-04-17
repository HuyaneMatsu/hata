__all__ = ('InteractionComponentMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder


class InteractionComponentMetadataBase(RichAttributeErrorBaseType):
    """
    Base type for interaction component metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new interaction component metadata from the given fields.
        
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
        Creates a new interaction component metadata from the given keyword parameters.
        
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
        """Returns repr(self)."""
        return f'<{type(self).__name__}>'
    
    
    def __hash__(self):
        """Returns hash(self)."""
        return 0
    
    
    def __eq__(self, other):
        """Returns self == other."""
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
    
    
    def _match_to_component(self, other):
        """
        matches self to an other component.
        
        Parameters
        ----------
        other : ``ComponentMetadataBase``
        
        Returns
        -------
        matching : `bool`
        """
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new interaction component metadata from the given data.
        
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
    
    
    def to_data(self, *, defaults = False):
        """
        Returns the interaction component metadata's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        return {}
    
    
    def copy(self):
        """
        Copies the interaction component metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the interaction component metadata with the given fields.
        
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
        Copies the interaction component metadata with the given keyword parameters.
        
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
    
    
    def iter_custom_ids_and_values(self):
        """
        Iterates over all the `custom_id`-s and values of the interaction component metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : `(str, ComponentType, None | str | tuple<str>)`
        """
        return
        yield
    
    
    component = PlaceHolder(
        None,
        """
        The sub-component nested inside. Applicable for the label component.
        
        Returns
        -------
        component : ``None | Component``
        """
    )
    
    
    components = PlaceHolder(
        None,
        """
        Sub-components nested inside. Applicable for the row component.
        
        Returns
        -------
        components : ``None | tuple<Component>``
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
    
    
    thumbnail = PlaceHolder(
        None,
        """
        The thumbnail or other accessory (button) of a section component.
        
        Returns
        -------
        thumbnail : ``None | Component``
        """
    )
    
    
    value = PlaceHolder(
        None,
        """
        The component's value defined by the user.
        
        Returns
        -------
        value : `None | str`
        """
    )
    
    
    values = PlaceHolder(
        None,
        """
        The component's values defined by the user.
        
        Returns
        -------
        values : `None | tuple<str>`
        """
    )
