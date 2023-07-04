__all__ = ('ChannelTypeFlag', )

from scarletio import class_property

from ...bases import FlagBase


CHANNEL_TYPE_SHIFT_CONNECTABLE = 0
CHANNEL_TYPE_SHIFT_GUILD = 1
CHANNEL_TYPE_SHIFT_GUILD_SORTABLE = 2
CHANNEL_TYPE_SHIFT_GUILD_SYSTEM = 3
CHANNEL_TYPE_SHIFT_INVITABLE = 4
CHANNEL_TYPE_SHIFT_PRIVATE = 5
CHANNEL_TYPE_SHIFT_READABLE = 6
CHANNEL_TYPE_SHIFT_TEXTUAL = 7
CHANNEL_TYPE_SHIFT_THREAD = 8
CHANNEL_TYPE_SHIFT_THREADABLE = 9
CHANNEL_TYPE_SHIFT_FORUM = 10

CHANNEL_TYPE_MASK_CONNECTABLE = 1 << CHANNEL_TYPE_SHIFT_CONNECTABLE
CHANNEL_TYPE_MASK_GUILD = 1 << CHANNEL_TYPE_SHIFT_GUILD
CHANNEL_TYPE_MASK_GUILD_SORTABLE = 1 << CHANNEL_TYPE_SHIFT_GUILD_SORTABLE
CHANNEL_TYPE_MASK_GUILD_SYSTEM = 1 << CHANNEL_TYPE_SHIFT_GUILD_SYSTEM
CHANNEL_TYPE_MASK_INVITABLE = 1 << CHANNEL_TYPE_SHIFT_INVITABLE
CHANNEL_TYPE_MASK_PRIVATE = 1 << CHANNEL_TYPE_SHIFT_PRIVATE
CHANNEL_TYPE_MASK_READABLE = 1 << CHANNEL_TYPE_SHIFT_READABLE
CHANNEL_TYPE_MASK_TEXTUAL = 1 << CHANNEL_TYPE_SHIFT_TEXTUAL
CHANNEL_TYPE_MASK_THREAD = 1 << CHANNEL_TYPE_SHIFT_THREAD
CHANNEL_TYPE_MASK_THREADABLE = 1 << CHANNEL_TYPE_SHIFT_THREADABLE
CHANNEL_TYPE_MASK_FORUM = 1 << CHANNEL_TYPE_SHIFT_FORUM


class ChannelTypeFlag(FlagBase):
    """
    Represents a channel type's flags.
    
    Channel type flags are used to define for which role a channel type can be used.
    
    The implemented channel flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | connectable                   | 0                 |
    +-------------------------------+-------------------+
    | guild                         | 1                 |
    +-------------------------------+-------------------+
    | guild_sortable                | 2                 |
    +-------------------------------+-------------------+
    | guild_system                  | 3                 |
    +-------------------------------+-------------------+
    | invitable                     | 4                 |
    +-------------------------------+-------------------+
    | private                       | 5                 |
    +-------------------------------+-------------------+
    | readable                      | 6                 |
    +-------------------------------+-------------------+
    | textual                       | 7                 |
    +-------------------------------+-------------------+
    | thread                        | 8                 |
    +-------------------------------+-------------------+
    | threadable                    | 9                 |
    +-------------------------------+-------------------+
    | forum                         | 10                |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'connectable': CHANNEL_TYPE_SHIFT_CONNECTABLE,
        'guild': CHANNEL_TYPE_SHIFT_GUILD,
        'guild_sortable': CHANNEL_TYPE_SHIFT_GUILD_SORTABLE,
        'guild_system': CHANNEL_TYPE_SHIFT_GUILD_SYSTEM,
        'invitable': CHANNEL_TYPE_SHIFT_INVITABLE,
        'private': CHANNEL_TYPE_SHIFT_PRIVATE,
        'readable': CHANNEL_TYPE_SHIFT_READABLE,
        'textual': CHANNEL_TYPE_SHIFT_TEXTUAL,
        'thread': CHANNEL_TYPE_SHIFT_THREAD,
        'threadable': CHANNEL_TYPE_SHIFT_THREADABLE,
        'forum': CHANNEL_TYPE_SHIFT_FORUM,
    }
    
    
    @class_property
    def all(cls):
        """
        Returns a value which has all flags.
        
        Returns
        -------
        value : ``ChannelTypeFlag``
        """
        value = 0
        
        for shift in cls.__keys__.values():
            value |= 1 << shift
        
        return cls(value)
