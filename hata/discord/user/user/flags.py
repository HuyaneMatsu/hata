__all__ = ('PurchasedFlag', 'UserFlag')

from ...bases import FlagBase, FlagDescriptor as F


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
    | bot_http_interactions         | 19                |
    +-------------------------------+-------------------+
    | spammer                       | 20                |
    +-------------------------------+-------------------+
    | premium_disabled              | 21                |
    +-------------------------------+-------------------+
    | active_developer              | 22                |
    +-------------------------------+-------------------+
    | provisional_account           | 23                |
    +-------------------------------+-------------------+
    | quarantined                   | 44                |
    +-------------------------------+-------------------+
    | collaborator                  | 50                |
    +-------------------------------+-------------------+
    | collaborator_restricted       | 51                |
    +-------------------------------+-------------------+
    """
    staff = F(0)
    partner = F(1)
    hypesquad = F(2)
    bug_hunter_level_1 = F(3)
    mfa_sms = F(4)
    premium_promo_dismissed = F(5)
    hypesquad_bravery = F(6)
    hypesquad_brilliance = F(7)
    hypesquad_balance = F(8)
    early_supporter = F(9)
    team_user = F(10)
    team_pseudo_user = F(11)
    system = F(12)
    has_unread_urgent_messages = F(13)
    bug_hunter_level_2 = F(14)
    underage_deleted = F(15)
    verified_bot = F(16)
    early_verified_developer = F(17)
    certified_moderator = F(18)
    bot_http_interactions = F(19)
    spammer = F(20)
    premium_disabled = F(21)
    active_developer = F(22)
    provisional_account = F(23)
    # ?????????????????????????????
    quarantined = F(44)
    # ???????
    collaborator = F(50)
    collaborator_restricted = F(51)


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
    premium_tier_1 = F(1)
    premium_tier_2 = F(2)
    premium_guild = F(4)
