__all__ = (
    'CONTEXT_TARGET_TYPES', 'INTEGRATION_CONTEXT_TYPES_ALL',
    'ApplicationCommandIntegrationContextType', 'ApplicationCommandTargetType',
)

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
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | chat                  | chat                  | 1     |
    +-----------------------+-----------------------+-------+
    | user                  | user                  | 2     |
    +-----------------------+-----------------------+-------+
    | message               | message               | 3     |
    +-----------------------+-----------------------+-------+
    | application_activity  | application_activity  | 4     |
    +-----------------------+-----------------------+-------+
    | channel               | channel               | 1004  |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    chat = P(1, 'chat',)
    user = P(2, 'user',)
    message = P(3, 'message',)
    activity_start = P(4, 'activity_start')
    channel = P(1004, 'channel')


CONTEXT_TARGET_TYPES = frozenset((
    ApplicationCommandTargetType.user,
    ApplicationCommandTargetType.message,
    ApplicationCommandTargetType.channel,
))


class ApplicationCommandIntegrationContextType(PreinstancedBase):
    """
    Represents an application command's integration's context's type or in other words, where it can be used.
    
    Attributes
    ----------
    name : `str`
        The name of the application command integration context.
    value : `int`
        The identifier value the application command integration context.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandIntegrationContextType``) items
        Stores the predefined ``ApplicationCommandIntegrationContextType``-s. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command integration contexts' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command integration contexts.
    
    Every predefined application command integration context can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | guild                 | guild             | 0     |
    +-----------------------+-------------------+-------+
    | bot_private_channel   | chat              | 1     |
    +-----------------------+-------------------+-------+
    | any_private_channel   | user              | 2     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    guild = P(0, 'guild')
    bot_private_channel = P(1, 'bot private channel')
    any_private_channel = P(2, 'any private channel')


INTEGRATION_CONTEXT_TYPES_ALL = tuple(sorted(
    ApplicationCommandIntegrationContextType.INSTANCES.values()
))
