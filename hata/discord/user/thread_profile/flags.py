__all__ = ('ThreadProfileFlag',)

from ...bases import FlagBase, FlagDescriptor as F


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
    has_interacted = F(0)
    all_messages = F(1)
    only_mentions = F(2)
    no_messages = F(3)
