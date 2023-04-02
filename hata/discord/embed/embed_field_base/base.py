__all__ = ('EmbedFieldBase',)

from scarletio import RichAttributeErrorBaseType


class EmbedFieldBase(RichAttributeErrorBaseType):
    """
    Base type for embed fields.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new embed field with the given parameters.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    def __len__(self):
        """Returns the embed field's contents' length."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the embed field is not empty."""
        return False
    
    
    def __repr__(self):
        """Returns the embed field's representation."""
        repr_parts = ['<', self.__class__.__name__]
        self._put_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Appends the embed field's representation parts.
        
        Parameters
        ----------
        repr_parts : `list` of `str`
        """
        pass
    
    
    def __hash__(self):
        """Returns the embed field's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two embed fields are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two embed fields.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed field from the data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed field data.
        
        Returns
        -------
        embed_field : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the embed field to json serializable object representing it.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the embed field by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : `None`, ``Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy(self):
        """
        Copies the embed field returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the embed field with the given parameters.
        
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
        return object.__new__(type(self))
    
    
    @property
    def contents(self):
        """
        Returns the contents of the embed field.
        
        Returns
        -------
        contents : `list` of `str`
        """
        return [*self.iter_contents()]
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the embed field.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        return
        yield
