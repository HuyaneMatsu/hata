__all__ = ('IntegrationType', )

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..integration_metadata import IntegrationMetadataBase, IntegrationMetadataSubscription, IntegrationMetadataDiscord


@export
class IntegrationType(PreinstancedBase):
    """
    Represents an ``Integration``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the integration type.
    value : `int`
        The Discord side identifier value of the integration type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``IntegrationType``) items
        Stores the predefined ``IntegrationType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The integration type' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the integration types.
    
    Every predefined integration type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | Class attribute name  | Name                  | Value                     | Metadata type                         |
    +=======================+=======================+===========================+=======================================+
    | none                  | none                  | `''`                      | ``IntegrationMetadataBase``           |
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | discord               | Discord               | `'discord'`               | ``IntegrationMetadataDiscord``        |
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | twitch                | Twitch                | `'twitch'`                | ``IntegrationMetadataSubscription``   |
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | youtube               | Youtube               | `'youtube'`               | ``IntegrationMetadataSubscription``   |
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | guild_subscription    | guild subscription    | `'guild_subscription'`    | ``IntegrationMetadataSubscription``   |
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    
    """
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ('metadata_type',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new integration type with the given value.
        
        Parameters
        ----------
        value : `str`
            The integration's type.
        
        Returns
        -------
        self : ``IntegrationType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = value
        self.value = value
        self.metadata_type = IntegrationMetadataSubscription
        return self
    

    
    def __init__(self, value, name, metadata_type):
        """
        Creates a new scheduled event entity type instance from the given parameters.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the scheduled event entity type.
        name : `str`
            The name of the scheduled event entity type.
        metadata_type : `None`, ``IntegrationMetadataBase`` subclass
            The integration's metadata's type.
        """
        self.name = name
        self.value = value
        self.metadata_type = metadata_type
        self.INSTANCES[value] = self
    
    
    # predefined
    none = P('', 'none', IntegrationMetadataBase)
    discord = P('discord', 'Discord', IntegrationMetadataDiscord)
    twitch = P('twitch', 'twitch', IntegrationMetadataSubscription)
    youtube = P('youtube', 'Youtube', IntegrationMetadataSubscription)
    guild_subscription = P('guild_subscription', 'guild subscription', IntegrationMetadataSubscription)
