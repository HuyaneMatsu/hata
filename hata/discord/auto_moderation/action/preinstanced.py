__all__ = ('AutoModerationActionType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..action_metadata import (
    AutoModerationActionMetadataBase, AutoModerationActionMetadataBlock, AutoModerationActionMetadataSendAlertMessage,
    AutoModerationActionMetadataTimeout
)


class AutoModerationActionType(PreinstancedBase, value_type = int):
    """
    Represents an ``AutoModerationAction``'s type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation action type.
    
    name : `str`
        The default name of the auto moderation action type.
    
    metadata_type : `type<<AutoModerationActionMetadataBase>`
        The action type's respective metadata type.
    
    Type Attributes
    ---------------
    Every predefined auto moderation action type is also stored as a type attribute:
    
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | Type attribute name       | Name                      | Value     | Metadata type                                     | Description                                                           |
    +===========================+===========================+===========+===================================================+=======================================================================+
    | none                      | none                      | 0         | ``AutoModerationActionMetadataBase``              | N/A                                                                   |
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | block_message             | block message             | 1         | ``AutoModerationActionMetadataBlock``             | Blocks the message's content according to the rule.                   |
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | send_alert_message        | send alert message        | 2         | ``AutoModerationActionMetadataSendAlertMessage``  | Sends an alert message to the specified channel.                      |
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | timeout                   | timeout                   | 3         | ``AutoModerationActionMetadataTimeout``           | Timeouts the user. Only applicable for `keyword` rules. Max 4 weeks.  |
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | block_user_interaction    | block user interaction    | 4         | ``AutoModerationActionMetadataBase``              | Blocks the user from using text, voice and interactions.              |
    +---------------------------+---------------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    """
    __slots__ = ('metadata_type',)
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates an auto moderation action type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the auto moderation action type.
        
        name : `None | str` = `None`, Optional
            The default name of the auto moderation action type.
        
        metadata_type : `None | type<AutoModerationActionMetadataBase>` = `None`, Optional
            The action type's respective metadata type.
        """
        if metadata_type is None:
            metadata_type = AutoModerationActionMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    # predefined
    none = P(0, 'none', AutoModerationActionMetadataBase)
    block_message = P(1, 'block message', AutoModerationActionMetadataBlock)
    send_alert_message = P(2, 'send alert message', AutoModerationActionMetadataSendAlertMessage)
    timeout = P(3, 'timeout', AutoModerationActionMetadataTimeout)
    block_user_interaction = P(4, 'block user interaction', AutoModerationActionMetadataBase)
