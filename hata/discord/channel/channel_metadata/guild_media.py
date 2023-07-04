__all__ = ('ChannelMetadataGuildMedia',)

from .guild_forum_base import ChannelMetadataGuildForumBase


class ChannelMetadataGuildMedia(ChannelMetadataGuildForumBase):
    """
    Guild media channel metadata.
    
    Attributes
    ----------
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    available_tags : `None`, `tuple` of ``ForumTag``
        The available tags to assign to the child-thread channels.
    default_forum_layout : ``ForumLayout``
        The default layout used to display threads of the forum.
    default_sort_order : ``SortOrder``
        The default thread ordering of the forum.
    default_thread_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    default_thread_reaction : `None`, ``Emoji``
        The emoji to show in the add reaction button on a thread of the forum channel.
    default_thread_slowmode : `int`
        The default slowmode applied to the channel's threads.
    flags : ``ChannelFlag``
        The channel's flags.
    name : `str`
        The channel's name.
    parent_id : `int`
        The channel's parent's identifier.
    permission_overwrites :`None`,  `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    topic : `None`, `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
