__all__ = ('ComponentTypeLayoutFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class ComponentTypeLayoutFlag(FlagBase):
    """
    Represents a components layout information.
    +-------------------+-------------------+
    | Respective name   | Bitwise position  |
    +===================+===================+
    | top_level         | 0                 |
    +-------------------+-------------------+
    | nestable          | 1                 |
    +-------------------+-------------------+
    """
    top_level = F(0)
    nestable = F(1)
