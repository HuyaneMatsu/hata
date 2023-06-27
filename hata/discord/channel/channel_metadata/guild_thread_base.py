__all__ = ('ChannelMetadataGuildThreadBase', )

from scarletio import copy_docs

from ...core import CHANNELS, GUILDS
from ...permission.permission import PERMISSION_NONE
from ...utils import id_to_datetime

from .constants import AUTO_ARCHIVE_DEFAULT, SLOWMODE_DEFAULT
from .fields import (
    parse_archived, parse_archived_at, parse_auto_archive_after, parse_created_at, parse_open, parse_owner_id,
    parse_slowmode, put_archived_at_into, put_archived_into, put_auto_archive_after_into, put_created_at_into,
    put_open_into, put_owner_id_into, put_slowmode_into, validate_archived, validate_archived_at,
    validate_auto_archive_after, validate_created_at, validate_open, validate_owner_id, validate_slowmode
)

from .guild_base import ChannelMetadataGuildBase


class ChannelMetadataGuildThreadBase(ChannelMetadataGuildBase):
    """
    Base guild channel metadata type.
    
    Attributes
    ----------
    _created_at : `None`, `datetime`
        When the channel was created.
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    archived : `bool`
        Whether the thread is archived.
    archived_at : `None`, `datetime`
        When the thread's archive status was last changed.
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    name : `str`
        The channel's name.
    parent_id : `int`
        The channel's parent's identifier.
    open : `bool`
        Whether the thread channel is open.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
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
    __slots__ = (
        '_created_at', 'archived', 'archived_at', 'auto_archive_after', 'open', 'owner_id', 'slowmode', 'thread_users'
    )
    
    
    def __new__(
        cls,
        *,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        created_at = ...,
        name = ...,
        parent_id = ...,
        open = ...,
        owner_id = ...,
        slowmode = ...,
    ):
        """
        Creates a new guild thread base channel metadata from the given parameters.
        
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
        # archived
        if archived is ...:
            archived = False
        else:
            archived = validate_archived(archived)
        
        # archived_at
        if archived_at is ...:
            archived_at = None
        else:
            archived_at = validate_archived_at(archived_at)
        
        # auto_archive_after
        if auto_archive_after is ...:
            auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            auto_archive_after = validate_auto_archive_after(auto_archive_after)
        
        # created_at
        if created_at is ...:
            created_at = None
        else:
            created_at = validate_created_at(created_at)
        
        # open
        if open is ...:
            open = True
        else:
            open = validate_open(open)
        
        # owner_id
        if owner_id is ...:
            owner_id = 0
        else:
            owner_id = validate_owner_id(owner_id)
        
        # slowmode
        if slowmode is ...:
            slowmode = SLOWMODE_DEFAULT
        else:
            slowmode = validate_slowmode(slowmode)
        
        # Construct
        self = ChannelMetadataGuildBase.__new__(
            cls,
            name = name,
            parent_id = parent_id,
        )
        self._created_at = created_at
        self.archived = archived
        self.archived_at = archived_at
        self.auto_archive_after = auto_archive_after
        self.open = open
        self.owner_id = owner_id
        self.slowmode = slowmode
        self.thread_users = None
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildBase.__hash__(self)
        
        # created_at
        created_at = self._created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # archived
        hash_value ^= self.archived << 5
        
        # archived_at
        hash_value ^= hash(self.archived_at)
        
        # open
        hash_value ^= self.open << 7
        
        # owner_id
        hash_value ^= self.owner_id
        
        # slowmode
        hash_value ^= self.slowmode << 4
        
        return hash_value
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildBase.from_data)
    def from_data(cls, data):
        self = super(ChannelMetadataGuildThreadBase, cls).from_data(data)

        # created_at
        self._created_at = parse_created_at(data)
        
        # owner_id
        self.owner_id = parse_owner_id(data)
        
        # thread_users
        self.thread_users = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildBase._created)
    def _created(self, channel_entity, client, strong_cache):
        if strong_cache:
            try:
                guild = GUILDS[channel_entity.guild_id]
            except KeyError:
                pass
            else:
                guild.threads[channel_entity.id] = channel_entity
    
    
    @copy_docs(ChannelMetadataGuildBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildBase._is_equal_same_type(self, other):
            return False
        
        # archived
        if self.archived != other.archived:
            return False
        
        # archived_at
        if self.archived_at != other.archived_at:
            return False
        
        # auto_archive_after
        if self.auto_archive_after != other.auto_archive_after:
            return False
        
        # created_at
        if self._created_at != other._created_at:
            return False
        
        # open
        if self.open != other.open:
            return False
        
        # owner_id
        if self.owner_id != other.owner_id:
            return False
        
        # slowmode
        if self.slowmode != other.slowmode:
            return False
        
        # thread_users
        # Ignore this field
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildThreadBase, cls)._create_empty()
        
        self._created_at = None
        self.archived = False
        self.archived_at = None
        self.auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.open = True
        self.owner_id = 0
        self.slowmode = SLOWMODE_DEFAULT
        self.thread_users = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildBase.copy)
    def copy(self):
        new = ChannelMetadataGuildBase.copy(self)
        new._created_at = self._created_at
        new.archived = self.archived
        new.archived_at = self.archived_at
        new.auto_archive_after = self.auto_archive_after
        new.open = self.open
        new.owner_id = self.owner_id
        new.slowmode = self.slowmode
        new.thread_users = None
        return new
    
    
    def copy_with(
        self,
        *,
        archived = ...,
        archived_at = ...,
        auto_archive_after = ...,
        created_at = ...,
        name = ...,
        parent_id = ...,
        open = ...,
        owner_id = ...,
        slowmode = ...,
    ):
        """
        Copies the guild thread base channel metadata with the given fields.
        
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
        # archived
        if archived is ...:
            archived = self.archived
        else:
            archived = validate_archived(archived)
        
        # archived_at
        if archived_at is ...:
            archived_at = self.archived_at
        else:
            archived_at = validate_archived_at(archived_at)
        
        # auto_archive_after
        if auto_archive_after is ...:
            auto_archive_after = self.auto_archive_after
        else:
            auto_archive_after = validate_auto_archive_after(auto_archive_after)
        
        # created_at
        if created_at is ...:
            created_at = self._created_at
        else:
            created_at = validate_created_at(created_at)
        
        # open
        if open is ...:
            open = self.open
        else:
            open = validate_open(open)
        
        # owner_id
        if owner_id is ...:
            owner_id = self.owner_id
        else:
            owner_id = validate_owner_id(owner_id)
        
        # slowmode
        if slowmode is ...:
            slowmode = self.slowmode
        else:
            slowmode = validate_slowmode(slowmode)
        
        # Construct
        new = ChannelMetadataGuildBase.copy_with(
            self,
            name = name,
            parent_id = parent_id,
        )
        new._created_at = created_at
        new.archived = archived
        new.archived_at = archived_at
        new.auto_archive_after = auto_archive_after
        new.open = open
        new.owner_id = owner_id
        new.slowmode = slowmode
        new.thread_users = None
        return new
    
    
    @copy_docs(ChannelMetadataGuildBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            archived = keyword_parameters.pop('archived', ...),
            archived_at = keyword_parameters.pop('archived_at', ...),
            auto_archive_after = keyword_parameters.pop('auto_archive_after', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            open = keyword_parameters.pop('open', ...),
            owner_id = keyword_parameters.pop('owner_id', ...),
            slowmode = keyword_parameters.pop('slowmode', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildBase._get_created_at)
    def _get_created_at(self, channel_entity):
        created_at = self._created_at
        if (created_at is None):
            created_at = id_to_datetime(channel_entity.id)
        
        return created_at
    
    
    @copy_docs(ChannelMetadataGuildBase._get_users)
    def _get_users(self, channel_entity):
        thread_users = self.thread_users
        if thread_users is None:
            users = []
        else:
            users = list(thread_users.values())
        
        return users
    
    
    @copy_docs(ChannelMetadataGuildBase._iter_users)
    def _iter_users(self, channel_entity):
        thread_users = self.thread_users
        if (thread_users is not None):
            yield from thread_users.values()
    
    
    @copy_docs(ChannelMetadataGuildBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildBase._update_attributes(self, data)
        
        # archived
        self.archived = parse_archived(data)
        
        # archived_at
        self.archived_at = parse_archived_at(data)
        
        # auto_archive_after
        self.auto_archive_after = parse_auto_archive_after(data)
        
        # open
        self.open = parse_open(data)
        
        # slowmode
        self.slowmode = parse_slowmode(data)
    
    
    @copy_docs(ChannelMetadataGuildBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildBase._difference_update_attributes(self, data)
        
        # archived
        archived = parse_archived(data)
        if (self.archived != archived):
            old_attributes['archived'] = self.archived
            self.archived = archived
        
        # archived_at
        archived_at = parse_archived_at(data)
        if (self.archived_at != archived_at):
            old_attributes['archived_at'] = self.archived_at
            self.archived_at = archived_at
        
        # auto_archive_after
        auto_archive_after = parse_auto_archive_after(data)
        if (self.auto_archive_after != auto_archive_after):
            old_attributes['auto_archive_after'] = self.auto_archive_after
            self.auto_archive_after = auto_archive_after
        
        # open
        open_ = parse_open(data)
        if (self.open != open_):
            old_attributes['open'] = self.open
            self.open = open_
        
        # slowmode
        slowmode = parse_slowmode(data)
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildBase._delete)
    def _delete(self, channel_entity, client):
        guild_id = channel_entity.guild_id
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            try:
                del guild.threads[channel_entity.id]
            except KeyError:
                pass
        
        thread_users = self.thread_users
        if (thread_users is not None):
            self.thread_users = None
            channel_id = channel_entity.id
            for user in thread_users.values():
                thread_profiles = user.thread_profiles
                if (thread_profiles is not None):
                    try:
                        del thread_profiles[channel_id]
                    except KeyError:
                        pass
                    else:
                        if (not thread_profiles):
                            user.thread_profiles = None
    
    
    @copy_docs(ChannelMetadataGuildBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        try:
            parent = CHANNELS[self.parent_id]
        except KeyError:
            return PERMISSION_NONE
        
        return parent.permissions_for(user)
    
    
    @copy_docs(ChannelMetadataGuildBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        try:
            parent = CHANNELS[self.parent_id]
        except KeyError:
            return PERMISSION_NONE
        
        return parent.permissions_for_roles(*roles)
    
    
    @copy_docs(ChannelMetadataGuildBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # archived
        if include_internals:
            put_archived_into(self.archived, data, defaults)
        
        # archived_at
        if include_internals:
            put_archived_at_into(self.archived_at, data, defaults)
        
        # auto_archive_after
        put_auto_archive_after_into(
            self.auto_archive_after, data, defaults, flatten_thread_metadata = not include_internals
        )
        
        # created_at
        if include_internals:
            put_created_at_into(self._created_at, data, defaults)
        
        # open
        put_open_into(self.open, data, defaults, flatten_thread_metadata = not include_internals)
        
        # owner_id
        if include_internals:
            put_owner_id_into(self.owner_id, data, defaults)
        
        # slowmode
        put_slowmode_into(self.slowmode, data, defaults)
        
        return data
