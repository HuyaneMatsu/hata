__all__ = ('AuditLogRole',)

from ...bases import DiscordEntity
from ...role import Role

from .fields import parse_id, parse_name, put_id, put_name, validate_id, validate_name


class AuditLogRole(DiscordEntity):
    """
    Represents a role object received with audit logs.
    
    Parameters
    ----------
    id : `int`
        The role's identifier.
    name : `str`
        The role's name.
    """
    __slots__ = ('name',)
    
    def __new__(cls, *, role_id = ..., name = ...):
        """
        Creates a new new audit log role with the given parameters.
        
        Parameters
        ----------
        role_id : `int`, Optional (Keyword only)
            The represented role's identifier.
        name : `str`, Optional (Keyword only)
            The name of the role.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # role_id
        if role_id is ...:
            role_id = 0
        else:
            role_id = validate_id(role_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Construct
        self = object.__new__(cls)
        self.id = role_id
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new audit log role.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Audit log role data.
        """
        role_id = parse_id(data)
        name = parse_name(data)
        
        self = object.__new__(cls)
        self.id = role_id
        self.name = name
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the audit log role field.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_id(self.id, data, defaults)
        put_name(self.name, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the audit log role's representation."""
        repr_parts = ['<',self.__class__.__name__]
        
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two audit log role's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two audit log role's are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """returns the audit log role's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= hash(self.id)
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the audit log role returning a new one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        return new
    
    
    def copy_with(self, *, role_id = ..., name = ...):
        """
        Copies the audit log role with the given fields.
        
        Parameters
        ----------
        role_id : `int`, Optional (Keyword only)
            The represented role's identifier.
        name : `str`, Optional (Keyword only)
            The name of the role.
        
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
        # role_id
        if role_id is ...:
            role_id = self.id
        else:
            role_id = validate_id(role_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Construct
        new = object.__new__(type(self))
        new.id = role_id
        new.name = name
        return new
    
    
    @property
    def entity(self):
        """
        Resolves the audit log role's entity.
        
        If the entity is not cached creates a new.
        
        Returns
        -------
        role : ``Role``
        """
        return Role.precreate(self.id, name = self.name)
