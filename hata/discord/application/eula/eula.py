__all__ = ('EULA', )

from ...bases import DiscordEntity
from ...core import EULAS

from .fields import (
    parse_content, parse_id, parse_name, put_content_into, put_id_into, put_name_into, validate_content, validate_id,
    validate_name
)


PRECREATE_FIELDS = {
    'content': ('content', validate_content),
    'name': ('name', validate_name),
}


class EULA(DiscordEntity, immortal = True):
    """
    Represents a Discord end-user license agreement
    
    Attributes
    ----------
    content : `None`, `str`
        The eula's content.
    id : `int`
        The unique identifier number of the eula.
    name : `str`
        The eula's name.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = ('content', 'name')
    
    
    def __new__(cls, *, content = ..., name = ...):
        """
        Creates a new partial application eula.
        
        Parameters
        ----------
        content : `None`, `str`, Optional (Keyword only)
            The eula's content.
        
        name : `str`, Optional (Keyword only)
            The eula's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # content
        if content is ...:
            content = None
        else:
            content = validate_content(content)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        self = object.__new__(cls)
        self.content = content
        self.id = 0
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new eula instance from the given data.
        
        If the eula already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Eula data.
        """
        eula_id = parse_id(data)
        
        try:
            self = EULAS[eula_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = eula_id
            EULAS[eula_id] = self
        
        self._update_attributes(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the eula into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        put_content_into(self.content, data, defaults)
        put_name_into(self.name, data, defaults)
        
        return data
    
    
    def _update_attributes(self, data):
        """
        Updates the eula with the received data from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.content = parse_content(data)
        self.name = parse_name(data)
    
    
    @classmethod
    def _create_empty(cls, entity_id):
        """
        Creates a new eula instance with it's attribute set to their default values.
        
        Parameters
        ----------
        entity_id : `int`
            The entity's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.content = None
        self.id = entity_id
        self.name = ''
        return self
    

    @classmethod
    def precreate(cls, eula_id, **keyword_parameters):
        """
        Creates an eula entity instance. When the eula is loaded with the same id, it will be picked up.
        
        Parameters
        ----------
        eula_id : `int`
            The eula's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        content : `str`, Optional (Keyword only)
            The eula's content.
        
        name : `str`, Optional (Keyword only)
            The eula's name.
        
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
        eula_id = validate_id(eula_id)

        if keyword_parameters:
            processable = []
            extra = None
            
            while keyword_parameters:
                field_name, field_value = keyword_parameters.popitem() 
                try:
                    attribute_name, validator = PRECREATE_FIELDS[field_name]
                except KeyError:
                    if extra is None:
                        extra = {}
                    extra[field_name] = field_value
                    continue
                
                attribute_value = validator(field_value)
                processable.append((attribute_name, attribute_value))
                continue
                
            if (extra is not None):
                raise TypeError(
                    f'Unused or unsettable keyword parameters: {extra!r}.'
                )
        
        else:
            processable = None
        
        try:
            self = EULAS[eula_id]
        except KeyError:
            self = cls._create_empty(eula_id)
            EULAS[eula_id] = self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    def __repr__(self):
        """Returns the eula's representation"""
        repr_parts = ['<', self.__class__.__name__]
        
        eula_id = self.id
        if eula_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two eulas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two eulas are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self.id != other.id:
                return False
        
        # content
        if self.content != other.content:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    

    
    def __hash__(self):
        """Returns the hash value of the eula."""
        hash_value = 0
        
        # content
        content = self.content
        if (content is not None):
            hash_value ^= hash(content)
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the eula.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.content = self.content
        new.id = 0
        new.name = self.name
        return new
    
    
    def copy_with(self, *, content = ..., name = ...):
        """
        Copies the eula with the defined fields.
        
        Parameters
        ----------
        content : `None`, `str`, Optional (Keyword only)
            The eula's content.
        
        name : `str`, Optional (Keyword only)
            The eula's name.
        
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
        # content
        if content is ...:
            content = self.content
        else:
            content = validate_content(content)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        new = object.__new__(type(self))
        new.content = content
        new.id = 0
        new.name = name
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the entity is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (self.id == 0)
