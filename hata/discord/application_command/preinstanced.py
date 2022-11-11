__all__ = (
    'ApplicationCommandOptionType', 'ApplicationCommandPermissionOverwriteTargetType', 'ApplicationCommandTargetType',
    'APPLICATION_COMMAND_CONTEXT_TARGET_TYPES'
)

from ..bases import Preinstance as P, PreinstancedBase


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
    | sub_command           | sub_command       | 1     |
    +-----------------------+-------------------+-------+
    | sub_command_group     | sub_command_group | 2     |
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
    sub_command = P(1, 'sub_command',)
    sub_command_group = P(2, 'sub_command_group',)
    string = P(3, 'string',)
    integer = P(4, 'integer',)
    boolean = P(5, 'boolean',)
    user = P(6, 'user',)
    channel = P(7, 'channel',)
    role = P(8, 'role',)
    mentionable = P(9, 'mentionable',)
    float = P(10, 'float',)
    attachment = P(11, 'attachment',)


class ApplicationCommandPermissionOverwriteTargetType(PreinstancedBase):
    """
    Represents an application command's permission's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command permission overwrite type.
    value : `int`
        The identifier value the application command permission overwrite type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandPermissionOverwriteTargetType``) items
        Stores the predefined ``ApplicationCommandPermissionOverwriteTargetType``-s. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command permission overwrite types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command permission overwrite types.
    
    Every predefined application command permission overwrite type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | Name      | Value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | role                  | role      | 1     |
    +-----------------------+-----------+-------+
    | user                  | user      | 2     |
    +-----------------------+-----------+-------+
    | channel               | channel   | 3     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    role = P(1, 'role',)
    user = P(2, 'user',)
    channel = P(3, 'channel',)


class ApplicationCommandTargetType(PreinstancedBase):
    """
    Represents an application command's target.
    
    Attributes
    ----------
    name : `str`
        The name of the application command target.
    value : `int`
        The identifier value the application command target.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandTargetType``) items
        Stores the predefined ``ApplicationCommandTargetType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command targets' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command targets.
    
    Every predefined application command target can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | chat                  | chat              | 1     |
    +-----------------------+-------------------+-------+
    | user                  | user              | 2     |
    +-----------------------+-------------------+-------+
    | message               | message           | 3     |
    +-----------------------+-------------------+-------+
    | channel               | channel           | 4     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    chat = P(1, 'chat',)
    user = P(2, 'user',)
    message = P(3, 'message',)
    channel = P(4, 'channel')


APPLICATION_COMMAND_CONTEXT_TARGET_TYPES = frozenset((
    ApplicationCommandTargetType.user,
    ApplicationCommandTargetType.message,
    ApplicationCommandTargetType.channel
))
