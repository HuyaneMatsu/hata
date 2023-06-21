__all__ = ('ChannelMetadataGuildThreadPrivate',)

from scarletio import copy_docs

from .fields import parse_invitable, put_invitable_into, validate_invitable

from .guild_thread_base import ChannelMetadataGuildThreadBase


class ChannelMetadataGuildThreadPrivate(ChannelMetadataGuildThreadBase):
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
    invitable : `bool`
        Whether non-moderators can invite other non-moderators to the threads.
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
    __slots__ = ('invitable',)
    
    
    def __new__(
        cls,
        *,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        created_at = ...,
        invitable = ...,
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
        archived : `bool`, Optional (Keyword only)
            Whether the thread is archived.
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        auto_archive_after : `int`, Optional (Keyword only)
            Duration in seconds to automatically archive the thread after recent activity.
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
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
        # invitable
        if invitable is ...:
            invitable = True
        else:
            invitable = validate_invitable(invitable)
        
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
        self.invitable = invitable
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            invitable = keyword_parameters.pop('invitable', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildThreadBase.__hash__(self)
        
        # invitable
        hash_value ^= self.invitable << 9
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildThreadBase._is_equal_same_type(self, other):
            return False
        
        # invitable
        if self.invitable != other.invitable:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildThreadPrivate, cls)._create_empty()
        
        self.invitable = True
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.copy)
    def copy(self):
        new = ChannelMetadataGuildThreadBase.copy(self)
        new.invitable = self.invitable
        return new
    
    
    def copy_with(
        self,
        *,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        created_at = ...,
        invitable = ...,
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
        archived : `bool`, Optional (Keyword only)
            Whether the thread is archived.
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        auto_archive_after : `int`, Optional (Keyword only)
            Duration in seconds to automatically archive the thread after recent activity.
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
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
        # invitable
        if invitable is ...:
            invitable = self.invitable
        else:
            invitable = validate_invitable(invitable)
        
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
        new.invitable = invitable
        return new
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            invitable = keyword_parameters.pop('invitable', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildThreadBase._update_attributes(self, data)
        
        # invitable
        self.invitable = parse_invitable(data)
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildThreadBase._difference_update_attributes(self, data)
        
        # invitable
        invitable = parse_invitable(data)
        if (self.invitable != invitable):
            old_attributes['invitable'] = self.invitable
            self.invitable = invitable
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildThreadBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # invitable
        put_invitable_into(self.invitable, data, defaults, flatten_thread_metadata = not include_internals)
        
        return data
