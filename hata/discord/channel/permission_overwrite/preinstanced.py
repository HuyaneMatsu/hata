__all__ = ('PermissionOverwriteTargetType',)

from scarletio import set_docs, export

from ....env import API_VERSION

from ...bases import Preinstance as P, PreinstancedBase


@export
class PermissionOverwriteTargetType(PreinstancedBase, value_type = (str if API_VERSION in (6, 7) else int)):
    __slots__ = ()
    
    unknown = P('unknown' if API_VERSION in (6, 7) else -1, 'unknown')
    role = P('role' if API_VERSION in (6, 7) else 0, 'role')
    user = P('member' if API_VERSION in (6, 7) else 1, 'user')


set_docs(PermissionOverwriteTargetType,
    """
    Represents a permission overwrite's target's type.
    
    Attributes
    ----------
    name : `str`
        The name of the permission overwrite target type.
    
    value : `int`
        The identifier value the permission overwrite target type.
    
    Type Attributes
    ---------------
    Every predefined permission overwrite target type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | unknown               | unknown       | `'unknown'`   |
    +-----------------------+---------------+---------------+
    | role                  | role          | `'role'`      |
    +-----------------------+---------------+---------------+
    | user                  | user          | `'member'`    |
    +-----------------------+---------------+---------------+
    """
    if API_VERSION in (6, 7) else
    """
    Represents a permission overwrite's target's type.
    
    Attributes
    ----------
    name : `str`
        The name of the permission overwrite target type.
    
    value : `int`
        The identifier value the permission overwrite target type.
    
    Type Attributes
    ---------------
    Every predefined permission overwrite target type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
    +=======================+===============+===============+
    | unknown               | unknown       | -1            |
    +-----------------------+---------------+---------------+
    | role                  | role          | 0             |
    +-----------------------+---------------+---------------+
    | user                  | user          | 1             |
    +-----------------------+---------------+---------------+
    """
)
