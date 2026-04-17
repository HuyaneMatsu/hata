__all__ = ('MessageActivityType',)

from ...bases import Preinstance as P, PreinstancedBase


class MessageActivityType(PreinstancedBase, value_type = int):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the message activity type.
    
    value : `int`
        The Discord side identifier value of the message activity type.
    
    Type Attributes
    ---------------
    Every predefined message activity type can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | join                  | join          | 1     |
    +-----------------------+---------------+-------+
    | spectate              | spectate      | 2     |
    +-----------------------+---------------+-------+
    | listen                | listen        | 3     |
    +-----------------------+---------------+-------+
    | watch                 | watch         | 4     |
    +-----------------------+---------------+-------+
    | join_request          | join_request  | 5     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    join = P(1, 'join')
    spectate = P(2, 'spectate')
    listen = P(3, 'listen')
    watch = P(4, 'watch')
    join_request = P(5, 'join_request')
