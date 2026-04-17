__all__ = ('RoleFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class RoleFlag(FlagBase):
    """
    Represents a role's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------------------+-------------------+
    | Respective name                           | Bitwise position  |
    +===========================================+===================+
    | in_prompt                                 | 0                 |
    +-------------------------------------------+-------------------+
    """
    in_prompt = F(0)
