__all__ = ('ChannelMetadataGuildThreadPublic',)

from scarletio import copy_docs

from .fields import (
    parse_applied_tag_ids, parse_flags, put_applied_tag_ids_into, put_flags_into, validate_applied_tag_ids,
    validate_flags
)
from .flags import ChannelFlag

from .guild_thread_base import ChannelMetadataGuildThreadBase


class ChannelMetadataGuildThreadPublic(ChannelMetadataGuildThreadBase):
    """
    Base guild channel metadata type.
    
    Attributes
    ----------
    _created_at : `None`, `datetime`
        When the channel was created.
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    applied_tag_ids : `None`, `tuple` of `int`
         The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
    archived : `bool`
        Whether the thread s archived.
    archived_at : `None`, `datetime`
        When the thread's archive status was last changed.
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    flags : ``ChannelFlag``
        The channel's flags.
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
    __slots__ = ('applied_tag_ids', 'flags',)
    
    
    def __new__(
        cls,
        *,
        applied_tag_ids = ...,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        flags = ...,
        created_at = ...,
        name = ...,
        parent_id = ...,
        open = ...,
        owner_id = ...,
        slowmode = ...,
    ):
        """
        Creates a new guild public thread channel metadata from the given parameters.
        
        Parameters
        ----------
        applied_tag_ids : `None`, `iterable` of (`int`, ``ForumTag``), Optional (Keyword only)
             The tags' identifier which have been applied to the thread.
        archived : `bool`, Optional (Keyword only)
            Whether the thread is archived.
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        auto_archive_after : `int`, Optional (Keyword only)
            Duration in seconds to automatically archive the thread after recent activity.
        flags : ``ChannelFlag``, `int`, Optional (Keyword only)
            The channel's flags.
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        open : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The channel's creator's identifier.
        slowmode : `int`, Optional (Keyword only)
            The amount of time in seconds what a user needs to wait between it's each message.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # applied_tag_ids
        if applied_tag_ids is ...:
            applied_tag_ids = None
        else:
            applied_tag_ids = validate_applied_tag_ids(applied_tag_ids)
        
        # flags
        if flags is ...:
            flags = ChannelFlag()
        else:
            flags = validate_flags(flags)
        
        # Construct
        self = ChannelMetadataGuildThreadBase.__new__(
            cls,
            archived = archived,
            archived_at = archived_at,
            auto_archive_after = auto_archive_after,
            created_at = created_at,
            name = name,
            open = open,
            owner_id = owner_id,
            parent_id = parent_id,
            slowmode = slowmode,
        )
        self.applied_tag_ids = applied_tag_ids
        self.flags = flags
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            applied_tag_ids = keyword_parameters.pop('applied_tag_ids', ...),
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            flags = keyword_parameters.pop('flags', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildThreadBase._is_equal_same_type(self, other):
            return False
        
        # applied_tag_ids
        if self.applied_tag_ids != other.applied_tag_ids:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildThreadPublic, cls)._create_empty()
        
        # applied_tag_ids
        self.applied_tag_ids = None
        
        # flags
        self.flags = ChannelFlag()
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.copy)
    def copy(self):
        new = ChannelMetadataGuildThreadBase.copy(self)
        
        applied_tag_ids = self.applied_tag_ids
        if (applied_tag_ids is not None):
            applied_tag_ids = (*applied_tag_ids,)
        new.applied_tag_ids = applied_tag_ids
        
        new.flags = self.flags
        
        return new
    
    
    def copy_with(
        self,
        *,
        applied_tag_ids = ...,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        flags = ...,
        created_at = ...,
        name = ...,
        parent_id = ...,
        open = ...,
        owner_id = ...,
        slowmode = ...,
    ):
        """
        Copies the guild public thread channel metadata with the given fields.
        
        Parameters
        ----------
        applied_tag_ids : `None`, `iterable` of (`int`, ``ForumTag``), Optional (Keyword only)
             The tags' identifier which have been applied to the thread.
        archived : `bool`, Optional (Keyword only)
            Whether the thread is archived.
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        auto_archive_after : `int`, Optional (Keyword only)
            Duration in seconds to automatically archive the thread after recent activity.
        flags : ``ChannelFlag``, `int`, Optional (Keyword only)
            The channel's flags.
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        open : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The channel's creator's identifier.
        slowmode : `int`, Optional (Keyword only)
            The amount of time in seconds what a user needs to wait between it's each message.
        
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
        # applied_tag_ids
        if applied_tag_ids is ...:
            applied_tag_ids = self.applied_tag_ids
            if (applied_tag_ids is not None):
                applied_tag_ids = (*applied_tag_ids,)
        else:
            applied_tag_ids = validate_applied_tag_ids(applied_tag_ids)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # Construct
        new = ChannelMetadataGuildThreadBase.copy_with(
            self,
            archived = archived,
            archived_at = archived_at,
            auto_archive_after = auto_archive_after,
            created_at = created_at,
            name = name,
            open = open,
            owner_id = owner_id,
            parent_id = parent_id,
            slowmode = slowmode,
        )
        new.applied_tag_ids = applied_tag_ids
        new.flags = flags
        return new
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            applied_tag_ids = keyword_parameters.pop('applied_tag_ids', ...),
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            flags = keyword_parameters.pop('flags', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildThreadBase._update_attributes(self, data)
        
        # applied_tag_ids
        self.applied_tag_ids = parse_applied_tag_ids(data)
        
        # flags
        self.flags = parse_flags(data)
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildThreadBase._difference_update_attributes(self, data)
        
        # applied_tag_ids
        applied_tag_ids = parse_applied_tag_ids(data)
        if (self.applied_tag_ids != applied_tag_ids):
            old_attributes['applied_tag_ids'] = self.applied_tag_ids
            self.applied_tag_ids = applied_tag_ids
        
        # flags
        flags = parse_flags(data)
        if (self.flags != flags):
            flags = ChannelFlag(flags)
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildThreadBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # applied_tag_ids
        put_applied_tag_ids_into(self.applied_tag_ids, data, defaults)
        
        # flags
        put_flags_into(self.flags, data, defaults)
        
        return data
