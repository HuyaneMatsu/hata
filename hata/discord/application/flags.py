__all__ = ('FlagBase',)

from ..bases import FlagBase

class ApplicationFlag(FlagBase):
    """
    Represents an application's flags.
    
    The implemented user flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | managed_emoji                     | 2                 |
    +-----------------------------------+-------------------+
    | group_dm_create                   | 4                 |
    +-----------------------------------+-------------------+
    | rpc_hash_connected                | 11                |
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
        'managed_emoji':  2,
        'group_dm_create':  4,
        'rpc_hash_connected': 11,
        'gateway_presence': 12,
        'gateway_presence_limited': 13,
        'gateway_guild_members': 14,
        'gateway_guild_members_limited': 15,
        'verification_pending_guild_limit': 16,
        'embedded': 17,
    }
