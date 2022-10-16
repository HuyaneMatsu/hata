__all__ = ('ChannelFlag', )

from ...bases import FlagBase


class ChannelFlag(FlagBase):
    """
    Represents a channel's flags.
    
    The implemented channel flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | guild_feed_removed            | 0                 |
    +-------------------------------+-------------------+
    | pinned                        | 1                 |
    +-------------------------------+-------------------+
    | active_channels_removed       | 2                 |
    +-------------------------------+-------------------+
    | ???                           | 3                 |
    +-------------------------------+-------------------+
    | require_tag                   | 4                 |
    +-------------------------------+-------------------+
    | spam                          | 5                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'guild_feed_removed': 0,
        'pinned': 1,
        'active_channels_removed': 2,
        'require_tag': 4,
        'spam': 5,
    }
