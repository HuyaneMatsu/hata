__all__ = ('EntitySelectDefaultValue',)

from scarletio import RichAttributeErrorBaseType

from .fields import parse_id, parse_type, put_id, put_type, validate_id, validate_type


class EntitySelectDefaultValue(RichAttributeErrorBaseType):
    """
    Entity presented in an entity select by default.
    
    Attributes
    ----------
    id : `int`
        The represented entity's identifier.
    
    type : ``EntitySelectDefaultValueType``
        The represented entity's type.
    """
    def __new__(cls, option_type, entity_id):
        """
        Creates a new component option with the given parameters.
        
        Parameters
        ----------
        option_type : ``str | EntitySelectDefaultValueType``
            The represented entity's type.
        
        entity_id : `int | str`
            The represented entity's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        entity_id = validate_id(entity_id)
        option_type = validate_type(option_type)
        
        # Construct
        self = object.__new__(cls)
        self.id = entity_id
        self.type = option_type
        return self
    
    
    @classmethod
    def from_fields(cls, option_type, entity_id):
        """
        Creates a new entity select default option with the given fields.
        
        > This constructor does not validation, ment for internal use.
        
        Parameters
        ----------
        option_type : ``EntitySelectDefaultValueType``
            The represented entity's type.
        
        entity_id : `int`
            The represented entity's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Construct
        self = object.__new__(cls)
        self.id = entity_id
        self.type = option_type
        return self
    

    @classmethod
    def from_data(cls, data):
        """
        Creates a new string select option from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            String select option data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the string select option to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_id(self.id, data, defaults)
        put_type(self.type, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the string select option's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # id
        repr_parts.append(', id = ')
        repr_parts.append(repr(self.id))
        
         # type
        option_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(option_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(option_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two string select options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        if self.id != other.id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the string select option's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # type
        hash_value ^= hash(self.type)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the string select option.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = self.id
        new.type = self.type
        return new
    
    
    def copy_with(self, entity_id = ..., option_type = ...):
        """
        Copes the string select with modifying it's defined attributes.
        
        Parameters
        ----------
        entity_id : `int | str`, Optional (Keyword only)
            The represented entity's identifier.
        
        option_type : ``str | EntitySelectDefaultValueType``, Optional (Keyword only)
            The represented entity's type.
        
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
        # entity_id
        if entity_id is ...:
            entity_id = self.id
        else:
            entity_id = validate_id(entity_id)
        
        # option_type
        if option_type is ...:
            option_type = self.type
        else:
            option_type = validate_type(option_type)
        
        # Construct
        new = object.__new__(type(self))
        new.id = entity_id
        new.type = option_type
        return new
