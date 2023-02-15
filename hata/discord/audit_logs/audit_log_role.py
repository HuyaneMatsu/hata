__all__ = ('AuditLogRole',)

from ..bases import DiscordEntity
from ..role import Role


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
    __slots__ = ('id', 'name')
    
    def __new__(cls, data):
        """
        Creates a new audit log role.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            partial role data.
        """
        role_id = int(data['id'])
        role_name = data.get('name', '')
        
        self = object.__new__(cls)
        self.id = role_id
        self.name = role_name
        return self
    
    
    def __repr__(self):
        """Returns the role's representation."""
        return f'<{self.__class__.__name__} id = {self.id!r}, name = {self.name!r}>'
    
    
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
