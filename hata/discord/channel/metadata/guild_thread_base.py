__all__ = ('ChannelMetadataGuildThreadBase', )

from datetime import datetime

from scarletio import copy_docs

from ...core import CHANNELS, GUILDS
from ...permission.permission import PERMISSION_NONE
from ...preconverters import preconvert_bool, preconvert_int, preconvert_int_options
from ...utils import datetime_to_timestamp, id_to_datetime, timestamp_to_datetime

from ..constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS

from .guild_base import ChannelMetadataGuildBase


class ChannelMetadataGuildThreadBase(ChannelMetadataGuildBase):
    """
    Base guild channel metadata type.
    
    Attributes
    ----------
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `int`
        The channel's parent's identifier.
    name : `str`
        The channel's name.
    _created_at : `None`, `datetime`
        When the channel was created.
    archived : `bool`
        Whether the thread s archived.
    archived_at : `None`, `datetime`
        When the thread's archive status was last changed.
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    open : `bool`
        Whether the thread channel is open.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages`, `manage_channel` permissions are unaffected.
    thread_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        The users inside of the thread if any.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
    
    Class Attributes
    ----------------
    type : `int` = `-1`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = (
        '_created_at', 'archived', 'archived_at', 'auto_archive_after', 'open', 'owner_id', 'slowmode', 'thread_users'
    )
    
    @copy_docs(ChannelMetadataGuildBase.__new__)
    def __new__(cls, data):
        self = ChannelMetadataGuildBase.__new__(cls, data)
        
        owner_id = data.get('owner_id', None)
        if owner_id is None:
            owner_id = 0
        else:
            owner_id = int(owner_id)
        self.owner_id = owner_id
        
        created_at = data.get('create_timestamp', None)
        if (created_at is not None):
            created_at = timestamp_to_datetime(created_at)
        self._created_at = created_at
        
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent_id = 0
        else:
            parent_id = int(parent_id)
        self.parent_id = parent_id
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildBase._created)
    def _created(self, channel_entity, client):
        try:
            guild = GUILDS[channel_entity.guild_id]
        except KeyError:
            pass
        else:
            guild.threads[channel_entity.id] = channel_entity
    
    
    @copy_docs(ChannelMetadataGuildBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataGuildBase._compare_attributes_to(self, other):
            return False
        
        if self._created_at != other._created_at:
            return False
        
        if self.archived != other.archived:
            return False
        
        if self.archived_at != other.archived_at:
            return False
        
        if self.auto_archive_after != other.auto_archive_after:
            return False
        
        if self.open != other.open:
            return False
        
        if self.owner_id != other.owner_id:
            return False
        
        if self.slowmode != other.slowmode:
            return False
        
        # Ignoring `thread_users`
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildThreadBase, cls)._create_empty()
        
        self._created_at = None
        self.archived = False
        self.archived_at = None
        self.auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.open = False
        self.owner_id = 0
        self.slowmode = 0
        self.thread_users = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildBase._get_display_name)
    def _get_display_name(self):
        return self.name.lower()
    
    
    @copy_docs(ChannelMetadataGuildBase._get_created_at)
    def _get_created_at(self, channel_entity):
        created_at = self._created_at
        if (created_at is None):
            created_at = id_to_datetime(channel_entity.id)
        
        return created_at
    
    
    @property
    @copy_docs(ChannelMetadataGuildBase._get_users)
    def _get_users(self, channel_entity):
        thread_users = self.thread_users
        if thread_users is None:
            users = []
        else:
            users = list(thread_users.values())
        
        return users
    
    
    @copy_docs(ChannelMetadataGuildBase._iter_users)
    def _iter_users(self):
        thread_users = self.thread_users
        if (thread_users is not None):
            yield from thread_users.values()
    
    
    @copy_docs(ChannelMetadataGuildBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildBase._update_attributes(self, data)
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        self.slowmode = slowmode
        
        # Move to sub data
        data = data['thread_metadata']
        
        self.archived = data.get('archived', False)
        
        
        self.auto_archive_after = data['auto_archive_duration'] * 60
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = timestamp_to_datetime(archived_at_data)
        self.archived_at = archived_at
        
        self.open = not data.get('locked', True)
    
    
    @copy_docs(ChannelMetadataGuildBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildBase._difference_update_attributes(self, data)
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        
        # Move to sub data
        data = data['thread_metadata']
        
        
        archived = data.get('archived', False)
        if (self.archived != archived):
            old_attributes['archived'] = self.archived
            self.archived = archived
        
        
        auto_archive_after = data['auto_archive_duration']*60
        if (self.auto_archive_after != auto_archive_after):
            old_attributes['auto_archive_after'] = self.auto_archive_after
            self.auto_archive_after = auto_archive_after
        
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = timestamp_to_datetime(archived_at_data)
        if (self.archived_at != archived_at):
            old_attributes['archived_at'] = self.archived_at
            self.archived_at = archived_at
        
        open_ = not data.get('locked', True)
        if (self.open != open_):
            old_attributes['open'] = self.open
            self.open = open_
        
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
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildThreadBase, cls)._precreate(keyword_parameters)
    
        try:
            slowmode = keyword_parameters.pop('slowmode')
        except KeyError:
            pass
        else:
            slowmode = preconvert_int(slowmode, 'slowmode', 0, 21600)
            self.slowmode = slowmode
        
        
        try:
            auto_archive_after = keyword_parameters.pop('auto_archive_after')
        except KeyError:
            pass
        else:
            auto_archive_after = preconvert_int_options(
                auto_archive_after,
                'auto_archive_after',
                AUTO_ARCHIVE_OPTIONS,
            )
            
            self.auto_archive_after = auto_archive_after
        
        
        try:
            created_at = keyword_parameters.pop('created_at')
        except KeyError:
            pass
        else:
            if (created_at is not None):
                if not isinstance(created_at, datetime):
                    raise TypeError(
                        f'`created_at` can be `None`, `datetime`, got {created_at.__class__.__name__}; '
                        f'{created_at!r}.'
                    )
                
                self._created_at = created_at
        
        try:
            open_ = keyword_parameters.pop('open')
        except KeyError:
            pass
        else:
            open_ = preconvert_bool(open_, 'open')
            self.open_ = open_
        
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildBase._to_data(self)
        
        slowmode = self.slowmode
        if slowmode:
            data['rate_limit_per_user'] = slowmode
        
        owner_id = self.owner_id
        if owner_id:
            data['owner_id'] = str(owner_id)
        
        thread_data = {}
        data['thread_metadata'] = thread_data
        
        thread_data['archived'] = self.archived
        
        thread_data['auto_archive_duration'] = self.auto_archive_after // 60
        
        archive_timestamp = self.archive_timestamp
        if (archive_timestamp is not None):
            archive_timestamp = datetime_to_timestamp(archive_timestamp)
        thread_data['archive_timestamp'] = archive_timestamp
        
        thread_data['locked'] = not self.open
        
        created_at = self._created_at
        if (created_at is not None):
            data['create_timestamp'] = datetime_to_timestamp(created_at)
        
        return data
