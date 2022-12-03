__all__ = ('ChannelMetadataGuildAnnouncements',)

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import (
    PERMISSION_DENY_SEND_MESSAGES_IN_THREADS_ONLY, PERMISSION_MASK_MANAGE_MESSAGES, PERMISSION_MASK_SEND_MESSAGES,
    PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_TEXT_DENY, PERMISSION_VOICE_DENY
)

from .guild_text_base import ChannelMetadataGuildTextBase


class ChannelMetadataGuildAnnouncements(ChannelMetadataGuildTextBase):
    """
    Guild announcements channel metadata.
    
    Attributes
    ----------
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `int`
        The channel's parent's identifier.
    name : `str`
        The channel's name.
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    default_thread_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    default_thread_slowmode : `int`
        Applied as `thread.slowmode` when one is created.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    topic : `None`, `str`
        The channel's topic.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages`, `manage_channels` permissions are unaffected.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
    
    @copy_docs(ChannelMetadataGuildTextBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if result & PERMISSION_MASK_MANAGE_MESSAGES:
            if result & PERMISSION_MASK_SEND_MESSAGES:
                result &= PERMISSION_DENY_SEND_MESSAGES_IN_THREADS_ONLY
            else:
                result &= PERMISSION_TEXT_DENY
        else:
            result &= PERMISSION_TEXT_DENY
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildTextBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if result & PERMISSION_MASK_MANAGE_MESSAGES:
            if result & PERMISSION_MASK_SEND_MESSAGES:
                result &= PERMISSION_DENY_SEND_MESSAGES_IN_THREADS_ONLY
            else:
                result &= PERMISSION_TEXT_DENY
        else:
            result &= PERMISSION_TEXT_DENY
        
        return Permission(result)
