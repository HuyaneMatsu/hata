__all__ = ('AutoModerationActionType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..action_metadata import (
    AutoModerationActionMetadataBase, AutoModerationActionMetadataSendAlertMessage, AutoModerationActionMetadataTimeout
)


class AutoModerationActionType(PreinstancedBase):
    """
    Represents an ``AutoModerationAction``'s type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation action type.
    name : `str`
        The default name of the auto moderation action type.
    metadata_type : ``AutoModerationActionMetadataBase``
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
    
    +-----------------------+-----------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | Class attribute name  | Name                  | Value     | Metadata type                                     | Description                                                           |
    +=======================+=======================+===========+===================================================+=======================================================================+
    | none                  | none                  | 0         | ``AutoModerationActionMetadataBase``              | N/A                                                                   |
    +-----------------------+-----------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | block_message         | block message         | 1         | ``AutoModerationActionMetadataBase``              | Blocks the message's content according to the rule.                   |
    +-----------------------+-----------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | send_alert_message    | send alert message    | 2         | ``AutoModerationActionMetadataSendAlertMessage``  | Sends an alert message to the specified channel.                      |
    +-----------------------+-----------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
    | timeout               | timeout               | 3         | ``AutoModerationActionMetadataTimeout``           | Timeouts the user. Only applicable for `keyword` rules. Max 4 weeks.  |
    +-----------------------+-----------------------+-----------+---------------------------------------------------+-----------------------------------------------------------------------+
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
        self.metadata_type = AutoModerationActionMetadataBase
        
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
        metadata_type : ``AutoModerationRuleTriggerMetadataBase``
            The action type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', AutoModerationActionMetadataBase)
    block_message = P(1, 'block message', AutoModerationActionMetadataBase)
    send_alert_message = P(2, 'send alert message', AutoModerationActionMetadataSendAlertMessage)
    timeout = P(3, 'timeout', AutoModerationActionMetadataTimeout)
