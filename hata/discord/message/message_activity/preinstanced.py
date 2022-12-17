__all__ = ('MessageActivityType',)

from ...bases import Preinstance as P, PreinstancedBase


class MessageActivityType(PreinstancedBase):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the message activity type.
    value : `int`
        The Discord side identifier value of the message activity type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageActivityType``) items
        Stores the predefined ``MessageActivityType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message activity types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message activity types.
    
    Every predefined message activity type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    join = P(1, 'join')
    spectate = P(2, 'spectate')
    listen = P(3, 'listen')
    watch = P(4, 'watch')
    join_request = P(5, 'join_request')
