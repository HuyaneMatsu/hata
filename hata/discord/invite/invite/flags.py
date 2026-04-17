__all__ = ('InviteFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class InviteFlag(FlagBase):
    """
    Represents an invite's flags.
    
    The implemented invite flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | guest                             | 1                 |
    +-----------------------------------+-------------------+
    """
    guest = F(1)
