__all__ = ('ChannelMetadataGuildForumBase',)

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_THREAD_AND_VOICE_DENY

from ..forum_tag import ForumTag
from ..forum_tag_change import ForumTagChange
from ..forum_tag_update import ForumTagUpdate

from .constants import AUTO_ARCHIVE_DEFAULT, SLOWMODE_DEFAULT
from .fields import (
    parse_available_tags, parse_default_forum_layout, parse_default_sort_order, parse_default_thread_auto_archive_after,
    parse_default_thread_reaction, parse_default_thread_slowmode, parse_flags, parse_topic, put_available_tags_into,
    put_default_forum_layout_into, put_default_sort_order_into, put_default_thread_auto_archive_after_into,
    put_default_thread_reaction_into, put_default_thread_slowmode_into, put_flags_into, put_topic_into,
    validate_available_tags, validate_default_forum_layout, validate_default_sort_order,
    validate_default_thread_auto_archive_after, validate_default_thread_reaction, validate_default_thread_slowmode,
    validate_flags, validate_topic
)
from .flags import ChannelFlag
from .guild_main_base import ChannelMetadataGuildMainBase
from .preinstanced import ForumLayout, SortOrder


class ChannelMetadataGuildForumBase(ChannelMetadataGuildMainBase):
    """
    Base type for guild forum-like channel metadatas.
    
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
    __slots__ = (
        'available_tags', 'default_forum_layout', 'default_sort_order', 'default_thread_auto_archive_after',
        'default_thread_reaction', 'default_thread_slowmode', 'flags', 'topic',
    )
    
    def __new__(
        cls,
        *,
        available_tags = ...,
        default_forum_layout = ...,
        default_sort_order = ...,
        default_thread_auto_archive_after = ...,
        default_thread_reaction = ...,
        default_thread_slowmode = ...,
        flags = ...,
        name = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        topic = ...,
    ):
        """
        Creates a new guild forum channel metadata from the given parameters.
        
        Parameters
        ----------
        available_tags : `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The available tags to assign to the child-thread channels.
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        flags : ``ChannelFlag``, `int`, Optional (Keyword only)
            The channel's flags.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # available_tags
        if available_tags is ...:
            available_tags = None
        else:
            available_tags = validate_available_tags(available_tags)
        
        # default_forum_layout
        if default_forum_layout is ...:
            default_forum_layout = ForumLayout.none
        else:
            default_forum_layout = validate_default_forum_layout(default_forum_layout)
        
        # default_sort_order
        if default_sort_order is ...:
            default_sort_order = SortOrder.latest_activity
        else:
            default_sort_order = validate_default_sort_order(default_sort_order)
        
        # default_thread_auto_archive_after
        if default_thread_auto_archive_after is ...:
            default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_reaction
        if default_thread_reaction is ...:
            default_thread_reaction = None
        else:
            default_thread_reaction = validate_default_thread_reaction(default_thread_reaction)
        
        # default_thread_slowmode
        if default_thread_slowmode is ...:
            default_thread_slowmode = SLOWMODE_DEFAULT
        else:
            default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # flags
        if flags is ...:
            flags = ChannelFlag()
        else:
            flags = validate_flags(flags)
        
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
        self.available_tags = available_tags
        self.default_forum_layout = default_forum_layout
        self.default_sort_order = default_sort_order
        self.default_thread_auto_archive_after = default_thread_auto_archive_after
        self.default_thread_reaction = default_thread_reaction
        self.default_thread_slowmode = default_thread_slowmode
        self.flags = flags
        self.topic = topic
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            available_tags = keyword_parameters.pop('available_tags', ...),
            default_forum_layout = keyword_parameters.pop('default_forum_layout', ...),
            default_sort_order = keyword_parameters.pop('default_sort_order', ...),
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after', ...),
            default_thread_reaction = keyword_parameters.pop('default_thread_reaction', ...),
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            topic = keyword_parameters.pop('topic', ...),
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
        
        # default_forum_layout
        hash_value ^= self.default_forum_layout.value << 24
        
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
        
        # default_forum_layout
        if self.default_forum_layout is not other.default_forum_layout:
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
        return self.name.lower()
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildForumBase, cls)._create_empty()
        
        self.available_tags = None
        self.default_forum_layout = ForumLayout.none
        self.default_sort_order = SortOrder.latest_activity
        self.default_thread_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.default_thread_reaction = None
        self.default_thread_slowmode = SLOWMODE_DEFAULT
        self.flags = ChannelFlag()
        self.topic = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy)
    def copy(self):
        new = ChannelMetadataGuildMainBase.copy(self)
        
        available_tags = self.available_tags
        if (available_tags is not None):
            available_tags = (*available_tags,)
        new.available_tags = available_tags
        
        new.default_forum_layout = self.default_forum_layout
        new.default_sort_order = self.default_sort_order
        new.default_thread_auto_archive_after = self.default_thread_auto_archive_after
        new.default_thread_reaction = self.default_thread_reaction
        new.default_thread_slowmode = self.default_thread_slowmode
        new.flags = self.flags
        new.topic = self.topic
        
        return new
    
    
    def copy_with(
        self,
        *,
        available_tags = ...,
        default_forum_layout = ...,
        default_sort_order = ...,
        default_thread_auto_archive_after = ...,
        default_thread_reaction = ...,
        default_thread_slowmode = ...,
        flags = ...,
        name = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        topic = ...,
    ):
        """
        Copies the guild forum channel metadata with the given fields.
        
        Parameters
        ----------
        available_tags : `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The available tags to assign to the child-thread channels.
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        flags : ``ChannelFlag``, `int`, Optional (Keyword only)
            The channel's flags.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # available_tags
        if available_tags is ...:
            available_tags = self.available_tags
            if (available_tags is not None):
                available_tags = (*available_tags,)
        else:
            available_tags = validate_available_tags(available_tags)
        
        # default_forum_layout
        if default_forum_layout is ...:
            default_forum_layout = self.default_forum_layout
        else:
            default_forum_layout = validate_default_forum_layout(default_forum_layout)
        
        # default_sort_order
        if default_sort_order is ...:
            default_sort_order = self.default_sort_order
        else:
            default_sort_order = validate_default_sort_order(default_sort_order)
        
        # default_thread_auto_archive_after
        if default_thread_auto_archive_after is ...:
            default_thread_auto_archive_after = self.default_thread_auto_archive_after
        else:
            default_thread_auto_archive_after = validate_default_thread_auto_archive_after(
                default_thread_auto_archive_after
            )
        
        # default_thread_reaction
        if default_thread_reaction is ...:
            default_thread_reaction = self.default_thread_reaction
        else:
            default_thread_reaction = validate_default_thread_reaction(default_thread_reaction)
        
        # default_thread_slowmode
        if default_thread_slowmode is ...:
            default_thread_slowmode = self.default_thread_slowmode
        else:
            default_thread_slowmode = validate_default_thread_slowmode(default_thread_slowmode)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
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
        new.available_tags = available_tags
        new.default_forum_layout = default_forum_layout
        new.default_sort_order = default_sort_order
        new.default_thread_auto_archive_after = default_thread_auto_archive_after
        new.default_thread_reaction = default_thread_reaction
        new.default_thread_slowmode = default_thread_slowmode
        new.flags = flags
        new.topic = topic
        return new
    
    
    @copy_docs(ChannelMetadataGuildMainBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            available_tags = keyword_parameters.pop('available_tags', ...),
            default_forum_layout = keyword_parameters.pop('default_forum_layout', ...),
            default_sort_order = keyword_parameters.pop('default_sort_order', ...),
            default_thread_auto_archive_after = keyword_parameters.pop('default_thread_auto_archive_after', ...),
            default_thread_reaction = keyword_parameters.pop('default_thread_reaction', ...),
            default_thread_slowmode = keyword_parameters.pop('default_thread_slowmode', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            topic = keyword_parameters.pop('topic', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        # available_tags
        self.available_tags = parse_available_tags(data)
        
        # default_forum_layout
        self.default_forum_layout = parse_default_forum_layout(data)
        
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
        forum_tag_change = self._difference_update_available_tags(data)
        if (forum_tag_change is not None):
            old_attributes['available_tags'] = forum_tag_change
        
        # default_forum_layout
        default_forum_layout = parse_default_forum_layout(data)
        if self.default_forum_layout is not default_forum_layout:
            old_attributes['default_forum_layout'] = self.default_forum_layout
            self.default_forum_layout = default_forum_layout
        
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
    
    
    def _difference_update_available_tags(self, data):
        """
        Updates the guild forum's available tags and returns a ``ForumTagChange`` instance if anything was modified.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Channel data.
        
        Returns
        -------
        forum_tag_change : `None`, ``ForumTagChange``
        """
        new_available_tag_datas = data.get('available_tags', None)
        if (new_available_tag_datas is not None) and (not new_available_tag_datas):
            new_available_tag_datas = None
        
        old_available_tags = self.available_tags
        if (old_available_tags is None) and (new_available_tag_datas is None):
            return None
        
        
        old_forum_tags = set()
        if (old_available_tags is not None):
            old_forum_tags.update(old_available_tags)
        
        new_forum_tags = set()
        
        # Update
        updated_forum_tags = None
        
        if (new_available_tag_datas is not None):
            for forum_tag_data in new_available_tag_datas:
                forum_tag, old_attributes = ForumTag._create_or_difference_update(forum_tag_data)
                if (old_attributes is not None) and old_attributes:
                    if (updated_forum_tags is None):
                        updated_forum_tags = []
                    
                    updated_forum_tags.append(ForumTagUpdate.from_fields(forum_tag, old_attributes))
                
                new_forum_tags.add(forum_tag)
                continue
        
        # Added
        added_forum_tags = old_forum_tags - new_forum_tags
        if added_forum_tags:
            added_forum_tags = sorted(added_forum_tags)
        else:
            added_forum_tags = None
        
        # Removed
        removed_forum_tags = new_forum_tags - old_forum_tags
        if removed_forum_tags:
            removed_forum_tags = sorted(removed_forum_tags)
        else:
            removed_forum_tags = None
        
        # Set new
        if new_forum_tags:
            new_available_tags = tuple(sorted(new_forum_tags))
        else:
            new_available_tags = None
        self.available_tags = new_available_tags
        
        # Construct
        if (added_forum_tags is None) and (removed_forum_tags is None) and (updated_forum_tags is None):
            return
        
        return ForumTagChange.from_fields(added_forum_tags, updated_forum_tags, removed_forum_tags)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._iter_delete)
    def _iter_delete(self, channel_entity, client):
        for thread in channel_entity.threads:
            thread._delete(client)
            yield thread
        
        yield from ChannelMetadataGuildMainBase._iter_delete(self, channel_entity, client)
    
    
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
    
    
    @copy_docs(ChannelMetadataGuildMainBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildMainBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # available_tags
        put_available_tags_into(self.available_tags, data, defaults, include_internals = include_internals)
        
        # default_forum_layout
        put_default_forum_layout_into(self.default_forum_layout, data, defaults)
        
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
