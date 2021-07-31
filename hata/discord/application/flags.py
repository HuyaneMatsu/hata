__all__ = ('FlagBase', 'SKUFlag',)

from ..bases import FlagBase

class ApplicationFlag(FlagBase):
    """
    Represents an application's flags.
    
    The implemented application flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | managed_emoji                     | 2                 |
    +-----------------------------------+-------------------+
    | group_dm_create                   | 4                 |
    +-----------------------------------+-------------------+
    | rpc_has_connected                 | 11                |
    +-----------------------------------+-------------------+
    | gateway_presence                  | 12                |
    +-----------------------------------+-------------------+
    | gateway_presence_limited          | 13                |
    +-----------------------------------+-------------------+
    | gateway_guild_members             | 14                |
    +-----------------------------------+-------------------+
    | gateway_guild_members_limited     | 15                |
    +-----------------------------------+-------------------+
    | verification_pending_guild_limit  | 16                |
    +-----------------------------------+-------------------+
    | embedded                          | 17                |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'managed_emoji': 2,
        'group_dm_create': 4,
        'rpc_has_connected': 11,
        'gateway_presence': 12,
        'gateway_presence_limited': 13,
        'gateway_guild_members': 14,
        'gateway_guild_members_limited': 15,
        'verification_pending_guild_limit': 16,
        'embedded': 17,
    }


class SKUFlag(FlagBase):
    """
    Represents an SKU's (stock keeping unit) flags.
    
    The implemented sku flags are the following:
    
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | premium_purchase          | 0                 |
    +---------------------------+-------------------+
    | has_free_premium_content  | 1                 |
    +---------------------------+-------------------+
    | available                 | 2                 |
    +---------------------------+-------------------+
    | premium_and_distribution  | 3                 |
    +---------------------------+-------------------+
    | sticker_pack              | 4                 |
    +---------------------------+-------------------+

    """
    __keys__ = {
        'premium_purchase': 0,
        'has_free_premium_content': 1,
        'available': 2,
        'premium_and_distribution': 3,
        'sticker_pack': 4,
    }
