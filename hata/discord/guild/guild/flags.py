__all__ = ('SystemChannelFlag',)

from ...bases import FlagBaseReversed, FlagDescriptor as F


class SystemChannelFlag(FlagBaseReversed):
    """
    The flags of a ``Guild``'s system channel.
    
    For Discord these flags tell, what ``MessageType`-s are not sent to the guild's system channel, but the wrapper
    reverses this behaviour.
    
    The implemented system channel flags are the following:
    
    +---------------------------------------+-------------------+
    | Respective name                       | Bitwise position  |
    +=======================================+===================+
    | welcome                               | 0                 |
    +---------------------------------------+-------------------+
    | boost                                 | 1                 |
    +---------------------------------------+-------------------+
    | setup_tips                            | 2                 |
    +---------------------------------------+-------------------+
    | join_sticker_replies                  | 3                 |
    +---------------------------------------+-------------------+
    | role_subscription_purchase            | 4                 |
    +---------------------------------------+-------------------+
    | role_subscription_purchase_replies    | 5                 |
    +---------------------------------------+-------------------+
    | ???                                   | 6                 |
    +---------------------------------------+-------------------+
    | ???                                   | 7                 |
    +---------------------------------------+-------------------+
    | emoji_added_notification              | 8                 |
    +---------------------------------------+-------------------+
    
    There are also predefined ``SystemChannelFlag``-s:
    
    +-----------------------+---------------------------+
    | Type attribute name   | value                     |
    +=======================+===========================+
    | NONE                  | ActivityFlag(0b100111111) |
    +-----------------------+---------------------------+
    | ALL                   | ActivityFlag(0b000000000) |
    +-----------------------+---------------------------+
    """
    welcome = F(0)
    boost = F(1)
    setup_tips = F(2)
    join_sticker_replies = F(3)
    role_subscription_purchase = F(4)
    role_subscription_purchase_replies = F(5)
    # 6 ???
    # 7 ???
    emoji_added_notification = F(8)
    
    @property
    def none(self):
        """
        Whether the flag not allows any system messages at the respective system channel.
        
        Returns
        -------
        none : `bool`
        """
        return (self == self.NONE)
    
    @property
    def all(self):
        """
        Whether the flag allows all the system messages at the respective system channel.
        
        Returns
        -------
        none : `bool`
        """
        return (self == self.ALL)
    
    
    NONE = NotImplemented
    ALL = NotImplemented


SystemChannelFlag.NONE = SystemChannelFlag(0b100111111)
SystemChannelFlag.ALL = SystemChannelFlag(0b000000000)
