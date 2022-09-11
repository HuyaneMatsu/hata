__all__ = ('ChannelMetadataGuildThreadPublic',)

from scarletio import copy_docs

from ...preconverters import preconvert_flag, preconvert_snowflake_array

from ..flags import ChannelFlag

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
        `manage_messages`, `manage_channel` permissions are unaffected.
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
        applied_tag_id_array = data.get('applied_tags', None)
        if (applied_tag_id_array is None) or (not applied_tag_id_array):
            applied_tag_ids = None
        else:
            applied_tag_ids = tuple(sorted(int(tag_id) for tag_id in applied_tag_id_array))
        self.applied_tag_ids = applied_tag_ids
        
        # flags
        self.flags = ChannelFlag(data.get('flags', 0))
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildThreadBase._difference_update_attributes(self, data)
        
        # applied_tag_ids
        applied_tag_id_array = data.get('applied_tags', None)
        if (applied_tag_id_array is None) or (not applied_tag_id_array):
            applied_tag_ids = None
        else:
            applied_tag_ids = tuple(sorted(int(tag_id) for tag_id in applied_tag_id_array))
        if (self.applied_tag_ids != applied_tag_ids):
            old_attributes['applied_tag_ids'] = self.applied_tag_ids
            self.applied_tag_ids = applied_tag_ids
        
        # flags
        flags = data.get('flags', 0)
        if (self.flags != flags):
            flags = ChannelFlag(flags)
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        return old_attributes
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildThreadPublic, cls)._precreate(keyword_parameters)
        
        # applied_tag_ids
        try:
            applied_tag_ids = keyword_parameters.pop('applied_tag_ids')
        except KeyError:
            pass
        else:
            applied_tag_ids = preconvert_snowflake_array(applied_tag_ids, 'applied_tag_ids')
            self.applied_tag_ids = applied_tag_ids
        
        # flags
        try:
            flags = keyword_parameters.pop('flags')
        except KeyError:
            pass
        else:
            flags = preconvert_flag(flags, 'flags', ChannelFlag)
            self.flags = flags
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildThreadBase._to_data(self)
        
        # applied_tag_ids
        applied_tag_ids = self.applied_tag_ids
        if applied_tag_ids is None:
            applied_tag_id_array = []
        else:
            applied_tag_id_array = [str(tag_id) for tag_id in applied_tag_ids]
        data['applied_tag_ids'] = applied_tag_id_array
        
        # flags
        data['flags'] = self.flags
        
        return data
