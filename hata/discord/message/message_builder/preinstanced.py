__all__ = ('MessageReferenceType',)

from ...bases import Preinstance as P, PreinstancedBase


class MessageReferenceType(PreinstancedBase, value_type = int):
    """
    Represents an message reference's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message reference type.
    
    value : `int`
        The Discord side identifier value of the message reference type.
        
    Type Attributes
    ---------------
    Every predefined message reference type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | name                      | value |
    +===========================+===========================+=======+
    | reply                     | reply                     | 0     |
    +---------------------------+---------------------------+-------+
    | forward                   | forward                   | 1     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    # predefined
    reply = P(0, 'reply')
    forward = P(1, 'forward')
