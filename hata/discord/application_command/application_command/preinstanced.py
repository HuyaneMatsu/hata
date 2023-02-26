__all__ = ('ApplicationCommandTargetType', 'APPLICATION_COMMAND_CONTEXT_TARGET_TYPES')

from ...bases import Preinstance as P, PreinstancedBase


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
