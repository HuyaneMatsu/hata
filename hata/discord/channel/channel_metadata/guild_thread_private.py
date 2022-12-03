__all__ = ('ChannelMetadataGuildThreadPrivate',)

from scarletio import copy_docs

from .fields import parse_invitable, put_invitable_into, validate_invitable

from .guild_thread_base import ChannelMetadataGuildThreadBase


class ChannelMetadataGuildThreadPrivate(ChannelMetadataGuildThreadBase):
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
    invitable : `bool`
        Whether non-moderators can invite other non-moderators to the threads.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('invitable',)
    
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
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildThreadBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # invitable
        try:
            invitable = keyword_parameters.pop('invitable')
        except KeyError:
            pass
        else:
            self.invitable = validate_invitable(invitable)
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildThreadBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildThreadBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # invitable
        put_invitable_into(self.invitable, data, defaults, flatten_thread_metadata = not include_internals)
        
        return data
