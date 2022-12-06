__all__ = ('ApplicationType',)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationType(PreinstancedBase):
    """
    Represents an application type.
    
    Attributes
    ----------
    name : `str`
        The name of the application type.
    value : `int`
        The Discord side identifier value of the application type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationType``) items
        Stores the created application type instances. This container is accessed when translating a Discord
        application type's value to it's representation.
    VALUE_TYPE : `type` = `int`
        The application types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the application types.
    
    Every predefined application type can be accessed as class attribute as well:
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | game                      | game                      | 1     |
    +---------------------------+---------------------------+-------+
    | music                     | music                     | 2     |
    +---------------------------+---------------------------+-------+
    | ticketed_event            | ticketed event            | 3     |
    +---------------------------+---------------------------+-------+
    | guild_role_subscription   | guild role subscription   | 4     |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    game = P(1, 'game')
    music = P(2, 'music')
    ticketed_event = P(3, 'ticketed event')
    guild_role_subscription = P(4, 'guild role subscription')
