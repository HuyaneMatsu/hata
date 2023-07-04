__all__ = ('ChannelMetadataGuildStage',)

from scarletio import copy_docs

from ...permission import Permission
from ...permission.permission import (
    PERMISSION_MASK_CONNECT, PERMISSION_MASK_VIEW_CHANNEL, PERMISSION_NONE, PERMISSION_TEXT_DENY,
    PERMISSION_VOICE_DENY_CONNECTION
)

from .fields import parse_topic, put_topic_into, validate_topic

from .guild_voice_base import ChannelMetadataGuildVoiceBase


class ChannelMetadataGuildStage(ChannelMetadataGuildVoiceBase):
    """
    Guild voice channel metadata.
    
    Attributes
    ----------
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    name : `str`
        The channel's name.
    parent_id : `int`
        The channel's parent's identifier.
    permission_overwrites :`None`,  `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    region : ``VoiceRegion``
        The voice region of the channel.
    topic : `None`, `str`
        The channel's topic.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    order_group: `int` = `2`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('topic',)
    
    
    def __new__(
        cls,
        *,
        bitrate = ...,
        name = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        region = ...,
        user_limit = ...,
        topic = ...,
    ):
        """
        Creates a new guild voice channel metadata from the given parameters.
        
        Parameters
        ----------
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        region : ``VoiceRegion``, `str`, Optional (Keyword only)
            The voice region of the channel.
        user_limit : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the voice channel, or `0` if unlimited.
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
            
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # topic
        if topic is ...:
            topic = None
        else:
            topic = validate_topic(topic)
        
        # Construct
        self = ChannelMetadataGuildVoiceBase.__new__(
            cls,
            bitrate = bitrate,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
            region = region,
            user_limit = user_limit,
        )
        self.topic = topic
        return self
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildVoiceBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            bitrate = keyword_parameters.pop('bitrate', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            region = keyword_parameters.pop('region', ...),
            user_limit = keyword_parameters.pop('user_limit', ...),
            topic = keyword_parameters.pop('topic', ...),
        )
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildVoiceBase.__hash__(self)
        
        # topic
        topic = self.topic
        if (topic is not None):
            hash_value ^= hash(topic)
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildVoiceBase._is_equal_same_type(self, other):
            return False
        
        # topic
        if self.topic != other.topic:
            return False
        
        return True
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._get_display_name)
    def _get_display_name(self):
        return self.name.upper()
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildVoiceBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildStage, cls)._create_empty()
        
        self.topic = None
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase.copy)
    def copy(self):
        new = ChannelMetadataGuildVoiceBase.copy(self)
        new.topic = self.topic
        return new
    
    
    def copy_with(
        self,
        *,
        bitrate = ...,
        name = ...,
        parent_id = ...,
        permission_overwrites = ...,
        position = ...,
        region = ...,
        user_limit = ...,
        topic = ...,
    ):
        """
        Copies the guild voice channel metadata with the given fields.
        
        Parameters
        ----------
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        name : `str`, Optional (Keyword only)
            The channel's name.
        parent_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        permission_overwrites : `None`, `iterable` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        position : `int`, Optional (Keyword only)
            The channel's position.
        region : ``VoiceRegion``, `str`, Optional (Keyword only)
            The voice region of the channel.
        user_limit : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the voice channel, or `0` if unlimited.
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
        # topic
        if topic is ...:
            topic = self.topic
        else:
            topic = validate_topic(topic)
        
        # Construct
        new = ChannelMetadataGuildVoiceBase.copy_with(
            self,
            bitrate = bitrate,
            name = name,
            permission_overwrites = permission_overwrites,
            parent_id = parent_id,
            position = position,
            region = region,
            user_limit = user_limit,
        )
        new.topic = topic
        return new
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            bitrate = keyword_parameters.pop('bitrate', ...),
            name = keyword_parameters.pop('name', ...),
            parent_id = keyword_parameters.pop('parent_id', ...),
            permission_overwrites = keyword_parameters.pop('permission_overwrites', ...),
            position = keyword_parameters.pop('position', ...),
            region = keyword_parameters.pop('region', ...),
            user_limit = keyword_parameters.pop('user_limit', ...),
            topic = keyword_parameters.pop('topic', ...),
        )
    
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildVoiceBase._update_attributes(self, data)
        
        # topic
        self.topic = parse_topic(data)
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildVoiceBase._difference_update_attributes(self, data)
        
        # topic
        topic = parse_topic(data)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildVoiceBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # topic
        put_topic_into(self.topic, data, defaults)
        
        return data
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._get_permissions_for)
    def _get_permissions_for(self, channel_entity, user):
        result = self._get_base_permissions_for(channel_entity, user)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    
    @copy_docs(ChannelMetadataGuildVoiceBase._get_permissions_for_roles)
    def _get_permissions_for_roles(self, channel_entity, roles):
        result = self._get_base_permissions_for_roles(channel_entity, roles)
        if not result & PERMISSION_MASK_VIEW_CHANNEL:
            return PERMISSION_NONE
        
        if not result & PERMISSION_MASK_CONNECT:
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
