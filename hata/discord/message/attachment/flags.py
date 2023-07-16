__all__ = ('AttachmentFlag',)

from ...bases import FlagBase


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
    __keys__ = {
        'clip': 0,
        'thumbnail': 1,
        'remix': 2,
    }
