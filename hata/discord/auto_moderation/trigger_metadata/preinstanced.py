__all__ = ('AutoModerationKeywordPresetType', )

from ...bases import Preinstance as P, PreinstancedBase


class AutoModerationKeywordPresetType(PreinstancedBase):
    """
    Represents an auto moderation keyword preset type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the auto moderation keyword preset type.
    name : `str`
        The default name of the auto moderation keyword preset type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``AutoModerationKeywordPresetType``) items
        Stores the predefined auto moderation keyword preset types. This container is accessed when translating a
        Discord side identifier of a auto moderation keyword preset type. The identifier value is used as a key to
        get it's wrapper side representation.
    VALUE_TYPE : `type` = `str`
        The auto moderation keyword preset types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the auto moderation keyword preset types.
    
    Every predefined auto moderation keyword preset type is also stored as a class attribute:
    
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | Class attribute name  | Name                  | Value     | Description                               |
    +=======================+=======================+===========+===========================================+
    | none                  | none                  | 0         | N/A                                       |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | cursing               | cursing               | 1         | Swearing or cursing.                      |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | sexually_suggestive   | sexually suggestive   | 2         | Sexually explicit behavior or activity.   |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | slur                  | slur                  | 3         | Personal insult or hate speech.           |
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    # predefined
    none = P(0, 'none')
    cursing = P(1, 'cursing')
    sexually_suggestive = P(2, 'sexually suggestive')
    slur = P(3, 'slur')
