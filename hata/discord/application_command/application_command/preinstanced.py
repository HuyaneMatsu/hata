__all__ = (
    'CONTEXT_TARGET_TYPES', 'INTEGRATION_CONTEXT_TYPES_ALL', 'ApplicationCommandHandlerType',
    'ApplicationCommandIntegrationContextType', 'ApplicationCommandTargetType',
)

from warnings import warn

from scarletio import class_property

from ...bases import Preinstance as P, PreinstancedBase


class ApplicationCommandHandlerType(PreinstancedBase):
    """
    Represents what handles an application command.
    
    Attributes
    ----------
    name : `str`
        The name of the handler.
    value : `int`
        The identifier value representing the handler.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandHandlerType``) items
        Stores the predefined ``ApplicationCommandHandlerType``-s. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The handlers' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command integration contexts.
    
    Every predefined application command handler type can be accessed as class attribute as well:
    
    +---------------------------------------+---------------------------------------+-------+
    | Class attribute name                  | Name                                  | Value |
    +=======================================+=======================================+=======+
    | guild                                 | guild                                 | 0     |
    +---------------------------------------+---------------------------------------+-------+
    | application                           | application                           | 1     |
    +---------------------------------------+---------------------------------------+-------+
    | discord_embedded_activity_launcher    | discord embedded activity launcher    | 2     |
    +---------------------------------------+---------------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    application = P(1, 'application')
    discord_embedded_activity_launcher = P(2, 'discord embedded activity launcher')


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
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | Name                      | Value |
    +============================+==========================+======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | chat                      | chat                      | 1     |
    +---------------------------+---------------------------+-------+
    | user                      | user                      | 2     |
    +---------------------------+---------------------------+-------+
    | message                   | message                   | 3     |
    +---------------------------+---------------------------+-------+
    | embedded_activity_launch  | embedded activity launch  | 4     |
    +---------------------------+---------------------------+-------+
    | channel                   | channel                   | 1004  |
    +---------------------------+---------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    chat = P(1, 'chat',)
    user = P(2, 'user',)
    message = P(3, 'message',)
    embedded_activity_launch = P(4, 'embedded activity launch')
    channel = P(1004, 'channel')
    
    @class_property
    def activity_start(cls):
        """
        Deprecated and will be removed in 2025 Jun. Use `.embedded_activity_launch` instead.
        """
        warn(
            (
                f'`{cls.__name__}.activity_start` is deprecated and will be removed in 2025 Jun. '
                f'Use `.embedded_activity_launch` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        return cls.embedded_activity_launch


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
