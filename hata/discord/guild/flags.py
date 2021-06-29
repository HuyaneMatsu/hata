__all__ = ('SystemChannelFlag',)

from ..bases import ReverseFlagBase

class SystemChannelFlag(ReverseFlagBase):
    """
    The flags of a ``Guild``'s system channel.
    
    For Discord these flags tell, what ``MessageType`-s are not sent to the guild's system channel, but the wrapper
    reverses this behaviour.
    
    The implemented system channel flags are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | welcome                   | 0                 |
    +---------------------------+-------------------+
    | boost                     | 1                 |
    +---------------------------+-------------------+
    | setup_tips                | 2                 |
    +---------------------------+-------------------+
    
    There are also predefined ``SystemChannelFlag``-s:
    
    +-----------------------+-----------------------+
    | Class attribute name  | value                 |
    +=======================+=======================+
    | NONE                  | ActivityFlag(0b111)   |
    +-----------------------+-----------------------+
    | ALL                   | ActivityFlag(0b000)   |
    +-----------------------+-----------------------+
    """
    __keys__ = {
        'welcome': 0,
        'boost': 1,
        'setup_tips': 2,
    }
    
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

SystemChannelFlag.NONE = SystemChannelFlag(0b111)
SystemChannelFlag.ALL = SystemChannelFlag(0b000)
