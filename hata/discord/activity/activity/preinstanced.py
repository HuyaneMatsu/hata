__all__ = ('ActivityType',)

from scarletio import class_property

from ...bases import Preinstance as P, PreinstancedBase

from ..activity_metadata import (
    ActivityMetadataBase, ActivityMetadataCustom, ActivityMetadataHanging, ActivityMetadataRich
)


class ActivityType(PreinstancedBase):
    """
    Represents an ``Activity``'s type.
    
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
    | playing               | playing               | 0         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | stream                | stream                | 1         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | spotify               | spotify               | 2         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | watching              | watching              | 3         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | custom                | custom                | 4         | ``ActivityMetadataCustom``            |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | competing             | competing             | 5         | ``ActivityMetadataRich``              |
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | hanging               | hanging               | 6         | ``ActivityMetadataHanging``           |
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
        self : `instance<cls>`
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.metadata_type = ActivityMetadataRich
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates an activity type and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the activity type.
        name : `str`
            The name of the activity type.
        metadata_type : `None`, `type<ActivityMetadataBase>`
            The activity type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    
    # predefined
    unknown = P(-1, 'unknown', ActivityMetadataBase)
    playing = P(0, 'playing', ActivityMetadataRich)
    stream = P(1, 'stream message', ActivityMetadataRich)
    spotify = P(2, 'spotify', ActivityMetadataRich)
    watching = P(3, 'watching', ActivityMetadataRich)
    custom = P(4, 'custom', ActivityMetadataCustom)
    competing = P(5, 'competing', ActivityMetadataRich)
    hanging = P(6, 'hanging', ActivityMetadataHanging)
    
    
    # Leave a date comment here, so we find it when looking for expired deprecations
    # 2024 january
    
    @class_property
    def game(self):
        """
        Please use `.playing instead. Will be deprecated in the future.
        """
        return self.playing
