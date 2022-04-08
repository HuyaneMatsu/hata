__all__ = ('ChannelMetadataGuildThreadPrivate',)

from scarletio import copy_docs

from ...preconverters import preconvert_bool

from .. import channel_types as CHANNEL_TYPES

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
        `manage_messages`, `manage_channel` permissions are unaffected.
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
    type : `int` = `CHANNEL_TYPES.guild_thread_private`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('invitable',)
    
    type = CHANNEL_TYPES.guild_thread_private
    
    @copy_docs(ChannelMetadataGuildThreadBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataGuildThreadBase._compare_attributes_to(self, other):
            return False
        
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
        
        self.invitable = data.get('invitable', True)
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildThreadBase._difference_update_attributes(self, data)
        
        invitable = data.get('invitable', True)
        if (self.invitable != invitable):
            old_attributes['invitable'] = self.invitable
            self.invitable = invitable
        
        return old_attributes
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildThreadBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildThreadPrivate, cls)._precreate(keyword_parameters)
        
        try:
            invitable = keyword_parameters.pop('invitable')
        except KeyError:
            pass
        else:
            invitable = preconvert_bool(invitable, 'invitable')
            self.invitable = invitable
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildThreadBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildThreadBase._to_data(self)
        
        data['thread_metadata']['invitable'] = self.invitable
        
        return data
