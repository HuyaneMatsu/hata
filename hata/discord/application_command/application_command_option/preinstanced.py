__all__ = ('ApplicationCommandOptionType',)

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationCommandOptionType(PreinstancedBase):
    """
    Represents an application command option's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command option type.
    value : `int`
        The identifier value the application command option type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandOptionType``) items
        Stores the predefined ``ApplicationCommandOptionType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command option types.
    
    Every predefined application command option type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | sub_command           | sub-command       | 1     |
    +-----------------------+-------------------+-------+
    | sub_command_group     | sub-command group | 2     |
    +-----------------------+-------------------+-------+
    | string                | string            | 3     |
    +-----------------------+-------------------+-------+
    | integer               | integer           | 4     |
    +-----------------------+-------------------+-------+
    | boolean               | boolean           | 5     |
    +-----------------------+-------------------+-------+
    | user                  | user              | 6     |
    +-----------------------+-------------------+-------+
    | channel               | channel           | 7     |
    +-----------------------+-------------------+-------+
    | role                  | role              | 8     |
    +-----------------------+-------------------+-------+
    | mentionable           | mentionable       | 9     |
    +-----------------------+-------------------+-------+
    | float                 | float             | 10    |
    +-----------------------+-------------------+-------+
    | attachment            | attachment        | 11    |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    sub_command = P(1, 'sub-command')
    sub_command_group = P(2, 'sub-command group')
    string = P(3, 'string')
    integer = P(4, 'integer')
    boolean = P(5, 'boolean')
    user = P(6, 'user')
    channel = P(7, 'channel')
    role = P(8, 'role')
    mentionable = P(9, 'mentionable')
    float = P(10, 'float')
    attachment = P(11, 'attachment')
