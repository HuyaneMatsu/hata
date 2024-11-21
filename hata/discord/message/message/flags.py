__all__ = ('MessageFlag',)

from datetime import datetime as DateTime, timezone as TimeZone

from ...bases import FlagBase, FlagDeprecation as FD, FlagDescriptor as F


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
    | ???                                       | 9                 |
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
    # 9 ???
    should_show_link_not_discord_warning = F(10)
    # 11 ???
    silent = F(12)
    voice_message = F(13)
    has_snapshot = F(14)

    is_crosspost = F(1, deprecation = FD('crosspost', DateTime(2024, 12, 15, tzinfo = TimeZone.utc)))
