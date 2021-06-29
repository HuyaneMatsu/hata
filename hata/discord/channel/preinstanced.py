__all__ = ('VideoQualityMode', )

from ..bases import PreinstancedBase, Preinstance as P

class VideoQualityMode(PreinstancedBase):
    """
    Represents a voice channel's video quality mode.
    
    Attributes
    ----------
    name : `str`
        The name of the video quality mode.
    value : `int`
        The identifier value the video quality mode.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VideoQualityMode``) items
        Stores the predefined ``VideoQualityMode`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The video quality modes' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the video quality modes.
    
    Every predefined video quality mode can be accessed as class attribute as well:
    
    +-----------------------+-------+-------+-------------------------------------------------------+
    | Class attribute name  | Name  | Value | Description                                           |
    +=======================+=======+=======+=======================================================+
    | none                  | none  | 0     | N/A                                                   |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | auto                  | auto  | 1     | Discord chooses the quality for optimal performance.  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    | full                  | full  | 2     | 720p                                                  |
    +-----------------------+-------+-------+-------------------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    auto = P(1, 'auto')
    full = P(2, 'full')
