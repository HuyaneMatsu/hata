__all__ = ('AutoModerationEventType', 'AutoModerationRuleTriggerType')

from ...bases import Preinstance as P, PreinstancedBase

from ..trigger_metadata import (
    AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerMetadataKeywordPreset,
    AutoModerationRuleTriggerMetadataKeyword, AutoModerationRuleTriggerMetadataMentionSpam, 
)


class AutoModerationRuleTriggerType(PreinstancedBase, value_type = int):
    """
    Represents an auto moderation rule's trigger type.
    
    Attributes
    ----------
    max_per_guild : `int`
        The maximal amount of rules of this type per guild.
    
    metadata_type : `type<AutoModerationRuleTriggerMetadataBase>`
        The trigger type's respective metadata type.
    
    name : `str`
        The default name of the auto moderation trigger type.
    
    value : `int`
        The Discord side identifier value of the auto moderation trigger type.
    
    Type Attributes
    ---------------
    Every predefined auto moderation trigger type is also stored as a type attribute:
    
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | Type attribute name   | Name              | Value     | Max per guild | Metadata type                                         |
    +=======================+===================+===========+===============+=======================================================+
    | none                  | none              | 0         | 0             | ``AutoModerationRuleTriggerMetadataBase``             |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | keyword               | keyword           | 1         | 5             | ``AutoModerationRuleTriggerMetadataKeyword``          |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | harmful_link          | harmful link      | 2         | 1             | ``AutoModerationRuleTriggerMetadataBase``             |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | spam                  | spam              | 3         | 1             | ``AutoModerationRuleTriggerMetadataBase``             |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | keyword_preset        | keyword preset    | 4         | 1             | ``AutoModerationRuleTriggerMetadataKeywordPreset``    |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | mention_spam          | mention spam      | 5         | 1             | ``AutoModerationRuleTriggerMetadataMentionSpam``      |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    | user_profile          | user profile      | 6         | 1             | ``AutoModerationRuleTriggerMetadataKeyword``          |
    +-----------------------+-------------------+-----------+---------------+-------------------------------------------------------+
    """
    __slots__ = ('max_per_guild', 'metadata_type')
    
    def __new__(cls, value, name = None, max_per_guild = 1, metadata_type = None):
        """
        Creates an auto moderation rule trigger type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the auto moderation trigger type.
        
        name : `None | str` = `None`, Optional
            The default name of the auto moderation trigger type.
        
        max_per_guild : `int` = `1`, Optional
            The native name of the auto moderation trigger type.
        
        metadata_type : `None | type<AutoModerationRuleTriggerMetadataBase>` = `None`, Optional
            The trigger type's respective metadata type.
        """
        if metadata_type is None:
            metadata_type = AutoModerationRuleTriggerMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.max_per_guild = max_per_guild
        self.metadata_type = metadata_type
        return self
    
    
    # predefined
    none = P(0, 'none', 0, AutoModerationRuleTriggerMetadataBase)
    keyword = P(1, 'keyword', 5, AutoModerationRuleTriggerMetadataKeyword)
    harmful_link = P(2, 'harmful link', 1, AutoModerationRuleTriggerMetadataBase)
    spam = P(3, 'spam', 1, AutoModerationRuleTriggerMetadataBase)
    keyword_preset = P(4, 'keyword preset', 1, AutoModerationRuleTriggerMetadataKeywordPreset)
    mention_spam = P(5, 'mention spam', 1, AutoModerationRuleTriggerMetadataMentionSpam)
    user_profile = P(6, 'user profile', 1, AutoModerationRuleTriggerMetadataKeyword)


class AutoModerationEventType(PreinstancedBase, value_type = int):
    """
    Represents an auto moderation rule's event type.
    
    Attributes
    ----------
    name : `str`
        The default name of the auto moderation event type.
    
    value : `int`
        The Discord side identifier value of the auto moderation event type.
    
    Type Attributes
    ---------------
    Every predefined auto moderation event type is also stored as a type attribute:
    
    +-----------------------+-------------------+-----------+
    | Type attribute name   | Name              | Value     |
    +=======================+===================+===========+
    | none                  | none              | 0         |
    +-----------------------+-------------------+-----------+
    | message_send          | message send      | 1         |
    +-----------------------+-------------------+-----------+
    | user_update           | user update       | 2         |
    +-----------------------+-------------------+-----------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    message_send = P(1, 'message send')
    user_update = P(2, 'user update')
