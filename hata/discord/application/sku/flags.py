__all__ = ('SKUFlag',)

from ...bases import FlagBase


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
    """
    __keys__ = {
        'premium_purchase': 0,
        'has_free_premium_content': 1,
        'available': 2,
        'premium_and_distribution': 3,
        'sticker_pack': 4,
        'guild_role': 5,
        'giftable': 6,
        'application_guild_subscription': 7,
        'application_user_subscription': 8,
    }
