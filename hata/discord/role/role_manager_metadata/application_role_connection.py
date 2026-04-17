__all__ = ('RoleManagerMetadataApplicationRoleConnection',)

from scarletio import copy_docs

from .constants import APPLICATION_ROLE_CONNECTION_KEY
from .integration import RoleManagerMetadataIntegration


class RoleManagerMetadataApplicationRoleConnection(RoleManagerMetadataIntegration):
    """
    Role manager metadata of a role managed by an application role connection.
    
    Attributes
    ----------
    integration_id : `int`
        The manager integration's identifier.
    """
    __slots__ = ()
    
    @copy_docs(RoleManagerMetadataIntegration.to_data)
    def to_data(self, *, defaults = False):
        data = RoleManagerMetadataIntegration.to_data(self)
        data[APPLICATION_ROLE_CONNECTION_KEY] = None
        return data
