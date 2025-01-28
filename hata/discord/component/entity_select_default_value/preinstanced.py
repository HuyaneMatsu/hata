__all__ = ('EntitySelectDefaultValueType',)

from ...bases import Preinstance as P, PreinstancedBase


class EntitySelectDefaultValueType(PreinstancedBase, value_type = str):
    """
    Represents an entity select default option's type.
    
    Attributes
    ----------
    name : `str`
        The name of the entity select default option type.
    
    value : `str`
        The Discord side identifier value of the entity select default option type.
        
    Type Attributes
    ---------------
    Every predefined entity select default option type can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+---------------+
    | Type attribute name       | name                      | value         |
    +===========================+===========================+===============+
    | none                      | none                      | `''`          |
    +---------------------------+---------------------------+---------------+
    | channel                   | channel                   | `'channel'`   |
    +---------------------------+---------------------------+---------------+
    | role                      | role                      | `'role'`      |
    +---------------------------+---------------------------+---------------+
    | user                      | user                      | `'user'`      |
    +---------------------------+---------------------------+---------------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    channel = P('channel', 'channel')
    role = P('role', 'role')
    user = P('user', 'user')
