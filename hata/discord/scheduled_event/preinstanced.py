__all__ = ('PrivacyLevel', 'ScheduledEventEntityType', 'ScheduledEventStatus',)

from ..bases import PreinstancedBase, Preinstance as P

from .metadata import StageEntityMetadata

class ScheduledEventStatus(PreinstancedBase):
    """
    Represents a scheduled event's status.
    
    Attributes
    ----------
    name : `str`
        The name of the scheduled event status.
    value : `int`
        The identifier value the scheduled event status.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ScheduledEventStatus``) items
        Stores the predefined ``ScheduledEventStatus`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The scheduled event status' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the scheduled event statuses.
    
    Every predefined scheduled event can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    scheduled = P(1, 'scheduled')
    active = P(2, 'active')
    completed = P(3, 'completed')
    cancelled = P(4, 'cancelled')


class ScheduledEventEntityType(PreinstancedBase):
    """
    Represents a scheduled event's entity's type.
    
    Attributes
    ----------
    name : `str`
        The name of the scheduled event's entity's type.
    value : `int`
        The identifier value the scheduled event's entity type.
    metadata_type : `None` or ``ScheduledEventEntityMetadata`` subclass
        The scheduled event's metadata's applicable type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ScheduledEventEntityType``) items
        Stores the predefined ``ScheduledEventEntityType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The scheduled event's entity's type's values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the scheduled event entity types.
    
    Every predefined scheduled event can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+---------------------------+
    | Class attribute name  | Name          | Value | Metadata type             |
    +=======================+===============+=======+===========================+
    | none                  | none          | 0     | None                      |
    +-----------------------+---------------+-------+---------------------------+
    | stage                 | stage         | 1     | ``StageEntityMetadata``   |
    +-----------------------+---------------+-------+---------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('metadata_type',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a scheduled event entity type from the given id and stores it at class's `.INSTANCES`.
        
        Called by `.get` when no scheduled event entity type was found with the given id.
        
        Parameters
        ----------
        id_ : `str`
            The identifier of the scheduled event entity type.
        
        Returns
        -------
        self : ``ScheduledEventEntityType``
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.metadata_type = None
        
        self.INSTANCES[value] = self
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
        metadata_type : `None` or ``ScheduledEventEntityMetadata`` subclass
            The scheduled event's metadata's applicable type.
        """
        self.name = name
        self.value = value
        self.metadata_type = metadata_type
        self.INSTANCES[value] = self
    
    
    none = P(0, 'none', None)
    stage = P(1, 'stage', StageEntityMetadata)


class PrivacyLevel(PreinstancedBase):
    """
    Represents a stage channel's privacy level.
    
    Attributes
    ----------
    name : `str`
        The name of the privacy level.
    value : `int`
        The identifier value the privacy level.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``PrivacyLevel``) items
        Stores the predefined ``PrivacyLevel`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The privacy level' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the privacy levels.
    
    Every predefined privacy level can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | public                | public        | 1     |
    +-----------------------+---------------+-------+
    | guild_only            | guild_only    | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    public = P(1, 'public')
    guild_only = P(2, 'guild_only')
