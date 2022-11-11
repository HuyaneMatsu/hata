__all__ = ('ChannelMetadataGuildForum',)


from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_THREAD_AND_VOICE_DENY

from .constants import AUTO_ARCHIVE_DEFAULT, SLOWMODE_DEFAULT
from .fields import (
    parse_available_tags, parse_default_sort_order, parse_default_thread_auto_archive_after,
    parse_default_thread_reaction, parse_default_thread_slowmode, parse_flags, parse_topic, put_available_tags_into,
    put_default_sort_order_into, put_default_thread_auto_archive_after_into, put_default_thread_reaction_into,
    put_default_thread_slowmode_into, put_flags_into, put_topic_into, validate_available_tags,
    validate_default_sort_order, validate_default_thread_auto_archive_after, validate_default_thread_reaction,
    validate_default_thread_slowmode, validate_flags, validate_topic
)
from .flags import ChannelFlag
from .preinstanced import SortOrder

from .guild_main_base import ChannelMetadataGuildMainBase


class ChannelMetadataGuildForum(ChannelMetadataGuildMainBase):
    """
    Guild forum channel metadata.
    
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
    available_tags : `None`, `tuple` of ``ForumTag``
        The available tags to assign to the child-thread channels.
    default_sort_order : ``SortOrder``
        How the posts ordered in a forum channel by default.
    default_thread_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    default_thread_reaction : `None`, ``Emoji``
        The emoji to show in the add reaction button on a thread of the forum channel.
    default_thread_slowmode : `int`
        The default slowmode applied to the channel's threads.
    flags : ``ChannelFlag``
        The channel's flags.
    topic : `None`, `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = (
        'available_tags', 'default_sort_order', 'default_thread_auto_archive_after', 'default_thread_reaction',
        'default_thread_slowmode', 'flags', 'topic',
    )
    
    @copy_docs(ChannelMetadataGuildMainBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildMainBase.__hash__(self)
        
        # available_tags
        available_tags = self.available_tags
        if (available_tags is not None):
            hash_value ^= len(available_tags) << 4
            
            for available_tag in available_tags:
                hash_value ^= hash(available_tag)
        
        # default_sort_order
        hash_value ^= self.default_sort_order.value << 20
        
        # default_thread_auto_archive_after
        hash_value ^= self.default_thread_auto_archive_after << 16
        
        # default_thread_reaction
        default_thread_reaction = self.default_thread_reaction
        if (default_thread_reaction is not None):
            hash_value ^= hash(default_thread_reaction)
        
        # default_thread_slowmode
        hash_value ^= self.default_thread_slowmode << 8
        
        # flags
        hash_value ^= self.flags
        
        # topic
        topic = self.topic
        if (topic is not None):
            hash_value ^= hash(topic)
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildMainBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildMainBase._is_equal_same_type(self, other):
            return False
        
        # available_tags
        if self.available_tags != other.available_tags:
            return False
        
        # default_sort_order
        if self.default_sort_order is not other.default_sort_order:
            return False
        
        # default_thread_auto_archive_after
        if self.default_thread_auto_archive_after != other.default_thread_auto_archive_after:
            return False
        
        # default_thread_reaction
        if self.default_thread_reaction != other.default_thread_reaction:
            return False
        
        # default_thread_slowmode
        if self.default_thread_slowmode != other.default_thread_slowmode:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # topic
        if self.topic != other.topic:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_display_name)
    def _get_display_name(self):
        return self.name.upper()
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildForum, cls)._create_empty()
        
        self.available_tags = None
        self.default_sort_order = SortOrder.latest_activity
        self.default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.default_thread_reaction = None
        self.default_thread_slowmode = SLOWMODE_DEFAULT
        self.flags = ChannelFlag()
        self.topic = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        # available_tags
        self.available_tags = parse_available_tags(data)
        
        # default_sort_order
        self.default_sort_order = parse_default_sort_order(data)
        
        # default_thread_auto_archive_after
        self.default_thread_auto_archive_after = parse_default_thread_auto_archive_after(data)
        
        # default_thread_reaction
        self.default_thread_reaction = parse_default_thread_reaction(data)
        
        # default_thread_slowmode
        self.default_thread_slowmode = parse_default_thread_slowmode(data)
        
        # flags
        self.flags = parse_flags(data)
        
        # topic
        self.topic = parse_topic(data)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        # available_tags
        available_tags = parse_available_tags(data)
        if (self.available_tags != available_tags):
            old_attributes['available_tags'] = self.available_tags
            self.available_tags = available_tags
        
        # default_sort_order
        default_sort_order = parse_default_sort_order(data)
        if self.default_sort_order is not default_sort_order:
            old_attributes['default_sort_order'] = self.default_sort_order
            self.default_sort_order = default_sort_order
        
        # default_thread_auto_archive_after
        default_thread_auto_archive_after = parse_default_thread_auto_archive_after(data)
        if self.default_thread_auto_archive_after != default_thread_auto_archive_after:
            old_attributes['default_thread_auto_archive_after'] = self.default_thread_auto_archive_after
            self.default_thread_auto_archive_after = default_thread_auto_archive_after
        
        # default_thread_reaction
        default_thread_reaction = parse_default_thread_reaction(data)
        if self.default_thread_reaction != default_thread_reaction:
            old_attributes['default_thread_reaction'] = self.default_thread_reaction
            self.default_thread_reaction = default_thread_reaction
        
        # default_thread_slowmode
        default_thread_slowmode = parse_default_thread_slowmode(data)
        if self.default_thread_slowmode != default_thread_slowmode:
            old_attributes['default_thread_slowmode'] = self.default_thread_slowmode
            self.default_thread_slowmode = default_thread_slowmode
        
        # flags
        flags = parse_flags(data)
        if (self.flags != flags):
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        # topic
        topic = parse_topic(data)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # forum channels do not have thread and voice related permissions
        result &= PERMISSION_THREAD_AND_VOICE_DENY
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        # forum channels do not have thread and voice related permissions
        result &= PERMISSION_THREAD_AND_VOICE_DENY
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # available_tags
        try:
            available_tags = keyword_parameters.pop('available_tags')
        except KeyError:
            pass
        else:
            self.available_tags = validate_available_tags(available_tags)
        
        # default_sort_order
        try:
            default_sort_order = keyword_parameters.pop('default_sort_order')
        except KeyError:
            pass
        else:
            self.default_sort_order = validate_default_sort_order(default_sort_order)
        
        # default_thread_auto_archive_after
        try:
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after')
        except KeyError:
            pass
        else:
            self.default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_reaction
        try:
            default_thread_reaction = keyword_parameters.pop('default_thread_reaction')
        except KeyError:
            pass
        else:
            self.default_thread_reaction = validate_default_thread_reaction(default_thread_reaction)
        
        # default_thread_slowmode
        try:
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode')
        except KeyError:
            pass
        else:
            self.default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # flags
        try:
            flags = keyword_parameters.pop('flags')
        except KeyError:
            pass
        else:
            self.flags = validate_flags(flags)
        
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
        
        # available_tags
        put_available_tags_into(self.available_tags, data, defaults, include_internals = include_internals)
        
        # default_sort_order
        put_default_sort_order_into(self.default_sort_order, data, defaults)
        
        # default_auto_archive_duration
        put_default_thread_auto_archive_after_into(self.default_thread_auto_archive_after, data, defaults)
        
        # default_thread_reaction
        put_default_thread_reaction_into(self.default_thread_reaction, data, defaults)
        
        # default_thread_slowmode
        put_default_thread_slowmode_into(self.default_thread_slowmode, data, defaults)
        
        # flags
        put_flags_into(self.flags, data, defaults)
        
        # topic
        put_topic_into(self.topic, data, defaults)
        
        return data
