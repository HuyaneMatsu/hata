__all__ = ('GuildJoinRequestFormResponse',)

from scarletio import RichAttributeErrorBaseType


class GuildJoinRequestFormResponse(RichAttributeErrorBaseType):
    """
    Form response of a guild join request.
    
    > No known fields.
    """
    def __new__(cls):
        """
        Creates a new guild join request form response with the given fields.
        
        > No known fields.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        self = object.__new__(cls)
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild join request form response instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items.
            Form response data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the guild join request form response into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        return data
    
    
    def __repr__(self):
        """Returns the guild join request form response's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # nothing yet
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two join requests responses are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        # Nothing yet
        
        return True
    
    
    def __hash__(self):
        """Returns the guild join request form response's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the guild join request form response.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        return new
    
    
    def copy_with(self):
        """
        Copies the guild join request form response with the given data.
        
        > No known fields.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        new = object.__new__(type(self))
        return new
