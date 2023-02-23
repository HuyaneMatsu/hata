__all__ = ('ApplicationCommandPermissionOverwriteTargetType',)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationCommandPermissionOverwriteTargetType(PreinstancedBase):
    """
    Represents an application command's permission's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command permission overwrite type.
    value : `int`
        The identifier value the application command permission overwrite type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandPermissionOverwriteTargetType``) items
        Stores the predefined ``ApplicationCommandPermissionOverwriteTargetType``-s. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command permission overwrite types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command permission overwrite types.
    
    Every predefined application command permission overwrite type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | Name      | Value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | role                  | role      | 1     |
    +-----------------------+-----------+-------+
    | user                  | user      | 2     |
    +-----------------------+-----------+-------+
    | channel               | channel   | 3     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    role = P(1, 'role',)
    user = P(2, 'user',)
    channel = P(3, 'channel',)
