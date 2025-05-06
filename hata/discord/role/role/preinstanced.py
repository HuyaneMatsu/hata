__all__ = ('RoleManagerType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..role_manager_metadata import (
    RoleManagerMetadataApplicationRoleConnection, RoleManagerMetadataBase, RoleManagerMetadataBooster,
    RoleManagerMetadataBot, RoleManagerMetadataIntegration, RoleManagerMetadataSubscription
)

class RoleManagerType(PreinstancedBase, value_type = int):
    """
    Represents a managed role's manager type.
    
    Attributes
    ----------
    name : `str`
        The name of the role manager type.
    
    value : `int`
        The identifier value the role manager type.
    
    Type Attributes
    ---------------
    Every predefined role manager type can be accessed as type attribute as well:
    
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | Type attribute name           | Name                          | Value | Metadata type                                     |
    +===============================+===============================+=======+===================================================+
    | none                          | none                          | 0     | ``RoleManagerMetadataBase``                       |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | unset                         | unset                         | 1     | ``RoleManagerMetadataBase``                       |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | unknown                       | unknown                       | 2     | ``RoleManagerMetadataBase``                       |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | bot                           | bot                           | 3     | ``RoleManagerMetadataBot``                        |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | booster                       | booster                       | 4     | ``RoleManagerMetadataBooster``                    |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | integration                   | integration                   | 5     | ``RoleManagerMetadataIntegration``                |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | subscription                  | subscription                  | 6     | ``RoleManagerMetadataSubscription``               |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | application_role_connection   | application role connection   | 7     | ``RoleManagerMetadataApplicationRoleConnection``  |
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    """
    __slots__ = ('metadata_type', )
    
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates a new scheduled event entity type instance from the given parameters.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the scheduled event entity type.
        
        name : `None | str` = `None`, Optional
            The name of the scheduled event entity type.
        
        metadata_type : `None | type<RoleManagerMetadataBase>` = `None`, Optional
            The role manager's metadata's type.
        """
        if metadata_type is None:
            metadata_type = RoleManagerMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    def __bool__(self):
        """Returns whether the role manager's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    
    none = P(0, 'none', RoleManagerMetadataBase)
    unset = P(1, 'unset', RoleManagerMetadataBase)
    unknown = P(2, 'unknown', RoleManagerMetadataBase)
    bot = P(3, 'bot', RoleManagerMetadataBot)
    booster = P(4, 'booster', RoleManagerMetadataBooster)
    integration = P(5, 'integration', RoleManagerMetadataIntegration)
    subscription = P(6, 'subscription', RoleManagerMetadataSubscription)
    application_role_connection = P(7, 'application role connection', RoleManagerMetadataApplicationRoleConnection)
