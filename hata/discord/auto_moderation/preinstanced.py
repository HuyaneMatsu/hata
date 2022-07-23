__all__ = (
    'AutoModerationActionType', 'AutoModerationEventType', 'AutoModerationKeywordPresetType',
    'AutoModerationRuleTriggerType'
)

from scarletio import export

from ..bases import Preinstance as P, PreinstancedBase

from .action_metadata import SendAlertMessageActionMetadata, TimeoutActionMetadata
from .trigger_metadata import KeywordPresetTriggerMetadata, KeywordTriggerMetadata, MentionSpamTriggerMetadata



class AutoModerationActionType(PreinstancedBase):
    """
    Represents an ``AutoModerationAction``'s type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation action type.
    name : `str`
        The default name of the auto moderation action type.
    metadata_type : `None`, ``AutoModerationActionMetadata``
        The action type's respective metadata type.
    
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationActionType``) items
        Stores the predefined auto moderation action types. This container is accessed when translating a Discord side
        identifier of a auto moderation action type. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation action types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation action types.
    
    Every predefined auto moderation action type is also stored as a class attribute:
    
    +-----------------------+-----------------------+-----------+---------------------------------------+-----------------------------------------------------------------------+
    | Class attribute name  | Name                  | Value     | Metadata type                         | Description                                                           |
    +=======================+=======================+===========+=======================================+=======================================================================+
    | none                  | none                  | 0         | `None`                                | N/A                                                                   |
    +-----------------------+-----------------------+-----------+---------------------------------------+-----------------------------------------------------------------------+
    | block_message         | block message         | 1         | `None`                                | Blocks the message's content according to the rule.                   |
    +-----------------------+-----------------------+-----------+---------------------------------------+-----------------------------------------------------------------------+
    | send_alert_message    | send alert message    | 2         | ``SendAlertMessageActionMetadata``    | Sends an alert message to the specified channel.                      |
    +-----------------------+-----------------------+-----------+---------------------------------------+-----------------------------------------------------------------------+
    | timeout               | timeout               | 3         | ``TimeoutActionMetadata``             | Timeouts the user. Only applicable for `keyword` rules. Max 4 weeks.  |
    +-----------------------+-----------------------+-----------+---------------------------------------+-----------------------------------------------------------------------+
    """
    __slots__ = ('metadata_type',)
    
    INSTANCES = {}
    VALUE_TYPE = int

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new auto moderation action type with the given value.
        
        Parameters
        ----------
        value : `int`
            The auto moderation action type's identifier value.
        
        Returns
        -------
        self : ``AutoModerationActionType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.metadata_type = None
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates an ``AutoModerationActionType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the auto moderation action type.
        name : `str`
            The default name of the auto moderation action type.
        max_per_guild : `int`
            The native name of the auto moderation action type.
        metadata_type : `None`, ``AutoModerationRuleTriggerMetadata``
            The action type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', None)
    block_message = P(1, 'block message', None)
    send_alert_message = P(2, 'send alert message', SendAlertMessageActionMetadata)
    timeout = P(3, 'timeout', TimeoutActionMetadata)


class AutoModerationRuleTriggerType(PreinstancedBase):
    """
    Represents an auto moderation rule's trigger type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation trigger type.
    name : `str`
        The default name of the auto moderation trigger type.
    max_per_guild : `int`
        The maximal amount of rules of this type per guild.
    metadata_type : `None`, ``AutoModerationRuleTriggerMetadata``
        The trigger type's respective metadata type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationRuleTriggerType``) items
        Stores the predefined auto moderation trigger types. This container is accessed when translating a Discord side
        identifier of a auto moderation trigger type. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation trigger types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation trigger types.
    
    Every predefined auto moderation trigger type is also stored as a class attribute:
    
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | Class attribute name  | Name              | Value     | Max per guild | Metadata type                     |
    +=======================+===================+===========+===============+===================================+
    | none                  | none              | 0         | 0             | `None`                            |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | keyword               | keyword           | 1         | 3             | ``KeywordTriggerMetadata``        |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | harmful_link          | harmful link      | 2         | 1             | `None`                            |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | spam                  | spam              | 3         | 1             | `None`                            |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | keyword_preset        | keyword preset    | 4         | 1             | ``KeywordPresetTriggerMetadata``  |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    | mention_spam          | mention spam      | 5         | 1             | ``MentionSpamTriggerMetadata``    |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------+
    """
    __slots__ = ('max_per_guild', 'metadata_type')
    
    INSTANCES = {}
    VALUE_TYPE = int

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new auto moderation trigger type with the given value.
        
        Parameters
        ----------
        value : `int`
            The auto moderation trigger type's identifier value.
        
        Returns
        -------
        self : ``AutoModerationRuleTriggerType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.max_per_guild = 1
        self.metadata_type = None
        
        return self
    
    
    def __init__(self, value, name, max_per_guild, metadata_type):
        """
        Creates an ``AutoModerationRuleTriggerType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the auto moderation trigger type.
        name : `str`
            The default name of the auto moderation trigger type.
        max_per_guild : `int`
            The native name of the auto moderation trigger type.
        metadata_type : `None`, ``AutoModerationRuleTriggerMetadata``
            The trigger type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.max_per_guild = max_per_guild
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', 0, None)
    keyword = P(1, 'keyword', 3, KeywordTriggerMetadata)
    harmful_link = P(2, 'harmful link', 1, None)
    spam = P(3, 'spam', 1, None)
    keyword_preset = P(4, 'keyword preset', 1, KeywordPresetTriggerMetadata)
    mention_spam = P(5, 'mention spam', 1, MentionSpamTriggerMetadata)


class AutoModerationEventType(PreinstancedBase):
    """
    Represents an auto moderation rule's event type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation event type.
    name : `str`
        The default name of the auto moderation event type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationEventType``) items
        Stores the predefined auto moderation event types. This container is accessed when translating a Discord side
        identifier of a auto moderation event type. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation event types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation event types.
    
    Every predefined auto moderation event type is also stored as a class attribute:
    
    +-----------------------+-------------------+-----------+
    | Class attribute name  | Name              | Value     |
    +=======================+===================+===========+
    | none                  | none              | 0         |
    +-----------------------+-------------------+-----------+
    | message_send          | message send      | 1         |
    +-----------------------+-------------------+-----------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    # predefined
    none = P(0, 'none')
    message_send = P(1, 'message send')


@export
class AutoModerationKeywordPresetType(PreinstancedBase):
    """
    Represents an auto moderation keyword preset type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation keyword preset type.
    name : `str`
        The default name of the auto moderation keyword preset type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationKeywordPresetType``) items
        Stores the predefined auto moderation keyword preset types. This container is accessed when translating a
        Discord side identifier of a auto moderation keyword preset type. The identifier value is used as a key to
        get it's wrapper side representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation keyword preset types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation keyword preset types.
    
    Every predefined auto moderation keyword preset type is also stored as a class attribute:
    
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | Class attribute name  | Name                  | Value     | Description                               |
    +=======================+=======================+===========+===========================================+
    | none                  | none                  | 0         | N/A                                       |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | cursing               | cursing               | 1         | Swearing or cursing.                      |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | sexually_suggestive   | sexually suggestive   | 2         | Sexually explicit behavior or activity.   |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | slur                  | slur                  | 3         | Personal insult or hate speech.           |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    # predefined
    none = P(0, 'none')
    cursing = P(1, 'cursing')
    sexually_suggestive = P(2, 'sexually suggestive')
    slur = P(3, 'slur')
