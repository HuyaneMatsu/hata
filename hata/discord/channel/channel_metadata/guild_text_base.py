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
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    default_thread_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    default_thread_slowmode : `int`
        Applied as `thread.slowmode` when one is created.
    name : `str`
        The channel's name.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    parent_id : `int`
        The channel's parent's identifier.
    permission_overwrites :`None`,  `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
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
    
    
    def __new__(
        cls,
        *,
        default_thread_auto_archive_after = ...,
        default_thread_slowmode = ...,
        name = ...,
        nsfw = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        slowmode = ...,
        topic = ...,
    ):
        """
        Creates a new guild text base channel metadata from the given parameters.
        
        Parameters
        ----------
        default_thread_auto_archive_after : `int``, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        default_thread_slowmode : `int`
            Applied as `thread.slowmode` when one is created.
        name : `str`, Optional (Keyword only)
            The channel's name.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        slowmode : `int`, Optional (Keyword only)
            The amount of time in seconds that a user needs to wait between it's each message.
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default_thread_auto_archive_after
        if default_thread_auto_archive_after is ...:
            default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_slowmode
        if default_thread_slowmode is ...:
            default_thread_slowmode = SLOWMODE_DEFAULT
        else:
            default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = validate_nsfw(nsfw)
        
        # slowmode
        if slowmode is ...:
            slowmode = SLOWMODE_DEFAULT
        else:
            slowmode = validate_slowmode(slowmode)
        
        # topic
        if topic is ...:
            topic = None
        else:
            topic = validate_topic(topic)
        
        # Construct
        self = ChannelMetadataGuildMainBase.__new__(
            cls,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
        )
        self.default_thread_auto_archive_after = default_thread_auto_archive_after
        self.default_thread_slowmode = default_thread_slowmode
        self.nsfw = nsfw
        self.slowmode = slowmode
        self.topic = topic
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            name = keyword_parameters.pop('name', ...),
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after', ...),
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode', ...),
            nsfw = keyword_parameters.pop('nsfw', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
            topic = keyword_parameters.pop('topic', ...),
        )
    
    
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
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy)
    def copy(self):
        new = ChannelMetadataGuildMainBase.copy(self)
        new.default_thread_auto_archive_after = self.default_thread_auto_archive_after
        new.default_thread_slowmode = self.default_thread_slowmode
        new.nsfw = self.nsfw
        new.slowmode = self.slowmode
        new.topic = self.topic
        return new
    
    
    def copy_with(
        self,
        *,
        default_thread_auto_archive_after = ...,
        default_thread_slowmode = ...,
        name = ...,
        nsfw = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        slowmode = ...,
        topic = ...,
    ):
        """
        Copies the guild text base channel metadata with the given fields.
        
        Parameters
        ----------
        default_thread_auto_archive_after : `int``, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        default_thread_slowmode : `int`
            Applied as `thread.slowmode` when one is created.
        name : `str`, Optional (Keyword only)
            The channel's name.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        slowmode : `int`, Optional (Keyword only)
            The amount of time in seconds that a user needs to wait between it's each message.
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default_thread_auto_archive_after
        if default_thread_auto_archive_after is ...:
            default_thread_auto_archive_after = self.default_thread_auto_archive_after
        else:
            default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_slowmode
        if default_thread_slowmode is ...:
            default_thread_slowmode = self.default_thread_slowmode
        else:
            default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # nsfw
        if nsfw is ...:
            nsfw = self.nsfw
        else:
            nsfw = validate_nsfw(nsfw)
        
        # slowmode
        if slowmode is ...:
            slowmode = self.slowmode
        else:
            slowmode = validate_slowmode(slowmode)
        
        # topic
        if topic is ...:
            topic = self.topic
        else:
            topic = validate_topic(topic)
        
        # Construct
        new = ChannelMetadataGuildMainBase.copy_with(
            self,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
        )
        new.default_thread_auto_archive_after = default_thread_auto_archive_after
        new.default_thread_slowmode = default_thread_slowmode
        new.nsfw = nsfw
        new.slowmode = slowmode
        new.topic = topic
        return new
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            name = keyword_parameters.pop('name', ...),
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after', ...),
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode', ...),
            nsfw = keyword_parameters.pop('nsfw', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
            topic = keyword_parameters.pop('topic', ...),
        )
    
    
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
