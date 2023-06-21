__all__ = ('ChannelMetadataGuildThreadAnnouncements',)

from .guild_thread_base import ChannelMetadataGuildThreadBase


class ChannelMetadataGuildThreadAnnouncements(ChannelMetadataGuildThreadBase):
    """
    Base guild channel metadata type.
    
    Attributes
    ----------
    _created_at : `None`, `datetime`
        When the channel was created.
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    archived : `bool`
        Whether the thread s archived.
    archived_at : `None`, `datetime`
        When the thread's archive status was last changed.
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    name : `str`
        The channel's name.
    open : `bool`
        Whether the thread channel is open.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
    parent_id : `int`
        The channel's parent's identifier.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages`, `manage_channels` permissions are unaffected.
    thread_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        The users inside of the thread if any.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
