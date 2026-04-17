__all__ = ('EmbedFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class EmbedFlag(FlagBase):
    """
    Bitwise flags of an embed.
    
    The implemented embed flags are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | explicit                  | 4                 |
    +---------------------------+-------------------+
    | content_inventory_entry   | 5                 |
    +---------------------------+-------------------+
    """
    # 0 ??
    # 1 ??
    # 2 ??
    # 3 ??
    explicit = F(4)
    content_inventory_entry = F(5)
