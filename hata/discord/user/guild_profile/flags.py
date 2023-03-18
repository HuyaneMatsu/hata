__all__ = ('GuildProfileFlag',)

from ...bases import FlagBase


class GuildProfileFlag(FlagBase):
    """
    Represents a guild profile's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------------------+-------------------+
    | Respective name                           | Bitwise position  |
    +===========================================+===================+
    | rejoined                                  | 0                 |
    +-------------------------------------------+-------------------+
    | onboarding_completed                      | 1                 |
    +-------------------------------------------+-------------------+
    | bypasses_verification                     | 2                 |
    +-------------------------------------------+-------------------+
    | onboarding_started                        | 3                 |
    +-------------------------------------------+-------------------+
    | ???                                       | 4                 |
    +-------------------------------------------+-------------------+
    | home_actions_started                      | 5                 |
    +-------------------------------------------+-------------------+
    | home_actions_completed                    | 6                 |
    +-------------------------------------------+-------------------+
    | auto_moderation_quarantined_name_or_nick  | 7                 |
    +-------------------------------------------+-------------------+
    | auto_moderation_quarantined_bio           | 8                 |
    +-------------------------------------------+-------------------+
    """
    __keys__ = {
        'rejoined': 0,
        'onboarding_completed': 1,
        'bypasses_verification': 2,
        'onboarding_started': 3,
        'home_actions_started': 5,
        'home_actions_completed': 6,
        'auto_moderation_quarantined_name_or_nick': 7,
        'auto_moderation_quarantined_bio': 8,
    }
