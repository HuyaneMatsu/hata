__all__ = ('EmbedMediaFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class EmbedMediaFlag(FlagBase):
    """
    Bitwise flags of an embed media.
    
    The implemented embed media flags are the following:
    
    +-------------------+-------------------+
    | Respective name   | Bitwise position  |
    +===================+===================+
    | animated          | 5                 |
    +-------------------+-------------------+
    """
    # 0 ??
    # 1 ??
    # 2 ??
    # 3 ??
    # 4 ??
    animated = F(5)
