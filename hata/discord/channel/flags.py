__all__ = ('ChannelFlag', )

from ..bases import FlagBase


class ChannelFlag(FlagBase):
    """
    Represents a channel's flags.
    
    The implemented channel flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | pinned                        | 1                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'pinned': 1,
    }
