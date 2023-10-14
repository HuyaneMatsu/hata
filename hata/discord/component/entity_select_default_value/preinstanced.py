__all__ = ('EntitySelectDefaultValueType',)

from ...bases import Preinstance as P, PreinstancedBase


class EntitySelectDefaultValueType(PreinstancedBase):
    """
    Represents an entity select default option's type.
    
    Attributes
    ----------
    name : `str`
        The name of the entity select default option type.
    value : `str`
        The Discord side identifier value of the entity select default option type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``EntitySelectDefaultValueType``) items
        Stores the created entity select default option type instances. This container is accessed when translating a
        Discord entity select default option type's value to it's representation.
    VALUE_TYPE : `type` = `str`
        The entity select default option types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the entity select default option types.
    
    Every predefined entity select default option type can be accessed as class attribute as well:
    +---------------------------+---------------------------+---------------+
    | Class attribute name      | name                      | value         |
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
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    channel = P('channel', 'channel')
    role = P('role', 'role')
    user = P('user', 'user')
