__all__ = ('AttachmentFlag',)

from datetime import datetime as DateTime, timezone as TimeZone

from ...bases import FlagBase, FlagDescriptor as F, FlagDeprecation as FD


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
    | erotic                                    | 4                 |
    +-------------------------------------------+-------------------+
    | animated                                  | 5                 |
    +-------------------------------------------+-------------------+
    | gore                                      | 6                 |
    +-------------------------------------------+-------------------+
    """
    clip = F(0)
    thumbnail = F(1)
    remix = F(2)
    spoiler = F(3)
    erotic = F(4)
    animated = F(5)
    gore = F(6)
    
    explicit = F(
        erotic.shift,
        deprecation = FD(
            'nestable_into_row',
            DateTime(2026, 1, 29, tzinfo = TimeZone.utc),
        ),
    )
