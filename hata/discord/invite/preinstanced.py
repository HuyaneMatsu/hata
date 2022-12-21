__all__ = ('InviteTargetType', 'InviteType')

from ..bases import Preinstance as P, PreinstancedBase


class InviteTargetType(PreinstancedBase):
    """
    Represents an ``Invite``'s target's type.
    
    Attributes
    ----------
    name : `str`
        The name of the target type.
    value : `int`
        The Discord side identifier value of the target type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InviteTargetType``) items
        Stores the predefined ``InviteTargetType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The invite target types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the invite target types.
    
    Every predefined invite target type can be accessed as class attribute as well:
    
    +-------------------------------+-------------------------------+-------+
    | Class attribute name          | name                          | value |
    +===============================+===============================+=======+
    | none                          | none                          | 0     |
    +-------------------------------+-------------------------------+-------+
    | stream                        | stream                        | 1     |
    +-------------------------------+-------------------------------+-------+
    | embedded_application          | embedded application          | 2     |
    +-------------------------------+-------------------------------+-------+
    | role_subscription_purchase    | role subscription purchase    | 2     |
    +-------------------------------+-------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    stream = P(1, 'stream')
    embedded_application = P(2, 'embedded application')
    role_subscription_purchase = P(3, 'role subscription purchase')


class InviteType(PreinstancedBase):
    """
    Represents an ``Invite``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the invite type.
    value : `int`
        The Discord side identifier value of the invite type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InviteType``) items
        Stores the predefined ``InviteType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The invite types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the invite types.
    
    Every predefined invite type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | name                  | value |
    +=======================+=======================+=======+
    | guild                 | guild                 | 0     |
    +-----------------------+-----------------------+-------+
    | group_channel         | group channel         | 1     |
    +-----------------------+-----------------------+-------+
    | friend                | friend                | 2     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    guild = P(0, 'guild')
    group_channel = P(1, 'group channel')
    friend = P(2, 'friend')
