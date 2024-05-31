__all__ = ('MessageReferenceType',)

from ...bases import Preinstance as P, PreinstancedBase


class MessageReferenceType(PreinstancedBase):
    """
    Represents an message reference's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message reference type.
    value : `int`
        The Discord side identifier value of the message reference type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageReferenceType``) items
        Stores the created message reference type instances. This container is accessed when translating a Discord
        message reference type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The message reference types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message reference types.
    
    Every predefined message reference type can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | reply                     | reply                     | 0     |
    +---------------------------+---------------------------+-------+
    | forward                   | forward                   | 1     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    reply = P(0, 'reply')
    forward = P(1, 'forward')
