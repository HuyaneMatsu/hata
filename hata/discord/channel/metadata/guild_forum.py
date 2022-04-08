__all__ = ('ChannelMetadataGuildForum',)


from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_THREAD_AND_VOICE_DENY
from ...preconverters import preconvert_int, preconvert_int_options, preconvert_str

from .. import channel_types as CHANNEL_TYPES
from ..constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS

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
    default_auto_archive_after : `int`
        The default duration (in seconds) for newly created threads to automatically archive the themselves. Defaults
        to `3600`. Can be one of: `3600`, `86400`, `259200`, `604800`.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages`, `manage_channel` permissions are unaffected.
    topic : `None`, `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    type : `int` = `CHANNEL_TYPES.guild_forum`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('default_auto_archive_after', 'slowmode', 'topic',)
    
    type = CHANNEL_TYPES.guild_forum
    
    @copy_docs(ChannelMetadataGuildMainBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataGuildMainBase._compare_attributes_to(self, other):
            return False
        
        if self.default_auto_archive_after != other.default_auto_archive_after:
            return False
        
        if self.slowmode != other.slowmode:
            return False
        
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
        
        self.default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.slowmode = 0
        self.topic = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        default_auto_archive_after = data.get('default_auto_archive_duration', None)
        if default_auto_archive_after is None:
            default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_auto_archive_after *= 60
        self.default_auto_archive_after = default_auto_archive_after
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        self.slowmode = slowmode
        
        self.topic = data.get('topic', None)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        
        default_auto_archive_after = data.get('default_auto_archive_duration', None)
        if default_auto_archive_after is None:
            default_auto_archive_after = AUTO_ARCHIVE_DEFAULT
        else:
            default_auto_archive_after *= 60
        if self.default_auto_archive_after != default_auto_archive_after:
            old_attributes['default_auto_archive_after'] = self.default_auto_archive_after
            self.default_auto_archive_after = default_auto_archive_after
        
        
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        
        topic = data.get('topic', None)
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
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildForum, cls)._precreate(keyword_parameters)
        
        try:
            default_auto_archive_after = keyword_parameters.pop('default_auto_archive_duration')
        except KeyError:
            pass
        else:
            default_auto_archive_after = preconvert_int_options(
                default_auto_archive_after,
                'default_auto_archive_after',
                AUTO_ARCHIVE_OPTIONS,
            )
            
            self.default_auto_archive_after = default_auto_archive_after
        
        
        try:
            slowmode = keyword_parameters.pop('slowmode')
        except KeyError:
            pass
        else:
            slowmode = preconvert_int(slowmode, 'slowmode', 0, 21600)
            self.slowmode = slowmode
        
        
        try:
            topic = keyword_parameters.pop('topic')
        except KeyError:
            pass
        else:
            if (topic is not None):
                topic = preconvert_str(topic, 'topic', 0, 1024)
                if topic:
                    self.topic = topic
        
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildMainBase._to_data(self)
        
        # default_auto_archive_duration
        data['default_auto_archive_duration'] = self.default_auto_archive_after // 60
        
        # slowmode
        slowmode = self.slowmode
        if slowmode:
            data['rate_limit_per_user'] = slowmode
        
        # topic
        data['topic'] = self.topic
        
        return data
