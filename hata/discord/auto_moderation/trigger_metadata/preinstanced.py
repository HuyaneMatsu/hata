__all__ = ('AutoModerationKeywordPresetType', )

from ...bases import Preinstance as P, PreinstancedBase


class AutoModerationKeywordPresetType(PreinstancedBase, value_type = int):
    """
    Represents an auto moderation keyword preset type.
    
    Attributes
    ----------
    name : `str`
        The default name of the auto moderation keyword preset type.
    
    value : `int`
        The Discord side identifier value of the auto moderation keyword preset type.
    
    Type Attributes
    ---------------
    Every predefined auto moderation keyword preset type is also stored as a type attribute:
    
    +-----------------------+-----------------------+-----------+-------------------------------------------+
    | Type attribute name   | Name                  | Value     | Description                               |
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
    
    # predefined
    none = P(0, 'none')
    cursing = P(1, 'cursing')
    sexually_suggestive = P(2, 'sexually suggestive')
    slur = P(3, 'slur')
