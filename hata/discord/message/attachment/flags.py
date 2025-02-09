__all__ = ('AttachmentFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class AttachmentFlag(FlagBase):
    """
    Represents a attachment's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------------------+-------------------+
    | Respective name                           | Bitwise position  |
    +===========================================+===================+
    | clip                                      | 0                 |
    +-------------------------------------------+-------------------+
    | thumbnail                                 | 1                 |
    +-------------------------------------------+-------------------+
    | remix                                     | 2                 |
    +-------------------------------------------+-------------------+
    | spoiler                                   | 3                 |
    +-------------------------------------------+-------------------+
    | explicit                                  | 4                 |
    +-------------------------------------------+-------------------+
    | animated                                  | 5                 |
    +-------------------------------------------+-------------------+
    """
    clip = F(0)
    thumbnail = F(1)
    remix = F(2)
    spoiler = F(3)
    explicit = F(4)
    animated = F(5)
