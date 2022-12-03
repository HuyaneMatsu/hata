__all__ = ('ChannelMetadataGuildTextBase',)

from scarletio import copy_docs

from .constants import AUTO_ARCHIVE_DEFAULT, SLOWMODE_DEFAULT
from .fields import (
    parse_default_thread_auto_archive_after, parse_default_thread_slowmode, parse_nsfw, parse_slowmode, parse_topic,
    put_default_thread_auto_archive_after_into, put_default_thread_slowmode_into, put_nsfw_into, put_slowmode_into,
    put_topic_into, validate_default_thread_auto_archive_after, validate_default_thread_slowmode, validate_nsfw,
    validate_slowmode, validate_topic
)

from .guild_main_base import ChannelMetadataGuildMainBase


class ChannelMetadataGuildTextBase(ChannelMetadataGuildMainBase):
    """
    Guild text channel metadata base.
    
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
    slowmode : `int`
        The amount of time in seconds that a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages`, `manage_channels` permissions are unaffected.
    topic : `None`, `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('default_thread_auto_archive_after', 'default_thread_slowmode', 'nsfw', 'slowmode', 'topic')
    
    
    @copy_docs(ChannelMetadataGuildMainBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildMainBase.__hash__(self)
        
        # default_thread_auto_archive_after
        hash_value ^= self.default_thread_auto_archive_after << 16
        
        # default_thread_slowmode
        hash_value ^= self.default_thread_slowmode << 8
        
        # nsfw
        hash_value ^= self.nsfw << 28
        
        # slowmode
        hash_value ^= self.slowmode << 4
        
        # topic
        topic = self.topic
        if (topic is not None):
            hash_value ^= hash(topic)
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildMainBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildMainBase._is_equal_same_type(self, other):
            return False
        
        # default_thread_auto_archive_after
        if self.default_thread_auto_archive_after != other.default_thread_auto_archive_after:
            return False
        
        # default_thread_slowmode
        if self.default_thread_slowmode != other.default_thread_slowmode:
            return False
        
        # nsfw
        if self.nsfw != other.nsfw:
            return False
        
        # slowmode
        if self.slowmode != other.slowmode:
            return False
        
        # topic
        if self.topic != other.topic:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_display_name)
    def _get_display_name(self):
        return self.name.lower()
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildTextBase, cls)._create_empty()
        
        self.default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.default_thread_slowmode = SLOWMODE_DEFAULT
        self.nsfw = False
        self.slowmode = SLOWMODE_DEFAULT
        self.topic = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        # default_thread_auto_archive_after
        self.default_thread_auto_archive_after = parse_default_thread_auto_archive_after(data)
        
        # default_thread_slowmode
        self.default_thread_slowmode = parse_default_thread_slowmode(data)
        
        # nsfw
        self.nsfw = parse_nsfw(data)
        
        # slowmode
        self.slowmode = parse_slowmode(data)
        
        # topic
        self.topic = parse_topic(data)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        # default_thread_auto_archive_after
        default_thread_auto_archive_after = parse_default_thread_auto_archive_after(data)
        if self.default_thread_auto_archive_after != default_thread_auto_archive_after:
            old_attributes['default_thread_auto_archive_after'] = self.default_thread_auto_archive_after
            self.default_thread_auto_archive_after = default_thread_auto_archive_after
        
        # default_thread_slowmode
        default_thread_slowmode = parse_default_thread_slowmode(data)
        if self.default_thread_slowmode != default_thread_slowmode:
            old_attributes['default_thread_slowmode'] = self.default_thread_slowmode
            self.default_thread_slowmode = default_thread_slowmode
        
        # nsfw
        nsfw = parse_nsfw(data)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        # slowmode
        slowmode = parse_slowmode(data)
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        # topic
        topic = parse_topic(data)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # default_thread_auto_archive_after
        try:
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after')
        except KeyError:
            pass
        else:
            self.default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_slowmode
        try:
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode')
        except KeyError:
            pass
        else:
            self.default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # nsfw
        try:
            nsfw = keyword_parameters.pop('nsfw')
        except KeyError:
            pass
        else:
            self.nsfw = validate_nsfw(nsfw)
        
        # slowmode
        try:
            slowmode = keyword_parameters.pop('slowmode')
        except KeyError:
            pass
        else:
            self.slowmode = validate_slowmode(slowmode)
        
        # topic
        try:
            topic = keyword_parameters.pop('topic')
        except KeyError:
            pass
        else:
            self.topic = validate_topic(topic)
    
    
    @copy_docs(ChannelMetadataGuildMainBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildMainBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # default_auto_archive_duration
        put_default_thread_auto_archive_after_into(self.default_thread_auto_archive_after, data, defaults)
        
        # default_thread_slowmode
        put_default_thread_slowmode_into(self.default_thread_slowmode, data, defaults)
        
        # nsfw
        put_nsfw_into(self.nsfw, data, defaults)
        
        # slowmode
        put_slowmode_into(self.slowmode, data, defaults)
        
        # topic
        put_topic_into(self.topic, data, defaults)
        
        return data
