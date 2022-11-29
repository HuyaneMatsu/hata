__all__ = ('AutoModerationEventType', 'AutoModerationRuleTriggerType')

from ...bases import Preinstance as P, PreinstancedBase

from ..trigger_metadata import (
    AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerMetadataKeywordPreset,
    AutoModerationRuleTriggerMetadataKeyword, AutoModerationRuleTriggerMetadataMentionSpam, 
)


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
    metadata_type : `AutoModerationRuleTriggerMetadataBase``
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
    
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | Class attribute name  | Name              | Value     | Max per guild | Metadata type                                       |
    +=======================+===================+===========+===============+=====================================================+
    | none                  | none              | 0         | 0             | ``AutoModerationRuleTriggerMetadataBase``           |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | keyword               | keyword           | 1         | 5             | ``AutoModerationRuleTriggerMetadataKeyword``        |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | harmful_link          | harmful link      | 2         | 1             | ``AutoModerationRuleTriggerMetadataBase``           |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | spam                  | spam              | 3         | 1             | ``AutoModerationRuleTriggerMetadataBase``           |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | keyword_preset        | keyword preset    | 4         | 1             | ``AutoModerationRuleTriggerMetadataKeywordPreset``  |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
    | mention_spam          | mention spam      | 5         | 1             | ``AutoModerationRuleTriggerMetadataMentionSpam``    |
    +-----------------------+-------------------+-----------+---------------+-----------------------------------------------------+
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
        self.metadata_type = AutoModerationRuleTriggerMetadataBase
        
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
        metadata_type : `None`, ``AutoModerationRuleTriggerMetadataBase``
            The trigger type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.max_per_guild = max_per_guild
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', 0, AutoModerationRuleTriggerMetadataBase)
    keyword = P(1, 'keyword', 5, AutoModerationRuleTriggerMetadataKeyword)
    harmful_link = P(2, 'harmful link', 1, AutoModerationRuleTriggerMetadataBase)
    spam = P(3, 'spam', 1, AutoModerationRuleTriggerMetadataBase)
    keyword_preset = P(4, 'keyword preset', 1, AutoModerationRuleTriggerMetadataKeywordPreset)
    mention_spam = P(5, 'mention spam', 1, AutoModerationRuleTriggerMetadataMentionSpam)


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
