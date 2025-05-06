__all__ = ('ApplicationCommandPermissionOverwriteTargetType',)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationCommandPermissionOverwriteTargetType(PreinstancedBase, value_type = int):
    """
    Represents an application command's permission's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command permission overwrite type.
    
    value : `int`
        The identifier value the application command permission overwrite type.
    
    Type Attributes
    ---------------
    Every predefined application command permission overwrite type can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | Name      | Value |
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
    __slots__ = ()
    
    none = P(0, 'none',)
    role = P(1, 'role',)
    user = P(2, 'user',)
    channel = P(3, 'channel',)
