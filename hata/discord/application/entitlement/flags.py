__all__ = ()

from ...bases import FlagBase, FlagDescriptor as F


class GiftCodeFlag(FlagBase):
    """
    Represents an entitlement gift code's flags.
    
    The gift code flags are the following:
    
    +-------------------------------------------+-------------------+
    | Respective name                           | Bitwise position  |
    +===========================================+===================+
    | playment_source_required                  | 0                 |
    +-------------------------------------------+-------------------+
    | not_redeemable_with_existing_subscription | 1                 |
    +-------------------------------------------+-------------------+
    | not_self_redeemable                       | 2                 |
    +-------------------------------------------+-------------------+
    | promotion                                 | 3                 |
    +-------------------------------------------+-------------------+
    """
    playment_source_required = F(0)
    not_redeemable_with_existing_subscription = F(1)
    not_self_redeemable = F(2)
    promotion = F(3)
