__all__ = ('ApplicationFlag',)

from ...bases import FlagBase


class ApplicationFlag(FlagBase):
    """
    Represents an application's flags.
    
    The implemented application flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | embedded_released                 | 1                 |
    +-----------------------------------+-------------------+
    | managed_emoji                     | 2                 |
    +-----------------------------------+-------------------+
    | embedded_iap                      | 3                 |
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
    | gateway_message_content           | 18                |
    +-----------------------------------+-------------------+
    | gateway_message_content_limited   | 19                |
    +-----------------------------------+-------------------+
    | embedded_first_party              | 20                |
    +-----------------------------------+-------------------+
    | application_command_badge         | 23                |
    +-----------------------------------+-------------------+
    | active                            | 24                |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'embedded_released': 1,
        'managed_emoji': 2,
        'embedded_iap': 3,
        'group_dm_create': 4,
        'rpc_has_connected': 11,
        'gateway_presence': 12,
        'gateway_presence_limited': 13,
        'gateway_guild_members': 14,
        'gateway_guild_members_limited': 15,
        'verification_pending_guild_limit': 16,
        'embedded': 17,
        'gateway_message_content': 18,
        'gateway_message_content_limited': 19,
        'embedded_first_party': 20,
        'application_command_badge': 23,
        'active': 24,
    }
