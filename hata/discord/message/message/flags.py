__all__ = ('MessageFlag',)

from ...bases import FlagBase, FlagDescriptor as F


class MessageFlag(FlagBase):
    """
    Bitwise flags of a ``Message``.
    
    The implemented message flags are the following:
    
    +-------------------------------------------+-------------------+
    | Respective name                           | Bitwise position  |
    +===========================================+===================+
    | crossposted                               | 0                 |
    +-------------------------------------------+-------------------+
    | crosspost                                 | 1                 |
    +-------------------------------------------+-------------------+
    | embeds_suppressed                         | 2                 |
    +-------------------------------------------+-------------------+
    | source_message_deleted                    | 3                 |
    +-------------------------------------------+-------------------+
    | urgent                                    | 4                 |
    +-------------------------------------------+-------------------+
    | has_thread                                | 5                 |
    +-------------------------------------------+-------------------+
    | invoking_user_only                        | 6                 |
    +-------------------------------------------+-------------------+
    | loading                                   | 7                 |
    +-------------------------------------------+-------------------+
    | failed_to_mention_some_roles_in_thread    | 8                 |
    +-------------------------------------------+-------------------+
    | guild_feed_hidden                         | 9                 |
    +-------------------------------------------+-------------------+
    | should_show_link_not_discord_warning      | 10                |
    +-------------------------------------------+-------------------+
    | ???                                       | 11                |
    +-------------------------------------------+-------------------+
    | silent                                    | 12                |
    +-------------------------------------------+-------------------+
    | voice_message                             | 13                |
    +-------------------------------------------+-------------------+
    | has_snapshot                              | 14                |
    +-------------------------------------------+-------------------+
    | components_v2                             | 15                |
    +-------------------------------------------+-------------------+
    | created_by_social_integration             | 16                |
    +-------------------------------------------+-------------------+
    """
    crossposted = F(0)
    crosspost = F(1)
    embeds_suppressed = F(2)
    source_message_deleted = F(3)
    urgent = F(4)
    has_thread = F(5)
    invoking_user_only = F(6)
    loading = F(7)
    failed_to_mention_some_roles_in_thread = F(8)
    guild_feed_hidden = F(9)
    should_show_link_not_discord_warning = F(10)
    # 11 ???
    silent = F(12)
    voice_message = F(13)
    has_snapshot = F(14)
    components_v2 = F(15)
    created_by_social_integration = F(16)
