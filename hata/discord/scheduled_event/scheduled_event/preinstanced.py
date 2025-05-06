__all__ = ('PrivacyLevel', 'ScheduledEventEntityType', 'ScheduledEventStatus',)

from ...bases import Preinstance as P, PreinstancedBase

from ..scheduled_event_entity_metadata import (
    ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation, ScheduledEventEntityMetadataStage
)


class ScheduledEventStatus(PreinstancedBase, value_type = int):
    """
    Represents a scheduled event's status.
    
    Attributes
    ----------
    name : `str`
        The name of the scheduled event status.
    
    value : `int`
        The identifier value the scheduled event status.
    
    Type Attributes
    ---------------
    Every predefined scheduled event can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | scheduled             | scheduled     | 1     |
    +-----------------------+---------------+-------+
    | active                | active        | 2     |
    +-----------------------+---------------+-------+
    | completed             | completed     | 3     |
    +-----------------------+---------------+-------+
    | cancelled             | cancelled     | 4     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    scheduled = P(1, 'scheduled')
    active = P(2, 'active')
    completed = P(3, 'completed')
    cancelled = P(4, 'cancelled')


class ScheduledEventEntityType(PreinstancedBase, value_type = int):
    """
    Represents a scheduled event's entity's type.
    
    Attributes
    ----------
    name : `str`
        The name of the scheduled event's entity's type.
    
    metadata_type : `type<ScheduledEventEntityMetadata>`
        The scheduled event's metadata's applicable type.
    
    value : `int`
        The identifier value the scheduled event's entity type.
    
    Type Attributes
    ---------------
    Every predefined scheduled event can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+---------------------------------------------+
    | Type attribute name   | Name          | Value | Metadata type                               |
    +=======================+===============+=======+=============================================+
    | none                  | none          | 0     | ``ScheduledEventEntityMetadataBase``        |
    +-----------------------+---------------+-------+---------------------------------------------+
    | stage                 | stage         | 1     | ``ScheduledEventEntityMetadataStage``       |
    +-----------------------+---------------+-------+---------------------------------------------+
    | voice                 | voice         | 2     | ``ScheduledEventEntityMetadataBase``        |
    +-----------------------+---------------+-------+---------------------------------------------+
    | location              | location      | 3     | ``ScheduledEventEntityMetadataLocation``    |
    +-----------------------+---------------+-------+---------------------------------------------+
    """
    __slots__ = ('metadata_type',)
    
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates a new scheduled event entity type instance from the given parameters.
        
        Parameters
        ----------
        value : `int`
            The unique identifier of the scheduled event entity type.
        
        name : `None | str` = `None`, Optional
            The name of the scheduled event entity type.
        
        metadata_type : `None | type<ScheduledEventEntityMetadata>` = `None`, Optional
            The scheduled event's metadata's applicable type.
        """
        if metadata_type is None:
            metadata_type = ScheduledEventEntityMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    none = P(0, 'none', ScheduledEventEntityMetadataBase)
    stage = P(1, 'stage', ScheduledEventEntityMetadataStage)
    voice = P(2, 'voice', ScheduledEventEntityMetadataBase)
    location = P(3, 'location', ScheduledEventEntityMetadataLocation)


class PrivacyLevel(PreinstancedBase, value_type = int):
    """
    Represents a stage channel's privacy level.
    
    Attributes
    ----------
    name : `str`
        The name of the privacy level.
    
    value : `int`
        The identifier value the privacy level.
    
    Type Attributes
    ---------------
    Every predefined privacy level can be accessed as type attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Type attribute name       | Name                      | Value |
    +===========================+===========================+=======+
    | none                      | none                      | 0     |
    +---------------------------+---------------------------+-------+
    | public                    | public                    | 1     |
    +---------------------------+---------------------------+-------+
    | guild_only                | guild only                | 2     |
    +---------------------------+---------------------------+-------+
    | public_with_join_request  | public with join request  | 3     |
    +---------------------------+---------------------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    public = P(1, 'public')
    guild_only = P(2, 'guild only')
    public_with_join_request = P(3, 'public with join request')
