__all__ = ('SKUFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class SKUFlag(FlagBase):
    """
    Represents an SKU's (stock keeping unit) flags.
    
    The implemented sku flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | premium_purchase                  | 0                 |
    +-----------------------------------+-------------------+
    | has_free_premium_content          | 1                 |
    +-----------------------------------+-------------------+
    | available                         | 2                 |
    +-----------------------------------+-------------------+
    | premium_and_distribution          | 3                 |
    +-----------------------------------+-------------------+
    | sticker_pack                      | 4                 |
    +-----------------------------------+-------------------+
    | guild_role                        | 5                 |
    +-----------------------------------+-------------------+
    | giftable                          | 6                 |
    +-----------------------------------+-------------------+
    | application_guild_subscription    | 7                 |
    +-----------------------------------+-------------------+
    | application_user_subscription     | 8                 |
    +-----------------------------------+-------------------+
    | creator_monetization              | 9                 |
    +-----------------------------------+-------------------+
    | guild_product                     | 10                |
    +-----------------------------------+-------------------+
    """
    premium_purchase = F(0)
    has_free_premium_content = F(1)
    available = F(2)
    premium_and_distribution = F(3)
    sticker_pack = F(4)
    guild_role = F(5)
    giftable = F(6)
    application_guild_subscription = F(7)
    application_user_subscription = F(8)
    creator_monetization = F(9)
    guild_product = F(10)
