__all__ = ('RoleManagerMetadataIntegration',)

from scarletio import copy_docs, include

from .base import RoleManagerMetadataBase
from .fields import parse_integration_id, put_integration_id_into, validate_integration_id


create_partial_integration_from_id = include('create_partial_integration_from_id')


class RoleManagerMetadataIntegration(RoleManagerMetadataBase):
    """
    Role manager metadata of a role managed by a integration.
    
    Attributes
    ----------
    integration_id : `int`
        The manager integration's identifier.
    """
    __slots__ = ('integration_id', )
    
    def __new__(cls, *, integration_id = ...):
        """
        Creates a new role manager.
        
        Parameters
        ----------
        integration_id : `int`, ``Integration``, Optional (Keyword only)
            The manager integration's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # integration_id
        if integration_id is ...:
            integration_id = 0
        else:
            integration_id = validate_integration_id(integration_id)
        
        self = object.__new__(cls)
        self.integration_id = integration_id
        return self
    
    
    @classmethod
    @copy_docs(RoleManagerMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.integration_id = parse_integration_id(data)
        return self
    
    
    @copy_docs(RoleManagerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_integration_id_into(self.integration_id, data, defaults)
        return data
    
    
    @copy_docs(RoleManagerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' integration_id = ')
        repr_parts.append(repr(self.integration_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(RoleManagerMetadataBase.__hash__)
    def __hash__(self):
        return self.integration_id
    
    
    @copy_docs(RoleManagerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.integration_id == other.integration_id
    
    
    @copy_docs(RoleManagerMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.integration_id = self.integration_id
        return new
    
    
    def copy_with(self, *, integration_id = ...):
        """
        Copies the role manager metadata with the given fields.
        
        Parameters
        ----------
        integration_id : `int`, ``Integration``, Optional (Keyword only)
            The manager integration's identifier.
        
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
        # integration_id
        if integration_id is ...:
            integration_id = self.integration_id
        else:
            integration_id = validate_integration_id(integration_id)
        
        new = object.__new__(type(self))
        new.integration_id = integration_id
        return new
    
    
    @property
    @copy_docs(RoleManagerMetadataBase.manager_id)
    def manager_id(self):
        return self.integration_id
    
    
    @property
    @copy_docs(RoleManagerMetadataBase.manager)
    def manager(self):
        return create_partial_integration_from_id(self.integration_id)
