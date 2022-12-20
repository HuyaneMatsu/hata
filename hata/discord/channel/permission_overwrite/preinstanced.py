__all__ = ('PermissionOverwriteTargetType',)

from scarletio import set_docs, export

from ....env import API_VERSION

from ...bases import Preinstance as P, PreinstancedBase


@export
class PermissionOverwriteTargetType(PreinstancedBase):
    INSTANCES = {}
    VALUE_TYPE = str if API_VERSION in (6, 7) else int
    DEFAULT_NAME = 'UNDEFINED'
    
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
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PermissionOverwriteTargetType``) items
        Stores the predefined ``PermissionOverwriteTargetType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `str`
        The permission overwrite target types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the permission overwrite target types.
    
    Every predefined permission overwrite target type can be accessed as class attribute as well:
    
    +-----------------------+---------------+---------------+
    | Class attribute name  | name          | value         |
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
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PermissionOverwriteTargetType``) items
        Stores the predefined ``PermissionOverwriteTargetType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The permission overwrite target types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the permission overwrite target types.
    
    Every predefined permission overwrite target type can be accessed as class attribute as well:
    
    +-----------------------+---------------+---------------+
    | Class attribute name  | name          | value         |
    +=======================+===============+===============+
    | unknown               | unknown       | -1            |
    +-----------------------+---------------+---------------+
    | role                  | role          | 0             |
    +-----------------------+---------------+---------------+
    | user                  | user          | 1             |
    +-----------------------+---------------+---------------+
    """
)
