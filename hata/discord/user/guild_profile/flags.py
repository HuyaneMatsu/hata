__all__ = ('GuildProfileFlag',)

from ...bases import FlagBase


class GuildProfileFlag(FlagBase):
    """
    Represents a guild profile's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | rejoined                      | 0                 |
    +-------------------------------+-------------------+
    | onboarding_completed          | 1                 |
    +-------------------------------+-------------------+
    | bypasses_verification         | 2                 |
    +-------------------------------+-------------------+
    | onboarding_started            | 3                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'rejoined': 0,
        'onboarding_completed': 1,
        'bypasses_verification': 2,
        'onboarding_started': 3,
    }
