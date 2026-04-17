__all__ = ('RoleColorConfiguration',)

from scarletio import RichAttributeErrorBaseType

from ...color import Color

from .fields import (
    parse_color_primary, parse_color_secondary, parse_color_tertiary, put_color_primary, put_color_secondary,
    put_color_tertiary, validate_color_primary, validate_color_secondary, validate_color_tertiary,
)


class RoleColorConfiguration(RichAttributeErrorBaseType):
    """
    Role color configuration.
    
    Attributes
    ----------
    color_primary : ``Color``
        A role's primary color.
    
    color_secondary : ``None | Color``
        A role's secondary color.
    
    color_tertiary : ``None | Color``
        A role's tertiary color.
    """
    __slots__ = ('color_primary', 'color_secondary', 'color_tertiary')
    
    def __new__(cls, *, color_primary = ..., color_secondary = ..., color_tertiary = ...):
        """
        Creates a role color configuration with the given fields.
        
        Parameters
        ----------
        color_primary : ``None | int | Color``
            A role's primary color.
        
        color_secondary : ``None | int | Color``
            A role's secondary color.
        
        color_tertiary : ``None | int | Color``
            A role's tertiary color.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        
        ValueError
            - If a parameter's value is incorrect.
        """
        # color_primary
        if color_primary is ...:
            color_primary = Color()
        else:
            color_primary = validate_color_primary(color_primary)
        
        # color_secondary
        if color_secondary is ...:
            color_secondary = None
        else:
            color_secondary = validate_color_secondary(color_secondary)
        
        # color_tertiary
        if color_tertiary is ...:
            color_tertiary = None
        else:
            color_tertiary = validate_color_tertiary(color_tertiary)
        
        # Construct
        self = object.__new__(cls)
        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.color_tertiary = color_tertiary
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # color_primary
        color_primary = self.color_primary
        if color_primary:
            repr_parts.append(' color_primary = ')
            repr_parts.append(repr(color_primary))
            
            field_added = True
        else:
            field_added = False

        # color_secondary
        color_secondary = self.color_secondary
        if (color_secondary is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' color_secondary = ')
            repr_parts.append(repr(color_secondary))
            
        
        # color_tertiary
        color_tertiary = self.color_tertiary
        if (color_tertiary is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' color_tertiary = ')
            repr_parts.append(repr(color_tertiary))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        # color_primary
        hash_value = hash(self.color_primary)
        
        # color_secondary
        color_secondary = self.color_secondary
        if (color_secondary is not None):
            hash_value ^= 1
            hash_value ^= hash(color_secondary)

        # color_tertiary
        color_tertiary = self.color_tertiary
        if (color_tertiary is not None):
            hash_value ^= 2
            hash_value ^= hash(color_tertiary)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # color_primary
        if self.color_primary != other.color_primary:
            return False
        
        # color_secondary
        if self.color_secondary != other.color_secondary:
            return False
        
        # color_tertiary
        if self.color_tertiary != other.color_tertiary:
            return False
        
        return True
    
    
    @classmethod
    def create_empty(cls):
        """
        Creates an empty role color configuration.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.color_primary = Color()
        self.color_secondary = None
        self.color_tertiary = None
        return self
    
    
    @classmethod
    def create_from_color_primary(cls, color_primary):
        """
        Creates an empty role color configuration.
        
        Parameters
        ----------
        color_primary : ``Color``
            Primary color to create instance with.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.color_primary = color_primary
        self.color_secondary = None
        self.color_tertiary = None
        return self
    
    
    def to_data(self, defaults = False):
        """
        Converts the role color configuration into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_color_primary(self.color_primary, data, defaults)
        put_color_secondary(self.color_secondary, data, defaults)
        put_color_tertiary(self.color_tertiary, data, defaults)
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Parses a role configuration out from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.color_primary = parse_color_primary(data)
        self.color_secondary = parse_color_secondary(data)
        self.color_tertiary = parse_color_tertiary(data)
        return self
    
    
    def copy(self):
        """
        Copies the role color configuration.
        
        Returns
        -------
        self : `instance<cls>`
        """
        new = object.__new__(type(self))
        new.color_primary = self.color_primary
        new.color_secondary = self.color_secondary
        new.color_tertiary = self.color_tertiary
        return new
    
    
    def copy_with(self, *, color_primary = ..., color_secondary = ..., color_tertiary = ...):
        """
        Copies the role color configuration with the given fields.
        
        Parameters
        ----------
        color_primary : ``None | int | Color``
            A role's primary color.
        
        color_secondary : ``None | int | Color``
            A role's secondary color.
        
        color_tertiary : ``None | int | Color``
            A role's tertiary color.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        
        ValueError
            - If a parameter's value is incorrect.
        """
        # color_primary
        if color_primary is ...:
            color_primary = self.color_primary
        else:
            color_primary = validate_color_primary(color_primary)
        
        # color_secondary
        if color_secondary is ...:
            color_secondary = self.color_secondary
        else:
            color_secondary = validate_color_secondary(color_secondary)
        
        # color_tertiary
        if color_tertiary is ...:
            color_tertiary = self.color_tertiary
        else:
            color_tertiary = validate_color_tertiary(color_tertiary)
        
        # Construct
        new = object.__new__(type(self))
        new.color_primary = color_primary
        new.color_secondary = color_secondary
        new.color_tertiary = color_tertiary
        return new
