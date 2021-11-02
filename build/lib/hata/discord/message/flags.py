__all__ = ('MessageFlag',)

from ..bases import FlagBase

class MessageFlag(FlagBase):
    """
    Bitwise flags of a ``Message``.
    
    The implemented message flags are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | crossposted               | 0                 |
    +---------------------------+-------------------+
    | is_crosspost              | 1                 |
    +---------------------------+-------------------+
    | embeds_suppressed         | 2                 |
    +---------------------------+-------------------+
    | source_message_deleted    | 3                 |
    +---------------------------+-------------------+
    | urgent                    | 4                 |
    +---------------------------+-------------------+
    | has_thread                | 5                 |
    +---------------------------+-------------------+
    | invoking_user_only        | 6                 |
    +---------------------------+-------------------+
    | loading                   | 7                 |
    +---------------------------+-------------------+
    """
    __keys__ = {
        'crossposted': 0,
        'is_crosspost': 1,
        'embeds_suppressed': 2,
        'source_message_deleted': 3,
        'urgent': 4,
        'has_thread': 5,
        'invoking_user_only': 6,
        'loading': 7,
    }
