__all__ = ('InviteTargetType', )

from ..bases import PreinstancedBase, Preinstance as P

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
        Stores the predefined ``InviteTargetType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The invite target types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the invite target types.
    
    Every predefined invite target type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | name                  | value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | stream                | stream                | 1     |
    +-----------------------+-----------------------+-------+
    | embedded_application  | embedded_application  | 2     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none', )
    stream = P(1, 'stream', )
    embedded_application = P(2, 'embedded_application', )
