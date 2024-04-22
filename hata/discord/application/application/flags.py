__all__ = ('ApplicationDiscoveryEligibilityFlags', 'ApplicationFlag', 'ApplicationMonetizationEligibilityFlags')

from ...bases import FlagBase


class ApplicationDiscoveryEligibilityFlags(FlagBase):
    """
    Represents which step the application passed to be eligible for discoverability.

    The implemented flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | verified                          | 0                 |
    +-----------------------------------+-------------------+
    | tag                               | 1                 |
    +-----------------------------------+-------------------+
    | description                       | 2                 |
    +-----------------------------------+-------------------+
    | terms_of_service                  | 3                 |
    +-----------------------------------+-------------------+
    | privacy_policy                    | 4                 |
    +-----------------------------------+-------------------+
    | install_parameters                | 5                 |
    +-----------------------------------+-------------------+
    | safe_name                         | 6                 |
    +-----------------------------------+-------------------+
    | safe_description                  | 7                 |
    +-----------------------------------+-------------------+
    | approved_commands                 | 8                 |
    +-----------------------------------+-------------------+
    | support_guild                     | 9                 |
    +-----------------------------------+-------------------+
    | safe_commands                     | 10                |
    +-----------------------------------+-------------------+
    | owner_mfa_enabled                 | 11                |
    +-----------------------------------+-------------------+
    | safe_directory_overview           | 12                |
    +-----------------------------------+-------------------+
    | supports_localization             | 13                |
    +-----------------------------------+-------------------+
    | safe_short_description            | 14                |
    +-----------------------------------+-------------------+
    | safe_role_connections             | 15                |
    +-----------------------------------+-------------------+
    | eligible                          | 16                |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'verified': 0,
        'tag': 1,
        'description': 2,
        'terms_of_service': 3,
        'privacy_policy': 4,
        'install_parameters': 5,
        'safe_name': 6,
        'safe_description': 7,
        'approved_commands': 8,
        'support_guild': 9,
        'safe_commands': 10,
        'owner_mfa_enabled': 11,
        'safe_directory_overview': 12,
        'supports_localization': 13,
        'safe_short_description': 14,
        'safe_role_connections': 15,
        'eligible': 16,
    }


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
    | auto_moderation_rule_create_badge | 6                 |
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
    | iframe_form                       | 26                |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'embedded_released': 1,
        'managed_emoji': 2,
        'embedded_iap': 3,
        'group_dm_create': 4,
        'auto_moderation_rule_create_badge': 6,
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
        'iframe_form': 26,
    }


class ApplicationMonetizationEligibilityFlags(FlagBase):
    """
    Represents which step the application passed to be eligible for monetization. 

    The implemented flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | verified                          | 0                 |
    +-----------------------------------+-------------------+
    | owned_by_team                     | 1                 |
    +-----------------------------------+-------------------+
    | approved_commands                 | 2                 |
    +-----------------------------------+-------------------+
    | terms_of_service                  | 3                 |
    +-----------------------------------+-------------------+
    | privacy_policy                    | 4                 |
    +-----------------------------------+-------------------+
    | safe_name                         | 5                 |
    +-----------------------------------+-------------------+
    | safe_description                  | 6                 |
    +-----------------------------------+-------------------+
    | safe_role_connections             | 7                 |
    +-----------------------------------+-------------------+
    | user_team_owner                   | 8                 |
    +-----------------------------------+-------------------+
    | not_quarantined                   | 9                 |
    +-----------------------------------+-------------------+
    | user_localization_supported       | 10                |
    +-----------------------------------+-------------------+
    | user_legal_adult                  | 11                |
    +-----------------------------------+-------------------+
    | user_birth_date_defined           | 12                |
    +-----------------------------------+-------------------+
    | user_mfa_enabled                  | 13                |
    +-----------------------------------+-------------------+
    | user_email_verified               | 14                |
    +-----------------------------------+-------------------+
    | team_members_email_verified       | 15                |
    +-----------------------------------+-------------------+
    | team_members_mfa_enabled          | 16                |
    +-----------------------------------+-------------------+
    | no_blocking_issues                | 17                |
    +-----------------------------------+-------------------+
    | valid_payout_status               | 18                |
    +-----------------------------------+-------------------+
    | eligible                          | 19                |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'verified': 0,
        'owned_by_team': 1,
        'approved_commands': 2,
        'terms_of_service': 3,
        'privacy_policy': 4,
        'safe_name': 5,
        'safe_description': 6,
        'safe_role_connections': 7,
        'user_team_owner': 8,
        'not_quarantined': 9,
        'user_localization_supported': 10,
        'user_legal_adult': 11,
        'user_birth_date_defined': 12,
        'user_mfa_enabled': 13,
        'user_email_verified': 14,
        'team_members_email_verified': 15,
        'team_members_mfa_enabled': 16,
        'no_blocking_issues': 17,
        'valid_payout_status': 18,
        'eligible': 19,
    }
    
    
    __deprecated_keys__ = {
        'user_2fa_enabled': (
            13, '2024 December', 'user_mfa_enabled'
        ),
    }


class ApplicationOverlayMethodFlags(FlagBase):
    """
    Represents which features the application's overlaying supports.

    The implemented flags are the following:
    
    +-----------------------------------+-------------------+
    | Respective name                   | Bitwise position  |
    +===================================+===================+
    | out_of_process                    | 0                 |
    +-----------------------------------+-------------------+
    """
    __keys__ = {
        'out_of_process': 0,
    }
