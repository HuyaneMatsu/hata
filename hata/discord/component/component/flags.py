__all__ = ('ComponentTypeLayoutFlag',)

from ...bases import FlagBase


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
    __keys__ = {
        'top_level': 0,
        'nestable': 1,
    }
