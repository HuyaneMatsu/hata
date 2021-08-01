__all__ = ('PurchasedFlag', 'ThreadProfileFlag', 'UserFlag', )

from ..bases import FlagBase

class UserFlag(FlagBase):
    """
    Represents a user's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | staff                         | 0                 |
    +-------------------------------+-------------------+
    | partner                       | 1                 |
    +-------------------------------+-------------------+
    | hypesquad                     | 2                 |
    +-------------------------------+-------------------+
    | bug_hunter_level_1            | 3                 |
    +-------------------------------+-------------------+
    | mfa_sms                       | 4                 |
    +-------------------------------+-------------------+
    | premium_promo_dismissed       | 5                 |
    +-------------------------------+-------------------+
    | hypesquad_bravery             | 6                 |
    +-------------------------------+-------------------+
    | hypesquad_brilliance          | 7                 |
    +-------------------------------+-------------------+
    | hypesquad_balance             | 8                 |
    +-------------------------------+-------------------+
    | early_supporter               | 9                 |
    +-------------------------------+-------------------+
    | team_user                     | 10                |
    +-------------------------------+-------------------+
    | team_pseudo_user              | 11                |
    +-------------------------------+-------------------+
    | system                        | 12                |
    +-------------------------------+-------------------+
    | has_unread_urgent_messages    | 13                |
    +-------------------------------+-------------------+
    | bug_hunter_level_2            | 14                |
    +-------------------------------+-------------------+
    | underage_deleted              | 15                |
    +-------------------------------+-------------------+
    | verified_bot                  | 16                |
    +-------------------------------+-------------------+
    | early_verified_developer      | 17                |
    +-------------------------------+-------------------+
    | certified_moderator           | 18                |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'staff': 0,
        'partner': 1,
        'hypesquad': 2,
        'bug_hunter_level_1': 3,
        'mfa_sms': 4,
        'premium_promo_dismissed': 5,
        'hypesquad_bravery': 6,
        'hypesquad_brilliance': 7,
        'hypesquad_balance': 8,
        'early_supporter': 9,
        'team_user': 10,
        'team_pseudo_user': 11,
        'system': 12,
        'has_unread_urgent_messages': 13,
        'bug_hunter_level_2': 14,
        'underage_deleted': 15,
        'verified_bot': 16,
        'early_verified_developer': 17,
        'certified_moderator': 18,
    }


class ThreadProfileFlag(FlagBase):
    """
    Represents a ``ThreadProfile``'s user specific bitwise flag based settings.
    
    The implemented thread flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | has_interacted                | 0                 |
    +-------------------------------+-------------------+
    | all_messages                  | 1                 |
    +-------------------------------+-------------------+
    | only_mentions                 | 2                 |
    +-------------------------------+-------------------+
    | no_messages                   | 3                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'has_interacted': 0,
        'all_messages': 1,
        'only_mentions': 2,
        'no_messages': 3,
    }


class PurchasedFlag(FlagBase):
    """
    A user's purchase flags.
    
    The implemented purchased flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | premium_tier_1                | 1                 |
    +-------------------------------+-------------------+
    | premium_tier_2                | 2                 |
    +-------------------------------+-------------------+
    | premium_guild                 | 4                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'premium_tier_1': 1,
        'premium_tier_2': 2,
        'premium_guild': 4,
    }
