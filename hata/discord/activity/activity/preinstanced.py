__all__ = ('ActivityType',)

from warnings import warn

from scarletio import class_property

from ...bases import Preinstance as P, PreinstancedBase

from ..activity_metadata import (
    ActivityMetadataBase, ActivityMetadataCustom, ActivityMetadataHanging, ActivityMetadataRich
)


class ActivityType(PreinstancedBase, value_type = int):
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
    
    Type Attributes
    ----------------
    Every predefined activity type is also stored as a type attribute:
    
    +-----------------------+-----------------------+-----------+---------------------------------------+
    | Type attribute name   | Name                  | Value     | Metadata type                         |
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
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates an new activity type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the activity type.
        
        name : `None | str` = `None`, Optional
            The name of the activity type.
        
        metadata_type : `None | type<ActivityMetadataBase>` = `None`, Optional
            The activity type's respective metadata type.
        """
        if metadata_type is None:
            metadata_type = ActivityMetadataRich
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    # predefined
    unknown = P(-1, 'unknown', ActivityMetadataBase)
    playing = P(0, 'playing', ActivityMetadataRich)
    stream = P(1, 'stream message', ActivityMetadataRich)
    spotify = P(2, 'spotify', ActivityMetadataRich)
    watching = P(3, 'watching', ActivityMetadataRich)
    custom = P(4, 'custom', ActivityMetadataCustom)
    competing = P(5, 'competing', ActivityMetadataRich)
    hanging = P(6, 'hanging', ActivityMetadataHanging)
    
    
    @class_property
    def game(cls):
        """
        Deprecated and will be removed n 2025 September.
        Please use `.playing` instead.
        """
        warn(
            (
                f'`{cls.__name__}.game` is deprecated and will be removed in 2025 September. '
                f'Please use `.playing` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        
        return cls.playing
