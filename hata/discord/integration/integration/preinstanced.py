__all__ = ('IntegrationType', )

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..integration_metadata import IntegrationMetadataBase, IntegrationMetadataSubscription, IntegrationMetadataDiscord


@export
class IntegrationType(PreinstancedBase, value_type = str):
    """
    Represents an ``Integration``'s type.
    
    Attributes
    ----------
    metadata_type : `type<IntegrationMetadataBase>`
        The integration's metadata's type.
        
    name : `str`
        The name of the integration type.
    
    value : `str`
        The Discord side identifier value of the integration type.
    
    Type Attributes
    ---------------
    Every predefined integration type can be accessed as type attribute as well:
    
    +-----------------------+-----------------------+---------------------------+---------------------------------------+
    | Type attribute name   | Name                  | Value                     | Metadata type                         |
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
    __slots__ = ('metadata_type',)
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates a new integration type.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the scheduled event entity type.
        
        name : `None | str` = `None`, Optional
            The name of the scheduled event entity type.
        
        metadata_type : `None | type<IntegrationMetadataBase>` = `None`, Optional
            The integration's metadata's type.
        """
        if metadata_type is None:
            metadata_type = IntegrationMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    # predefined
    none = P('', 'none', IntegrationMetadataBase)
    discord = P('discord', 'Discord', IntegrationMetadataDiscord)
    twitch = P('twitch', 'twitch', IntegrationMetadataSubscription)
    youtube = P('youtube', 'Youtube', IntegrationMetadataSubscription)
    guild_subscription = P('guild_subscription', 'guild subscription', IntegrationMetadataSubscription)
