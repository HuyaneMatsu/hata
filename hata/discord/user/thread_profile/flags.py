__all__ = ('ThreadProfileFlag',)

from ...bases import FlagBase


class ThreadProfileFlag(FlagBase):
    """
    Represents a ``ThreadProfile``'s user specific bitwise flag based settings.
    
    The implemented thread flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | has_interacted                | 0                 |
    +-------------------------------+-------------------+
    | all_messages                  | 1                 |
    +-------------------------------+-------------------+
    | only_mentions                 | 2                 |
    +-------------------------------+-------------------+
    | no_messages                   | 3                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'has_interacted': 0,
        'all_messages': 1,
        'only_mentions': 2,
        'no_messages': 3,
    }

