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
        `manage_messages`, `manage_channels` permissions are unaffected.
    thread_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        The users inside of the thread if any.
    type : `int` = `12`
        The channel's Discord side type.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
    applied_tag_ids : `None`, `tuple` of `int`
         The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
    flags : ``ChannelFlag``
        The channel's flags.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('applied_tag_ids', 'flags',)
    
    
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
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildThreadBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # applied_tag_ids
        try:
            applied_tag_ids = keyword_parameters.pop('applied_tag_ids')
        except KeyError:
            pass
        else:
            self.applied_tag_ids = validate_applied_tag_ids(applied_tag_ids)
        
        # flags
        try:
            flags = keyword_parameters.pop('flags')
        except KeyError:
            pass
        else:
            self.flags = validate_flags(flags)
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildThreadBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # applied_tag_ids
        put_applied_tag_ids_into(self.applied_tag_ids, data, defaults)
        
        # flags
        put_flags_into(self.flags, data, defaults)
        
        return data
