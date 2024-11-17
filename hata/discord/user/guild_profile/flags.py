__all__ = ('GuildProfileFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class GuildProfileFlag(FlagBase):
    """
    Represents a guild profile's flags.
    
    The implemented user flags are the following:
    
    +-----------------------------------------------------------+-------------------+
    | Respective name                                           | Bitwise position  |
    +===========================================================+===================+
    | rejoined                                                  | 0                 |
    +-----------------------------------------------------------+-------------------+
    | onboarding_completed                                      | 1                 |
    +-----------------------------------------------------------+-------------------+
    | bypasses_verification                                     | 2                 |
    +-----------------------------------------------------------+-------------------+
    | onboarding_started                                        | 3                 |
    +-----------------------------------------------------------+-------------------+
    | guest                                                     | 4                 |
    +-----------------------------------------------------------+-------------------+
    | home_actions_started                                      | 5                 |
    +-----------------------------------------------------------+-------------------+
    | home_actions_completed                                    | 6                 |
    +-----------------------------------------------------------+-------------------+
    | auto_moderation_quarantined_name_or_nick                  | 7                 |
    +-----------------------------------------------------------+-------------------+
    | auto_moderation_quarantined_bio                           | 8                 |
    +-----------------------------------------------------------+-------------------+
    | privacy_settings_direct_message_promotion_acknowledged    | 9                 |
    +------------------------------------------------------------+------------------+
    | auto_moderation_quarantined_clan_tag                      | 10                |
    +------------------------------------------------------------+------------------+
    """
    rejoined = F(0)
    onboarding_completed = F(1)
    bypasses_verification = F(2)
    onboarding_started = F(3)
    guest = F(4)
    home_actions_started = F(5)
    home_actions_completed = F(6)
    auto_moderation_quarantined_name_or_nick = F(7)
    auto_moderation_quarantined_bio = F(8)
    privacy_settings_direct_message_promotion_acknowledged = F(9)
    auto_moderation_quarantined_clan_tag = F(10)
