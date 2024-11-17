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
    """
    clip = F(0)
    thumbnail = F(1)
    remix = F(2)
