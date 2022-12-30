__all__ = ('ActivityType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..activity_metadata import ActivityMetadataBase, ActivityMetadataCustom, ActivityMetadataRich


class ActivityType(PreinstancedBase):
    """
    Represents an ``AutoModerationAction``'s type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the activity type.
    name : `str`
        The default name of the activity type.
    metadata_type : `type<ActivityMetadataBase>`
        The activity type's respective metadata type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``ActivityType``) items
        Stores the predefined activity types. This container is accessed when translating a Discord side
        identifier of a activity type. The identifier value is used as a key to get it's wrapper side
        representation.
    VALUE_TYPE : `type` = `str`
        The activity types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the activity types.
    
    Every predefined activity type is also stored as a class attribute:
    
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | Class attribute name  | Name                  | Value     | Metadata type                         |
    +=======================+=======================+===========+=======================================+
    | unknown               | unknown               | -1        | ``ActivityMetadataBase``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | game                  | game                  | 0         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | stream                | block stream          | 1         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | spotify               | spotify               | 2         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | watching              | watching              | 3         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | custom                | custom                | 4         | ``ActivityMetadataCustom``            |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | competing             | competing             | 5         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    """
    __slots__ = ('metadata_type',)
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new activity type with the given value.
        
        Parameters
        ----------
        value : `int`
            The activity type's identifier value.
        
        Returns
        -------
        self : ``ActivityType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.metadata_type = ActivityMetadataRich
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates an ``ActivityType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the activity type.
        name : `str`
            The default name of the activity type.
        metadata_type : `None`, `type<ActivityMetadataBase>`
            The activity type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    # predefined
    unknown = P(-1, 'unknown', ActivityMetadataBase)
    game = P(0, 'game', ActivityMetadataRich)
    stream = P(1, 'stream message', ActivityMetadataRich)
    spotify = P(2, 'spotify', ActivityMetadataRich)
    watching = P(3, 'watching', ActivityMetadataRich)
    custom = P(4, 'custom', ActivityMetadataCustom)
    competing = P(5, 'competing', ActivityMetadataRich)
