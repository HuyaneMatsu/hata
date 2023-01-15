__all__ = ('RoleManagerType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..role_manager_metadata import (
    RoleManagerMetadataApplicationRoleConnection, RoleManagerMetadataBase, RoleManagerMetadataBooster,
    RoleManagerMetadataBot, RoleManagerMetadataIntegration, RoleManagerMetadataSubscription
)

class RoleManagerType(PreinstancedBase):
    """
    Represents a managed role's manager type.
    
    Attributes
    ----------
    name : `str`
        The name of the role manager type.
    value : `int`
        The identifier value the role manager type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``RoleManagerType``) items
        Stores the predefined ``RoleManagerType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The role manager types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the role manager types.
    
    Every predefined role manager type can be accessed as class attribute as well:
    
    +-------------------------------+-------------------------------+-------+---------------------------------------------------+
    | Class attribute name          | Name                          | Value | Metadata type                                     |
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
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('metadata_type', )
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new role manager type with the given value.
        
        Parameters
        ----------
        value : `int`
            Value representing the role manager.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.name = value
        self.value = value
        self.metadata_type = RoleManagerMetadataBase
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates a new scheduled event entity type instance from the given parameters.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the scheduled event entity type.
        name : `str`
            The name of the scheduled event entity type.
        metadata_type : `None`, ``RoleManagerMetadataBase`` subclass
            The role manager's metadata's type.
        """
        self.name = name
        self.value = value
        self.metadata_type = metadata_type
        self.INSTANCES[value] = self
    
    
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
