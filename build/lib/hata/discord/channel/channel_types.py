__all__ = ()

__doc__ = """
Contains channel type identifiers.

+---------------------------------------+-------+
| Name                                  | Value |
+=======================================+=======+
| guild_text                            | 0     |
+---------------------------------------+-------+
| private                               | 1     |
+---------------------------------------+-------+
| guild_voice                           | 2     |
+---------------------------------------+-------+
| private_group                         | 3     |
+---------------------------------------+-------+
| guild_category                        | 4     |
+---------------------------------------+-------+
| guild_announcements                   | 5     |
+---------------------------------------+-------+
| guild_store                           | 6     |
+---------------------------------------+-------+
| thread                                | 9     |
+---------------------------------------+-------+
| guild_thread_announcements            | 10    |
+---------------------------------------+-------+
| guild_thread_public                   | 11    |
+---------------------------------------+-------+
| guild_thread_private                  | 12    |
+---------------------------------------+-------+
| guild_stage                           | 13    |
+---------------------------------------+-------+
| guild_directory                       | 14    |
+---------------------------------------+-------+

In addition also extra groups are defined:

+---------------------------------------+-------------------------------+
| Name                                  | Elements                      |
+=======================================+===============================+
| GROUP_MESSAGEABLE                     | guild_text,                   |
|                                       | private,                      |
|                                       | private_group,                |
|                                       | guild_announcements,          |
|                                       | guild_thread_announcements,   |
|                                       | guild_thread_public,          |
|                                       | guild_thread_private          |
+---------------------------------------+-------------------------------+
| GROUP_GUILD_MESSAGEABLE               | guild_text,                   |
|                                       | guild_announcements,          |
|                                       | guild_thread_announcements,   |
|                                       | guild_thread_public,          |
|                                       | guild_thread_private          |
+---------------------------------------+-------------------------------+
| GROUP_GUILD_TEXT_LIKE                 | guild_text,                   |
|                                       | guild_announcements           |
+---------------------------------------+-------------------------------+
| GROUP_CONNECTABLE                     | private,                      |
|                                       | guild_voice,                  |
|                                       | private_group,                |
|                                       | guild_stage                   |
+---------------------------------------+-------------------------------+
| GROUP_GUILD_CONNECTABLE               | guild_voice,                  |
|                                       | guild_stage                   |
+---------------------------------------+-------------------------------+
| GROUP_PRIVATE                         | private,                      |
|                                       | private_group                 |
+---------------------------------------+-------------------------------+
| GROUP_GUILD                           | guild_text,                   |
|                                       | guild_voice,                  |
|                                       | guild_category,               |
|                                       | guild_announcements,          |
|                                       | guild_store,                  |
|                                       | guild_thread_announcements,   |
|                                       | guild_thread_public,          |
|                                       | guild_thread_private,         |
|                                       | guild_stage,                  |
|                                       | guild_directory               |
+---------------------------------------+-------------------------------+
| GROUP_THREAD                          | guild_thread_announcements,   |
|                                       | guild_thread_public,          |
|                                       | guild_thread_private          |
+---------------------------------------+-------------------------------+
"""
guild_text = 0
private = 1
guild_voice = 2
private_group = 3
guild_category = 4
guild_announcements = 5
guild_store = 6
# 7? Not in use
# 8? Not in use
thread = 9 # Not in use
guild_thread_announcements = 10
guild_thread_public = 11
guild_thread_private = 12
guild_stage = 13
guild_directory = 14


GROUP_MESSAGEABLE = frozenset((
    guild_text,
    private,
    private_group,
    guild_announcements,
    guild_thread_announcements,
    guild_thread_public,
    guild_thread_private,
))

GROUP_GUILD_MESSAGEABLE = frozenset((
    guild_text,
    guild_announcements,
    guild_thread_announcements,
    guild_thread_public,
    guild_thread_private,
))


GROUP_GUILD_TEXT_LIKE = frozenset((
    guild_text,
    guild_announcements,
))


GROUP_CONNECTABLE = frozenset((
    private,
    guild_voice,
    private_group,
    guild_stage,
))


GROUP_GUILD_CONNECTABLE = frozenset((
    guild_voice,
    guild_stage,
))


GROUP_PRIVATE = frozenset((
    private,
    private_group,
))


GROUP_GUILD = frozenset((
    guild_text,
    guild_voice,
    guild_category,
    guild_announcements,
    guild_store,
    guild_thread_announcements,
    guild_thread_public,
    guild_thread_private,
    guild_stage,
    guild_directory,
))

GROUP_THREAD = frozenset((
    guild_thread_announcements,
    guild_thread_public,
    guild_thread_private,
))
